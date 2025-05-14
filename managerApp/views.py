from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, TaskForm
from .models import Task, User
from django.shortcuts import render, redirect
from .forms import TaskForm
from .models import Task
from django.shortcuts import get_object_or_404

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print('Form is valid')
            login(request, user)
            return redirect('task_list')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


@login_required
def add_task(request):
    user = request.user
    is_admin = user.is_superuser or (hasattr(user, 'role') and user.role == user.Role.ADMIN)

    if request.method == 'POST':
        form = TaskForm(request.POST, user=user)
        if form.is_valid():
            task = form.save(commit=False)

            # Assign task to current user if not admin
            if not is_admin:
                task.assigned_to = user

            task.created_by = user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm(user=user)

    return render(request, 'tasks/add_task.html', {
        'form': form,
        'is_admin': is_admin,  # Pass this to template if needed
    })
# def add_task(request):
#     if request.method == 'POST':
#         form = TaskForm(request.POST, user=request.user)
#         if form.is_valid():
#             task = form.save(commit=False)

#             if request.user.role != request.user.Role.ADMIN:
#                 task.assigned_to = request.user  # Auto-assign
#             task.save()
#             return redirect('task_list')
#     else:
#         form = TaskForm(user=request.user)

#     return render(request, 'tasks/add_task.html', {'form': form})


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
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if not request.user.is_staff:
            form.fields['assigned_to'].required = False

        if form.is_valid():
            task = form.save(commit=False)
            if not request.user.is_staff:
                task.assigned_to = request.user
            task.save()
            return redirect('task_list')

    else:
        form = TaskForm(instance=task)
        if not request.user.is_staff:
            form.fields['assigned_to'].required = False

    return render(request, 'tasks/edit_task.html', {
        'form': form,
        'is_admin': request.user.is_staff,
    })


def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/confirm_delete.html', {'task': task})
