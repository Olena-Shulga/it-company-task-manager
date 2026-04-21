from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Task, TaskType, Position

TASK_URL = reverse("task_manager:task-list")
TASK_CREATE_URL = reverse("task_manager:task-create")


class PublicTaskTests(TestCase):
    def test_login_required(self):
        res = self.client.get(TASK_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        today = date.today()
        cls.task_type1 = TaskType.objects.create(name="Test TaskType1")
        cls.task_type2 = TaskType.objects.create(name="Test TaskType2")
        Task.objects.create(
            name="Add search function",
            description="Add search function",
            task_type=cls.task_type1,
            deadline= today + timedelta(days=1),
            priority="U",
        )
        Task.objects.create(
            name="Delete search function",
            description="Add search function",
            task_type=cls.task_type1,
            deadline=today + timedelta(days=4),
        )
        Task.objects.create(
            name="Update search function",
            description="Add search function",
            task_type=cls.task_type2,
            deadline=today + timedelta(days=1)
        )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            position=Position.objects.create(name="Boss"),
        )
        self.client.force_login(self.user)

    def test_retrieve_tasks(self):
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks)
        )
        self.assertEqual(len(response.context["task_list"]), 3)
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_task_search_with_results(self):
        query_params = {
            "name": "search",
            "priority": "M",
            "task_type": PrivateTaskTests.task_type2.id,
        }
        response = self.client.get(TASK_URL, query_params=query_params)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks.filter(
                Q(name__icontains=query_params["name"])
                & Q(priority__icontains=query_params["priority"])
                & Q(task_type_id=query_params["task_type"])
            ))
        )

    def test_task_search_without_results(self):
        query_params = {"name": "Non-existent task"}
        response = self.client.get(TASK_URL, query_params=query_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            []
        )
