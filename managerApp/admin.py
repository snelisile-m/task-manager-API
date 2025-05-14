from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone

from .forms import RegisterForm
from .models import Task

User = get_user_model()

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = User
    add_form = RegisterForm

    list_display = ('username', 'email', 'is_staff', 'is_active', 'display_role', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'role', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    list_per_page = 20

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
        ('Role', {
            'fields': ('role',),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'role'),
        }),
    )

    @admin.display(description='Role')
    def display_role(self, obj):
        return obj.get_role_display()

# Unregister existing User admin to avoid duplicate registration
if admin.site.is_registered(User):
    admin.site.unregister(User)

# Task Admin Customisation
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to_display', 'due_date', 'status_column', 'assigned_date', 'task_actions')
    list_filter = ('status', 'assigned_date', 'due_date')
    search_fields = ('title', 'description', 'assigned_to__username')
    list_display_links = ('title',)
    date_hierarchy = 'assigned_date'
    list_per_page = 20

    @admin.display(description='Status', ordering='completed')
    def status_column(self, obj):
        if obj.completed:
            return format_html(
                '<span class="badge bg-success">Completed</span> <small class="text-muted">on {}</small>',
                obj.completed_date.strftime('%Y-%m-%d') if obj.completed_date else 'N/A'
            )
        elif obj.due_date and obj.due_date < timezone.now().date():
            return format_html('<span class="badge bg-danger">Overdue</span>')
        return format_html('<span class="badge bg-warning">Pending</span>')

    @admin.display(description='Assigned To')
    def assigned_to_display(self, obj):
        return obj.assigned_to.get_full_name() or obj.assigned_to.username or str(obj.assigned_to)

    @admin.display(description='Actions')
    def task_actions(self, obj):
        if not obj:
            return ""
        edit_url = reverse('admin:managerApp_task_change', args=[obj.pk])
        delete_url = reverse('admin:managerApp_task_delete', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}">Edit</a> | <a class="button" style="color:red;" href="{}">Delete</a>',
            edit_url, delete_url
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not self._is_admin_user(request.user):
            return qs.filter(assigned_to=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return self._is_admin_user(request.user) or obj.assigned_to == request.user

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return self._is_admin_user(request.user) or obj.assigned_to == request.user

    def get_list_display(self, request):
        display = list(super().get_list_display(request))
        if not self._is_admin_user(request.user) and 'task_actions' in display:
            display.remove('task_actions')
        return display

    def _is_admin_user(self, user):
        # Ensure robustness if .is_admin() is undefined
        return getattr(user, 'is_superuser', False) or getattr(user, 'is_admin', lambda: False)()

# Register the custom models with admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Task, TaskAdmin)
