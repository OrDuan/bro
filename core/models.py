import uuid

from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    """Base model we will inherit from"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class BroType(BaseModel):
    """Details about specific Bro"""
    name = models.TextField()  # The to show to the users
    code = models.TextField()  # When we have to associate it with inner app tasks(like file names, css classes etc)


class Message(BaseModel):
    """A bro message from one user to anther"""
    sender = models.ForeignKey(User, related_name='sender')
    receiver = models.ForeignKey(User, related_name='receiver')
    bro = models.ForeignKey(BroType)


class UserProfile(BaseModel):
    """Additional info for the User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
