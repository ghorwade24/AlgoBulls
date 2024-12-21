from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import toDoList

class CreateTaskAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='sourabh', password='sourabh123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {
            'todo_name': 'Sample Task'
        }
        self.invalid_payload = {
            'todo_name': ''  # Invalid because todo_name is required
        }

    def test_create_task_success(self):
        response = self.client.post('/api/create_task/', self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['todo_name'], 'Sample Task')

    def test_create_task_failure(self):
        response = self.client.post('/api/create_task/', self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
class UpdateTaskAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.task = toDoList.objects.create(user=self.user, todo_name='Initial Task')
        self.valid_payload = {
            'todo_name': 'Updated Task'
        }

    def test_update_task_success(self):
        response = self.client.put(f'/api/update_task/{self.task.id}/', self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['todo_name'], 'Updated Task')

    def test_update_task_not_found(self):
        response = self.client.put('/api/update_task/9999/', self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UserIntegrationTestCase(APITestCase):
    def test_user_registration_and_login(self):
        # Register a new user
        register_payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'Password': 'password123'
        }
        response = self.client.post('/register/', register_payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "register successfully")
        
        # Login with the registered user
        login_payload = {
            'uname': 'newuser',
            'pass': 'password123'
        }
        response = self.client.post('/login/', login_payload)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/home_page')
class TaskLifecycleIntegrationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_task_lifecycle(self):
        # Create a new task
        create_payload = {'todo_name': 'Test Task'}
        create_response = self.client.post('/api/create_task/', create_payload)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        task_id = create_response.data['id']

        # Update the task
        update_payload = {'todo_name': 'Updated Task'}
        update_response = self.client.put(f'/api/update_task/{task_id}/', update_payload)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['todo_name'], 'Updated Task')

        # Delete the task
        delete_response = self.client.delete(f'/api/delete_task/{task_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
