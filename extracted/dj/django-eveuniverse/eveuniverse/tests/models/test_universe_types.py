import datetime as dt
from typing import NamedTuple
from unittest.mock import Mock, patch

import pook
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.timezone import now

from eveuniverse.constants import EveCategoryId
from eveuniverse.models import (
    EveCategory,
    EveDogmaAttribute,
    EveDogmaEffect,
    EveEntity,
    EveGraphic,
    EveGroup,
    EveMarketGroup,
    EveMarketPrice,
    EveType,
    EveTypeDogmaAttribute,
    EveTypeDogmaEffect,
    EveUnit,
)
from eveuniverse.tests.helpers import TestCaseWithClearCache
from eveuniverse.tests.testdata.factories_2 import (
    BlueprintTypeFactory,
    EveCategoryFactory,
    EveDogmaAttributeFactory,
    EveDogmaEffectFactory,
    EveGraphicFactory,
    EveGroupFactory,
    EveMarketGroupFactory,
    EveMarketPriceFactory,
    EveTypeFactory,
    SKINTypeFactory,
    make_esi_url,
)

MODELS_PATH = "eveuniverse.models"


class TestEveCategory(TestCaseWithClearCache):

    @pook.on
    def test_should_create_object_from_esi(self):
        # given
        category_id = 6
        pook.get(
            make_esi_url(f"universe/categories/{category_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "groups": [25, 26],
                "name": "Ship",
                "published": True,
            },
        )

        # when
        obj: EveCategory
        obj, created = EveCategory.objects.get_or_create_esi(id=category_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, category_id)
        self.assertEqual(obj.name, "Ship")
        self.assertTrue(obj.published)
        self.assertEqual(obj.eve_entity_category(), "")


@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", True)
class TestEveDogmaAttribute(TestCaseWithClearCache):

    @pook.on
    def test_can_create_from_esi(self):
        # given
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
        obj: EveDogmaAttribute
        obj, created = EveDogmaAttribute.objects.update_or_create_esi(id=attribute_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, attribute_id)
        self.assertEqual(obj.name, "shieldEmDamageResonance")
        self.assertEqual(obj.default_value, 1)
        self.assertEqual(obj.description, "Multiplies EM damage taken by shield")
        self.assertEqual(obj.display_name, "Shield EM Damage Resistance")
        self.assertEqual(obj.icon_id, 1396)
        self.assertTrue(obj.published)
        self.assertEqual(obj.eve_unit.id, 108)


@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", True)
class TestEveDogmaEffect(TestCaseWithClearCache):

    @pook.on
    def test_can_create_from_esi(self):
        # given
        attribute_1_id = 271
        attribute_2_id = 463
        effect_id = 1816
        pook.get(
            make_esi_url(f"dogma/attributes/{attribute_1_id}"),
            reply=200,
            response_json={
                "attribute_id": attribute_1_id,
                "default_value": 1,
                "description": "Multiplies EM damage taken by shield",
                "display_name": "Shield EM Damage Resistance",
                "icon_id": 1396,
                "name": "shieldEmDamageResonance",
                "published": True,
                "unit_id": 108,
            },
        )
        pook.get(
            make_esi_url(f"dogma/attributes/{attribute_2_id}"),
            reply=200,
            response_json={
                "attribute_id": attribute_2_id,
                "default_value": 0,
                "description": "",
                "display_name": "",
                "high_is_good": True,
                "icon_id": 0,
                "name": "shipBonusCF",
                "stackable": True,
            },
        )
        pook.get(
            make_esi_url(f"dogma/effects/{effect_id}"),
            reply=200,
            response_json={
                "description": "",
                "display_name": "",
                "effect_category": 0,
                "effect_id": effect_id,
                "icon_id": 0,
                "modifiers": [
                    {
                        "domain": "shipID",
                        "func": "ItemModifier",
                        "modified_attribute_id": attribute_1_id,
                        "modifying_attribute_id": attribute_2_id,
                        "operator": 6,
                    }
                ],
                "name": "shipShieldEMResistanceCF2",
            },
        )

        # when
        obj: EveDogmaEffect
        obj, created = EveDogmaEffect.objects.update_or_create_esi(id=effect_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, effect_id)
        self.assertEqual(obj.name, "shipShieldEMResistanceCF2")
        self.assertEqual(obj.display_name, "")
        self.assertEqual(obj.effect_category, 0)
        self.assertEqual(obj.icon_id, 0)
        modifiers = obj.modifiers.first()
        self.assertEqual(modifiers.domain, "shipID")
        self.assertEqual(modifiers.func, "ItemModifier")
        self.assertEqual(
            modifiers.modified_attribute,
            EveDogmaAttribute.objects.get(id=attribute_1_id),
        )
        self.assertEqual(
            modifiers.modifying_attribute,
            EveDogmaAttribute.objects.get(id=463),
        )
        self.assertEqual(modifiers.operator, 6)


class TestEveGraphic(TestCaseWithClearCache):

    @pook.on
    def test_create_from_esi(self):
        # given
        id = 314
        pook.get(
            make_esi_url(f"universe/graphics/{id}"),
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
        obj: EveGraphic
        obj, created = EveGraphic.objects.get_or_create_esi(id=id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, id)
        self.assertEqual(obj.sof_dna, "cf7_t1:caldaribase:caldari")
        self.assertEqual(obj.sof_fation_name, "caldaribase")
        self.assertEqual(obj.sof_hull_name, "cf7_t1")
        self.assertEqual(obj.sof_race_name, "caldari")


class TestEveGroup(TestCaseWithClearCache):

    @pook.on
    def test_can_create_from_esi(self):
        # given
        category_id = 6
        EveCategoryFactory(id=category_id)
        group_id = 25
        group_name = "Frigate"
        pook.get(
            make_esi_url(f"universe/groups/{group_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "group_id": group_id,
                "name": group_name,
                "published": True,
                "types": [603],
            },
        )

        # when
        obj: EveGroup
        obj, created = EveGroup.objects.get_or_create_esi(id=group_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, group_id)
        self.assertEqual(obj.name, group_name)
        self.assertTrue(obj.published)


class TestEveMarketGroup(TestCaseWithClearCache):

    @pook.on
    def test_can_fetch_group(self):
        # given
        id = 4
        name = "Ships"
        description = "Capsuleer spaceships of all sizes and roles, ..."
        pook.get(
            make_esi_url(f"markets/groups/{id}"),
            reply=200,
            response_json={
                "description": description,
                "market_group_id": id,
                "name": name,
                "types": [],
            },
        )

        # when
        obj: EveMarketGroup
        obj, created = EveMarketGroup.objects.get_or_create_esi(id=id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, id)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.description, description)


class TestEveMarketPriceManager(TestCaseWithClearCache):

    @pook.on
    def test_add_new_prices_from_esi_but_for_existing_types_only(self):
        # given
        et = EveTypeFactory()
        adjusted_price = 306988.09
        average_price = 306292.67
        pook.get(
            make_esi_url("markets/prices"),
            reply=200,
            response_json=[
                {
                    "adjusted_price": adjusted_price,
                    "average_price": average_price,
                    "type_id": et.id,
                },
                {
                    "adjusted_price": 123.45,
                    "average_price": 678.90,
                    "type_id": 420,
                },
            ],
        )

        # when
        result = EveMarketPrice.objects.update_from_esi()

        # then
        self.assertEqual(result, 1)
        self.assertEqual(EveMarketPrice.objects.count(), 1)
        et.refresh_from_db()
        self.assertEqual(float(et.market_price.adjusted_price), adjusted_price)
        self.assertEqual(float(et.market_price.average_price), average_price)

    @pook.on
    def test_should_not_update_prices_which_are_not_stale_1(self):
        # given
        et = EveTypeFactory()
        mp = EveMarketPriceFactory(eve_type=et)
        pook.get(
            make_esi_url("markets/prices"),
            reply=200,
            response_json=[
                {
                    "adjusted_price": 12,
                    "average_price": 42,
                    "type_id": et.id,
                }
            ],
        )

        # when
        result = EveMarketPrice.objects.update_from_esi()

        # then
        self.assertEqual(result, 0)
        et.refresh_from_db()
        self.assertEqual(float(et.market_price.adjusted_price), mp.adjusted_price)
        self.assertEqual(float(et.market_price.average_price), mp.average_price)

    @pook.on
    def test_should_update_stale_prices(self):
        # given
        et = EveTypeFactory()
        mocked_update_at = now() - dt.timedelta(minutes=65)
        with patch("django.utils.timezone.now", Mock(return_value=mocked_update_at)):
            EveMarketPriceFactory(eve_type=et)

        adjusted_price = 306988.09
        average_price = 306292.67
        pook.get(
            make_esi_url("markets/prices"),
            reply=200,
            response_json=[
                {
                    "adjusted_price": adjusted_price,
                    "average_price": average_price,
                    "type_id": et.id,
                },
                {"adjusted_price": 123.45, "average_price": 678.90, "type_id": 420},
            ],
        )

        # when
        result = EveMarketPrice.objects.update_from_esi(minutes_until_stale=60)

        # then
        self.assertEqual(result, 1)
        et.refresh_from_db()
        self.assertEqual(float(et.market_price.adjusted_price), adjusted_price)
        self.assertEqual(float(et.market_price.average_price), average_price)

    @pook.on
    def test_should_remove_obsolete_prices(self):
        # given
        et_1 = EveTypeFactory()
        mp_1 = EveMarketPriceFactory(eve_type=et_1)
        et_2 = EveTypeFactory()
        EveMarketPriceFactory(eve_type=et_2)
        pook.get(
            make_esi_url("markets/prices"),
            reply=200,
            response_json=[
                {
                    "adjusted_price": 12,
                    "average_price": 42,
                    "type_id": et_1.id,
                }
            ],
        )

        # when
        result = EveMarketPrice.objects.update_from_esi()

        # then
        self.assertEqual(result, 0)
        self.assertEqual(EveMarketPrice.objects.count(), 1)
        et_1.refresh_from_db()
        self.assertEqual(float(et_1.market_price.adjusted_price), mp_1.adjusted_price)
        self.assertEqual(float(et_1.market_price.average_price), mp_1.average_price)


class TestEveType_Basics(TestCase):
    def test_should_return_value_as_str(self):
        self.assertEqual(str(EveType.Section.DOGMAS), "dogmas")

    def test_should_return_values(self):
        self.assertSetEqual(
            set(EveType.Section),
            {
                "dogmas",
                "graphics",
                "market_groups",
                "type_materials",
                "industry_activities",
            },
        )


class TestEveType_ESI(TestCaseWithClearCache):

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @pook.on
    def test_can_create_type_from_esi_without_sections(self):
        # given
        capacity = 150
        description = "The Merlin is the most powerful combat frigate of ..."
        graphic = EveGraphicFactory()
        eg = EveGroupFactory()
        mass = 997000
        mg = EveMarketGroupFactory()
        name = "Merlin"
        packaged_volume = 2500
        portion_size = 1
        radius = 39
        type_id = 603
        volume = 16500
        da = EveDogmaAttributeFactory()
        de = EveDogmaEffectFactory()
        da_value = 5
        de_is_default = True
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": capacity,
                "description": description,
                "dogma_attributes": [
                    {"attribute_id": da.id, "value": da_value},
                ],
                "dogma_effects": [
                    {"effect_id": de.id, "is_default": de_is_default},
                ],
                "graphic_id": graphic.id,
                "group_id": eg.id,
                "market_group_id": mg.id,
                "mass": mass,
                "name": name,
                "packaged_volume": packaged_volume,
                "portion_size": portion_size,
                "published": True,
                "radius": radius,
                "type_id": type_id,
                "volume": volume,
            },
        )

        # when
        obj: EveType
        obj, created = EveType.objects.get_or_create_esi(id=type_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.capacity, capacity)
        self.assertEqual(obj.description, description)
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_INVENTORY_TYPE)
        self.assertEqual(obj.eve_group, eg)
        self.assertEqual(obj.id, type_id)
        self.assertEqual(obj.mass, mass)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.packaged_volume, packaged_volume)
        self.assertEqual(obj.portion_size, portion_size)
        self.assertEqual(obj.radius, radius)
        self.assertEqual(obj.volume, volume)
        self.assertFalse(obj.dogma_attributes.exists())
        self.assertFalse(obj.dogma_effects.exists())
        self.assertIsNone(obj.eve_graphic)
        self.assertIsNone(obj.eve_market_group)
        self.assertTrue(obj.published)

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", True)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", True)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", True)
    @pook.on
    def test_can_create_type_from_esi_with_all_sections(self):
        # given
        capacity = 150
        description = "The Merlin is the most powerful combat frigate of ..."
        graphic = EveGraphicFactory()
        eg = EveGroupFactory()
        mass = 997000
        mg = EveMarketGroupFactory()
        name = "Merlin"
        packaged_volume = 2500
        portion_size = 1
        radius = 39
        type_id = 603
        volume = 16500
        da = EveDogmaAttributeFactory()
        de = EveDogmaEffectFactory()
        da_value = 5
        de_is_default = True
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": capacity,
                "description": description,
                "dogma_attributes": [
                    {"attribute_id": da.id, "value": da_value},
                ],
                "dogma_effects": [
                    {"effect_id": de.id, "is_default": de_is_default},
                ],
                "graphic_id": graphic.id,
                "group_id": eg.id,
                "market_group_id": mg.id,
                "mass": mass,
                "name": name,
                "packaged_volume": packaged_volume,
                "portion_size": portion_size,
                "published": True,
                "radius": radius,
                "type_id": type_id,
                "volume": volume,
            },
        )

        # when
        obj: EveType
        obj, created = EveType.objects.get_or_create_esi(id=type_id)

        # then
        self.assertEqual(obj.capacity, capacity)
        self.assertEqual(obj.description, description)
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_INVENTORY_TYPE)
        self.assertEqual(obj.eve_graphic, graphic)
        self.assertEqual(obj.eve_group, eg)
        self.assertEqual(obj.eve_market_group, mg)
        self.assertEqual(obj.id, type_id)
        self.assertEqual(obj.mass, mass)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.packaged_volume, packaged_volume)
        self.assertEqual(obj.portion_size, portion_size)
        self.assertEqual(obj.radius, radius)
        self.assertEqual(obj.volume, volume)
        self.assertTrue(created)
        self.assertTrue(obj.published)

        etda: EveTypeDogmaAttribute = obj.dogma_attributes.first()
        self.assertEqual(etda.eve_dogma_attribute, da)
        self.assertEqual(etda.value, da_value)

        etde: EveTypeDogmaEffect = obj.dogma_effects.first()
        self.assertEqual(etde.eve_dogma_effect, de)
        self.assertIs(etde.is_default, de_is_default)

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @pook.on
    def test_can_create_type_from_scratch_with_parents(self):
        # given
        category_id = 6
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
                "name": "Ship",
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
        obj: EveType
        obj, created = EveType.objects.get_or_create_esi(id=type_id)

        # then
        self.assertTrue(created)
        self.assertEqual(obj.name, type_name)

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", True)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @pook.on
    def test_can_create_type_from_esi_with_dogmas(self):
        # given
        graphic = EveGraphicFactory()
        eg = EveGroupFactory()
        mg = EveMarketGroupFactory()
        type_id = 603
        da = EveDogmaAttributeFactory()
        de = EveDogmaEffectFactory()
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [
                    {"attribute_id": da.id, "value": 5},
                ],
                "dogma_effects": [
                    {"effect_id": de.id, "is_default": True},
                ],
                "graphic_id": graphic.id,
                "group_id": eg.id,
                "market_group_id": mg.id,
                "mass": 997000,
                "name": "Merlin",
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": type_id,
                "volume": 16500,
            },
        )

        # when
        obj: EveType
        obj, created = EveType.objects.get_or_create_esi(id=type_id)

        # then
        self.assertTrue(created)
        self.assertIsNone(obj.eve_graphic)
        self.assertEqual(obj.eve_group, eg)
        self.assertIsNone(obj.eve_market_group)
        self.assertEqual(obj.id, type_id)
        self.assertTrue(
            obj.dogma_attributes.filter(eve_dogma_attribute_id=da.id).exists()
        )
        self.assertTrue(obj.dogma_effects.filter(eve_dogma_effect_id=de.id).exists())

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", True)
    @pook.on
    def test_when_disabled_can_create_type_from_esi_excluding_dogmas(self):
        # given
        graphic = EveGraphicFactory()
        eg = EveGroupFactory()
        mg = EveMarketGroupFactory()
        type_id = 603
        da = EveDogmaAttributeFactory()
        de = EveDogmaEffectFactory()
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [
                    {"attribute_id": da.id, "value": 5},
                ],
                "dogma_effects": [
                    {"effect_id": de.id, "is_default": True},
                ],
                "graphic_id": graphic.id,
                "group_id": eg.id,
                "market_group_id": mg.id,
                "mass": 997000,
                "name": "Merlin",
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": type_id,
                "volume": 16500,
            },
        )

        # when
        obj: EveType
        obj, created = EveType.objects.get_or_create_esi(id=type_id)

        # then
        self.assertTrue(created)
        self.assertIsNone(obj.eve_graphic)
        self.assertEqual(obj.eve_group, eg)
        self.assertEqual(obj.eve_market_group, mg)
        self.assertEqual(obj.id, type_id)
        self.assertFalse(obj.dogma_attributes.exists())
        self.assertFalse(obj.dogma_effects.exists())

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @pook.on
    def test_can_create_type_from_esi_including_dogmas_when_disabled_1(self):
        # given
        graphic = EveGraphicFactory()
        eg = EveGroupFactory()
        mg = EveMarketGroupFactory()
        type_id = 603
        da = EveDogmaAttributeFactory()
        de = EveDogmaEffectFactory()
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [
                    {"attribute_id": da.id, "value": 5},
                ],
                "dogma_effects": [
                    {"effect_id": de.id, "is_default": True},
                ],
                "graphic_id": graphic.id,
                "group_id": eg.id,
                "market_group_id": mg.id,
                "mass": 997000,
                "name": "Merlin",
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": type_id,
                "volume": 16500,
            },
        )

        # when
        obj: EveType
        obj, created = EveType.objects.get_or_create_esi(
            id=type_id, enabled_sections=[EveType.LOAD_DOGMAS]
        )

        # then
        self.assertTrue(created)
        self.assertIsNone(obj.eve_graphic)
        self.assertEqual(obj.eve_group, eg)
        self.assertIsNone(obj.eve_market_group)
        self.assertEqual(obj.id, type_id)
        self.assertTrue(
            obj.dogma_attributes.filter(eve_dogma_attribute_id=da.id).exists()
        )
        self.assertTrue(obj.dogma_effects.filter(eve_dogma_effect_id=de.id).exists())

    @override_settings(
        CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True
    )
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @pook.on
    def test_can_create_type_from_esi_including_children_as_task(self):
        # given
        graphic = EveGraphicFactory()
        eg = EveGroupFactory()
        mg = EveMarketGroupFactory()
        type_id = 603
        da = EveDogmaAttributeFactory()
        de = EveDogmaEffectFactory()
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [
                    {"attribute_id": da.id, "value": 5},
                ],
                "dogma_effects": [
                    {"effect_id": de.id, "is_default": True},
                ],
                "graphic_id": graphic.id,
                "group_id": eg.id,
                "market_group_id": mg.id,
                "mass": 997000,
                "name": "Merlin",
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": type_id,
                "volume": 16500,
            },
        )

        # when
        obj: EveType
        obj, created = EveType.objects.get_or_create_esi(
            id=type_id, wait_for_children=False, enabled_sections=[EveType.LOAD_DOGMAS]
        )

        # then
        self.assertTrue(created)
        self.assertIsNone(obj.eve_graphic)
        self.assertEqual(obj.eve_group, eg)
        self.assertIsNone(obj.eve_market_group)
        self.assertEqual(obj.id, type_id)
        self.assertTrue(
            obj.dogma_attributes.filter(eve_dogma_attribute_id=da.id).exists()
        )
        self.assertTrue(obj.dogma_effects.filter(eve_dogma_effect_id=de.id).exists())


@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
class TestEveType_URLs(TestCase):
    def test_can_create_render_url(self):
        eve_type = EveTypeFactory(id=603)
        got = eve_type.render_url(256)
        self.assertEqual(got, "https://images.evetech.net/types/603/render?size=256")

    def test_can_create_profile_url(self):
        eve_type = EveTypeFactory(id=603)
        got = eve_type.profile_url
        self.assertEqual(got, "https://www.kalkoken.org/apps/eveitems/?typeId=603")

    def test_can_create_icon_url_1(self):
        """icon from regular type, automatically detected"""

        eve_type = EveTypeFactory(id=603)
        got = eve_type.icon_url(256)
        self.assertEqual(got, "https://images.evetech.net/types/603/icon?size=256")

    def test_can_create_icon_url_2(self):
        """icon from blueprint type, automatically detected"""

        eve_type = BlueprintTypeFactory(id=950)
        got = eve_type.icon_url(256)
        self.assertEqual(got, "https://images.evetech.net/types/950/bp?size=256")

    def test_can_create_icon_url_3(self):
        """icon from regular type, preset as blueprint"""

        eve_type = EveTypeFactory(id=603)
        got = eve_type.icon_url(size=256, is_blueprint=True)
        self.assertEqual(got, "https://images.evetech.net/types/603/bp?size=256")

    def test_can_create_icon_url_3a(self):
        """icon from regular type, preset as blueprint"""

        eve_type = EveTypeFactory(id=603)
        got = eve_type.icon_url(size=256, category_id=EveCategoryId.BLUEPRINT)
        self.assertEqual(got, "https://images.evetech.net/types/603/bp?size=256")

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", False)
    def test_can_create_icon_url_5(self):
        """when called for SKIN type, will return dummy SKIN URL with requested size"""

        eve_type = SKINTypeFactory(id=34599)
        got = eve_type.icon_url(size=64)
        self.assertIn("skin_generic_64.png", got)

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", False)
    def test_can_create_icon_url_5a(self):
        """when called for SKIN type, will return dummy SKIN URL with requested size"""

        eve_type = SKINTypeFactory(id=34599)
        got = eve_type.icon_url(size=32)
        self.assertIn("skin_generic_32.png", got)

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", False)
    def test_can_create_icon_url_5b(self):
        """when called for SKIN type, will return dummy SKIN URL with requested size"""

        eve_type = SKINTypeFactory(id=34599)
        got = eve_type.icon_url(size=128)
        self.assertIn("skin_generic_128.png", got)

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", False)
    def test_can_create_icon_url_5c(self):
        """when called for SKIN type and size is invalid, then raise exception"""

        eve_type = SKINTypeFactory(id=34599)

        with self.assertRaises(ValueError):
            eve_type.icon_url(size=512)

        with self.assertRaises(ValueError):
            eve_type.icon_url(size=1024)

        with self.assertRaises(ValueError):
            eve_type.icon_url(size=31)

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", False)
    def test_can_create_icon_url_6(self):
        """when called for non SKIN type and SKIN is forced, then return SKIN URL"""

        eve_type = BlueprintTypeFactory(id=950)
        got = eve_type.icon_url(size=128, category_id=EveCategoryId.SKIN)
        self.assertIn("skin_generic_128.png", got)

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", False)
    def test_can_create_icon_url_7(self):
        """when called for SKIN type and regular is forced, then return regular URL"""

        eve_type, _ = EveType.objects.get_or_create_esi(id=34599)

        self.assertEqual(
            eve_type.icon_url(size=256, category_id=EveCategoryId.STRUCTURE),
            "https://images.evetech.net/types/34599/icon?size=256",
        )

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", True)
    def test_can_create_icon_url_8(self):
        """
        when called for SKIN type and eveskinserver is enabled,
        then return corresponding eveskinserver URL
        """

        eve_type = SKINTypeFactory(id=34599)
        got = eve_type.icon_url(size=256)
        self.assertEqual(
            got, "https://eveskinserver.kalkoken.net/skin/34599/icon?size=256"
        )

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", True)
    def test_can_create_icon_url_9(self):
        """can use variants"""

        class Case(NamedTuple):
            name: str
            variant: EveType.IconVariant
            want: str

        cases = [
            Case(
                "regular",
                EveType.IconVariant.REGULAR,
                "https://images.evetech.net/types/603/icon?size=256",
            ),
            Case(
                "regular",
                EveType.IconVariant.BPO,
                "https://images.evetech.net/types/603/bp?size=256",
            ),
            Case(
                "regular",
                EveType.IconVariant.BPC,
                "https://images.evetech.net/types/603/bpc?size=256",
            ),
        ]

        for tc in cases:
            with self.subTest(name=tc.name):
                eve_type = EveTypeFactory(id=603)
                got = eve_type.icon_url(size=256, variant=tc.variant)
                self.assertEqual(got, tc.want)


class TestEveUnit(TestCase):
    def test_get_object(self):
        obj = EveUnit.objects.get(id=10)
        self.assertEqual(obj.id, 10)
        self.assertEqual(obj.name, "Speed")
