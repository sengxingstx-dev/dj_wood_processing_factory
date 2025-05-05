from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone

from common.models import BaseModel


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"


class Client(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Full Name or Company Name")
    contact_number = models.CharField(max_length=20, verbose_name="Contact Number")
    address = models.CharField(max_length=255, verbose_name="Physical Address")
    registration_date = models.DateField(auto_now_add=True, verbose_name="Registration Date")
    user = models.OneToOneField(
        Account,
        on_delete=models.SET_NULL,
        related_name="client_profile",
        verbose_name="Associated User",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"


class Employee(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    contact_number = models.CharField(max_length=20, verbose_name="Contact Number")
    date_hired = models.DateField(verbose_name="Date Hired")
    user = models.OneToOneField(
        Account,
        on_delete=models.SET_NULL,
        related_name="employee_profile",
        verbose_name="Associated User",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"
