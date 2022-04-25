from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setup(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@andandrade.com',
            'password': 'testpass',
            'name': 'Test name'
        }

        # Validate the status code on response
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Validate that the user was created, first get the user
        # then validate the password
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))

        # The password must be not included inside response
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'test@andandrade.com', 'password': 'testpass'}

        # Create a fake user to later validate that it already exists
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {'email': 'test@andandrade.com', 'password': 'sho'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Validate that the user wasn created
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@andandrade.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email="test@andandrade.com", password='testpass')
        payload = {
            'email': 'test@andandrade',
            'password': 'testpass'
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'andandrade@test.com', 'password': 'testpass'}

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """test that email and password are required"""
        payload = {'email': 'one', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
