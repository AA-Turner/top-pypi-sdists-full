import unittest
import json
from unittest.mock import MagicMock, patch

from locust import TaskSet, Locust

from appian_locust.uiform import DesignObjectUiForm
from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from appian_locust import AppianTaskSet


class TestDesignObjectUiform(unittest.TestCase):
    site_with_expression_editor = read_mock_file("site_with_expression_editor.json")
    record_with_application_navigation_tab = read_mock_file("record_with_application_navigation_bar.json")

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(Locust())
        parent_task_set = TaskSet(self.custom_locust)
        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "auth", ["", ""])
        self.task_set = AppianTaskSet(parent_task_set)
        self.task_set.host = ""

        # test_on_start_auth_success is covered here.
        self.custom_locust.set_response("auth?appian_environment=tempo", 200, '{}')
        self.task_set.on_start()

    def tearDown(self) -> None:
        self.task_set.on_stop()

    def test_launch_vqd_editor(self) -> None:
        design_object_id = "koBGwdcAdRO6tHOqesC5VrRQaOImjMHbae8gSHbTkBgcBzQ9tfWwA5Uy5XbNCjSc7OdVCy8-cbbmM1spiLkA9ZnNKmMrbGI6cSJqA"
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/app/design/{design_object_id}", 200, self.site_with_expression_editor)
        sail_form = self.task_set.appian.visitor.visit_design_object_by_id(design_object_id)
        result_dict = '{"ase": "ase2", "saveInto": "whatever"}'
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/app/design/{design_object_id}", 200, result_dict)
        sail_form.launch_query_editor()
        self.assertEqual(sail_form.get_latest_state(), json.loads(result_dict))

    @patch('appian_locust._interactor._Interactor.click_generic_element')
    def test_click_record_type_application_navigation_tab(self, click_generic_mock: MagicMock) -> None:
        design_object_id = "koBHhnlH6FVusQ4yRwpEkTWNA7yg1f0HA7nK6eVL9FOxAr9cMU0Ygi-5qZsepPcq1rSjlV57X1QWHnI5Usbdf2qurMQqG4tK334ew"
        # Visit the record type
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/app/design/{design_object_id}", 200, self.record_with_application_navigation_tab)
        sail_form = self.task_set.appian.visitor.visit_design_object_by_id(design_object_id)
        # Click action
        page_to_visit = "Actions"
        design_object = sail_form.click_record_type_application_navigation_tab(page_to_visit)

        _, kwargs = click_generic_mock.call_args_list[0]
        value = kwargs["new_value"]
        self.assertEqual(value, {
            "#t": "Text", "#v": "related-actions"
        })
