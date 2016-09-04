import uuid
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """Base model we will inherit from"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class BroType(BaseModel):
    """Details about specific Bro"""
    name = models.TextField()  # The to show to the users
    code = models.TextField()  # When we have to associate it with inner app tasks(like file names, css classes etc)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
        }


class Message(BaseModel):
    """A bro message from one user to anther"""
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, related_name='sender')
    receiver = models.ForeignKey(User, related_name='receiver')
    bro = models.ForeignKey(BroType)

    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender_id,
            'receiver': self.receiver_id,
            'bro': self.bro.to_dict(),
        }

    @staticmethod
    def get_message_from_n_date(days):
        """Returns QuerySet object with all the messages from last n days"""
        time_delta = timezone.now() - timedelta(days=days)
        return Message.objects.filter(created_at__gte=time_delta)

    @staticmethod
    def get_messages_from_last_day():
        """Returns QuerySet object with all the messages from last day"""
        return Message.get_message_from_n_date(1)

    @staticmethod
    def get_messages_from_last_week():
        """Returns QuerySet object with all the messages from last week"""
        return Message.get_message_from_n_date(7)


class UserProfile(BaseModel):
    """Additional info for the User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bros = models.ManyToManyField(BroType)
