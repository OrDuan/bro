from datetime import timedelta

from django.test import Client
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.models import Message
from core.tests.factories import MessageFactory, UserProfileFactory


class TestMessageCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_superuser(username='test', email='test@test.com', password='test')
        self.sender_profile = UserProfileFactory(user=self.sender)

    def test_get_message_from_n_date(self):
        batch_size = 20
        days = 365

        messages = MessageFactory.create_batch(batch_size)
        self.assertEqual(Message.get_message_from_n_date(days).count(), batch_size)

        # Split the batch to half, and change the objects' created_at
        for m in messages[:batch_size//2]:
            m.created_at = timezone.now() - timedelta(days=days)
            m.save()

        self.assertEqual(Message.get_message_from_n_date(days).count(), batch_size//2)


class TestViewsCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='test')
        self.user_profile = UserProfileFactory(user=user)
        self.client = Client()
        self.client.login(username='test', password='test')

    def test_get_messages(self):
        per_page = 40  # As defined in the view
        total_messages = per_page+1  # We want to have 2 pages
        messages = MessageFactory.create_batch(total_messages, receiver=self.user_profile)

        json_data = self.client.post(reverse('core.get_messages'))
        json_data = json_data.json()

        self.assertEqual(json_data.status_code, 200)
        self.assertEqual(json_data['status'], 'ok')
        self.assertEqual(json_data['totalMessages'], len(messages))
        self.assertEqual(json_data['totalPages'], 2)

        # TODO why the hell sender id is 'a8edf470b66049beb7b0e74f5266f42d'
        # TODO and message id is 'f59a98bd-0c27-4b15-9694-6eee9d75e65d'??

