"""Forms for the task manager application."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .models import User

from .models import Task


class RegisterForm(UserCreationForm):
    """User registration form."""
    
    class Meta:
        """Meta class for RegisterForm."""
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email required
        self.fields['email'].required = True


class TaskForm(forms.ModelForm):
    """Form for creating and updating tasks."""

    class Meta:
        """Meta class for TaskForm."""
        model = Task
        fields = [
            'assigned_to',
            'title',
            'description',
            'due_date',
            'status',
            'completed_date',
        ]

    def __init__(self, *args, **kwargs):
        """Initialize the form with custom settings."""
        super().__init__(*args, **kwargs)
        
        # Update the queryset for assigned_to to use the custom User model
        from .models import User
        self.fields['assigned_to'].queryset = User.objects.all()
