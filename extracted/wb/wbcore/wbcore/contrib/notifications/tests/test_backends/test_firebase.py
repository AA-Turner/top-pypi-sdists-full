import pytest

from wbcore.contrib.notifications.backends.firebase.backends import (
    NotificationBackend as FirebaseNotificationBackend,
)
from wbcore.contrib.notifications.factories.tokens import (
    NotificationUserTokenModelFactory,
)
from wbcore.contrib.notifications.models.tokens import NotificationUserToken


@pytest.mark.django_db
def test_send_notification(mocker, notification, user):
    mocked_get_app = mocker.patch(
        "wbcore.contrib.notifications.backends.firebase.backends.firebase_admin.get_app",
    )
    mocked_initialize_app = mocker.patch(
        "wbcore.contrib.notifications.backends.firebase.backends.firebase_admin.initialize_app",
    )
    mocked_send = mocker.patch("wbcore.contrib.notifications.backends.firebase.backends.messaging.send")
    mocked_get_firebase_credentials = mocker.patch.object(FirebaseNotificationBackend, "get_firebase_credentials")

    NotificationUserTokenModelFactory.create(user=user, device_type=NotificationUserToken.NotificationDeviceType.WEB)
    notification.notification_type.user_settings.filter(user=notification.user).update(enable_web=True)
    FirebaseNotificationBackend.send_web_notification(notification)

    mocked_send.assert_called_once()
    mocked_get_firebase_credentials.assert_called_once()
    mocked_get_app.assert_called_once()
    mocked_initialize_app.assert_not_called()


@pytest.mark.django_db
def test_send_multiple_notifications(mocker, notification, user):
    mocked_get_app = mocker.patch(
        "wbcore.contrib.notifications.backends.firebase.backends.firebase_admin.get_app",
    )
    mocked_initialize_app = mocker.patch(
        "wbcore.contrib.notifications.backends.firebase.backends.firebase_admin.initialize_app",
    )
    mocked_send = mocker.patch("wbcore.contrib.notifications.backends.firebase.backends.messaging.send")
    mocked_get_firebase_credentials = mocker.patch.object(FirebaseNotificationBackend, "get_firebase_credentials")

    NotificationUserTokenModelFactory.create_batch(
        3, user=user, device_type=NotificationUserToken.NotificationDeviceType.WEB
    )
    notification.notification_type.user_settings.filter(user=notification.user).update(enable_web=True)
    FirebaseNotificationBackend.send_web_notification(notification)

    assert mocked_send.call_count == 3
    mocked_get_firebase_credentials.assert_called_once()
    mocked_get_app.assert_called_once()
    mocked_initialize_app.assert_not_called()


@pytest.mark.django_db
def test_send_notification_with_initialize(mocker, notification, user):
    mocked_get_app = mocker.patch(
        "wbcore.contrib.notifications.backends.firebase.backends.firebase_admin.get_app",
        side_effect=ValueError(),
    )
    mocked_initialize_app = mocker.patch(
        "wbcore.contrib.notifications.backends.firebase.backends.firebase_admin.initialize_app"
    )
    mocked_send = mocker.patch("wbcore.contrib.notifications.backends.firebase.backends.messaging.send")
    mocked_get_firebase_credentials = mocker.patch.object(FirebaseNotificationBackend, "get_firebase_credentials")
    NotificationUserTokenModelFactory.create(user=user, device_type=NotificationUserToken.NotificationDeviceType.WEB)
    notification.notification_type.user_settings.filter(user=notification.user).update(enable_web=True)
    FirebaseNotificationBackend.send_web_notification(notification)

    mocked_get_app.assert_called_once()
    mocked_initialize_app.assert_called_once()
    mocked_send.assert_called_once()
    mocked_get_firebase_credentials.assert_called_once()


def test_get_configuration(mocker):
    mocker.patch.dict("os.environ", {"FIREBASE_WEB_CONFIG": '{"ABC": "123"}', "FIREBASE_VAPID_KEY": "DEF"})
    assert FirebaseNotificationBackend.get_configuration() == {"firebase_config": {"ABC": "123"}, "vapid_key": "DEF"}
