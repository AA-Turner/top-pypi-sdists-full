import datetime as dt
import unittest
from collections import namedtuple
from unittest.mock import Mock, patch

from bravado.exception import HTTPNotFound
from django.test.utils import override_settings
from django.utils.timezone import now

from eveuniverse.helpers import meters_to_ly
from eveuniverse.models import (
    EveAncestry,
    EveAsteroidBelt,
    EveBloodline,
    EveCategory,
    EveConstellation,
    EveDogmaAttribute,
    EveDogmaEffect,
    EveEntity,
    EveFaction,
    EveGraphic,
    EveGroup,
    EveMarketGroup,
    EveMarketPrice,
    EveMoon,
    EvePlanet,
    EveRace,
    EveRegion,
    EveSolarSystem,
    EveStar,
    EveStargate,
    EveStation,
    EveType,
)
from eveuniverse.tests.testdata.esi import BravadoOperationStub, EsiClientStub
from eveuniverse.tests.testdata.factories_2 import EveSolarSystemFactory
from eveuniverse.utils import NoSocketsTestCase

unittest.util._MAX_LENGTH = 1000
MODELS_PATH = "eveuniverse.models.base"
MANAGERS_PATH = "eveuniverse.managers.universe"


@patch(MANAGERS_PATH + ".esi")
class TestEveAncestry(NoSocketsTestCase):
    def test_create_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveAncestry.objects.update_or_create_esi(id=8)
        self.assertTrue(created)
        self.assertEqual(obj.id, 8)
        self.assertEqual(obj.name, "Mercs")
        self.assertEqual(obj.icon_id, 1648)
        self.assertEqual(obj.eve_bloodline, EveBloodline.objects.get(id=2))
        self.assertEqual(
            obj.short_description,
            "Guns for hire that are always available to the highest bidder.",
        )

    def test_raise_404_exception_when_object_not_found(self, mock_esi):
        mock_esi.client = EsiClientStub()

        with self.assertRaises(HTTPNotFound):
            EveAncestry.objects.update_or_create_esi(id=1)


@patch(MANAGERS_PATH + ".esi")
class TestEveAsteroidBelt(NoSocketsTestCase):
    def test_create_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveAsteroidBelt.objects.update_or_create_esi(id=40349487)
        self.assertTrue(created)
        self.assertEqual(obj.id, 40349487)
        self.assertEqual(obj.name, "Enaluri III - Asteroid Belt 1")
        self.assertEqual(obj.position_x, -214506997304.68906)
        self.assertEqual(obj.position_y, -41236109278.05316)
        self.assertEqual(obj.position_z, 219234300596.24887)
        self.assertEqual(obj.eve_planet, EvePlanet.objects.get(id=40349471))


@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", True)
@patch(MANAGERS_PATH + ".esi")
class TestEveCategory(NoSocketsTestCase):
    """These tests also cover the manager functionality shared among
    all entity models. (1/2)
    """

    def test_when_not_exists_load_object_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveCategory.objects.get_or_create_esi(id=6)
        self.assertTrue(created)
        self.assertEqual(obj.id, 6)
        self.assertEqual(obj.name, "Ship")
        self.assertTrue(obj.published)
        self.assertEqual(obj.eve_entity_category(), "")

    def test_when_exists_just_return_object(self, mock_esi):
        mock_esi.client = EsiClientStub()

        EveCategory.objects.update_or_create_esi(id=6)

        obj, created = EveCategory.objects.get_or_create_esi(id=6)
        self.assertFalse(created)
        self.assertEqual(obj.id, 6)
        self.assertEqual(obj.name, "Ship")
        self.assertTrue(obj.published)

    def test_when_exists_can_reload_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, _ = EveCategory.objects.update_or_create_esi(id=6)
        obj.name = "xxx"
        obj.save()

        obj, created = EveCategory.objects.update_or_create_esi(id=6)
        self.assertFalse(created)
        self.assertEqual(obj.id, 6)
        self.assertEqual(obj.name, "Ship")
        self.assertTrue(obj.published)

    def test_can_load_from_esi_including_children(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveCategory.objects.get_or_create_esi(
            id=6, include_children=True, wait_for_children=True
        )
        self.assertTrue(created)
        self.assertEqual(obj.id, 6)
        self.assertEqual(obj.name, "Ship")
        self.assertTrue(obj.published)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    def test_can_create_types_of_category_from_esi_including_dogmas_when_disabled(
        self, mock_esi
    ):
        mock_esi.client = EsiClientStub()

        EveCategory.objects.update_or_create_esi(
            id=6, include_children=True, enabled_sections=[EveType.LOAD_DOGMAS]
        )
        eve_type = EveType.objects.get(id=603)
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


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
@patch(MANAGERS_PATH + ".esi")
class TestEveCategoryUpdateAll(NoSocketsTestCase):
    """These tests also cover the manager functionality shared among
    all entity models. (2/2)
    """

    def test_should_update_without_children_and_sync(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        EveCategory.objects.update_or_create_all_esi(
            include_children=False, wait_for_children=True
        )
        # then
        self.assertSetEqual(
            set(EveCategory.objects.values_list("id", flat=True)),
            {1, 2, 3, 4, 6, 9, 16, 17, 65, 91},
        )
        self.assertEqual(EveGroup.objects.count(), 0)
        self.assertEqual(EveType.objects.count(), 0)

    def test_should_update_without_children_and_sync_task_priority(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        EveCategory.objects.update_or_create_all_esi(
            include_children=False, wait_for_children=True, task_priority=7
        )
        # then
        self.assertSetEqual(
            set(EveCategory.objects.values_list("id", flat=True)),
            {1, 2, 3, 4, 6, 9, 16, 17, 65, 91},
        )
        self.assertEqual(EveGroup.objects.count(), 0)
        self.assertEqual(EveType.objects.count(), 0)

    def test_should_raise_exception_on_error(self, mock_esi):
        # given
        mock_esi.client.Universe.get_universe_categories.side_effect = OSError
        # when/then
        with self.assertRaises(OSError):
            EveCategory.objects.update_or_create_all_esi(
                include_children=False, wait_for_children=True
            )

    def test_should_update_with_children_and_sync(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        EveCategory.objects.update_or_create_all_esi(
            include_children=True, wait_for_children=True
        )
        # then
        self.assertSetEqual(
            set(EveCategory.objects.values_list("id", flat=True)),
            {1, 2, 3, 4, 6, 9, 16, 17, 65, 91},
        )
        self.assertSetEqual(
            set(EveGroup.objects.values_list("id", flat=True)),
            {1, 5, 6, 7, 8, 9, 10, 105, 15, 18, 536, 25, 26, 268, 1404, 1950},
        )
        self.assertSetEqual(
            set(EveType.objects.values_list("id", flat=True)),
            {
                13,
                14,
                15,
                16,
                34,
                35,
                36,
                37,
                38,
                39,
                40,
                34599,
                950,
                21947,
                29627,
                21949,
                21951,
                21953,
                21955,
                21957,
                21959,
                21961,
                21967,
                3800,
                603,
                608,
                2016,
                621,
                45038,
                35825,
                626,
                1529,
                1376,
                5,
                52678,
                3380,
            },
        )

    def test_should_update_with_children_and_async(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        # when
        EveCategory.objects.update_or_create_all_esi(
            include_children=True, wait_for_children=False, task_priority=7
        )
        # then
        self.assertSetEqual(
            set(EveCategory.objects.values_list("id", flat=True)),
            {1, 2, 3, 4, 6, 9, 16, 17, 65, 91},
        )
        self.assertSetEqual(
            set(EveGroup.objects.values_list("id", flat=True)),
            {1, 5, 6, 7, 8, 9, 10, 105, 15, 18, 536, 25, 26, 268, 1404, 1950},
        )
        self.assertSetEqual(
            set(EveType.objects.values_list("id", flat=True)),
            {
                5,
                13,
                14,
                15,
                16,
                34,
                35,
                36,
                37,
                38,
                39,
                40,
                950,
                1376,
                34599,
                21947,
                29627,
                21949,
                21951,
                21953,
                21955,
                21957,
                21959,
                21961,
                21967,
                3800,
                603,
                608,
                2016,
                621,
                45038,
                35825,
                626,
                1529,
                52678,
                3380,
            },
        )


@patch(MANAGERS_PATH + ".esi")
class TestBulkGetOrCreateEsi(NoSocketsTestCase):
    def test_can_load_all_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        result = EveCategory.objects.bulk_get_or_create_esi(ids=[2, 3])
        self.assertEqual({x.id for x in result}, {2, 3})

    def test_can_load_parts_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        EveCategory.objects.get_or_create_esi(id=2)
        result = EveCategory.objects.bulk_get_or_create_esi(ids=[2, 3])
        self.assertEqual({x.id for x in result}, {2, 3})


@patch(MANAGERS_PATH + ".esi")
class TestEveConstellation(NoSocketsTestCase):
    def test_create_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveConstellation.objects.update_or_create_esi(id=20000785)
        self.assertTrue(created)
        self.assertEqual(obj.id, 20000785)
        self.assertEqual(obj.name, "Ishaga")
        self.assertEqual(obj.position_x, -222687068034733630)
        self.assertEqual(obj.position_y, 108368351346494510)
        self.assertEqual(obj.position_z, 136029596082308480)
        self.assertEqual(obj.eve_region, EveRegion.objects.get(id=10000069))
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_CONSTELLATION)


@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", True)
@patch(MANAGERS_PATH + ".esi")
class TestEveDogmaAttribute(NoSocketsTestCase):
    def test_can_create_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveDogmaAttribute.objects.update_or_create_esi(id=271)
        self.assertTrue(created)
        self.assertEqual(obj.id, 271)
        self.assertEqual(obj.name, "shieldEmDamageResonance")
        self.assertEqual(obj.default_value, 1)
        self.assertEqual(obj.description, "Multiplies EM damage taken by shield")
        self.assertEqual(obj.display_name, "Shield EM Damage Resistance")
        self.assertEqual(obj.icon_id, 1396)
        self.assertTrue(obj.published)
        self.assertEqual(obj.eve_unit_id, 108)


@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", True)
@patch(MANAGERS_PATH + ".esi")
class TestEveDogmaEffect(NoSocketsTestCase):
    def test_can_create_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveDogmaEffect.objects.update_or_create_esi(id=1816)
        self.assertTrue(created)
        self.assertEqual(obj.id, 1816)
        self.assertEqual(obj.name, "shipShieldEMResistanceCF2")
        self.assertEqual(obj.display_name, "")
        self.assertEqual(obj.effect_category, 0)
        self.assertEqual(obj.icon_id, 0)
        modifiers = obj.modifiers.first()
        self.assertEqual(modifiers.domain, "shipID")
        self.assertEqual(modifiers.func, "ItemModifier")
        self.assertEqual(
            modifiers.modified_attribute, EveDogmaAttribute.objects.get(id=271)
        )
        self.assertEqual(
            modifiers.modifying_attribute,
            EveDogmaAttribute.objects.get(id=463),
        )
        self.assertEqual(modifiers.operator, 6)

    def test_repr(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, _ = EveDogmaEffect.objects.update_or_create_esi(id=1816)
        self.assertEqual(
            repr(obj),
            "EveDogmaEffect(description='', disallow_auto_repeat=None, discharge_attribute_id=None, display_name='', duration_attribute_id=None, effect_category=0, electronic_chance=None, falloff_attribute_id=None, icon_id=0, id=1816, is_assistance=None, is_offensive=None, is_warp_safe=None, name='shipShieldEMResistanceCF2', post_expression=None, pre_expression=None, published=None, range_attribute_id=None, range_chance=None, tracking_speed_attribute_id=None)",
        )
        modifier = obj.modifiers.first()
        self.assertEqual(
            repr(modifier),
            f"EveDogmaEffectModifier(domain='shipID', eve_dogma_effect_id=1816, func='ItemModifier', id={modifier.id}, modified_attribute_id=271, modifying_attribute_id=463, modifying_effect_id=None, operator=6)",
        )


@patch(MANAGERS_PATH + ".esi")
class TestEveFaction(NoSocketsTestCase):
    def test_can_create_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveFaction.objects.update_or_create_esi(id=500001)
        self.assertTrue(created)
        self.assertEqual(obj.id, 500001)
        self.assertEqual(obj.name, "Caldari State")
        self.assertTrue(obj.is_unique)
        self.assertEqual(obj.militia_corporation_id, 1000180)
        self.assertEqual(obj.eve_solar_system, EveSolarSystem.objects.get(id=30045339))
        self.assertEqual(obj.size_factor, 5)
        self.assertEqual(obj.station_count, 1503)
        self.assertEqual(obj.station_system_count, 503)
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_FACTION)


@patch(MANAGERS_PATH + ".esi")
class TestEveGraphic(NoSocketsTestCase):
    def test_create_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveGraphic.objects.update_or_create_esi(id=314)
        self.assertTrue(created)
        self.assertEqual(obj.id, 314)
        self.assertEqual(obj.sof_dna, "cf7_t1:caldaribase:caldari")
        self.assertEqual(obj.sof_fation_name, "caldaribase")
        self.assertEqual(obj.sof_hull_name, "cf7_t1")
        self.assertEqual(obj.sof_race_name, "caldari")


@patch(MANAGERS_PATH + ".esi")
class TestEveGroup(NoSocketsTestCase):
    def test_can_create_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveGroup.objects.update_or_create_esi(id=10)
        self.assertTrue(created)
        self.assertEqual(obj.id, 10)
        self.assertEqual(obj.name, "Stargate")
        self.assertFalse(obj.published)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
    def test_can_create_types_of_group_from_esi_including_dogmas_when_disabled(
        self, mock_esi
    ):
        mock_esi.client = EsiClientStub()

        EveGroup.objects.update_or_create_esi(
            id=25, include_children=True, enabled_sections=[EveType.LOAD_DOGMAS]
        )
        eve_type = EveType.objects.get(id=603)
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


@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", True)
@patch(MANAGERS_PATH + ".esi")
class TestEveMarketGroup(NoSocketsTestCase):
    def test_can_fetch_parent_group(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveMarketGroup.objects.get_or_create_esi(id=4)
        self.assertTrue(created)
        self.assertEqual(obj.name, "Ships")

    def test_can_fetch_group_and_all_parents(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveMarketGroup.objects.get_or_create_esi(id=61)
        self.assertTrue(created)
        self.assertEqual(obj.name, "Caldari")
        self.assertEqual(obj.parent_market_group.name, "Standard Frigates")
        self.assertEqual(obj.parent_market_group.parent_market_group.name, "Frigates")
        self.assertEqual(
            obj.parent_market_group.parent_market_group.parent_market_group.name,
            "Ships",
        )


@patch(MANAGERS_PATH + ".esi")
class TestEveMarketPriceManager(NoSocketsTestCase):
    def test_add_new_prices_from_esi_but_for_existing_types_only(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        merlin, _ = EveType.objects.get_or_create_esi(id=603)

        # when
        result = EveMarketPrice.objects.update_from_esi()

        # then
        self.assertEqual(result, 1)
        self.assertEqual(EveMarketPrice.objects.count(), 1)
        merlin.refresh_from_db()
        self.assertEqual(float(merlin.market_price.adjusted_price), 306988.09)
        self.assertEqual(float(merlin.market_price.average_price), 306292.67)

    def test_should_not_update_prices_which_are_not_stale_1(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        merlin, _ = EveType.objects.get_or_create_esi(id=603)
        EveMarketPrice.objects.create(
            eve_type=merlin, adjusted_price=2, average_price=3
        )

        # when
        result = EveMarketPrice.objects.update_from_esi()

        # then
        self.assertEqual(result, 0)
        self.assertEqual(EveMarketPrice.objects.count(), 1)
        merlin.refresh_from_db()
        self.assertEqual(float(merlin.market_price.adjusted_price), 2)
        self.assertEqual(float(merlin.market_price.average_price), 3)

    def test_should_not_update_prices_which_are_not_stale_2(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        merlin, _ = EveType.objects.get_or_create_esi(id=603)
        mocked_update_at = now() - dt.timedelta(minutes=60)
        with patch("django.utils.timezone.now", Mock(return_value=mocked_update_at)):
            EveMarketPrice.objects.create(
                eve_type=merlin, adjusted_price=2, average_price=3
            )

        # when
        result = EveMarketPrice.objects.update_from_esi(minutes_until_stale=65)

        # then
        self.assertEqual(result, 0)
        self.assertEqual(EveMarketPrice.objects.count(), 1)
        merlin.refresh_from_db()
        self.assertEqual(float(merlin.market_price.adjusted_price), 2)
        self.assertEqual(float(merlin.market_price.average_price), 3)

    def test_should_update_stale_prices(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        merlin, _ = EveType.objects.get_or_create_esi(id=603)
        mocked_update_at = now() - dt.timedelta(minutes=65)
        with patch("django.utils.timezone.now", Mock(return_value=mocked_update_at)):
            EveMarketPrice.objects.create(
                eve_type=merlin, adjusted_price=2, average_price=3
            )

        # when
        result = EveMarketPrice.objects.update_from_esi(minutes_until_stale=60)

        # then
        self.assertEqual(result, 1)
        self.assertEqual(EveMarketPrice.objects.count(), 1)
        merlin.refresh_from_db()
        self.assertEqual(float(merlin.market_price.adjusted_price), 306988.09)
        self.assertEqual(float(merlin.market_price.average_price), 306292.67)

    def test_should_remove_obsolete_prices(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        merlin, _ = EveType.objects.get_or_create_esi(id=603)
        EveMarketPrice.objects.create(
            eve_type=merlin, adjusted_price=2, average_price=3
        )
        atron, _ = EveType.objects.get_or_create_esi(id=608)
        atron_prices = EveMarketPrice.objects.create(
            eve_type=atron, adjusted_price=2, average_price=3
        )

        # when
        result = EveMarketPrice.objects.update_from_esi()

        # then
        self.assertEqual(result, 0)
        self.assertEqual(EveMarketPrice.objects.count(), 1)
        merlin.refresh_from_db()
        self.assertTrue(merlin.market_price.adjusted_price)
        self.assertTrue(merlin.market_price.average_price)
        self.assertFalse(EveMarketPrice.objects.filter(pk=atron_prices.pk).exists())


@patch(MANAGERS_PATH + ".esi")
class TestEveMoon(NoSocketsTestCase):
    def test_create_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveMoon.objects.update_or_create_esi(id=40349468)
        self.assertTrue(created)
        self.assertEqual(obj.id, 40349468)
        self.assertEqual(obj.name, "Enaluri I - Moon 1")
        self.assertEqual(obj.position_x, -79612836383.01112)
        self.assertEqual(obj.position_y, -1951529197.9895465)
        self.assertEqual(obj.position_z, 48035834113.70182)
        self.assertEqual(obj.eve_planet, EvePlanet.objects.get(id=40349467))


@patch(MANAGERS_PATH + ".esi")
class TestEvePlanet(NoSocketsTestCase):
    def test_create_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EvePlanet.objects.update_or_create_esi(id=40349467)
        self.assertTrue(created)
        self.assertEqual(obj.id, 40349467)
        self.assertEqual(obj.name, "Enaluri I")
        self.assertEqual(obj.position_x, -79928787523.97133)
        self.assertEqual(obj.position_y, -1951674993.3224173)
        self.assertEqual(obj.position_z, 48099232021.23506)
        self.assertEqual(obj.eve_type, EveType.objects.get(id=2016))
        self.assertEqual(obj.eve_solar_system, EveSolarSystem.objects.get(id=30045339))

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_ASTEROID_BELTS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", True)
    def test_create_from_esi_with_children_1(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EvePlanet.objects.update_or_create_esi(
            id=40349467,
            include_children=True,
        )
        self.assertTrue(created)
        self.assertEqual(obj.id, 40349467)
        self.assertEqual(obj.name, "Enaluri I")
        self.assertEqual(obj.position_x, -79928787523.97133)
        self.assertEqual(obj.position_y, -1951674993.3224173)
        self.assertEqual(obj.position_z, 48099232021.23506)
        self.assertEqual(obj.eve_type, EveType.objects.get(id=2016))
        self.assertEqual(obj.eve_solar_system, EveSolarSystem.objects.get(id=30045339))
        self.assertTrue(EveMoon.objects.filter(id=40349468).exists())

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_ASTEROID_BELTS", True)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", True)
    def test_create_from_esi_with_children_2(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EvePlanet.objects.update_or_create_esi(
            id=40349471, include_children=True
        )
        self.assertTrue(created)
        self.assertEqual(obj.id, 40349471)
        self.assertEqual(obj.name, "Enaluri III")
        self.assertEqual(obj.eve_type, EveType.objects.get(id=13))
        self.assertEqual(obj.eve_solar_system, EveSolarSystem.objects.get(id=30045339))

        self.assertTrue(EveAsteroidBelt.objects.filter(id=40349487).exists())
        self.assertTrue(EveMoon.objects.filter(id=40349472).exists())
        self.assertTrue(EveMoon.objects.filter(id=40349473).exists())

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_ASTEROID_BELTS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", False)
    def test_create_from_esi_with_children_2_when_disabled(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EvePlanet.objects.update_or_create_esi(
            id=40349471,
            include_children=True,
        )
        self.assertTrue(created)
        self.assertEqual(obj.id, 40349471)
        self.assertEqual(obj.name, "Enaluri III")
        self.assertEqual(obj.eve_type, EveType.objects.get(id=13))
        self.assertEqual(obj.eve_solar_system, EveSolarSystem.objects.get(id=30045339))

        self.assertFalse(EveAsteroidBelt.objects.filter(id=40349487).exists())
        self.assertFalse(EveMoon.objects.filter(id=40349472).exists())
        self.assertFalse(EveMoon.objects.filter(id=40349473).exists())

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", True)
    def test_does_not_update_children_on_get_by_default(self, mock_esi):
        mock_esi.client = EsiClientStub()

        # create scenario
        obj, created = EvePlanet.objects.update_or_create_esi(
            id=40349467,
            include_children=True,
        )
        self.assertTrue(created)
        self.assertEqual(obj.id, 40349467)
        self.assertEqual(obj.eve_type, EveType.objects.get(id=2016))
        self.assertEqual(obj.eve_solar_system, EveSolarSystem.objects.get(id=30045339))
        self.assertTrue(EveMoon.objects.filter(id=40349468).exists())
        moon = EveMoon.objects.get(id=40349468)
        moon.name = "Dummy"
        moon.save()

        # action
        EvePlanet.objects.get_or_create_esi(
            id=40349467,
            include_children=True,
        )

        # validate
        moon.refresh_from_db()
        self.assertEqual(moon.name, "Dummy")

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", True)
    def test_does_not_update_children_on_update(self, mock_esi):
        mock_esi.client = EsiClientStub()

        # create scenario
        obj, created = EvePlanet.objects.update_or_create_esi(
            id=40349467,
            include_children=True,
        )
        self.assertTrue(created)
        self.assertEqual(obj.id, 40349467)
        self.assertEqual(obj.eve_type, EveType.objects.get(id=2016))
        self.assertEqual(obj.eve_solar_system, EveSolarSystem.objects.get(id=30045339))
        self.assertTrue(EveMoon.objects.filter(id=40349468).exists())
        moon = EveMoon.objects.get(id=40349468)
        moon.name = "Dummy"
        moon.save()

        # action
        EvePlanet.objects.update_or_create_esi(id=40349467, include_children=True)

        # validate
        moon.refresh_from_db()
        self.assertNotEqual(moon.name, "Dummy")

    def test_can_return_planet_type_name(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        obj, _ = EvePlanet.objects.update_or_create_esi(id=40349467)
        # when/then
        self.assertEqual(obj.type_name(), "Barren")


@patch(MANAGERS_PATH + ".esi")
class TestEveRace(NoSocketsTestCase):
    def test_create_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveRace.objects.update_or_create_esi(id=1)
        self.assertTrue(created)
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.name, "Caldari")
        self.assertEqual(obj.alliance_id, 500001)

    def test_create_all_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        EveRace.objects.update_or_create_all_esi()
        self.assertTrue(EveRace.objects.filter(id=1).exists())
        self.assertTrue(EveRace.objects.filter(id=8).exists())


@patch(MANAGERS_PATH + ".esi")
class TestEveRegion(NoSocketsTestCase):
    def test_create_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveRegion.objects.update_or_create_esi(id=10000069)
        self.assertTrue(created)
        self.assertEqual(obj.id, 10000069)
        self.assertEqual(obj.name, "Black Rise")
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_REGION)

    def test_create_all_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        EveRegion.objects.update_or_create_all_esi()
        self.assertTrue(EveRegion.objects.filter(id=10000002).exists())
        self.assertTrue(EveRegion.objects.filter(id=10000069).exists())


@patch(MANAGERS_PATH + ".esi")
class TestEveSolarSystem(NoSocketsTestCase):
    maxDiff = None

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STATIONS", False)
    def test_create_from_esi_minimal(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveSolarSystem.objects.update_or_create_esi(id=30045339)
        self.assertTrue(created)
        self.assertEqual(obj.id, 30045339)
        self.assertEqual(obj.name, "Enaluri")
        self.assertEqual(
            obj.eve_constellation, EveConstellation.objects.get(id=20000785)
        )
        self.assertEqual(obj.position_x, -227875173313944580)
        self.assertEqual(obj.position_y, 104688385699531790)
        self.assertEqual(obj.position_z, 120279417692650270)
        self.assertEqual(obj.security_status, 0.3277980387210846)
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_SOLAR_SYSTEM)

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STATIONS", False)
    def test_repr(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, _ = EveSolarSystem.objects.update_or_create_esi(id=30045339)
        expected = "EveSolarSystem(enabled_sections=0, eve_constellation_id=20000785, eve_star_id=None, id=30045339, name='Enaluri', position_x=-227875173313944580, position_y=104688385699531790, position_z=120279417692650270, security_status=0.3277980387210846)"
        self.assertEqual(repr(obj), expected)

    def test_str(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, _ = EveSolarSystem.objects.update_or_create_esi(id=30045339)
        self.assertEqual(str(obj), "Enaluri")

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARS", True)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STATIONS", False)
    def test_create_from_esi_with_stars(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveSolarSystem.objects.update_or_create_esi(id=30045339)
        self.assertTrue(created)
        self.assertEqual(obj.id, 30045339)
        self.assertEqual(obj.eve_star, EveStar.objects.get(id=40349466))

    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_PLANETS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARGATES", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARS", False)
    @patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STATIONS", True)
    def test_create_from_esi_with_stations(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveSolarSystem.objects.update_or_create_esi(
            id=30045339, include_children=True
        )
        self.assertTrue(created)
        self.assertEqual(obj.id, 30045339)

        self.assertTrue(EveStation.objects.filter(id=60015068).exists())


"""
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARGATES", True)
@patch(MODELS_PATH + ".cache")
def test_can_calculate_route(self, mock_cache, mock_esi):
    def my_get_or_set(key, func, timeout):
        return func()

    mock_esi.client = EsiClientStub()
    mock_cache.get.return_value = None
    mock_cache.get_or_set.side_effect = my_get_or_set

    enaluri, _ = EveSolarSystem.objects.get_or_create_esi(
        id=30045339, include_children=True
    )
    akidagi, _ = EveSolarSystem.objects.get_or_create_esi(
        id=30045342, include_children=True
    )
    self.assertEqual(enaluri.jumps_to(akidagi), 1)
"""


@patch(MANAGERS_PATH + ".esi")
class TestEveSolarSystemsSpaceType(NoSocketsTestCase):
    def test_can_identify_highsec_system(self, mock_esi):
        mock_esi.client = EsiClientStub()

        jita, _ = EveSolarSystem.objects.get_or_create_esi(id=30000142)
        self.assertTrue(jita.is_high_sec)
        self.assertFalse(jita.is_low_sec)
        self.assertFalse(jita.is_null_sec)
        self.assertFalse(jita.is_w_space)
        self.assertFalse(jita.is_trig_space)
        self.assertFalse(jita.is_abyssal_deadspace)

    def test_can_identify_lowsec_system(self, mock_esi):
        mock_esi.client = EsiClientStub()

        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        self.assertTrue(enaluri.is_low_sec)
        self.assertFalse(enaluri.is_high_sec)
        self.assertFalse(enaluri.is_null_sec)
        self.assertFalse(enaluri.is_w_space)
        self.assertFalse(enaluri.is_trig_space)
        self.assertFalse(enaluri.is_abyssal_deadspace)

    def test_can_identify_nullsec_system(self, mock_esi):
        mock_esi.client = EsiClientStub()

        hed_gp, _ = EveSolarSystem.objects.get_or_create_esi(id=30001161)
        self.assertTrue(hed_gp.is_null_sec)
        self.assertFalse(hed_gp.is_low_sec)
        self.assertFalse(hed_gp.is_high_sec)
        self.assertFalse(hed_gp.is_w_space)
        self.assertFalse(hed_gp.is_trig_space)
        self.assertFalse(hed_gp.is_abyssal_deadspace)

    def test_can_identify_ws_system(self, mock_esi):
        mock_esi.client = EsiClientStub()

        thera, _ = EveSolarSystem.objects.get_or_create_esi(id=31000005)
        self.assertTrue(thera.is_w_space)
        self.assertFalse(thera.is_null_sec)
        self.assertFalse(thera.is_low_sec)
        self.assertFalse(thera.is_high_sec)
        self.assertFalse(thera.is_trig_space)
        self.assertFalse(thera.is_abyssal_deadspace)

    def test_can_identify_trig_system(self, mock_esi):
        mock_esi.client = EsiClientStub()

        otela, _ = EveSolarSystem.objects.get_or_create_esi(id=30000157)
        self.assertFalse(otela.is_w_space)
        self.assertFalse(otela.is_null_sec)
        self.assertFalse(otela.is_low_sec)
        self.assertFalse(otela.is_high_sec)
        self.assertTrue(otela.is_trig_space)
        self.assertFalse(otela.is_abyssal_deadspace)

    def test_can_identify_abyssal_deadspace(self, mock_esi):
        mock_esi.client = EsiClientStub()

        solar_system: EveSolarSystem = EveSolarSystem.objects.get_or_create_esi(
            id=32000018
        )[0]
        self.assertFalse(solar_system.is_w_space)
        self.assertFalse(solar_system.is_null_sec)
        self.assertFalse(solar_system.is_low_sec)
        self.assertFalse(solar_system.is_high_sec)
        self.assertFalse(solar_system.is_trig_space)
        self.assertTrue(solar_system.is_abyssal_deadspace)


class TestEveSolarSystemsSpaceType2(NoSocketsTestCase):
    def test_all(self):
        X = namedtuple(
            "X", ["name", "security_status", "is_high_sec", "is_low_sec", "is_null_sec"]
        )
        cases = [
            X("high sec normal", 1.0, True, False, False),
            X("low sec normal", 0.3, False, True, False),
            X("null sec normal", -0.3, False, False, True),
            X("low sec lower border", 0.049993, False, True, False),
            X("low sec upper border", 0.0449, False, True, False),
        ]
        for tc in cases:
            with self.subTest(name=tc.name):
                system = EveSolarSystemFactory(security_status=tc.security_status)
                self.assertIs(system.is_high_sec, tc.is_high_sec)
                self.assertIs(system.is_low_sec, tc.is_low_sec)
                self.assertIs(system.is_null_sec, tc.is_null_sec)


@patch(MANAGERS_PATH + ".esi")
class TestEveSolarSystemDistanceTo(NoSocketsTestCase):
    def test_should_calculate_distance_between_normal_systems(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        abune, _ = EveSolarSystem.objects.get_or_create_esi(id=30004984)
        # when
        result = enaluri.distance_to(abune)
        # then
        self.assertEqual(round(meters_to_ly(result), 3), 6.831)

    def test_should_return_none_when_one_system_in_wh_space_1(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        thera, _ = EveSolarSystem.objects.get_or_create_esi(id=31000005)
        # when
        result = enaluri.distance_to(thera)
        # then
        self.assertIsNone(result)

    def test_should_return_none_when_one_system_in_wh_space_2(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        thera, _ = EveSolarSystem.objects.get_or_create_esi(id=31000005)
        # when
        result = thera.distance_to(enaluri)
        # then
        self.assertIsNone(result)

    def test_should_return_none_when_no_destination(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        # when
        result = enaluri.distance_to(None)
        # then
        self.assertIsNone(result)

    def test_should_return_none_when_origin_has_not_coordinates(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        enaluri.position_x = None
        enaluri.position_y = None
        enaluri.position_z = None
        akidagi, _ = EveSolarSystem.objects.get_or_create_esi(id=30045342)
        # when
        result = enaluri.distance_to(akidagi)
        # then
        self.assertIsNone(result)

    def test_should_return_none_when_destination_has_not_coordinates(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        enaluri.position_x = None
        enaluri.position_y = None
        enaluri.position_z = None
        akidagi, _ = EveSolarSystem.objects.get_or_create_esi(id=30045342)
        # when
        result = akidagi.distance_to(enaluri)
        # then
        self.assertIsNone(result)

    def test_should_return_none_when_one_system_is_in_trig_space_1(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        otela, _ = EveSolarSystem.objects.get_or_create_esi(id=30000157)
        # when
        result = enaluri.distance_to(otela)
        # then
        self.assertIsNone(result)

    def test_should_return_none_when_one_system_is_in_trig_space_2(self, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        otela, _ = EveSolarSystem.objects.get_or_create_esi(id=30000157)
        # when
        result = otela.distance_to(enaluri)
        # then
        self.assertIsNone(result)


@patch(MANAGERS_PATH + ".esi")
@patch("eveuniverse.models.universe_2.esi")
class TestEveSolarSystemJumpsTo(NoSocketsTestCase):
    def test_can_calculate_jumps(self, mock_esi_2, mock_esi_1):
        # given
        mock_esi_1.client = EsiClientStub()
        mock_esi_2.client.Routes.get_route_origin_destination.return_value = (
            BravadoOperationStub([30045339, 30045342])
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        akidagi, _ = EveSolarSystem.objects.get_or_create_esi(id=30045342)
        # when/then
        self.assertEqual(enaluri.jumps_to(akidagi), 1)

    def test_route_calc_returns_none_if_no_route_found(self, mock_esi_2, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        mock_esi_2.client.Routes.get_route_origin_destination.side_effect = (
            HTTPNotFound(Mock(**{"response.status_code": 404}))
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        jita, _ = EveSolarSystem.objects.get_or_create_esi(id=30000142)
        # when/then
        self.assertIsNone(enaluri.jumps_to(jita))

    def test_should_return_none_if_any_system_is_in_wh_space_1(
        self, mock_esi_2, mock_esi_1
    ):
        # given
        mock_esi_1.client = EsiClientStub()
        mock_esi_2.client.Routes.get_route_origin_destination.return_value = (
            BravadoOperationStub([30045339, 30045342])
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        thera, _ = EveSolarSystem.objects.get_or_create_esi(id=31000005)
        # when/then
        self.assertIsNone(enaluri.jumps_to(thera))

    def test_should_return_none_if_any_system_is_in_wh_space_2(
        self, mock_esi_2, mock_esi_1
    ):
        # given
        mock_esi_1.client = EsiClientStub()
        mock_esi_2.client.Routes.get_route_origin_destination.return_value = (
            BravadoOperationStub([30045339, 30045342])
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        thera, _ = EveSolarSystem.objects.get_or_create_esi(id=31000005)
        # when/then
        self.assertIsNone(thera.jumps_to(enaluri))

    def test_should_return_none_if_any_system_is_in_trig_space_1(
        self, mock_esi_2, mock_esi_1
    ):
        # given
        mock_esi_1.client = EsiClientStub()
        mock_esi_2.client.Routes.get_route_origin_destination.return_value = (
            BravadoOperationStub([30045339, 30045342])
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        otela, _ = EveSolarSystem.objects.get_or_create_esi(id=30000157)
        # when/then
        self.assertIsNone(enaluri.jumps_to(otela))

    def test_should_return_none_if_any_system_is_in_trig_space_2(
        self, mock_esi_2, mock_esi_1
    ):
        # given
        mock_esi_1.client = EsiClientStub()
        mock_esi_2.client.Routes.get_route_origin_destination.return_value = (
            BravadoOperationStub([30045339, 30045342])
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        otela, _ = EveSolarSystem.objects.get_or_create_esi(id=30000157)
        # when/then
        self.assertIsNone(otela.jumps_to(enaluri))


@patch("eveuniverse.models.universe_2.esi")
@patch(MANAGERS_PATH + ".esi")
class TestEveSolarSystemRouteTo(NoSocketsTestCase):
    def test_should_return_valid_route(self, mock_esi_1, mock_esi_2):
        # given
        mock_esi_1.client = EsiClientStub()
        mock_esi_2.client.Routes.get_route_origin_destination.return_value = (
            BravadoOperationStub([30045339, 30045342])
        )
        enaluri: EveSolarSystem = EveSolarSystem.objects.get_or_create_esi(id=30045339)[
            0
        ]
        akidagi: EveSolarSystem = EveSolarSystem.objects.get_or_create_esi(id=30045342)[
            0
        ]
        # when
        result = enaluri.route_to(akidagi)
        # then
        self.assertListEqual(result, [(enaluri, False), (akidagi, False)])

    def test_should_return_none_when_no_route_found(self, mock_esi_1, mock_esi_2):
        # given
        mock_esi_1.client = EsiClientStub()
        mock_esi_2.client.Routes.get_route_origin_destination.side_effect = (
            HTTPNotFound(Mock(**{"response.status_code": 404}))
        )
        enaluri: EveSolarSystem = EveSolarSystem.objects.get_or_create_esi(id=30045339)[
            0
        ]
        akidagi: EveSolarSystem = EveSolarSystem.objects.get_or_create_esi(id=30045342)[
            0
        ]
        # when
        result = enaluri.route_to(akidagi)
        # then
        self.assertIsNone(result)

    def test_should_return_none_if_any_system_is_in_wh_space_1(
        self, mock_esi_1, mock_esi_2
    ):
        # given
        mock_esi_1.client = EsiClientStub()
        mock_esi_2.client.Routes.get_route_origin_destination.return_value = (
            BravadoOperationStub([30045339, 30045342])
        )
        enaluri: EveSolarSystem = EveSolarSystem.objects.get_or_create_esi(id=30045339)[
            0
        ]
        thera: EveSolarSystem = EveSolarSystem.objects.get_or_create_esi(id=31000005)[0]
        # when
        result = enaluri.route_to(thera)
        # then
        self.assertIsNone(result)

    def test_should_return_none_if_any_system_is_in_wh_space_2(
        self, mock_esi_1, mock_esi_2
    ):
        # given
        mock_esi_1.client = EsiClientStub()
        mock_esi_2.client.Routes.get_route_origin_destination.return_value = (
            BravadoOperationStub([30045339, 30045342])
        )
        enaluri: EveSolarSystem = EveSolarSystem.objects.get_or_create_esi(id=30045339)[
            0
        ]
        thera: EveSolarSystem = EveSolarSystem.objects.get_or_create_esi(id=31000005)[0]
        # when
        result = thera.route_to(enaluri)
        # then
        self.assertIsNone(result)

    def test_should_return_none_if_any_system_is_in_trig_space_1(
        self, mock_esi_1, mock_esi_2
    ):
        # given
        mock_esi_1.client = EsiClientStub()
        mock_esi_2.client.Routes.get_route_origin_destination.return_value = (
            BravadoOperationStub([30045339, 30045342])
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        otela, _ = EveSolarSystem.objects.get_or_create_esi(id=30000157)
        # when
        result = otela.route_to(enaluri)
        # then
        self.assertIsNone(result)

    def test_should_return_none_if_any_system_is_in_trig_space_2(
        self, mock_esi_1, mock_esi_2
    ):
        # given
        mock_esi_1.client = EsiClientStub()
        mock_esi_2.client.Routes.get_route_origin_destination.return_value = (
            BravadoOperationStub([30045339, 30045342])
        )
        enaluri, _ = EveSolarSystem.objects.get_or_create_esi(id=30045339)
        otela, _ = EveSolarSystem.objects.get_or_create_esi(id=30000157)
        # when
        result = enaluri.route_to(otela)
        # then
        self.assertIsNone(result)


@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
@patch(MANAGERS_PATH + ".esi")
class TestEveStar(NoSocketsTestCase):
    def test_create_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveStar.objects.update_or_create_esi(id=40349466)
        self.assertTrue(created)
        self.assertEqual(obj.id, 40349466)
        self.assertEqual(obj.name, "Enaluri - Star")
        self.assertEqual(obj.luminosity, 0.02542000077664852)
        self.assertEqual(obj.radius, 590000000)
        self.assertEqual(obj.spectral_class, "M6 V")
        self.assertEqual(obj.temperature, 2385)
        self.assertEqual(obj.eve_type, EveType.objects.get(id=3800))


@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STARGATES", True)
@patch(MANAGERS_PATH + ".esi")
class TestEveStargate(NoSocketsTestCase):
    def test_create_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveStargate.objects.get_or_create_esi(id=50016284)
        self.assertTrue(created)
        self.assertEqual(obj.id, 50016284)
        self.assertEqual(obj.name, "Stargate (Akidagi)")
        self.assertEqual(obj.position_x, 4845263708160)
        self.assertEqual(obj.position_y, 97343692800)
        self.assertEqual(obj.position_z, 3689037127680)
        self.assertEqual(obj.eve_solar_system, EveSolarSystem.objects.get(id=30045339))
        self.assertEqual(obj.eve_type, EveType.objects.get(id=16))
        self.assertIsNone(obj.destination_eve_stargate)
        self.assertIsNone(obj.destination_eve_solar_system)
        self.assertEqual(obj.eve_entity_category(), "")

    def test_create_from_esi_2nd_gate(self, mock_esi):
        mock_esi.client = EsiClientStub()

        akidagi, _ = EveStargate.objects.get_or_create_esi(id=50016284)
        self.assertEqual(akidagi.id, 50016284)
        enaluri, _ = EveStargate.objects.get_or_create_esi(id=50016283)
        self.assertEqual(enaluri.id, 50016283)
        akidagi.refresh_from_db()

        self.assertEqual(enaluri.destination_eve_stargate, akidagi)
        self.assertEqual(akidagi.destination_eve_stargate, enaluri)

        self.assertEqual(
            enaluri.destination_eve_solar_system,
            EveSolarSystem.objects.get(id=30045339),
        )
        self.assertEqual(
            akidagi.destination_eve_solar_system,
            EveSolarSystem.objects.get(id=30045342),
        )


@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False)
@patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_STATIONS", True)
@patch(MANAGERS_PATH + ".esi")
class TestEveStation(NoSocketsTestCase):
    def test_create_from_esi(self, mock_esi):
        mock_esi.client = EsiClientStub()

        obj, created = EveStation.objects.update_or_create_esi(id=60015068)
        self.assertTrue(created)
        self.assertEqual(obj.id, 60015068)
        self.assertEqual(obj.name, "Enaluri V - State Protectorate Assembly Plant")
        self.assertEqual(obj.max_dockable_ship_volume, 50000000)
        self.assertEqual(obj.office_rental_cost, 118744)
        self.assertEqual(obj.owner_id, 1000180)
        self.assertEqual(obj.position_x, 96519659520)
        self.assertEqual(obj.position_y, 65249280)
        self.assertEqual(obj.position_z, 976627507200)
        self.assertEqual(obj.reprocessing_efficiency, 0.5)
        self.assertEqual(obj.reprocessing_stations_take, 0.025)
        self.assertEqual(obj.eve_race, EveRace.objects.get(id=1))
        self.assertEqual(obj.eve_type, EveType.objects.get(id=1529))
        self.assertEqual(obj.eve_solar_system, EveSolarSystem.objects.get(id=30045339))
        self.assertEqual(obj.eve_entity_category(), EveEntity.CATEGORY_STATION)

        self.assertEqual(
            set(obj.services.values_list("name", flat=True)),
            set(
                [
                    "bounty-missions",
                    "courier-missions",
                    "reprocessing-plant",
                    "market",
                    "repair-facilities",
                    "factory",
                    "fitting",
                    "news",
                    "insurance",
                    "docking",
                    "office-rental",
                    "loyalty-point-store",
                    "navy-offices",
                    "security-offices",
                ]
            ),
        )
