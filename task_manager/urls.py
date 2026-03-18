from django.urls import path

from task_manager.views import index, PositionListView, PositionDetailView, PositionCreateView

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


]

app_name = "task_manager"