import json
from django.shortcuts import render, redirect
from .models import Board, Task
from home.form import TaskForm, BoardForm, RegisterForm
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

def register_user(request):
    formregister = RegisterForm()
    if request.method == 'POST':
        formregister = RegisterForm(request.POST)
        if formregister.is_valid():
            formregister.save()
            return JsonResponse({'success': 'User created successfully'})
        else:
            return JsonResponse({'error': formregister.errors})
    else:
        formregister = RegisterForm()
    
    context = {
        'RegisterForm': formregister
    }
    return render(request, 'register.html', context)

def home_view(request):
    tasks_not_started = Task.objects.filter(status='not_started').order_by('-board__created')
    tasks_in_progress = Task.objects.filter(status='in_progress').order_by('-board__created')
    tasks_completed = Task.objects.filter(status='completed').order_by('-board__created')
    board = Board.objects.prefetch_related('Task').order_by('-created')

    context = {
        'tasks_not_started': tasks_not_started,
        'tasks_in_progress': tasks_in_progress,
        'tasks_completed': tasks_completed,
        'board': board
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
        'TaskForm': form,
        'BoardForm': formboard,
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
        'BoardForm': board        
    }
    return render(request, 'delete.html', context)

def statistics_view(request):
    tasks_not_started = Task.objects.filter(status='not_started')
    tasks_in_progress = Task.objects.filter(status='in_progress')
    tasks_completed = Task.objects.filter(status='completed')
    
    context = {
        'tasks_not_started': tasks_not_started,
        'tasks_in_progress': tasks_in_progress,
        'tasks_completed': tasks_completed,
        'tasks_total': Task.objects.all(),
    }
    return render(request, 'statistics.html', context)

@require_http_methods(["POST"])
def update_task_status(request):
    data = json.loads(request.body)
    task_id = data.get('taskId')
    new_status = data.get('status')
    
    try:
        task = Task.objects.get(id=task_id)
        task.status = new_status
        task.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Task status updated successfully'
        })
    except Task.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Task not found'
        }, status=404)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('home')
