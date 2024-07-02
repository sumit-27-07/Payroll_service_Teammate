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
    path('calculate_total_leave_days/', views.calculate_total_leave_days, name='calculate_total_leave_days'),
    path('add_salary_job_type/', views.add_salary_job_type, name='add_salary_job_type'),
    path('calculate_payroll/', views.calculate_payroll, name='calculate_payroll'),
    path('show_payroll_details/', views.show_payroll_details, name='show_payroll_details'),
]
