from unittest.mock import patch

from eveuniverse.constants import EveGroupId
from eveuniverse.core import evesdeapi
from eveuniverse.models import (
    EveAsteroidBelt,
    EveMoon,
    EvePlanet,
    EveSolarSystem,
    EveStar,
    EveStargate,
    EveStation,
    EveType,
)
from eveuniverse.utils import NoSocketsTestCase

from ..testdata.esi import EsiClientStub

MODELS_PATH = "eveuniverse.models"
MANAGERS_PATH = "eveuniverse.managers.universe"


class TestEveTypeSection(NoSocketsTestCase):
    def test_should_return_value_as_str(self):
        self.assertEqual(str(EveType.Section.DOGMAS), "dogmas")

    def test_should_return_values(self):
        self.assertEqual(
            list(EveType.Section),
            [
                "dogmas",
                "graphics",
                "market_groups",
                "type_materials",
                "industry_activities",
            ],
        )


@patch(MANAGERS_PATH + ".esi")
class TestEveSolarSystemWithSections(NoSocketsTestCase):
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_create_solar_system_without_sections(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveSolarSystem.objects.update_or_create_esi(id=30045339)
        # then
        self.assertEqual(obj.id, 30045339)
        self.assertEqual(obj.enabled_sections._value, 0)

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", True)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_create_solar_system_with_planets_global(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveSolarSystem.objects.update_or_create_esi(
            id=30045339, include_children=True
        )
        # then
        self.assertEqual(obj.id, 30045339)
        self.assertTrue(obj.enabled_sections.planets)
        self.assertEqual(
            set(obj.eve_planets.values_list("id", flat=True)), {40349467, 40349471}
        )

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_create_solar_system_with_planets_on_demand(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveSolarSystem.objects.update_or_create_esi(
            id=30045339,
            include_children=True,
            enabled_sections=[EveSolarSystem.Section.PLANETS],
        )
        # then
        self.assertEqual(obj.id, 30045339)
        self.assertTrue(obj.enabled_sections.planets)
        self.assertEqual(
            set(obj.eve_planets.values_list("id", flat=True)), {40349467, 40349471}
        )

    # @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
    # @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    # @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    # @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    # def test_should_create_solar_system_with_planets_on_demand_2(self, mock_esi):
    #     # given
    #     mock_esi.client = EsiClientStub()
    #     # when
    #     obj, _ = EveSolarSystem.objects.update_or_create_esi(
    #         id=30045339,
    #         include_children=True,
    #         enabled_sections=[EveSolarSystem.Section.PLANETS],
    #     )
    #     # then
    #     self.assertEqual(obj.id, 30045339)
    #     self.assertTrue(obj.enabled_sections.planets)
    #     self.assertEqual(
    #         set(obj.eve_planets.values_list("id", flat=True)), {40349467, 40349471}
    #     )

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", True)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_create_solar_system_with_stargates_global(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveSolarSystem.objects.update_or_create_esi(
            id=30045339, include_children=True
        )
        # then
        self.assertEqual(obj.id, 30045339)
        self.assertTrue(obj.enabled_sections.stargates)
        self.assertEqual(
            set(obj.eve_stargates.values_list("id", flat=True)), {50016284, 50016286}
        )

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_create_solar_system_with_stargates_on_demand(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveSolarSystem.objects.update_or_create_esi(
            id=30045339,
            include_children=True,
            enabled_sections=[EveSolarSystem.Section.STARGATES],
        )
        # then
        self.assertEqual(obj.id, 30045339)
        self.assertTrue(obj.enabled_sections.stargates)
        self.assertEqual(
            set(obj.eve_stargates.values_list("id", flat=True)), {50016284, 50016286}
        )

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_not_mark_section_as_updated_when_children_are_not_fetched(
        self, mock_esi
    ):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveSolarSystem.objects.update_or_create_esi(
            id=30045339,
            enabled_sections=[EveSolarSystem.Section.STARGATES, EveType.Section.DOGMAS],
        )
        # then
        self.assertEqual(obj.id, 30045339)
        self.assertFalse(obj.enabled_sections.stargates)

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", True)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_create_solar_system_with_stars_global(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveSolarSystem.objects.update_or_create_esi(
            id=30045339, include_children=True
        )
        # then
        self.assertEqual(obj.id, 30045339)
        self.assertTrue(obj.enabled_sections.stars)
        self.assertEqual(obj.eve_star_id, 40349466)

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_create_solar_system_with_stars_on_demand(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveSolarSystem.objects.update_or_create_esi(
            id=30045339,
            include_children=True,
            enabled_sections=[EveSolarSystem.Section.STARS],
        )
        # then
        self.assertEqual(obj.id, 30045339)
        self.assertTrue(obj.enabled_sections.stars)
        self.assertEqual(obj.eve_star_id, 40349466)

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", True)
    def test_should_create_solar_system_with_stations_global(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveSolarSystem.objects.update_or_create_esi(
            id=30045339, include_children=True
        )
        # then
        self.assertEqual(obj.id, 30045339)
        self.assertTrue(obj.enabled_sections.stations)
        self.assertEqual(
            set(obj.eve_stations.values_list("id", flat=True)), {60015068, 60015069}
        )

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_create_solar_system_with_stations_on_demand(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveSolarSystem.objects.update_or_create_esi(
            id=30045339,
            include_children=True,
            enabled_sections=[EveSolarSystem.Section.STATIONS],
        )
        # then
        self.assertEqual(obj.id, 30045339)
        self.assertTrue(obj.enabled_sections.stations)
        self.assertEqual(
            set(obj.eve_stations.values_list("id", flat=True)), {60015068, 60015069}
        )

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_create_solar_system_with_planets_moons_asteroid_belts_on_demand(
        self, mock_esi
    ):
        # given
        mock_esi.client = EsiClientStub()
        # when
        solar_system, _ = EveSolarSystem.objects.update_or_create_esi(
            id=30045339,
            include_children=True,
            enabled_sections=[
                EveSolarSystem.Section.PLANETS,
                EvePlanet.Section.ASTEROID_BELTS,
                EvePlanet.Section.MOONS,
            ],
        )
        # then
        self.assertEqual(solar_system.id, 30045339)
        self.assertTrue(solar_system.enabled_sections.planets)
        self.assertEqual(
            set(solar_system.eve_planets.values_list("id", flat=True)),
            {40349467, 40349471},
        )
        planet = solar_system.eve_planets.get(id=40349471)
        self.assertTrue(planet.enabled_sections.asteroid_belts)
        self.assertTrue(planet.enabled_sections.moons)
        self.assertEqual(
            set(planet.eve_asteroid_belts.values_list("id", flat=True)), {40349487}
        )
        self.assertEqual(
            set(planet.eve_moons.values_list("id", flat=True)), {40349472, 40349473}
        )


@patch(MANAGERS_PATH + ".esi")
class TestEveSolarSystemBulkWithSection(NoSocketsTestCase):
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", True)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_create_solar_system_with_planets_global(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        EveSolarSystem.objects.update_or_create_all_esi(include_children=True)
        # then
        self.assertEqual(
            set(
                EveSolarSystem.objects.filter(
                    enabled_sections=EveSolarSystem.enabled_sections.planets
                ).values_list("id", flat=True)
            ),
            {
                30000142,
                30001161,
                30045339,
                30045342,
                31000005,
                30000157,
                32000018,
                30004984,
            },
        )
        self.assertEqual(
            set(EvePlanet.objects.values_list("id", flat=True)),
            {40009077, 40349467, 40349471},
        )

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_create_solar_system_with_planets_on_demand(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        EveSolarSystem.objects.update_or_create_all_esi(
            include_children=True, enabled_sections=[EveSolarSystem.Section.PLANETS]
        )
        # then
        self.assertSetEqual(
            set(
                EveSolarSystem.objects.filter(
                    enabled_sections=EveSolarSystem.enabled_sections.planets
                ).values_list("id", flat=True)
            ),
            {
                30000142,
                30001161,
                30045339,
                30045342,
                31000005,
                30000157,
                32000018,
                30004984,
            },
        )
        self.assertEqual(
            set(EvePlanet.objects.values_list("id", flat=True)),
            {40009077, 40349467, 40349471},
        )

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", True)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_get_solar_system_with_planets_global(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        EveSolarSystem.objects.bulk_get_or_create_esi(
            ids=[30000142, 30045339], include_children=True
        )
        # then
        self.assertEqual(
            set(
                EveSolarSystem.objects.filter(
                    enabled_sections=EveSolarSystem.enabled_sections.planets
                ).values_list("id", flat=True)
            ),
            {30000142, 30045339},
        )
        self.assertEqual(
            set(EvePlanet.objects.values_list("id", flat=True)),
            {40009077, 40349467, 40349471},
        )

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_get_all_solar_system_with_planets_on_demand_from_scratch(
        self, mock_esi
    ):
        # given
        mock_esi.client = EsiClientStub()
        # when
        EveSolarSystem.objects.bulk_get_or_create_esi(
            ids=[30000142, 30045339],
            include_children=True,
            enabled_sections=[EveSolarSystem.Section.PLANETS],
        )
        # then
        self.assertEqual(
            set(
                EveSolarSystem.objects.filter(
                    enabled_sections=EveSolarSystem.enabled_sections.planets
                ).values_list("id", flat=True)
            ),
            {30000142, 30045339},
        )
        self.assertEqual(
            set(EvePlanet.objects.values_list("id", flat=True)),
            {40009077, 40349467, 40349471},
        )

    @patch(
        MODELS_PATH + ".universe_2.EveSolarSystem.objects.update_or_create_esi",
        wraps=EveSolarSystem.objects.update_or_create_esi,
    )
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_get_all_solar_system_with_planets_on_demand(
        self, spy_manager, mock_esi
    ):
        # given
        mock_esi.client = EsiClientStub()
        # when
        EveSolarSystem.objects.get_or_create_esi(id=30000142)
        EveSolarSystem.objects.bulk_get_or_create_esi(
            ids=[30000142, 30045339],
            include_children=True,
            enabled_sections=[EveSolarSystem.Section.PLANETS],
        )
        # then
        self.assertEqual(
            set(
                EveSolarSystem.objects.filter(
                    enabled_sections=EveSolarSystem.enabled_sections.planets
                ).values_list("id", flat=True)
            ),
            {30000142, 30045339},
        )
        self.assertEqual(
            set(EvePlanet.objects.values_list("id", flat=True)),
            {40009077, 40349467, 40349471},
        )
        self.assertEqual(spy_manager.call_count, 3)

    @patch(
        MODELS_PATH + ".universe_2.EveSolarSystem.objects.update_or_create_esi",
        wraps=EveSolarSystem.objects.update_or_create_esi,
    )
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
    def test_should_get_one_and_load_one_solar_system_with_planets(
        self, spy_manager, mock_esi
    ):
        # given
        mock_esi.client = EsiClientStub()
        # when
        EveSolarSystem.objects.get_or_create_esi(
            id=30000142,
            include_children=True,
            enabled_sections=[EveSolarSystem.Section.PLANETS],
        )
        EveSolarSystem.objects.bulk_get_or_create_esi(
            ids=[30000142, 30045339],
            include_children=True,
            enabled_sections=[EveSolarSystem.Section.PLANETS],
        )
        # then
        self.assertEqual(
            set(
                EveSolarSystem.objects.filter(
                    enabled_sections=EveSolarSystem.enabled_sections.planets
                ).values_list("id", flat=True)
            ),
            {30000142, 30045339},
        )
        self.assertEqual(
            set(EvePlanet.objects.values_list("id", flat=True)),
            {40009077, 40349467, 40349471},
        )
        self.assertEqual(spy_manager.call_count, 2)


@patch(MANAGERS_PATH + ".esi")
class TestEvePlanetWithSections(NoSocketsTestCase):
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_ASTEROID_BELTS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MOONS", False)
    def test_should_create_new_instance_without_sections(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EvePlanet.objects.update_or_create_esi(id=40349471)
        # then
        self.assertEqual(obj.id, 40349471)
        self.assertEqual(obj.eve_asteroid_belts.count(), 0)
        self.assertEqual(obj.eve_moons.count(), 0)
        self.assertEqual(obj.enabled_sections._value, 0)

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_ASTEROID_BELTS", True)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MOONS", False)
    def test_should_create_new_instance_with_asteroid_belts_global(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EvePlanet.objects.update_or_create_esi(
            id=40349471, include_children=True
        )
        # then
        self.assertEqual(obj.id, 40349471)
        self.assertEqual(
            set(obj.eve_asteroid_belts.values_list("id", flat=True)), {40349487}
        )
        self.assertEqual(obj.eve_moons.count(), 0)
        self.assertTrue(obj.enabled_sections.asteroid_belts)
        self.assertFalse(obj.enabled_sections.moons)

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_ASTEROID_BELTS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MOONS", False)
    def test_should_create_new_instance_with_asteroid_belts_on_demand(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EvePlanet.objects.update_or_create_esi(
            id=40349471,
            include_children=True,
            enabled_sections=[EvePlanet.Section.ASTEROID_BELTS],
        )
        # then
        self.assertEqual(obj.id, 40349471)
        self.assertEqual(
            set(obj.eve_asteroid_belts.values_list("id", flat=True)), {40349487}
        )
        self.assertEqual(obj.eve_moons.count(), 0)
        self.assertTrue(obj.enabled_sections.asteroid_belts)
        self.assertFalse(obj.enabled_sections.moons)

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_ASTEROID_BELTS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MOONS", True)
    def test_should_create_new_instance_with_moons_global(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EvePlanet.objects.update_or_create_esi(
            id=40349471, include_children=True
        )
        # then
        self.assertEqual(obj.id, 40349471)
        self.assertEqual(obj.eve_asteroid_belts.count(), 0)
        self.assertEqual(
            set(obj.eve_moons.values_list("id", flat=True)), {40349472, 40349473}
        )
        self.assertFalse(obj.enabled_sections.asteroid_belts)
        self.assertTrue(obj.enabled_sections.moons)

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_ASTEROID_BELTS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MOONS", False)
    def test_should_create_new_instance_with_moons_on_demand(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EvePlanet.objects.update_or_create_esi(
            id=40349471,
            include_children=True,
            enabled_sections=[EvePlanet.Section.MOONS],
        )
        # then
        self.assertEqual(obj.id, 40349471)
        self.assertEqual(obj.eve_asteroid_belts.count(), 0)
        self.assertEqual(
            set(obj.eve_moons.values_list("id", flat=True)), {40349472, 40349473}
        )
        self.assertFalse(obj.enabled_sections.asteroid_belts)
        self.assertTrue(obj.enabled_sections.moons)

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_ASTEROID_BELTS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MOONS", False)
    def test_should_create_new_instance_with_moons_and_asteroid_belts_on_demand(
        self, mock_esi
    ):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EvePlanet.objects.update_or_create_esi(
            id=40349471,
            include_children=True,
            enabled_sections=[
                EvePlanet.Section.MOONS,
                EvePlanet.Section.ASTEROID_BELTS,
            ],
        )
        # then
        self.assertEqual(obj.id, 40349471)
        self.assertEqual(
            set(obj.eve_asteroid_belts.values_list("id", flat=True)), {40349487}
        )
        self.assertEqual(
            set(obj.eve_moons.values_list("id", flat=True)), {40349472, 40349473}
        )
        self.assertTrue(obj.enabled_sections.asteroid_belts)
        self.assertTrue(obj.enabled_sections.moons)


@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_ASTEROID_BELTS", False)
@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False)
@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MOONS", False)
@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False)
@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False)
@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False)
@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False)
@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
@patch(MODELS_PATH + ".universe_2.evesdeapi")
@patch(MANAGERS_PATH + ".esi")
class TestEveSolarSystemNearestCelestial(NoSocketsTestCase):
    def test_should_return_stargate(self, mock_esi, mock_evesdeapi):
        # given
        mock_esi.client = EsiClientStub()
        mock_evesdeapi.nearest_celestial.return_value = evesdeapi.EveItem(
            id=50016284, name="Stargate (Akidagi)", type_id=16, distance=1000
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        # when
        result = enaluri.nearest_celestial(x=-1, y=-2, z=3)
        # then
        self.assertEqual(result.eve_type, EveType.objects.get_or_create_esi(id=16)[0])
        self.assertEqual(
            result.eve_object, EveStargate.objects.get_or_create_esi(id=50016284)[0]
        )
        self.assertEqual(result.distance, 1000)

    def test_should_return_star(self, mock_esi, mock_evesdeapi):
        # given
        mock_esi.client = EsiClientStub()
        mock_evesdeapi.nearest_celestial.return_value = evesdeapi.EveItem(
            id=40349466, name="StaEnaluri - Star", type_id=3800, distance=0
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        # when
        result = enaluri.nearest_celestial(x=0, y=0, z=0)
        # then
        self.assertEqual(result.eve_type, EveType.objects.get_or_create_esi(id=3800)[0])
        self.assertEqual(
            result.eve_object, EveStar.objects.get_or_create_esi(id=40349466)[0]
        )
        self.assertEqual(result.distance, 0)

    def test_should_return_planet(self, mock_esi, mock_evesdeapi):
        # given
        mock_esi.client = EsiClientStub()
        mock_evesdeapi.nearest_celestial.return_value = evesdeapi.EveItem(
            id=40349471, name="Enaluri III", type_id=13, distance=1000
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        # when
        result = enaluri.nearest_celestial(x=-1, y=-2, z=3)
        # then
        self.assertEqual(result.eve_type, EveType.objects.get_or_create_esi(id=13)[0])
        self.assertEqual(
            result.eve_object, EvePlanet.objects.get_or_create_esi(id=40349471)[0]
        )
        self.assertEqual(result.distance, 1000)

    def test_should_return_station(self, mock_esi, mock_evesdeapi):
        # given
        mock_esi.client = EsiClientStub()
        mock_evesdeapi.nearest_celestial.return_value = evesdeapi.EveItem(
            id=60015068,
            name="Enaluri V - State Protectorate Assembly Plant",
            type_id=1529,
            distance=1000,
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        # when
        result = enaluri.nearest_celestial(x=-1, y=-2, z=3)
        # then
        self.assertEqual(result.eve_type, EveType.objects.get_or_create_esi(id=1529)[0])
        self.assertEqual(
            result.eve_object, EveStation.objects.get_or_create_esi(id=60015068)[0]
        )
        self.assertEqual(result.distance, 1000)

    def test_should_return_asteroid_belt(self, mock_esi, mock_evesdeapi):
        # given
        mock_esi.client = EsiClientStub()
        mock_evesdeapi.nearest_celestial.return_value = evesdeapi.EveItem(
            id=40349487, name="Enaluri III - Asteroid Belt 1", type_id=15, distance=1000
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        # when
        result = enaluri.nearest_celestial(x=-1, y=-2, z=3)
        # then
        self.assertEqual(
            result.eve_type,
            EveType.objects.get_or_create_esi(id=15)[0],
        )
        self.assertEqual(
            result.eve_object, EveAsteroidBelt.objects.get_or_create_esi(id=40349487)[0]
        )
        self.assertEqual(result.distance, 1000)

    def test_should_return_moon(self, mock_esi, mock_evesdeapi):
        # given
        mock_esi.client = EsiClientStub()
        mock_evesdeapi.nearest_celestial.return_value = evesdeapi.EveItem(
            id=40349472, name="Enaluri III - Moon 1", type_id=14, distance=1000
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        # when
        result = enaluri.nearest_celestial(x=-1, y=-2, z=3)
        # then
        self.assertEqual(result.eve_type, EveType.objects.get_or_create_esi(id=14)[0])
        self.assertEqual(
            result.eve_object, EveMoon.objects.get_or_create_esi(id=40349472)[0]
        )
        self.assertEqual(result.distance, 1000)

    def test_should_return_none_if_unknown_type(self, mock_esi, mock_evesdeapi):
        # given
        mock_esi.client = EsiClientStub()
        mock_evesdeapi.nearest_celestial.return_value = evesdeapi.EveItem(
            id=99, name="Merlin", type_id=603, distance=1000
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        # when
        result = enaluri.nearest_celestial(x=-1, y=-2, z=3)
        # then
        self.assertIsNone(result)

    def test_should_return_none_if_not_found(self, mock_esi, mock_evesdeapi):
        # given
        mock_esi.client = EsiClientStub()
        mock_evesdeapi.nearest_celestial.return_value = None
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        # when
        result = enaluri.nearest_celestial(x=-1, y=-2, z=3)
        # then
        self.assertIsNone(result)

    def test_should_return_moon_by_group(self, mock_esi, mock_evesdeapi):
        # given
        mock_esi.client = EsiClientStub()
        mock_evesdeapi.nearest_celestial.return_value = evesdeapi.EveItem(
            id=40349472, name="Enaluri III - Moon 1", type_id=14, distance=1000
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        # when
        result = enaluri.nearest_celestial(x=-1, y=-2, z=3, group_id=EveGroupId.MOON)
        # then
        self.assertEqual(result.eve_type, EveType.objects.get_or_create_esi(id=14)[0])
        self.assertEqual(
            result.eve_object, EveMoon.objects.get_or_create_esi(id=40349472)[0]
        )
        self.assertEqual(result.distance, 1000)
