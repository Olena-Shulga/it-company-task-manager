from django.contrib.auth import get_user_model
from django.test import TestCase
from datetime import date

from task_manager.models import Position, Task, TaskType


class ModelsTests(TestCase):
    def test_position_str(self):
        position = Position.objects.create(
            name="Test",
        )
        self.assertEqual(
            str(position),
            position.name
        )

    def test_task_type_str(self):
        task_type = TaskType.objects.create(
            name="Test type",
        )
        self.assertEqual(str(task_type), task_type.name)

    def test_worker_str(self):
        position = Position.objects.create(
            name="Test position"
        )
        worker = get_user_model().objects.create_user(
            username="Test",
            password="test1234",
            first_name="Test First",
            last_name="Test Last",
            position=position,
        )
        self.assertEqual(
            str(worker),
            f"{worker.username} ({worker.first_name} {worker.last_name})"
        )

    def test_task_str(self):
        task_type = TaskType.objects.create(
            name="Test type",
        )
        task = Task.objects.create(
            name="Test Task",
            description="Test Task Description",
            is_completed=False,
            priority="M",
            task_type=task_type,
            deadline=date.today()
        )
        self.assertEqual(
            str(task),
            task.name
        )
