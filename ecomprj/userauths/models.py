from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length = 100)
    
    USERNAME_FIELD = "email"             # while filling login form set username will accept email 
    REQUIRED_FIELDS = ['username']       # required fiels with email and password and password 2

    def __str__(self):
        
        return self.username                # functio return name when we see user table in admin database it returns name and shows name 
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    
    image = models.ImageField(upload_to="image", null=True, blank=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        
            return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

class ContectUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return self.name

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_profile, sender=User)  # when user is created then create profile
post_save.connect(save_profile, sender=User)  # when user is saved then save profile
