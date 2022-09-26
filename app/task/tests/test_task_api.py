"""
Test task API.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Task
from task.serializers import TaskDetailSerializer, TaskSerializer

TASK_URL = reverse('task:task-list')


def create_task(user, **params):
    """Create and return a task object for use in test cases."""
    defaults = {
        'title': 'Sample task title',
        # 'time_created': datetime.now().strftime("%Y%m%d-%H%M%S"),
        'description': 'Sample description.',
    }
    defaults.update(params)

    task = Task.objects.create(user=user, **defaults)
    return task


def detail_url(task_id):
    """Create and return a recipe detail URL."""
    return reverse('task:task-detail', args=[task_id])


class TestPublicTaskAPI(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required to use API."""
        res = self.client.get(TASK_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateTaskAPI(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='user@example.com', password='securepassword909')
        self.client.force_authenticate(self.user)

    def test_retrieve_tasks(self):
        """Test retrieving a list of tasks."""
        create_task(user=self.user)
        create_task(user=self.user)

        res = self.client.get(TASK_URL)

        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_task_list_limited_to_user(self):
        """Test list of tasks is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(email='other@example.com', password='testpass123')
        create_task(user=other_user)
        create_task(user=self.user)

        res = self.client.get(TASK_URL)

        tasks = Task.objects.filter(user=self.user)
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_task_detail(self):
        """Test get task detail."""
        task = create_task(user=self.user)
        url = detail_url(task.id)
        res = self.client.get(url)

        serializer = TaskDetailSerializer(task)
        self.assertEqual(res.data, serializer.data)

    def test_create_task(self):
        """Test creating a task."""
        payload = {
            'title': 'Sample recipe',
            'description': 'Wash the dishes.',
        }
        res = self.client.post(path=TASK_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(task, k), v)
        self.assertEqual(task.user, self.user)
