"""Unit tests for KillmailBody helper class."""

# Standard Library
from datetime import timedelta
from http import HTTPStatus
from unittest.mock import Mock, patch

# Third Party
import pook

# Django
from django.core.cache import cache
from django.test import override_settings
from django.utils import timezone

# AA Killstats
from killstats import __title__
from killstats.constants import LAST_REQUEST_KEY, RETRY_AFTER_KEY
from killstats.helpers.killmailbody import (
    KillboardException,
    KillmailBody,
    KillmailDoesNotExist,
)
from killstats.models import EveEntity
from killstats.tests import AuthTestCase
from killstats.tests.testdata.killstats import KillmailBodyFactory

APP_SETTINGS_PATH = "killstats.app_settings"
MODULE_PATH = "killstats.helpers.killmailbody"


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
class TestKillmailHelper(AuthTestCase):
    def setUp(self) -> None:
        super().setUp()
        cache.clear()

    @patch(MODULE_PATH + ".time.sleep")
    def test_should_wait_for_retry_after(self, mocked_sleep):
        # Test Data
        now = timezone.now()
        retry_after = now + timedelta(seconds=0.75)
        cache.set(RETRY_AFTER_KEY, retry_after)

        # Test Action
        with patch(MODULE_PATH + ".timezone.now", return_value=now):
            result = KillmailBody._rate_limit()

        # Expected Result
        self.assertTrue(result)
        mocked_sleep.assert_called_once_with(0.75)

    @patch(MODULE_PATH + ".time.sleep")
    def test_should_wait_when_within_timeout(self, mocked_sleep):
        # Test Data
        now = timezone.now()
        last_request = now - timedelta(seconds=0.2)
        cache.set(LAST_REQUEST_KEY, last_request.isoformat())

        # Test Action
        with (
            patch(APP_SETTINGS_PATH + ".KILLSTATS_MAX_ZKB_PER_SEC", 2),
            patch(APP_SETTINGS_PATH + ".KILLSTATS_ZKB_RATE_TIMEOUT", 0.5),
            patch(MODULE_PATH + ".timezone.now", return_value=now),
        ):
            result = KillmailBody._rate_limit()

        # Expected Result
        self.assertTrue(result)
        mocked_sleep.assert_called_once_with(0.3)

    @patch(MODULE_PATH + ".time.sleep")
    def test_should_skip_when_wait_exceeds_timeout(self, mocked_sleep):
        # Test Data
        now = timezone.now()
        last_request = now - timedelta(seconds=0.1)
        cache.set(LAST_REQUEST_KEY, last_request.isoformat())

        # Test Action
        with (
            patch(APP_SETTINGS_PATH + ".KILLSTATS_MAX_ZKB_PER_SEC", 2),
            patch(APP_SETTINGS_PATH + ".KILLSTATS_ZKB_RATE_TIMEOUT", 0.2),
            patch(MODULE_PATH + ".timezone.now", return_value=now),
        ):
            result = KillmailBody._rate_limit()

        # Expected Result
        self.assertFalse(result)
        mocked_sleep.assert_not_called()

    @patch(MODULE_PATH + ".requests.get")
    @patch.object(KillmailBody, "_rate_limit", return_value=False)
    def test_should_return_none_from_sequence_when_rate_limited(
        self, _mock_rate_limit, mock_requests_get
    ):
        # Test Action
        result = KillmailBody.get_sequence()

        # Expected Result
        self.assertIsNone(result)
        mock_requests_get.assert_not_called()

    @patch(MODULE_PATH + ".requests.get")
    @patch.object(KillmailBody, "_too_many_requests_delay", return_value=False)
    @patch.object(KillmailBody, "_rate_limit", return_value=True)
    def test_should_return_sequence(
        self, _mock_rate_limit, _mock_delay, mock_requests_get
    ):
        # Test Data
        response = Mock()
        response.json.return_value = {"sequence": 123456}
        mock_requests_get.return_value = response

        # Test Action
        result = KillmailBody.get_sequence()

        # Expected Result
        self.assertEqual(result, 123456)
        self.assertIsNotNone(cache.get(LAST_REQUEST_KEY))
        mock_requests_get.assert_called_once()

    @patch(MODULE_PATH + ".requests.get")
    @patch.object(KillmailBody, "_too_many_requests_delay", return_value=True)
    @patch.object(KillmailBody, "_rate_limit", return_value=True)
    def test_should_return_none_from_sequence_on_too_many_requests(
        self, _mock_rate_limit, _mock_delay, mock_requests_get
    ):
        # Test Data
        response = Mock()
        response.json.return_value = {"sequence": 123456}
        mock_requests_get.return_value = response

        # Test Action
        result = KillmailBody.get_sequence()

        # Expected Result
        self.assertIsNone(result)

    @patch(MODULE_PATH + ".requests.get")
    @patch.object(KillmailBody, "_rate_limit", return_value=True)
    def test_should_return_none_from_sequence_on_worker_shutdown(
        self, _mock_rate_limit, mock_requests_get
    ):
        # Test Data
        cache.set(f"{__title__.upper()}_WORKER_SHUTDOWN", True)

        # Test Action
        result = KillmailBody.create_from_sequence(123456)

        # Expected Result
        self.assertIsNone(result)
        mock_requests_get.assert_not_called()

    @patch(MODULE_PATH + ".requests.get")
    @patch.object(KillmailBody, "_too_many_requests_delay", return_value=False)
    @patch.object(KillmailBody, "_rate_limit", return_value=True)
    def test_should_return_killmail_from_sequence(
        self,
        _mock_rate_limit,
        _mock_delay,
        mock_requests_get,
    ):
        # Test Data
        killmailbody = KillmailBodyFactory()
        response = Mock()
        response.status_code = 200
        response.json.return_value = killmailbody.as_dict()
        mock_requests_get.return_value = response

        # Test Action
        result = KillmailBody.create_from_sequence(killmailbody.sequence_id)

        # Expected Result
        self.assertEqual(result.sequence_id, killmailbody.sequence_id)
        self.assertEqual(result.victim.character_id, killmailbody.victim.character_id)
        self.assertIsNotNone(cache.get(LAST_REQUEST_KEY))

    @patch(MODULE_PATH + ".requests.get")
    @patch.object(KillmailBody, "_too_many_requests_delay", return_value=False)
    @patch.object(KillmailBody, "_rate_limit", return_value=True)
    def test_should_raise_validation_error(
        self,
        _mock_rate_limit,
        _mock_delay,
        mock_requests_get,
    ):
        # Test Data
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"invalid": "data"}
        mock_requests_get.return_value = response

        # Test Action & Expected Result
        killmail_body = KillmailBody.create_from_sequence(123456)
        self.assertIsNone(killmail_body)

    def test_convenience_properties_should_return_underlying_values(self):
        # Test Data
        killmail = KillmailBodyFactory()

        # Test Action & Expected Result
        self.assertEqual(killmail.id, killmail.killmail_id)
        self.assertEqual(killmail.killmail_time, killmail.esi.killmail_time)
        self.assertEqual(killmail.solar_system_id, killmail.esi.solar_system_id)
        self.assertEqual(killmail.victim, killmail.esi.victim)
        self.assertEqual(killmail.attackers, killmail.esi.attackers)

    def test_attackers_distinct_alliance_ids_should_return_unique_alliances(self):
        # Test Data
        killmail = KillmailBodyFactory()
        killmail.esi.attackers[0].alliance_id = 99001

        # Test Action
        alliances = killmail.attackers_distinct_alliance_ids()

        # Expected Result
        self.assertIn(99001, alliances)

    def test_attackers_distinct_corporation_ids_should_return_unique_corporations(self):
        # Test Data
        killmail = KillmailBodyFactory()
        killmail.esi.attackers[0].corporation_id = 98001

        # Test Action
        corporations = killmail.attackers_distinct_corporation_ids()

        # Expected Result
        self.assertIn(98001, corporations)

    def test_serialization_helpers_should_produce_valid_dict_and_json(self):
        # Test Data
        killmail = KillmailBodyFactory()

        # Test Action
        as_dict = killmail.as_dict()
        to_dict = killmail.to_dict()
        as_json = killmail.as_json()
        to_json = killmail.to_json()
        repr_str = repr(killmail)

        # Expected Result
        self.assertIsInstance(as_dict, dict)
        self.assertEqual(as_dict, to_dict)
        self.assertIsInstance(as_json, str)
        self.assertEqual(as_json, to_json)
        self.assertIn(str(killmail.killmail_id), repr_str)

    def test_storage_lifecycle_save_get_and_delete(self):
        # Test Data
        killmail = KillmailBodyFactory()

        # Test Action: Save
        killmail.save()

        # Expected Result: Get
        loaded = KillmailBody.get(killmail.killmail_id)
        self.assertEqual(loaded.killmail_id, killmail.killmail_id)

        # Test Action: Delete
        killmail.delete()

        # Expected Result: Get raises DoesNotExist
        with self.assertRaises(KillmailDoesNotExist):
            KillmailBody.get(killmail.killmail_id)

    def test_storage_get_should_raise_killboard_exception_on_corrupt_data(self):
        # Test Data
        cache_key = KillmailBody._storage_key(999999)
        cache.set(cache_key, "{invalid_json")

        # Test Action & Expected Result
        with self.assertRaises(KillboardException):
            KillmailBody.get(999999)

    def test_get_esi_killmail_bucket_remaining_should_return_cached_or_default(self):
        # Test Data: Default
        cache.delete("esi:bucket:killmail")
        self.assertEqual(KillmailBody.get_esi_killmail_bucket_remaining(), 1200)

        # Test Data: Cached int
        cache.set("esi:bucket:killmail", 450)
        self.assertEqual(KillmailBody.get_esi_killmail_bucket_remaining(), 450)

        # Test Data: Invalid value
        cache.set("esi:bucket:killmail", "not_a_number")
        self.assertEqual(KillmailBody.get_esi_killmail_bucket_remaining(), 1200)

    @pook.on
    def test_create_names_bulk_should_delegate_when_ids_provided(self):
        # Test Data
        killmail = KillmailBodyFactory()
        pook.post(
            "https://esi.evetech.net/universe/names",
            reply=HTTPStatus.OK,
            response_json=[
                {"id": 1001, "name": "Test Name 1", "category": "character"},
                {"id": 1002, "name": "Test Name 2", "category": "character"},
            ],
        )
        # Test Action & Expected Result
        self.assertTrue(killmail.create_names_bulk([1001, 1002]))
        self.assertFalse(killmail.create_names_bulk([]))

    @pook.on
    def test_get_or_create_entity_should_delegate_to_manager(self):
        # Test Data
        pook.post(
            "https://esi.evetech.net/universe/names",
            reply=HTTPStatus.OK,
            response_json=[
                {"id": 1001, "name": "Test Name 1", "category": "character"}
            ],
        )
        # Test Action
        result = KillmailBody.get_or_create_entity(1001)
        # Expected Result
        self.assertEqual(result, EveEntity.objects.filter(id=1001).first())

    def test_get_region_id_should_return_none_when_solar_system_not_found(self):
        # Test Action & Expected Result
        self.assertIsNone(KillmailBody.get_region_id(99999999))

    def test_too_many_requests_delay_handling(self):
        # Test Data: Status 200
        ok_response = Mock()
        ok_response.status_code = HTTPStatus.OK
        self.assertFalse(KillmailBody._too_many_requests_delay(ok_response))

        # Test Data: Status 429
        rate_limited_response = Mock()
        rate_limited_response.status_code = HTTPStatus.TOO_MANY_REQUESTS
        rate_limited_response.headers = {"Retry-After": "5"}

        # Test Action
        result = KillmailBody._too_many_requests_delay(rate_limited_response)

        # Expected Result
        self.assertTrue(result)
        self.assertIsNotNone(cache.get(f"{__title__.upper()}_RETRY_AFTER"))
