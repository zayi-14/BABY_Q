from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AdminManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

class Admin(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)  # Added email for communication
    full_name = models.CharField(max_length=255)  # Optional: for display
    phone_number = models.CharField(max_length=15, blank=True)  # Optional
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)  # This enables the admin staff login
    
    objects = AdminManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']  # Include any required fields here

    def __str__(self):
        return self.username
