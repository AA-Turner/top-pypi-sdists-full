from unittest.mock import patch

import pook
from django.test import TestCase
from django.test.utils import override_settings
from esi.exceptions import HTTPServerError

from eveuniverse.models import (
    EveAncestry,
    EveBloodline,
    EveCategory,
    EveConstellation,
    EveDogmaEffect,
    EveGroup,
    EveRegion,
    EveType,
    EveTypeDogmaEffect,
)
from eveuniverse.models.base import _EsiFieldMapping, determine_effective_sections
from eveuniverse.tests.helpers import TestCaseWithClearCache
from eveuniverse.tests.testdata.factories_2 import (
    EveCategoryFactory,
    EveDogmaAttributeFactory,
    EveDogmaEffectFactory,
    make_esi_url,
)

MODELS_PATH = "eveuniverse.models.base"


class TestGetOrCreateEsi(TestCaseWithClearCache):

    @pook.on
    def test_should_load_object_from_esi_when_not_exists(self):
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

    @pook.on
    def test_should_return_object_when_exists(self):
        # given
        o1 = EveCategoryFactory()

        # when
        o2: EveCategory
        o2, created = EveCategory.objects.get_or_create_esi(id=o1.id)

        # then
        self.assertFalse(created)
        self.assertEqual(o2.id, o1.id)
        self.assertEqual(o2.name, o1.name)
        self.assertTrue(o2.published)

    @pook.on
    def test_can_load_from_esi_including_children(self):
        category_id = 6
        group_id = 25
        type_id = 603
        pook.get(
            make_esi_url(f"universe/categories/{category_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "groups": [25],
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
                "name": "Frigate",
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
                "graphic_id": 314,
                "group_id": 25,
                "market_group_id": 61,
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
        obj: EveCategory
        obj, created = EveCategory.objects.get_or_create_esi(
            id=category_id, include_children=True, wait_for_children=True
        )

        # then
        self.assertTrue(created)
        self.assertEqual(obj.id, category_id)
        self.assertTrue(EveGroup.objects.filter(id=group_id).exists())
        self.assertTrue(EveType.objects.filter(id=type_id).exists())

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @pook.on
    def test_can_enable_sections_on_demand(self):
        # given
        category_id = 6
        da = EveDogmaAttributeFactory()
        de = EveDogmaEffectFactory()
        group_id = 25
        type_id = 603
        pook.get(
            make_esi_url(f"universe/categories/{category_id}"),
            reply=200,
            response_json={
                "category_id": category_id,
                "groups": [25],
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
                "name": "Frigate",
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
                "dogma_attributes": [
                    {"attribute_id": da.id, "value": 5},
                ],
                "dogma_effects": [
                    {"effect_id": de.id, "is_default": True},
                ],
                "graphic_id": 314,
                "group_id": 25,
                "market_group_id": 61,
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
        EveCategory.objects.get_or_create_esi(
            id=category_id,
            include_children=True,
            wait_for_children=True,
            enabled_sections=[EveType.LOAD_DOGMAS],
        )

        # then
        et = EveType.objects.get(id=type_id)
        self.assertTrue(
            et.dogma_attributes.filter(eve_dogma_attribute_id=da.id).exists()
        )
        self.assertTrue(et.dogma_effects.filter(eve_dogma_effect_id=de.id).exists())


class TestUpdateOrCreateEsi(TestCaseWithClearCache):
    @pook.on
    def test_should_update_from_esi_when_it_exists(self):
        # given
        o1 = EveCategoryFactory(name="Replace me", published=False)
        pook.get(
            make_esi_url(f"universe/categories/{o1.id}"),
            reply=200,
            response_json={
                "category_id": o1.id,
                "groups": [25, 26],
                "name": "Alpha",
                "published": True,
            },
        )

        # when
        o2: EveCategory
        o2, created = EveCategory.objects.update_or_create_esi(id=o1.id)

        # then
        self.assertFalse(created)
        self.assertEqual(o2.name, "Alpha")
        self.assertTrue(o2.published)


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
class TestUpdateOrCreateAllESI(TestCaseWithClearCache):
    @pook.on
    def test_should_update_without_children_and_sync(self):
        # given
        category_id = 6
        group_id = 25
        type_id = 603
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
                "groups": [25],
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
                "name": "Frigate",
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
                "graphic_id": 314,
                "group_id": 25,
                "market_group_id": 61,
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
        EveCategory.objects.update_or_create_all_esi(
            include_children=False, wait_for_children=True
        )

        # then
        self.assertTrue(EveCategory.objects.filter(id=category_id).exists())
        self.assertFalse(EveGroup.objects.filter(id=group_id).exists())
        self.assertFalse(EveType.objects.filter(id=type_id).exists())

    @pook.on
    def test_should_update_with_children_and_sync(self):
        # given
        category_id = 6
        group_id = 25
        type_id = 603
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
                "groups": [25],
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
                "name": "Frigate",
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
                "graphic_id": 314,
                "group_id": 25,
                "market_group_id": 61,
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
        EveCategory.objects.update_or_create_all_esi(
            include_children=True, wait_for_children=True
        )

        # then
        self.assertTrue(EveCategory.objects.filter(id=category_id).exists())
        self.assertTrue(EveGroup.objects.filter(id=group_id).exists())
        self.assertTrue(EveType.objects.filter(id=type_id).exists())

    @pook.on
    def test_should_update_with_children_and_async(self):
        # given
        category_id = 6
        group_id = 25
        type_id = 603
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
                "groups": [25],
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
                "name": "Frigate",
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
                "graphic_id": 314,
                "group_id": 25,
                "market_group_id": 61,
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
        EveCategory.objects.update_or_create_all_esi(
            include_children=True, wait_for_children=False
        )

        # then
        self.assertTrue(EveCategory.objects.filter(id=category_id).exists())
        self.assertTrue(EveGroup.objects.filter(id=group_id).exists())
        self.assertTrue(EveType.objects.filter(id=type_id).exists())

    @pook.on
    def test_should_raise_exception_on_error(self):
        # given
        pook.get(
            make_esi_url("universe/categories"),
            reply=500,
            response_json={"error": "some error"},
        )

        # when/then
        with self.assertRaises(HTTPServerError):
            EveCategory.objects.update_or_create_all_esi(
                include_children=False, wait_for_children=True
            )


class TestBulkGetOrCreateEsi(TestCaseWithClearCache):
    @pook.on
    def test_can_load_all_from_esi(self):
        # given
        obj_1_id = 6
        obj_2_id = 7
        pook.get(
            make_esi_url(f"universe/categories/{obj_1_id}"),
            reply=200,
            response_json={
                "category_id": obj_1_id,
                "groups": [],
                "name": "Alpha",
                "published": True,
            },
        )
        pook.get(
            make_esi_url(f"universe/categories/{obj_2_id}"),
            reply=200,
            response_json={
                "category_id": obj_1_id,
                "groups": [],
                "name": "Bravo",
                "published": True,
            },
        )

        # when
        result = EveCategory.objects.bulk_get_or_create_esi(ids=[obj_1_id, obj_2_id])

        # then
        self.assertEqual({x.id for x in result}, {obj_1_id, obj_2_id})
        self.assertTrue(EveCategory.objects.filter(id=obj_1_id).exists())
        self.assertTrue(EveCategory.objects.filter(id=obj_2_id).exists())

    @pook.on
    def test_can_load_parts_from_esi(self):
        # given
        obj_1_id = 6
        obj_2_id = 7
        EveCategoryFactory(id=obj_1_id)
        pook.get(
            make_esi_url(f"universe/categories/{obj_2_id}"),
            reply=200,
            response_json={
                "category_id": obj_1_id,
                "groups": [],
                "name": "Bravo",
                "published": True,
            },
        )

        # when
        result = EveCategory.objects.bulk_get_or_create_esi(ids=[obj_1_id, obj_2_id])

        # then
        self.assertEqual({x.id for x in result}, {obj_1_id, obj_2_id})


class TestEsiMapping(TestCase):
    maxDiff = None

    def test_single_pk(self):
        mapping = EveCategory._esi_field_mappings()
        self.assertEqual(len(mapping.keys()), 3)
        self.assertEqual(
            mapping["id"],
            _EsiFieldMapping(
                esi_name="category_id",
                is_optional=False,
                is_pk=True,
                is_fk=False,
                related_model=None,
                is_parent_fk=False,
                is_charfield=False,
                create_related=True,
            ),
        )
        self.assertEqual(
            mapping["name"],
            _EsiFieldMapping(
                esi_name="name",
                is_optional=True,
                is_pk=False,
                is_fk=False,
                related_model=None,
                is_parent_fk=False,
                is_charfield=True,
                create_related=True,
            ),
        )
        self.assertEqual(
            mapping["published"],
            _EsiFieldMapping(
                esi_name="published",
                is_optional=False,
                is_pk=False,
                is_fk=False,
                related_model=None,
                is_parent_fk=False,
                is_charfield=False,
                create_related=True,
            ),
        )

    def test_with_fk(self):
        mapping = EveConstellation._esi_field_mappings()
        self.assertEqual(len(mapping.keys()), 6)
        self.assertEqual(
            mapping["id"],
            _EsiFieldMapping(
                esi_name="constellation_id",
                is_optional=False,
                is_pk=True,
                is_fk=False,
                related_model=None,
                is_parent_fk=False,
                is_charfield=False,
                create_related=True,
            ),
        )
        self.assertEqual(
            mapping["name"],
            _EsiFieldMapping(
                esi_name="name",
                is_optional=True,
                is_pk=False,
                is_fk=False,
                related_model=None,
                is_parent_fk=False,
                is_charfield=True,
                create_related=True,
            ),
        )
        self.assertEqual(
            mapping["eve_region"],
            _EsiFieldMapping(
                esi_name="region_id",
                is_optional=False,
                is_pk=False,
                is_fk=True,
                related_model=EveRegion,
                is_parent_fk=False,
                is_charfield=False,
                create_related=True,
            ),
        )
        self.assertEqual(
            mapping["position_x"],
            _EsiFieldMapping(
                esi_name=("position", "x"),
                is_optional=True,
                is_pk=False,
                is_fk=False,
                related_model=None,
                is_parent_fk=False,
                is_charfield=False,
                create_related=True,
            ),
        )
        self.assertEqual(
            mapping["position_y"],
            _EsiFieldMapping(
                esi_name=("position", "y"),
                is_optional=True,
                is_pk=False,
                is_fk=False,
                related_model=None,
                is_parent_fk=False,
                is_charfield=False,
                create_related=True,
            ),
        )
        self.assertEqual(
            mapping["position_z"],
            _EsiFieldMapping(
                esi_name=("position", "z"),
                is_optional=True,
                is_pk=False,
                is_fk=False,
                related_model=None,
                is_parent_fk=False,
                is_charfield=False,
                create_related=True,
            ),
        )

    def test_optional_fields(self):
        mapping = EveAncestry._esi_field_mappings()
        self.assertEqual(len(mapping.keys()), 6)
        self.assertEqual(
            mapping["id"],
            _EsiFieldMapping(
                esi_name="id",
                is_optional=False,
                is_pk=True,
                is_fk=False,
                related_model=None,
                is_parent_fk=False,
                is_charfield=False,
                create_related=True,
            ),
        )
        self.assertEqual(
            mapping["name"],
            _EsiFieldMapping(
                esi_name="name",
                is_optional=True,
                is_pk=False,
                is_fk=False,
                related_model=None,
                is_parent_fk=False,
                is_charfield=True,
                create_related=True,
            ),
        )
        self.assertEqual(
            mapping["eve_bloodline"],
            _EsiFieldMapping(
                esi_name="bloodline_id",
                is_optional=False,
                is_pk=False,
                is_fk=True,
                related_model=EveBloodline,
                is_parent_fk=False,
                is_charfield=False,
                create_related=True,
            ),
        )
        self.assertEqual(
            mapping["description"],
            _EsiFieldMapping(
                esi_name="description",
                is_optional=False,
                is_pk=False,
                is_fk=False,
                related_model=None,
                is_parent_fk=False,
                is_charfield=True,
                create_related=True,
            ),
        )
        self.assertEqual(
            mapping["icon_id"],
            _EsiFieldMapping(
                esi_name="icon_id",
                is_optional=True,
                is_pk=False,
                is_fk=False,
                related_model=None,
                is_parent_fk=False,
                is_charfield=False,
                create_related=True,
            ),
        )
        self.assertEqual(
            mapping["short_description"],
            _EsiFieldMapping(
                esi_name="short_description",
                is_optional=True,
                is_pk=False,
                is_fk=False,
                related_model=None,
                is_parent_fk=False,
                is_charfield=True,
                create_related=True,
            ),
        )

    def test_inline_model(self):
        mapping = EveTypeDogmaEffect._esi_field_mappings()
        self.assertEqual(len(mapping.keys()), 3)
        self.assertEqual(
            mapping["eve_type"],
            _EsiFieldMapping(
                esi_name="eve_type",
                is_optional=False,
                is_pk=True,
                is_fk=True,
                related_model=EveType,
                is_parent_fk=True,
                is_charfield=False,
                create_related=True,
            ),
        )
        self.assertEqual(
            mapping["eve_dogma_effect"],
            _EsiFieldMapping(
                esi_name="effect_id",
                is_optional=False,
                is_pk=True,
                is_fk=True,
                related_model=EveDogmaEffect,
                is_parent_fk=False,
                is_charfield=False,
                create_related=True,
            ),
        )
        self.assertEqual(
            mapping["is_default"],
            _EsiFieldMapping(
                esi_name="is_default",
                is_optional=False,
                is_pk=False,
                is_fk=False,
                related_model=None,
                is_parent_fk=False,
                is_charfield=False,
                create_related=True,
            ),
        )

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", True)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", True)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", True)
    def test_esi_field_mapping(self):
        mapping = EveType._esi_field_mappings()
        self.assertSetEqual(
            set(mapping.keys()),
            {
                "id",
                "name",
                "description",
                "capacity",
                "eve_group",
                "eve_graphic",
                "icon_id",
                "eve_market_group",
                "mass",
                "packaged_volume",
                "portion_size",
                "radius",
                "published",
                "volume",
            },
        )


class TestDetermineEnabledSections(TestCase):
    def test_should_return_empty_1(self):
        # when
        with (
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_ASTEROID_BELTS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_PLANETS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARGATES", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STATIONS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False),
        ):
            result = determine_effective_sections()
        # then
        self.assertSetEqual(result, set())

    def test_should_return_empty_2(self):
        # when
        with (
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_ASTEROID_BELTS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_PLANETS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARGATES", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STATIONS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False),
        ):
            result = determine_effective_sections(None)
        # then
        self.assertSetEqual(result, set())

    def test_should_return_global_section(self):
        # when
        with (
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_ASTEROID_BELTS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", True),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_PLANETS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARGATES", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STATIONS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False),
        ):
            result = determine_effective_sections()
        # then
        self.assertSetEqual(result, {EveType.Section.DOGMAS})

    def test_should_combine_global_and_local_sections(self):
        # when
        with (
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_ASTEROID_BELTS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", True),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_PLANETS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARGATES", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STATIONS", False),
            patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False),
        ):
            result = determine_effective_sections(["type_materials"])
        # then
        self.assertSetEqual(
            result, {EveType.Section.DOGMAS, EveType.Section.TYPE_MATERIALS}
        )
