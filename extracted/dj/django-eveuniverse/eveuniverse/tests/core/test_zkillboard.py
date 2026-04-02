from django.test import TestCase

from eveuniverse.core import zkillboard


class TestZkillboard(TestCase):
    def test_alliance_url(self):
        self.assertEqual(
            zkillboard.alliance_url(12345678),
            "https://zkillboard.com/alliance/12345678/",
        )

    def test_corporation_url(self):
        self.assertEqual(
            zkillboard.corporation_url(12345678),
            "https://zkillboard.com/corporation/12345678/",
        )

    def test_character_url(self):
        self.assertEqual(
            zkillboard.character_url(12345678),
            "https://zkillboard.com/character/12345678/",
        )

    def test_killmail_url(self):
        self.assertEqual(
            zkillboard.killmail_url(12345678), "https://zkillboard.com/kill/12345678/"
        )

    def test_region_url(self):
        self.assertEqual(
            zkillboard.region_url(12345678), "https://zkillboard.com/region/12345678/"
        )

    def test_solar_system_url(self):
        self.assertEqual(
            zkillboard.solar_system_url(12345678),
            "https://zkillboard.com/system/12345678/",
        )
