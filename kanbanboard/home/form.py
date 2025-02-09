from django.forms import ModelForm
from home.models import Board, Task
from django import forms

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
