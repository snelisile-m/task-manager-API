from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Task

class TaskManagerViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        # Create admin user
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', role=User.Role.ADMIN)
        # Create regular user
        self.regular_user = User.objects.create_user(username='user', password='userpass', role=User.Role.USER)
        # Create a task
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            assigned_to=self.regular_user,
            status=Task.Status.PENDING,
            due_date='2025-05-14'
        )

    def test_task_creation_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('add_task'), {
            'title': 'New Task',
            'description': 'New Description',
            'assigned_to': self.regular_user.id,
            'status': Task.Status.PENDING,
            'due_date': '2025-05-20',
        })
        # Expecting redirect after successful form submission
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_task_creation_non_admin(self):
        self.client.login(username='user', password='userpass')
        response = self.client.post(reverse('add_task'), {
            'title': 'User Task',
            'description': 'User Description',
            'status': Task.Status.PENDING,
            'due_date': '2025-05-20',
        })

        self.assertEqual(response.status_code, 302)

        task = Task.objects.get(title='User Task')
        self.assertEqual(task.assigned_to, self.regular_user)
    
    def test_task_editing(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('edit_task', args=[self.task.id]), {
            'title': 'Updated Task',
            'description': self.task.description,
            'assigned_to': self.task.assigned_to.id,
            'status': self.task.status,
            'due_date': self.task.due_date,
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_task_listing(self):
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
