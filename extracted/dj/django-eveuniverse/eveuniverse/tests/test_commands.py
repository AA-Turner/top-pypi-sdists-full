from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test.utils import override_settings

from eveuniverse.models import EveCategory, EveGroup, EveType
from eveuniverse.utils import NoSocketsTestCase

from .testdata.esi import EsiClientStub
from .testdata.factories_2 import (
    EveMoonFactory,
    EvePlanetFactory,
    EveSolarSystemFactory,
)

MODELS_PATH = "eveuniverse.models.base"
PACKAGE_PATH = "eveuniverse.management.commands"


@patch(PACKAGE_PATH + ".eveuniverse_load_data.is_esi_online", lambda: True)
@patch(PACKAGE_PATH + ".eveuniverse_load_data.get_input")
@patch(PACKAGE_PATH + ".eveuniverse_load_data.chain")
class TestLoadDataCommand(NoSocketsTestCase):
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
        with patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_ASTEROID_BELTS", False), patch(
            MODELS_PATH + ".EVEUNIVERSE_LOAD_DOGMAS", False
        ), patch(MODELS_PATH + ".EVEUNIVERSE_LOAD_GRAPHICS", False), patch(
            MODELS_PATH + ".EVEUNIVERSE_LOAD_MARKET_GROUPS", False
        ), patch(
            MODELS_PATH + ".EVEUNIVERSE_LOAD_MOONS", False
        ), patch(
            MODELS_PATH + ".EVEUNIVERSE_LOAD_PLANETS", False
        ), patch(
            MODELS_PATH + ".EVEUNIVERSE_LOAD_STARGATES", False
        ), patch(
            MODELS_PATH + ".EVEUNIVERSE_LOAD_STARS", False
        ), patch(
            MODELS_PATH + ".EVEUNIVERSE_LOAD_STATIONS", False
        ), patch(
            MODELS_PATH + ".EVEUNIVERSE_LOAD_TYPE_MATERIALS", False
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
@patch("eveuniverse.managers.universe.esi")
@patch(PACKAGE_PATH + ".eveuniverse_load_types.is_esi_online", lambda: True)
@patch(PACKAGE_PATH + ".eveuniverse_load_types.get_input")
class TestLoadTypes(NoSocketsTestCase):
    def test_load_one_type(self, mock_get_input, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        mock_get_input.return_value = "y"
        # when
        call_command(
            "eveuniverse_load_types", "dummy_app", "--type_id", "603", stdout=StringIO()
        )
        # then
        obj = EveType.objects.get(id=603)
        self.assertEqual(obj.dogma_attributes.count(), 0)
        self.assertEqual(obj.dogma_effects.count(), 0)

    def test_load_multiple_types(self, mock_get_input, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        mock_get_input.return_value = "y"
        # when
        call_command(
            "eveuniverse_load_types",
            "dummy_app",
            "--type_id",
            "1529",
            "--type_id",
            "35825",
            stdout=StringIO(),
        )
        # then
        self.assertTrue(EveType.objects.filter(id=1529).exists())
        self.assertTrue(EveType.objects.filter(id=35825).exists())

    def test_load_multiple_combined(self, mock_get_input, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        mock_get_input.return_value = "y"
        # when
        call_command(
            "eveuniverse_load_types",
            "dummy_app",
            "--category_id",
            "65",
            stdout=StringIO(),
        )
        # then
        self.assertTrue(EveCategory.objects.filter(id=65).exists())
        self.assertTrue(EveGroup.objects.filter(id=1404).exists())
        self.assertTrue(EveType.objects.filter(id=35825).exists())

    def test_can_handle_no_params(self, mock_get_input, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        mock_get_input.return_value = "y"
        # when/then
        call_command(
            "eveuniverse_load_types",
            "dummy_app",
            stdout=StringIO(),
        )

    def test_can_abort(self, mock_get_input, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        mock_get_input.return_value = "n"
        # when
        call_command(
            "eveuniverse_load_types",
            "dummy_app",
            "--type_id",
            "35825",
            stdout=StringIO(),
        )
        # then
        self.assertFalse(EveType.objects.filter(id=35825).exists())

    def test_load_one_type_with_dogma(self, mock_get_input, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        mock_get_input.return_value = "y"
        # when
        call_command(
            "eveuniverse_load_types",
            "dummy_app",
            "--type_id_with_dogma",
            "603",
            stdout=StringIO(),
        )
        # then
        obj = EveType.objects.get(id=603)
        self.assertEqual(obj.dogma_attributes.count(), 2)
        self.assertEqual(obj.dogma_effects.count(), 2)

    def test_should_understand_no_input_1(self, mock_get_input, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        mock_get_input.side_effect = RuntimeError
        # when
        call_command(
            "eveuniverse_load_types",
            "dummy_app",
            "--type_id",
            "35825",
            "--noinput",
            stdout=StringIO(),
        )
        # then
        self.assertTrue(EveType.objects.filter(id=35825).exists())

    def test_should_understand_no_input_2(self, mock_get_input, mock_esi):
        # given
        mock_esi.client = EsiClientStub()
        mock_get_input.side_effect = RuntimeError
        # when
        call_command(
            "eveuniverse_load_types",
            "dummy_app",
            "--type_id",
            "35825",
            "--no-input",
            stdout=StringIO(),
        )
        # then
        self.assertTrue(EveType.objects.filter(id=35825).exists())


@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
@patch("eveuniverse.managers.universe.esi")
@patch(PACKAGE_PATH + ".eveuniverse_load_types.is_esi_online")
@patch(PACKAGE_PATH + ".eveuniverse_load_types.get_input")
class TestLoadTypesEsiCheck(NoSocketsTestCase):
    def test_checks_esi_by_default(self, mock_get_input, mock_is_esi_online, mock_esi):
        mock_esi.client = EsiClientStub()
        mock_get_input.return_value = "y"

        call_command(
            "eveuniverse_load_types",
            "dummy_app",
            "--type_id",
            "603",
            stdout=StringIO(),
        )
        self.assertTrue(EveType.objects.filter(id=603).exists())
        self.assertTrue(mock_is_esi_online.called)

    def test_can_disable_esi_check(self, mock_get_input, mock_is_esi_online, mock_esi):
        mock_esi.client = EsiClientStub()
        mock_get_input.return_value = "y"

        call_command(
            "eveuniverse_load_types",
            "dummy_app",
            "--type_id",
            "603",
            "--disable_esi_check",
            stdout=StringIO(),
        )
        self.assertTrue(EveType.objects.filter(id=603).exists())
        self.assertFalse(mock_is_esi_online.called)


class TestFixSections(NoSocketsTestCase):
    def test_should_remove_planets_flag_when_no_planet(self):
        # given
        obj = EveSolarSystemFactory()
        obj.enabled_sections.planets = True
        obj.save()
        # when
        call_command("eveuniverse_fix_section_flags", stdout=StringIO())
        # then
        obj.refresh_from_db()
        self.assertFalse(obj.enabled_sections.planets)

    def test_should_not_remove_planets_flag_when_planets_exist(self):
        # given
        obj = EveSolarSystemFactory()
        obj.enabled_sections.planets = True
        obj.save()
        EvePlanetFactory(eve_solar_system=obj)
        # when
        call_command("eveuniverse_fix_section_flags", stdout=StringIO())
        # then
        obj.refresh_from_db()
        self.assertTrue(obj.enabled_sections.planets)

    def test_should_remove_moons_flag_when_no_moons(self):
        # given
        obj = EvePlanetFactory()
        obj.enabled_sections.moons = True
        obj.save()
        # when
        call_command("eveuniverse_fix_section_flags", stdout=StringIO())
        # then
        obj.refresh_from_db()
        self.assertFalse(obj.enabled_sections.moons)

    def test_should_not_remove_moons_flag_when_moons_exist(self):
        # given
        obj = EvePlanetFactory()
        obj.enabled_sections.moons = True
        obj.save()
        EveMoonFactory(eve_planet=obj)
        # when
        call_command("eveuniverse_fix_section_flags", stdout=StringIO())
        # then
        obj.refresh_from_db()
        self.assertTrue(obj.enabled_sections.moons)
