from django.contrib.auth import get_user_model
from django.db.models import Q
from django.test import TestCase
from django.urls import reverse
from task_manager.models import Position

WORKER_URL = reverse("task_manager:worker-list")
WORKER_CREATE_URL = reverse("task_manager:worker-create")


class PublicWorkerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(WORKER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateWorkerTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.position1 = Position.objects.create(
            name="Position1"
        )
        position2 = Position.objects.create(
            name="Position2"
        )
        get_user_model().objects.create_user(
            username="user1",
            password="test123",
            position=cls.position1,
        )
        get_user_model().objects.create_user(
            username="user2",
            password="test123",
            position=cls.position1,
        )
        get_user_model().objects.create_user(
            username="user3",
            password="test123",
            position=position2,
        )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            position = PrivateWorkerTests.position1,
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(WORKER_URL)
        self.assertEqual(response.status_code, 200)
        workers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["worker_list"]),
            list(workers)
        )
        self.assertTemplateUsed(response, "task_manager/worker_list.html")

    def test_worker_search_with_results(self):
        query_params = {
            "username": "1",
            "position": PrivateWorkerTests.position1.id
        }
        response = self.client.get(WORKER_URL, query_params=query_params)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["worker_list"]),
            list(drivers.filter(
                Q(username__icontains=query_params["username"])
                & Q(position_id=query_params["position"])
            ))
        )

    def test_driver_search_without_results(self):
        query_params = {"username": "No results"}
        response = self.client.get(WORKER_URL, query_params=query_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["worker_list"]),
            []
        )
