import datetime as dt
from unittest.mock import patch

from django.test import TestCase
from django.test.utils import override_settings
from django.utils.timezone import now

from eveuniverse.constants import EveCategoryId, EveGroupId
from eveuniverse.models import (
    EveCategory,
    EveConstellation,
    EveDogmaAttribute,
    EveEntity,
    EveGroup,
    EveRegion,
    EveSolarSystem,
    EveType,
)
from eveuniverse.tasks import (
    create_eve_entities,
    load_all_types,
    load_eve_object,
    load_eve_types,
    load_map,
    load_ship_types,
    load_structure_types,
    update_market_prices,
    update_or_create_eve_object,
    update_or_create_inline_object,
    update_stale_entities,
    update_unresolved_eve_entities,
)
from eveuniverse.utils import NoSocketsTestCase

from .testdata.esi import BravadoOperationStub, EsiClientStub
from .testdata.factories_2 import EveEntityFactory

TASKS_PATH = "eveuniverse.tasks"
MANAGERS_PATH = "eveuniverse.managers"


class TestTasks(NoSocketsTestCase):
    @patch(MANAGERS_PATH + ".universe.esi")
    def test_load_eve_object(self, mock_esi):
        mock_esi.client = EsiClientStub()

        load_eve_object(
            "EveRegion", 10000002, include_children=False, wait_for_children=False
        )

        self.assertTrue(EveRegion.objects.filter(id=10000002).exists())

    @patch(MANAGERS_PATH + ".universe.esi")
    def test_update_or_create_eve_object(self, mock_esi):
        mock_esi.client = EsiClientStub()
        obj, _ = EveRegion.objects.update_or_create_esi(id=10000002)
        obj.name = "Dummy"
        obj.save()

        update_or_create_eve_object(
            "EveRegion", 10000002, include_children=False, wait_for_children=False
        )

        obj.refresh_from_db()
        self.assertNotEqual(obj.name, "Dummy")

    @patch(MANAGERS_PATH + ".universe.esi")
    def test_update_or_create_inline_object(self, mock_esi):
        mock_esi.client = EsiClientStub()
        eve_type, _ = EveType.objects.update_or_create_esi(id=603)

        update_or_create_inline_object(
            parent_obj_id=eve_type.id,
            parent_fk="eve_type",
            eve_data_obj={"attribute_id": 588, "value": 5},
            other_pk_info={
                "esi_name": "attribute_id",
                "is_fk": True,
                "name": "eve_dogma_attribute",
            },
            parent2_model_name="EveDogmaAttribute",
            inline_model_name="EveTypeDogmaAttribute",
            parent_model_name=type(eve_type).__name__,
        )
        dogma_attribute_1 = eve_type.dogma_attributes.filter(
            eve_dogma_attribute=EveDogmaAttribute.objects.get(id=588)
        ).first()
        self.assertEqual(dogma_attribute_1.value, 5)

    @patch(MANAGERS_PATH + ".entities.esi")
    def test_create_eve_entities(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()

        # when
        create_eve_entities([1001, 2001])

        # then
        obj = EveEntity.objects.get(id=1001)
        self.assertEqual(obj.name, "Bruce Wayne")
        self.assertEqual(obj.category, EveEntity.CATEGORY_CHARACTER)

        obj = EveEntity.objects.get(id=2001)
        self.assertEqual(obj.name, "Wayne Technologies")
        self.assertEqual(obj.category, EveEntity.CATEGORY_CORPORATION)


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
@patch(MANAGERS_PATH + ".entities.esi")
class TestTasks2(TestCase):
    def test_update_unresolved_eve_entities(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        obj_1 = EveEntity.objects.create(id=1001)
        obj_2 = EveEntity.objects.create(id=1002)
        obj_3 = EveEntity.objects.create(id=2001)
        # when
        update_unresolved_eve_entities.delay()
        # then
        obj_1.refresh_from_db()
        self.assertEqual(obj_1.category, EveEntity.CATEGORY_CHARACTER)
        obj_2.refresh_from_db()
        self.assertEqual(obj_2.category, EveEntity.CATEGORY_CHARACTER)
        obj_3.refresh_from_db()
        self.assertEqual(obj_3.category, EveEntity.CATEGORY_CORPORATION)


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
@patch(TASKS_PATH + ".esi")
@patch(MANAGERS_PATH + ".universe.esi")
class TestLoadData(TestCase):
    def test_load_map(self, mock_esi_1, mock_esi_2):
        mock_esi_1.client = EsiClientStub()
        mock_esi_2.client = EsiClientStub()
        load_map()

        for id in [10000002, 10000014, 10000069, 11000031]:
            self.assertTrue(EveRegion.objects.filter(id=id).exists())

        for id in [20000169, 20000785, 21000324]:
            self.assertTrue(EveConstellation.objects.filter(id=id).exists())

        for id in [30001161, 30045339, 31000005]:
            self.assertTrue(EveSolarSystem.objects.filter(id=id).exists())

    def test_load_ship_types(self, mock_esi_1, mock_esi_2):
        mock_esi_1.client = EsiClientStub()
        mock_esi_2.client = EsiClientStub()
        load_ship_types()

        self.assertTrue(EveCategory.objects.filter(id=6).exists())
        for id in [25, 26]:
            self.assertTrue(EveGroup.objects.filter(id=id).exists())

        for id in [603, 608, 621, 626]:
            self.assertTrue(EveType.objects.filter(id=id).exists())

    def test_load_structure_types(self, mock_esi_1, mock_esi_2):
        mock_esi_1.client = EsiClientStub()
        mock_esi_2.client = EsiClientStub()
        load_structure_types()

        self.assertTrue(EveCategory.objects.filter(id=65).exists())
        for id in [1404]:
            self.assertTrue(EveGroup.objects.filter(id=id).exists())

        for id in [35825]:
            self.assertTrue(EveType.objects.filter(id=id).exists())


@patch(TASKS_PATH + ".update_or_create_eve_object")
@patch(TASKS_PATH + ".esi")
class TestLoadAllTypes(NoSocketsTestCase):
    def test_should_load_all_types(self, mock_esi, mock_update_or_create_eve_object):
        # given
        mock_esi.client.Universe.get_universe_categories.return_value = (
            BravadoOperationStub([1, 2])
        )
        # when
        load_all_types()
        # then
        self.assertEqual(mock_update_or_create_eve_object.delay.call_count, 2)

    def test_should_abort_when_esi_returns_no_data(
        self, mock_esi, mock_update_or_create_eve_object
    ):
        # given
        mock_esi.client.Universe.get_universe_categories.return_value = (
            BravadoOperationStub(None)
        )
        # when/then
        with self.assertRaises(ValueError):
            load_all_types()

    def test_should_load_all_types_with_enabled_sections(
        self, mock_esi, mock_update_or_create_eve_object
    ):
        # given
        mock_esi.client.Universe.get_universe_categories.return_value = (
            BravadoOperationStub([1])
        )
        # when
        load_all_types(["alpha", "bravo"])
        # then
        _, kwargs = mock_update_or_create_eve_object.delay.call_args
        self.assertEqual(kwargs["enabled_sections"], ["alpha", "bravo"])


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
@patch(TASKS_PATH + ".esi")
@patch(MANAGERS_PATH + ".universe.esi")
class TestLoadEveTypes(TestCase):
    def test_should_load_all_types(self, mock_esi_1, mock_esi_2):
        # given
        mock_esi_1.client = EsiClientStub()
        mock_esi_2.client = EsiClientStub()
        category_ids = [EveCategoryId.STRUCTURE.value]
        group_ids = [EveGroupId.PLANET.value]
        type_ids = [603]
        # when
        load_eve_types.delay(
            category_ids=category_ids, group_ids=group_ids, type_ids=type_ids
        )
        # then
        self.assertTrue(EveCategory.objects.filter(id=EveCategoryId.STRUCTURE).exists())
        self.assertTrue(EveGroup.objects.filter(id=EveGroupId.PLANET).exists())
        self.assertTrue(EveType.objects.filter(id=603).exists())


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
@patch(TASKS_PATH + ".EveMarketPrice.objects.update_objs_from_esi_data", spec=True)
@patch(TASKS_PATH + ".EveMarketPrice.objects.fetch_data_from_esi", spec=True)
class TestUpdateMarketPrices(TestCase):
    def test_should_update_market_prices_when_there_is_data(
        self, mock_fetch, mock_update
    ):
        # given
        mock_fetch.return_value = [1]
        # when
        update_market_prices.delay()
        # then
        self.assertTrue(mock_fetch.called)
        self.assertTrue(mock_update.called)

    def test_should_not_update_market_prices_when_no_data(
        self, mock_fetch, mock_update
    ):
        # given
        mock_fetch.return_value = []
        # when
        update_market_prices.delay()
        # then
        self.assertTrue(mock_fetch.called)
        self.assertFalse(mock_update.called)


@patch(TASKS_PATH + ".is_esi_online")
@patch(TASKS_PATH + ".EveEntity.objects.update_from_esi_by_id")
@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
class TestUpdateStaleEntities(TestCase):
    def test_should_update_stale_names_only(
        self, mock_update_from_esi_by_id, mock_is_online
    ):
        def update_entity(ids: list) -> int:
            EveEntity.objects.filter(id__in=list(ids)).update(name="updated")
            return len(ids)

        # given
        mock_is_online.return_value = True
        mock_update_from_esi_by_id.side_effect = update_entity
        my_now = now()
        with patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = my_now - dt.timedelta(hours=10)
            e1 = EveEntityFactory(category=EveEntity.CATEGORY_CHARACTER)
            e2 = EveEntityFactory(category=EveEntity.CATEGORY_INVENTORY_TYPE)
            mock_now.return_value = my_now
            e3 = EveEntityFactory(category=EveEntity.CATEGORY_CHARACTER)
            # when
            got = update_stale_entities(expiration_time=1800)

        # then
        self.assertEqual(got, 1)
        e1.refresh_from_db()
        self.assertEqual(e1.name, "updated")
        e2.refresh_from_db()
        self.assertNotEqual(e2.name, "updated")
        e3.refresh_from_db()
        self.assertNotEqual(e3.name, "updated")

    def test_should_abort_when_esi_is_offline(
        self, mock_update_from_esi_by_id, mock_is_online
    ):
        # given
        mock_is_online.return_value = False
        with self.assertRaises(RuntimeError):
            update_stale_entities(expiration_time=1800)

    def test_should_do_nothing_when_no_stales_found(
        self, mock_update_from_esi_by_id, mock_is_online
    ):
        # given
        mock_is_online.return_value = True
        mock_update_from_esi_by_id.side_effect = ValueError
        e1 = EveEntityFactory(category=EveEntity.CATEGORY_CHARACTER)
        # when
        got = update_stale_entities(expiration_time=1800)
        # then
        self.assertEqual(got, 0)
        e1.refresh_from_db()
        self.assertNotEqual(e1.name, "updated")
