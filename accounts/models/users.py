from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

from .profiles import Profile


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('vendor', 'Vendor'),
        ('customer', 'Customer'),
    )
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='customer')
    username = None  # Remove default username
    email = models.EmailField(unique=True)


    verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        db_table = 'Users'
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def profile_or_none(self):
        try:
            return self.profile
        except Profile.DoesNotExist:
            return None

    @property
    def user_comments(self):
        """Returns all comments made by the user."""
        return self.comments.all()
