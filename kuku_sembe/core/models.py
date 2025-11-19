from django.db import models
from django.contrib.auth.base_user import  BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid 
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta
import secrets
from  .managers import SoftDeleteManager
from django.core.exceptions import ValidationError
from  drf_spectacular.utils import extend_schema_field
from  django.utils.text import slugify
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self,email, password=None, **extra_fields):
        if not email_address:
            raise ValueError('The Email field must be set')
        
        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address,**extra_fields)


        if password:
            user.set_password(password)

            user.save(using=self._db)
            return user

    def create(self,email_address,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('provider','email')
        extra_fields.setdefault('provider','email')
        extra_fields.setdefault('verified_at',timezone.now()) 

        if not password:
            raise ValueError('Superuser must have a password') 
        return self.create_user(email_address,password,**extra_fields)
    
    


REGISTRATION_PROVIDERS = [
    ('email','Email Registration'),
    ('google','Google OAuth'),
    ('facebook','Facebook OAuth'),
    ('x','XOAuth'),
]



class User(AbstractBaseUser, PermissionsMixin):


    ROLE_CHOICES = [
        ('customer','Customer'),
        ('admin','Home Chef'),
        ('partner','Delivery Partner'),
    ]
     

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    phone  = models.CharField(max_length=20, unique=True)
    address =  models.TextField(blank=True, null=True)
    vehicle_details = models.CharField(max_length=500,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
    


class AdminProfile(models.Model):
    admin =  models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.URLField(blank=True, null=True)
    ratings_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.IntegerField(default=0)


    









       




        


