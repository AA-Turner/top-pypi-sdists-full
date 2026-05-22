from unittest import TestCase

import pook
from django.core.cache import cache
from requests.exceptions import HTTPError

from eveuniverse.constants import EveGroupId
from eveuniverse.core import evesdeapi

_BASE_URL = "https://evesdeapi.kalkoken.net/latest"


class TestEveSdeApiNearestCelestial(TestCase):
    def setUp(self) -> None:
        cache.clear()

    @pook.on
    def test_should_return_item_from_api(self):
        # given
        distance = 701983769
        item_id = 40170698
        item_name = "Colelie VI - Asteroid Belt 1"
        item_type_id = 15
        solar_system_id = 30002682
        x = 660502472160
        y = -130687672800
        z = -813545103840
        pook.get(
            url=(
                f"{_BASE_URL}/universe/systems/{solar_system_id}/nearest_celestials"
                f"?x={x}&y={y}&z={z}"
            ),
            reply=200,
            response_json=[
                {
                    "distance": distance,
                    "group_id": 9,
                    "group_name": "Asteroid Belt",
                    "item_id": item_id,
                    "name": item_name,
                    "position": {
                        "x": 392074567680.0,
                        "y": 78438850560.0,
                        "z": -199546920960.0,
                    },
                    "type_id": item_type_id,
                    "type_name": "Asteroid Belt",
                },
            ],
        )

        # when
        result = evesdeapi.nearest_celestial(
            solar_system_id=solar_system_id, x=x, y=y, z=z
        )

        # then
        self.assertEqual(result.id, item_id)
        self.assertEqual(result.name, item_name)
        self.assertEqual(result.type_id, item_type_id)
        self.assertEqual(result.distance, distance)

    @pook.on
    def test_should_return_none_if_nothing_found(self):
        # given
        solar_system_id = 30002682
        x = 660502472160
        y = -130687672800
        z = -813545103840
        pook.get(
            url=(
                f"{_BASE_URL}/universe/systems/{solar_system_id}/nearest_celestials"
                f"?x={x}&y={y}&z={z}"
            ),
            reply=200,
            response_json=[],
        )

        # when
        result = evesdeapi.nearest_celestial(
            solar_system_id=solar_system_id, x=x, y=y, z=z
        )

        # then
        self.assertIsNone(result)

    @pook.on
    def test_should_raise_exception_for_http_errors(self):
        # given
        solar_system_id = 30002682
        x = 660502472160
        y = -130687672800
        z = -813545103840
        pook.get(
            url=(
                f"{_BASE_URL}/universe/systems/{solar_system_id}/nearest_celestials"
                f"?x={x}&y={y}&z={z}"
            ),
            reply=500,
            response_json=[],
        )

        # when/then
        with self.assertRaises(HTTPError):
            evesdeapi.nearest_celestial(solar_system_id=solar_system_id, x=x, y=y, z=z)

    @pook.on
    def test_should_cache_responses(self):
        # given
        item_id = 40170699
        solar_system_id = 30002682
        x = 660502472160
        y = -130687672800
        z = -813545103840
        group_id = EveGroupId.MOON
        pook.get(
            url=(
                f"{_BASE_URL}/universe/systems/{solar_system_id}/nearest_celestials"
                f"?x={x}&y={y}&z={z}&group_id={group_id}"
            ),
            reply=200,
            response_json=[
                {
                    "distance": 701983769,
                    "group_id": group_id,
                    "group_name": "Moon",
                    "item_id": item_id,
                    "name": "Colelie VI - Moon 1",
                    "position": {
                        "x": 390796699186.0,
                        "y": 78460132168.0,
                        "z": -199482549699.0,
                    },
                    "type_id": 14,
                    "type_name": "Moon",
                },
            ],
        )
        evesdeapi.nearest_celestial(
            solar_system_id=solar_system_id,
            x=x,
            y=y,
            z=z,
            group_id=group_id,
        )  # first request hits API

        # when
        result = evesdeapi.nearest_celestial(
            solar_system_id=solar_system_id,
            x=x,
            y=y,
            z=z,
            group_id=group_id,
        )  # second request hits cache as pook route is now expired

        # then
        self.assertEqual(result.id, item_id)
        self.assertTrue(pook.isdone())

    @pook.on
    def test_should_return_moon_from_api(self):
        # given
        item_id = 40170699
        solar_system_id = 30002682
        x = 660502472160
        y = -130687672800
        z = -813545103840
        group_id = EveGroupId.MOON
        pook.get(
            url=(
                f"{_BASE_URL}/universe/systems/{solar_system_id}/nearest_celestials"
                f"?x={x}&y={y}&z={z}&group_id={group_id}"
            ),
            reply=200,
            response_json=[
                {
                    "distance": 701983769,
                    "group_id": group_id,
                    "group_name": "Moon",
                    "item_id": item_id,
                    "name": "Colelie VI - Moon 1",
                    "position": {
                        "x": 390796699186.0,
                        "y": 78460132168.0,
                        "z": -199482549699.0,
                    },
                    "type_id": 14,
                    "type_name": "Moon",
                },
            ],
        )

        # when
        result = evesdeapi.nearest_celestial(
            solar_system_id=solar_system_id,
            x=x,
            y=y,
            z=z,
            group_id=group_id,
        )

        # then
        self.assertEqual(result.id, item_id)
