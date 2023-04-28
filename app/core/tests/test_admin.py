"""
Test for the django admin modifications
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.shortcuts import reverse


class AdminSiteTest(TestCase):
    """Test for django admin"""

    def setUp(self) -> None:
        """create user and client"""
        # allows you to simulate HTTP requests to your application
        self.Client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@gmail.com",
            password="admin1234"
        )
        # Why using force login?
        # Regular login requires credentials
        # `force_login()` method requires no input from the user

        # alternatively,
        # self.client.login(email="admin@example.com", password="admin_pass")
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_superuser(
            email="user@example.com",
            password="testpass123",
            name="Test User"

        )

    # admin interface user list endpoint
    def test_user_list(self):
        """Whenever you hit URL endpoint `/admin/core/user/` with logged in
        superuser you get list of users.
        This tests cases validates the list of users"""

        # TODO (TOPIC - reversing admin URLs)
        # refer
        # https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#reversing-admin-urls
        # Also known as `named URLs`
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works
        PLURAL (GET) - list of resources
        SINGULAR ENDPOINT (POST, PUT, DELETE, PATCH)
            """

        # TODO (TOPIC - Reversing admin URLs) - refer
        #  https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#reversing-admin-urls
        # also known as `named urls`
        # matches with admin url to edit user

        url = reverse("admin:core_user_change", args=[self.user.id])
        req = self.client.get(url)
        self.assertEqual(req.status_code, 200)

    def test_create_user_group(self):
        """Test the create user page works"""

        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
