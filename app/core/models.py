"""
################################################################
TOPIC :: customizing default authentication system in django
################################################################
How to customize default djnago user model and authentication?
REFER FULL EXAMPLE HERE -
https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#a-full-example
"""

from django.contrib.auth.models import User



from django.db import models  # noqa
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)


# Create your models here
class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str = None, **extra_fields):
        """
        create, save and returns a new user
        Args:
            email (str): will be set as new default value for `username` field
            password: encrypted password via hashing
            **extra_fields: arbitraru keyword arguments to accomodate
            any additional user attributes
        Returns:
            user object
        """

        if not email:
            raise ValueError("User *MUST* have an email address")

        # with `self.model` we are already associated with default user model
        # as we are deriving from `BaseUserManager`
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # user without email normalization
        # user = self.model(email=email)

        # best practice to hash password using super class method `set_password`
        user.set_password(password)

        # best practicec to use `using=self._db` when using multiple database
        # saving a new object using `UserManager`
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        WHen we call `python manage.py createsuperuser` command, django calls
        this method.
        So make sure you are spelling hte method name correctly
        Refer -
        https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
        Args:
            email:
            password:
        Returns:
        """

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    # new user is active user by default
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Assign `UserManager` in django to custom user class.
    # When using ORM queries say `objects.get()`, `objects.create()` etc
    # all those methods come from this objects attribute
    # We are overriding default manager with our custom manager here.
    objects = UserManager()

    USERNAME_FIELD = "email"  # overrides the default user field from base class
