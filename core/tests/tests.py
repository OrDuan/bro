from core.models import Message
from core.tests.factories import MessageFactory, UserProfileFactory
from django.contrib.auth.models import User
from django.test import TestCase


class TestMessageCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_superuser(username='test', email='test@test.com', password='test')
        self.sender_profile = UserProfileFactory(user=self.sender)

    def test_get_messages_from_last_week(self):
        message = MessageFactory()
        Message.get_messages_from_last_week().count()