import factory

from wbcore.contrib.notifications.models import (
    NotificationType,
    NotificationTypeSetting,
)


class NotificationTypeFactory(factory.django.DjangoModelFactory):
    code = factory.Faker("pystr")
    title = factory.Faker("pystr")
    help_text = factory.Faker("pystr")
    default_enable_email = False

    class Meta:
        model = NotificationType


class NotificationTypeSettingModelFactory(factory.django.DjangoModelFactory):
    notification_type = factory.SubFactory(NotificationTypeFactory)
    user = factory.SubFactory("wbcore.contrib.authentication.factories.UserFactory")

    class Meta:
        model = NotificationTypeSetting
        django_get_or_create = ("user", "notification_type")
