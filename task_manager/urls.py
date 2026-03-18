from django.urls import path

from task_manager.views import index, PositionListView, PositionDetailView, PositionCreateView, PositionUpdateView, \
    TaskTypeListView, PositionDeleteView

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
]

app_name = "task_manager"