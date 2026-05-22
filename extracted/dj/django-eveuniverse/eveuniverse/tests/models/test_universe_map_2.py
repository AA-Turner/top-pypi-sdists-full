from typing import NamedTuple
from unittest.mock import patch

import pook
from django.test import TestCase

from eveuniverse.core import evesdeapi
from eveuniverse.helpers import meters_to_ly
from eveuniverse.models import EveEntity, EvePlanet, EveSolarSystem, EveStar, EveType
from eveuniverse.tests.helpers import TestCaseWithClearCache
from eveuniverse.tests.testdata.factories_2 import (
    AsteroidBeltTypeFactory,
    EveAsteroidBeltFactory,
    EveConstellationFactory,
    EveMoonFactory,
    EvePlanetFactory,
    EveRaceFactory,
    EveSolarSystemAbyssalSpaceFactory,
    EveSolarSystemFactory,
    EveSolarSystemHighSecFactory,
    EveSolarSystemLowSecFactory,
    EveSolarSystemNullSecFactory,
    EveSolarSystemTrigSpaceFactory,
    EveSolarSystemWSpaceFactory,
    EveStarFactory,
    EveStargateFactory,
    EveStationFactory,
    EveTypeFactory,
    MoonTypeFactory,
    PositionFactory,
    ShipTypeFactory,
    make_esi_url,
)

MODELS_PATH = "eveuniverse.models.base"


class TestEveSolarSystem(TestCaseWithClearCache):
    def test_str(self):
        obj = EveSolarSystemFactory()
        self.assertEqual(str(obj), obj.name)


@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_PLANETS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARGATES", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STATIONS", False)
class TestEveSolarSystem_Sections(TestCase):

    def test_str(self):
        obj = EveSolarSystemFactory()
        self.assertEqual(str(obj), obj.name)

    @pook.on
    def test_create_from_esi_minimal(self):
        # given
        constellation = EveConstellationFactory()
        solar_system_id = 30045339
        name = "Enaluri"
        security_status = 0.3277980387210846
        position = PositionFactory()
        pook.get(
            make_esi_url(f"universe/systems/{solar_system_id}"),
            reply=200,
            response_json={
                "constellation_id": constellation.id,
                "name": name,
                "planets": [],
                "position": position,
                "security_status": security_status,
                "system_id": solar_system_id,
            },
        )

        # when
        obj: EveSolarSystem
        obj, created = EveSolarSystem.objects.get_or_create_esi(id=30045339)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, solar_system_id)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.eve_constellation, constellation)
        self.assertEqual(obj.position_x, position["x"])
        self.assertEqual(obj.position_y, position["y"])
        self.assertEqual(obj.position_z, position["z"])
        self.assertEqual(obj.security_status, security_status)
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_SOLAR_SYSTEM)

        self.assertFalse(obj.enabled_sections.planets)
        self.assertFalse(obj.enabled_sections.stargates)
        self.assertFalse(obj.enabled_sections.stars)
        self.assertFalse(obj.enabled_sections.stations)

    @pook.on
    def test_should_create_from_esi_with_all_sections_full(self):
        # given
        constellation_id = 20000785
        name = "Enaluri"
        planet_id = 40349467
        region_id = 10000069
        security_status = 0.3277980387210846
        solar_system_id = 30045339
        star_id = 40349466
        stargate_id = 50016284
        station_id = 60015068
        system_position = PositionFactory()
        pook.get(
            make_esi_url(f"universe/regions/{region_id}"),
            reply=200,
            response_json={
                "constellations": [constellation_id],
                "description": "...",
                "name": "Black Rise",
                "region_id": region_id,
            },
        )
        pook.get(
            make_esi_url(f"universe/constellations/{constellation_id}"),
            reply=200,
            response_json={
                "constellation_id": constellation_id,
                "name": "Ishaga",
                "position": PositionFactory(),
                "region_id": region_id,
                "systems": [solar_system_id],
            },
        )
        pook.get(
            make_esi_url(f"universe/systems/{solar_system_id}"),
            reply=200,
            response_json={
                "constellation_id": constellation_id,
                "name": name,
                "planets": [{"planet_id": planet_id}],
                "position": system_position,
                "security_status": security_status,
                "star_id": star_id,
                "stargates": [stargate_id],
                "stations": [station_id],
                "system_id": solar_system_id,
            },
        )
        planet_type = EveTypeFactory()
        pook.get(
            make_esi_url(f"universe/planets/{planet_id}"),
            reply=200,
            response_json={
                "name": "Enaluri I",
                "planet_id": planet_id,
                "position": PositionFactory(),
                "system_id": solar_system_id,
                "type_id": planet_type.id,
            },
        )
        star_type = EveTypeFactory()
        pook.get(
            make_esi_url(f"universe/stars/{star_id}"),
            reply=200,
            response_json={
                "age": 37075060962,
                "luminosity": 0.02542000077664852,
                "name": "Enaluri - Star",
                "radius": 590000000,
                "solar_system_id": solar_system_id,
                "spectral_class": "M6 V",
                "temperature": 2385,
                "type_id": star_type.id,
            },
        )
        destination = EveStargateFactory()
        stargate_type = EveTypeFactory()
        pook.get(
            make_esi_url(f"universe/stargates/{stargate_id}"),
            reply=200,
            response_json={
                "destination": {
                    "stargate_id": destination.id,
                    "system_id": destination.eve_solar_system.id,
                },
                "name": "Stargate (Akidagi)",
                "position": PositionFactory(),
                "stargate_id": stargate_id,
                "system_id": solar_system_id,
                "type_id": stargate_type.id,
            },
        )
        station_type = EveTypeFactory()
        er = EveRaceFactory()
        pook.get(
            make_esi_url(f"universe/stations/{station_id}"),
            reply=200,
            response_json={
                "max_dockable_ship_volume": 50000000,
                "name": "Enaluri V - State Protectorate Assembly Plant",
                "office_rental_cost": 118744,
                "owner": 1000180,
                "position": PositionFactory(),
                "race_id": er.id,
                "reprocessing_efficiency": 0.5,
                "reprocessing_stations_take": 0.025,
                "services": [
                    "bounty-missions",
                    "courier-missions",
                    "reprocessing-plant",
                    "market",
                    "repair-facilities",
                    "factory",
                    "fitting",
                    "news",
                    "insurance",
                    "docking",
                    "office-rental",
                    "loyalty-point-store",
                    "navy-offices",
                    "security-offices",
                ],
                "station_id": station_id,
                "system_id": solar_system_id,
                "type_id": station_type.id,
            },
        )

        # when
        obj: EveSolarSystem
        obj, created = EveSolarSystem.objects.get_or_create_esi(
            id=solar_system_id,
            include_children=True,
            enabled_sections=[
                EveSolarSystem.Section.PLANETS,
                EveSolarSystem.Section.STATIONS,
                EveSolarSystem.Section.STARS,
                EveSolarSystem.Section.STARGATES,
            ],
        )

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, solar_system_id)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.eve_constellation.id, constellation_id)
        self.assertEqual(obj.position_x, system_position["x"])
        self.assertEqual(obj.position_y, system_position["y"])
        self.assertEqual(obj.position_z, system_position["z"])
        self.assertEqual(obj.security_status, security_status)
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_SOLAR_SYSTEM)

        self.assertTrue(obj.enabled_sections.planets)
        self.assertTrue(obj.enabled_sections.stargates)
        self.assertTrue(obj.enabled_sections.stars)
        self.assertTrue(obj.enabled_sections.stations)

        self.assertEqual(obj.eve_star, EveStar.objects.get(id=star_id))
        self.assertTrue(obj.eve_planets.filter(id=planet_id).exists())
        self.assertTrue(obj.eve_stations.filter(id=station_id).exists())
        self.assertTrue(obj.eve_stargates.filter(id=stargate_id).exists())

    @pook.on
    def test_should_not_mark_section_as_updated_when_children_are_not_fetched(self):
        # given
        constellation = EveConstellationFactory()
        solar_system_id = 30045339
        name = "Enaluri"
        security_status = 0.3277980387210846
        position = PositionFactory()
        stargate_id = 50016284
        pook.get(
            make_esi_url(f"universe/systems/{solar_system_id}"),
            reply=200,
            response_json={
                "constellation_id": constellation.id,
                "name": name,
                "planets": [],
                "position": position,
                "security_status": security_status,
                "stargates": [stargate_id],
                "system_id": solar_system_id,
            },
        )
        destination = EveStargateFactory()
        stargate_type = EveTypeFactory()
        pook.get(
            make_esi_url(f"universe/stargates/{stargate_id}"),
            reply=200,
            response_json={
                "destination": {
                    "stargate_id": destination.id,
                    "system_id": destination.eve_solar_system.id,
                },
                "name": "Stargate (Akidagi)",
                "position": PositionFactory(),
                "stargate_id": stargate_id,
                "system_id": solar_system_id,
                "type_id": stargate_type.id,
            },
        )

        # when
        obj: EveSolarSystem
        obj, _ = EveSolarSystem.objects.get_or_create_esi(
            id=solar_system_id,
            enabled_sections=[EveSolarSystem.Section.STARGATES],
        )
        # then
        self.assertEqual(obj.id, solar_system_id)
        self.assertFalse(obj.enabled_sections.stargates)

    @pook.on
    def test_should_create_solar_system_with_planets_and_moons(self):
        # given
        constellation = EveConstellationFactory()
        moon_id = 40349468
        name = "Enaluri"
        planet_id = 40349467
        position = PositionFactory()
        security_status = 0.3277980387210846
        solar_system_id = 30045339
        pook.get(
            make_esi_url(f"universe/systems/{solar_system_id}"),
            reply=200,
            response_json={
                "constellation_id": constellation.id,
                "name": name,
                "planets": [
                    {
                        "moons": [moon_id],
                        "planet_id": planet_id,
                    }
                ],
                "position": position,
                "security_status": security_status,
                "system_id": solar_system_id,
            },
            persist=True,
        )
        pook.get(
            make_esi_url(f"universe/moons/{moon_id}"),
            reply=200,
            response_json={
                "moon_id": moon_id,
                "name": "Enaluri I - Moon 1",
                "position": position,
                "system_id": solar_system_id,
            },
            persist=True,
        )
        planet_type = EveTypeFactory()
        pook.get(
            make_esi_url(f"universe/planets/{planet_id}"),
            reply=200,
            response_json={
                "name": "Enaluri I",
                "planet_id": planet_id,
                "position": PositionFactory(),
                "system_id": solar_system_id,
                "type_id": planet_type.id,
            },
            persist=True,
        )

        # when
        solar_system: EveSolarSystem
        solar_system, _ = EveSolarSystem.objects.update_or_create_esi(
            id=solar_system_id,
            include_children=True,
            enabled_sections=[EveSolarSystem.Section.PLANETS, EvePlanet.Section.MOONS],
        )

        # then
        self.assertEqual(solar_system.id, solar_system_id)
        self.assertTrue(solar_system.enabled_sections.planets)
        self.assertTrue(solar_system.eve_planets.filter(id=planet_id).exists())

        planet = solar_system.eve_planets.get(id=planet_id)
        self.assertTrue(planet.enabled_sections.moons)
        self.assertTrue(planet.eve_moons.filter(id=moon_id).exists())


@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_ASTEROID_BELTS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_PLANETS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARGATES", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STATIONS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
class TestEveSolarSystem_NearestCelestial(TestCaseWithClearCache):

    @pook.on
    def test_should_return_celestial(self):
        belt = EveAsteroidBeltFactory()
        belt_type = AsteroidBeltTypeFactory()
        planet = EvePlanetFactory()
        solar_system = EveSolarSystemFactory()
        star = EveStarFactory()
        stargate = EveStargateFactory()
        moon = EveMoonFactory()
        moon_type = MoonTypeFactory()
        station = EveStationFactory()
        ship = ShipTypeFactory()

        class Case(NamedTuple):
            name: str
            obj: object
            eve_type: EveType
            is_valid: bool

        cases = [
            Case("asteroid belt", belt, belt_type, True),
            Case("moon", moon, moon_type, True),
            Case("planet", planet, planet.eve_type, True),
            Case("star", star, star.eve_type, True),
            Case("stargate", stargate, stargate.eve_type, True),
            Case("station", station, station.eve_type, True),
            Case("invalid", ship, ship, False),
        ]

        for tc in cases:
            with self.subTest(name=tc.name):
                with patch("eveuniverse.models.universe_2.evesdeapi") as m:
                    response = evesdeapi.EveItem(
                        id=tc.obj.id,
                        name=tc.obj.name,
                        type_id=tc.eve_type.id,
                        distance=1000,
                    )
                    m.nearest_celestial.return_value = response

                    # when
                    result = solar_system.nearest_celestial(x=-1, y=-2, z=3)

                    # then
                    if not tc.is_valid:
                        self.assertIsNone(result)
                        continue

                    self.assertEqual(result.eve_type, tc.eve_type)
                    self.assertEqual(result.eve_object, tc.obj)
                    self.assertEqual(result.distance, 1000)


"""
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARGATES", True)
@patch(MODELS_PATH + ".cache")
def test_can_calculate_route(self, mock_cache, mock_esi):
    def my_get_or_set(key, func, timeout):
        return func()


    mock_cache.get.return_value = None
    mock_cache.get_or_set.side_effect = my_get_or_set

    enaluri, _ = EveSolarSystem.objects.get_or_create_esi(
        id=30045339, include_children=True
    )
    akidagi, _ = EveSolarSystem.objects.get_or_create_esi(
        id=30045342, include_children=True
    )
    self.assertEqual(enaluri.jumps_to(akidagi), 1)
"""


class TestEveSolarSystem_DistanceTo(TestCase):
    def test_should_calculate_distance_between_normal_systems(self):
        # given
        a = EveSolarSystemLowSecFactory(
            position_x=-227875173313944580,
            position_y=104688385699531790,
            position_z=120279417692650270,
        )
        b = EveSolarSystemLowSecFactory(
            position_x=-211265901041153470,
            position_y=55806528490315120,
            position_z=81416396747037220,
        )

        # when
        result = a.distance_to(b)

        # then
        self.assertEqual(round(meters_to_ly(result), 3), 6.831)

    def test_should_return_none_when_one_system_in_wh_space_1(self):
        # given
        a = EveSolarSystemLowSecFactory(
            position_x=-227875173313944580,
            position_y=104688385699531790,
            position_z=120279417692650270,
        )
        b = EveSolarSystemWSpaceFactory(
            position_x=-211265901041153470,
            position_y=55806528490315120,
            position_z=81416396747037220,
        )

        # when
        result = a.distance_to(b)
        # then
        self.assertIsNone(result)

    def test_should_return_none_when_one_system_in_wh_space_2(self):
        # given
        a = EveSolarSystemLowSecFactory(
            position_x=-227875173313944580,
            position_y=104688385699531790,
            position_z=120279417692650270,
        )
        b = EveSolarSystemWSpaceFactory(
            position_x=-211265901041153470,
            position_y=55806528490315120,
            position_z=81416396747037220,
        )

        # when
        result = b.distance_to(a)
        # then
        self.assertIsNone(result)

    def test_should_return_none_when_no_destination(self):
        # given
        a = EveSolarSystemLowSecFactory(
            position_x=-227875173313944580,
            position_y=104688385699531790,
            position_z=120279417692650270,
        )

        # when
        result = a.distance_to(None)

        # then
        self.assertIsNone(result)

    def test_should_return_none_when_origin_has_not_coordinates(self):
        # given
        a = EveSolarSystemLowSecFactory(
            position_x=None,
            position_y=None,
            position_z=None,
        )
        b = EveSolarSystemLowSecFactory(
            position_x=-211265901041153470,
            position_y=55806528490315120,
            position_z=81416396747037220,
        )

        # when
        result = a.distance_to(b)

        # then
        self.assertIsNone(result)

    def test_should_return_none_when_destination_has_not_coordinates(self):
        # given
        a = EveSolarSystemLowSecFactory(
            position_x=-227875173313944580,
            position_y=104688385699531790,
            position_z=120279417692650270,
        )
        b = EveSolarSystemLowSecFactory(
            position_x=None,
            position_y=None,
            position_z=None,
        )

        # when
        result = a.distance_to(b)

        # then
        self.assertIsNone(result)

    def test_should_return_none_when_one_system_is_in_trig_space_1(self):
        # given
        a = EveSolarSystemLowSecFactory(
            position_x=-227875173313944580,
            position_y=104688385699531790,
            position_z=120279417692650270,
        )
        b = EveSolarSystemTrigSpaceFactory(
            position_x=-211265901041153470,
            position_y=55806528490315120,
            position_z=81416396747037220,
        )

        # when
        result = a.distance_to(b)

        # then
        self.assertIsNone(result)

    def test_should_return_none_when_one_system_is_in_trig_space_2(self):
        # given
        a = EveSolarSystemLowSecFactory(
            position_x=-227875173313944580,
            position_y=104688385699531790,
            position_z=120279417692650270,
        )
        b = EveSolarSystemTrigSpaceFactory(
            position_x=-211265901041153470,
            position_y=55806528490315120,
            position_z=81416396747037220,
        )

        # when
        result = b.distance_to(a)

        # then
        self.assertIsNone(result)


class TestEveSolarSystem_JumpsTo(TestCaseWithClearCache):

    @pook.on
    def test_can_calculate_jumps(self):
        # given
        a = EveSolarSystemLowSecFactory()
        b = EveSolarSystemLowSecFactory()
        c = EveSolarSystemLowSecFactory()
        pook.post(
            make_esi_url(f"route/{a.id}/{c.id}"),
            reply=200,
            response_json={"route": [a.id, b.id, c.id]},
        )

        # when/then
        self.assertEqual(a.jumps_to(c), 2)

    @pook.on
    def test_route_calc_returns_none_if_no_route_found(self):
        # given
        a = EveSolarSystemLowSecFactory()
        b = EveSolarSystemLowSecFactory()
        pook.post(
            make_esi_url(f"route/{a.id}/{b.id}"),
            reply=404,
            response_json={"error": "not found"},
        )

        # when/then
        self.assertIsNone(a.jumps_to(b))

    @pook.on
    def test_should_return_none_if_any_system_is_in_wh_space(self):
        # given
        a = EveSolarSystemLowSecFactory()
        b = EveSolarSystemWSpaceFactory()
        pook.post(
            make_esi_url(f"route/{a.id}/{b.id}"),
            reply=500,
            response_json=[],
        )

        # when/then
        self.assertIsNone(a.jumps_to(b))
        self.assertIsNone(b.jumps_to(a))

    @pook.on
    def test_should_return_none_if_any_system_is_in_trig_space(self):
        # given
        a = EveSolarSystemLowSecFactory()
        b = EveSolarSystemTrigSpaceFactory()
        pook.post(
            make_esi_url(f"route/{a.id}/{b.id}"),
            reply=500,
            response_json=[],
        )

        # when/then
        self.assertIsNone(a.jumps_to(b))
        self.assertIsNone(b.jumps_to(a))


class TestEveSolarSystem_RouteTo(TestCaseWithClearCache):

    @pook.on
    def test_should_return_valid_route(self):
        # given
        a = EveSolarSystemLowSecFactory()
        b = EveSolarSystemLowSecFactory()
        c = EveSolarSystemLowSecFactory()
        pook.post(
            make_esi_url(f"route/{a.id}/{c.id}"),
            reply=200,
            response_json={"route": [a.id, b.id, c.id]},
        )

        # when
        result = a.route_to(c)

        # then
        self.assertListEqual(result, [(a, False), (b, False), (c, False)])

    @pook.on
    def test_should_return_none_when_no_route_found(self):
        # given
        # given
        a = EveSolarSystemLowSecFactory()
        b = EveSolarSystemLowSecFactory()
        pook.post(
            make_esi_url(f"route/{a.id}/{b.id}"),
            reply=404,
            response_json={"error": "not found"},
        )

        # when
        result = a.route_to(b)

        # then
        self.assertIsNone(result)

    @pook.on
    def test_should_return_none_if_any_system_is_in_wh_space(self):
        # given
        a = EveSolarSystemLowSecFactory()
        b = EveSolarSystemWSpaceFactory()
        pook.post(
            make_esi_url(f"route/{a.id}/{b.id}"),
            reply=500,
            response_json={},
        )

        # when/then
        self.assertIsNone(a.route_to(b))
        self.assertIsNone(b.route_to(a))

    @pook.on
    def test_should_return_none_if_any_system_is_in_trig_space(self):
        # given
        a = EveSolarSystemLowSecFactory()
        b = EveSolarSystemTrigSpaceFactory()
        pook.post(
            make_esi_url(f"route/{a.id}/{b.id}"),
            reply=500,
            response_json={},
        )

        # when/then
        self.assertIsNone(a.route_to(b))
        self.assertIsNone(b.route_to(a))


class TestEveSolarSystems_SpaceTypes(TestCase):
    def test_can_identify_highsec_system(self):
        obj = EveSolarSystemHighSecFactory()
        self.assertTrue(obj.is_high_sec)
        self.assertFalse(obj.is_low_sec)
        self.assertFalse(obj.is_null_sec)
        self.assertFalse(obj.is_w_space)
        self.assertFalse(obj.is_trig_space)
        self.assertFalse(obj.is_abyssal_deadspace)

    def test_can_identify_lowsec_system(self):
        obj = EveSolarSystemLowSecFactory()
        self.assertTrue(obj.is_low_sec)
        self.assertFalse(obj.is_high_sec)
        self.assertFalse(obj.is_null_sec)
        self.assertFalse(obj.is_w_space)
        self.assertFalse(obj.is_trig_space)
        self.assertFalse(obj.is_abyssal_deadspace)

    def test_can_identify_nullsec_system(self):
        obj = EveSolarSystemNullSecFactory()
        self.assertTrue(obj.is_null_sec)
        self.assertFalse(obj.is_low_sec)
        self.assertFalse(obj.is_high_sec)
        self.assertFalse(obj.is_w_space)
        self.assertFalse(obj.is_trig_space)
        self.assertFalse(obj.is_abyssal_deadspace)

    def test_can_identify_ws_system(self):
        obj = EveSolarSystemWSpaceFactory()
        self.assertTrue(obj.is_w_space)
        self.assertFalse(obj.is_null_sec)
        self.assertFalse(obj.is_low_sec)
        self.assertFalse(obj.is_high_sec)
        self.assertFalse(obj.is_trig_space)
        self.assertFalse(obj.is_abyssal_deadspace)

    def test_can_identify_trig_system(self):
        obj = EveSolarSystemTrigSpaceFactory()
        self.assertFalse(obj.is_w_space)
        self.assertFalse(obj.is_null_sec)
        self.assertFalse(obj.is_low_sec)
        self.assertFalse(obj.is_high_sec)
        self.assertTrue(obj.is_trig_space)
        self.assertFalse(obj.is_abyssal_deadspace)

    def test_can_identify_abyssal_deadspace(self):
        obj = EveSolarSystemAbyssalSpaceFactory()
        self.assertFalse(obj.is_w_space)
        self.assertFalse(obj.is_null_sec)
        self.assertFalse(obj.is_low_sec)
        self.assertFalse(obj.is_high_sec)
        self.assertFalse(obj.is_trig_space)
        self.assertTrue(obj.is_abyssal_deadspace)

    def test_all(self):
        class Case(NamedTuple):
            name: str
            security_status: float
            is_high_sec: bool
            is_low_sec: bool
            is_null_sec: bool

        cases = [
            Case("high sec normal", 1.0, True, False, False),
            Case("low sec normal", 0.3, False, True, False),
            Case("null sec normal", -0.3, False, False, True),
            Case("low sec lower border", 0.049993, False, True, False),
            Case("low sec upper border", 0.0449, False, True, False),
        ]
        for tc in cases:
            with self.subTest(name=tc.name):
                system = EveSolarSystemFactory(security_status=tc.security_status)
                self.assertIs(system.is_high_sec, tc.is_high_sec)
                self.assertIs(system.is_low_sec, tc.is_low_sec)
                self.assertIs(system.is_null_sec, tc.is_null_sec)
