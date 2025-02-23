from django.db import models
from django.utils.timezone import timezone

class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    username = models.CharField(max_length = 50)
    password1 = models.CharField(max_length = 125)
    password2 = models.CharField(max_length = 125)
    
    def __str__(self):
        return self.username

class Board(models.Model):
    name = models.CharField(max_length = 50)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.name
    

class Task(models.Model):
    status_option = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    board = models.ForeignKey(Board, related_name = 'task', on_delete = models.CASCADE)
    title = models.CharField(max_length = 50)
    description = models.TextField(blank = True, null = True )
    date_start = models.DateTimeField(verbose_name='Start Date')
    date_end = models.DateTimeField(verbose_name='End Date')
    status = models.CharField(max_length= 20, choices = status_option, default = 'not_started')

    class Meta:
        ordering = ['-board__created']

    def __str__(self):
        return self.title
    




