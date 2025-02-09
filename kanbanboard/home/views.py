from django.shortcuts import render, redirect
from .models import Board, Task
from django.template.loader import get_template
from home.form import TaskForm, BoardForm
from django.http import JsonResponse


def home_view(request):
    tasks_not_started = Task.objects.filter(status ='not_started').order_by('-board__created')
    tasks_in_progress = Task.objects.filter(status = 'in_progress').order_by('-board__created')
    tasks_completed = Task.objects.filter(status = 'completed').order_by('-board__created')
    board = Board.objects.prefetch_related('Task').order_by('-created')


    context ={
        'tasks_not_started': tasks_not_started,
        'tasks_in_progress': tasks_in_progress,
        'tasks_completed': tasks_completed,
        'board' : board
    }
    return render(request, 'home.html', context)

def addtask(request):
    form = TaskForm()
    formboard = BoardForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        formboard = BoardForm(request.POST)
        if formboard.is_valid():
            formboard.save()
            return redirect('addtask')

        elif form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'TaskForm':form,
        'BoardForm' : formboard,
    }
    return render(request, 'form.html', context)

def updatetask(request, pk):
    task = Task.objects.get(id=pk)
    board = task.board 

    if request.method == 'POST':
        formtask = TaskForm(request.POST, instance=task)
        formboard = BoardForm(request.POST, instance=board)

        if formtask.is_valid():
            formtask.save()
            return redirect('home')

        if formboard.is_valid():
            formboard.save()
            return redirect('home')

    else:
        formtask = TaskForm(instance=task)
        formboard = BoardForm(instance=board)

    context = {
        'TaskForm': formtask,    
        'BoardForm': formboard
    }
    return render(request, 'form.html', context)

def deletetask(request, pk):
    task = Task.objects.get(id=pk)
    board = task.board 
    if request.method == 'POST':
        task.delete()
    if request.method == 'POST':
        board.delete()
        return redirect('home')
    context ={
        'TaskForm': task,
        'BoardForm':board        
    }
    return render(request, 'delete.html', context)