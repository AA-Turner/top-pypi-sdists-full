"""Unit tests for KillboardStatsApiEndpoints (V2)."""

# Standard Library
from datetime import datetime, timezone
from http import HTTPStatus
from unittest.mock import patch

# Third Party
# Django Ninja
from ninja.testing import TestClient

# Django
from django.core.cache import cache
from django.test import override_settings

# AA Killstats
from killstats.api import api
from killstats.models.killboard import Killmail
from killstats.tests import AuthTestCase
from killstats.tests.testdata.killstats import (
    AttackerFactory,
    EveEntityCorporationFactory,
    KillmailFactory,
    UserMainFactory,
)

# cache_page keys cannot be rebuilt, so the endpoints run against LocMem;
# cache.clear() then only empties LocMem, not the shared Redis DB
LOCMEM_CACHE = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}


@override_settings(CACHES=LOCMEM_CACHE)
class TestKillboardStatsApi(AuthTestCase):
    def setUp(self):
        super().setUp()
        cache.clear()
        self.client = TestClient(api)
        self.user = UserMainFactory()

    def test_get_hall_endpoint_should_return_hall_of_fame_and_shame(self):
        # Test Data
        corp_id = 98000011
        corp_entity = EveEntityCorporationFactory(id=corp_id)
        test_date = datetime(2026, 9, 15, 12, 0, 0, tzinfo=timezone.utc)
        km = KillmailFactory(
            killmail_date=test_date,
            victim_corporation_id=corp_id,
            victim_total_value=50000000,
        )
        AttackerFactory(
            killmail=km,
            corporation=corp_entity,
            damage_done=5000,
        )

        # Test Action
        response = self.client.get(
            f"/hall/v2/corporation/{corp_id}/?year=2026&month=9",
            user=self.user,
        )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertIn("hall_of_fame", data)
        self.assertIn("hall_of_shame", data)

    def test_get_killmails_endpoint_should_return_killmails_list(self):
        # Test Data
        corp_id = 98000012
        corp_entity = EveEntityCorporationFactory(id=corp_id)
        test_date = datetime(2026, 9, 15, 12, 0, 0, tzinfo=timezone.utc)
        km = KillmailFactory(
            killmail_date=test_date,
            victim_corporation_id=corp_id,
            victim_total_value=7500000,
        )
        AttackerFactory(
            killmail=km,
            corporation=corp_entity,
        )

        # Test Action
        response = self.client.get(
            f"/killmails/corporation/{corp_id}/?year=2026&month=9&mode=all",
            user=self.user,
        )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertIn("killmails", data)
        self.assertIn("total", data)
        self.assertEqual(data["page"], 1)
        self.assertEqual(data["page_size"], 50)
        self.assertGreaterEqual(data["total"], 1)

    def test_get_killmails_endpoint_should_paginate(self):
        # Test Data
        corp_id = 98000014
        corp_entity = EveEntityCorporationFactory(id=corp_id)
        test_date = datetime(2026, 9, 15, 12, 0, 0, tzinfo=timezone.utc)
        for i in range(5):
            km = KillmailFactory(
                killmail_id=500000 + i,
                killmail_date=test_date,
                victim_corporation_id=corp_id,
            )
            AttackerFactory(killmail=km, corporation=corp_entity)

        # Test Action
        response = self.client.get(
            f"/killmails/corporation/{corp_id}/?year=2026&month=9&mode=all&page=2&page_size=2",
            user=self.user,
        )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertEqual(data["page"], 2)
        self.assertEqual(data["page_size"], 2)
        self.assertEqual(len(data["killmails"]), 2)
        self.assertEqual(data["total"], 5)

    def test_get_killmails_endpoint_should_filter_by_mode(self):
        # Test Data
        corp_id = 98000013
        corp_entity = EveEntityCorporationFactory(id=corp_id)
        test_date = datetime(2026, 9, 15, 12, 0, 0, tzinfo=timezone.utc)
        km = KillmailFactory(
            killmail_date=test_date,
            victim_corporation_id=corp_id,
            victim_total_value=8000000,
        )
        AttackerFactory(
            killmail=km,
            corporation=corp_entity,
        )

        # Test Action - Kills mode
        response_kills = self.client.get(
            f"/killmails/corporation/{corp_id}/?year=2026&month=9&mode=kills",
            user=self.user,
        )

        # Test Action - Losses mode
        response_losses = self.client.get(
            f"/killmails/corporation/{corp_id}/?year=2026&month=9&mode=losses",
            user=self.user,
        )

        # Expected Result
        self.assertEqual(response_kills.status_code, HTTPStatus.OK)
        self.assertEqual(response_losses.status_code, HTTPStatus.OK)

    def test_get_hall_endpoint_should_return_500_without_exception_text(self):
        # Test Data
        secret = "relation killstats_killmail does not exist"

        # Test Action
        with (
            patch.object(Killmail.objects, "filter", side_effect=RuntimeError(secret)),
            self.assertLogs("extensions.killstats.providers", level="ERROR") as logs,
        ):
            response = self.client.get(
                "/hall/v2/corporation/98000011/?year=2026&month=9",
                user=self.user,
            )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"error": "An internal error occurred."})
        self.assertNotIn(secret, response.content.decode())
        self.assertIn(secret, "\n".join(logs.output))

    def test_get_killmails_endpoint_should_return_500_without_exception_text(self):
        # Test Data
        secret = "relation killstats_killmail does not exist"

        # Test Action
        with (
            patch.object(
                Killmail.objects, "get_paged_ids", side_effect=RuntimeError(secret)
            ),
            self.assertLogs("extensions.killstats.providers", level="ERROR") as logs,
        ):
            response = self.client.get(
                "/killmails/corporation/98000012/?year=2026&month=9",
                user=self.user,
            )

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"error": "An internal error occurred."})
        self.assertNotIn(secret, response.content.decode())
        self.assertIn(secret, "\n".join(logs.output))
