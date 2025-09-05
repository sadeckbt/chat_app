import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager


# Create your models here.
class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(max_length=256, unique=True, verbose_name='email')

    otp = models.CharField(max_length=5, null=True, blank=True)

    is_online = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    joined_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
