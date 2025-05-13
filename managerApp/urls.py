from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('add/', views.add_task, name='add_task'),
    path('tasks/', views.task_list, name='task_list'),
    path('my_tasks/', views.my_tasks, name='my_tasks'),
    path('logout/', views.logout_handler, name='logout'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('', views.home, name='home'),
]