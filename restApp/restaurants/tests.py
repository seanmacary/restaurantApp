from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, UserToken


class UserRegistrationTestCase(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            "UserName": "testuser",
            "password": "testpassword123",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User"
        }

    def test_valid_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email=self.user_data["email"]).exists())

    def test_invalid_registration_missing_fields(self):
        # Remove the email field from user data
        del self.user_data["email"]
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(CustomUser.objects.filter(UserName=self.user_data["UserName"]).exists())

    def test_invalid_registration_duplicate_email(self):
        # Create a user with the same email
        CustomUser.objects.create_user(
            UserName="existinguser",
            email=self.user_data["email"],
            password="existingpassword"
        )
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTestCase(APITestCase):

    def setUp(self):
        self.login_url = reverse('login')
        self.login_data = {
            'UserName': 'testuser',
            'Password': 'testpassword'
        }
        self.user = CustomUser.objects.create_user(
            UserName='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_valid_login(self):
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_invalid_login(self):
        self.login_data['Password'] = 'wrongpassword'
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid credentials')

    def test_missing_fields(self):
        response = self.client.post(self.login_url, {'UserName': 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Both UserName and Password are required.')
