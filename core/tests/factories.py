import factory
from core.models import BroType, UserProfile, Message
from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: 'person{0}@example.com'.format(n))
    username = factory.Sequence(lambda n: 'person{0}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password',
                                                factory.Sequence(lambda n: 'person{0}@example.com'.format(n)))


class UserProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)


class BroTypeFactory(factory.DjangoModelFactory):
    class Meta:
        model = BroType

    name = factory.Sequence(lambda n: 'name{}'.format(n))
    code = factory.Sequence(lambda n: 'code{}'.format(n))


class MessageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Message

    bro = factory.SubFactory(BroTypeFactory)
    receiver = factory.SubFactory(UserProfileFactory)
    sender = factory.SubFactory(UserProfileFactory)

