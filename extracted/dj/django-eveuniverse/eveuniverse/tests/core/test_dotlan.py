from django.test import TestCase

from eveuniverse.core import dotlan


class TestDotlan(TestCase):
    def test_alliance_url(self):
        self.assertEqual(
            dotlan.alliance_url("Wayne Enterprices"),
            "https://evemaps.dotlan.net/alliance/Wayne_Enterprices",
        )

    def test_corporation_url(self):
        self.assertEqual(
            dotlan.corporation_url("Wayne Technology"),
            "https://evemaps.dotlan.net/corp/Wayne_Technology",
        )
        self.assertEqual(
            dotlan.corporation_url("Crédit Agricole"),
            "https://evemaps.dotlan.net/corp/Cr%C3%A9dit_Agricole",
        )

    def test_faction_url(self):
        self.assertEqual(
            dotlan.faction_url("Amarr Empire"),
            "https://evemaps.dotlan.net/factionwarfare/Amarr_Empire",
        )

    def test_region_url(self):
        self.assertEqual(
            dotlan.region_url("Black Rise"), "https://evemaps.dotlan.net/map/Black_Rise"
        )

    def test_solar_system_url(self):
        self.assertEqual(
            dotlan.solar_system_url("Jita"), "https://evemaps.dotlan.net/system/Jita"
        )

    def test_station_url(self):
        self.assertEqual(
            dotlan.station_url("Rakapas V - Home Guard Assembly Plant"),
            "https://evemaps.dotlan.net/station/Rakapas_V_-_Home_Guard_Assembly_Plant",
        )
