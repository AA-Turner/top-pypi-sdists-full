import requests_mock
from django.core.cache import cache
from django.test import TestCase
from requests.exceptions import HTTPError

from eveuniverse.constants import EveGroupId
from eveuniverse.core import evesdeapi
from eveuniverse.tests.testdata.factories import create_evesdeapi_response


@requests_mock.Mocker()
class TestEveSdeApiNearestCelestial(TestCase):
    _BASE_URL = "https://evesdeapi.kalkoken.net/latest"

    def setUp(self) -> None:
        cache.clear()

    def test_should_return_item_from_api(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "GET",
            url=(
                f"{self._BASE_URL}/universe/systems/30002682/nearest_celestials"
                "?x=660502472160&y=-130687672800&z=-813545103840"
            ),
            json=create_evesdeapi_response(40170698, 50011472, 40170697),
        )
        # when
        result = evesdeapi.nearest_celestial(
            solar_system_id=30002682, x=660502472160, y=-130687672800, z=-813545103840
        )
        # then
        self.assertEqual(result.id, 40170698)
        self.assertEqual(result.name, "Colelie VI - Asteroid Belt 1")
        self.assertEqual(result.type_id, 15)
        self.assertEqual(result.distance, 701983769)

    def test_should_return_item_from_cache(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "GET",
            url=(
                f"{self._BASE_URL}/universe/systems/30002682/nearest_celestials"
                "?x=660502472160&y=-130687672800&z=-813545103840"
            ),
            json=create_evesdeapi_response(40170698, 50011472, 40170697),
        )
        evesdeapi.nearest_celestial(
            solar_system_id=30002682, x=660502472160, y=-130687672800, z=-813545103840
        )  # when
        result = evesdeapi.nearest_celestial(
            solar_system_id=30002682, x=660502472160, y=-130687672800, z=-813545103840
        )  # then
        self.assertEqual(result.id, 40170698)
        self.assertEqual(requests_mocker.call_count, 1)

    def test_should_return_none_if_nothing_found(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "GET",
            url=(
                f"{self._BASE_URL}/universe/systems/30002682/nearest_celestials"
                "?x=1&y=2&z=3"
            ),
            json=create_evesdeapi_response(),
        )
        # when
        result = evesdeapi.nearest_celestial(solar_system_id=30002682, x=1, y=2, z=3)
        # then
        self.assertIsNone(result)

    def test_should_raise_exception_for_http_errors(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "GET",
            url=(
                f"{self._BASE_URL}/universe/systems/30002682/nearest_celestials"
                "?x=1&y=2&z=3"
            ),
            status_code=500,
        )
        # when
        with self.assertRaises(HTTPError):
            evesdeapi.nearest_celestial(solar_system_id=30002682, x=1, y=2, z=3)

    def test_should_return_moon_from_api(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "GET",
            url=(
                f"{self._BASE_URL}/universe/systems/30002682/nearest_celestials"
                "?x=660502472160&y=-130687672800&z=-813545103840&group_id=8"
            ),
            json=create_evesdeapi_response(40170699),
        )
        # when
        result = evesdeapi.nearest_celestial(
            solar_system_id=30002682,
            x=660502472160,
            y=-130687672800,
            z=-813545103840,
            group_id=EveGroupId.MOON,
        )
        # then
        self.assertEqual(result.id, 40170699)

    def test_should_log_response_on_debug(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "GET",
            url=(
                f"{self._BASE_URL}/universe/systems/30002682/nearest_celestials"
                "?x=660502472160&y=-130687672800&z=-813545103840&group_id=8"
            ),
            json=create_evesdeapi_response(40170699),
        )
        # when
        with self.assertLogs(level="DEBUG") as my_log:
            evesdeapi.nearest_celestial(
                solar_system_id=30002682,
                x=660502472160,
                y=-130687672800,
                z=-813545103840,
                group_id=EveGroupId.MOON,
            )
            # then
            self.assertEqual(len(my_log.output), 2)
            self.assertIn("Response from evesdeapi", my_log.output[1])
