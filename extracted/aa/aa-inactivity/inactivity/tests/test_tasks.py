import datetime as dt
from http import HTTPStatus
from unittest.mock import patch

import discord
from celery.exceptions import Retry as CeleryRetry
from memberaudit.tests.testdata.factories import (
    create_character_from_user,
    create_character_online_status,
)

from django.utils.timezone import now

from app_utils.testing import NoSocketsTestCase

from inactivity.models import InactivityPing, Webhook
from inactivity.tasks import (
    check_inactivity,
    check_inactivity_for_user,
    send_inactivity_ping,
    send_message_to_webhook,
)

from .factories import (
    InactivityPingConfigFactory,
    InactivityPingFactory,
    LeaveOfAbsenceFactory,
    UserMainRequestorFactory,
    WebhookFactory,
)

MODELS_PATH = "inactivity.models"
TASKS_PATH = "inactivity.tasks"


@patch(TASKS_PATH + ".send_message_to_webhook.apply_async", spec=True)
@patch(TASKS_PATH + ".notify.danger", spec=True)
class TestSendInactivityPing(NoSocketsTestCase):
    def test_should_ping_user_and_webhook_when_configured_for_inactivity(
        self, mock_notify_user, mock_send_message_to_webhook
    ):
        # given
        config = InactivityPingConfigFactory()
        user = UserMainRequestorFactory()
        WebhookFactory(
            ping_configs=[config],
            notification_types=[Webhook.NotificationType.INACTIVE_USER],
        )
        # when
        send_inactivity_ping(user_pk=user.pk, config_pk=config.pk, last_login_at=now())
        # then
        args, _ = mock_notify_user.call_args
        self.assertEqual(args[0], user)
        self.assertTrue(mock_send_message_to_webhook.called)
        self.assertTrue(
            InactivityPing.objects.filter(
                user=user,
                config=config,
                timestamp__gte=now() - dt.timedelta(seconds=10),
            ).exists()
        )

    def test_should_not_ping_webhooks_with_correct_configuration(
        self, _, mock_send_message_to_webhook
    ):
        # given
        config = InactivityPingConfigFactory()
        user = UserMainRequestorFactory()
        # Webhooks to ping
        hook_1 = WebhookFactory(
            is_active=True,
            ping_configs=[config],
            notification_types=[Webhook.NotificationType.INACTIVE_USER],
        )
        hook_2 = WebhookFactory(
            is_active=True,
            notification_types=[Webhook.NotificationType.INACTIVE_USER],
        )
        hook_3 = WebhookFactory(
            is_active=True,
            notification_types=[
                Webhook.NotificationType.INACTIVE_USER,
                Webhook.NotificationType.LOA_APPROVED,
                Webhook.NotificationType.LOA_NEW,
            ],
        )
        # Webhooks not to ping
        WebhookFactory(
            is_active=True,
            ping_configs=[config],
            notification_types=[Webhook.NotificationType.LOA_APPROVED],
        )
        WebhookFactory(
            is_active=False,
            notification_types=[Webhook.NotificationType.INACTIVE_USER],
        )
        # when
        send_inactivity_ping(user_pk=user.pk, config_pk=config.pk, last_login_at=now())
        # then
        called_webhook_pks = {
            x[1]["kwargs"]["webhook_pk"]
            for x in mock_send_message_to_webhook.call_args_list
        }
        self.assertEqual(called_webhook_pks, {hook_1.pk, hook_2.pk, hook_3.pk})

    def test_should_ping_user_only(
        self, mock_notify_user, mock_send_message_to_webhook
    ):
        # given
        config = InactivityPingConfigFactory()
        user = UserMainRequestorFactory()
        # when
        send_inactivity_ping(user_pk=user.pk, config_pk=config.pk, last_login_at=now())
        # then
        args, _ = mock_notify_user.call_args
        self.assertEqual(args[0], user)
        self.assertFalse(mock_send_message_to_webhook.called)


@patch(TASKS_PATH + ".send_inactivity_ping", spec=True)
class TestCheckInactivityForUser(NoSocketsTestCase):
    def test_should_ping_for_inactive_user(self, mock_send_inactivity_ping):
        # given
        user = UserMainRequestorFactory()
        character = create_character_from_user(user=user)
        last_login = now() - dt.timedelta(days=5)
        create_character_online_status(
            character=character,
            last_login=last_login,
            last_logout=last_login + dt.timedelta(hours=4),
        )
        InactivityPingConfigFactory(days=3)
        # when
        check_inactivity_for_user(user_pk=user.pk)
        # then
        self.assertTrue(mock_send_inactivity_ping.apply_async.called)

    def test_should_not_ping_for_active_user(self, mock_send_inactivity_ping):
        # given
        user = UserMainRequestorFactory()
        character = create_character_from_user(user=user)
        last_login = now() - dt.timedelta(days=1)
        create_character_online_status(
            character=character,
            last_login=last_login,
            last_logout=last_login + dt.timedelta(hours=4),
        )
        InactivityPingConfigFactory(days=3)
        # when
        check_inactivity_for_user(user_pk=user.pk)
        # then
        self.assertFalse(mock_send_inactivity_ping.apply_async.called)

    def test_should_not_ping_for_user_without_character(
        self, mock_send_inactivity_ping
    ):
        # given
        user = UserMainRequestorFactory()
        InactivityPingConfigFactory(days=3)
        # when
        check_inactivity_for_user(user_pk=user.pk)
        # then
        self.assertFalse(mock_send_inactivity_ping.apply_async.called)

    def test_should_not_ping_for_excused_user(self, mock_send_inactivity_ping):
        # given
        user = UserMainRequestorFactory()
        character = create_character_from_user(user=user)
        last_login = now() - dt.timedelta(days=4)
        create_character_online_status(
            character=character,
            last_login=last_login,
            last_logout=last_login + dt.timedelta(hours=4),
        )
        LeaveOfAbsenceFactory(
            user=user,
            start=last_login,
            end=now().date() + dt.timedelta(days=7),
            is_approved=True,
        )
        InactivityPingConfigFactory(days=3)
        # when
        check_inactivity_for_user(user_pk=user.pk)
        # then
        self.assertFalse(mock_send_inactivity_ping.apply_async.called)

    def test_should_not_ping_when_already_pinged(self, mock_send_inactivity_ping):
        # given
        user = UserMainRequestorFactory()
        character = create_character_from_user(user=user)
        last_login = now() - dt.timedelta(days=4)
        create_character_online_status(
            character=character,
            last_login=last_login,
            last_logout=last_login + dt.timedelta(hours=4),
        )
        config = InactivityPingConfigFactory(days=3)
        InactivityPingFactory(user=user, config=config)
        # when
        check_inactivity_for_user(user_pk=user.pk)
        # then
        self.assertFalse(mock_send_inactivity_ping.apply_async.called)

    def test_should_ping_when_existing_loa_expired(self, mock_send_inactivity_ping):
        # given
        user = UserMainRequestorFactory()
        character = create_character_from_user(user=user)
        last_login = now() - dt.timedelta(days=4)
        create_character_online_status(
            character=character,
            last_login=last_login,
            last_logout=last_login + dt.timedelta(hours=4),
        )
        LeaveOfAbsenceFactory(
            user=user,
            start=now().date() - dt.timedelta(days=14),
            end=now().date() - dt.timedelta(days=7),
            is_approved=True,
        )
        InactivityPingConfigFactory(days=3)
        # when
        check_inactivity_for_user(user_pk=user.pk)
        # then
        self.assertTrue(mock_send_inactivity_ping.apply_async.called)

    def test_should_ping_when_loa_not_approved_yet(self, mock_send_inactivity_ping):
        # given
        user = UserMainRequestorFactory()
        character = create_character_from_user(user=user)
        last_login = now() - dt.timedelta(days=4)
        create_character_online_status(
            character=character,
            last_login=last_login,
            last_logout=last_login + dt.timedelta(hours=4),
        )
        LeaveOfAbsenceFactory(
            user=user,
            start=last_login,
            end=now().date() + dt.timedelta(days=7),
            is_approved=False,
        )
        InactivityPingConfigFactory(days=3)
        # when
        check_inactivity_for_user(user_pk=user.pk)
        # then
        self.assertTrue(mock_send_inactivity_ping.apply_async.called)


@patch(TASKS_PATH + ".check_inactivity_for_user", spec=True)
class TestCheckInactivity(NoSocketsTestCase):
    def test_should_check_inactivity_for_registered_users_only(
        self, mock_check_inactivity_for_user
    ):
        # given
        InactivityPingConfigFactory()
        user = UserMainRequestorFactory()
        create_character_from_user(user=user)
        UserMainRequestorFactory()  # will not be checked
        # when
        check_inactivity()
        # then
        users_pks_checked = {
            obj[1]["kwargs"]["user_pk"]
            for obj in mock_check_inactivity_for_user.apply_async.call_args_list
        }
        self.assertSetEqual(users_pks_checked, {user.pk})

    def test_should_do_nothing_when_no_config(self, mock_check_inactivity_for_user):
        # given
        user = UserMainRequestorFactory()
        create_character_from_user(user=user)
        UserMainRequestorFactory()  # will not be checked
        # when
        check_inactivity()
        # then
        users_pks_checked = {
            obj[1]["kwargs"]["user_pk"]
            for obj in mock_check_inactivity_for_user.apply_async.call_args_list
        }
        self.assertSetEqual(users_pks_checked, set())


class FakeResponse:
    def __init__(self, status: int, headers: dict = None):
        self.status = int(status)
        self.reason = "Dummy reason"
        self.text = "Dummy text"
        if headers:
            self.headers = {str(key): str(value) for key, value in headers.items()}


@patch(TASKS_PATH + ".cache.lock", spec=True)
@patch(TASKS_PATH + ".discord.SyncWebhook.send", spec=True)
class TestSendMessageToWebhook(NoSocketsTestCase):
    def test_send_message(self, mock_send, mock_cache_lock):
        # given
        webhook = WebhookFactory()
        # when
        send_message_to_webhook(webhook.pk, "dummy")
        # then
        self.assertTrue(mock_send.called)

    def test_retry_when_rate_limited(self, mock_send, mock_cache_lock):
        # given
        response = FakeResponse(
            status=HTTPStatus.TOO_MANY_REQUESTS,
            headers={"Retry-After": 99},
        )
        my_exception = discord.HTTPException(
            response=response, message="Test exception"
        )
        mock_send.side_effect = my_exception
        webhook = WebhookFactory()
        # when/then
        with self.assertRaises(CeleryRetry):
            send_message_to_webhook(webhook.pk, "dummy")

    def test_raise_error_when_other_http_error(self, mock_send, mock_cache_lock):
        # given
        response = FakeResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        my_exception = discord.HTTPException(
            response=response, message="Test exception"
        )
        mock_send.side_effect = my_exception
        webhook = WebhookFactory()
        # when/then
        with self.assertRaises(discord.HTTPException):
            send_message_to_webhook(webhook.pk, "dummy")
