import datetime as dt
from unittest.mock import patch

import pook
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.timezone import now

from eveuniverse import tasks
from eveuniverse.models import (
    EveDogmaAttribute,
    EveEntity,
    EveRegion,
    EveSolarSystem,
    EveType,
)
from eveuniverse.tests.helpers import TestCaseWithClearCache
from eveuniverse.tests.testdata.factories_2 import (
    EveEntityFactory,
    EveEntityUnresolvedFactory,
    EveRegionFactory,
    EveTypeFactory,
    PositionFactory,
    make_esi_url,
)

TASKS_PATH = "eveuniverse.tasks"


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
class TestTasks(TestCaseWithClearCache):
    @pook.on
    def test_should_load_eve_object_from_scratch(self):
        # given
        region_id = 10000069
        pook.get(
            make_esi_url(f"universe/regions/{region_id}"),
            reply=200,
            response_json={
                "constellations": [20000785],
                "description": "description",
                "name": "Black Rise",
                "region_id": region_id,
            },
        )

        # when
        tasks.load_eve_object(
            "EveRegion", region_id, include_children=False, wait_for_children=False
        )

        # then
        self.assertTrue(EveRegion.objects.filter(id=region_id).exists())

    @pook.on
    def test_should_update_existing_object(self):
        # given
        obj = EveRegionFactory()
        pook.get(
            make_esi_url(f"universe/regions/{obj.id}"),
            reply=200,
            response_json={
                "constellations": [666],
                "description": "description",
                "name": "Alpha",
                "region_id": obj.id,
            },
        )

        # when
        tasks.update_or_create_eve_object(
            "EveRegion", obj.id, include_children=False, wait_for_children=False
        )

        # then
        obj.refresh_from_db()
        self.assertEqual(obj.name, "Alpha")

    @pook.on
    def test_update_or_create_inline_object(self):
        # given
        eve_type = EveTypeFactory()
        attribute_id = 271
        pook.get(
            make_esi_url(f"dogma/attributes/{attribute_id}"),
            reply=200,
            response_json={
                "attribute_id": attribute_id,
                "default_value": 1,
                "description": "Multiplies EM damage taken by shield",
                "display_name": "Shield EM Damage Resistance",
                "icon_id": 1396,
                "name": "shieldEmDamageResonance",
                "published": True,
                "unit_id": 108,
            },
        )

        # when
        tasks.update_or_create_inline_object(
            parent_obj_id=eve_type.id,
            parent_fk="eve_type",
            eve_data_obj={"attribute_id": attribute_id, "value": 5},
            other_pk_info={
                "esi_name": "attribute_id",
                "is_fk": True,
                "name": "eve_dogma_attribute",
            },
            parent2_model_name="EveDogmaAttribute",
            inline_model_name="EveTypeDogmaAttribute",
            parent_model_name=type(eve_type).__name__,
        )

        # then
        dogma_attribute_1 = eve_type.dogma_attributes.filter(
            eve_dogma_attribute=EveDogmaAttribute.objects.get(id=attribute_id)
        ).first()
        self.assertEqual(dogma_attribute_1.value, 5)

    @pook.on
    def test_create_eve_entities(self):
        # given
        entity_id = 1001
        name = "Alpha"
        category = EveEntity.CATEGORY_CHARACTER
        pook.post(
            make_esi_url("universe/names"),
            reply=200,
            response_json=[
                {"category": category, "id": entity_id, "name": name},
            ],
        )

        # when
        tasks.create_eve_entities([entity_id])

        # then
        obj = EveEntity.objects.get(id=entity_id)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.category, category)

    @pook.on
    def test_update_unresolved_eve_entities(self):
        # given
        obj = EveEntityUnresolvedFactory()
        name = "Alpha"
        category = EveEntity.CATEGORY_CHARACTER
        pook.post(
            make_esi_url("universe/names"),
            reply=200,
            response_json=[
                {"category": category, "id": obj.id, "name": name},
            ],
        )

        # when
        tasks.update_unresolved_eve_entities.delay()

        # then
        obj.refresh_from_db()
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.category, category)


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
class TestLoadData(TestCaseWithClearCache):
    @pook.on
    def test_load_map(self):
        # given
        constellation_id = 20000785
        region_id = 10000069
        solar_system_id = 30045339
        solar_system_name = "Alpha"
        pook.get(
            make_esi_url("universe/regions"),
            reply=200,
            response_json=[region_id],
        )
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
                "name": solar_system_name,
                "planets": [],
                "position": PositionFactory(),
                "security_status": 0.3,
                "star_id": 42,
                "system_id": solar_system_id,
            },
        )

        # when
        tasks.load_map()

        # then
        obj = EveSolarSystem.objects.get(id=solar_system_id)
        self.assertEqual(obj.name, solar_system_name)

    @pook.on
    def test_load_ship_types(self):
        # given
        category_id = 6
        category_name = "Ship"
        group_id = 25
        group_name = "Frigate"
        type_id = 603
        type_name = "Merlin"
        pook.get(
            make_esi_url(f"universe/categories/{category_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "groups": [group_id],
                "name": category_name,
                "published": True,
            },
        )
        pook.get(
            make_esi_url(f"universe/groups/{group_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "group_id": group_id,
                "name": group_name,
                "published": True,
                "types": [type_id],
            },
        )
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [],
                "dogma_effects": [],
                "graphic_id": 42,
                "group_id": group_id,
                "market_group_id": 666,
                "mass": 997000,
                "name": type_name,
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": type_id,
                "volume": 16500,
            },
        )

        # when
        tasks.load_ship_types()

        # then
        obj = EveType.objects.get(id=type_id)
        self.assertEqual(obj.name, type_name)

    @pook.on
    def test_load_structure_types(self):
        # given
        category_id = 65
        category_name = "Structure"
        group_id = 1406
        group_name = "Refinery"
        type_id = 35835
        type_name = "Athanor"
        pook.get(
            make_esi_url(f"universe/categories/{category_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "groups": [group_id],
                "name": category_name,
                "published": True,
            },
        )
        pook.get(
            make_esi_url(f"universe/groups/{group_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "group_id": group_id,
                "name": group_name,
                "published": True,
                "types": [type_id],
            },
        )
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [],
                "dogma_effects": [],
                "graphic_id": 42,
                "group_id": group_id,
                "market_group_id": 666,
                "mass": 997000,
                "name": type_name,
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": type_id,
                "volume": 16500,
            },
        )

        # when
        tasks.load_structure_types()

        # then
        obj = EveType.objects.get(id=type_id)
        self.assertEqual(obj.name, type_name)

    @pook.on
    def test_should_load_all_types_categoryIDs(self):
        # given
        category_id = 65
        category_name = "Structure"
        group_id = 1406
        group_name = "Refinery"
        type_id = 35835
        type_name = "Athanor"
        pook.get(
            make_esi_url(f"universe/categories/{category_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "groups": [group_id],
                "name": category_name,
                "published": True,
            },
        )
        pook.get(
            make_esi_url(f"universe/groups/{group_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "group_id": group_id,
                "name": group_name,
                "published": True,
                "types": [type_id],
            },
        )
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [],
                "dogma_effects": [],
                "graphic_id": 42,
                "group_id": group_id,
                "market_group_id": 666,
                "mass": 997000,
                "name": type_name,
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": type_id,
                "volume": 16500,
            },
        )

        # when
        tasks.load_eve_types.delay(category_ids=[category_id])

        # then
        self.assertTrue(EveType.objects.filter(id=type_id).exists())

    @pook.on
    def test_should_load_all_types_groupIDs(self):
        # given
        category_id = 65
        category_name = "Structure"
        group_id = 1406
        group_name = "Refinery"
        type_id = 35835
        type_name = "Athanor"
        pook.get(
            make_esi_url(f"universe/categories/{category_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "groups": [group_id],
                "name": category_name,
                "published": True,
            },
        )
        pook.get(
            make_esi_url(f"universe/groups/{group_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "group_id": group_id,
                "name": group_name,
                "published": True,
                "types": [type_id],
            },
        )
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [],
                "dogma_effects": [],
                "graphic_id": 42,
                "group_id": group_id,
                "market_group_id": 666,
                "mass": 997000,
                "name": type_name,
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": type_id,
                "volume": 16500,
            },
        )

        # when
        tasks.load_eve_types.delay(group_ids=[group_id])

        # then
        self.assertTrue(EveType.objects.filter(id=type_id).exists())

    @pook.on
    def test_should_load_all_types_typeIDs(self):
        # given
        category_id = 65
        category_name = "Structure"
        group_id = 1406
        group_name = "Refinery"
        type_id = 35835
        type_name = "Athanor"
        pook.get(
            make_esi_url(f"universe/categories/{category_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "groups": [group_id],
                "name": category_name,
                "published": True,
            },
        )
        pook.get(
            make_esi_url(f"universe/groups/{group_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "group_id": group_id,
                "name": group_name,
                "published": True,
                "types": [type_id],
            },
        )
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [],
                "dogma_effects": [],
                "graphic_id": 42,
                "group_id": group_id,
                "market_group_id": 666,
                "mass": 997000,
                "name": type_name,
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": type_id,
                "volume": 16500,
            },
        )

        # when
        tasks.load_eve_types.delay(type_ids=[type_id])

        # then
        self.assertTrue(EveType.objects.filter(id=type_id).exists())


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
class TestLoadAllTypes(TestCaseWithClearCache):
    @pook.on
    def test_should_load_all_types(self):
        # given
        category_id = 65
        category_name = "Structure"
        group_id = 1406
        group_name = "Refinery"
        type_id = 35835
        type_name = "Athanor"
        pook.get(
            make_esi_url("universe/categories"),
            reply=200,
            response_json=[category_id],
        )
        pook.get(
            make_esi_url(f"universe/categories/{category_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "groups": [group_id],
                "name": category_name,
                "published": True,
            },
        )
        pook.get(
            make_esi_url(f"universe/groups/{group_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "group_id": group_id,
                "name": group_name,
                "published": True,
                "types": [type_id],
            },
        )
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [],
                "dogma_effects": [],
                "graphic_id": 42,
                "group_id": group_id,
                "market_group_id": 666,
                "mass": 997000,
                "name": type_name,
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": type_id,
                "volume": 16500,
            },
        )

        # when
        tasks.load_all_types()

        # then
        self.assertTrue(EveType.objects.filter(id=type_id).exists())

    @pook.on
    def test_should_load_all_types_with_enabled_sections(self):
        # given
        category_id = 65
        category_name = "Structure"
        group_id = 1406
        group_name = "Refinery"
        type_id = 35835
        type_name = "Athanor"
        graphic_id = 314
        pook.get(
            make_esi_url("universe/categories"),
            reply=200,
            response_json=[category_id],
        )
        pook.get(
            make_esi_url(f"universe/categories/{category_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "groups": [group_id],
                "name": category_name,
                "published": True,
            },
        )
        pook.get(
            make_esi_url(f"universe/groups/{group_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "group_id": group_id,
                "name": group_name,
                "published": True,
                "types": [type_id],
            },
        )
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [],
                "dogma_effects": [],
                "graphic_id": graphic_id,
                "group_id": group_id,
                "market_group_id": 666,
                "mass": 997000,
                "name": type_name,
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": type_id,
                "volume": 16500,
            },
        )
        pook.get(
            make_esi_url(f"universe/graphics/{graphic_id}"),
            reply=200,
            response_json={
                "graphic_id": 314,
                "sof_dna": "cf7_t1:caldaribase:caldari",
                "sof_fation_name": "caldaribase",
                "sof_hull_name": "cf7_t1",
                "sof_race_name": "caldari",
            },
        )

        # when
        tasks.load_all_types(["graphics"])

        # then
        obj = EveType.objects.get(id=type_id)
        self.assertEqual(obj.eve_graphic.id, graphic_id)

    @pook.on
    def test_should_abort_when_esi_returns_no_categories(self):
        # given
        pook.get(
            make_esi_url("universe/categories"),
            reply=200,
            response_json=[],
        )

        # when/then
        with self.assertRaises(ValueError):
            tasks.load_all_types()


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
        tasks.update_market_prices.delay()
        # then
        self.assertTrue(mock_fetch.called)
        self.assertTrue(mock_update.called)

    def test_should_not_update_market_prices_when_no_data(
        self, mock_fetch, mock_update
    ):
        # given
        mock_fetch.return_value = []
        # when
        tasks.update_market_prices.delay()
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
            got = tasks.update_stale_entities(expiration_time=1800)

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
            tasks.update_stale_entities(expiration_time=1800)

    def test_should_do_nothing_when_no_stales_found(
        self, mock_update_from_esi_by_id, mock_is_online
    ):
        # given
        mock_is_online.return_value = True
        mock_update_from_esi_by_id.side_effect = ValueError
        e1 = EveEntityFactory(category=EveEntity.CATEGORY_CHARACTER)
        # when
        got = tasks.update_stale_entities(expiration_time=1800)
        # then
        self.assertEqual(got, 0)
        e1.refresh_from_db()
        self.assertNotEqual(e1.name, "updated")
        self.assertNotEqual(e1.name, "updated")
        # then
        self.assertEqual(got, 0)
        e1.refresh_from_db()
        self.assertNotEqual(e1.name, "updated")
        self.assertNotEqual(e1.name, "updated")
