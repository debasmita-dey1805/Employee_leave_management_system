from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from leave.models import LeaveRequest
from users.forms import AddEmployeeForm
from .models import Profile

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on role
            if user.profile.role == 'manager':
                return redirect('manager_dashboard')
            elif user.profile.role == 'employee':
                return redirect('employee_dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')



@login_required
def manager_dashboard(request):
    if request.user.profile.role != 'manager':
        return render(request, '403.html', status=403)

    manager_department = request.user.profile.department

    pending_count = LeaveRequest.objects.filter(
        status='pending',
        employee__profile__department=manager_department
    ).count()

    approved_count = LeaveRequest.objects.filter(
        status='approved',
        employee__profile__department=manager_department
    ).count()

    return render(request, 'dashboard/manager_dashboard.html', {
        'pending_leave': pending_count,   # match your template variable names
        'approve_leave': approved_count
    })

   
    


@login_required
def employee_dashboard(request):
    pending_count = LeaveRequest.objects.filter(employee=request.user, status='pending').count()
    approved_count = LeaveRequest.objects.filter(employee=request.user, status='approved').count()
    return render(request, 'dashboard/employee_dashboard.html', {
        'pending_count':pending_count,
        'approved_count':approved_count
    })


def logout_view(request):
    logout(request)
    return redirect('login')




@login_required
def add_employee(request):
    if request.user.profile.role != 'manager':
        messages.error(request, "Only managers can add employees.")
        return redirect('dashboard')

    form = AddEmployeeForm(request.POST or None, manager_department=request.user.profile.department)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully.")
            return redirect('team_members')  

    return render(request, 'dashboard/add_employee.html', {'form': form})