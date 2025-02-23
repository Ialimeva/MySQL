from django.forms import ModelForm
from home.models import Board, Task
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['board', 'title', 'description', 'date_start', 'date_end', 'status']
        widgets = {
            'date_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = '__all__'
