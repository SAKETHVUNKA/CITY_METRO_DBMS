from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, phone=''):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, phone=''):
        user = self.create_user(username, password, phone)
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
