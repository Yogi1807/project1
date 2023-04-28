"""
Tests the user API
# Endpoints
- HTTP POST `/api/user/create/`
- HTTP POST `/api/user/token/`
- HTTP GET, PUT, PATCH   -  `/api/user/me`
# Types of endpoint based on authorization
- public
- private
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status

CREATE_USER_URL = reverse("create")
TOKEN_URL = reverse("token")
ME_URL = reverse("me")


class PublicUserAPITest(TestCase):
    """Test the public API user from client"""

    @staticmethod
    def create_user(**params):
        """return user from whichever default user model"""
        return get_user_model().objects.create_user(**params)

    def setUp(self):
        """Instantiate client"""

        self.client = APIClient()

    def test_create_user_success(self):
        """test creating user is successfull (/api/user/create)"""

        payload = {
            "email": "test@gmail.com",
            "password": "password123",
            "name": "test"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        breakpoint()
        self.assertEqual(res.status_code, 201)

    # scenario 2 - short password (len(password) < 5 )
    def test_create_user_with_short_password(self):
        """Test error returned if password is less than 5 characters"""

        payload = {
            "email": "test@example.com",
            "password": "",
            "name": "Test Name"
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, 400)

        # scenario 3 - user email already exists in database
    def test_user_with_email_exists_error(self):
        """Test error returned if user email already exists"""

        payload = {
            "email": "test@example.com",
            "password": "password@321",
            "name": "Test Name"
            }

        # step 1: create user using ORM
        self.create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, 400 )

    def test_create_token_for_user(self):
        """Test generates a token for valid user credentials"""

        payload = {
            "email": "Random@gmail.com",
            "password": "Random123"
        }
        self.create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_retrieve_user_unauthorised(self):
        """Test authentication is required for user"""

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_bad_credential(self):
        """Test return error if credential invalid"""

        self.create_user(email="new@gmail.com", password="newpassword")
        payload = {"email": "new@gmail.com", "password": "oldpassword"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("tocker", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        """Test return error if email found in database"""

        payload = {"email": "nothing@gmail.com", "password": "Noting"}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""

        payload = {"email": "nothing", "password": ""}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    @staticmethod
    def create_user(**params):
        """returns user from whichever default user model"""

        return get_user_model().objects.create_user(**params)

    def setUp(self) -> None:
        self.user = self.create_user(
            email="test@example.com",
            password="password@321",
            name="Test name"
        )
        self.client = APIClient()

        # TODO - refer
        # https://www.django-rest-framework.org/api-guide/testing/#forcing-authentication
        """
        We are using `force_authenticate` function to set authentication flag
        to `True`
        We don't want to create token and authenticate user under each test case
        SO we have handled authentication part by `force authentication`.

        So any subsequent request to `/api/user/me` gets an already authenticated
        user

        """
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_profile(self):
        """Test retriving user information with valid token"""

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"name": self.user.name,
                                    "email": self.user.email})

    def test_update_user_profile(self):
        """Test updating the user profile for an authenticated user"""

        payload = {"name": "updated name", "email": "updated@email.com"}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload.get("name"))
        self.assertEqual(self.user.email, payload.get("email"))

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint"""

        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
