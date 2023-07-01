from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    nickname = models.CharField(max_length=20, blank=True)
    pass


# Create Message Model
class Message(models.Model):
    author = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=20, blank=True)
    subject = models.TextField(blank=True)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    solved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} | {self.email} | {self.subject} | {self.body} | {self.timestamp} | "

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author,
            "email": self.email,
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "solved": self.solved
        }


class Pack(models.Model):
    name = models.CharField(max_length=20, blank=False)
    desc1 = models.CharField(max_length=100, blank=False)
    desc2 = models.CharField(max_length=100, blank=False)
    desc3 = models.CharField(max_length=100, blank=False)
    desc4 = models.CharField(max_length=100, blank=False)
    desc5 = models.CharField(max_length=100, blank=False)
    desc6 = models.CharField(max_length=100, blank=False)
    image = models.ImageField(upload_to ='static/finalproject/')
    video = models.FileField(upload_to='static/finalproject/', null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    short = models.CharField(max_length=20, blank=True)
    fitr = models.CharField(max_length=20, blank=True)


    def __str__(self):
        return f"Pack Name: {self.name}"


class Team(models.Model):
    name = models.CharField(max_length=20, blank=False)
    title = models.CharField(max_length=60, blank=True)
    desc1 = models.CharField(max_length=60, blank=False)
    desc2 = models.CharField(max_length=60, blank=False)
    image = models.ImageField(upload_to ='static/finalproject/')
    link = models.CharField(max_length=60, blank=True)
    short = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Trainer: {self.name} | Title: {self.title}"
