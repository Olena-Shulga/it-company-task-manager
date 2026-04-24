from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position

POSITION_URL = reverse("task_manager:position-list")
POSITION_CREATE_URL = reverse("task_manager:position-create")


class PublicPositionTests(TestCase):
    def test_login_required(self):
        res = self.client.get(POSITION_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivatePositionTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.position = Position.objects.create(name="Admin")
        Position.objects.create(name="Developer")
        Position.objects.create(name="Designer")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            position=PrivatePositionTests.position,
        )
        self.client.force_login(self.user)

    def test_retrieve_positions(self):
        response = self.client.get(POSITION_URL)
        self.assertEqual(response.status_code, 200)
        positions = Position.objects.all()
        self.assertEqual(
            list(response.context["position_list"]),
            list(positions)
        )
        self.assertEqual(len(response.context["position_list"]), 3)
        self.assertTemplateUsed(response, "task_manager/position_list.html")

    def test_position_search_with_results(self):
        query_params = {"name": "De"}
        response = self.client.get(POSITION_URL, query_params=query_params)
        self.assertEqual(response.status_code, 200)
        positions = Position.objects.all()
        self.assertEqual(
            list(response.context["position_list"]),
            list(positions.filter(name__icontains=query_params["name"]))
        )

    def test_position_search_without_results(self):
        query_params = {"name": "Boss"}
        response = self.client.get(POSITION_URL, query_params=query_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]),
            []
        )

    def test_position_create_successful(self):
        response = self.client.post(
            POSITION_CREATE_URL,
            data={
                "name": "Test Position",
            }
        )
        self.assertRedirects(response, reverse("task_manager:position-list"))
