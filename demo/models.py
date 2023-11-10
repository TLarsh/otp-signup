from django.db import models
from django.contrib.auth.models import (BaseUserManager, PermissionsMixin, AbstractBaseUser)
from django.core.validators import RegexValidator, validate_email
from django.conf import settings
import re
# Create your models here.

phone_number_regex = re.compile(r'^\d{11}$')
phone_regex = RegexValidator(
    regex=phone_number_regex, message="phone number must be 11 digits only. "
)

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError("phone number is  required. ")
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(phone_number, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user

class UserModel(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(unique=True, max_length=11, blank=False, null=False, validators=[phone_regex])
    email = models.EmailField(max_length=50, blank=True,null=True, validators=[validate_email])
    otp = models.CharField(max_length=6)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=settings.MAX_OTP_TRY)
    otp_max_out = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_registered_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone_number"
    # REQUIRED_FIELDS: []
    
    
    objects = UserManager()
    
    
    def __str__(self):
        return self.phone_number