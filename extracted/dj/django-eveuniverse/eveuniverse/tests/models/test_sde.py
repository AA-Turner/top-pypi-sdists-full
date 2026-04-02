from unittest.mock import patch

import requests_mock

from eveuniverse.models import (
    EveIndustryActivityDuration,
    EveIndustryActivityMaterial,
    EveIndustryActivityProduct,
    EveIndustryActivitySkill,
    EveType,
    EveTypeMaterial,
)
from eveuniverse.utils import NoSocketsTestCase

from ..testdata.esi import EsiClientStub
from ..testdata.sde import cache_content, sde_data, type_materials_cache_content

MODELS_PATH = "eveuniverse.models.base"
MANAGERS_PATH = "eveuniverse.managers"


def get_cache_content(cache_key):
    table_name = {
        "EVEUNIVERSE_INDUSTRY_ACTIVITY_MATERIALS_REQUEST": "industry_activity_materials",
        "EVEUNIVERSE_INDUSTRY_ACTIVITY_PRODUCTS_REQUEST": "industry_activity_products",
        "EVEUNIVERSE_INDUSTRY_ACTIVITY_SKILLS_REQUEST": "industry_activity_skills",
        "EVEUNIVERSE_INDUSTRY_ACTIVITY_DURATIONS_REQUEST": "industry_activity_durations",
        "EVEUNIVERSE_TYPE_MATERIALS_REQUEST": "type_materials",
    }.get(cache_key)
    return cache_content(table=table_name)


@patch(MANAGERS_PATH + ".sde.EVEUNIVERSE_API_SDE_URL", "https://sde.eve-o.tech/latest")
@patch(MANAGERS_PATH + ".sde.cache")
@patch(MANAGERS_PATH + ".universe.esi")
@requests_mock.Mocker()
class TestEveTypeMaterial(NoSocketsTestCase):
    def test_should_create_new_instance(self, mock_esi, mock_cache, requests_mocker):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = None
        mock_cache.set.return_value = None
        requests_mocker.register_uri(
            "GET",
            url="https://sde.eve-o.tech/latest/invTypeMaterials.json",
            json=sde_data["type_materials"],
        )
        with patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False):
            eve_type, _ = EveType.objects.get_or_create_esi(id=603)
        # when
        EveTypeMaterial.objects.update_or_create_api(eve_type=eve_type)
        # then
        self.assertTrue(requests_mocker.called)
        self.assertTrue(mock_cache.set.called)
        self.assertSetEqual(
            set(
                EveTypeMaterial.objects.filter(eve_type_id=603).values_list(
                    "material_eve_type_id", flat=True
                )
            ),
            {34, 35, 36, 37, 38, 39, 40},
        )
        obj = EveTypeMaterial.objects.get(eve_type_id=603, material_eve_type_id=34)
        self.assertEqual(obj.quantity, 21111)
        obj = EveTypeMaterial.objects.get(eve_type_id=603, material_eve_type_id=35)
        self.assertEqual(obj.quantity, 8889)
        obj = EveTypeMaterial.objects.get(eve_type_id=603, material_eve_type_id=36)
        self.assertEqual(obj.quantity, 3111)
        obj = EveTypeMaterial.objects.get(eve_type_id=603, material_eve_type_id=37)
        self.assertEqual(obj.quantity, 589)
        obj = EveTypeMaterial.objects.get(eve_type_id=603, material_eve_type_id=38)
        self.assertEqual(obj.quantity, 2)
        obj = EveTypeMaterial.objects.get(eve_type_id=603, material_eve_type_id=39)
        self.assertEqual(obj.quantity, 4)
        obj = EveTypeMaterial.objects.get(eve_type_id=603, material_eve_type_id=40)
        self.assertEqual(obj.quantity, 4)

    def test_should_use_cache_if_available(self, mock_esi, mock_cache, requests_mocker):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = type_materials_cache_content()
        mock_cache.set.return_value = None
        requests_mocker.register_uri(
            "GET",
            url="https://sde.eve-o.tech/latest/invTypeMaterials.json",
            json=sde_data["type_materials"],
        )
        with patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False):
            eve_type, _ = EveType.objects.get_or_create_esi(id=603)
        # when
        EveTypeMaterial.objects.update_or_create_api(eve_type=eve_type)
        # then
        self.assertFalse(requests_mocker.called)
        self.assertFalse(mock_cache.set.called)
        self.assertSetEqual(
            set(
                EveTypeMaterial.objects.filter(eve_type_id=603).values_list(
                    "material_eve_type_id", flat=True
                )
            ),
            {34, 35, 36, 37, 38, 39, 40},
        )

    def test_should_handle_no_type_materials_for_type(
        self, mock_esi, mock_cache, requests_mocker
    ):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = None
        mock_cache.set.return_value = None
        requests_mocker.register_uri(
            "GET",
            url="https://sde.eve-o.tech/latest/invTypeMaterials.json",
            json=sde_data["type_materials"],
        )
        with patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False):
            eve_type, _ = EveType.objects.get_or_create_esi(id=34)
        # when
        EveTypeMaterial.objects.update_or_create_api(eve_type=eve_type)
        # then
        self.assertTrue(requests_mocker.called)
        self.assertTrue(mock_cache.set.called)
        self.assertSetEqual(
            set(
                EveTypeMaterial.objects.filter(eve_type_id=603).values_list(
                    "material_eve_type_id", flat=True
                )
            ),
            set(),
        )

    def test_should_fetch_typematerials_when_creating_type_and_enabled(
        self, mock_esi, mock_cache, requests_mocker
    ):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = None
        mock_cache.set.return_value = None
        requests_mocker.register_uri(
            "GET",
            url="https://sde.eve-o.tech/latest/invTypeMaterials.json",
            json=sde_data["type_materials"],
        )
        # when
        with patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", True):
            eve_type, _ = EveType.objects.update_or_create_esi(id=603)
        # then
        self.assertTrue(requests_mocker.called)
        self.assertTrue(mock_cache.set.called)
        self.assertSetEqual(
            set(
                EveTypeMaterial.objects.filter(eve_type_id=603).values_list(
                    "material_eve_type_id", flat=True
                )
            ),
            {34, 35, 36, 37, 38, 39, 40},
        )

    def test_should_ignore_typematerials_when_creating_type_and_disabled(
        self, mock_esi, mock_cache, requests_mocker
    ):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = None
        mock_cache.set.return_value = None
        requests_mocker.register_uri(
            "GET",
            url="https://sde.eve-o.tech/latest/invTypeMaterials.json",
            json=sde_data["type_materials"],
        )
        # when
        with patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False):
            eve_type, _ = EveType.objects.update_or_create_esi(id=603)
        # then
        self.assertFalse(requests_mocker.called)
        self.assertFalse(mock_cache.set.called)
        self.assertSetEqual(
            set(
                EveTypeMaterial.objects.filter(eve_type_id=603).values_list(
                    "material_eve_type_id", flat=True
                )
            ),
            set(),
        )


@patch(MANAGERS_PATH + ".sde.cache")
@patch(MANAGERS_PATH + ".universe.esi")
@requests_mock.Mocker()
class TestEveIndustryActivityDuration(NoSocketsTestCase):
    def test_should_create_new_instance(self, mock_esi, mock_cache, requests_mocker):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = None
        mock_cache.set.return_value = None
        requests_mocker.register_uri(
            "GET",
            url="https://sde.eve-o.tech/latest/industryActivity.json",
            json=sde_data["industry_activity_durations"],
        )
        merlin_blueprint, _ = EveType.objects.get_or_create_esi(id=950)

        EveIndustryActivityDuration.objects.update_or_create_api(
            eve_type=merlin_blueprint,
        )
        # then
        self.assertTrue(requests_mocker.called)
        self.assertTrue(mock_cache.set.called)
        self.assertSetEqual(
            set(
                EveIndustryActivityDuration.objects.filter(eve_type_id=950).values_list(
                    "activity_id", flat=True
                )
            ),
            {1, 8, 3, 4, 5},
        )
        obj = EveIndustryActivityDuration.objects.get(eve_type_id=950, activity_id=8)
        self.assertEqual(obj.time, 63900)
        obj = EveIndustryActivityDuration.objects.get(eve_type_id=950, activity_id=1)
        self.assertEqual(obj.time, 6000)
        obj = EveIndustryActivityDuration.objects.get(eve_type_id=950, activity_id=3)
        self.assertEqual(obj.time, 2100)
        obj = EveIndustryActivityDuration.objects.get(eve_type_id=950, activity_id=4)
        self.assertEqual(obj.time, 2100)

        obj = EveIndustryActivityDuration.objects.get(eve_type_id=950, activity_id=5)
        self.assertEqual(obj.time, 4800)

    def test_should_use_cache_if_available(self, mock_esi, mock_cache, requests_mocker):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = cache_content("industry_activity_durations")
        mock_cache.set.return_value = None
        requests_mocker.register_uri(
            "GET",
            url="https://sde.eve-o.tech/latest/industryActivity.json",
            json=sde_data["industry_activity_durations"],
        )
        eve_type, _ = EveType.objects.get_or_create_esi(id=950)
        # when
        EveIndustryActivityDuration.objects.update_or_create_api(eve_type=eve_type)
        # then
        self.assertFalse(requests_mocker.called)
        self.assertFalse(mock_cache.set.called)
        self.assertSetEqual(
            set(
                EveIndustryActivityDuration.objects.filter(eve_type_id=950).values_list(
                    "activity_id", flat=True
                )
            ),
            {1, 8, 3, 4, 5},
        )


@patch(MANAGERS_PATH + ".sde.cache")
@patch(MANAGERS_PATH + ".universe.esi")
@requests_mock.Mocker()
class TestEveIndustryActivityMaterial(NoSocketsTestCase):
    def test_should_create_new_instance(self, mock_esi, mock_cache, requests_mocker):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = None
        mock_cache.set.return_value = None
        requests_mocker.register_uri(
            "GET",
            url="https://sde.eve-o.tech/latest/industryActivityMaterials.json",
            json=sde_data["industry_activity_materials"],
        )
        merlin_blueprint, _ = EveType.objects.get_or_create_esi(id=950)
        EveIndustryActivityMaterial.objects.update_or_create_api(
            eve_type=merlin_blueprint,
        )
        # then
        self.assertTrue(requests_mocker.called)
        self.assertTrue(mock_cache.set.called)
        self.assertSetEqual(
            set(
                EveIndustryActivityMaterial.objects.filter(
                    eve_type=merlin_blueprint
                ).values_list("material_eve_type_id", flat=True)
            ),
            {34, 35, 36, 37},
        )
        obj = EveIndustryActivityMaterial.objects.get(
            eve_type_id=950, material_eve_type_id=34
        )
        self.assertEqual(obj.quantity, 32000)
        obj = EveIndustryActivityMaterial.objects.get(
            eve_type_id=950, material_eve_type_id=35
        )
        self.assertEqual(obj.quantity, 6000)
        obj = EveIndustryActivityMaterial.objects.get(
            eve_type_id=950, material_eve_type_id=36
        )
        self.assertEqual(obj.quantity, 2500)

        obj = EveIndustryActivityMaterial.objects.get(
            eve_type_id=950, material_eve_type_id=37
        )
        self.assertEqual(obj.quantity, 500)

    def test_should_use_cache_if_available(self, mock_esi, mock_cache, requests_mocker):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = cache_content("industry_activity_materials")
        mock_cache.set.return_value = None
        requests_mocker.register_uri(
            "GET",
            url="https://sde.eve-o.tech/latest/industryActivityMaterials.json",
            json=sde_data["industry_activity_materials"],
        )
        eve_type, _ = EveType.objects.get_or_create_esi(id=950)
        # when
        EveIndustryActivityMaterial.objects.update_or_create_api(eve_type=eve_type)
        # then
        self.assertFalse(requests_mocker.called)
        self.assertFalse(mock_cache.set.called)
        self.assertSetEqual(
            set(
                EveIndustryActivityMaterial.objects.filter(
                    eve_type=eve_type
                ).values_list("material_eve_type_id", flat=True)
            ),
            {34, 35, 36, 37},
        )


@patch(MANAGERS_PATH + ".sde.cache")
@patch(MANAGERS_PATH + ".universe.esi")
@requests_mock.Mocker()
class TestEveIndustryActivityProduct(NoSocketsTestCase):
    def test_should_create_new_instance(self, mock_esi, mock_cache, requests_mocker):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = None
        mock_cache.set.return_value = None
        requests_mocker.register_uri(
            "GET",
            url="https://sde.eve-o.tech/latest/industryActivityProducts.json",
            json=sde_data["industry_activity_products"],
        )
        merlin_blueprint, _ = EveType.objects.get_or_create_esi(id=950)
        EveIndustryActivityProduct.objects.update_or_create_api(
            eve_type=merlin_blueprint,
        )
        # then
        self.assertTrue(requests_mocker.called)
        self.assertTrue(mock_cache.set.called)
        self.assertSetEqual(
            set(
                EveIndustryActivityProduct.objects.filter(
                    eve_type=merlin_blueprint
                ).values_list("product_eve_type_id", flat=True)
            ),
            {603},
        )
        obj = EveIndustryActivityProduct.objects.get(
            eve_type_id=950, product_eve_type_id=603
        )
        self.assertEqual(obj.quantity, 1)

    def test_should_use_cache_if_available(self, mock_esi, mock_cache, requests_mocker):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = cache_content("industry_activity_products")
        mock_cache.set.return_value = None
        requests_mocker.register_uri(
            "GET",
            url="https://sde.eve-o.tech/latest/industryActivityProducts.json",
            json=sde_data["industry_activity_products"],
        )
        eve_type, _ = EveType.objects.get_or_create_esi(id=950)
        # when
        EveIndustryActivityProduct.objects.update_or_create_api(eve_type=eve_type)
        # then
        self.assertFalse(requests_mocker.called)
        self.assertFalse(mock_cache.set.called)
        self.assertSetEqual(
            set(
                EveIndustryActivityProduct.objects.filter(
                    eve_type=eve_type
                ).values_list("product_eve_type_id", flat=True)
            ),
            {603},
        )


@patch(MANAGERS_PATH + ".sde.cache")
@patch(MANAGERS_PATH + ".universe.esi")
@requests_mock.Mocker()
class TestEveIndustryActivitySkill(NoSocketsTestCase):
    def test_should_create_new_instance(self, mock_esi, mock_cache, requests_mocker):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = None
        mock_cache.set.return_value = None
        requests_mocker.register_uri(
            "GET",
            url="https://sde.eve-o.tech/latest/industryActivitySkills.json",
            json=sde_data["industry_activity_skills"],
        )
        merlin_blueprint, _ = EveType.objects.get_or_create_esi(id=950)
        EveIndustryActivitySkill.objects.update_or_create_api(
            eve_type=merlin_blueprint,
        )
        # then
        self.assertTrue(requests_mocker.called)
        self.assertTrue(mock_cache.set.called)
        self.assertSetEqual(
            set(
                EveIndustryActivitySkill.objects.filter(
                    eve_type=merlin_blueprint
                ).values_list("skill_eve_type_id", flat=True)
            ),
            {3380},
        )

    def test_should_use_cache_if_avaliable(self, mock_esi, mock_cache, requests_mocker):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = cache_content("industry_activity_skills")
        mock_cache.set.return_value = None
        requests_mocker.register_uri(
            "GET",
            url="https://sde.eve-o.tech/latest/industryActivitySkills.json",
            json=sde_data["industry_activity_skills"],
        )
        merlin_blueprint, _ = EveType.objects.get_or_create_esi(id=950)
        EveIndustryActivitySkill.objects.update_or_create_api(
            eve_type=merlin_blueprint,
        )
        # then
        self.assertFalse(requests_mocker.called)
        self.assertFalse(mock_cache.set.called)
        self.assertSetEqual(
            set(
                EveIndustryActivitySkill.objects.filter(
                    eve_type=merlin_blueprint
                ).values_list("skill_eve_type_id", flat=True)
            ),
            {3380},
        )
        obj = EveIndustryActivitySkill.objects.get(
            eve_type_id=950,
        )
        self.assertEqual(obj.level, 1)


@patch(MANAGERS_PATH + ".sde.cache")
@patch(MANAGERS_PATH + ".universe.esi")
class TestEveTypeWithSections(NoSocketsTestCase):
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
    def test_should_create_type_with_no_enabled_sections(self, mock_esi, mock_cache):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, created = EveType.objects.update_or_create_esi(id=603)
        # then
        self.assertEqual(obj.id, 603)
        self.assertEqual(obj.materials.count(), 0)
        self.assertEqual(obj.enabled_sections._value, 0)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", True)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
    def test_should_create_type_with_dogmas_global(self, mock_esi, mock_cache):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveType.objects.update_or_create_esi(id=603)
        # then
        self.assertEqual(obj.id, 603)
        self.assertEqual(
            set(obj.dogma_attributes.values_list("eve_dogma_attribute_id", flat=True)),
            {129, 588},
        )
        self.assertEqual(
            set(obj.dogma_effects.values_list("eve_dogma_effect_id", flat=True)),
            {1816, 1817},
        )
        self.assertTrue(obj.enabled_sections.dogmas)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
    def test_should_create_type_with_dogmas_on_demand(self, mock_esi, mock_cache):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveType.objects.update_or_create_esi(
            id=603, enabled_sections=[EveType.Section.DOGMAS]
        )
        # then
        self.assertEqual(obj.id, 603)
        self.assertEqual(
            set(obj.dogma_attributes.values_list("eve_dogma_attribute_id", flat=True)),
            {129, 588},
        )
        self.assertEqual(
            set(obj.dogma_effects.values_list("eve_dogma_effect_id", flat=True)),
            {1816, 1817},
        )
        self.assertTrue(obj.enabled_sections.dogmas)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", True)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
    def test_should_create_type_with_graphics_global(self, mock_esi, mock_cache):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveType.objects.update_or_create_esi(id=603)
        # then
        self.assertEqual(obj.id, 603)
        self.assertEqual(obj.eve_graphic_id, 314)
        self.assertTrue(obj.enabled_sections.graphics)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
    def test_should_create_type_with_graphics_on_demand(self, mock_esi, mock_cache):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveType.objects.update_or_create_esi(
            id=603, enabled_sections=[EveType.Section.GRAPHICS]
        )
        # then
        self.assertEqual(obj.id, 603)
        self.assertEqual(obj.eve_graphic_id, 314)
        self.assertTrue(obj.enabled_sections.graphics)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", True)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
    def test_should_create_type_with_market_groups_global(self, mock_esi, mock_cache):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveType.objects.update_or_create_esi(id=603)
        # then
        self.assertEqual(obj.id, 603)
        self.assertEqual(obj.eve_market_group_id, 61)
        self.assertTrue(obj.enabled_sections.market_groups)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
    def test_should_create_type_with_market_groups_on_demand(
        self, mock_esi, mock_cache
    ):
        # given
        mock_esi.client = EsiClientStub()
        # when
        obj, _ = EveType.objects.update_or_create_esi(
            id=603, enabled_sections=[EveType.Section.MARKET_GROUPS]
        )
        # then
        self.assertEqual(obj.id, 603)
        self.assertEqual(obj.eve_market_group_id, 61)
        self.assertTrue(obj.enabled_sections.market_groups)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", True)
    def test_should_create_type_with_type_materials_global(self, mock_esi, mock_cache):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = type_materials_cache_content()
        # when
        obj, created = EveType.objects.update_or_create_esi(id=603)
        # then
        self.assertEqual(obj.id, 603)
        self.assertEqual(
            set(obj.materials.values_list("material_eve_type_id", flat=True)),
            {34, 35, 36, 37, 38, 39, 40},
        )
        self.assertTrue(obj.enabled_sections.type_materials)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
    def test_should_create_type_with_type_materials_on_demand(
        self, mock_esi, mock_cache
    ):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = type_materials_cache_content()
        # when
        obj, created = EveType.objects.update_or_create_esi(
            id=603, enabled_sections=[EveType.Section.TYPE_MATERIALS]
        )
        # then
        self.assertEqual(obj.id, 603)
        self.assertEqual(
            set(obj.materials.values_list("material_eve_type_id", flat=True)),
            {34, 35, 36, 37, 38, 39, 40},
        )
        self.assertTrue(obj.enabled_sections.type_materials)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
    def test_should_not_fetch_type_again(self, mock_esi, mock_cache):
        # given
        mock_esi.client = EsiClientStub()
        EveType.objects.update_or_create_esi(id=603)
        # when
        obj, created = EveType.objects.get_or_create_esi(id=603)
        # then
        self.assertEqual(obj.id, 603)
        self.assertFalse(created)
        self.assertEqual(obj.enabled_sections._value, 0)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
    def test_should_fetch_type_again_with_section_on_demand_1(
        self, mock_esi, mock_cache
    ):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = type_materials_cache_content()
        EveType.objects.update_or_create_esi(id=603)
        # when
        obj, created = EveType.objects.get_or_create_esi(
            id=603, enabled_sections=[EveType.Section.TYPE_MATERIALS]
        )
        # then
        self.assertEqual(obj.id, 603)
        self.assertFalse(created)
        self.assertEqual(
            set(obj.materials.values_list("material_eve_type_id", flat=True)),
            {34, 35, 36, 37, 38, 39, 40},
        )
        self.assertTrue(obj.enabled_sections.type_materials)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
    def test_should_fetch_type_again_with_section_on_demand_2(
        self, mock_esi, mock_cache
    ):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get.return_value = type_materials_cache_content()
        EveType.objects.update_or_create_esi(
            id=603, enabled_sections=[EveType.Section.TYPE_MATERIALS]
        )
        # when
        obj, created = EveType.objects.get_or_create_esi(
            id=603, enabled_sections=[EveType.Section.GRAPHICS]
        )
        # then
        self.assertEqual(obj.id, 603)
        self.assertFalse(created)
        self.assertEqual(
            set(obj.materials.values_list("material_eve_type_id", flat=True)),
            {34, 35, 36, 37, 38, 39, 40},
        )
        self.assertEqual(obj.eve_graphic_id, 314)
        self.assertTrue(obj.enabled_sections.graphics)
        self.assertTrue(obj.enabled_sections.type_materials)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_INDUSTRY_ACTIVITIES", True)
    def test_should_create_blueprint_with_industry_records_global(
        self, mock_esi, mock_cache
    ):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get = get_cache_content
        # when
        obj, created = EveType.objects.update_or_create_esi(
            id=950,
        )  # Merlin BPC
        self.assertTrue(EveIndustryActivityDuration.objects.filter(eve_type_id=950))
        self.assertTrue(EveIndustryActivityMaterial.objects.filter(eve_type_id=950))
        self.assertTrue(EveIndustryActivityProduct.objects.filter(eve_type_id=950))
        self.assertTrue(EveIndustryActivitySkill.objects.filter(eve_type_id=950))

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_INDUSTRY_ACTIVITIES", False)
    def test_should_create_blueprint_with_industry_records_on_demand(
        self, mock_esi, mock_cache
    ):
        # given
        mock_esi.client = EsiClientStub()
        mock_cache.get = get_cache_content
        # when
        obj, created = EveType.objects.update_or_create_esi(
            id=950, enabled_sections=[EveType.Section.INDUSTRY_ACTIVITIES]
        )  # Merlin BPC
        self.assertTrue(EveIndustryActivityDuration.objects.filter(eve_type_id=950))
        self.assertTrue(EveIndustryActivityMaterial.objects.filter(eve_type_id=950))
        self.assertTrue(EveIndustryActivityProduct.objects.filter(eve_type_id=950))
        self.assertTrue(EveIndustryActivitySkill.objects.filter(eve_type_id=950))
