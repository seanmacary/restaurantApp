from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"username": "testcase", "password": "strongpassword123", "email": "testcase@example.com"}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password!123")

    def test_login(self):
        data = {"username": "example", "password": "Password!123"}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ... Add more tests for other views