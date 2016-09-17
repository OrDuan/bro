import uuid
from datetime import timedelta
import binascii
import os

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
    note = models.TextField(null=True, blank=True)  # Where to get, how rare etc

    # How many bros a user need to get it, if null - means you get it from different way then just
    # send bros, future implementation.
    bros_needed = models.IntegerField(null=True, blank=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'note': self.note,
            'brosNeeded': self.bros_needed,
        }


class UserProfile(BaseModel):
    """Additional info for the User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=40, null=True, blank=True)
    bros = models.ManyToManyField(BroType)

    @staticmethod
    def _generate_auth_token():
        return binascii.hexlify(os.urandom(20)).decode()

    def set_new_auth_token(self):
        self.auth_token = UserProfile._generate_auth_token()
        return self.auth_token

    def verify_has_bro(self, bro_id):
        """
        Verify the user has this bro_id
        """
        return self.bros.filter(id=bro_id).exists()

    def get_next_bro_type(self):
        """
        Returns the next bro the user will get if he keep sending messages
        """
        # TODO Is it possible to do it in one db hit?
        current_count = self.sender.count()
        return BroType.objects.filter(bros_needed__gt=current_count).order_by('bros_needed').first()

    def has_new_bro_type(self):
        """
        Return BroType of right now the user has exactly as much as needed for
        the new BroType. If not, return None.
        """
        # TODO Is it possible to do it in one db hit?
        return BroType.objects.filter(bros_needed=self.sender.count()).first()


class Message(BaseModel):
    """A bro message from one user to anther"""
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(UserProfile, related_name='sender')
    receiver = models.ForeignKey(UserProfile, related_name='receiver')
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
        """
        Returns QuerySet object with all the messages from last n days
        """
        time_delta = timezone.now() - timedelta(days=days)
        return Message.objects.filter(created_at__gte=time_delta)

    @staticmethod
    def get_messages_from_last_day():
        """
        Returns QuerySet object with all the messages from last day
        """
        return Message.get_message_from_n_date(1)

    @staticmethod
    def get_messages_from_last_week():
        """
        Returns QuerySet object with all the messages from last week
        """
        return Message.get_message_from_n_date(7)


