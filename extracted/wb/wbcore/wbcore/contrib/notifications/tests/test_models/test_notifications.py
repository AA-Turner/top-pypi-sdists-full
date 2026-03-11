from datetime import timedelta
from unittest.mock import patch

import pytest
from bs4 import BeautifulSoup
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.test.utils import override_settings
from django.utils import timezone

from wbcore.contrib.notifications.models import Notification, NotificationTypeSetting
from wbcore.contrib.notifications.utils import base_domain


@pytest.fixture
def patched_import_string(mocker):
    return mocker.patch("wbcore.contrib.notifications.models.notifications.import_string")


@pytest.fixture
def mock_backend():
    from wbcore.contrib.notifications.backends.abstract_backend import (
        AbstractNotificationBackend,
    )

    class MockedBackend(AbstractNotificationBackend):
        @classmethod
        def send_web_notification(cls, notification):
            pass

        @classmethod
        def send_mobile_notification_notification(cls, notification):
            cls.send_web_notification(notification)

        @classmethod
        def get_configuration(cls) -> dict:
            return {}

    return MockedBackend


@pytest.mark.django_db
class TestNotification:
    def test_factory(self, notification: Notification):
        assert isinstance(notification, Notification)
        assert notification.pk is not None

    def test_to_str(self, notification: Notification):
        assert str(notification) == f"{notification.user} {notification.title}"

    def test_endpoint_basename(self):
        assert Notification.get_endpoint_basename() == "wbcore:notifications:notification"

    def test_representation_value_key(self):
        assert Notification.get_representation_value_key() == "id"

    def test_representation_label_key(self):
        assert Notification.get_representation_label_key() == "{{title}}"

    def test_has_duplicated(self, notification_factory):
        notification = notification_factory.create()
        assert notification.has_email_duplicated() is False
        duplicated_notification = notification_factory.create(
            user=notification.user,
            title=notification.title,
            body=notification.body,
            endpoint=notification.endpoint,
            notification_type=notification.notification_type,
            created=notification.created + timedelta(minutes=60),
        )
        assert notification.has_email_duplicated(interval=61) is False
        assert notification.has_email_duplicated(interval=59) is False
        duplicated_notification.sent_email = duplicated_notification.created
        duplicated_notification.save()
        assert notification.has_email_duplicated(interval=59) is True

    @pytest.mark.parametrize("notification__endpoint", ["/wbcore/notifications/"])
    def test_full_valid_internal_endpoint(self, notification):
        assert notification.get_full_endpoint() == f"{base_domain()}{notification.endpoint}"

    @pytest.mark.parametrize("notification__endpoint", ["/some_invalid_namespace/notifications/"])
    def test_full_invalid_internal_endpoint(self, notification):
        assert notification.get_full_endpoint() is None

    @pytest.mark.parametrize("notification__endpoint", ["/wbcore/notifications/"])
    def test_full_internal_endpoint_as_shareable_link(self, notification):
        assert (
            notification.get_full_endpoint(as_shareable_internal_link=True)
            == f"{base_domain()}?widget_endpoint={notification.endpoint}"
        )

    @pytest.mark.parametrize("notification__endpoint", ["https://www.google.com"])
    def test_full_valid_external_endpoint(self, notification):
        assert notification.get_full_endpoint() == notification.endpoint

    @pytest.mark.parametrize("notification__endpoint", ["https.www.google.com"])
    def test_full_invalid_external_endpoint(self, notification):
        assert notification.get_full_endpoint() is None

    @patch.object(EmailMultiAlternatives, "send")
    @patch.object(Notification, "has_email_duplicated")
    def test_send_exclude_mail_with_duplicate(self, mock_has_duplicated, mock_send_as_mail, notification):
        mock_has_duplicated.return_value = False
        setting = notification.notification_type.get_setting_for_user(notification.user)
        setting.enable_email = True
        setting.save()

        assert mock_send_as_mail.call_count == 0
        notification = Notification.objects.get(id=notification.id)
        notification.send()
        assert mock_send_as_mail.call_count == 1

        mock_has_duplicated.return_value = True
        notification = Notification.objects.get(id=notification.id)
        notification.send()
        assert mock_send_as_mail.call_count == 1

    @patch.object(Notification, "send_email")
    def test_send_notification_task(
        self, patched_send_notification_email, notification, mock_backend, mocker, patched_import_string
    ):
        spy = mocker.spy(mock_backend, "send_web_notification")
        patched_import_string.return_value = mock_backend

        setting = notification.notification_type.get_setting_for_user(notification.user)
        setting.enable_email = False
        setting.save()

        notification.send()
        patched_send_notification_email.assert_not_called()

        setting.enable_email = True
        setting.save()
        notification = Notification.objects.get(id=notification.id)
        notification.send()
        patched_send_notification_email.assert_called_once_with()

        setting.enable_web = True
        setting.save()
        notification = Notification.objects.get(id=notification.id)
        notification.send()
        patched_import_string.assert_called_once()
        spy.assert_called_once_with(notification)

    @patch.object(Notification, "send_email")
    def test_send_notification_task_without_mail(
        self, patched_send_notification_email, notification, mock_backend, patched_import_string
    ):
        notification.user.wbnotification_user_settings.update(enable_email=False)
        patched_import_string.return_value = mock_backend

        notification.send()

        assert not patched_send_notification_email.called

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    @pytest.mark.parametrize("notification__endpoint", ["/wbcore/notifications/"])
    def test_send_notification_email(self, notification):
        setting = notification.notification_type.get_setting_for_user(notification.user)
        setting.enable_email = True
        setting.save()

        assert len(mail.outbox) == 0
        notification.send()
        assert len(mail.outbox) == 1
        soup = BeautifulSoup(mail.outbox[0].alternatives[0][0], "html.parser")
        assert soup.find("a", href=notification.get_full_endpoint(as_shareable_internal_link=True))


@pytest.mark.django_db
class TestNotificationManager:
    def test_filter_unsent_and_due(self, user_factory, notification_factory, notification_type_factory):
        type1 = notification_type_factory.create(default_enable_email=True, is_important=False)
        type2 = notification_type_factory.create(default_enable_email=True, is_important=False)
        user = user_factory.create()
        setting1 = type1.get_setting_for_user(user)
        setting2 = type2.get_setting_for_user(user)
        setting2.frequency = NotificationTypeSetting.Frequency.DAILY
        setting2.save()

        assert setting1.frequency == NotificationTypeSetting.Frequency.IMMEDIATLY
        assert setting1.enable_email is True
        now = timezone.now()
        sent_notification = notification_factory.create(  # noqa: F841
            title="Sent notification", user=user, notification_type=type1, sent_email=now
        )
        first_unsent_notification = notification_factory.create(
            title="first Unset notification", user=user, notification_type=type1, sent_email=None
        )
        first_daily_unsent_notification = notification_factory.create(
            title="first Daily Unset notification", user=user, notification_type=type2, sent_email=None
        )
        unset_notification_hourly = notification_factory.create(
            title="Unset Hourly Notification", user=user, notification_type=type1, sent_email=None
        )
        assert set(Notification.objects.filter_unsent_and_due()) == {
            first_unsent_notification,
            unset_notification_hourly,
        }

        setting1.enable_email = False
        setting1.save()
        assert set(Notification.objects.filter_unsent_and_due()) == set()

        setting1.enable_email = True
        setting1.frequency = NotificationTypeSetting.Frequency.HOURLY
        setting1.save()
        assert set(Notification.objects.filter_unsent_and_due()) == set()

        Notification.objects.filter(id=first_daily_unsent_notification.id).update(
            created=now - timedelta(hours=23, minutes=59)
        )
        assert set(Notification.objects.filter_unsent_and_due()) == set()

        Notification.objects.filter(id=first_unsent_notification.id).update(created=now - timedelta(minutes=61))
        assert set(Notification.objects.filter_unsent_and_due()) == {
            first_unsent_notification,
            unset_notification_hourly,
        }

        Notification.objects.filter(id=first_daily_unsent_notification.id).update(
            created=now - timedelta(hours=24, minutes=1)
        )
        assert set(Notification.objects.filter_unsent_and_due()) == {
            first_unsent_notification,
            unset_notification_hourly,
            first_daily_unsent_notification,
        }
