from django.urls import path
from . import views

urlpatterns = [
    path('employee/apply/', views.apply_leave, name='apply_leave'),
    path('employee/my_leaves/', views.my_leaves, name='my_leaves'),

    path('employee/calendar/', views.leave_calendar, name='leave_calendar'),
    path('employee/calendar/events/', views.leave_events, name='leave_events'),

    path('manager/pending-leaves/', views.pending_leaves, name='pending_leaves'),
    path('manager/approve-leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('manager/reject-leave/<int:leave_id>/', views.reject_leave, name='reject_leave'),

    path('manager/team-members/', views.team_members, name='team_members'),

    path('manager/calendar/', views.manager_leave_calendar, name='manager_leave_calendar'),
    path('manager/calendar/events/', views.manager_leave_events, name='manager_leave_events'),


]