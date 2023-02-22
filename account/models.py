from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    GENDER = (
        ('male', 'male'),
        ('female', 'female'),
    )
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER, default='male')
    address = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.ImageField(blank=True, upload_to='profile/')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def image_tag(self):
        if self.avatar:
            img_html = '<img src="%s" height="50" width="50">'
            return mark_safe(img_html %self.avatar.url)
        return "No image found"
    image_tag.short_description = 'Avatar'

    def __str__(self):
        return str(f"{self.customer.username}'s profile")
