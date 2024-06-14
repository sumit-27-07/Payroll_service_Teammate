from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserForm, EmployeeForm, HRForm, LeaveForm
from .models import Employee, HR, Leave

def signup_employee(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        employee_form = EmployeeForm(request.POST)
        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()
            login(request, user)
            return redirect('dashboard')
    else:
        user_form = UserForm()
        employee_form = EmployeeForm()
    return render(request, 'signup_employee.html', {'user_form': user_form, 'employee_form': employee_form})

def signup_hr(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        hr_form = HRForm(request.POST)
        if user_form.is_valid() and hr_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            hr = hr_form.save(commit=False)
            hr.user = user
            hr.save()
            login(request, user)
            return redirect('dashboard')
    else:
        user_form = UserForm()
        hr_form = HRForm()
    return render(request, 'signup_hr.html', {'user_form': user_form, 'hr_form': hr_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if hasattr(request.user, 'employee'):
        return redirect('employee_dashboard')
    elif hasattr(request.user, 'hr'):
        return render(request, 'hr_dashboard.html')

@login_required
def employee_dashboard(request):
    if hasattr(request.user, 'employee'):
        leave_requests = Leave.objects.filter(employee=request.user.employee)
        return render(request, 'employee_dashboard.html', {'leave_requests': leave_requests})
    return redirect('dashboard')

@login_required
def show_employees(request):
    if hasattr(request.user, 'hr'):
        employees = Employee.objects.filter(hr=request.user.hr)
        return render(request, 'show_employees.html', {'employees': employees})
    return redirect('dashboard')

@login_required
def change_employee_status(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.user.hr == employee.hr:
        if employee.status == 'inactive':
            employee.status = 'active'
        else:
            employee.status = 'inactive'
        employee.save()
    return redirect('show_employees')

@login_required
def apply_leave(request):
    if request.method == 'POST':
        leave_form = LeaveForm(request.POST)
        if leave_form.is_valid():
            leave = leave_form.save(commit=False)
            leave.employee = request.user.employee
            leave.save()
            return redirect('employee_dashboard')
    else:
        leave_form = LeaveForm()
    return render(request, 'apply_leave.html', {'leave_form': leave_form})

@login_required
def show_leave_requests(request):
    if hasattr(request.user, 'hr'):
        leave_requests = Leave.objects.filter(employee__hr=request.user.hr)
        return render(request, 'show_leave_requests.html', {'leave_requests': leave_requests})
    return redirect('dashboard')

@login_required
def manage_leave_request(request, leave_id, decision):
    leave_request = get_object_or_404(Leave, id=leave_id)
    if request.user.hr == leave_request.employee.hr:
        if decision == 'approve':
            leave_request.status = 'approved'
        elif decision == 'reject':
            leave_request.status = 'rejected'
        leave_request.save()
    return redirect('show_leave_requests')



def home(request):
    return render(request, 'home.html')
