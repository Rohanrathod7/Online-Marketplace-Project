from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length = 100)
    
    USERNAME_FIELD = "email"             # while filling login form set username will accept email 
    REQUIRED_FIELDS = ['username']       # required fiels with email and password and password 2

    def __str__(self):
        return self.username                # functio return name when we see user table in admin database it returns name and shows name 

