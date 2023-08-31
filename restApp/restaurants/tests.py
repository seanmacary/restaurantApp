from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
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

        # Check if token key is present in the response data
        self.assertIn('token', response.data)

        # Optionally, check if the token value is valid (i.e., not empty)
        self.assertTrue(response.data['token'])


class ProfileTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password!123")
        self.client.login(username="example", password="Password!123")

    def test_get_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)


class LogoutTestCase(APITestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        # Authenticate the user
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_logout(self):
        # Ensure user is authenticated
        self.assertTrue(Token.objects.filter(key=self.token.key).exists())

        # Make a request to the logout endpoint
        response = self.client.post(reverse('logout'))

        # Check that the response indicates success
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the token is deleted, thus logging the user out
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())
