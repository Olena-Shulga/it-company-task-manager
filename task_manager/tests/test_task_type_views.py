from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import TaskType, Position

TASK_TYPE_URL = reverse("task_manager:task-type-list")
TASK_TYPE_CREATE_URL = reverse("task_manager:task-type-create")


class PublicTaskTypeTests(TestCase):
    def test_login_required(self):
        res = self.client.get(TASK_TYPE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTypeTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        TaskType.objects.create(name="Add feature")
        TaskType.objects.create(name="Delete")
        TaskType.objects.create(name="Update")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            position=Position.objects.create(name="Boss"),
        )
        self.client.force_login(self.user)

    def test_retrieve_task_types(self):
        response = self.client.get(TASK_TYPE_URL)
        self.assertEqual(response.status_code, 200)
        task_types = TaskType.objects.all()
        self.assertEqual(
            list(response.context["tasktype_list"]),
            list(task_types)
        )
        self.assertEqual(len(response.context["tasktype_list"]), 3)
        self.assertTemplateUsed(response, "task_manager/tasktype_list.html")

    def test_task_type_search_with_results(self):
        query_params = {"name": "e"}
        response = self.client.get(TASK_TYPE_URL, query_params=query_params)
        self.assertEqual(response.status_code, 200)
        task_types = TaskType.objects.all()
        self.assertEqual(
            list(response.context["tasktype_list"]),
            list(task_types.filter(name__icontains=query_params["name"]))
        )

    def test_task_type_search_without_results(self):
        query_params = {"name": "Non-existent type"}
        response = self.client.get(TASK_TYPE_URL, query_params=query_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["tasktype_list"]),
            []
        )

    def test_task_type_create_successful(self):
        response = self.client.post(
            TASK_TYPE_CREATE_URL,
            data={
                "name": "Test TaskType",
            }
        )
        self.assertRedirects(response, reverse("task_manager:task-type-list"))
