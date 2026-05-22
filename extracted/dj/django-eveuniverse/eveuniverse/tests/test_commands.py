from io import StringIO
from unittest.mock import patch

import pook
from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings

from eveuniverse.models import EveType
from eveuniverse.tests.helpers import TestCaseWithClearCache
from eveuniverse.tests.testdata.factories_2 import (
    EveDogmaAttributeFactory,
    EveDogmaEffectFactory,
    EveGroupFactory,
    make_esi_url,
)

MODELS_PATH = "eveuniverse.models.base"
PACKAGE_PATH = "eveuniverse.management.commands"


@patch(PACKAGE_PATH + ".eveuniverse_load_data.is_esi_online", lambda: True)
@patch(PACKAGE_PATH + ".eveuniverse_load_data.get_input")
@patch(PACKAGE_PATH + ".eveuniverse_load_data.chain")
class TestLoadDataCommand(TestCase):
    def test_load_data_map(self, mock_chain, mock_get_input):
        # given
        mock_get_input.return_value = "y"
        # when
        call_command("eveuniverse_load_data", "map", stdout=StringIO())
        # then
        args, _ = mock_chain.call_args
        tasks = {o.task for o in args[0]}
        self.assertSetEqual({"eveuniverse.tasks.load_map"}, tasks)

    def test_load_data_ship_types(self, mock_chain, mock_get_input):
        # given
        mock_get_input.return_value = "y"
        # when
        call_command("eveuniverse_load_data", "ships", stdout=StringIO())
        # then
        args, _ = mock_chain.call_args
        tasks = {o.task for o in args[0]}
        self.assertSetEqual({"eveuniverse.tasks.load_ship_types"}, tasks)

    def test_load_data_structure_types(self, mock_chain, mock_get_input):
        # given
        mock_get_input.return_value = "y"
        # when
        call_command("eveuniverse_load_data", "structures", stdout=StringIO())
        # then
        args, _ = mock_chain.call_args
        tasks = {o.task for o in args[0]}
        self.assertSetEqual({"eveuniverse.tasks.load_structure_types"}, tasks)

    def test_should_load_all_types_with_sections(self, mock_chain, mock_get_input):
        # given
        mock_get_input.return_value = "y"
        # when
        call_command("eveuniverse_load_data", "types", stdout=StringIO())
        # then
        args, _ = mock_chain.call_args
        tasks = {o.task for o in args[0]}
        self.assertSetEqual({"eveuniverse.tasks.load_all_types"}, tasks)

    def test_should_load_all_types(self, mock_chain, mock_get_input):
        # given
        mock_get_input.return_value = "y"
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
            call_command(
                "eveuniverse_load_data",
                "types",
                "--types-enabled-sections",
                "dogmas",
                "type_materials",
                stdout=StringIO(),
            )
        # then
        args, _ = mock_chain.call_args
        tasks = {o.task: {"kwargs": o.kwargs, "args": o.args} for o in args[0]}
        self.assertSetEqual({"eveuniverse.tasks.load_all_types"}, set(tasks.keys()))
        self.assertSetEqual(
            set(tasks["eveuniverse.tasks.load_all_types"]["args"][0]),
            {"dogmas", "type_materials"},
        )

    def test_can_abort(self, mock_chain, mock_get_input):
        # given
        mock_get_input.return_value = "n"
        # when
        call_command("eveuniverse_load_data", "map", stdout=StringIO())
        # then
        self.assertFalse(mock_chain.called)

    def test_should_skip_confirmation_question(self, mock_chain, mock_get_input):
        # given
        mock_get_input.side_effect = RuntimeError
        # when
        call_command("eveuniverse_load_data", "map", "--noinput", stdout=StringIO())
        # then
        args, _ = mock_chain.call_args
        tasks = {o.task for o in args[0]}
        self.assertSetEqual({"eveuniverse.tasks.load_map"}, tasks)

    def test_should_load_structures_and_ships(self, mock_chain, mock_get_input):
        # given
        mock_get_input.return_value = "y"
        # when
        call_command("eveuniverse_load_data", "structures", "ships", stdout=StringIO())
        # then
        args, _ = mock_chain.call_args
        tasks = {o.task for o in args[0]}
        self.assertSetEqual(
            {
                "eveuniverse.tasks.load_structure_types",
                "eveuniverse.tasks.load_ship_types",
            },
            tasks,
        )


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
@patch(PACKAGE_PATH + ".eveuniverse_load_types.is_esi_online", lambda: True)
class TestLoadTypes(TestCaseWithClearCache):
    @pook.on
    def test_load_one_type(self):
        # given
        type_id = 603
        eg = EveGroupFactory()
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [],
                "dogma_effects": [],
                "graphic_id": 42,
                "group_id": eg.id,
                "market_group_id": 666,
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
        with patch(PACKAGE_PATH + ".eveuniverse_load_types.get_input") as m:
            m.return_value = "y"

            call_command(
                "eveuniverse_load_types",
                "dummy_app",
                "--type_id",
                f"{type_id}",
                stdout=StringIO(),
            )

        # then
        self.assertTrue(EveType.objects.filter(id=type_id).exists())

    @pook.on
    def test_load_multiple_types(self):
        # given
        type_id_1 = 603
        type_id_2 = 605
        eg = EveGroupFactory()
        pook.get(
            make_esi_url(f"universe/types/{type_id_1}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [],
                "dogma_effects": [],
                "graphic_id": 42,
                "group_id": eg.id,
                "market_group_id": 666,
                "mass": 997000,
                "name": "Merlin",
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": type_id_1,
                "volume": 16500,
            },
        )
        pook.get(
            make_esi_url(f"universe/types/{type_id_2}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [],
                "dogma_effects": [],
                "graphic_id": 42,
                "group_id": eg.id,
                "market_group_id": 666,
                "mass": 997000,
                "name": "Heron",
                "packaged_volume": 2500,
                "portion_size": 1,
                "published": True,
                "radius": 39,
                "type_id": type_id_2,
                "volume": 16500,
            },
        )

        # when
        with patch(PACKAGE_PATH + ".eveuniverse_load_types.get_input") as m:
            m.return_value = "y"

            call_command(
                "eveuniverse_load_types",
                "dummy_app",
                "--type_id",
                f"{type_id_1}",
                "--type_id",
                f"{type_id_2}",
                stdout=StringIO(),
            )

        # then
        self.assertTrue(EveType.objects.filter(id=type_id_1).exists())
        self.assertTrue(EveType.objects.filter(id=type_id_2).exists())

    @pook.on
    def test_should_load_category_with_all_children(self):
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
        with patch(PACKAGE_PATH + ".eveuniverse_load_types.get_input") as m:
            m.return_value = "y"

            call_command(
                "eveuniverse_load_types",
                "dummy_app",
                "--category_id",
                f"{category_id}",
                stdout=StringIO(),
            )

        # then
        self.assertTrue(EveType.objects.filter(id=type_id).exists())

    @pook.on
    def test_can_handle_no_params(self):
        # when/then
        with patch(PACKAGE_PATH + ".eveuniverse_load_types.get_input") as m:
            m.return_value = "y"

            call_command(
                "eveuniverse_load_types",
                "dummy_app",
                stdout=StringIO(),
            )

    @pook.on
    def test_can_abort(self):
        # when
        with patch(PACKAGE_PATH + ".eveuniverse_load_types.get_input") as m:
            m.return_value = "n"

            call_command(
                "eveuniverse_load_types",
                "dummy_app",
                "--type_id",
                "35825",
                stdout=StringIO(),
            )

        # then
        self.assertFalse(EveType.objects.filter(id=35825).exists())

    @pook.on
    def test_load_one_type_with_dogma(self):
        # given
        type_id = 603
        eg = EveGroupFactory()
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
                "graphic_id": 42,
                "group_id": eg.id,
                "market_group_id": 666,
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
        with patch(PACKAGE_PATH + ".eveuniverse_load_types.get_input") as m:
            m.return_value = "y"

            call_command(
                "eveuniverse_load_types",
                "dummy_app",
                "--type_id_with_dogma",
                f"{type_id}",
                stdout=StringIO(),
            )

        # then
        obj = EveType.objects.get(id=type_id)
        self.assertEqual(obj.dogma_attributes.count(), 1)
        self.assertEqual(obj.dogma_effects.count(), 1)


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
class TestLoadTypes_EsiCheck(TestCaseWithClearCache):
    @patch(PACKAGE_PATH + ".eveuniverse_load_types.is_esi_online")
    @pook.on
    def test_checks_esi_by_default(self, mock_is_esi_online):
        # given
        type_id = 603
        eg = EveGroupFactory()
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [],
                "dogma_effects": [],
                "graphic_id": 42,
                "group_id": eg.id,
                "market_group_id": 666,
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
        with patch(PACKAGE_PATH + ".eveuniverse_load_types.get_input") as m:
            m.return_value = "y"

            call_command(
                "eveuniverse_load_types",
                "dummy_app",
                "--type_id",
                f"{type_id}",
                stdout=StringIO(),
            )

        # then
        self.assertTrue(EveType.objects.filter(id=type_id).exists())
        self.assertTrue(mock_is_esi_online.called)

    @patch(PACKAGE_PATH + ".eveuniverse_load_types.is_esi_online")
    @pook.on
    def test_can_disable_esi_check(self, mock_is_esi_online):
        # given
        type_id = 603
        eg = EveGroupFactory()
        pook.get(
            make_esi_url(f"universe/types/{type_id}"),
            reply=200,
            response_json={
                "capacity": 150,
                "description": "",
                "dogma_attributes": [],
                "dogma_effects": [],
                "graphic_id": 42,
                "group_id": eg.id,
                "market_group_id": 666,
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
        with patch(PACKAGE_PATH + ".eveuniverse_load_types.get_input") as m:
            m.return_value = "y"

            call_command(
                "eveuniverse_load_types",
                "dummy_app",
                "--type_id",
                f"{type_id}",
                "--disable_esi_check",
                stdout=StringIO(),
            )

        # then
        self.assertTrue(EveType.objects.filter(id=type_id).exists())
        self.assertFalse(mock_is_esi_online.called)
