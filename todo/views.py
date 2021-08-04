from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from todo.forms import TodoForm
from todo.models import Todo


def home(request):
    return render(request, 'todo/home.html')


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todo/signup_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_tasks')
            except IntegrityError:
                return render(request, 'todo/signup_user.html',
                              {'form': UserCreationForm(),
                               'error': 'Это имя пользователя уже используется! Пожалуйста, '
                                        'введите новое имя'})
        else:
            return render(request, 'todo/signup_user.html',
                          {'form': UserCreationForm(), 'error': 'Пароли не совпадают!'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login_user.html',
                          {'form': AuthenticationForm(), 'error': 'Неверный логин/пароль'})
        else:
            login(request, user)
            return redirect('current_tasks')


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/create_task.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('current_tasks')
        except ValueError:
            return render(request, 'todo/create_task.html', {'form': TodoForm(), 'error': 'Переданы неверные данные'})


@login_required
def current_tasks(request):
    todos = Todo.objects.filter(user=request.user, completedAt__isnull=True)
    return render(request, 'todo/current_tasks.html', {'todos': todos})


@login_required
def completed_tasks(request):
    todos = Todo.objects.filter(user=request.user, completedAt__isnull=False).order_by('-completedAt')
    return render(request, 'todo/completed_tasks.html', {'todos': todos})


@login_required
def view_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/view_todo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_tasks')
        except ValueError:
            return render(request, 'todo/view_todo.html',
                          {'todo': todo, 'form': form, 'error': 'Плохую инфу даешь! Вводи правильно'})


@login_required
def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completedAt = timezone.now()
        todo.save()
        return redirect('current_tasks')
    else:
        pass


@login_required
def delete_task(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_tasks')
    else:
        pass
