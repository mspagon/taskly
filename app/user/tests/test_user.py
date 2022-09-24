"""
Tests the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**kwargs):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**kwargs)


class PublicUserAPITests(TestCase):
    """Tests the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test the successful creation of a new user."""
        payload = {
            'email': 'bob23@example.com',
            'password': 'securepassword909',
            'name': 'Bob Shaw',
        }

        res = self.client.post(path=CREATE_USER_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

        # Ensure that the user's password is not in the response.
        self.assertNotIn('password', res.data)

    def test_create_user_email_already_exists_error(self):
        """Test the failure of creating a new user when the email is already taken."""
        payload = {
            'email': 'bob23@example.com',
            'password': 'securepassword909',
            'name': 'Bob Shaw',
        }
        create_user(**payload)
        res = self.client.post(path=CREATE_USER_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Raises an error """
        payload = {
            'email': 'bob23@example.com',
            'password': 'test',
            'name': 'Bob Shaw',
        }
        res = self.client.post(path=CREATE_USER_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token(self):
        """Generate a token with valid credentials."""
        user_details = {
            'email': 'bob23@example.com',
            'password': 'securepassword909',
            'name': 'Bob Shaw',
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }

        res = self.client.post(path=TOKEN_URL, data=payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_with_invalid_credentials_error(self):
        """Creating a token with invalid credentials should raise an error."""
        create_user(email='test@example.com', password='goodpassword')

        payload = {'email': 'test@example.com', 'password': 'badpassword'}

        res = self.client.post(path=TOKEN_URL, data=payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_blank_password(self):
        """Creating a token with no password should raise an error."""
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(path=TOKEN_URL, data=payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='securepassword909',
            name='Bob Shaw',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {'name': 'Updated Name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
