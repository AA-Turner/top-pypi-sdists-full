import factory

from wbcore.contrib.notifications.factories.notification_types import (
    NotificationTypeFactory,
)
from wbcore.contrib.notifications.models import Notification


class NotificationFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("pystr")
    body = factory.Faker("pystr")
    notification_type = factory.SubFactory(NotificationTypeFactory)
    user = factory.SubFactory("wbcore.contrib.authentication.factories.UserFactory")
    endpoint = None

    class Meta:
        model = Notification
