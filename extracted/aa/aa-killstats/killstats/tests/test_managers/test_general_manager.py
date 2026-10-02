"""Unit tests for EveEntityManager in killstats.managers.general_manager."""

# Standard Library
from http import HTTPStatus

# Third Party
import pook

# AA Killstats
from killstats.errors import ObjectNotFound
from killstats.models.general import EveEntity
from killstats.tests import AuthTestCase
from killstats.tests.testdata.killstats import EveEntityFactory


class TestGeneralManager(AuthTestCase):
    def setUp(self):
        super().setUp()
        self.manager = EveEntity.objects

    @pook.on
    def test_get_or_create_esi_should_return_existing_entity_without_esi_call(
        self,
    ):
        # Test Data
        existing = EveEntityFactory(
            id=1001, name="Existing Pilot", category="character"
        )

        # Test Action
        entity, created = self.manager.get_or_create_esi(eve_id=1001)

        # Expected Result
        self.assertEqual(entity, existing)
        self.assertFalse(created)

    @pook.on
    def test_get_or_create_esi_should_fetch_from_esi_when_not_exists(self):
        # Test Data
        pook.post(
            "https://esi.evetech.net/universe/names",
            reply=HTTPStatus.OK,
            response_json=[{"id": 99001, "name": "New Pilot", "category": "character"}],
        )

        # Test Action
        entity, created = self.manager.get_or_create_esi(eve_id=99001)

        # Expected Result
        self.assertTrue(created)
        self.assertEqual(entity.id, 99001)
        self.assertEqual(entity.name, "New Pilot")
        self.assertEqual(entity.category, "character")

    @pook.on
    def test_update_or_create_esi_should_raise_object_not_found_when_empty_response(
        self,
    ):
        # Test Data
        pook.post(
            "https://esi.evetech.net/universe/names",
            reply=HTTPStatus.OK,
            response_json=[],
        )

        # Test Action & Expected Result
        with self.assertRaises(ObjectNotFound):
            self.manager.update_or_create_esi(eve_id=999999)

    @pook.on
    def test_create_bulk_from_esi_should_create_entities_in_bulk(self):
        # Test Data
        pook.post(
            "https://esi.evetech.net/universe/names",
            reply=HTTPStatus.OK,
            response_json=[
                {"id": 99002, "name": "Corp One", "category": "corporation"},
                {"id": 99003, "name": "Alliance One", "category": "alliance"},
            ],
        )

        # Test Action
        result = self.manager.create_bulk_from_esi([99002, 99003])

        # Expected Result
        self.assertTrue(result)
        self.assertTrue(EveEntity.objects.filter(id=99002, name="Corp One").exists())
        self.assertTrue(
            EveEntity.objects.filter(id=99003, name="Alliance One").exists()
        )

    @pook.on
    def test_create_bulk_from_esi_should_return_true_for_empty_list_without_esi_call(
        self,
    ):
        # Test Action
        result = self.manager.create_bulk_from_esi([])

        # Expected Result
        self.assertTrue(result)
