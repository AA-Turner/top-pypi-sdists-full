import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient, APIRequestFactory
from wbcore.contrib.authentication.factories import UserFactory
from wbcore.contrib.directory.factories import PersonFactory
from wbcore.contrib.notifications.factories.notification_types import (
    NotificationTypeFactory,
    NotificationTypeSettingModelFactory,
)
from wbcore.contrib.notifications.factories.notifications import (
    NotificationFactory,
)
from wbcore.contrib.notifications.factories.tokens import (
    NotificationUserTokenModelFactory,
)
from wbcore.tests.conftest import *

register(UserFactory)
register(PersonFactory)
register(NotificationTypeFactory)
register(NotificationTypeSettingModelFactory, name="notification_type_setting")
register(NotificationFactory)
register(NotificationUserTokenModelFactory, name="notification_user_token")


@pytest.fixture
def request_with_user(user):
    request = APIRequestFactory().get("/")
    request.user = user
    return request


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture(
    autouse=True, scope="session"
)  # Might want to find a way to registered default conftest logic automatically
def django_test_environment(django_test_environment):
    from django.apps import apps

    get_models = apps.get_models

    for m in [m for m in get_models() if not m._meta.managed]:
        m._meta.managed = True
