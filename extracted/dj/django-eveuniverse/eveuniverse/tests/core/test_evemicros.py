import requests_mock
from django.core.cache import cache
from django.test import TestCase
from requests.exceptions import HTTPError

from eveuniverse.constants import EveGroupId
from eveuniverse.core import evemicros
from eveuniverse.tests.testdata.factories import create_evemicros_response


@requests_mock.Mocker()
class TestEveMicrosNearestCelestial(TestCase):
    def setUp(self) -> None:
        cache.clear()

    def test_should_return_item_from_api(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "GET",
            url="https://www.kalkoken.org/apps/evemicros/eveUniverse.php?nearestCelestials=30002682,660502472160,-130687672800,-813545103840",
            json=create_evemicros_response(40170698, 50011472, 40170697),
        )
        # when
        result = evemicros.nearest_celestial(
            solar_system_id=30002682, x=660502472160, y=-130687672800, z=-813545103840
        )
        # then
        self.assertEqual(result.id, 40170698)
        self.assertEqual(result.name, "Colelie VI - Asteroid Belt 1")
        self.assertEqual(result.type_id, 15)
        self.assertEqual(result.distance, 701983769)
        self.assertEqual(requests_mocker.call_count, 1)

    def test_should_return_item_from_cache(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "GET",
            url="https://www.kalkoken.org/apps/evemicros/eveUniverse.php?nearestCelestials=99,1,2,3",
            json=create_evemicros_response(40170698, 50011472, 40170697),
        )
        evemicros.nearest_celestial(solar_system_id=99, x=1, y=2, z=3)
        # when
        result = evemicros.nearest_celestial(solar_system_id=99, x=1, y=2, z=3)
        # then
        self.assertEqual(result.id, 40170698)
        self.assertEqual(requests_mocker.call_count, 1)

    def test_should_return_none_if_nothing_found(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "GET",
            url="https://www.kalkoken.org/apps/evemicros/eveUniverse.php?nearestCelestials=30002682,1,2,3",
            json=create_evemicros_response(),
        )
        # when
        result = evemicros.nearest_celestial(solar_system_id=30002682, x=1, y=2, z=3)
        # then
        self.assertIsNone(result)

    def test_should_return_none_if_api_reports_error(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "GET",
            url="https://www.kalkoken.org/apps/evemicros/eveUniverse.php?nearestCelestials=30002682,1,2,3",
            json=create_evemicros_response(40170698, 50011472, ok=False),
        )
        # when
        result = evemicros.nearest_celestial(solar_system_id=30002682, x=1, y=2, z=3)
        # then
        self.assertIsNone(result)

    def test_should_raise_exception_for_http_errors(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "GET",
            url="https://www.kalkoken.org/apps/evemicros/eveUniverse.php?nearestCelestials=30002682,1,2,3",
            status_code=500,
        )
        # when
        with self.assertRaises(HTTPError):
            evemicros.nearest_celestial(solar_system_id=30002682, x=1, y=2, z=3)

    def test_should_return_moon_from_api(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "GET",
            url="https://www.kalkoken.org/apps/evemicros/eveUniverse.php?nearestCelestials=30002682,660502472160,-130687672800,-813545103840",
            json=create_evemicros_response(40170698, 50011472, 40170697, 40170699),
        )
        # when
        result = evemicros.nearest_celestial(
            solar_system_id=30002682,
            x=660502472160,
            y=-130687672800,
            z=-813545103840,
            group_id=EveGroupId.MOON,
        )
        # then
        self.assertEqual(result.id, 40170699)
