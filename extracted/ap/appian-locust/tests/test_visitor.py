import unittest
from unittest.mock import patch
import json

from typing import Any
from locust import TaskSet, Locust, stats
from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from appian_locust import AppianTaskSet
from appian_locust.exceptions import IncorrectDesignAccessException
from appian_locust.uiform import SailUiForm, ApplicationUiForm, DesignUiForm, DesignObjectUiForm, RecordListUiForm, RecordInstanceUiForm
from appian_locust.objects import DesignObjectType
from appian_locust.utilities.helper import ENV
from appian_locust.utilities.url_provider import URL_PROVIDER_V0, URL_PROVIDER_V1
from appian_locust._admin import ADMIN_URI_PATH
from appian_locust._tasks import _Tasks
from appian_locust._reports import REPORTS_INTERFACE_PATH
from appian_locust._records import RECORDS_INTERFACE_PATH
from appian_locust._actions import ACTIONS_INTERFACE_PATH, ACTIONS_FEED_PATH

RDO_HOST = "https://ai-skill-server.net"


class TestVisitor(unittest.TestCase):
    design_landing_page = read_mock_file("design_landing_page.json")
    application_page = read_mock_file("design_app_landing_page.json")
    interface_page = read_mock_file("interface_resp.json")
    task_feed_resp = read_mock_file("tasks_response.json")
    task_feed_with_next = read_mock_file("tasks_response_with_next.json")
    record_types = read_mock_file("record_types_response.json")
    # Record Instance List for a specific RecordType
    records = read_mock_file("records_response.json")
    grid_records = read_mock_file("records_grid_response.json")
    # Record Summary dashboard response for a specific Record Instance
    record_summary_view = read_mock_file("record_summary_view_response.json")
    record_instance_name = "Actions Page"
    records_interface = read_mock_file("records_interface.json")
    records_nav = read_mock_file("records_nav.json")
    sites_nav_resp = read_mock_file("sites_nav_resp.json")
    sites_with_groups_nav_resp = read_mock_file("sites_groups_nav.json")
    actions = read_mock_file("actions_response.json")
    actions_interface = read_mock_file("actions_interface.json")
    actions_nav = read_mock_file("actions_nav.json")
    actions_feed = read_mock_file("actions_feed.json")
    bff_token_response = read_mock_file("bff_token_response.json")
    ai_skill_design_object_response = read_mock_file("ai_skill_design_object_response.json")
    ai_skill_response = read_mock_file("ai_skill_response.json")

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(Locust())
        parent_task_set = TaskSet(self.custom_locust)
        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "auth", ["fake_user", ""])
        self.task_set = AppianTaskSet(parent_task_set)
        self.task_set.host = ""

        # test_on_start_auth_success is covered here.
        self.custom_locust.set_response("auth?appian_environment=tempo", 200, '{}')
        self.task_set.on_start()

        # Setup responses for tasks
        self.setUp_task_responses()

        # Setup responses for page types
        self.setUp_report_responses()

        # Setup responses for records
        self.setUp_record_responses()

        # Setup responses for sites
        self.setUp_sites_responses()

        # Setup responses for actions
        self.setUp_actions_json()

        # Setup responses for AI Skills
        self.setup_rdo_responses()

    def setUp_task_responses(self) -> None:
        self.custom_locust.set_response(_Tasks.INITIAL_FEED_URI, 200, self.task_feed_resp)

    def get_task_attributes(self, is_auto_acceptable: bool) -> str:
        return f"""
        {{
            "isOfflineTask": false,
            "isSailTask": true,
            "isQuickTask": false,
            "taskId": "1",
            "isAutoAcceptable": {'true' if is_auto_acceptable else 'false'}
        }}"""

    def setUp_report_responses(self) -> None:
        self.custom_locust.set_response("/suite/rest/a/uicontainer/latest/reports", 200, read_mock_file("reports_response.json"))
        self.custom_locust.set_response(REPORTS_INTERFACE_PATH, 200, read_mock_file("reports_interface.json"))
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/page/reports/nav", 200, read_mock_file("reports_nav.json"))

    def setUp_record_responses(self) -> None:
        self.custom_locust.set_response("/suite/rest/a/applications/latest/app/records/view/all", 200,
                                        self.record_types)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/commit", 200,
                                        self.records)
        self.custom_locust.set_response("/suite/rest/a/applications/latest/legacy/tempo/records/type/commit/view/all", 200,
                                        self.records)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/BE5pSw", 200,
                                        self.grid_records)
        self.custom_locust.set_response("/suite/rest/a/applications/latest/legacy/tempo/records/type/BE5pSw/view/all", 200,
                                        self.grid_records)
        self.custom_locust.set_response(
            "/suite/rest/a/sites/latest/D6JMim/page/records/record/lQB0K7YxC0UQ2Fhx4pmY1F49C_MjItD4hbtRdKDmOo6V3MOBxI47ipGa_bJKZf86CLtvOCp1cfX-sa2O9hp6WTKZpbGo5MxRaaTwMkcYMeDl8kN8Hg/view/summary",
            200,
            self.record_summary_view)
        self.custom_locust.set_response(RECORDS_INTERFACE_PATH, 200, self.records_interface)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/page/records/nav", 200, self.records_nav)

    def setup_rdo_responses(self) -> None:
        self.custom_locust.set_response("/suite/rfx/bff-token", 200, self.bff_token_response)
        self.custom_locust.set_response(f"{RDO_HOST}/rdo-server/DesignObjects/InterfaceAuthentication/v1", 200, "{}")

    def setUp_sites_responses(self) -> None:
        page_resp_json = read_mock_file("page_resp.json")
        all_sites_str = read_mock_file("all_sites.json")
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/page/news/nav", 200, all_sites_str)
        self.custom_locust.client.set_default_response(200, page_resp_json)

    def setUp_sites_json(self, site_name: str) -> None:
        self.custom_locust.set_response(f"/suite/rest/a/sites/latest/{site_name}/nav", 200, self.sites_nav_resp)

    def setUp_actions_json(self) -> None:
        self.custom_locust.set_response(
            "auth?appian_environment=tempo", 200, '{}')
        self.custom_locust.set_response(
            "/suite/api/tempo/open-a-case/available-actions?ids=%5B%5D", 200, self.actions)
        self.custom_locust.set_response(ACTIONS_INTERFACE_PATH, 200, self.actions_interface)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/page/actions/nav", 200, self.actions_nav)
        self.custom_locust.set_response(ACTIONS_FEED_PATH, 200, self.actions_feed)

    def tearDown(self) -> None:
        self.task_set.on_stop()

    def test_visit_task_success(self) -> None:
        task_to_accept = read_mock_file('task_accept_resp.json')
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/1/status",
            200,
            task_to_accept
        )
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/1/form",
            200,
            task_to_accept
        )
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/1/attributes",
            200,
            self.get_task_attributes(is_auto_acceptable=False))
        output = self.task_set.appian.visitor.visit_task("t-1", False)
        self.assertEqual(output.form_url, "/suite/rest/a/task/latest/1/form")

    def test_visit_task_failure(self) -> None:
        task_to_accept = read_mock_file('task_accept_resp.json')
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/1/status",
            200,
            task_to_accept
        )
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/1/form",
            200,
            task_to_accept
        )
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/1/attributes",
            200,
            self.get_task_attributes(is_auto_acceptable=False))

        task_name = "nonexistent task"
        exact_match = False
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_task(task_name, exact_match)
            self.assertEqual(context.exception.args[0], f"There is no task with name {task_name} in the system under test (Exact match = {exact_match})")

    def test_visit_report_success(self) -> None:
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/p.reports/report/qdjDPA/reportlink",
                                        200, '{"context":123, "uuid":123}')

        sail_form = self.task_set.appian.visitor.visit_report(
            "RTE Basic Test Report", False)
        self.assertTrue(isinstance(sail_form, SailUiForm))

    def test_visit_report_failure(self) -> None:
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/p.reports/report/qdjDPA/reportlink",
                                        200, '{"context":123, "uuid":123}')

        report_name = "Fake Report"
        exact_match = False
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_report(
                report_name, exact_match)
        self.assertEqual(
            context.exception.args[0], f"There is no report with name {report_name} in the system under test (Exact match = {exact_match})")

    def test_design_visit_error(self) -> None:
        ENV.stats.clear_all()
        self.custom_locust.set_response(
            "/suite/rest/a/applications/latest/app/design", 400, "")
        with self.assertRaises(Exception) as context:
            sail_form = self.task_set.appian.visitor.visit_design()

    def test_visit_design(self) -> None:
        self.custom_locust.set_response(
            "/suite/rest/a/applications/latest/app/design", 200, self.design_landing_page)
        ENV.stats.clear_all()
        design_form = self.task_set.appian.visitor.visit_design()
        self.assertEqual(type(design_form), DesignUiForm)
        self.assertEqual(0, len(ENV.stats.errors))

    def test_visit_application(self) -> None:
        app_id = "thisIsAnAppId"
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/app/design/app/{app_id}", 200, self.application_page)
        ENV.stats.clear_all()
        sail_form = self.task_set.appian.visitor.visit_application_by_id(app_id)
        self.assertEqual(type(sail_form), ApplicationUiForm)
        self.assertEqual(0, len(ENV.stats.errors))

    def test_visit_application_by_name(self) -> None:
        app_name = "SOAP Test App"
        app_id = "AADgJqdggACYugHvkAHvkAAAXgk"
        self.custom_locust.enqueue_response(200, self.design_landing_page)  # First request to "/suite/rest/a/applications/latest/app/design", returns base design page
        self.custom_locust.enqueue_response(200, self.design_landing_page)  # Second request to "/suite/rest/a/applications/latest/app/design", this is the search
        self.custom_locust.enqueue_response(200, self.application_page)    # Final request to "/suite/rest/a/applications/latest/app/design", this is for clicking on application link
        ENV.stats.clear_all()
        sail_form = self.task_set.appian.visitor.visit_application_by_name(app_name)
        self.assertEqual(type(sail_form), ApplicationUiForm)
        self.assertEqual(sail_form.get_latest_state()["_cId"], json.loads(self.application_page)["_cId"])
        self.assertEqual(0, len(ENV.stats.errors))

    def test_visit_design_object(self) -> None:
        design_object_id = "thisIsADesignObjectId"
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/app/design/{design_object_id}", 200, self.design_landing_page)
        ENV.stats.clear_all()
        sail_form = self.task_set.appian.visitor.visit_design_object_by_id(design_object_id)
        self.assertEqual(type(sail_form), DesignObjectUiForm)
        self.assertEqual(0, len(ENV.stats.errors))

    def test_visit_design_object_by_name(self) -> None:
        self.custom_locust.enqueue_response(200, self.application_page)                             # Navigate to /design
        self.custom_locust.enqueue_response(200, read_mock_file("empty_design_objects.json"))       # Click on objects
        self.custom_locust.enqueue_response(200, read_mock_file("design_objects.json"))             # Filter to Interfaces
        self.custom_locust.enqueue_response(200, read_mock_file("design_objects.json"))             # Search for "FTA_"
        design_object_id = "lIBvbWpmCW-DXb2Ymh0Z0BoA4mWVpvJiz89VdsTcjtGkRoZgOr6ytR1w9IzvBtl4UqC4SkzwXbxvgAnqiJbQX0k4x_-Dh8FA0svqT6RsalzjxaP"
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/app/design/{design_object_id}", 200, self.interface_page)
        ENV.stats.clear_all()
        design_form = self.task_set.appian.visitor.visit_design_object_by_name("FTA_", DesignObjectType.INTERFACE)
        self.assertEqual(type(design_form), DesignObjectUiForm)
        self.assertEqual(design_form.get_latest_state()["_cId"], json.loads(self.interface_page)["_cId"])
        self.assertEqual(0, len(ENV.stats.errors))

    def test_visit_design_object_throws_ai_skill_exception(self) -> None:
        design_object_id = "thisIsADesignObjectId"
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/app/design/{design_object_id}", 200, self.ai_skill_design_object_response)
        ENV.stats.clear_all()
        with self.assertRaises(IncorrectDesignAccessException) as context:
            self.task_set.appian.visitor.visit_design_object_by_id(design_object_id)
        self.assertEqual(
            context.exception.args[0],
            "Selected Design Object was of type aiSkill, use visit_ai_skill_by_id method instead")

    def test_visit_ai_skill(self) -> None:
        design_object_id = "thisIsADesignObjectId"
        self.setup_rdo_responses()
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/app/design/{design_object_id}", 200, self.ai_skill_design_object_response)
        self.custom_locust.set_response(f"{RDO_HOST}/sail-server/SYSTEM_SYSRULES_aiSkillDesigner/ui", 200, "{\"this_is\": \"a_response\"}")
        ENV.stats.clear_all()
        ai_skill_form = self.task_set.appian.visitor.visit_ai_skill_by_id(design_object_id)
        self.assertEqual(ai_skill_form.get_latest_state(), {"this_is": "a_response"})
        self.assertEqual(0, len(ENV.stats.errors))

    def test_visit_ai_skill_by_name(self) -> None:
        self.custom_locust.enqueue_response(200, self.application_page)                             # Navigate to /design
        self.custom_locust.enqueue_response(200, read_mock_file("empty_design_objects.json"))       # Click on objects
        self.custom_locust.enqueue_response(200, read_mock_file("design_objects.json"))             # Filter to Interfaces
        self.custom_locust.enqueue_response(200, read_mock_file("design_objects.json"))             # Search for "FTA_"
        design_object_id = "lIBvbWpmCW-DXb2Ymh0Z0BoA4mWVpvJiz89VdsTcjtGkRoZgOr6ytR1w9IzvBtl4UqC4SkzwXbxvgAnqiJbQX0k4x_-Dh8FA0svqT6RsalzjxaP"
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/app/design/{design_object_id}", 200, self.ai_skill_design_object_response)
        self.custom_locust.set_response(f"{RDO_HOST}/sail-server/SYSTEM_SYSRULES_aiSkillDesigner/ui", 200,
                                        "{\"this_is\": \"a_response\"}")
        ENV.stats.clear_all()
        ai_skill_form = self.task_set.appian.visitor.visit_ai_skill_by_name("FTA_")
        self.assertEqual(ai_skill_form.get_latest_state(), {"this_is": "a_response"})
        self.assertEqual(0, len(ENV.stats.errors))

    @patch('appian_locust._records_helper.find_component_by_attribute_in_dict', return_value={'children': None})
    def test_records_form_no_embedded_summary(self, find_component_by_attribute_in_dict_function: Any) -> None:
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_record_instance(
                record_type="Commits",
                record_name=self.record_instance_name,
                view_url_stub="summary",
                exact_match=False)
        self.assertEqual(
            context.exception.args[0],
            "Parser was not able to find embedded SAIL code within JSON response for the requested Record Instance")

    def test_record_types_form_example_success(self) -> None:
        sail_form = self.task_set.appian.visitor.visit_record_type(
            "Commits",
        )
        self.assertTrue(isinstance(sail_form, RecordListUiForm))

    def test_record_type_random_form_example_success(self) -> None:
        sail_form = self.task_set.appian.visitor.visit_record_type()
        self.assertTrue(isinstance(sail_form, RecordListUiForm))

    def test_record_type_form_incorrect_type(self) -> None:
        record_type = "Fake Type"
        exact_match = True
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_record_type(
                record_type,
            )
        self.assertEqual(
            context.exception.args[0], f"There is no record type with name {record_type} in the system under test")

    @patch('appian_locust._records_helper.find_component_by_attribute_in_dict', return_value={'children': [json.dumps({"a": "b"})]})
    def test_records_form_example_success(self, find_component_by_attribute_in_dict_function: Any) -> None:
        sail_form = self.task_set.appian.visitor.visit_record_instance(
            "Commits",
            self.record_instance_name,
            view_url_stub="summary",
            exact_match=False
        )
        self.assertTrue(isinstance(sail_form, RecordInstanceUiForm))
        self.assertEqual(sail_form.get_latest_state(), {"a": "b"})

    @patch('appian_locust._records_helper.find_component_by_attribute_in_dict',
           return_value={'children': [json.dumps({"a": "b"})]})
    def test_records_form_example_must_search(self, find_component_by_attribute_in_dict_function: Any) -> None:
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/commit",
                                        200,
                                        self.grid_records)
        self.custom_locust.set_response(
            f"/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/commit?searchTerm=Actions%20Page", 200,
            self.records)
        self.custom_locust.set_response(
            f"/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/BE5pSw?searchTerm=Actions%20Page", 200,
            self.grid_records)

        sail_form = self.task_set.appian.visitor.visit_record_instance(
            "Commits",
            self.record_instance_name,
            view_url_stub="summary",
            exact_match=False
        )
        self.assertTrue(isinstance(sail_form, RecordInstanceUiForm))
        self.assertEqual(sail_form.get_latest_state(), {"a": "b"})

    def test_records_form_incorrect_name(self) -> None:
        record_name = "Fake Record"
        record_type = "Commits"
        exact_match = False
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/commit?searchTerm=Fake%20Record", 200,
                                        self.records)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/BE5pSw?searchTerm=Fake%20Record", 200,
                                        self.grid_records)
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_record_instance(
                record_type,
                record_name,
                view_url_stub="summary",
                exact_match=exact_match
            )
        self.assertEqual(
            context.exception.args[0], f"There is no record with name {record_name} found in record type {record_type} (Exact match = {exact_match})")

    def test_records_form_incorrect_type(self) -> None:
        exact_match = False
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_record_instance(
                "Fake Type",
                self.record_instance_name,
                view_url_stub="summary",
                exact_match=exact_match
            )
        self.assertEqual(
            context.exception.args[0], f"There is no record type with name Fake Type in the system under test (Exact match = {exact_match})")

    def test_visit_site_recordlist_and_get_random_record_form_failure(self) -> None:
        site_name = "abc"
        page_name = "create-mrn"
        link_type = "report"  # Default Page Info

        self.setUp_sites_json(site_name)
        expected_uuid = 'abc123'
        expected_context = '{"abc":"123"}'
        expected_url = f"/suite/rest/a/sites/latest/{site_name}/pages/{page_name}/{link_type}"
        form_content = f'{{"context": {expected_context}, "uuid": " {expected_uuid}", "links": [{{"href": "{expected_url}", "rel": "update"}}]}}'
        self.custom_locust.set_response(expected_url,
                                        200,
                                        form_content)
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_site_recordlist_and_get_random_record_form(site_name, page_name)
        self.assertEqual(
            context.exception.args[0], f"Page {page_name} on site {site_name} is not of type record")

    def test_visit_site_recordlist_failure(self) -> None:
        site_name = "abc"
        page_name = "create-mrn"
        link_type = "report"  # Default Page Info

        self.setUp_sites_json(site_name)
        expected_uuid = 'abc123'
        expected_context = '{"abc":"123"}'
        expected_url = f"/suite/rest/a/sites/latest/{site_name}/pages/{page_name}/{link_type}"
        form_content = f'{{"context": {expected_context}, "uuid": "{expected_uuid}", "links": [{{"href": "{expected_url}", "rel": "update"}}]}}'
        self.custom_locust.set_response(expected_url,
                                        200,
                                        form_content)
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_site_recordlist(site_name, page_name)
        self.assertEqual(
            context.exception.args[0], f"Page {page_name} on site {site_name} is not of type record")

    def test_visit_site(self) -> None:
        site_name = "abc"
        page_name = "create-mrn"
        link_type = "report"  # Default Page Info

        self.setUp_sites_json(site_name)
        expected_uuid = 'abc123'
        expected_context = '{"abc":"123"}'
        expected_url = f"/suite/rest/a/sites/latest/{site_name}/pages/{page_name}/{link_type}"
        form_content = f'{{"context": {expected_context}, "uuid": "{expected_uuid}", "links": [{{"href": "{expected_url}", "rel": "update"}}]}}'
        self.custom_locust.set_response(expected_url,
                                        200,
                                        form_content)
        ui_form: SailUiForm = self.task_set.appian.visitor.visit_site(site_name, page_name)
        self.assertEqual(expected_uuid, ui_form.uuid)
        self.assertEqual(json.loads(expected_context), ui_form.context)
        self.assertEqual(expected_url, ui_form.form_url)

    def test_visit_group_site(self) -> None:
        site_name = "test_site"
        page_name = "it"
        group_name = "first"
        expected_state = '{"abc":"123"}'
        self.custom_locust.set_response(f"/suite/rest/a/sites/latest/{site_name}/nav", 200, self.sites_with_groups_nav_resp)
        self.custom_locust.set_response(f"/suite/rest/a/sites/latest/{site_name}/page/g.{group_name}.p.{page_name}", 200, expected_state)

        self.task_set.appian._interactor.set_url_provider(URL_PROVIDER_V1)
        form = self.task_set.appian.visitor.visit_site(site_name, page_name)
        self.task_set.appian._interactor.set_url_provider(URL_PROVIDER_V0)

        self.assertEqual(json.loads(expected_state), form.get_latest_state())

    def setup_action_response_no_ui(self) -> None:
        action = self.task_set.appian.actions_info.get_action_info("Create a Case", False)
        self.custom_locust.set_response(action['formHref'], 200, "{}")

    def test_actions_visit(self) -> None:
        self.setup_action_response_no_ui()
        action = self.task_set.appian.visitor.visit_action("Create a Case", False).get_latest_state()
        self.assertIsInstance(action, dict)

    def test_visit_admin_success(self) -> None:
        sail_form = self.task_set.appian.visitor.visit_admin()
        self.assertTrue(isinstance(sail_form, SailUiForm))

    def test_visit_admin_failure(self) -> None:
        ENV.stats.clear_all()
        self.custom_locust.set_response(ADMIN_URI_PATH, 400, "")
        with self.assertRaises(Exception) as context:
            sail_form = self.task_set.appian.visitor.visit_admin()

    def test_visit_portal_verify_return_type(self) -> None:
        portal_page_form = self.task_set.appian.visitor.visit_portal_page("performance-test", "one")
        self.assertTrue(isinstance(portal_page_form, SailUiForm))

    def test_visit_portal_verify_returned_form_state(self) -> None:
        portal_page_dummy_response = f'{{"portals": "hello"}}'
        self.custom_locust.set_response("/performance-test/_/ui/page/one",
                                        200,
                                        portal_page_dummy_response)
        portal_page_form = self.task_set.appian.visitor.visit_portal_page("performance-test", "one")
        self.assertDictEqual(portal_page_form.get_latest_state(), json.loads(portal_page_dummy_response))

    def test_visit_portal_page_verify_label(self) -> None:
        expected_label = "Portals./performance-test/_/ui/page/one.SailUi"
        portal_page_form = self.task_set.appian.visitor.visit_portal_page("performance-test", "one")
        self.assertEqual(portal_page_form.breadcrumb, expected_label)


if __name__ == '__main__':
    unittest.main()
