from django.test import TestCase
from managerApp.models import User, Task
from api.serializers import TaskSerializer
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from datetime import date  # Import date from datetime

class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass'))

class TaskModelTests(TestCase):
    def test_create_task(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        task = Task.objects.create(title='Test Task', assigned_to=user, due_date=date.today())
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.assigned_to, user)



class TaskSerializerTests(TestCase):
    def test_serialize_task(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        task = Task.objects.create(title='Test Task', assigned_to=user, due_date=date.today())
        serializer = TaskSerializer(task)
        self.assertEqual(serializer.data['title'], 'Test Task')

class TaskViewTests(APITestCase):
    # def setUp(self):
    #     self.user = User.objects.create_user(username='testuser', password='testpass', role=User.Role.USER)
    #     self.client.login(username='testuser', password='testpass')
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', role=User.Role.ADMIN)
        # Obtain JWT token
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpass'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)  # Set the token in the headers

    def test_view_my_tasks(self):
        # Create a task for the user
        Task.objects.create(title='Test Task', assigned_to=self.user, due_date=date.today())

        # View tasks
        url = reverse('my-tasks')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task')
        self.assertEqual(response.data[0]['due_date'], str(date.today()))

    def test_create_task(self):
        url = reverse('task-list')
        data = {'title': 'New Task', 'assigned_to': self.user.id, 'due_date': str(date.today()), 'description': 'This is a test task description.'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'New Task')
        self.assertEqual(Task.objects.get().due_date, date.today())