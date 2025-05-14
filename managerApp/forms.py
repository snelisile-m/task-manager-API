# from django import forms
# from .models import Task, User


# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import User

# class RegisterForm(UserCreationForm):
#     """User registration form."""
    
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['email'].required = True


# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ['title', 'description', 'assigned_to', 'status', 'due_date']

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)

#         if user is not None:
#             # Use a safer check for admin depending on how your roles are defined
#             is_admin = getattr(user, 'role', None) == getattr(user, 'Role', {}).ADMIN or user.is_staff

#             if not is_admin:
#                 # Hide the field entirely for non-admins
#                 self.fields.pop('assigned_to')
#             else:
#                 # Optionally: limit choices to active users or staff
#                 self.fields['assigned_to'].queryset = User.objects.all()
from django import forms
from .models import Task, User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """User registration form."""
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'status', 'due_date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Safely extract the user if provided
        super().__init__(*args, **kwargs)

        if user:
            # Handle is_admin check robustly
            role = getattr(user, 'role', None)
            role_class = getattr(user, 'Role', None)
            is_admin = user.is_superuser or (role_class and role == role_class.ADMIN)

            if not is_admin:
                self.fields.pop('assigned_to', None)
            else:
                # Optional: filter to active users only
                self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)
