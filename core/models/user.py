from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager 
from libs.models import TimeInfo 
from libs.utils import CoreUtilsMixin


class UserManager(BaseUserManager, CoreUtilsMixin):
    def create_user(self, email, password, **extra_fields):
        if not email or not self.is_valid_email(email):
            raise ValueError("Email invalid!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user 
    

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin, TimeInfo):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    
    def __str__(self):
        return self.email 
    

    def save(self, *args, **kwargs):
        if self.first_name and self.last_name:
            self.full_name = self.first_name + " " + self.last_name 
        if not self.full_name:
            self.full_name = self.email.split('@')[0]
        super(User, self).save(*args, **kwargs)

