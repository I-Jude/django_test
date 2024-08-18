from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Employee
from .forms import EmployeeForm
from .forms import RegisterForm  , LoginForm
from django.shortcuts import render, redirect, get_object_or_404

def home_view(request):
    return render(request, 'employee/home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            print("Login successful")
            return redirect('employee_list')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = LoginForm()
    
    return render(request, 'employee/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  # Redirect to login or another page
    else:
        form = RegisterForm()
    
    return render(request, 'employee/register.html', {'form': form})
@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee/employee_list.html', {'employees': employees})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_employees(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    employees = Employee.objects.all()
    return render(request, 'employee/manage_employees.html', {'form': form, 'employees': employees})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_employee(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    employee.delete()
    return redirect('employee_list')

@login_required
def add_employee(request):
    if request.user.username != 'admin':
        return redirect('login')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = RegisterForm()
    
    return render(request, 'employee/add_employee.html', {'form': form})

@login_required
def edit_employee(request, pk):
    if request.user.username != 'admin':
        return redirect('login')
    
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = RegisterForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = RegisterForm(instance=employee)
    
    return render(request, 'employee/edit_employee.html', {'form': form})

@login_required
def delete_employee(request, pk):
    if request.user.username != 'admin':
        return redirect('login')
    
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    
    return render(request, 'employee/delete_employee.html', {'employee': employee})
