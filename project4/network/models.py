from django.contrib.auth.models import AbstractUser
from django.db import models
from django import template

register = template.Library()

#Model Class to Manage all the users and the user it follows and users that follow him/her.
class User(AbstractUser):
    pass

#Model Class for Managing all the user Posts.
class Post(models.Model):
    content = models.CharField(max_length=140,blank=True)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    creation_time = models.DateTimeField(auto_now_add=True)
    scope = models.CharField(max_length=140,blank=True)

#Model Class for Managing Likes on a post.
class Likes(models.Model):
    like = models.BooleanField(default=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, null=True)


#Model Class for Managing followers/following for a post.
class Follow(models.Model):
    following = models.ManyToManyField("User", blank=True, related_name="follows")
    follower = models.ManyToManyField("User", blank=True, related_name="followed")
    follow_time = models.DateTimeField(auto_now_add=True)
    
#Model Class for Managing List of all other Users that a current user follows .
class Following(models.Model):
    followerId = models.IntegerField(null=True)
    followingId = models.IntegerField(null=True)
    
#Model Class for Managing Messages sent and Recieved!!!!.
class Messages(models.Model):
    recipient = models.CharField(max_length=140,blank=True)
    sender = models.ForeignKey("User", on_delete=models.CASCADE, related_name="sender")
    content = models.CharField(max_length=140,blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.username,
            "recipient": self.recipient,
            "content": self.content,
            "creation_time": self.creation_time.strftime("%b %-d %Y, %-I:%M %p"),
            "read": self.read
        }
    


    
