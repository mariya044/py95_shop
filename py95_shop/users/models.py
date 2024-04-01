from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("email must exists")
        if not password:
            raise ValueError('Password field must be fill in ')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)





class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    phone_number=models.CharField(max_length=14,blank=True,null=True)
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    first_name=models.CharField(max_length=40,blank=True,null=True)
    last_name=models.CharField(max_length=40,blank=True,null=True)
    cashback_points=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    is_notification_required=models.BooleanField(default=True)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS = []

    objects=CustomUserManager()

    def __str__(self):
        return self.email


# Create your models here.
