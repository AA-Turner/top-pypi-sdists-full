# Django
from django.test import TestCase
from django.utils import timezone

# Alliance Auth (External Libs)
from eve_sde.models.types import ItemType

# AA Killstats
from killstats.models.general import EveEntity
from killstats.tests.testdata.eveentity import load_eveentity
from killstats.tests.testdata.load_allianceauth import load_allianceauth
from killstats.tests.testdata.utils import create_killmail

MODULE_PATH = "killstats.models.killstatsaudit"


class TestKillstatsAuditModel(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_allianceauth()
        load_eveentity()

        cls.killmail = create_killmail(
            killmail_id=1,
            killmail_date=timezone.datetime(2023, 1, 30, 0, 0, 0),
            victim=EveEntity.objects.get(id=1001),
            victim_ship=ItemType.objects.get(id=10001),
            victim_corporation_id=2001,
            victim_alliance_id=None,
            hash="hash1",
            victim_total_value=1_500_000,
            victim_fitted_value=1_500_000,
            victim_destroyed_value=1_500_000,
            victim_dropped_value=1_500_000,
            victim_region_id=1001,
            victim_solar_system_id=2001,
            victim_position_x=1.0,
            victim_position_y=1.0,
            victim_position_z=1.0,
        )
        cls.killmail2 = create_killmail(
            killmail_id=2,
            killmail_date=timezone.now(),
            victim=EveEntity.objects.get(id=1001),
            victim_ship=ItemType.objects.get(id=30001),
            victim_corporation_id=2001,
            victim_alliance_id=3001,
            hash="hash2",
            victim_total_value=1000,
            victim_fitted_value=500,
            victim_destroyed_value=500,
            victim_dropped_value=500,
            victim_region_id=1001,
            victim_solar_system_id=2001,
            victim_position_x=1.0,
            victim_position_y=1.0,
            victim_position_z=1.0,
        )
        cls.killmail3 = create_killmail(
            killmail_id=3,
            killmail_date=timezone.now(),
            victim=EveEntity.objects.get(id=1001),
            victim_ship=ItemType.objects.get(id=670),
            victim_corporation_id=2001,
            victim_alliance_id=3001,
            hash="hash3",
            victim_total_value=1000,
            victim_fitted_value=500,
            victim_destroyed_value=500,
            victim_dropped_value=500,
            victim_region_id=1001,
            victim_solar_system_id=2001,
            victim_position_x=1.0,
            victim_position_y=1.0,
            victim_position_z=1.0,
        )

    def test_str(self):
        self.assertEqual(
            str(self.killmail),
            "Killmail 1 - 2023-01-30 00:00:00 - Gneuten - Victim Ship I (10001)",
        )

    def test_get_victim_name(self):
        expected_url = "Gneuten"
        self.assertEqual(self.killmail.get_or_unknown_victim_name(), expected_url)

    def test_get_victim_ship_name(self):
        expected_url = "Victim Ship I"
        self.assertEqual(self.killmail.get_or_unknown_victim_ship_name(), expected_url)

    def test_evaluate_zkb_link(self):
        expected_url = "https://zkillboard.com/character/1001/"
        self.assertEqual(self.killmail.evaluate_zkb_link(), expected_url)

        self.killmail.victim.category = "corporation"
        expected_url = "https://zkillboard.com/corporation/2001/"
        self.assertEqual(self.killmail.evaluate_zkb_link(), expected_url)

        self.killmail2.victim.category = "alliance"
        expected_url = "https://zkillboard.com/alliance/3001/"
        self.assertEqual(self.killmail2.evaluate_zkb_link(), expected_url)
