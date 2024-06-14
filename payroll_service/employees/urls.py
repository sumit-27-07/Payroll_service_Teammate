from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/employee/', views.signup_employee, name='signup_employee'),
    path('signup/hr/', views.signup_hr, name='signup_hr'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('show_employees/', views.show_employees, name='show_employees'),
    path('change_employee_status/<int:employee_id>/', views.change_employee_status, name='change_employee_status'),
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('show_leave_requests/', views.show_leave_requests, name='show_leave_requests'),
    path('manage_leave_request/<int:leave_id>/<str:decision>/', views.manage_leave_request, name='manage_leave_request'),
]
