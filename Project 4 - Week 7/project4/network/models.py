from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.URLField(null=True, blank=True, max_length=9999)
    pass


# Create Post Model
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="likes")

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": [author.username for author in self.likes.all()],
        }
    
# Create Model for follow function
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follow")
    followers = models.ManyToManyField(User, related_name="subs")
    following = models.ManyToManyField(User, related_name="subbing")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "followers": [user.username for user in self.followers.all()],
            "following": [user.username for user in self.following.all()]
        }

