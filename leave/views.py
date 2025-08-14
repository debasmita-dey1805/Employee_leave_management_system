from datetime import timedelta
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from leave.models import LeaveRequest
from .forms import LeaveRequestForm

from django.utils.dateformat import DateFormat
from django.contrib.auth.models import User
from users.models import Profile

# Create your views here.
@login_required
def apply_leave(request):
    if request.user.profile.role != 'employee':
        messages.error(request, "Only employees can apply for leave.")
        return redirect('home')
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            messages.success(request, "Leave application submitted successfully.")
            return redirect('employee_dashboard')  
    else:
        form = LeaveRequestForm()
    
    return render(request, 'dashboard/apply_leave.html', {'form': form})

@login_required
def my_leaves(request):
    leaves = LeaveRequest.objects.filter(employee=request.user).order_by('-created_at')
    context = {
        'leaves': leaves
    }
    return render(request, 'dashboard/my_leaves.html', context)


@login_required
def leave_calendar(request):    
    return render(request, 'dashboard/leave_calendar.html')

@login_required
def leave_events(request):
    leaves = LeaveRequest.objects.filter(status='approved', employee=request.user)

    events = []
    for leave in leaves:
        events.append({
            'title': f"{leave.employee.username} - {leave.get_leave_type_display()}",
            'start': leave.start_date.strftime("%Y-%m-%d"),
            'end': (leave.end_date + timedelta(days=1)).strftime("%Y-%m-%d"),  
            'color': 'green'
        })
    return JsonResponse(events, safe=False)


#pending request for manager


@login_required
def pending_leaves(request):
    if request.user.profile.role != 'manager':
        return render(request, '403.html', status=403)

    manager_department = request.user.profile.department

    leaves = LeaveRequest.objects.filter(
        status='pending',
        employee__profile__department=manager_department
    )

    return render(request, 'dashboard/pending_leaves.html', {'leaves': leaves})


@login_required
def approve_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = 'approved'
    leave.save()
    messages.success(request, "Leave approved successfully.")
    return redirect('pending_leaves')

@login_required
def reject_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = 'rejected'
    leave.save()
    messages.error(request, "Leave rejected successfully.")
    return redirect('pending_leaves')


@login_required
def team_members(request):
    # Ensure only managers can see this
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'manager':
        return render(request, '403.html', status=403)

    manager_department = request.user.profile.department  

    # Get all employees in same department as the manager
    employees = User.objects.filter(
        profile__department=manager_department,
        profile__role='employee'
    ).select_related('profile').order_by('first_name')

    return render(request, 'dashboard/team_members.html', {
        'employees': employees,
        'department_name': manager_department.name if manager_department else 'No Department'
    })


# calenar for manager
@login_required
def manager_leave_calendar(request):
    return render(request, 'dashboard/manager_leave_calendar.html')

@login_required
def manager_leave_events(request):
    try:
        department = request.user.profile.department
    except Profile.DoesNotExist:
        return JsonResponse([], safe=False)  

    employees_in_dept = (
        Profile.objects
        .filter(department=department, role='employee')
        .values_list('user', flat=True)
    )

    leaves = LeaveRequest.objects.filter(status='approved', employee_id__in=employees_in_dept)

    events = []
    for leave in leaves:
        events.append({
            'title': f"{leave.employee.get_full_name() or leave.employee.username} - {leave.get_leave_type_display()}",
            'start': leave.start_date.strftime("%Y-%m-%d"),
            'end': (leave.end_date + timedelta(days=1)).strftime("%Y-%m-%d"),  
            'color': 'green'
        })

    return JsonResponse(events, safe=False)