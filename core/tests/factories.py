import factory
from core.models import BroType, UserProfile


class UserProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.LazyFunction(lambda: exec('raise(Exception("Override this!"))'))


class BroTypeFactory(factory.DjangoModelFactory):
    class Meta:
        model = BroType

    name = factory.Sequence(lambda n: 'name{}'.format(n))
    code = factory.Sequence(lambda n: 'code{}'.format(n))


class MessageFactory(factory.DjangoModelFactory):
    class Meta:
        model = BroType

    bro = factory.SubFactory(BroTypeFactory)






