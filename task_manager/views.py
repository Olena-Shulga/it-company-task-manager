from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from task_manager.models import Position, TaskType, Task


def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""

    num_workers = get_user_model().objects.count()
    num_positions = Position.objects.count()
    num_task_types = TaskType.objects.count()
    num_tasks = Task.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_positions": num_positions,
        "num_task_types": num_task_types,
        "num_tasks": num_tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "task_manager/index.html", context=context)


"""View classes for Position model."""
class PositionListView(ListView):
    model = Position


class PositionDetailView(DetailView):
    model = Position


class PositionCreateView(CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionUpdateView(UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


"""View classes for TaskType model."""
class TaskTypeListView(ListView):
    model = TaskType


class TaskTypeDetailView(DetailView):
    model = TaskType


class TaskTypeCreateView(CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeUpdateView(UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task-type-list")