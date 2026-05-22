from typing import NamedTuple
from unittest.mock import patch

import pook
from django.test import TestCase

from eveuniverse.constants import EveGroupId
from eveuniverse.core import evexml
from eveuniverse.models import EveEntity
from eveuniverse.tests.testdata.factories_2 import (
    CitadelTypeFactory,
    EveEntityFactory,
    EveTypeFactory,
    ShipTypeFactory,
    StationTypeFactory,
)

MODEL_PATH = "eveuniverse.models.base"


class TestEveXml(TestCase):
    def test_should_remove_loc_tag_1(self):
        input = "<loc>Character</loc>"
        expected = "Character"
        self.assertHTMLEqual(evexml.remove_loc_tag(input), expected)

    def test_should_remove_loc_tag_2(self):
        input = "Character"
        expected = "Character"
        self.assertHTMLEqual(evexml.remove_loc_tag(input), expected)

    def test_should_detect_url(self):
        self.assertTrue(evexml.is_url("https://www.example.com/bla"))

    def test_should_detect_non_url(self):
        self.assertFalse(evexml.is_url("no-url"))

    @patch(MODEL_PATH + ".EVEUNIVERSE_LOAD_ASTEROID_BELTS", False)
    @patch(MODEL_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODEL_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODEL_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODEL_PATH + ".EVEUNIVERSE_LOAD_MOONS", False)
    @patch(MODEL_PATH + ".EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODEL_PATH + ".EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODEL_PATH + ".EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODEL_PATH + ".EVEUNIVERSE_LOAD_STATIONS", False)
    @patch(MODEL_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
    @pook.on
    def test_should_convert_links(self):
        # given
        ShipTypeFactory(id=603)
        StationTypeFactory(id=52678)
        CitadelTypeFactory(id=35825)
        EveTypeFactory(id=16159, eve_group__id=EveGroupId.ALLIANCE)
        EveTypeFactory(id=1376, eve_group__id=EveGroupId.CHARACTER)
        EveTypeFactory(id=2, eve_group__id=EveGroupId.CORPORATION)
        EveTypeFactory(id=5, eve_group__id=EveGroupId.SOLAR_SYSTEM)

        EveEntityFactory(
            id=1001, name="Bruce Wayne", category=EveEntity.CATEGORY_CHARACTER
        )
        EveEntityFactory(
            id=2001, name="Wayne Technologies", category=EveEntity.CATEGORY_CORPORATION
        )
        EveEntityFactory(
            id=3001, name="Wayne Enterprises", category=EveEntity.CATEGORY_ALLIANCE
        )
        EveEntityFactory(
            id=30004984, name="Abune", category=EveEntity.CATEGORY_SOLAR_SYSTEM
        )
        EveEntityFactory(
            id=60003760,
            name="Jita IV - Moon 4 - Caldari Navy Assembly Plant",
            category=EveEntity.CATEGORY_STATION,
        )

        class Case(NamedTuple):
            name: str
            input: str
            want: str

        my_tests = [
            Case(
                "Alliance",
                "showinfo:16159//3001",
                "https://evemaps.dotlan.net/alliance/Wayne_Enterprises",
            ),
            Case(
                "Character",
                "showinfo:1376//1001",
                "https://evewho.com/character/1001",
            ),
            Case(
                "Corporation",
                "showinfo:2//2001",
                "https://evemaps.dotlan.net/corp/Wayne_Technologies",
            ),
            Case(
                "Killmail",
                "killReport:84900666:9e6fe9e5392ff0cfc6ab956677dbe1deb69c4b04",
                "https://zkillboard.com/kill/84900666/",
            ),
            Case(
                "Solar System",
                "showinfo:5//30004984",
                "https://evemaps.dotlan.net/system/Abune",
            ),
            Case(
                "Station",
                "showinfo:52678//60003760",
                "https://evemaps.dotlan.net/station/Jita_IV_-_Moon_4_-_Caldari_Navy_Assembly_Plant",
            ),
            Case(
                "Inventory Type",
                "showinfo:603",
                "https://www.kalkoken.org/apps/eveitems/?typeId=603",
            ),
            Case(
                "Valid URL",
                "https://www.example.com",
                "https://www.example.com",
            ),
            Case(
                "Not support eve link 1",
                "fitting:11987:2048;1:1952;1:26914;2:31366;1:16487;2:31059;1:19057;2:18867;1:18710;1:18871;1:12058;1:31900;1:41155;1::",
                "",
            ),
            Case(
                "Not support eve link 2",
                "hyperNet:9ff5fa81-942e-49c2-9469-623b2abcb05d",
                "",
            ),
            Case(
                "Invalid URL",
                "not-valid",
                "",
            ),
            Case(
                "Unsupported eve links",
                'showinfo:35825//1000000000001">Amamake - Test Structure Alpha',
                "",
            ),
            Case(
                "incomplete",
                "showinfo:52678//",
                "",
            ),
        ]

        for tc in my_tests:
            with self.subTest(test=tc.name):
                self.assertEqual(evexml.eve_link_to_url(tc.input), tc.want)
