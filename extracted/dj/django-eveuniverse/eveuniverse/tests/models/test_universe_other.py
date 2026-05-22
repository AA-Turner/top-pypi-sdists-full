import pook
from esi.exceptions import HTTPClientError

from eveuniverse.models import EveAncestry, EveBloodline, EveEntity, EveFaction
from eveuniverse.tests.helpers import TestCaseWithClearCache
from eveuniverse.tests.testdata.factories_2 import (
    EveBloodlineFactory,
    EveEntityCorporationFactory,
    EveRaceFactory,
    EveSolarSystemFactory,
    ShipTypeFactory,
    make_esi_url,
)


class TestEveAncestry(TestCaseWithClearCache):
    @pook.on
    def test_create_from_esi(self):
        # given
        bloodline_1 = EveBloodlineFactory()
        bloodline_2 = EveBloodlineFactory()
        pook.get(
            make_esi_url("universe/ancestries"),
            reply=200,
            response_json=[
                {
                    "bloodline_id": bloodline_1.id,
                    "description": "string",
                    "icon_id": 11,
                    "id": 1,
                    "name": "Alpha",
                    "short_description": "alpha-description",
                },
                {
                    "bloodline_id": bloodline_2.id,
                    "description": "string",
                    "icon_id": 12,
                    "id": 2,
                    "name": "Bravo",
                    "short_description": "bravo-description",
                },
            ],
        )

        # when
        obj: EveAncestry
        obj, created = EveAncestry.objects.update_or_create_esi(id=2)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, 2)
        self.assertEqual(obj.name, "Bravo")
        self.assertEqual(obj.icon_id, 12)
        self.assertEqual(obj.eve_bloodline, bloodline_2)
        self.assertEqual(obj.short_description, "bravo-description")


class TestEveBloodline(TestCaseWithClearCache):
    @pook.on
    def test_can_create_from_esi_with_all_fields(self):
        # given
        corporation = EveEntityCorporationFactory()
        ship_type = ShipTypeFactory()
        race = EveRaceFactory()
        bloodline_id = 42
        name = "Alpha"
        charisma = 1
        intelligence = 2
        memory = 3
        perception = 4
        willpower = 5
        description = "description"
        pook.get(
            make_esi_url("universe/bloodlines"),
            reply=200,
            response_json=[
                {
                    "bloodline_id": bloodline_id,
                    "charisma": charisma,
                    "corporation_id": corporation.id,
                    "description": description,
                    "intelligence": intelligence,
                    "memory": memory,
                    "name": name,
                    "perception": perception,
                    "race_id": race.id,
                    "ship_type_id": ship_type.id,
                    "willpower": willpower,
                }
            ],
        )

        # when
        obj: EveBloodline
        obj, created = EveBloodline.objects.update_or_create_esi(id=bloodline_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.charisma, charisma)
        self.assertEqual(obj.corporation_id, corporation.id)
        self.assertEqual(obj.description, description)
        self.assertEqual(obj.eve_race, race)
        self.assertEqual(obj.eve_ship_type, ship_type)
        self.assertEqual(obj.id, bloodline_id)
        self.assertEqual(obj.intelligence, intelligence)
        self.assertEqual(obj.memory, memory)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.perception, perception)
        self.assertEqual(obj.willpower, willpower)

    @pook.on
    def test_create_from_esi_without_ship_type(self):
        """
        This test verifies that the workaround for issue #27 is in place.
        The workaround is set the field `ship_type_id` as optional in the spec file.
        """
        # given
        corporation = EveEntityCorporationFactory()
        ship_type_id = None
        race = EveRaceFactory()
        bloodline_id = 42
        name = "Bravo"
        charisma = 0
        intelligence = 0
        memory = 0
        perception = 0
        willpower = 0
        description = "description"
        pook.get(
            make_esi_url("universe/bloodlines"),
            reply=200,
            response_json=[
                {
                    "bloodline_id": bloodline_id,
                    "charisma": charisma,
                    "corporation_id": corporation.id,
                    "description": description,
                    "intelligence": intelligence,
                    "memory": memory,
                    "name": name,
                    "perception": perception,
                    "race_id": race.id,
                    "ship_type_id": ship_type_id,
                    "willpower": willpower,
                }
            ],
        )

        # when
        obj: EveBloodline
        obj, created = EveBloodline.objects.update_or_create_esi(id=bloodline_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.charisma, charisma)
        self.assertEqual(obj.corporation_id, corporation.id)
        self.assertEqual(obj.description, description)
        self.assertEqual(obj.eve_race, race)
        self.assertIsNone(obj.eve_ship_type)
        self.assertEqual(obj.id, bloodline_id)
        self.assertEqual(obj.intelligence, intelligence)
        self.assertEqual(obj.memory, memory)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.perception, perception)
        self.assertEqual(obj.willpower, willpower)

    @pook.on
    def test_raise_404_exception_when_object_not_found(self):
        # given
        bloodline = EveBloodlineFactory()
        pook.get(
            make_esi_url("universe/ancestries"),
            reply=200,
            response_json=[
                {
                    "bloodline_id": bloodline.id,
                    "description": "string",
                    "icon_id": 11,
                    "id": 1,
                    "name": "Alpha",
                    "short_description": "alpha-description",
                }
            ],
        )

        # when/then
        with self.assertRaises(HTTPClientError) as ex:
            EveAncestry.objects.update_or_create_esi(id=666)
            self.assertEqual(ex.exception.status_code, 404)


class TestEveFaction(TestCaseWithClearCache):
    @pook.on
    def test_can_create_from_esi(self):
        # given
        faction_id = 500001
        solar_system = EveSolarSystemFactory()
        pook.get(
            make_esi_url("universe/factions"),
            reply=200,
            response_json=[
                {
                    "corporation_id": 1000035,
                    "description": "The Caldari State is ruled by several mega-corporations. ...",
                    "faction_id": faction_id,
                    "is_unique": True,
                    "militia_corporation_id": 1000180,
                    "name": "Caldari State",
                    "size_factor": 5,
                    "solar_system_id": solar_system.id,
                    "station_count": 1503,
                    "station_system_count": 503,
                },
                {
                    "corporation_id": 1000051,
                    "description": "The Minmatar Republic was formed ...",
                    "faction_id": 500002,
                    "is_unique": True,
                    "militia_corporation_id": 1000182,
                    "name": "Minmatar Republic",
                    "size_factor": 5,
                    "solar_system_id": solar_system.id,
                    "station_count": 570,
                    "station_system_count": 291,
                },
            ],
        )

        # when
        obj: EveFaction
        obj, created = EveFaction.objects.get_or_create_esi(id=faction_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, faction_id)
        self.assertEqual(obj.name, "Caldari State")
        self.assertTrue(obj.is_unique)
        self.assertEqual(obj.militia_corporation_id, 1000180)
        self.assertEqual(obj.eve_solar_system, solar_system)
        self.assertEqual(obj.size_factor, 5)
        self.assertEqual(obj.station_count, 1503)
        self.assertEqual(obj.station_system_count, 503)
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_FACTION)
        self.assertEqual(obj.size_factor, 5)
        self.assertEqual(obj.station_count, 1503)
        self.assertEqual(obj.station_system_count, 503)
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_FACTION)
