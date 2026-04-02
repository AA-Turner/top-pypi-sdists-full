import unittest
from unittest.mock import patch

from django.test.utils import override_settings

from eveuniverse.constants import EveCategoryId
from eveuniverse.models import (
    EveAncestry,
    EveBloodline,
    EveCategory,
    EveConstellation,
    EveDogmaAttribute,
    EveDogmaEffect,
    EveEntity,
    EveGraphic,
    EveGroup,
    EveMarketGroup,
    EveRegion,
    EveType,
    EveTypeDogmaEffect,
    EveUnit,
)
from eveuniverse.models.base import _EsiFieldMapping, determine_effective_sections
from eveuniverse.utils import NoSocketsTestCase

from ..testdata.esi import EsiClientStub

unittest.util._MAX_LENGTH = 1000
MODELS_PATH = "eveuniverse.models"
MANAGERS_PATH = "eveuniverse.managers.universe"


@patch(MANAGERS_PATH + ".esi")
class TestEveType(NoSocketsTestCase):
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    def test_can_create_type_from_esi_excluding_all(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveType.objects.get_or_create_esi(id=603)
        self.assertTrue(created)
        self.assertEqual(obj.id, 603)
        self.assertEqual(obj.name, "Merlin")
        self.assertEqual(
            obj.description,
            """The Merlin is the most powerful combat frigate of the Caldari. Its role has evolved through the years, and while its defenses have always remained exceptionally strong for a Caldari vessel, its offensive capabilities have evolved from versatile, jack-of-all-trades attack patterns into focused and deadly gunfire tactics. The Merlin's primary aim is to have its turrets punch holes in opponents' hulls.""",
        )
        self.assertEqual(obj.capacity, 150)
        self.assertEqual(obj.eve_group, EveGroup.objects.get(id=25))
        self.assertEqual(obj.mass, 997000)
        self.assertEqual(obj.packaged_volume, 2500)
        self.assertEqual(obj.portion_size, 1)
        self.assertTrue(obj.published)
        self.assertEqual(obj.radius, 39)
        self.assertEqual(obj.volume, 16500)
        self.assertIsNone(obj.eve_graphic)
        self.assertIsNone(obj.eve_market_group)
        self.assertEqual(obj.dogma_attributes.count(), 0)
        self.assertEqual(obj.dogma_effects.count(), 0)
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_INVENTORY_TYPE)

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", True)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", True)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", True)
    def test_can_create_type_from_esi_including_dogmas(self, mock_esi):
        mock_esi.client = EsiClientStub()

        eve_type, created = EveType.objects.get_or_create_esi(id=603)
        self.assertTrue(created)
        self.assertEqual(eve_type.id, 603)
        self.assertEqual(eve_type.eve_graphic, EveGraphic.objects.get(id=314))
        self.assertEqual(eve_type.eve_market_group, EveMarketGroup.objects.get(id=61))

        dogma_attribute_1 = eve_type.dogma_attributes.filter(
            eve_dogma_attribute=EveDogmaAttribute.objects.get(id=588)
        ).first()
        self.assertEqual(dogma_attribute_1.value, 5)
        dogma_attribute_1 = eve_type.dogma_attributes.filter(
            eve_dogma_attribute=EveDogmaAttribute.objects.get(id=129)
        ).first()
        self.assertEqual(dogma_attribute_1.value, 12)

        dogma_effect_1 = eve_type.dogma_effects.filter(
            eve_dogma_effect=EveDogmaEffect.objects.get(id=1816)
        ).first()
        self.assertFalse(dogma_effect_1.is_default)
        dogma_effect_2 = eve_type.dogma_effects.filter(
            eve_dogma_effect=EveDogmaEffect.objects.get(id=1817)
        ).first()
        self.assertTrue(dogma_effect_2.is_default)

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", True)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
    def test_when_disabled_can_create_type_from_esi_excluding_dogmas(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveType.objects.get_or_create_esi(id=603)
        self.assertTrue(created)
        self.assertEqual(obj.id, 603)
        self.assertTrue(obj.eve_market_group, EveMarketGroup.objects.get(id=61))
        self.assertEqual(obj.dogma_attributes.count(), 0)
        self.assertEqual(obj.dogma_effects.count(), 0)

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", True)
    def test_when_disabled_can_create_type_from_esi_excluding_market_groups(
        self, mock_esi
    ):
        mock_esi.client = EsiClientStub()

        eve_type, created = EveType.objects.get_or_create_esi(id=603)
        self.assertTrue(created)
        self.assertEqual(eve_type.id, 603)
        self.assertIsNone(eve_type.eve_market_group)
        self.assertSetEqual(
            set(
                eve_type.dogma_attributes.values_list(
                    "eve_dogma_attribute_id", flat=True
                )
            ),
            {588, 129},
        )
        self.assertSetEqual(
            set(eve_type.dogma_effects.values_list("eve_dogma_effect_id", flat=True)),
            {1816, 1817},
        )

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    def test_can_create_type_from_esi_including_dogmas_when_disabled_1(self, mock_esi):
        mock_esi.client = EsiClientStub()

        eve_type, created = EveType.objects.update_or_create_esi(
            id=603, enabled_sections=[EveType.LOAD_DOGMAS]
        )
        self.assertTrue(created)
        self.assertEqual(eve_type.id, 603)
        self.assertSetEqual(
            set(
                eve_type.dogma_attributes.values_list(
                    "eve_dogma_attribute_id", flat=True
                )
            ),
            {588, 129},
        )
        self.assertSetEqual(
            set(eve_type.dogma_effects.values_list("eve_dogma_effect_id", flat=True)),
            {1816, 1817},
        )

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    def test_can_create_type_from_esi_including_dogmas_when_disabled_2(self, mock_esi):
        mock_esi.client = EsiClientStub()

        eve_type, created = EveType.objects.get_or_create_esi(
            id=603, enabled_sections=[EveType.LOAD_DOGMAS]
        )
        self.assertTrue(created)
        self.assertEqual(eve_type.id, 603)
        self.assertSetEqual(
            set(
                eve_type.dogma_attributes.values_list(
                    "eve_dogma_attribute_id", flat=True
                )
            ),
            {588, 129},
        )
        self.assertSetEqual(
            set(eve_type.dogma_effects.values_list("eve_dogma_effect_id", flat=True)),
            {1816, 1817},
        )

    @override_settings(
        CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True
    )
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    def test_can_create_type_from_esi_including_children_as_task(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        eve_type, created = EveType.objects.update_or_create_esi(
            id=603, wait_for_children=False, enabled_sections=[EveType.LOAD_DOGMAS]
        )
        # then
        self.assertTrue(created)
        self.assertEqual(eve_type.id, 603)
        self.assertSetEqual(
            set(
                eve_type.dogma_attributes.values_list(
                    "eve_dogma_attribute_id", flat=True
                )
            ),
            {588, 129},
        )
        self.assertSetEqual(
            set(eve_type.dogma_effects.values_list("eve_dogma_effect_id", flat=True)),
            {1816, 1817},
        )

    @override_settings(
        CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True
    )
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    def test_can_create_type_from_esi_including_children_as_task_with_priority(
        self, mock_esi
    ):
        # given
        mock_esi.client = EsiClientStub()
        # when
        eve_type, created = EveType.objects.update_or_create_esi(
            id=603,
            wait_for_children=False,
            enabled_sections=[EveType.LOAD_DOGMAS],
            task_priority=7,
        )
        # then
        self.assertTrue(created)
        self.assertEqual(eve_type.id, 603)
        self.assertSetEqual(
            set(
                eve_type.dogma_attributes.values_list(
                    "eve_dogma_attribute_id", flat=True
                )
            ),
            {588, 129},
        )
        self.assertSetEqual(
            set(eve_type.dogma_effects.values_list("eve_dogma_effect_id", flat=True)),
            {1816, 1817},
        )

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
    def test_can_create_render_url(self, mock_esi):
        mock_esi.client = EsiClientStub()

        eve_type, created = EveType.objects.get_or_create_esi(id=603)
        self.assertTrue(created)
        self.assertEqual(
            eve_type.render_url(256),
            "https://images.evetech.net/types/603/render?size=256",
        )


@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
@patch(MANAGERS_PATH + ".esi")
class TestEveTypeIconUrl(NoSocketsTestCase):
    def test_can_create_icon_url_1(self, mock_esi):
        """icon from regular type, automatically detected"""
        mock_esi.client = EsiClientStub()
        eve_type, _ = EveType.objects.get_or_create_esi(id=603)

        self.assertEqual(
            eve_type.icon_url(256), "https://images.evetech.net/types/603/icon?size=256"
        )

    def test_can_create_icon_url_2(self, mock_esi):
        """icon from blueprint type, automatically detected"""
        mock_esi.client = EsiClientStub()
        eve_type, _ = EveType.objects.get_or_create_esi(id=950)

        self.assertEqual(
            eve_type.icon_url(256), "https://images.evetech.net/types/950/bp?size=256"
        )

    def test_can_create_icon_url_3(self, mock_esi):
        """icon from regular type, preset as blueprint"""
        mock_esi.client = EsiClientStub()
        eve_type, _ = EveType.objects.get_or_create_esi(id=603)

        self.assertEqual(
            eve_type.icon_url(size=256, is_blueprint=True),
            "https://images.evetech.net/types/603/bp?size=256",
        )

    def test_can_create_icon_url_3a(self, mock_esi):
        """icon from regular type, preset as blueprint"""
        mock_esi.client = EsiClientStub()
        eve_type, _ = EveType.objects.get_or_create_esi(id=603)

        self.assertEqual(
            eve_type.icon_url(size=256, category_id=EveCategoryId.BLUEPRINT),
            "https://images.evetech.net/types/603/bp?size=256",
        )

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", False)
    def test_can_create_icon_url_5(self, mock_esi):
        """when called for SKIN type, will return dummy SKIN URL with requested size"""
        mock_esi.client = EsiClientStub()
        eve_type, _ = EveType.objects.get_or_create_esi(id=34599)

        self.assertIn("skin_generic_64.png", eve_type.icon_url(size=64))

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", False)
    def test_can_create_icon_url_5a(self, mock_esi):
        """when called for SKIN type, will return dummy SKIN URL with requested size"""
        mock_esi.client = EsiClientStub()
        eve_type, _ = EveType.objects.get_or_create_esi(id=34599)

        self.assertIn("skin_generic_32.png", eve_type.icon_url(size=32))

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", False)
    def test_can_create_icon_url_5b(self, mock_esi):
        """when called for SKIN type, will return dummy SKIN URL with requested size"""
        mock_esi.client = EsiClientStub()
        eve_type, _ = EveType.objects.get_or_create_esi(id=34599)

        self.assertIn("skin_generic_128.png", eve_type.icon_url(size=128))

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", False)
    def test_can_create_icon_url_5c(self, mock_esi):
        """when called for SKIN type and size is invalid, then raise exception"""
        mock_esi.client = EsiClientStub()
        eve_type, _ = EveType.objects.get_or_create_esi(id=34599)

        with self.assertRaises(ValueError):
            eve_type.icon_url(size=512)

        with self.assertRaises(ValueError):
            eve_type.icon_url(size=1024)

        with self.assertRaises(ValueError):
            eve_type.icon_url(size=31)

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", False)
    def test_can_create_icon_url_6(self, mock_esi):
        """when called for non SKIN type and SKIN is forced, then return SKIN URL"""
        mock_esi.client = EsiClientStub()
        eve_type, _ = EveType.objects.get_or_create_esi(id=950)

        self.assertIn(
            "skin_generic_128.png",
            eve_type.icon_url(size=128, category_id=EveCategoryId.SKIN),
        )

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", False)
    def test_can_create_icon_url_7(self, mock_esi):
        """when called for SKIN type and regular is forced, then return regular URL"""
        mock_esi.client = EsiClientStub()
        eve_type, _ = EveType.objects.get_or_create_esi(id=34599)

        self.assertEqual(
            eve_type.icon_url(size=256, category_id=EveCategoryId.STRUCTURE),
            "https://images.evetech.net/types/34599/icon?size=256",
        )

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", True)
    def test_can_create_icon_url_8(self, mock_esi):
        """
        when called for SKIN type and eveskinserver is enabled,
        then return corresponding eveskinserver URL
        """
        mock_esi.client = EsiClientStub()
        eve_type, _ = EveType.objects.get_or_create_esi(id=34599)

        self.assertEqual(
            eve_type.icon_url(size=256),
            "https://eveskinserver.kalkoken.net/skin/34599/icon?size=256",
        )

    @patch(MODELS_PATH + ".universe_1.EVEUNIVERSE_USE_EVESKINSERVER", True)
    def test_can_create_icon_url_9(self, mock_esi):
        """can use variants"""
        mock_esi.client = EsiClientStub()
        eve_type, _ = EveType.objects.get_or_create_esi(id=603)

        self.assertEqual(
            eve_type.icon_url(size=256, variant=EveType.IconVariant.REGULAR),
            "https://images.evetech.net/types/603/icon?size=256",
        )
        self.assertEqual(
            eve_type.icon_url(size=256, variant=EveType.IconVariant.BPO),
            "https://images.evetech.net/types/603/bp?size=256",
        )
        self.assertEqual(
            eve_type.icon_url(size=256, variant=EveType.IconVariant.BPC),
            "https://images.evetech.net/types/603/bpc?size=256",
        )
        self.assertEqual(
            eve_type.icon_url(size=256, variant=EveType.IconVariant.SKIN),
            "https://eveskinserver.kalkoken.net/skin/603/icon?size=256",
        )


@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
@patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False)
@patch(MANAGERS_PATH + ".esi")
class TestEveTypeProfileUrl(NoSocketsTestCase):
    def test_can_url(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        eve_type, _ = EveType.objects.get_or_create_esi(id=603)
        # when
        result = eve_type.profile_url
        # then
        self.assertEqual(result, "https://www.kalkoken.org/apps/eveitems/?typeId=603")


class TestEveUnit(NoSocketsTestCase):
    def test_get_object(self):
        obj = EveUnit.objects.get(id=10)
        self.assertEqual(obj.id, 10)
        self.assertEqual(obj.name, "Speed")


class TestEsiMapping(NoSocketsTestCase):
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

    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", True)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", True)
    @patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", True)
    def test_EveType_mapping(self):
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


class TestDetermineEnabledSections(NoSocketsTestCase):
    def test_should_return_empty_1(self):
        # when
        with patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_ASTEROID_BELTS", False), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False
        ), patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MOONS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_TYPE_MATERIALS", False
        ):
            result = determine_effective_sections()
        # then
        self.assertSetEqual(result, set())

    def test_should_return_empty_2(self):
        # when
        with patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_ASTEROID_BELTS", False), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", False
        ), patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MOONS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_TYPE_MATERIALS", False
        ):
            result = determine_effective_sections(None)
        # then
        self.assertSetEqual(result, set())

    def test_should_return_global_section(self):
        # when
        with patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_ASTEROID_BELTS", False), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", True
        ), patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MOONS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_TYPE_MATERIALS", False
        ):
            result = determine_effective_sections()
        # then
        self.assertSetEqual(result, {EveType.Section.DOGMAS})

    def test_should_combine_global_and_local_sections(self):
        # when
        with patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_ASTEROID_BELTS", False), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_DOGMAS", True
        ), patch(MODELS_PATH + ".base.EVEUNIVERSE_LOAD_GRAPHICS", False), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MARKET_GROUPS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_MOONS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_PLANETS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARGATES", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STARS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_STATIONS", False
        ), patch(
            MODELS_PATH + ".base.EVEUNIVERSE_LOAD_TYPE_MATERIALS", False
        ):
            result = determine_effective_sections(["type_materials"])
        # then
        self.assertSetEqual(
            result, {EveType.Section.DOGMAS, EveType.Section.TYPE_MATERIALS}
        )
