"""Unit tests for KillboardApiEndpoints (V2)."""

# Standard Library
from datetime import datetime, timezone
from http import HTTPStatus

# Third Party
# Django Ninja
from ninja.testing import TestClient

# Django
from django.core.cache import cache

# AA Killstats
from killstats.api import api
from killstats.tests import AuthTestCase
from killstats.tests.testdata.killstats import (
    AttackerFactory,
    EveEntityCorporationFactory,
    KillmailFactory,
    UserMainFactory,
)


class TestKillboardApi(AuthTestCase):
    def setUp(self):
        super().setUp()
        cache.clear()
        self.client = TestClient(api)
        self.user = UserMainFactory()

    def tearDown(self):
        cache.clear()
        super().tearDown()

    def test_get_combat_summary_api_should_return_summary(self):
        # Test Data
        corp_id = 98000001
        corp_entity = EveEntityCorporationFactory(id=corp_id)
        test_date = datetime(2026, 9, 15, 12, 0, 0, tzinfo=timezone.utc)
        km = KillmailFactory(
            killmail_date=test_date,
            victim_corporation_id=corp_id,
            victim_total_value=5000000,
        )
        AttackerFactory(
            killmail=km,
            corporation=corp_entity,
        )

        # Test Action
        response = self.client.get(
            f"/stats/v2/summary/corporation/{corp_id}/?year=2026&month=9",
            user=self.user,
        )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertEqual(data["total_kills"], 1)
        self.assertGreaterEqual(data["active_pvpers"], 1)
        self.assertEqual(data["destroyed_isk"], 5000000)
        self.assertEqual(data["lost_isk"], 5000000)

    def test_get_combat_summary_api_should_return_403_when_no_permission(self):
        # Test Data
        unauthed_user = UserMainFactory(permissions__=[])

        # Test Action
        response = self.client.get(
            "/stats/v2/summary/corporation/98000001/?year=2026&month=9",
            user=unauthed_user,
        )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_get_top_attackers_api_should_return_top_attackers(self):
        # Test Data
        corp_id = 98000002
        corp_entity = EveEntityCorporationFactory(id=corp_id)
        test_date = datetime(2026, 9, 15, 12, 0, 0, tzinfo=timezone.utc)
        km = KillmailFactory(
            killmail_date=test_date,
            victim_total_value=10000000,
        )
        AttackerFactory(
            killmail=km,
            corporation=corp_entity,
        )

        # Test Action
        response = self.client.get(
            f"/stats/v2/attackers/corporation/{corp_id}/?year=2026&month=9",
            user=self.user,
        )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertIn("pilots", data)
        self.assertEqual(len(data["pilots"]), 1)
        self.assertEqual(data["pilots"][0]["count"], 1)
        self.assertEqual(data["pilots"][0]["total_value"], 10000000)

    def test_get_top_attackers_api_should_return_403_when_no_permission(self):
        # Test Data
        unauthed_user = UserMainFactory(permissions__=[])

        # Test Action
        response = self.client.get(
            "/stats/v2/attackers/corporation/98000002/?year=2026&month=9",
            user=unauthed_user,
        )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_get_top_victims_api_should_return_top_victims(self):
        # Test Data
        corp_id = 98000003
        test_date = datetime(2026, 9, 15, 12, 0, 0, tzinfo=timezone.utc)
        KillmailFactory(
            killmail_date=test_date,
            victim_corporation_id=corp_id,
            victim_total_value=25000000,
        )

        # Test Action
        response = self.client.get(
            f"/stats/v2/victims/corporation/{corp_id}/?year=2026&month=9",
            user=self.user,
        )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertIn("pilots", data)
        self.assertEqual(len(data["pilots"]), 1)
        self.assertEqual(data["pilots"][0]["count"], 1)
        self.assertEqual(data["pilots"][0]["total_value"], 25000000)

    def test_get_top_victims_api_should_return_403_when_no_permission(self):
        # Test Data
        unauthed_user = UserMainFactory(permissions__=[])

        # Test Action
        response = self.client.get(
            "/stats/v2/victims/corporation/98000003/?year=2026&month=9",
            user=unauthed_user,
        )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
