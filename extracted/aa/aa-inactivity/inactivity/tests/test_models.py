import datetime as dt
from unittest.mock import patch

from django.utils.timezone import now

from app_utils.testing import NoSocketsTestCase

from .factories import (
    GroupFactory,
    InactivityPingConfigFactory,
    InactivityPingFactory,
    LeaveOfAbsenceFactory,
    StateFactory,
    UserMainRequestorFactory,
    WebhookFactory,
)

MODELS_PATH = "inactivity.models"
TASKS_PATH = "inactivity.tasks"


class TestInactivityPing(NoSocketsTestCase):
    def test_str_normal(self):
        # given
        ping = InactivityPingFactory()
        # when
        result = str(ping)
        # then
        self.assertIn(ping.user.last_name, result)

    def test_str_user_without_main(self):
        # given
        ping = InactivityPingFactory(user=UserMainRequestorFactory())
        # when
        result = str(ping)
        # then
        self.assertTrue(result)


class TestInactivityPingConfig(NoSocketsTestCase):
    def test_str_normal(self):
        # given
        ping = InactivityPingConfigFactory()
        # when
        result = str(ping)
        # then
        self.assertTrue(result)


class TestInactivityPingConfigIsApplicableTo(NoSocketsTestCase):
    def test_true_when_no_group_or_state_set(self):
        # given
        config = InactivityPingConfigFactory()
        user = UserMainRequestorFactory()
        # when/then
        self.assertTrue(config.is_applicable_to(user))

    def test_true_when_group_is_matching(self):
        # given
        group = GroupFactory()
        config = InactivityPingConfigFactory(groups=[group])
        user = UserMainRequestorFactory(groups=[group])
        # when/then
        self.assertTrue(config.is_applicable_to(user))

    def test_false_when_group_is_not_matching(self):
        # given
        group_1 = GroupFactory()
        group_2 = GroupFactory()
        config = InactivityPingConfigFactory(groups=[group_1])
        user = UserMainRequestorFactory(groups=[group_2])
        # when/then
        self.assertFalse(config.is_applicable_to(user))

    def test_true_when_state_is_matching(self):
        # given
        user = UserMainRequestorFactory()
        state = StateFactory(member_characters=[user.profile.main_character])
        config = InactivityPingConfigFactory(states=[state])
        # when/then
        self.assertTrue(config.is_applicable_to(user))

    def test_false_when_state_is_not_matching(self):
        # given
        user = UserMainRequestorFactory()
        StateFactory(member_characters=[user.profile.main_character])
        state_2 = StateFactory()
        config = InactivityPingConfigFactory(states=[state_2])
        # when/then
        self.assertFalse(config.is_applicable_to(user))


class TestLeaveOfAbsence(NoSocketsTestCase):
    def test_str(self):
        # given
        loa = LeaveOfAbsenceFactory()
        # when/then
        self.assertIsInstance(str(loa), str)

    def test_should_set_created_at_when_created(self):
        # when
        my_now = now()
        with patch(MODELS_PATH + ".now", lambda: my_now):
            obj = LeaveOfAbsenceFactory()
        # then
        self.assertEqual(obj.created_at, my_now)

    def test_should_not_update_created_at_when_changed(self):
        # given
        my_dt = now() - dt.timedelta(days=3)
        obj = LeaveOfAbsenceFactory(created_at=my_dt)
        # when
        obj.save()
        # then
        self.assertEqual(obj.created_at, my_dt)


@patch(TASKS_PATH + ".send_message_to_webhook", spec=True)
class TestWebhook(NoSocketsTestCase):
    def test_send_message(self, mock_send_message_to_webhook):
        # given
        webhook = WebhookFactory()
        # when
        webhook.send_message("dummy")
        # then
        self.assertTrue(mock_send_message_to_webhook.apply_async.called)
