from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import task
from .forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
import datetime


@login_required
def taskList(request):
    # faz um select na tabela tasks.

    search = request.GET.get('search')
    filter = request.GET.get('filter')
    tasksDoneRecently = task.objects.filter(
        done='done', updated__gt=datetime.datetime.now()-datetime.timedelta(days=30)).count()
    tasksDone = task.objects.filter(done='done', user=request.user).count()
    tasksDoing = task.objects.filter(done='doing', user=request.user).count()

    if search:
        task1 = task.objects.filter(title__icontains=search, user=request.user)

    elif filter:
        task1 = task.objects.filter(done=filter, user=request.user)

    else:
        tasks_list = task.objects.all().order_by('-created').filter(user=request.user)
        paginator1 = Paginator(tasks_list, 5)
        page = request.GET.get('page')
        task1 = paginator1.get_page(page)

    return render(request, 'tasks/list.html', {'tasks': task1, 
    'tasksrecently': tasksDoneRecently, 'tasksdone': tasksDone, 
    'tasksdoing': tasksDoing})


@login_required
def taskView(request, id):
    task1 = get_object_or_404(task, pk=id)
    return render(request, 'tasks/task.html', {'task': task1})


@login_required
def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'doing'
            task.user = request.user
            task.save()
            return redirect('/')
    else:
        form = TaskForm()
        return render(request, 'tasks/addtask.html', {'form': form})


@login_required
def editTask(request, id):
    task1 = get_object_or_404(task, pk=id)
    form = TaskForm(instance=task1)

    if(request.method == 'POST'):
        form = TaskForm(request.POST, instance=task1)

        if (form.is_valid()):
            task1.save()
            return redirect('/')
        else:
            return render(request, 'task/edittask.html', {'form': form, 'task': task1})
    else:
        return render(request, 'tasks/edittask.html', {'form': form, 'task': task1})


@login_required
def deleteTask(request, id):
    task1 = get_object_or_404(task, pk=id)
    task1.delete()
    messages.info(request, 'Tarefa deletada com sucesso.')
    return redirect('/')


@login_required
def changeStatus(request, id):
    task1 = get_object_or_404(task, pk=id)

    if(task1.done == 'doing'):
        task1.done = 'done'
    else:
        task1.done = 'doing'

    task1.save()

    return redirect('/')


@login_required
def helloWorld(request):
    return HttpResponse('Hello World!')


@login_required
def yourName(request, name):
    return render(request, 'tasks/yourname.html', {'name': name})
