import datetime as dt
from http import HTTPStatus
from unittest.mock import patch

from memberaudit.tests.testdata.factories import (
    create_character_from_user,
    create_character_online_status,
)

from django.test import override_settings
from django.utils.timezone import now

from app_utils.testing import NoSocketsTestCase

from inactivity.models import LeaveOfAbsence, Webhook
from inactivity.tasks import check_inactivity

from .factories import (
    GroupFactory,
    InactivityPingConfigFactory,
    LeaveOfAbsenceFactory,
    UserMainManagerFactory,
    UserMainRequestorFactory,
    WebhookFactory,
)

MODELS_PATH = "inactivity.models"
TASKS_PATH = "inactivity.tasks"
VIEWS_PATH = "inactivity.views"


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
@patch(TASKS_PATH + ".discord.SyncWebhook.send", spec=True)
@patch(VIEWS_PATH + ".messages", spec=True)
class TestFrontend(NoSocketsTestCase):
    def test_should_create_new_request_and_notify_when_matching_webhook(
        self, mock_messages, mock_send
    ):
        # given
        group = GroupFactory()
        config = InactivityPingConfigFactory(groups=[group])
        WebhookFactory(
            ping_configs=[config], notification_types=[Webhook.NotificationType.LOA_NEW]
        )
        user = UserMainRequestorFactory(groups=[group])
        self.client.force_login(user)
        start = now().date() + dt.timedelta(days=3)
        end = start + dt.timedelta(days=7)
        # when
        response = self.client.post(
            "/inactivity/loa_requests/create",
            data={"start": start, "end": end, "notes": "test"},
        )
        # then
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, "/inactivity/")
        obj = LeaveOfAbsence.objects.first()
        self.assertEqual(obj.user, user)
        self.assertEqual(obj.start, start)
        self.assertEqual(obj.end, end)
        self.assertEqual(obj.notes, "test")
        self.assertTrue(mock_messages.info.called)
        self.assertTrue(mock_send.called)

    def test_should_create_new_request_and_not_notify_when_no_matching_webhook(
        self, mock_messages, mock_send
    ):
        # given
        group = GroupFactory()
        config = InactivityPingConfigFactory(groups=[group])
        WebhookFactory(
            ping_configs=[config],
            notification_types=[Webhook.NotificationType.LOA_APPROVED],
        )
        user = UserMainRequestorFactory()
        self.client.force_login(user)
        start = now().date() + dt.timedelta(days=3)
        # when
        self.client.post(
            "/inactivity/loa_requests/create", data={"start": start, "notes": "test"}
        )
        # then
        self.assertTrue(LeaveOfAbsence.objects.filter(user=user, start=start).exists())
        self.assertTrue(mock_messages.info.called)
        self.assertFalse(mock_send.called)

    def test_should_approve_request_and_notify(self, mock_messages, mock_send):
        # given
        WebhookFactory()
        loa = LeaveOfAbsenceFactory()
        user = UserMainManagerFactory()
        self.client.force_login(user)
        # when
        response = self.client.get(f"/inactivity/loa_requests/{loa.pk}/approve")
        # then
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, "/inactivity/manage_requests")
        loa.refresh_from_db()
        self.assertEqual(loa.approver, user)
        self.assertTrue(mock_messages.success.called)
        self.assertTrue(mock_send)

    def test_manager_can_reject_a_request(self, mock_messages, mock_send):
        # given
        WebhookFactory()
        loa = LeaveOfAbsenceFactory()
        manager = UserMainManagerFactory()
        self.client.force_login(manager)
        # when
        response = self.client.post(
            f"/inactivity/loa_requests/{loa.pk}/reject",
            data={"reason": "do not like you much"},
        )
        # then
        loa.refresh_from_db()
        self.assertEqual(loa.approver, manager)
        self.assertTrue(loa.reason)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, "/inactivity/manage_requests")


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
@patch(TASKS_PATH + ".discord.SyncWebhook.send", spec=True)
@patch(TASKS_PATH + ".notify.danger", spec=True)
class TestTasksEnd2End(NoSocketsTestCase):
    def test_check_inactivity_e2e(self, mock_notify_user, mock_send):
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
        WebhookFactory()
        mock_notify_user.reset_mock()
        mock_send.reset_mock()
        # when
        check_inactivity.delay()
        # then
        self.assertTrue(mock_notify_user.called)
        self.assertTrue(mock_send.called)
