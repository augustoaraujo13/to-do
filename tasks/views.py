from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import task
from .forms import TaskForm


def taskList(request):
    # faz um select na tabela tasks.
    tasks = task.objects.all().order_by('-created')
    return render(request, 'tasks/list.html', {'tasks': tasks})


def taskView(request, id):
    task1 = get_object_or_404(task, pk=id)
    return render(request, 'tasks/task.html', {'task': task1})


def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'doing'
            task.save()
            return redirect('/')
    else:
        form = TaskForm()
        return render(request, 'tasks/addtask.html', {'form': form})



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


def helloWorld(request):
    return HttpResponse('Hello World!')


def yourName(request, name):
    return render(request, 'tasks/yourname.html', {'name': name})
