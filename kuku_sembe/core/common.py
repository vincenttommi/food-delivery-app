from django.utils import timezone
from django.db import models
from .managers import SoftDeleteManager
import uuid
from django.utils.text import slugify
from  django.conf import settings





#TimeStampedModel for common timestamp fields

class  TimeStampedModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,related_name='+')    
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    deleted_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        abstract = True




#SoftDeleteableModel for soft deletion functionality
class SoftDeleteableModel(TimeStampedModel):
    objects = SoftDeleteManager() #Default manager excluded deleted
    all_objects = models.Manager()
    class Meta:
        abstract =True


    def soft_delete(self, user=None):
        self.deleted_at = timezone.now()
        if user:
            self.deleted_by = user
        self.save()

        
                
