from django.urls import path

from task_manager.views import index, PositionListView, PositionDetailView

urlpatterns = [
    path("", index, name="index"),
    path(
        "positions/", PositionListView.as_view(), name="position-list"
    ),
    path(
        "positions/<int:pk>/",
        PositionDetailView.as_view(),
        name="position-view"
    ),

]

app_name = "task_manager"