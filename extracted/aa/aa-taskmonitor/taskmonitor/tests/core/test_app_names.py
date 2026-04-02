from unittest.mock import patch

from django.test import TestCase

from taskmonitor.core import app_names

MODULE_PATH = "taskmonitor.core.app_names"


class TestExtractAppName(TestCase):
    def test_can_extract_from_normal_task_name(self):
        # when
        result = app_names.from_task_name("alpha.tasks.task_name")
        # then
        self.assertEqual(result, "alpha")

    def test_can_extract_from_long_task_name(self):
        # when
        result = app_names.from_task_name("omega.alpha.tasks.task_name")
        # then
        self.assertEqual(result, "alpha")

    def test_can_extract_from_extra_long_task_name(self):
        # when
        result = app_names.from_task_name("echo.omega.alpha.tasks.task_name")
        # then
        self.assertEqual(result, "alpha")

    def test_can_extract_from_custom_task_name(self):
        # when
        result = app_names.from_task_name("alpha.task_name")
        # then
        self.assertEqual(result, "alpha")

    def test_should_return_empty_string_if_no_match_1(self):
        # when
        result = app_names.from_task_name("dummy")
        # then
        self.assertEqual(result, "")

    def test_should_return_empty_string_if_no_match_2(self):
        # when
        result = app_names.from_task_name("tasks.dummy")
        # then
        self.assertEqual(result, "")


class TestAppNameMapping(TestCase):
    @patch(MODULE_PATH + "._app_names_mapping", {"alpha": "bravo"})
    def test_should_map_to_alternate_name(self):
        # when
        result = app_names.from_task_name("alpha.tasks.task_name")
        # then
        self.assertEqual(result, "bravo")

    @patch(MODULE_PATH + "._app_names_mapping", {"charlie": "bravo"})
    def test_should_not_map(self):
        # when
        result = app_names.from_task_name("alpha.tasks.task_name")
        # then
        self.assertEqual(result, "alpha")


class TestConsolidateApp(TestCase):
    @patch(MODULE_PATH + ".TASKMONITOR_APP_NAME_MAPPING_CONFIG", {"alpha": ["alpha_3"]})
    @patch(
        MODULE_PATH + ".TASKMONITOR_APP_NAME_MAPPING_DEFAULTS", {"alpha": ["alpha_2"]}
    )
    def test_should_return_mapping(self):
        # when
        result = app_names._consolidate_app_names_mapping()
        # then
        expected = {"alpha_2": "alpha", "alpha_3": "alpha"}
        self.assertEqual(result, expected)
