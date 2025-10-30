from django.db import models 
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid
from  django.contq  arib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timezone
from datetime import timedelta
import secrets
from django.core.exceptions import ValidationError
from  drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class CustomUserManager(BaseUserManager):
    def create_user(self,email_address,password=None,**extra_fields):
        if not  email_address:
            raise ValueError("The Email field must be set ")
      
        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address,**extra_fields)


        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user
    


    def create_superuser(self,email_address,password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('provider','email')
        extra_fields.setdefault('verified_at',timezone.now())

        if not password:
            raise ValueError('Superuser must have a password ')
        
        return self.create_user(email_address,password,**extra_fields)
    

    REGISRATION_PROVIDERS = [
        ('email','Email Registrations')
        ('google','Google OAuth'),
        ('facebook',' Facebook OAUTH'),
        ('x', 'X OAAUTH'),
    ]




class User(AbstractBaseUser,PermissionsMixin):

    ROLE_CHOICES = [
        ('customer','Customer'),
        ('admin','Home Chef'),
        ('partner','Delivery Partner'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname  = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150, null=True blank=True)
    email_address = models.CharField(unique=True)
    role =  models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')   
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
    

class Admin(models.Model):
    admin = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    profile_image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.admin.username}"
    


class MenuItem(models.Model):
    name = models.CharField(max_length=255,default='Ugali Kuku Kienyeji') 
    description = models.TextField(blank=True)
    price  = models.DecimalField(max_length=10,decimal_places=2)
    image = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        verbose_name_plural ="Menu Items"

    def __str__(self):
        return self.name
    








class PaymentType(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='payment_logos', null=True, blank=True)
    is_active  = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    


class PaymentMethod(TimeStampedModel):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    name  = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='payment_logos/', null=True, blank=True)
    description = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)


    def get_field_configuration(self):
        """
        Dynamic method to build configuration object
        """
        configs = obj.field_configs.all()  #Uses the related_name from my model
        configuration = {
            'required':[],
            'optional':[],
            'disallowed':[],
            'validations':{}
        }
       
        for config in configs:
                if config.is_required:
                    configuration['required'].append(config.field_name)
                elif config.is_allowed:
                    configuration['optional'].append(config.field_name)
                else:
                    configuration['disallowed'].append(config.field_name)

                if config.validation_regex:
                    configuration['validations'][config.field_name] = {
                        'regex':config.validation_regex,
                        'message':config.validation_message or f"Invalid format for {config.field_name} "
                    }           
            
        return configuration
    
    def get_logo_url(self,obj):
        request = self.context.get('request')
        if obj.logo and request:
            return request.build_absolute_uri(obj.logo.url)
        return None
    



class PaymentMethodFieldConfigSerializer(serializers.ModelSerializer):
        id = models.ForeignKey(primary_key=True,default=uuid.uuid4, editable=False)
        payment_method = models.CharField(max_length=100)
        field_name  = models.CharField(max_length=100)
        field_label = models.CharField(max_length=100,blank=True, null=True)
        field_placeholdeer = models.BooleanField(max_length=100,blank=True,null=True)
        is_required = models.BooleanField(default=False)
        is_allowed = models.BooleanField(default=True)
        validation_regex = models.CharField(max_length=200,blank=True, null=True)
        validation_message  = models.CharField(max_length=200, blank=True, null=True)

        class Meta:
            unique_together = ('payment_method','field_name')
