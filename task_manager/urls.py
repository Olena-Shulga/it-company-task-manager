from django.urls import path

from task_manager.views import index, PositionListView

urlpatterns = [
    path("", index, name="index"),
    path(
        "positions/", PositionListView.as_view(), name="position-list"
    ),

]

app_name = "task_manager"