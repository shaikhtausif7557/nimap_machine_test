from django.test import TestCase
from django.contrib.auth.models import User
from .models import Client, Project

class ClientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client.objects.create(client_name='Test Client', created_by=self.user)

    def test_client_creation(self):
        self.assertEqual(self.client.client_name, 'Test Client')
        self.assertEqual(self.client.created_by.username, 'testuser')

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client.objects.create(client_name='Test Client', created_by=self.user)
        self.project = Project.objects.create(project_name='Test Project', client=self.client, created_by=self.user)

    def test_project_creation(self):
        self.assertEqual(self.project.project_name, 'Test Project')
        self.assertEqual(self.project.client.client_name, 'Test Client')

        
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Client, Project

class ClientAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.client_data = {'client_name': 'New Client'}

    def test_create_client(self):
        response = self.client.post(reverse('client-list'), self.client_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_clients(self):
        Client.objects.create(client_name='Existing Client', created_by=self.user)
        response = self.client.get(reverse('client-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)