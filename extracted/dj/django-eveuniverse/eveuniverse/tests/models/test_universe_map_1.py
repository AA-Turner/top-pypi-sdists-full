from unittest.mock import patch

import pook

from eveuniverse.models import (
    EveAsteroidBelt,
    EveConstellation,
    EveEntity,
    EveMoon,
    EvePlanet,
    EveRace,
    EveRegion,
    EveSolarSystem,
    EveStar,
    EveStargate,
    EveStation,
)
from eveuniverse.tests.helpers import TestCaseWithClearCache
from eveuniverse.tests.testdata.factories_2 import (
    EveMoonFactory,
    EvePlanetFactory,
    EveRaceFactory,
    EveSolarSystemFactory,
    EveStargateFactory,
    EveTypeFactory,
    PositionFactory,
    make_esi_url,
)

MODELS_PATH = "eveuniverse.models.base"


class TestEveAsteroidBelt(TestCaseWithClearCache):

    @pook.on
    def test_create_from_esi(self):
        # given
        belt_id = 40349487
        planet = EvePlanetFactory()
        solar_system: EveSolarSystem = planet.eve_solar_system
        position = PositionFactory()
        obj_name = "Enaluri III - Asteroid Belt 1"
        pook.get(
            make_esi_url(f"universe/asteroid_belts/{belt_id}"),
            reply=200,
            response_json={
                "name": obj_name,
                "position": position,
                "system_id": solar_system.id,
            },
        )
        pook.get(
            make_esi_url(f"universe/systems/{solar_system.id}"),
            reply=200,
            response_json={
                "constellation_id": solar_system.eve_constellation.id,
                "name": "Enaluri",
                "planets": [{"asteroid_belts": [belt_id], "planet_id": planet.id}],
                "position": {
                    "x": solar_system.position_x,
                    "y": solar_system.position_y,
                    "z": solar_system.position_z,
                },
                "security_status": solar_system.security_status,
                "system_id": solar_system.id,
            },
        )

        # when
        obj: EveAsteroidBelt
        obj, created = EveAsteroidBelt.objects.get_or_create_esi(id=belt_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, belt_id)
        self.assertEqual(obj.name, obj_name)
        self.assertEqual(obj.position_x, position["x"])
        self.assertEqual(obj.position_y, position["y"])
        self.assertEqual(obj.position_z, position["z"])
        self.assertEqual(obj.eve_planet, planet)


class TestEveConstellation(TestCaseWithClearCache):

    @pook.on
    def test_create_from_esi(self):
        # given
        constellation_id = 20000785
        region_id = 10000069
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
        position = PositionFactory()
        pook.get(
            make_esi_url(f"universe/constellations/{constellation_id}"),
            reply=200,
            response_json={
                "constellation_id": constellation_id,
                "name": "Ishaga",
                "position": position,
                "region_id": region_id,
                "systems": [30045339],
            },
        )

        # when
        obj: EveConstellation
        obj, created = EveConstellation.objects.update_or_create_esi(
            id=constellation_id
        )

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, constellation_id)
        self.assertEqual(obj.name, "Ishaga")
        self.assertEqual(obj.position_x, position["x"])
        self.assertEqual(obj.position_y, position["y"])
        self.assertEqual(obj.position_z, position["z"])
        self.assertEqual(obj.eve_region.id, region_id)
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_CONSTELLATION)
        self.assertEqual(obj.name, "Ishaga")
        self.assertEqual(obj.position_x, position["x"])
        self.assertEqual(obj.position_y, position["y"])
        self.assertEqual(obj.position_z, position["z"])
        self.assertEqual(obj.eve_region.id, region_id)
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_CONSTELLATION)


class TestEveMoon(TestCaseWithClearCache):

    @pook.on
    def test_create_from_esi(self):
        # given
        moon_id = 40349468
        moon_name = "Enaluri I - Moon 1"
        planet = EvePlanetFactory()
        solar_system: EveSolarSystem = planet.eve_solar_system
        position = PositionFactory()
        pook.get(
            make_esi_url(f"universe/moons/{moon_id}"),
            reply=200,
            response_json={
                "moon_id": moon_id,
                "name": moon_name,
                "position": position,
                "system_id": solar_system.id,
            },
        )
        pook.get(
            make_esi_url(f"universe/systems/{solar_system.id}"),
            reply=200,
            response_json={
                "constellation_id": solar_system.eve_constellation.id,
                "name": "Enaluri",
                "planets": [{"moons": [moon_id], "planet_id": planet.id}],
                "position": {
                    "x": solar_system.position_x,
                    "y": solar_system.position_y,
                    "z": solar_system.position_z,
                },
                "security_status": solar_system.security_status,
                "system_id": solar_system.id,
            },
        )

        # when
        obj: EveMoon
        obj, created = EveMoon.objects.get_or_create_esi(id=moon_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, moon_id)
        self.assertEqual(obj.name, moon_name)
        self.assertEqual(obj.position_x, position["x"])
        self.assertEqual(obj.position_y, position["y"])
        self.assertEqual(obj.position_z, position["z"])
        self.assertEqual(obj.eve_planet, planet)


class TestEvePlanet(TestCaseWithClearCache):

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_ASTEROID_BELTS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", False)
    @pook.on
    def test_create_from_esi(self):
        # given
        planet_id = 40349467
        planet_name = "Enaluri I"
        solar_system = EveSolarSystemFactory()
        et = EveTypeFactory()
        position = PositionFactory()
        pook.get(
            make_esi_url(f"universe/planets/{planet_id}"),
            reply=200,
            response_json={
                "name": planet_name,
                "planet_id": planet_id,
                "position": position,
                "system_id": solar_system.id,
                "type_id": et.id,
            },
        )

        # when
        obj: EvePlanet
        obj, created = EvePlanet.objects.get_or_create_esi(id=planet_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, planet_id)
        self.assertEqual(obj.name, planet_name)
        self.assertEqual(obj.position_x, position["x"])
        self.assertEqual(obj.position_y, position["y"])
        self.assertEqual(obj.position_z, position["z"])
        self.assertEqual(obj.eve_type, et)
        self.assertEqual(obj.eve_solar_system, solar_system)

        self.assertFalse(obj.enabled_sections.asteroid_belts)
        self.assertFalse(obj.enabled_sections.moons)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_ASTEROID_BELTS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", True)
    @pook.on
    def test_create_from_esi_with_children_1(self):
        # given
        planet_id = 40349467
        planet_name = "Enaluri I"
        solar_system = EveSolarSystemFactory()
        et = EveTypeFactory()
        planet_position = PositionFactory()
        pook.get(
            make_esi_url(f"universe/planets/{planet_id}"),
            reply=200,
            response_json={
                "name": planet_name,
                "planet_id": planet_id,
                "position": planet_position,
                "system_id": solar_system.id,
                "type_id": et.id,
            },
        )
        moon_id = 40349468
        pook.get(
            make_esi_url(f"universe/moons/{moon_id}"),
            reply=200,
            response_json={
                "moon_id": moon_id,
                "name": "Enaluri I - Moon 1",
                "position": PositionFactory(),
                "system_id": solar_system.id,
            },
        )
        pook.get(
            make_esi_url(f"universe/systems/{solar_system.id}"),
            reply=200,
            response_json={
                "constellation_id": solar_system.eve_constellation.id,
                "name": "Enaluri",
                "planets": [{"moons": [moon_id], "planet_id": planet_id}],
                "position": {
                    "x": solar_system.position_x,
                    "y": solar_system.position_y,
                    "z": solar_system.position_z,
                },
                "security_status": solar_system.security_status,
                "system_id": solar_system.id,
            },
            persist=True,
        )

        # when
        obj: EvePlanet
        obj, created = EvePlanet.objects.get_or_create_esi(
            id=planet_id, include_children=True
        )

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, planet_id)
        self.assertEqual(obj.name, planet_name)
        self.assertEqual(obj.position_x, planet_position["x"])
        self.assertEqual(obj.position_y, planet_position["y"])
        self.assertEqual(obj.position_z, planet_position["z"])
        self.assertEqual(obj.eve_type, et)
        self.assertEqual(obj.eve_solar_system, solar_system)
        self.assertTrue(EveMoon.objects.filter(id=moon_id).exists())

        self.assertFalse(obj.enabled_sections.asteroid_belts)
        self.assertTrue(obj.enabled_sections.moons)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_ASTEROID_BELTS", True)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", True)
    @pook.on
    def test_create_from_esi_with_children_2(self):
        # given
        planet_id = 40349467
        planet_name = "Enaluri I"
        solar_system = EveSolarSystemFactory()
        et = EveTypeFactory()
        planet_position = PositionFactory()
        pook.get(
            make_esi_url(f"universe/planets/{planet_id}"),
            reply=200,
            response_json={
                "name": planet_name,
                "planet_id": planet_id,
                "position": planet_position,
                "system_id": solar_system.id,
                "type_id": et.id,
            },
        )
        moon_id = 40349468
        moon_name = "Enaluri I - Moon 1"
        pook.get(
            make_esi_url(f"universe/moons/{moon_id}"),
            reply=200,
            response_json={
                "moon_id": moon_id,
                "name": moon_name,
                "position": PositionFactory(),
                "system_id": solar_system.id,
            },
        )
        belt_id = 40349487
        belt_name = "Enaluri III - Asteroid Belt 1"
        pook.get(
            make_esi_url(f"universe/asteroid_belts/{belt_id}"),
            reply=200,
            response_json={
                "name": belt_name,
                "position": PositionFactory(),
                "system_id": solar_system.id,
            },
        )
        pook.get(
            make_esi_url(f"universe/systems/{solar_system.id}"),
            reply=200,
            response_json={
                "constellation_id": solar_system.eve_constellation.id,
                "name": "Enaluri",
                "planets": [
                    {
                        "asteroid_belts": [belt_id],
                        "moons": [moon_id],
                        "planet_id": planet_id,
                    }
                ],
                "position": {
                    "x": solar_system.position_x,
                    "y": solar_system.position_y,
                    "z": solar_system.position_z,
                },
                "security_status": solar_system.security_status,
                "system_id": solar_system.id,
            },
            persist=True,
        )

        # when
        obj: EvePlanet
        obj, created = EvePlanet.objects.get_or_create_esi(
            id=planet_id, include_children=True
        )

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, planet_id)
        self.assertEqual(obj.name, planet_name)
        self.assertEqual(obj.eve_type, et)
        self.assertEqual(obj.eve_solar_system, solar_system)

        self.assertTrue(obj.enabled_sections.asteroid_belts)
        self.assertTrue(EveAsteroidBelt.objects.filter(id=belt_id).exists())

        self.assertTrue(obj.enabled_sections.moons)
        self.assertTrue(EveMoon.objects.filter(id=moon_id).exists())

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_ASTEROID_BELTS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", False)
    @pook.on
    def test_should_not_create_children_from_esi_when_disabled(self):
        # given
        planet_id = 40349467
        planet_name = "Enaluri I"
        solar_system = EveSolarSystemFactory()
        et = EveTypeFactory()
        position = PositionFactory()
        pook.get(
            make_esi_url(f"universe/planets/{planet_id}"),
            reply=200,
            response_json={
                "name": planet_name,
                "planet_id": planet_id,
                "position": position,
                "system_id": solar_system.id,
                "type_id": et.id,
            },
        )
        belt_id = 40349487
        moon_id = 40349468
        pook.get(
            make_esi_url(f"universe/systems/{solar_system.id}"),
            reply=200,
            response_json={
                "constellation_id": solar_system.eve_constellation.id,
                "name": "Enaluri",
                "planets": [
                    {
                        "asteroid_belts": [belt_id],
                        "moons": [moon_id],
                        "planet_id": planet_id,
                    }
                ],
                "position": {
                    "x": solar_system.position_x,
                    "y": solar_system.position_y,
                    "z": solar_system.position_z,
                },
                "security_status": solar_system.security_status,
                "system_id": solar_system.id,
            },
            persist=True,
        )

        # when
        obj: EvePlanet
        obj, created = EvePlanet.objects.get_or_create_esi(
            id=planet_id, include_children=True
        )

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, planet_id)
        self.assertEqual(obj.name, planet_name)
        self.assertEqual(obj.eve_type, et)
        self.assertEqual(obj.eve_solar_system, solar_system)

        self.assertFalse(EveAsteroidBelt.objects.filter(id=belt_id).exists())
        self.assertFalse(EveMoon.objects.filter(id=moon_id).exists())

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", True)
    @pook.on
    def test_should_update_children(self):
        # given
        planet = EvePlanetFactory()
        solar_system: EveSolarSystem = planet.eve_solar_system
        moon = EveMoonFactory(eve_planet=planet)
        planet_name = "Enaluri I"
        pook.get(
            make_esi_url(f"universe/planets/{planet.id}"),
            reply=200,
            response_json={
                "name": planet_name,
                "planet_id": planet.id,
                "position": PositionFactory(),
                "system_id": solar_system.id,
                "type_id": planet.eve_type.id,
            },
        )
        pook.get(
            make_esi_url(f"universe/moons/{moon.id}"),
            reply=200,
            response_json={
                "moon_id": moon.id,
                "name": "other name",
                "position": PositionFactory(),
                "system_id": solar_system.id,
            },
        )
        pook.get(
            make_esi_url(f"universe/systems/{solar_system.id}"),
            reply=200,
            response_json={
                "constellation_id": solar_system.eve_constellation.id,
                "name": "Enaluri",
                "planets": [
                    {
                        "moons": [moon.id],
                        "planet_id": planet.id,
                    }
                ],
                "position": {
                    "x": solar_system.position_x,
                    "y": solar_system.position_y,
                    "z": solar_system.position_z,
                },
                "security_status": solar_system.security_status,
                "system_id": solar_system.id,
            },
            persist=True,
        )

        # when
        obj: EvePlanet
        obj, created = EvePlanet.objects.update_or_create_esi(
            id=planet.id, include_children=True
        )

        # then
        self.assertFalse(created)
        self.assertEqual(obj.name, planet_name)
        moon.refresh_from_db()
        self.assertEqual(moon.name, "other name")

    @pook.on
    def test_can_return_planet_type_name(self):
        # given
        obj = EvePlanetFactory()

        # when/then
        self.assertEqual(obj.type_name(), "Barren")


class TestEveRace(TestCaseWithClearCache):

    @pook.on
    def test_create_from_esi(self):
        # given
        race_id = 1
        alliance_id = 500001
        description = "Founded on the tenets of patriotism and ..."
        name = "Caldari"
        pook.get(
            make_esi_url("universe/races"),
            reply=200,
            response_json=[
                {
                    "alliance_id": alliance_id,
                    "description": description,
                    "name": name,
                    "race_id": race_id,
                },
                {
                    "alliance_id": 500004,
                    "description": "Champions of liberty and defenders of ...",
                    "name": "Gallente",
                    "race_id": 8,
                },
            ],
        )

        # when
        obj: EveRace
        obj, created = EveRace.objects.get_or_create_esi(id=race_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, race_id)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.alliance_id, alliance_id)

    @pook.on
    def test_create_all_from_esi(self):
        # given
        race_1_id = 1
        race_2_id = 8
        pook.get(
            make_esi_url("universe/races"),
            reply=200,
            response_json=[
                {
                    "alliance_id": 500001,
                    "description": "Founded on the tenets of patriotism and ..",
                    "name": "Caldari",
                    "race_id": race_1_id,
                },
                {
                    "alliance_id": 500004,
                    "description": "Champions of liberty and defenders of ...",
                    "name": "Gallente",
                    "race_id": race_2_id,
                },
            ],
        )

        # when
        EveRace.objects.update_or_create_all_esi()

        # then
        self.assertEqual(EveRace.objects.count(), 2)
        self.assertTrue(EveRace.objects.filter(id=race_1_id).exists())
        self.assertTrue(EveRace.objects.filter(id=race_2_id).exists())


class TestEveRegion(TestCaseWithClearCache):

    @pook.on
    def test_create_from_esi(self):
        # given
        region_id = 10000069
        description = "Black Rise description"
        name = "Black Rise"
        pook.get(
            make_esi_url(f"universe/regions/{region_id}"),
            reply=200,
            response_json={
                "constellations": [20000785],
                "description": description,
                "name": name,
                "region_id": region_id,
            },
        )

        # when
        obj: EveRegion
        obj, created = EveRegion.objects.update_or_create_esi(id=region_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, region_id)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.description, description)
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_REGION)

    @pook.on
    def test_create_all_from_esi(self):
        # given
        id_1 = 1
        id_2 = 2
        pook.get(
            make_esi_url("universe/regions"),
            reply=200,
            response_json=[id_1, id_2],
        )
        pook.get(
            make_esi_url(f"universe/regions/{id_1}"),
            reply=200,
            response_json={
                "constellations": [20000785],
                "description": "description-1",
                "name": "name-1",
                "region_id": id_1,
            },
        )
        pook.get(
            make_esi_url(f"universe/regions/{id_2}"),
            reply=200,
            response_json={
                "constellations": [42],
                "description": "description-2",
                "name": "name-2",
                "region_id": id_2,
            },
        )

        # when
        EveRegion.objects.update_or_create_all_esi()

        # then
        self.assertTrue(EveRegion.objects.filter(id=id_1).exists())


@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
class TestEveStar(TestCaseWithClearCache):

    @pook.on
    def test_create_from_esi(self):
        # given
        star_id = 40349466
        age = 37075060962
        et = EveTypeFactory()
        luminosity = 0.02542000077664852
        name = "Enaluri - Star"
        radius = 590000000
        solar_system = EveSolarSystemFactory()
        spectral_class = "M6 V"
        temperature = 2385
        pook.get(
            make_esi_url(f"universe/stars/{star_id}"),
            reply=200,
            response_json={
                "age": age,
                "luminosity": luminosity,
                "name": name,
                "radius": radius,
                "solar_system_id": solar_system.id,
                "spectral_class": spectral_class,
                "temperature": temperature,
                "type_id": et.id,
            },
        )

        # when
        obj: EveStar
        obj, created = EveStar.objects.update_or_create_esi(id=star_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.age, age)
        self.assertEqual(obj.eve_type, et)
        self.assertEqual(obj.id, star_id)
        self.assertEqual(obj.luminosity, luminosity)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.radius, radius)
        self.assertEqual(obj.spectral_class, spectral_class)
        self.assertEqual(obj.temperature, temperature)


class TestEveStargate(TestCaseWithClearCache):

    @pook.on
    def test_should_create_stargate_from_esi(self):
        # given
        stargate_id = 50016284
        destination = EveStargateFactory()
        et = EveTypeFactory()
        name = "Stargate (Akidagi)"
        position = PositionFactory()
        solar_system = EveSolarSystemFactory()
        pook.get(
            make_esi_url(f"universe/stargates/{stargate_id}"),
            reply=200,
            response_json={
                "destination": {
                    "stargate_id": destination.id,
                    "system_id": destination.eve_solar_system.id,
                },
                "name": name,
                "position": position,
                "stargate_id": stargate_id,
                "system_id": solar_system.id,
                "type_id": et.id,
            },
        )

        # when
        obj: EveStargate
        obj, created = EveStargate.objects.get_or_create_esi(id=stargate_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, stargate_id)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.position_x, position["x"])
        self.assertEqual(obj.position_y, position["y"])
        self.assertEqual(obj.position_z, position["z"])
        self.assertEqual(obj.eve_solar_system, solar_system)
        self.assertEqual(obj.eve_type, et)
        self.assertEqual(obj.destination_eve_stargate, destination)
        self.assertEqual(obj.destination_eve_solar_system, destination.eve_solar_system)
        self.assertEqual(obj.eve_entity_category(), "")

    @pook.on
    def test_should_create_stargate_from_esi_without_destination(self):
        # given
        stargate_id = 50016284
        et = EveTypeFactory()
        name = "Stargate (Akidagi)"
        position = PositionFactory()
        solar_system = EveSolarSystemFactory()
        pook.get(
            make_esi_url(f"universe/stargates/{stargate_id}"),
            reply=200,
            response_json={
                "destination": {
                    "stargate_id": 42,
                    "system_id": 666,
                },
                "name": name,
                "position": position,
                "stargate_id": stargate_id,
                "system_id": solar_system.id,
                "type_id": et.id,
            },
        )

        # when
        obj: EveStargate
        obj, created = EveStargate.objects.get_or_create_esi(id=stargate_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, stargate_id)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.position_x, position["x"])
        self.assertEqual(obj.position_y, position["y"])
        self.assertEqual(obj.position_z, position["z"])
        self.assertEqual(obj.eve_solar_system, solar_system)
        self.assertEqual(obj.eve_type, et)
        self.assertIsNone(obj.destination_eve_stargate)
        self.assertIsNone(obj.destination_eve_solar_system)
        self.assertEqual(obj.eve_entity_category(), "")


class TestEveStation(TestCaseWithClearCache):

    @pook.on
    def test_create_from_esi(self):
        # given
        station_id = 60015068
        et = EveTypeFactory()
        er = EveRaceFactory()
        es = EveSolarSystemFactory()
        position = PositionFactory()
        owner_id = 1000180
        volume = 50000000
        cost = 118744
        reprocessing_efficiency = 0.5
        reprocessing_stations_take = 0.025
        name = "Enaluri V - State Protectorate Assembly Plant"
        pook.get(
            make_esi_url(f"universe/stations/{station_id}"),
            reply=200,
            response_json={
                "max_dockable_ship_volume": volume,
                "name": name,
                "office_rental_cost": cost,
                "owner": owner_id,
                "position": position,
                "race_id": er.id,
                "reprocessing_efficiency": reprocessing_efficiency,
                "reprocessing_stations_take": reprocessing_stations_take,
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
                "system_id": es.id,
                "type_id": et.id,
            },
        )

        # when
        obj: EveStation
        obj, created = EveStation.objects.update_or_create_esi(id=station_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, station_id)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.max_dockable_ship_volume, volume)
        self.assertEqual(obj.office_rental_cost, cost)
        self.assertEqual(obj.owner_id, owner_id)
        self.assertEqual(obj.position_x, position["x"])
        self.assertEqual(obj.position_y, position["y"])
        self.assertEqual(obj.position_z, position["z"])
        self.assertEqual(obj.reprocessing_efficiency, reprocessing_efficiency)
        self.assertEqual(obj.reprocessing_stations_take, reprocessing_stations_take)
        self.assertEqual(obj.eve_race, er)
        self.assertEqual(obj.eve_type, et)
        self.assertEqual(obj.eve_solar_system, es)
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_STATION)

        self.assertSetEqual(
            set(obj.services.values_list("name", flat=True)),
            {
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
            },
        )
