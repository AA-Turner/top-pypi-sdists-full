# Standard Library
from datetime import timedelta
from unittest.mock import Mock, patch

# Django
from django.core.cache import cache
from django.test import RequestFactory, override_settings
from django.utils import timezone

# AA Killstats
from killstats import __title__
from killstats.constants import LAST_REQUEST_KEY, RETRY_AFTER_KEY
from killstats.helpers.killmail import KillmailBody
from killstats.tests import NoSocketsTestCase
from killstats.tests.testdata.load_allianceauth import load_allianceauth

MODULE_PATH = "killstats.helpers.killmail"


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
class TestKillmailHelper(NoSocketsTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_allianceauth()
        cls.factory = RequestFactory()

    def setUp(self) -> None:
        cache.clear()

    @patch(MODULE_PATH + ".time.sleep")
    def test_rate_limit_waits_for_retry_after(self, mocked_sleep):
        now = timezone.now()
        retry_after = now + timedelta(seconds=0.75)
        cache.set(RETRY_AFTER_KEY, retry_after)

        with patch(MODULE_PATH + ".timezone.now", return_value=now):
            result = KillmailBody._rate_limit()

        self.assertTrue(result)
        mocked_sleep.assert_called_once_with(0.75)

    @patch(MODULE_PATH + ".time.sleep")
    def test_rate_limit_waits_when_within_timeout(self, mocked_sleep):
        now = timezone.now()
        # min_interval = 1 / 2 = 0.5s, elapsed = 0.2s => wait = 0.3s
        last_request = now - timedelta(seconds=0.2)
        cache.set(LAST_REQUEST_KEY, last_request.isoformat())

        with (
            patch(MODULE_PATH + ".KILLSTATS_MAX_ZKB_PER_SEC", 2),
            patch(MODULE_PATH + ".KILLSTATS_ZKB_RATE_TIMEOUT", 0.5),
            patch(MODULE_PATH + ".timezone.now", return_value=now),
        ):
            result = KillmailBody._rate_limit()

        self.assertTrue(result)
        mocked_sleep.assert_called_once_with(0.3)

    @patch(MODULE_PATH + ".time.sleep")
    def test_rate_limit_skips_when_wait_exceeds_timeout(self, mocked_sleep):
        now = timezone.now()
        # min_interval = 1 / 2 = 0.5s, elapsed = 0.1s => wait = 0.4s (> timeout 0.2s)
        last_request = now - timedelta(seconds=0.1)
        cache.set(LAST_REQUEST_KEY, last_request.isoformat())

        with (
            patch(MODULE_PATH + ".KILLSTATS_MAX_ZKB_PER_SEC", 2),
            patch(MODULE_PATH + ".KILLSTATS_ZKB_RATE_TIMEOUT", 0.2),
            patch(MODULE_PATH + ".timezone.now", return_value=now),
        ):
            result = KillmailBody._rate_limit()

        self.assertFalse(result)
        mocked_sleep.assert_not_called()

    @patch(MODULE_PATH + ".requests.get")
    @patch.object(KillmailBody, "_rate_limit", return_value=False)
    def test_get_sequence_from_r2z2_returns_none_when_rate_limited(
        self, _mock_rate_limit, mock_requests_get
    ):
        result = KillmailBody.get_sequence_from_r2z2()

        self.assertIsNone(result)
        mock_requests_get.assert_not_called()

    @patch(MODULE_PATH + ".requests.get")
    @patch.object(KillmailBody, "_too_many_requests_delay", return_value=False)
    @patch.object(KillmailBody, "_rate_limit", return_value=True)
    def test_get_sequence_from_r2z2_returns_sequence(
        self, _mock_rate_limit, _mock_delay, mock_requests_get
    ):
        response = Mock()
        response.json.return_value = {"sequence": 123456}
        mock_requests_get.return_value = response

        result = KillmailBody.get_sequence_from_r2z2()

        self.assertEqual(result, 123456)
        self.assertIsNotNone(cache.get(LAST_REQUEST_KEY))
        mock_requests_get.assert_called_once()

    @patch(MODULE_PATH + ".requests.get")
    @patch.object(KillmailBody, "_too_many_requests_delay", return_value=True)
    @patch.object(KillmailBody, "_rate_limit", return_value=True)
    def test_get_sequence_from_r2z2_returns_none_on_too_many_requests(
        self, _mock_rate_limit, _mock_delay, mock_requests_get
    ):
        response = Mock()
        response.json.return_value = {"sequence": 123456}
        mock_requests_get.return_value = response

        result = KillmailBody.get_sequence_from_r2z2()

        self.assertIsNone(result)

    @patch(MODULE_PATH + ".requests.get")
    @patch.object(KillmailBody, "_rate_limit", return_value=True)
    def test_create_from_r2z2_sequence_returns_none_on_worker_shutdown(
        self, _mock_rate_limit, mock_requests_get
    ):
        cache.set(f"{__title__.upper()}_WORKER_SHUTDOWN", True)

        result = KillmailBody.create_from_r2z2_sequence(123456)

        self.assertIsNone(result)
        mock_requests_get.assert_not_called()

    @patch(MODULE_PATH + ".requests.get")
    @patch.object(KillmailBody, "_create_from_dict")
    @patch.object(KillmailBody, "_too_many_requests_delay", return_value=False)
    @patch.object(KillmailBody, "_rate_limit", return_value=True)
    def test_create_from_r2z2_sequence_returns_killmail(
        self,
        _mock_rate_limit,
        _mock_delay,
        mock_create_from_dict,
        mock_requests_get,
    ):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"killmail_id": 999999}
        mock_requests_get.return_value = response

        expected_killmail = Mock()
        mock_create_from_dict.return_value = expected_killmail

        result = KillmailBody.create_from_r2z2_sequence(123456)

        self.assertEqual(result, expected_killmail)
        mock_create_from_dict.assert_called_once_with({"killmail_id": 999999})
        self.assertIsNotNone(cache.get(LAST_REQUEST_KEY))
