from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from task_manager.forms import (TaskForm,
                                WorkerForm,
                                WorkerUpdateForm,
                                TaskSearchForm,
                                WorkerSearchForm,
                                SearchForm)
from task_manager.models import Position, TaskType, Task


@login_required
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
@method_decorator(login_required, name='dispatch')
class PositionListView(ListView):
    model = Position
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = SearchForm(
            initial={"name": name,}
        )
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


@method_decorator(login_required, name='dispatch')
class PositionDetailView(DetailView):
    model = Position


@method_decorator(login_required, name='dispatch')
class PositionCreateView(CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


@method_decorator(login_required, name='dispatch')
class PositionUpdateView(UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


@method_decorator(login_required, name='dispatch')
class PositionDeleteView(DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")



"""View classes for TaskType model."""
@method_decorator(login_required, name='dispatch')
class TaskTypeListView(ListView):
    model = TaskType
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = SearchForm(
            initial={"name": name,}
        )
        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


@method_decorator(login_required, name='dispatch')
class TaskTypeDetailView(DetailView):
    model = TaskType


@method_decorator(login_required, name='dispatch')
class TaskTypeCreateView(CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


@method_decorator(login_required, name='dispatch')
class TaskTypeUpdateView(UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


@method_decorator(login_required, name='dispatch')
class TaskTypeDeleteView(DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task-type-list")



"""View classes for TaskType model."""
@method_decorator(login_required, name='dispatch')
class TaskListView(ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        priority = self.request.GET.get("priority", "")
        context["search_form"] = TaskSearchForm(
            initial={"name": name, "priority": priority}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                Q(name__icontains=form.cleaned_data["name"])
                & Q(priority__icontains=form.cleaned_data["priority"])
            )
            if form.cleaned_data["task_type"]:
                queryset = queryset.filter(task_type_id=form.cleaned_data["task_type"])
        return queryset


@method_decorator(login_required, name='dispatch')
class TaskDetailView(DetailView):
    model = Task


@method_decorator(login_required, name='dispatch')
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


@method_decorator(login_required, name='dispatch')
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


@method_decorator(login_required, name='dispatch')
class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")



"""View classes for Worker model."""
@method_decorator(login_required, name='dispatch')
class WorkerListView(ListView):
    model = get_user_model()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("username", "")
        priority = self.request.GET.get("position", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": name, "position": priority}
        )
        return context

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                Q(username__icontains=form.cleaned_data["username"])
            )
            if form.cleaned_data["position"]:
                queryset = queryset.filter(position_id=form.cleaned_data["position"])
        return queryset


@method_decorator(login_required, name='dispatch')
class WorkerDetailView(DetailView):
    model = get_user_model()
    queryset = get_user_model().objects.prefetch_related("tasks")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerDetailView, self).get_context_data(**kwargs)
        context["active_tasks"] = context["worker"].tasks.filter(is_completed=False)
        context["completed_tasks"] = context["worker"].tasks.filter(is_completed=True)
        return context


@method_decorator(login_required, name='dispatch')
class WorkerCreateView(CreateView):
    model = get_user_model()
    form_class = WorkerForm
    success_url = reverse_lazy("task_manager:worker-list")


@method_decorator(login_required, name='dispatch')
class WorkerDeleteView(DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("task_manager:worker-list")


@method_decorator(login_required, name='dispatch')
class WorkerUpdateView(UpdateView):
    model = get_user_model()
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("task_manager:worker-list")
