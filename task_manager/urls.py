from django.urls import path

from task_manager.views import (index,
                                PositionListView,
                                PositionDetailView,
                                PositionCreateView,
                                PositionUpdateView,
                                TaskTypeListView,
                                PositionDeleteView,
                                TaskTypeDetailView,
                                TaskTypeCreateView,
                                TaskTypeUpdateView,
                                TaskTypeDeleteView,
                                TaskListView,
                                TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView,
                                )


urlpatterns = [
    path("", index, name="index"),
    path(
        "positions/", PositionListView.as_view(), name="position-list"
    ),
    path(
        "positions/<int:pk>/",
        PositionDetailView.as_view(),
        name="position-detail"
    ),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path(
        "positions/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update"
    ),

    path(
        "positions/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete"
    ),

    path(
        "task_types/",
        TaskTypeListView.as_view(),
        name="task-type-list"
    ),
    path(
        "task_types/<int:pk>/",
        TaskTypeDetailView.as_view(),
        name="task-type-detail"
    ),
    path(
        "task_types/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create"
    ),
    path(
        "task_types/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update"
    ),
    path(
        "task_types/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete"
    ),

    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list"
    ),
    path(
        "tasks/<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "tasks/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
]

app_name = "task_manager"