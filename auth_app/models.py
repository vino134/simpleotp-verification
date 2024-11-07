from django.db import models
from django.contrib.auth.models import User

class PhoneNumber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    verification_code = models.CharField(max_length=6, blank=True)
    is_verified = models.BooleanField(default=False)
