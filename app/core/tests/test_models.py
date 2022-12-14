"""
Test user model.
"""
from core import models

from django.test import TestCase
from django.contrib.auth import get_user_model


class TestUserModel(TestCase):
    """Test user model."""

    def test_create_user_successful(self):
        """Test the creation of a user with a valid email."""
        email = 'fake.email@example.com'
        password = 'securepassword909'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_normalizes_email(self):
        """Test that email is normalized for new users."""
        sample_emails = [
            ('BRANDON101@EXAMPLE.COM', 'BRANDON101@example.com'),
            ('Mary.Smith@Example.com', 'Mary.Smith@example.com'),
            ('blueRideR200@example.COM', 'blueRideR200@example.com'),
        ]

        for raw_email, normalized_email in sample_emails:
            user = get_user_model().objects.create_user(
                email=raw_email,
                password='securepassword909'
            )
            self.assertEqual(user.email, normalized_email)

    def test_create_user_without_email_raises_error(self):
        """Creating a user without an email should raise a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='securepassword909')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='securepassword909',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class TestTaskModel(TestCase):
    """Test cases for the tasks model."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@example.com', password='securepassword909')

    def test_create_task(self):
        """Test creating a task is successful."""
        task = models.Task.objects.create(
            user=self.user,
            title='Walk the dog',
        )
        self.assertEqual(str(task), task.title)
