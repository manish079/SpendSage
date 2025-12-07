# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Added field from DB design
    currency_preference = models.CharField(max_length=5, default='INR')
    
    # Use email for login (overrides the username field in Django default auth)
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username 