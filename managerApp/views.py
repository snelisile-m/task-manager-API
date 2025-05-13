from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, TaskForm
from .models import Task, User

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            # If the current user is not an admin, assign the task to the current user
            if not request.user.is_admin():
                task.assigned_to = request.user
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
        # If user is admin, show all users in the dropdown
        if request.user.is_admin():
            form.fields['assigned_to'].queryset = User.objects.all()
        else:
            # For non-admin users, hide the assigned_to field since we'll set it to current user
            form.fields['assigned_to'].widget = forms.HiddenInput()
            form.fields['assigned_to'].initial = request.user
    return render(request, 'tasks/add_task.html', {'form': form, 'is_admin': request.user.is_admin()})


@login_required
def task_list(request):
    tasks = Task.objects.all().order_by('due_date')
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'is_admin': request.user.is_admin()
    })


@login_required
def my_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tasks/my_tasks.html', {'tasks': tasks})


def home(request):
    return render(request, 'base/home.html')


def logout_handler(request):
    logout(request)
    return render(request, 'auth/logoutt.html')

@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            # Update the completed status based on the form data
            completed = form.cleaned_data.get('completed', False)
            task.completed = completed
            
            # Update completion date if needed
            if completed and not task.completed_date:
                task.completed_date = timezone.now()
            elif not completed:
                task.completed_date = None
                
            task.save()
            form.save_m2m()  # Save many-to-many data if any
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form})


def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/confirm_delete.html', {'task': task})
