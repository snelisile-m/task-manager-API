from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from .forms import RegisterForm
from .models import Task

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = User
    add_form = RegisterForm
    list_display = ('username', 'email', 'is_staff', 'is_active', 'get_role_display', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'role', 'is_superuser')
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
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'role')
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    list_per_page = 20
    
    def get_role_display(self, obj):
        return obj.get_role_display()
    get_role_display.short_description = 'Role'

# Unregister any existing User model if it's already registered
if admin.site.is_registered(User):
    admin.site.unregister(User)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to_display', 'due_date', 'status_column', 'assigned_date', 'task_actions')
    list_filter = ('status', 'assigned_date', 'due_date')
    search_fields = ('title', 'description', 'assigned_to__username')
    list_per_page = 20
    date_hierarchy = 'assigned_date'
    list_display_links = ('title',)
    
    def status_column(self, obj):
        if obj.completed:
            return format_html(
                '<span class="badge bg-success">Completed</span> <small class="text-muted">on {}</small>',
                obj.completed_date.strftime('%Y-%m-%d') if obj.completed_date else 'N/A'
            )
        elif obj.due_date < timezone.now().date():
            return format_html('<span class="badge bg-danger">Overdue</span>')
        else:
            return format_html('<span class="badge bg-warning">Pending</span>')
    status_column.short_description = 'Status'
    status_column.admin_order_field = 'completed'
    
    def assigned_to_display(self, obj):
        return obj.assigned_to.get_full_name() or obj.assigned_to.username
    assigned_to_display.short_description = 'Assigned To'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and not request.user.is_admin():
            return qs.filter(assigned_to=request.user)
        return qs
    
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser or request.user.is_admin() or obj.assigned_to == request.user
    
    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser or request.user.is_admin() or obj.assigned_to == request.user
    
    def task_actions(self, obj):
        if not obj:
            return ""
        
        edit_url = reverse('admin:managerApp_task_change', args=[obj.id])
        delete_url = reverse('admin:managerApp_task_delete', args=[obj.id])
        
        return format_html(
            '<a href="{}" class="button">Edit</a> | <a href="{}" class="button" style="color:red;">Delete</a>',
            edit_url, delete_url
        )
    task_actions.short_description = 'Actions'
    task_actions.allow_tags = True
    
    def get_list_display(self, request):
        default_list_display = list(self.list_display)
        if not (request.user.is_superuser or request.user.is_admin()):
            # Remove the task_actions column for non-admin users
            if 'task_actions' in default_list_display:
                default_list_display.remove('task_actions')
        return default_list_display

# Register the custom User model with the admin site
admin.site.register(User, CustomUserAdmin)
admin.site.register(Task, TaskAdmin)
