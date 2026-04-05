# Standard Library
import json
from types import SimpleNamespace
from unittest.mock import Mock, patch

# Third Party
import requests

# Django
from django.core.cache import cache
from django.utils.timezone import datetime

# Alliance Auth (External Libs)
from eve_sde.models.types import ItemType

# AA Killstats
# Create a properly structured killmail object
from killstats.helpers.killmail import (
    KillmailBody,
    KillmailPosition,
    KillmailVictim,
    KillmailZkb,
)
from killstats.models.general import EveEntity
from killstats.models.killboard import Killmail
from killstats.tests import NoSocketsTestCase
from killstats.tests.testdata.esi_stub_openapi import (
    EsiEndpoint,
    create_esi_client_stub,
)
from killstats.tests.testdata.eveentity import load_eveentity
from killstats.tests.testdata.load_allianceauth import load_allianceauth

MODULE_PATH = "killstats.helpers.killmail"

KILLSTATS_ENDPOINTS = [
    EsiEndpoint(
        "Killmails",
        "GetKillmailsKillmailIdKillmailHash",
        "killmail_id",
        "killmail_hash",
    ),
]


class TestKillmailBody(NoSocketsTestCase):
    """Tests for KillmailBody.get_single_killmail method"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_allianceauth()
        load_eveentity()

        # Load test data
        with open("killstats/tests/zkb_package.json", encoding="utf-8") as f:
            cls.zkb_package_data = json.load(f)

        # Sample killmail data from ESI
        cls.esi_killmail_data = {
            "killmail_id": 121152845,
            "hash": "test_hash",
            "esi": {
                "killmail_id": 121152845,
                "killmail_time": "2024-06-15T12:30:45Z",
                "solar_system_id": 30004608,
                "victim": {
                    "character_id": 95538921,
                    "corporation_id": 98711194,
                    "alliance_id": 99012345,
                    "ship_type_id": 670,
                    "damage_taken": 1234,
                    "position": {"x": 123.0, "y": 456.0, "z": 789.0},
                },
                "attackers": [
                    {
                        "character_id": 1234567,
                        "corporation_id": 98098098,
                        "alliance_id": 99011111,
                        "ship_type_id": 11176,
                        "weapon_type_id": 3520,
                        "damage_done": 1234,
                        "final_blow": True,
                        "security_status": -10.0,
                    }
                ],
            },
            "zkb": {
                "hash": "zkb_test_hash",
                "fitted_value": 1000000.0,
                "total_value": 1000000.0,
                "points": 1,
            },
        }

    def setUp(self):
        """Clear cache before each test"""
        cache.clear()

    def tearDown(self):
        """Clear cache after each test"""
        cache.clear()

    @patch(MODULE_PATH + ".esi")
    @patch(MODULE_PATH + ".requests.get")
    def test_get_single_killmail_success(self, mock_requests_get, mock_esi):
        """Test successful killmail retrieval"""
        killmail_id = 121152845

        # Mock zKillboard API response
        mock_zkb_response = Mock()
        mock_zkb_response.json.return_value = [self.zkb_package_data[0]]
        mock_zkb_response.raise_for_status = Mock()
        mock_zkb_response.status_code = 200

        # Configure requests.get to return different responses based on URL
        def get_side_effect(url, **kwargs):
            if "zkillboard.com" in url:
                return mock_zkb_response
            return Mock()

        mock_requests_get.side_effect = get_side_effect
        mock_esi.client = create_esi_client_stub(endpoints=KILLSTATS_ENDPOINTS)

        # Call the method
        result = KillmailBody.get_single_killmail(killmail_id)

        # Assertions
        self.assertIsNotNone(result)
        self.assertIsInstance(result, KillmailBody)
        self.assertEqual(result.id, killmail_id)
        self.assertEqual(mock_requests_get.call_count, 1)  # zKillboard

    @patch("killstats.helpers.killmail.requests.get")
    def test_get_single_killmail_from_cache(self, mock_requests_get):
        """Test that killmail is retrieved from cache if available"""
        killmail_id = 121152845

        victim = KillmailVictim(
            character_id=95538921,
            corporation_id=98711194,
            alliance_id=99012345,
            ship_type_id=670,
            damage_taken=1234,
        )
        position = KillmailPosition(x=0.0, y=0.0, z=0.0)
        zkb = KillmailZkb(
            hash="test_hash", fitted_value=1000000.0, total_value=1000000.0, points=1
        )

        # Create KillmailBody and serialize it properly
        killmail_body = KillmailBody(
            id=killmail_id,
            time=datetime(2024, 6, 15, 12, 30, 45),
            victim=victim,
            attackers=[],
            position=position,
            zkb=zkb,
            solar_system_id=30004608,
        )

        # Use correct cache key format from STORAGE_BASE_KEY
        cache_key = f"killstats_storage__KILLMAIL_{killmail_id}"
        cache.set(cache_key, killmail_body.asjson())

        # Call the method
        result = KillmailBody.get_single_killmail(killmail_id)

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result.id, killmail_id)
        # Should not call external APIs when data is in cache
        mock_requests_get.assert_not_called()

        # Should not call external APIs when data is in cache
        mock_requests_get.assert_not_called()

    @patch("killstats.helpers.killmail.requests.get")
    def test_get_single_killmail_already_exists(self, mock_requests_get):
        """Test that None is returned if killmail already exists in database"""
        killmail_id = 121152845

        # Create required entities for the killmail
        victim_entity = EveEntity.objects.get(id=1001)
        victim_ship = ItemType.objects.get(id=670)

        # Create existing killmail in database
        Killmail.objects.create(
            killmail_id=killmail_id,
            victim=victim_entity,
            victim_ship=victim_ship,
            victim_solar_system_id=30004608,
            victim_corporation_id=2001,
            victim_alliance_id=3001,
            victim_total_value=1000000,
            hash="test_hash_12345",
        )

        # Mock zKillboard API response
        mock_zkb_response = Mock()
        mock_zkb_response.json.return_value = [self.zkb_package_data[0]]
        mock_zkb_response.raise_for_status = Mock()
        mock_requests_get.return_value = mock_zkb_response

        # Call the method
        result = KillmailBody.get_single_killmail(killmail_id)

        # Assertions
        self.assertIsNone(result)
        mock_requests_get.assert_called_once()

    @patch(MODULE_PATH + ".requests.get")
    def test_get_single_killmail_zkb_http_error(self, mock_requests_get):
        """Test that HTTPError from zKillboard is handled"""
        killmail_id = 121152845

        # Mock zKillboard API error
        mock_zkb_response = Mock()
        mock_zkb_response.raise_for_status.side_effect = requests.HTTPError(
            "Test 404 Not Found"
        )
        mock_requests_get.return_value = mock_zkb_response

        # Call the method and expect ValueError
        with self.assertRaises(ValueError):
            KillmailBody.get_single_killmail(killmail_id)

    @patch(MODULE_PATH + ".requests.get")
    def test_get_single_killmail_zkb_timeout(self, mock_requests_get):
        """Test that Timeout from zKillboard is handled"""
        killmail_id = 121152845

        # Mock zKillboard API timeout
        mock_zkb_response = Mock()
        mock_zkb_response.raise_for_status.side_effect = requests.Timeout(
            "Connection timed out"
        )
        mock_requests_get.return_value = mock_zkb_response
        with self.assertRaises(ValueError):
            KillmailBody.get_single_killmail(killmail_id)

    @patch(MODULE_PATH + ".esi")
    @patch(MODULE_PATH + ".requests.get")
    def test_get_single_killmail_caches_result(self, mock_requests_get, mock_esi):
        """Test that successful killmail is cached after retrieval"""
        killmail_id = 121152845

        # Mock zKillboard API response
        mock_zkb_response = Mock()
        mock_zkb_response.json.return_value = [self.zkb_package_data[0]]
        mock_zkb_response.raise_for_status = Mock()
        mock_zkb_response.status_code = 200

        # Configure requests.get to return different responses based on URL
        def get_side_effect(url, **kwargs):
            if "zkillboard.com" in url:
                return mock_zkb_response
            return Mock()

        mock_requests_get.side_effect = get_side_effect
        mock_esi.client = create_esi_client_stub(endpoints=KILLSTATS_ENDPOINTS)
        # Ensure cache is empty before test
        cache_key = f"killstats_storage__KILLMAIL_{killmail_id}"
        self.assertIsNone(cache.get(cache_key), "Cache should be empty before test")

        # Call the method
        result = KillmailBody.get_single_killmail(killmail_id)

        # Verify result is valid
        self.assertIsNotNone(result)
        self.assertIsInstance(result, KillmailBody)
        self.assertEqual(result.id, killmail_id)

        # Verify the killmail was cached
        cached_value = cache.get(cache_key)
        self.assertIsNotNone(
            cached_value, "Killmail should be cached after successful retrieval"
        )

        # Verify we can retrieve from cache
        cached_killmail = KillmailBody.from_json(cached_value)
        self.assertEqual(cached_killmail.id, killmail_id)
        self.assertEqual(
            cached_killmail.victim.character_id, result.victim.character_id
        )
