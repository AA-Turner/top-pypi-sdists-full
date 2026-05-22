from unittest.mock import patch

import pook
from django.core.cache import cache
from django.test import TestCase

from eveuniverse.models import (
    EveIndustryActivityDuration,
    EveIndustryActivityMaterial,
    EveIndustryActivityProduct,
    EveIndustryActivitySkill,
    EveType,
    EveTypeMaterial,
)
from eveuniverse.tests.testdata.factories_2 import (
    EveGroupFactory,
    EveTypeFactory,
    make_esi_url,
)

MODELS_PATH = "eveuniverse.models.base"
MANAGERS_PATH = "eveuniverse.managers"


@patch(MANAGERS_PATH + ".sde.EVEUNIVERSE_API_SDE_URL", "https://sde.eve-o.tech/latest")
@patch(MANAGERS_PATH + ".sde.cache")
class TestEveTypeMaterial(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cache.clear()

    @pook.on
    def test_should_create_new_instance(self, mock_cache):
        # given
        mock_cache.get.return_value = None
        mock_cache.set.return_value = None

        base_type = EveTypeFactory()
        material_type = EveTypeFactory()
        quantity = 42
        pook.get(
            "https://sde.eve-o.tech/latest/invTypeMaterials.json",
            reply=200,
            response_json=[
                {
                    "materialTypeID": material_type.id,
                    "quantity": quantity,
                    "typeID": base_type.id,
                },
            ],
        )

        # when
        EveTypeMaterial.objects.update_or_create_api(eve_type=base_type)

        # then
        obj = EveTypeMaterial.objects.get(
            eve_type=base_type, material_eve_type=material_type
        )
        self.assertEqual(obj.quantity, quantity)

    @pook.on
    def test_should_use_cache_if_available(self, mock_cache):
        # given
        base_type = EveTypeFactory()
        material_type = EveTypeFactory()
        quantity = 42
        data = [
            {
                "materialTypeID": material_type.id,
                "quantity": quantity,
                "typeID": base_type.id,
            },
        ]
        mock_cache.get.return_value = {base_type.id: data}
        mock_cache.set.return_value = None
        pook.get(
            "https://sde.eve-o.tech/latest/invTypeMaterials.json",
            reply=200,
            response_json=data,
        )

        # when
        EveTypeMaterial.objects.update_or_create_api(eve_type=base_type)

        # then
        obj = EveTypeMaterial.objects.get(
            eve_type=base_type, material_eve_type=material_type
        )
        self.assertEqual(obj.quantity, quantity)

    @pook.on
    def test_should_handle_no_type_materials_for_type(self, mock_cache):
        # given
        mock_cache.get.return_value = None
        mock_cache.set.return_value = None

        base_type = EveTypeFactory()
        pook.get(
            "https://sde.eve-o.tech/latest/invTypeMaterials.json",
            reply=200,
            response_json=[],
        )

        # when
        EveTypeMaterial.objects.update_or_create_api(eve_type=base_type)

        # then
        self.assertFalse(EveTypeMaterial.objects.filter(eve_type=base_type).exists())

    @pook.on
    def test_should_fetch_typematerials_when_creating_type_and_enabled(
        self, mock_cache
    ):
        # given
        mock_cache.get.return_value = None
        mock_cache.set.return_value = None
        base_type_id = 603
        eg = EveGroupFactory()
        pook.get(
            make_esi_url(f"universe/types/{base_type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [],
                "dogma_effects": [],
                "graphic_id": 314,
                "group_id": eg.id,
                "market_group_id": 61,
                "mass": 997000,
                "name": "Merlin",
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": base_type_id,
                "volume": 16500,
            },
        )
        material_type = EveTypeFactory(enabled_sections=8)  # prevent refetching

        quantity = 42
        pook.get(
            "https://sde.eve-o.tech/latest/invTypeMaterials.json",
            reply=200,
            response_json=[
                {
                    "materialTypeID": material_type.id,
                    "quantity": quantity,
                    "typeID": base_type_id,
                },
            ],
        )

        # when
        with patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", True):
            EveType.objects.get_or_create_esi(id=base_type_id)

        # then
        obj = EveTypeMaterial.objects.get(
            eve_type_id=base_type_id, material_eve_type=material_type
        )
        self.assertEqual(obj.quantity, quantity)

    @pook.on
    def test_should_ignore_typematerials_when_creating_type_and_disabled(
        self, mock_cache
    ):
        # given
        mock_cache.get.return_value = None
        mock_cache.set.return_value = None
        base_type_id = 603
        eg = EveGroupFactory()
        pook.get(
            make_esi_url(f"universe/types/{base_type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [],
                "dogma_effects": [],
                "graphic_id": 314,
                "group_id": eg.id,
                "market_group_id": 61,
                "mass": 997000,
                "name": "Merlin",
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": base_type_id,
                "volume": 16500,
            },
        )
        material_type = EveTypeFactory(enabled_sections=8)  # prevent refetching

        quantity = 42
        pook.get(
            "https://sde.eve-o.tech/latest/invTypeMaterials.json",
            reply=200,
            response_json=[
                {
                    "materialTypeID": material_type.id,
                    "quantity": quantity,
                    "typeID": base_type_id,
                },
            ],
        )

        # when
        with patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False):
            EveType.objects.get_or_create_esi(id=base_type_id)

        # then
        self.assertFalse(
            EveTypeMaterial.objects.filter(eve_type_id=base_type_id).exists()
        )


@patch(MANAGERS_PATH + ".sde.EVEUNIVERSE_API_SDE_URL", "https://sde.eve-o.tech/latest")
class TestEveIndustryManagers(TestCase):
    def setUp(self):
        cache.clear()

    @pook.on
    def test_industry_activity(self):
        # given
        base_type = EveTypeFactory()
        activity_id = 1
        time = 6000
        pook.get(
            "https://sde.eve-o.tech/latest/industryActivity.json",
            reply=200,
            response_json=[
                {"activityID": 1, "time": time, "typeID": base_type.id},
            ],
        )

        # when
        EveIndustryActivityDuration.objects.update_or_create_api(eve_type=base_type)

        # then
        obj = EveIndustryActivityDuration.objects.get(
            eve_type=base_type, activity_id=activity_id
        )
        self.assertEqual(obj.time, time)

    @pook.on
    def test_industry_activity_materials(self):
        # given
        base_type = EveTypeFactory()
        activity_id = 1
        quantity = 32000
        material_type = EveTypeFactory()
        pook.get(
            "https://sde.eve-o.tech/latest/industryActivityMaterials.json",
            reply=200,
            response_json=[
                {
                    "typeID": base_type.id,
                    "activityID": activity_id,
                    "materialTypeID": material_type.id,
                    "quantity": quantity,
                },
            ],
        )

        # when
        EveIndustryActivityMaterial.objects.update_or_create_api(eve_type=base_type)

        # then
        obj = EveIndustryActivityMaterial.objects.get(
            eve_type=base_type, material_eve_type=material_type, activity_id=activity_id
        )
        self.assertEqual(obj.quantity, quantity)

    @pook.on
    def test_industry_activity_products(self):
        # given
        base_type = EveTypeFactory()
        activity_id = 1
        quantity = 32000
        product_type = EveTypeFactory()
        pook.get(
            "https://sde.eve-o.tech/latest/industryActivityProducts.json",
            reply=200,
            response_json=[
                {
                    "typeID": base_type.id,
                    "activityID": activity_id,
                    "productTypeID": product_type.id,
                    "quantity": quantity,
                }
            ],
        )

        # when
        EveIndustryActivityProduct.objects.update_or_create_api(eve_type=base_type)

        # then
        obj = EveIndustryActivityProduct.objects.get(
            eve_type=base_type, product_eve_type=product_type, activity_id=activity_id
        )
        self.assertEqual(obj.quantity, quantity)

    @pook.on
    def test_industry_activity_skills(self):
        # given
        base_type = EveTypeFactory()
        activity_id = 1
        level = 3
        skill_type = EveTypeFactory()
        pook.get(
            "https://sde.eve-o.tech/latest/industryActivitySkills.json",
            reply=200,
            response_json=[
                {
                    "typeID": base_type.id,
                    "activityID": activity_id,
                    "skillID": skill_type.id,
                    "level": level,
                }
            ],
        )

        # when
        EveIndustryActivitySkill.objects.update_or_create_api(eve_type=base_type)

        # then
        obj = EveIndustryActivitySkill.objects.get(
            eve_type=base_type, skill_eve_type=skill_type, activity_id=activity_id
        )
        self.assertEqual(obj.level, level)
