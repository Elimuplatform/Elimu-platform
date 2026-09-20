from django.db import models
from django.contrib.auth.models import User

class FounderInfo(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    image1 = models.ImageField(upload_to='founder/', blank=True, null=True)
    image2 = models.ImageField(upload_to='founder/', blank=True, null=True)
    image3 = models.ImageField(upload_to='founder/', blank=True, null=True)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name

class Notice(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='notices_pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    passport_photo = models.ImageField(upload_to='passports/', blank=True, null=True)

    def __str__(self):
        return self.user.username