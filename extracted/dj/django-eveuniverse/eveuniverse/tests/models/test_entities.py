"""Eve Entity tests."""

from typing import Dict
from unittest.mock import patch

from eveuniverse.models import EveEntity
from eveuniverse.utils import NoSocketsTestCase

from ..testdata.esi import BravadoOperationStub, EsiClientStub
from ..testdata.factories import create_eve_entity

MANAGERS_PATH = "eveuniverse.managers.entities"


@patch(MANAGERS_PATH + ".esi")
class TestEveEntityQuerySet(NoSocketsTestCase):
    def test_can_update_one(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        obj_1001 = create_eve_entity(id=1001)
        entities = EveEntity.objects.all()
        # when
        result = entities.update_from_esi()
        # then
        obj_1001.refresh_from_db()
        self.assertEqual(result, 1)
        self.assertEqual(obj_1001.name, "Bruce Wayne")
        self.assertEqual(obj_1001.category, EveEntity.CATEGORY_CHARACTER)

    def test_can_update_many(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        obj_1001 = create_eve_entity(id=1001)
        obj_1002 = create_eve_entity(id=1002)
        obj_2001 = create_eve_entity(id=2001)
        entities = EveEntity.objects.all()
        # when
        result = entities.update_from_esi()
        # then
        self.assertEqual(result, 3)
        obj_1001.refresh_from_db()
        self.assertEqual(obj_1001.name, "Bruce Wayne")
        self.assertEqual(obj_1001.category, EveEntity.CATEGORY_CHARACTER)
        obj_1002.refresh_from_db()
        self.assertEqual(obj_1002.name, "Peter Parker")
        self.assertEqual(obj_1002.category, EveEntity.CATEGORY_CHARACTER)
        obj_2001.refresh_from_db()
        self.assertEqual(obj_2001.name, "Wayne Technologies")
        self.assertEqual(obj_2001.category, EveEntity.CATEGORY_CORPORATION)

    def test_can_divide_and_conquer(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        obj_1001 = create_eve_entity(id=1001)
        obj_1002 = create_eve_entity(id=1002)
        obj_2001 = create_eve_entity(id=2001)
        create_eve_entity(id=9999)
        entities = EveEntity.objects.all()
        # when
        result = entities.update_from_esi()
        self.assertEqual(result, 3)
        obj_1001.refresh_from_db()
        self.assertEqual(obj_1001.name, "Bruce Wayne")
        self.assertEqual(obj_1001.category, EveEntity.CATEGORY_CHARACTER)
        obj_1002.refresh_from_db()
        self.assertEqual(obj_1002.name, "Peter Parker")
        self.assertEqual(obj_1002.category, EveEntity.CATEGORY_CHARACTER)
        obj_2001.refresh_from_db()
        self.assertEqual(obj_2001.name, "Wayne Technologies")
        self.assertEqual(obj_2001.category, EveEntity.CATEGORY_CORPORATION)

    def test_can_ignore_invalid_ids(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        obj_1001 = create_eve_entity(id=1001)
        create_eve_entity(id=1)
        entities = EveEntity.objects.all()
        # when
        result = entities.update_from_esi()
        # then
        self.assertEqual(result, 1)
        obj_1001.refresh_from_db()
        self.assertEqual(result, 1)
        self.assertEqual(obj_1001.name, "Bruce Wayne")
        self.assertEqual(obj_1001.category, EveEntity.CATEGORY_CHARACTER)


class TestEveEntityModel(NoSocketsTestCase):
    def test_is_npc_1(self):
        """when entity is NPC character, then return True"""
        obj = EveEntity(id=3019583, category=EveEntity.CATEGORY_CHARACTER)
        self.assertTrue(obj.is_npc)

    def test_is_npc_2(self):
        """when entity is NPC corporation, then return True"""
        obj = EveEntity(id=1000274, category=EveEntity.CATEGORY_CORPORATION)
        self.assertTrue(obj.is_npc)

    def test_is_npc_3(self):
        """when entity is normal character, then return False"""
        obj = EveEntity(id=93330670, category=EveEntity.CATEGORY_CHARACTER)
        self.assertFalse(obj.is_npc)

    def test_is_npc_4(self):
        """when entity is normal corporation, then return False"""
        obj = EveEntity(id=98394960, category=EveEntity.CATEGORY_CORPORATION)
        self.assertFalse(obj.is_npc)

    def test_is_npc_5(self):
        """when entity is normal alliance, then return False"""
        obj = EveEntity(id=99008435, category=EveEntity.CATEGORY_ALLIANCE)
        self.assertFalse(obj.is_npc)

    def test_is_npc_starter_corporation_1(self):
        obj = EveEntity(id=1000165, category=EveEntity.CATEGORY_CORPORATION)
        self.assertTrue(obj.is_npc_starter_corporation)

    def test_is_npc_starter_corporation_2(self):
        obj = EveEntity(id=98394960, category=EveEntity.CATEGORY_CORPORATION)
        self.assertFalse(obj.is_npc_starter_corporation)

    def test_is_npc_starter_corporation_3(self):
        obj = EveEntity(id=1000274, category=EveEntity.CATEGORY_CORPORATION)
        self.assertFalse(obj.is_npc_starter_corporation)

    def test_repr(self):
        # given
        obj = EveEntity(
            id=1001, name="Bruce Wayne", category=EveEntity.CATEGORY_CHARACTER
        )
        # when/then
        self.assertEqual(
            repr(obj), "EveEntity(category='character', id=1001, name='Bruce Wayne')"
        )

    def test_can_create_icon_urls_alliance(self):
        obj = EveEntity(id=3001, category=EveEntity.CATEGORY_ALLIANCE)
        expected = "https://images.evetech.net/alliances/3001/logo?size=128"
        self.assertEqual(obj.icon_url(128), expected)

    def test_can_create_icon_urls_character(self):
        obj = EveEntity(id=1001, category=EveEntity.CATEGORY_CHARACTER)
        expected = "https://images.evetech.net/characters/1001/portrait?size=128"
        self.assertEqual(obj.icon_url(128), expected)

    def test_can_create_icon_urls_corporation(self):
        obj = EveEntity(id=2001, category=EveEntity.CATEGORY_CORPORATION)
        expected = "https://images.evetech.net/corporations/2001/logo?size=128"
        self.assertEqual(obj.icon_url(128), expected)

    def test_can_create_icon_urls_type(self):
        obj = EveEntity(id=603, category=EveEntity.CATEGORY_INVENTORY_TYPE)
        expected = "https://images.evetech.net/types/603/icon?size=128"
        self.assertEqual(obj.icon_url(128), expected)


@patch(MANAGERS_PATH + ".esi")
class TestEveEntityManagerEsi(NoSocketsTestCase):
    def test_can_create_new_from_esi_with_id(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, created = EveEntity.objects.update_or_create_esi(id=1001)
        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, 1001)
        self.assertEqual(obj.name, "Bruce Wayne")
        self.assertEqual(obj.category, EveEntity.CATEGORY_CHARACTER)

    def test_get_or_create_esi_with_id_1(self, mock_esi):
        """when object already exists, then just return it"""
        # given
        mock_esi.client = EsiClientStub()
        obj_1 = create_eve_entity(id=1001, name="New Name")
        # when
        obj_2, created = EveEntity.objects.get_or_create_esi(id=1001)
        # then
        self.assertFalse(created)
        self.assertEqual(obj_1, obj_2)

    def test_get_or_create_esi_with_id_2(self, mock_esi):
        """when object doesn't exist, then fetch it from ESi"""
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, created = EveEntity.objects.get_or_create_esi(id=1001)
        # then
        self.assertTrue(created)
        self.assertEqual(obj.name, "Bruce Wayne")

    def test_get_or_create_esi_with_id_3(self, mock_esi):
        """when ID is invalid, then return an empty object"""
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, created = EveEntity.objects.get_or_create_esi(id=9999)
        # then
        self.assertIsNone(obj)
        self.assertFalse(created)

    def test_get_or_create_esi_with_id_4(self, mock_esi):
        """when object already exists and has not yet been resolved, fetch it from ESI"""
        # given
        mock_esi.client = EsiClientStub()
        create_eve_entity(id=1001)
        # when
        obj, created = EveEntity.objects.get_or_create_esi(id=1001)
        # then
        self.assertFalse(created)
        self.assertEqual(obj.name, "Bruce Wayne")

    def test_can_update_existing_from_esi(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        create_eve_entity(
            id=1001, name="John Doe", category=EveEntity.CATEGORY_CORPORATION
        )
        # when
        obj, created = EveEntity.objects.update_or_create_esi(id=1001)
        # then
        self.assertFalse(created)
        self.assertEqual(obj.id, 1001)
        self.assertEqual(obj.name, "Bruce Wayne")
        self.assertEqual(obj.category, EveEntity.CATEGORY_CHARACTER)

    def test_should_return_none_when_trying_to_create_from_invalid_id(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, created = EveEntity.objects.update_or_create_esi(id=1)
        # then
        self.assertFalse(created)
        self.assertIsNone(obj)

    def test_update_or_create_all_esi_raises_exception(self, _):
        with self.assertRaises(NotImplementedError):
            EveEntity.objects.update_or_create_all_esi()

    def test_can_bulk_update_new_from_esi(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        create_eve_entity(id=1001)
        create_eve_entity(id=2001)
        # when
        result = EveEntity.objects.bulk_update_new_esi()
        # then
        self.assertEqual(result, 2)
        obj = EveEntity.objects.get(id=1001)
        self.assertEqual(obj.id, 1001)
        self.assertEqual(obj.name, "Bruce Wayne")
        self.assertEqual(obj.category, EveEntity.CATEGORY_CHARACTER)
        obj = EveEntity.objects.get(id=2001)
        self.assertEqual(obj.id, 2001)
        self.assertEqual(obj.name, "Wayne Technologies")
        self.assertEqual(obj.category, EveEntity.CATEGORY_CORPORATION)

    def test_bulk_update_all_esi(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        e1 = create_eve_entity(id=1001)
        e2 = create_eve_entity(id=2001)
        # when
        EveEntity.objects.bulk_update_all_esi()
        # then
        e1.refresh_from_db()
        self.assertEqual(e1.name, "Bruce Wayne")
        e2.refresh_from_db()
        self.assertEqual(e2.name, "Wayne Technologies")

    def test_can_resolve_name(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        self.assertEqual(EveEntity.objects.resolve_name(1001), "Bruce Wayne")
        self.assertEqual(EveEntity.objects.resolve_name(2001), "Wayne Technologies")
        self.assertEqual(EveEntity.objects.resolve_name(3001), "Wayne Enterprises")
        self.assertEqual(EveEntity.objects.resolve_name(999), "")
        self.assertEqual(EveEntity.objects.resolve_name(None), "")

    def test_can_bulk_resolve_names(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        resolver = EveEntity.objects.bulk_resolve_names([1001, 2001, 3001])
        # when
        self.assertEqual(resolver.to_name(1001), "Bruce Wayne")
        self.assertEqual(resolver.to_name(2001), "Wayne Technologies")
        self.assertEqual(resolver.to_name(3001), "Wayne Enterprises")

    def test_is_alliance(self, mock_esi):
        """when entity is an alliance, then return True, else False"""
        mock_esi.client = EsiClientStub()

        obj, _ = EveEntity.objects.update_or_create_esi(id=3001)  # alliance
        self.assertTrue(obj.is_alliance)
        obj, _ = EveEntity.objects.update_or_create_esi(id=1001)  # character
        self.assertFalse(obj.is_alliance)
        obj, _ = EveEntity.objects.update_or_create_esi(id=20000020)  # constellation
        self.assertFalse(obj.is_alliance)
        obj, _ = EveEntity.objects.update_or_create_esi(id=2001)  # corporation
        self.assertFalse(obj.is_alliance)
        obj, _ = EveEntity.objects.update_or_create_esi(id=500001)  # faction
        self.assertFalse(obj.is_alliance)
        obj, _ = EveEntity.objects.update_or_create_esi(id=603)  # inventory type
        self.assertFalse(obj.is_alliance)
        obj, _ = EveEntity.objects.update_or_create_esi(id=10000069)  # region
        self.assertFalse(obj.is_alliance)
        obj, _ = EveEntity.objects.update_or_create_esi(id=30004984)  # solar system
        self.assertFalse(obj.is_alliance)
        obj, _ = EveEntity.objects.update_or_create_esi(id=60015068)  # station
        self.assertFalse(obj.is_alliance)
        obj = EveEntity(id=666)
        self.assertFalse(obj.is_alliance)

    def test_is_character(self, mock_esi):
        """when entity is a character, then return True, else False"""
        mock_esi.client = EsiClientStub()

        obj, _ = EveEntity.objects.update_or_create_esi(id=3001)  # alliance
        self.assertFalse(obj.is_character)
        obj, _ = EveEntity.objects.update_or_create_esi(id=1001)  # character
        self.assertTrue(obj.is_character)
        obj, _ = EveEntity.objects.update_or_create_esi(id=20000020)  # constellation
        self.assertFalse(obj.is_character)
        obj, _ = EveEntity.objects.update_or_create_esi(id=2001)  # corporation
        self.assertFalse(obj.is_character)
        obj, _ = EveEntity.objects.update_or_create_esi(id=500001)  # faction
        self.assertFalse(obj.is_character)
        obj, _ = EveEntity.objects.update_or_create_esi(id=603)  # inventory type
        self.assertFalse(obj.is_character)
        obj, _ = EveEntity.objects.update_or_create_esi(id=10000069)  # region
        self.assertFalse(obj.is_character)
        obj, _ = EveEntity.objects.update_or_create_esi(id=30004984)  # solar system
        self.assertFalse(obj.is_character)
        obj, _ = EveEntity.objects.update_or_create_esi(id=60015068)  # station
        self.assertFalse(obj.is_character)
        obj = EveEntity(id=666)
        self.assertFalse(obj.is_character)

    def test_is_constellation(self, mock_esi):
        """when entity is a constellation, then return True, else False"""
        mock_esi.client = EsiClientStub()

        obj, _ = EveEntity.objects.update_or_create_esi(id=3001)  # alliance
        self.assertFalse(obj.is_constellation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=1001)  # character
        self.assertFalse(obj.is_constellation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=20000020)  # constellation
        self.assertTrue(obj.is_constellation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=2001)  # corporation
        self.assertFalse(obj.is_constellation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=500001)  # faction
        self.assertFalse(obj.is_constellation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=603)  # inventory type
        self.assertFalse(obj.is_constellation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=10000069)  # region
        self.assertFalse(obj.is_constellation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=30004984)  # solar system
        self.assertFalse(obj.is_constellation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=60015068)  # station
        self.assertFalse(obj.is_constellation)
        obj = EveEntity(id=666)
        self.assertFalse(obj.is_constellation)

    def test_is_corporation(self, mock_esi):
        """when entity is a corporation, then return True, else False"""
        mock_esi.client = EsiClientStub()

        obj, _ = EveEntity.objects.update_or_create_esi(id=3001)  # alliance
        self.assertFalse(obj.is_corporation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=1001)  # character
        self.assertFalse(obj.is_corporation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=20000020)  # constellation
        self.assertFalse(obj.is_corporation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=2001)  # corporation
        self.assertTrue(obj.is_corporation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=500001)  # faction
        self.assertFalse(obj.is_corporation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=603)  # inventory type
        self.assertFalse(obj.is_corporation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=10000069)  # region
        self.assertFalse(obj.is_corporation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=30004984)  # solar system
        self.assertFalse(obj.is_corporation)
        obj, _ = EveEntity.objects.update_or_create_esi(id=60015068)  # station
        self.assertFalse(obj.is_corporation)
        obj = EveEntity(id=666)
        self.assertFalse(obj.is_corporation)

    def test_is_faction(self, mock_esi):
        """when entity is a faction, then return True, else False"""
        mock_esi.client = EsiClientStub()

        obj, _ = EveEntity.objects.update_or_create_esi(id=3001)  # alliance
        self.assertFalse(obj.is_faction)
        obj, _ = EveEntity.objects.update_or_create_esi(id=1001)  # character
        self.assertFalse(obj.is_faction)
        obj, _ = EveEntity.objects.update_or_create_esi(id=20000020)  # constellation
        self.assertFalse(obj.is_faction)
        obj, _ = EveEntity.objects.update_or_create_esi(id=2001)  # corporation
        self.assertFalse(obj.is_faction)
        obj, _ = EveEntity.objects.update_or_create_esi(id=500001)  # faction
        self.assertTrue(obj.is_faction)
        obj, _ = EveEntity.objects.update_or_create_esi(id=603)  # inventory type
        self.assertFalse(obj.is_faction)
        obj, _ = EveEntity.objects.update_or_create_esi(id=10000069)  # region
        self.assertFalse(obj.is_faction)
        obj, _ = EveEntity.objects.update_or_create_esi(id=30004984)  # solar system
        self.assertFalse(obj.is_faction)
        obj, _ = EveEntity.objects.update_or_create_esi(id=60015068)  # station
        self.assertFalse(obj.is_faction)
        obj = EveEntity(id=666)
        self.assertFalse(obj.is_faction)

    def test_is_type(self, mock_esi):
        """when entity is an inventory type, then return True, else False"""
        mock_esi.client = EsiClientStub()

        obj, _ = EveEntity.objects.update_or_create_esi(id=3001)  # alliance
        self.assertFalse(obj.is_type)
        obj, _ = EveEntity.objects.update_or_create_esi(id=1001)  # character
        self.assertFalse(obj.is_type)
        obj, _ = EveEntity.objects.update_or_create_esi(id=20000020)  # constellation
        self.assertFalse(obj.is_type)
        obj, _ = EveEntity.objects.update_or_create_esi(id=2001)  # corporation
        self.assertFalse(obj.is_type)
        obj, _ = EveEntity.objects.update_or_create_esi(id=500001)  # faction
        self.assertFalse(obj.is_type)
        obj, _ = EveEntity.objects.update_or_create_esi(id=603)  # inventory type
        self.assertTrue(obj.is_type)
        obj, _ = EveEntity.objects.update_or_create_esi(id=10000069)  # region
        self.assertFalse(obj.is_type)
        obj, _ = EveEntity.objects.update_or_create_esi(id=30004984)  # solar system
        self.assertFalse(obj.is_type)
        obj, _ = EveEntity.objects.update_or_create_esi(id=60015068)  # station
        self.assertFalse(obj.is_type)
        obj = EveEntity(id=666)
        self.assertFalse(obj.is_type)

    def test_is_region(self, mock_esi):
        """when entity is a region, then return True, else False"""
        mock_esi.client = EsiClientStub()

        obj, _ = EveEntity.objects.update_or_create_esi(id=3001)  # alliance
        self.assertFalse(obj.is_region)
        obj, _ = EveEntity.objects.update_or_create_esi(id=1001)  # character
        self.assertFalse(obj.is_region)
        obj, _ = EveEntity.objects.update_or_create_esi(id=20000020)  # constellation
        self.assertFalse(obj.is_region)
        obj, _ = EveEntity.objects.update_or_create_esi(id=2001)  # corporation
        self.assertFalse(obj.is_region)
        obj, _ = EveEntity.objects.update_or_create_esi(id=500001)  # faction
        self.assertFalse(obj.is_region)
        obj, _ = EveEntity.objects.update_or_create_esi(id=603)  # inventory type
        self.assertFalse(obj.is_region)
        obj, _ = EveEntity.objects.update_or_create_esi(id=10000069)  # region
        self.assertTrue(obj.is_region)
        obj, _ = EveEntity.objects.update_or_create_esi(id=30004984)  # solar system
        self.assertFalse(obj.is_region)
        obj, _ = EveEntity.objects.update_or_create_esi(id=60015068)  # station
        self.assertFalse(obj.is_region)
        obj = EveEntity(id=666)
        self.assertFalse(obj.is_region)

    def test_is_solar_system(self, mock_esi):
        """when entity is a solar system, then return True, else False"""
        mock_esi.client = EsiClientStub()

        obj, _ = EveEntity.objects.update_or_create_esi(id=3001)  # alliance
        self.assertFalse(obj.is_solar_system)
        obj, _ = EveEntity.objects.update_or_create_esi(id=1001)  # character
        self.assertFalse(obj.is_solar_system)
        obj, _ = EveEntity.objects.update_or_create_esi(id=20000020)  # constellation
        self.assertFalse(obj.is_solar_system)
        obj, _ = EveEntity.objects.update_or_create_esi(id=2001)  # corporation
        self.assertFalse(obj.is_solar_system)
        obj, _ = EveEntity.objects.update_or_create_esi(id=500001)  # faction
        self.assertFalse(obj.is_solar_system)
        obj, _ = EveEntity.objects.update_or_create_esi(id=603)  # inventory type
        self.assertFalse(obj.is_solar_system)
        obj, _ = EveEntity.objects.update_or_create_esi(id=10000069)  # region
        self.assertFalse(obj.is_solar_system)
        obj, _ = EveEntity.objects.update_or_create_esi(id=30004984)  # solar system
        self.assertTrue(obj.is_solar_system)
        obj, _ = EveEntity.objects.update_or_create_esi(id=60015068)  # station
        self.assertFalse(obj.is_solar_system)
        obj = EveEntity(id=666)
        self.assertFalse(obj.is_solar_system)

    def test_is_station(self, mock_esi):
        """when entity is a station, then return True, else False"""
        mock_esi.client = EsiClientStub()

        obj, _ = EveEntity.objects.update_or_create_esi(id=3001)  # alliance
        self.assertFalse(obj.is_station)
        obj, _ = EveEntity.objects.update_or_create_esi(id=1001)  # character
        self.assertFalse(obj.is_station)
        obj, _ = EveEntity.objects.update_or_create_esi(id=20000020)  # constellation
        self.assertFalse(obj.is_station)
        obj, _ = EveEntity.objects.update_or_create_esi(id=2001)  # corporation
        self.assertFalse(obj.is_station)
        obj, _ = EveEntity.objects.update_or_create_esi(id=500001)  # faction
        self.assertFalse(obj.is_station)
        obj, _ = EveEntity.objects.update_or_create_esi(id=603)  # inventory type
        self.assertFalse(obj.is_station)
        obj, _ = EveEntity.objects.update_or_create_esi(id=10000069)  # region
        self.assertFalse(obj.is_station)
        obj, _ = EveEntity.objects.update_or_create_esi(id=30004984)  # solar system
        self.assertFalse(obj.is_station)
        obj, _ = EveEntity.objects.update_or_create_esi(id=60015068)  # station
        self.assertTrue(obj.is_station)
        obj = EveEntity(id=666)
        self.assertFalse(obj.is_station)


@patch(MANAGERS_PATH + ".esi")
class TestEveEntityManagerFetchEntitiesByName(NoSocketsTestCase):
    def test_can_fetch_entity_by_name_from_esi(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        result = EveEntity.objects.fetch_by_names_esi(["Bruce Wayne"])
        # then
        self.assertListEqual(list(result), list(EveEntity.objects.filter(id=1001)))

    def test_can_fetch_multiple_entities_by_name_from_esi(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        result = EveEntity.objects.fetch_by_names_esi(["Bruce Wayne", "Caldari State"])
        # then
        self.assertListEqual(
            list(result), list(EveEntity.objects.filter(id__in=[500001, 1001]))
        )

    def test_should_make_multiple_esi_request_when_fetching_large_number_of_entities(
        self, mock_esi
    ):
        # given
        def my_endpoint(names):
            characters = [
                {"id": int(name.split("_")[1]), "name": name} for name in names
            ]
            data = {"characters": characters}
            return BravadoOperationStub(data)

        mock_esi.client.Universe.post_universe_ids.side_effect = my_endpoint
        names = [f"dummy_{num + 1001}" for num in range(600)]
        # when
        result = EveEntity.objects.fetch_by_names_esi(names)
        # then
        self.assertEqual(mock_esi.client.Universe.post_universe_ids.call_count, 2)
        self.assertEqual(len(result), 600)

    def test_should_fetch_unknown_entities_from_esi_only(self, mock_esi):
        # given
        mock_esi.client.Universe.post_universe_ids.return_value = BravadoOperationStub(
            {
                "characters": [
                    {"id": 9991, "name": "alpha"},
                    {"id": 9992, "name": "bravo"},
                ],
                "corporations": [
                    {"id": 9993, "name": "charlie"},
                ],
            }
        )
        create_eve_entity(
            id=1001, name="Bruce Wayne", category=EveEntity.CATEGORY_CHARACTER
        )
        # when
        result_qs = EveEntity.objects.fetch_by_names_esi(
            ["Bruce Wayne", "alpha", "bravo", "charlie"]
        )
        # then
        self.assertTrue(mock_esi.client.Universe.post_universe_ids.called)
        _, kwargs = mock_esi.client.Universe.post_universe_ids.call_args
        self.assertSetEqual(set(kwargs["names"]), {"alpha", "bravo", "charlie"})
        objs: Dict[int, EveEntity] = {obj.id: obj for obj in result_qs}
        self.assertSetEqual(set(objs.keys()), {1001, 9991, 9992, 9993})
        self.assertEqual(objs[1001].name, "Bruce Wayne")
        self.assertTrue(objs[1001].is_character)
        self.assertEqual(objs[9991].name, "alpha")
        self.assertTrue(objs[9991].is_character)
        self.assertEqual(objs[9992].name, "bravo")
        self.assertTrue(objs[9992].is_character)
        self.assertEqual(objs[9993].name, "charlie")
        self.assertTrue(objs[9993].is_corporation)

    def test_should_fetch_all_names_when_requested(self, mock_esi):
        # given
        mock_esi.client.Universe.post_universe_ids.return_value = BravadoOperationStub(
            {
                "characters": [
                    {"id": 9991, "name": "alpha"},
                    {"id": 1001, "name": "Bruce Wayne"},
                ],
            }
        )
        create_eve_entity(
            id=1001, name="Bruce Wayne", category=EveEntity.CATEGORY_FACTION
        )
        # when
        result_qs = EveEntity.objects.fetch_by_names_esi(
            ["Bruce Wayne", "alpha"], update=True
        )
        # then
        self.assertTrue(mock_esi.client.Universe.post_universe_ids.called)
        _, kwargs = mock_esi.client.Universe.post_universe_ids.call_args
        self.assertSetEqual(set(kwargs["names"]), {"Bruce Wayne", "alpha"})
        objs: Dict[int, EveEntity] = {obj.id: obj for obj in result_qs}
        self.assertSetEqual(set(objs.keys()), {1001, 9991})
        self.assertEqual(objs[1001].name, "Bruce Wayne")
        self.assertTrue(objs[1001].is_character)
        self.assertEqual(objs[9991].name, "alpha")
        self.assertTrue(objs[9991].is_character)


class TestEveEntityProfileUrl(NoSocketsTestCase):
    def test_should_handle_alliance(self):
        # given
        obj = create_eve_entity(
            id=3001, name="Wayne Enterprises", category=EveEntity.CATEGORY_ALLIANCE
        )
        # when/then
        self.assertEqual(
            obj.profile_url, "https://evemaps.dotlan.net/alliance/Wayne_Enterprises"
        )

    def test_should_handle_character(self):
        # given
        obj = create_eve_entity(
            id=1001, name="Bruce Wayne", category=EveEntity.CATEGORY_CHARACTER
        )
        # when/then
        self.assertEqual(obj.profile_url, "https://evewho.com/character/1001")

    def test_should_handle_corporation(self):
        # given
        obj = create_eve_entity(
            id=2001, name="Wayne Technologies", category=EveEntity.CATEGORY_CORPORATION
        )
        # when/then
        self.assertEqual(
            obj.profile_url, "https://evemaps.dotlan.net/corp/Wayne_Technologies"
        )

    def test_should_handle_faction(self):
        # given
        obj = create_eve_entity(
            id=99, name="Amarr Empire", category=EveEntity.CATEGORY_FACTION
        )
        # when/then
        self.assertEqual(
            obj.profile_url, "https://evemaps.dotlan.net/factionwarfare/Amarr_Empire"
        )

    def test_should_handle_inventory_type(self):
        # given
        obj = create_eve_entity(
            id=603, name="Merlin", category=EveEntity.CATEGORY_INVENTORY_TYPE
        )
        # when/then
        self.assertEqual(
            obj.profile_url, "https://www.kalkoken.org/apps/eveitems/?typeId=603"
        )

    def test_should_handle_solar_system(self):
        # given
        obj = create_eve_entity(
            id=30004984, name="Abune", category=EveEntity.CATEGORY_SOLAR_SYSTEM
        )
        # when/then
        self.assertEqual(obj.profile_url, "https://evemaps.dotlan.net/system/Abune")

    def test_should_handle_station(self):
        # given
        obj = create_eve_entity(
            id=60003760,
            name="Jita IV - Moon 4 - Caldari Navy Assembly Plant",
            category=EveEntity.CATEGORY_STATION,
        )
        # when/then
        self.assertEqual(
            obj.profile_url,
            "https://evemaps.dotlan.net/station/Jita_IV_-_Moon_4_-_Caldari_Navy_Assembly_Plant",
        )

    def test_should_return_empty_string_for_undefined_category(self):
        # given
        obj = create_eve_entity(
            id=99, name="Wayne Technologies", category=EveEntity.CATEGORY_CONSTELLATION
        )
        self.assertEqual(obj.profile_url, "")


@patch(MANAGERS_PATH + ".esi")
class TestEveEntityBulkResolveIds(NoSocketsTestCase):
    def test_should_resolve_and_create_new_objs(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()

        # when
        result = EveEntity.objects.bulk_resolve_ids(ids=[1001, 2001])
        self.assertEqual(result, 2)

        obj = EveEntity.objects.get(id=1001)
        self.assertEqual(obj.name, "Bruce Wayne")
        self.assertEqual(obj.category, EveEntity.CATEGORY_CHARACTER)

        obj = EveEntity.objects.get(id=2001)
        self.assertEqual(obj.name, "Wayne Technologies")
        self.assertEqual(obj.category, EveEntity.CATEGORY_CORPORATION)

    def test_should_return_zero_when_nothing_to_do(self, mock_esi):
        # when
        result = EveEntity.objects.bulk_resolve_ids(ids=[])
        # then
        self.assertEqual(result, 0)

    def test_should_create_only_non_existing_entities(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        create_eve_entity(
            id=1001, name="Bruce Wayne", category=EveEntity.CATEGORY_CHARACTER
        )

        # when
        result = EveEntity.objects.bulk_resolve_ids(ids=[1001, 2001])

        # then
        self.assertEqual(result, 1)

        obj = EveEntity.objects.get(id=1001)
        self.assertEqual(obj.name, "Bruce Wayne")
        self.assertEqual(obj.category, EveEntity.CATEGORY_CHARACTER)

        obj = EveEntity.objects.get(id=2001)
        self.assertEqual(obj.name, "Wayne Technologies")
        self.assertEqual(obj.category, EveEntity.CATEGORY_CORPORATION)

    def test_entities_without_name_will_be_refetched(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        create_eve_entity(id=1001, category=EveEntity.CATEGORY_CORPORATION)

        # when
        result = EveEntity.objects.bulk_resolve_ids(ids=[1001, 2001])

        # then
        self.assertEqual(result, 2)

        obj = EveEntity.objects.get(id=1001)
        self.assertEqual(obj.name, "Bruce Wayne")
        self.assertEqual(obj.category, EveEntity.CATEGORY_CHARACTER)

        obj = EveEntity.objects.get(id=2001)
        self.assertEqual(obj.name, "Wayne Technologies")
        self.assertEqual(obj.category, EveEntity.CATEGORY_CORPORATION)

    def test_should_resolve_existing_entity_without_name(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        create_eve_entity(id=1001)

        # when
        result = EveEntity.objects.bulk_resolve_ids(ids=[1001])

        # then
        self.assertEqual(result, 1)

        obj = EveEntity.objects.get(id=1001)
        self.assertEqual(obj.name, "Bruce Wayne")
        self.assertEqual(obj.category, EveEntity.CATEGORY_CHARACTER)

    def test_should_resolve_and_create_new_objs_with_old_api(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()

        # when
        result = EveEntity.objects.bulk_create_esi(ids=[1001, 2001])
        self.assertEqual(result, 2)

        obj = EveEntity.objects.get(id=1001)
        self.assertEqual(obj.name, "Bruce Wayne")
        self.assertEqual(obj.category, EveEntity.CATEGORY_CHARACTER)

        obj = EveEntity.objects.get(id=2001)
        self.assertEqual(obj.name, "Wayne Technologies")
        self.assertEqual(obj.category, EveEntity.CATEGORY_CORPORATION)


@patch(MANAGERS_PATH + ".esi")
class TestEveEntityUpdateFromEsiById(NoSocketsTestCase):
    def test_should_update_entity(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        obj = create_eve_entity(
            id=1001, name="Bruce Wayne", category=EveEntity.CATEGORY_CORPORATION
        )
        # when
        result = EveEntity.objects.update_from_esi_by_id(ids=[1001])
        # then
        self.assertEqual(result, 1)
        obj.refresh_from_db()
        self.assertEqual(obj.category, EveEntity.CATEGORY_CHARACTER)

    def test_should_return_0_when_no_id_given(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        result = EveEntity.objects.update_from_esi_by_id(ids=[])
        # then
        self.assertEqual(result, 0)

    def test_should_ignore_invalid_ids(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        result = EveEntity.objects.update_from_esi_by_id(ids=[1])
        # then
        self.assertEqual(result, 0)

    def test_should_handle_none(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        result = EveEntity.objects.update_from_esi_by_id(ids=None)
        # then
        self.assertEqual(result, 0)
