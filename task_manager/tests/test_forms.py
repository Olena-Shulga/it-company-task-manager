from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.forms import TaskForm
from task_manager.models import TaskType, Position


class TestTaskForm(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Test Position",
        )
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="test123",
            position=self.position,
        )
        self.task_type = TaskType.objects.create(
            name="Task Type number 1",
        )
        self.data = {
            "name": "Test Task",
            "description": "Test Task Description",
            "is_completed": False,
            "priority": "M",
            "assignees": [self.user],
            "task_type": self.task_type,
        }


    def test_task_form_deadline_is_valid(self):
        new_date = date.today() + timedelta(days=1)
        self.data["deadline"] = new_date
        form = TaskForm(
            self.data
        )
        self.assertTrue(form.is_valid())

    def test_task_form_deadline_is_invalid(self):
        new_date = date.today() - timedelta(days=5)
        self.data["deadline"] = new_date
        form = TaskForm(
            self.data
        )
        self.assertFalse(form.is_valid())
