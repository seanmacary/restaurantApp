from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {"username": "testcase", "password": "strongpassword123", "email": "testcase@example.com"}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_missing_fields(self):
        data = {"username": "testcase", "password": "strongpassword123"}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password!123")

    def test_login(self):
        data = {"username": "example", "password": "Password!123"}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password!123")
        self.client.login(username="example", password="Password!123")

    def test_get_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
