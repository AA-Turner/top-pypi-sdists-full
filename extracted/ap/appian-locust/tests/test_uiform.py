import datetime
import json
import unittest
from typing import Any, List, Optional
from unittest.mock import MagicMock, patch

from appian_locust import AppianTaskSet, ComponentNotFoundException
from appian_locust.uiform import SailUiForm, RecordInstanceUiForm
from appian_locust.utilities.helper import (ENV, find_component_by_attribute_in_dict,
                                            find_component_by_index_in_dict,
                                            find_component_by_attribute_and_type_in_dict)
from appian_locust.utilities.url_provider import URL_PROVIDER_V1, URL_PROVIDER_V0
from appian_locust.uiform import PROCESS_TASK_LINK_TYPE
from appian_locust.exceptions import (InvalidComponentException,
                                      ChoiceNotFoundException,
                                      InvalidDateRangeException,
                                      DisabledComponentException,
                                      IgnoredValidationException)
from locust import TaskSet, User
from requests.exceptions import HTTPError

from .mock_client import CustomLocust
from .mock_reader import read_mock_file, read_mock_file_as_dict
from appian_locust._reports import REPORTS_INTERFACE_PATH
from appian_locust._actions import ACTIONS_INTERFACE_PATH, ACTIONS_FEED_PATH
from appian_locust._data_fabric import DATA_FABRIC_URI_PATH

from appian_locust.exceptions import ComponentNotFoundException, ChoiceNotFoundException
from appian_locust.uiform import SailUiForm


class TestSailUiForm(unittest.TestCase):
    reports = read_mock_file("reports_response.json")
    record_instance_response = read_mock_file("record_summary_dashboard_response.json")
    related_action_response = read_mock_file("related_action_response.json")
    spl_response = read_mock_file("test_response.json")
    spl_group_response = read_mock_file("start_process_with_group.json")
    sites_task_report_resp = read_mock_file("sites_task_report.json")
    date_response = read_mock_file("date_task.json")
    multi_dropdown_response = read_mock_file("dropdown_test_ui.json")
    grouped_dropdown_initial = read_mock_file("grouped_dropdown_test_ui.json")
    checkbox_initial = read_mock_file("checkbox_link_duplicate_label.json")
    sail_ui_actions_response = read_mock_file("sail_ui_actions_cmf.json")
    file_upload_initial = read_mock_file("multiple_file_upload_widget.json")
    radio_button_initial = read_mock_file("radio_button_selector.json")
    card_choice_initial = read_mock_file("cardchoice_layout_interface.json")
    validations_not_present = read_mock_file("validations_not_present.json")
    validations_present = read_mock_file("validations_present.json")
    record_action_launch_form_before_refresh = read_mock_file("record_action_launch_form_before_refresh.json")
    record_action_refresh_response = read_mock_file("record_action_refresh_response.json")
    site_with_record_search_button = read_mock_file("site_with_record_search_button.json")
    uiform_click_record_search_button_response = read_mock_file("uiform_click_record_search_button_response.json")
    design_uri = "/suite/rest/a/applications/latest/app/design"
    report_link_uri = "/suite/rest/a/sites/latest/D6JMim/pages/p.reports/report/nXLBqg/reportlink"
    date_task_uri = '/suite/rest/a/task/latest/EMlJYSQyFKe2tvm5/form'
    sites_task_uri = '/suite/rest/a/sites/latest/tst-site/pages/action/action'
    validations_uri = '/suite/rest/a/model/latest/232/form'
    multi_dropdown_uri = "/suite/rest/a/sites/latest/io/page/onboarding-requests/action/34"
    report_name = "Batch Query Report"
    picker_label = '1. Select a Customer'
    picker_value = 'Antilles Transport'
    process_model_form_uri = "/suite/rest/a/model/latest/8/form"
    locust_label = "I am a label"
    reports_interface = read_mock_file("reports_interface.json")
    reports_nav = read_mock_file("reports_nav.json")
    actions = read_mock_file("actions_response.json")
    actions_interface = read_mock_file("actions_interface.json")
    actions_nav = read_mock_file("actions_nav.json")
    actions_feed = read_mock_file("actions_feed.json")
    duplicate_date_field = read_mock_file("duplicate_date_field.json")
    gridfield_async = read_mock_file("gridfield_async.json")
    textfield_async = read_mock_file("textfield_async.json")

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(User(ENV))
        parent_task_set = TaskSet(self.custom_locust)
        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "auth", ["", ""])
        self.task_set = AppianTaskSet(parent_task_set)
        self.task_set.host = ""

        # test_on_start_auth_success is covered here.
        self.custom_locust.set_response("auth?appian_environment=tempo", 200, '{}')
        self.task_set.on_start()

        self.custom_locust.set_response("/suite/rest/a/uicontainer/latest/reports", 200, self.reports)
        ENV.stats.clear_all()
        self.custom_locust.set_response(REPORTS_INTERFACE_PATH, 200, self.reports_interface)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/page/reports/nav", 200, self.reports_nav)
        self.setUp_actions_json()

    def setUp_actions_json(self) -> None:
        self.custom_locust.set_response(
            "auth?appian_environment=tempo", 200, '{}')
        self.custom_locust.set_response(
            "/suite/api/tempo/open-a-case/available-actions?ids=%5B%5D", 200, self.actions)
        self.custom_locust.set_response(ACTIONS_INTERFACE_PATH, 200, self.actions_interface)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/page/actions/nav", 200, self.actions_nav)
        self.custom_locust.set_response(ACTIONS_FEED_PATH, 200, self.actions_feed)

    def test_get_latest_state(self) -> None:
        mock_state = {"a": {"b": 2}}
        mock_url = self.process_model_form_uri
        sail_form = SailUiForm(self.task_set.appian._interactor, mock_state, mock_url)
        returned_state = sail_form.get_latest_state()
        self.assertEqual(mock_state, returned_state)

    def test_if_get_latest_state_returns_deepcopy(self) -> None:
        mock_state = {"a": {"b": 2}}
        mock_url = self.process_model_form_uri
        sail_form = SailUiForm(self.task_set.appian._interactor, mock_state, mock_url)
        returned_state = sail_form.get_latest_state()
        self.assertIsNotNone(returned_state, "Unexpected behavior: returned_state is None")
        if returned_state is not None:
            returned_state["b"] = 45
            """
            If we don't return deep copy, then change in returned_state dict should result in
            same change in mock_state dict as well, and ultimately both should be equal.
            """
            self.assertNotEqual(mock_state, returned_state)

    def test_reports_form_example_fail(self) -> None:
        self.custom_locust.set_response(self.report_link_uri,
                                        500, '{}')
        with self.assertRaises(HTTPError):
            self.task_set.appian.visitor.visit_report(self.report_name, False)

    def test_reports_form_modify_grid(self) -> None:
        form_label = 'Top Sales Reps by Total Sales'
        report_form = read_mock_file("report_with_rep_sales_grid.json")
        self.custom_locust.set_response(self.report_link_uri,
                                        200, report_form)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, False)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/p.reports/report/yS9bXA/reportlink",
                                        200, report_form)

        keyWords: List[dict] = [{'label': form_label}, {'index': 0}]
        for i in range(len(keyWords)):
            keyword_args: dict = keyWords[i]
            sail_form.move_to_beginning_of_paging_grid(**keyword_args)
            sail_form.move_to_end_of_paging_grid(**keyword_args)
            sail_form.move_to_left_in_paging_grid(**keyword_args)
            sail_form.move_to_right_in_paging_grid(**keyword_args)
            keyword_args['field_name'] = 'Total'
            sail_form.sort_paging_grid(**keyword_args)

    def test_reports_form_modify_grid_errors(self) -> None:
        report_form = read_mock_file("report_with_rep_sales_grid.json")
        self.custom_locust.set_response(self.report_link_uri,
                                        200, report_form)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, False)
        with self.assertRaisesRegex(Exception, "Grid with label 'dummy_label' not found in form") as context:
            sail_form.move_to_beginning_of_paging_grid(label='dummy_label')
        with self.assertRaisesRegex(Exception, "Index 5 out of range"):
            sail_form.move_to_left_in_paging_grid(index=5)
        with self.assertRaisesRegex(Exception, "Cannot sort, field 'Abc' not found"):
            sail_form.sort_paging_grid(index=0, field_name='Abc')
        with self.assertRaisesRegex(Exception, "Field to sort cannot be blank"):
            sail_form.sort_paging_grid(index=0)

    def test_paging_grid_sort_by_label_finds_grid(self) -> None:
        report_form = read_mock_file("paging_grid_sortable.json")
        self.custom_locust.set_response(self.report_link_uri, 200, report_form)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, False)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/p.reports/report/TNCDrA/reportlink", 200, report_form)
        sail_form.sort_paging_grid(label=" Dogs", field_name="Name")

    def test_datatype_caching(self) -> None:
        body_with_types = read_mock_file("page_resp.json")
        self.custom_locust.set_response(self.report_link_uri,
                                        200, body_with_types)
        self.task_set.appian.visitor.visit_report(self.report_name, False)
        self.assertEqual(len(self.task_set.appian._interactor.datatype_cache._cached_datatype), 105)

        self.task_set.appian.visitor.visit_report(self.report_name, False)
        self.assertEqual(len(self.task_set.appian._interactor.datatype_cache._cached_datatype), 105)

    def test_deployments_click_tab(self) -> None:
        design_landing_page_response = read_mock_file("design_landing_page.json")
        deployment_tab_response = read_mock_file("design_deployments_ui.json")
        deployment_outgoing_tab_response = read_mock_file("design_deployments_outgoing_tab.json")

        self.custom_locust.set_response(self.design_uri,
                                        200, design_landing_page_response)
        design_sail_form = self.task_set.appian.visitor.visit_design()

        self.custom_locust.set_response(self.design_uri,
                                        200, deployment_tab_response)
        deployments_sail_form = design_sail_form.click("Deployments")

        self.custom_locust.set_response("/suite/rest/a/applications/latest/app/design/deployments",
                                        200, deployment_outgoing_tab_response)
        outgoing_tab_form = deployments_sail_form.click_tab_by_label("Outgoing", "deployment-secondary-tabs")

        component = find_component_by_attribute_in_dict("label", "OneApp", outgoing_tab_form.get_latest_state())
        self.assertEqual("OneApp", component.get('label'))

    def test_deployments_click_tab_exception(self) -> None:
        deployment_tab_response = read_mock_file("design_deployments_ui.json")
        design_landing_page_response = read_mock_file("design_landing_page.json")
        self.custom_locust.set_response(self.design_uri,
                                        200, design_landing_page_response)
        design_sail_form = self.task_set.appian.visitor.visit_design()

        self.custom_locust.set_response(self.design_uri,
                                        200, deployment_tab_response)
        deployments_sail_form = design_sail_form.click("Deployments")
        with self.assertRaisesRegex(Exception, "Cannot click a tab with label: 'DoesNotExistLabel' inside the TabButtonGroup component"):
            deployments_sail_form.click_tab_by_label("DoesNotExistLabel", "deployment-secondary-tabs")

    def test_fill_text_field(self) -> None:
        report_body = read_mock_file("text_fields_same_label.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(report_name=self.report_name, exact_match=False)

        label = 'Text'
        value = 'Filling out the form...'
        sail_form.fill_text_field(label, value)

    def test_fill_text_field_by_index(self) -> None:
        report_body = read_mock_file("text_fields_same_label.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(report_name=self.report_name, exact_match=False)

        label = 'Text'
        value = 'Filling out the form...'
        index = 1
        sail_form.fill_text_field(label, value, index=index)

    def test_fill_text_field_no_fields(self) -> None:
        report_body = read_mock_file("text_fields_same_label.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        label = 'Non-existant label'
        value = 'Filling out the form...'
        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.fill_text_field(label, value)
        self.assertEqual(
            context.exception.args[0], f"No components with label 'Non-existant label' found on page")

    def test_fill_text_field_out_of_bounds_index(self) -> None:
        report_body = read_mock_file("text_fields_same_label.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        label = 'Text'
        value = 'Filling out the form...'
        index = 3
        with self.assertRaisesRegex(Exception, "Component found but index: '3' out of range"):
            sail_form.fill_text_field(label, value, index=index)

    def test_fill_text_field_zero_index(self) -> None:
        report_body = read_mock_file("text_fields_same_label.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        label = 'Text'
        value = 'Filling out the form...'
        index = 0
        with self.assertRaisesRegex(Exception, "Invalid index: '0'. Please enter a positive number. Indexing is 1-based to match SAIL indexing convention"):
            sail_form.fill_text_field(label, value, index=index)

    def test_fill_text_field_negative_index(self) -> None:
        report_body = read_mock_file("text_fields_same_label.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        label = 'Text'
        value = 'Filling out the form...'
        index = -1
        with self.assertRaisesRegex(Exception, "Invalid index: '-1'. Please enter a positive number"):
            sail_form.fill_text_field(label, value, index=index)

    def test_fill_picker_field_interaction(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        picker_widget_suggestions = read_mock_file("picker_widget_suggestions.json")
        picker_widget_selected = read_mock_file("picker_widget_selected.json")

        self.custom_locust.enqueue_response(200, picker_widget_suggestions)
        self.custom_locust.enqueue_response(200, picker_widget_selected)

        sail_form = SailUiForm(self.task_set.appian._interactor, sail_ui_actions_cmf)

        label = self.picker_label
        value = self.picker_value
        sail_form.fill_picker_field(label, value)

    def test_fill_picker_field_user(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        picker_widget_selected = read_mock_file("picker_widget_selected.json")
        label = '1. Select a Customer'
        resp = {
            'testLabel': f'test-{label}',
            '#t': 'PickerWidget',
            'suggestions': [{'identifier': {'id': 1, "#t": "User"}}],
            'saveInto': {},
            '_cId': "abc"
        }
        self.custom_locust.enqueue_response(200, json.dumps(resp))
        self.custom_locust.enqueue_response(200, picker_widget_selected)
        sail_form = SailUiForm(self.task_set.appian._interactor, sail_ui_actions_cmf)

        value = 'Admin User'
        sail_form.fill_picker_field(label, value)

    def test_fill_picker_field_suggestions_identifier_is_code(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        picker_widget_suggestions = read_mock_file("picker_widget_suggestions_code.json")
        picker_widget_selected = read_mock_file("picker_widget_selected.json")

        self.custom_locust.enqueue_response(200, picker_widget_suggestions)
        self.custom_locust.enqueue_response(200, picker_widget_selected)
        sail_form = SailUiForm(self.task_set.appian._interactor, sail_ui_actions_cmf)

        label = self.picker_label
        value = 'GAC Guyana'

        sail_form.fill_picker_field(label, value, identifier='code')

    def test_fill_picker_field_no_suggestions(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        picker_widget_suggestions = read_mock_file("picker_widget_no_suggestions.json")

        self.custom_locust.enqueue_response(200, picker_widget_suggestions)
        sail_form = SailUiForm(self.task_set.appian._interactor, sail_ui_actions_cmf)

        label = self.picker_label
        value = 'You will not find me'
        with self.assertRaises(Exception) as context:
            sail_form.fill_picker_field(label, value)
        self.assertEqual(context.exception.args[0], "No identifiers found when 'You will not find me' was entered in the picker field.")

    def test_fill_picker_field_no_response(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        self.custom_locust.enqueue_response(200, '{}')
        sail_form = SailUiForm(self.task_set.appian._interactor, sail_ui_actions_cmf)

        label = self.picker_label
        value = 'You will not find me'
        with self.assertRaisesRegex(Exception, "No response returned"):
            sail_form.fill_picker_field(label, value)

    def test_fill_picker_field_no_identifiers(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        label = self.picker_label
        resp = {
            'testLabel': f'test-{label}',
            '#t': 'PickerWidget',
            'suggestions': [{'a': 'b'}]
        }
        self.custom_locust.enqueue_response(200, json.dumps(resp))
        sail_form = SailUiForm(self.task_set.appian._interactor, sail_ui_actions_cmf)

        value = self.picker_value
        with self.assertRaisesRegex(Exception, "No identifiers found"):
            sail_form.fill_picker_field(label, value)

    def test_fill_picker_field_not_id_or_v(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        label = self.picker_label
        resp = {
            'testLabel': f'test-{label}',
            '#t': 'PickerWidget',
            'suggestions': [{'identifier': {'idx': 1}}]
        }
        self.custom_locust.enqueue_response(200, json.dumps(resp))
        sail_form = SailUiForm(self.task_set.appian._interactor, sail_ui_actions_cmf)

        value = self.picker_value
        with self.assertRaisesRegex(Exception, "Could not extract picker values"):
            sail_form.fill_picker_field(label, value)

    def test_fill_picker_field_interaction_no_selection_resp(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        picker_widget_suggestions = read_mock_file("picker_widget_suggestions.json")

        self.custom_locust.enqueue_response(200, picker_widget_suggestions)
        self.custom_locust.enqueue_response(200, '{}')

        sail_form = SailUiForm(self.task_set.appian._interactor, sail_ui_actions_cmf)

        label = self.picker_label
        value = self.picker_value
        with self.assertRaisesRegex(Exception, 'No response returned'):
            sail_form.fill_picker_field(label, value)

    def test_upload_document_invalid_component(self) -> None:
        with self.assertRaisesRegex(Exception, 'Provided component was not a FileUploadWidget'):
            label = 'my_label'
            ui = {
                'contents': [

                    {
                        "contents": {
                            "label": label,
                            "#t": "Some other thing"
                        },
                        "label": label,
                        "labelPosition": "ABOVE",
                        "instructions": "",
                        "instructionsPosition": "",
                        "helpTooltip": "Upload an application or a multi-patch package",
                        "requiredStyle": "",
                        "skinName": "",
                        "marginBelow": "",
                        "accessibilityText": "",
                        "#t": "FieldLayout"
                    },
                ]
            }
            sail_form = SailUiForm(self.task_set.appian._interactor, ui)
            sail_form.upload_document_to_upload_field(label, 'fake_file')

    def test_upload_document_missing_file(self) -> None:
        file = 'fake_file'
        with self.assertRaisesRegex(Exception, f"No such file or directory: '{file}'"):
            label = 'my_label'
            ui = {
                'contents': [

                    {
                        "label": label,
                        "labelPosition": "ABOVE",
                        "instructions": "",
                        "instructionsPosition": "",
                        "helpTooltip": "Upload an application or a multi-patch package",
                        "requiredStyle": "",
                        "skinName": "",
                        "marginBelow": "",
                        "accessibilityText": "",
                        "#t": "FileUploadWidget"
                    },
                ]
            }
            sail_form = SailUiForm(self.task_set.appian._interactor, ui)
            sail_form.upload_document_to_upload_field(label, file)

    def test_multi_upload_document_invalid_component(self) -> None:
        with self.assertRaisesRegex(Exception, 'Provided component was not a MultipleFileUploadWidget'):
            label = 'Form'
            ui = ui = {
                'contents': [

                    {
                        "label": label,
                        "labelPosition": "ABOVE",
                        "instructions": "",
                        "instructionsPosition": "",
                        "helpTooltip": "Upload an application or a multi-patch package",
                        "requiredStyle": "",
                        "skinName": "",
                        "marginBelow": "",
                        "accessibilityText": "",
                        "#t": "FormLayout"
                    },
                ]
            }
            sail_form = SailUiForm(self.task_set.appian._interactor, ui)
            sail_form.upload_documents_to_multiple_file_upload_field(label, ['fake_file'])

    def test_multi_upload_document_invalid_file(self) -> None:
        with self.assertRaisesRegex(FileNotFoundError, "No such file or directory: "):
            ui = json.loads(self.file_upload_initial)
            label = 'File Upload 5'
            sail_form = SailUiForm(self.task_set.appian._interactor, ui)
            sail_form.upload_documents_to_multiple_file_upload_field(label, ['fake_file'])

    @patch('appian_locust.uiform.SailUiForm.upload_documents_to_multiple_file_upload_field')
    def test_single_to_multi_upload_document(self, mock_upload_documents_to_multiple_file_upload_field: MagicMock) -> None:
        ui = json.loads(self.file_upload_initial)
        label = 'File Upload 5'
        sail_form = SailUiForm(self.task_set.appian._interactor, ui)
        sail_form.upload_document_to_upload_field(label, 'fake_file')
        mock_upload_documents_to_multiple_file_upload_field.assert_called_once()
        args, kwargs = mock_upload_documents_to_multiple_file_upload_field.call_args_list[0]
        self.assertEqual(args[1], ['fake_file'])

    @patch('os.path.exists', return_value=True)
    @patch('appian_locust._interactor._Interactor.upload_document_to_field')
    @patch('appian_locust._interactor._Interactor.upload_document_to_server')
    def test_single_to_multi_upload_document_to_server(self, mock_upload_document_to_server: MagicMock,
                                                       mock_upload_document_to_field: MagicMock,
                                                       mock_os_path_exists: MagicMock) -> None:
        ui = json.loads(self.file_upload_initial)
        label = 'File Upload 5'
        sail_form = SailUiForm(self.task_set.appian._interactor, ui)

        sail_form.upload_document_to_upload_field(label, 'fake_file')

        mock_upload_document_to_server.assert_called_once_with('fake_file', is_encrypted=False, validate_extensions=True)
        mock_upload_document_to_field.assert_called_once()

    @patch('appian_locust.uiform.SailUiForm.upload_document_to_upload_field')
    def test_multi_to_single_upload_document(self, mock_upload_document_to_upload_field: MagicMock) -> None:
        ui = json.loads(self.file_upload_initial)
        label = 'File Upload 4'
        sail_form = SailUiForm(self.task_set.appian._interactor, ui)
        sail_form.upload_documents_to_multiple_file_upload_field(label, ['fake_file'])
        mock_upload_document_to_upload_field.assert_called_once()
        args, _ = mock_upload_document_to_upload_field.call_args_list[0]

    @patch('os.path.exists', return_value=True)
    @patch('appian_locust._interactor._Interactor.upload_document_to_field')
    @patch('appian_locust._interactor._Interactor.upload_document_to_server')
    def test_multi_upload_duplicate_label(self, mock_upload_document_to_server: MagicMock, mock_upload_document_to_field: MagicMock,  mock_os_path_exists: MagicMock) -> None:
        ui = json.loads(read_mock_file("upload_field_multi_index.json"))
        label = "ASE"
        sail_form = SailUiForm(self.task_set.appian._interactor, ui)

        sail_form.upload_documents_to_multiple_file_upload_field(label, ['fake_file'], index=2)

        args, _ = mock_upload_document_to_field.call_args_list[0]
        component = args[1]
        self.assertEqual(component["_cId"], "6727f939a82122fcf913822c444b7464")

    def test_click_related_action_on_record_form(self) -> None:
        self.custom_locust.set_response('/suite/rest/a/record/latest/BE5pSw/ioBHer_bdD8Emw8hMSiA_CnpxaK0CVK61sPetEqM0lI_pHvjAsXVOlJtUo/actions/'
                                        'ioBHer_bdD8Emw8hMSiA_CnpxaA0SVKp1kzE9BURlYvkxHjzPlX0d81Hmk',
                                        200,
                                        self.related_action_response)
        record_instance_header_form = RecordInstanceUiForm(self.task_set.appian._interactor, json.loads(self.record_instance_response), summary_view=False)
        # perform a related action
        record_instance_related_action_form = record_instance_header_form.click_related_action("Discuss Case History")

        # Assert fields on the related action form
        text_component = find_component_by_attribute_in_dict('label', 'Action Type', record_instance_related_action_form.get_latest_state())
        self.assertEqual(text_component.get("#t"), "TextField")

    def test_click_related_action_link_on_summary_dashboard(self) -> None:
        related_action_dialog_response = read_mock_file("related_action_in_a_dialog_response.json")
        record_instance_with_related_action_link_response = read_mock_file("record_summary_with_related_action_response.json")

        # Mocking the response for related action
        self.custom_locust.set_response('/suite/rest/a/record/latest/lMBIWonPMarTw_zHV5oHY7Qv6e46NZWjhAVMg-o7QVtt-3W0zJoYQxILKZhEkSJs0tCAhEektXxP2N01AkR32ISfkpTKGeoz4L6tNR8PBwsRRWEtw/'
                                        'actionDialog/iwBIWonPMarTw_zHTsSC5HBmvtUFIZ8Nar8xAVLL-EvREVFV-D4OAWQ4z8a2Q',
                                        200, related_action_dialog_response)

        record_instance_summary_form = RecordInstanceUiForm(self.task_set.appian._interactor, json.loads(record_instance_with_related_action_link_response))
        # perform a related action that opens in a dialog (which is a on the summary dashboard itself)
        record_instance_related_action_form = record_instance_summary_form.click_related_action("Document Reconciliation")

        # Assert fields on the related action form
        dropdown_component = find_component_by_attribute_in_dict('label', 'Document Type', record_instance_related_action_form.get_latest_state())
        self.assertEqual(dropdown_component.get("#t"), "DropdownField")

    @patch('appian_locust._interactor._Interactor.click_related_action')
    def test_click_related_action_with_test_label(self, mock_click_related_action: MagicMock) -> None:
        sail_ui_record_action = json.loads(self.record_action_launch_form_before_refresh)
        sail_form = SailUiForm(self.task_set.appian._interactor, sail_ui_record_action)

        sail_form.click_related_action("updateTable1-1", is_test_label=True)

        args, _ = mock_click_related_action.call_args_list[0]

        self.assertEqual(args[0]['label'], "Update Table 1 (Dup) (PSF)")

    @patch('appian_locust.uiform.SailUiForm._reconcile_state')
    @patch('appian_locust._interactor._Interactor.click_generic_element')
    def test_evaluate_record_action_field_security_by_test_label(self, mock_trigger_security: MagicMock, mock_reconcile_state: MagicMock) -> None:
        sail_ui_record_action = json.loads(self.record_action_launch_form_before_refresh)
        sail_form = SailUiForm(self.task_set.appian._interactor, sail_ui_record_action)

        sail_form.evaluate_record_action_field_security(test_label="my-record-action-field-access-text-21")

        args, kwargs = mock_trigger_security.call_args_list[0]

        # trigger method should have record_action_field as a param
        record_action_field_cid = "c5d475751b05967c681daebde0a86159qqq"

        self.assertEqual(args[1]['_cId'], record_action_field_cid)
        self.assertTrue(args[1]['securityOnDemand'])

    @patch('appian_locust.uiform.SailUiForm._reconcile_state')
    @patch('appian_locust._interactor._Interactor.click_generic_element')
    def test_evaluate_record_action_field_security_by_index(self, mock_trigger_security: MagicMock, mock_reconcile_state: MagicMock) -> None:
        sail_ui_record_action = json.loads(self.record_action_launch_form_before_refresh)
        sail_form = SailUiForm(self.task_set.appian._interactor, sail_ui_record_action)

        sail_form.evaluate_record_action_field_security(index=2)

        args, kwargs = mock_trigger_security.call_args_list[0]

        # trigger method should have record_action_field as a param
        record_action_field_cid = "c5d475751b05967c681daebde0a86159qqq"

        self.assertEqual(args[1]['_cId'], record_action_field_cid)
        self.assertTrue(args[1]['securityOnDemand'])

    @patch('appian_locust._interactor._Interactor.click_start_process_link')
    def test_click_start_process_link(self, mock_click_spl: MagicMock) -> None:
        test_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.spl_response))
        mock_component_object = {
            "processModelOpaqueId": "iQB8GmxIr5iZT6YnVytCx9QKdJBPaRDdv_-hRj3HM747ZtRjSw",
            "cacheKey": "c93e2f33-06eb-42b2-9cfc-2c4a0e14088e"
        }
        test_form._click_start_process_link("z1ck30E1", "home", None, False, component=mock_component_object,
                                            locust_request_label="I am a label!")

        mock_click_spl.assert_called_once()
        args, kwargs = mock_click_spl.call_args_list[0]

        self.assertEqual(kwargs['component'], mock_component_object)
        self.assertEqual(kwargs['process_model_opaque_id'], "iQB8GmxIr5iZT6YnVytCx9QKdJBPaRDdv_-hRj3HM747ZtRjSw")
        self.assertEqual(kwargs['cache_key'], "c93e2f33-06eb-42b2-9cfc-2c4a0e14088e")
        self.assertEqual(kwargs['is_mobile'], False)
        self.assertEqual(kwargs['locust_request_label'], "I am a label!")

    def test_click_start_process_link_with_group(self) -> None:
        test_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.spl_group_response))
        processModelOpaqueId = "iIBCbKan8kNUdA5Ncjzwr9UnD7wJjYmZdCufbWETWwhuG2e",
        cacheKey = "2141c24b-2dd2-44db-a390-5515e3d154d1"
        resp = '{"it": "worked"}'
        self.custom_locust.set_response(
            f"/suite/rest/a/sites/latest/test_site/page/g.first.p.it/startProcess/iIBCbKan8kNUdA5Ncjzwr9UnD7wJjYmZdCufbWETWwhuG2e?cacheKey=2141c24b-2dd2-44db-a390-5515e3d154d1",
            200,
            resp
        )

        self.task_set.appian._interactor.set_url_provider(URL_PROVIDER_V1)
        test_form.click_start_process_link(label="ASE")
        self.task_set.appian._interactor.set_url_provider(URL_PROVIDER_V0)

        self.assertEqual(json.loads(resp), test_form.get_latest_state())

    @patch('appian_locust.uiform.SailUiForm._click_start_process_link')
    def test_click_card_layout_by_index_spl(self, mock_click_spl: MagicMock) -> None:
        test_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.spl_response))
        test_form_state = test_form.get_latest_state()
        self.assertIsNotNone(test_form_state, "Unexpected behavior: test form state is None")
        if test_form_state is not None:
            component = find_component_by_attribute_and_type_in_dict('label', 'Request Pass', 'StartProcessLink', test_form_state)
        test_form.click_card_layout_by_index(1, locust_request_label=self.locust_label)

        mock_click_spl.assert_called_once()
        args, kwargs = mock_click_spl.call_args_list[0]

        self.assertTupleEqual(args, ('z1ck30E1', 'home', None, False, component))
        self.assertEqual(kwargs["locust_request_label"], self.locust_label)

    @patch('appian_locust._interactor._Interactor.click_component')
    def test_click_card_layout_by_index_other_link(self, mock_click_component: MagicMock) -> None:
        test_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.spl_response))

        def get_call(name: str) -> Optional[Any]:
            return {
                'uuid': test_form.uuid,
                'context': test_form.context
            }.get(name)

        mock_state = MagicMock()
        mock_state.get.side_effect = get_call
        mock_click_component.return_value = mock_state
        test_form_state = test_form.get_latest_state()
        self.assertIsNotNone(test_form_state, "Unexpected behavior: test_form_state is None")
        if test_form_state is not None:
            component = find_component_by_index_in_dict("DynamicLink", 3, test_form_state)
        test_form.click_card_layout_by_index(3, locust_request_label=self.locust_label)

        mock_click_component.assert_called_once()
        args, kwargs = mock_click_component.call_args_list[0]
        self.assertEqual(args[0], "/suite/rest/a/sites/latest/z1ck30E1/pages/home/report")
        self.assertEqual(args[1], component)
        self.assertEqual(args[2], test_form.context)
        self.assertEqual(args[3], test_form.uuid)
        self.assertEqual(kwargs["label"], self.locust_label)

    @patch('appian_locust._interactor._Interactor.select_radio_button')
    def test_radio_button_select_by_label(self, mock_radio_select_component: MagicMock) -> None:
        test_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.radio_button_initial))
        test_form_state = test_form.get_latest_state()
        self.assertIsNotNone(test_form_state, "Unexpected behavior: test_form_state is None")
        if test_form_state is not None:
            component = find_component_by_attribute_in_dict("label", "Cool Buttons", test_form_state)
        test_uuid = test_form.uuid
        test_context = test_form.context
        test_form.select_radio_button_by_label("Cool Buttons", 1, locust_request_label=self.locust_label)
        mock_radio_select_component.assert_called_once()
        args, kwargs = mock_radio_select_component.call_args_list[0]
        self.assertEqual(args[0], self.report_link_uri)
        self.assertEqual(args[1], component)
        self.assertEqual(args[2], test_context)
        self.assertEqual(args[3], test_uuid)
        self.assertEqual(kwargs["context_label"], self.locust_label)

    @patch('appian_locust._interactor._Interactor.click_generic_element')
    def test_card_choice_field_select_by_label(self, mock_radio_select_component: MagicMock) -> None:
        uri = "/suite/rest/a/sites/latest/test01/pages/test01/interface"
        test_form = SailUiForm(self.task_set.appian._interactor,
                               json.loads(self.card_choice_initial),
                               uri)
        test_form_state = test_form.get_latest_state()
        self.assertIsNotNone(test_form_state, "Unexpected behavior: test_form_state is None")
        if test_form_state is not None:
            component = find_component_by_attribute_in_dict("testLabel", "cardChoiceField-Card Choices", test_form_state)
        index = 2
        test_uuid = test_form.uuid
        test_context = test_form.context
        test_new_value = {
            "#t": "Variant?list",
            "#v": [component["identifiers"][index - 1]]
        }
        test_form.select_card_choice_field_by_label("Card Choices", index, locust_request_label=self.locust_label)
        mock_radio_select_component.assert_called_once()
        args, kwargs = mock_radio_select_component.call_args_list[0]
        self.assertEqual(args[0], uri)
        self.assertEqual(args[1], component)
        self.assertEqual(args[2], test_context)
        self.assertEqual(args[3], test_uuid)
        self.assertEqual(kwargs["new_value"], test_new_value)
        self.assertEqual(kwargs["label"], self.locust_label)

    def test_click_card_layout_by_index_no_link(self) -> None:
        test_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.spl_response))

        with self.assertRaisesRegex(Exception, "CardLayout found at index: 2 does not have a link on it"):
            test_form.click_card_layout_by_index(2)

    def _setup_date_form(self) -> SailUiForm:
        self.custom_locust.set_response(self.date_task_uri, 200, self.date_response)
        test_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.date_response))
        return test_form

    def _setup_multi_dropdown_form(self) -> SailUiForm:
        self.custom_locust.set_response(self.multi_dropdown_uri, 200, self.multi_dropdown_response)
        test_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.multi_dropdown_response))
        return test_form

    def _setup_action_response_with_ui(self, file_name: str = "form_content_response.json") -> None:
        action = self.task_set.appian.actions_info.get_action_info("Create a Case", False)
        resp_json = read_mock_file(file_name)
        self.custom_locust.set_response(action['formHref'], 200, resp_json)

    def test_reconcile_ui_changes_context(self) -> None:
        # State one
        test_form = self._setup_date_form()
        original_uuid = test_form.uuid
        original_context = test_form.context
        # State two, different uuid
        new_state = json.loads(self.spl_response)

        test_form._reconcile_state(new_state)

        self.assertNotEqual(test_form.uuid, original_uuid)
        self.assertNotEqual(test_form.context, original_context)
        self.assertEqual(test_form.uuid, new_state['uuid'])
        self.assertEqual(test_form.context, new_state['context'])

    def _unwrap_value(self, json_str: str) -> str:
        return json.loads(json_str)['updates']['#v'][0]['value']['#v']

    def test_fill_datefield_not_found(self) -> None:
        test_form = self._setup_date_form()
        with self.assertRaises(ComponentNotFoundException) as context:
            test_form.fill_date_field('Datey', datetime.date.today())
        self.assertEqual(context.exception.args[0], "No components with label 'Datey' found on page")

    def test_fill_datefield_success(self) -> None:
        test_form = self._setup_date_form()
        test_form.fill_date_field('Date', datetime.date(1990, 1, 5))

        last_request = self.custom_locust.get_request_list().pop()
        self.assertEqual('post', last_request['method'])
        self.assertEqual(self.date_task_uri, last_request['path'])
        self.assertEqual('1990-01-05Z', self._unwrap_value(last_request['data']))

    @patch("appian_locust._interactor._Interactor.update_date_field")
    def test_fill_datefield_duplicate(self, mock_update_datefield: MagicMock) -> None:
        test_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.duplicate_date_field))

        test_form.fill_date_field('ASE', datetime.date(1990, 1, 5), 2)

        args, _ = mock_update_datefield.call_args_list[0]

        self.assertEqual(args[1]["_cId"], "f007b725f8b0903f70179b3307fa0b96")

    def test_get_dropdown_choices_multiple(self) -> None:
        resp_json = read_mock_file(file_name='dropdown_test_ui.json')
        ui_form = SailUiForm(self.task_set.appian._interactor, json.loads(resp_json))
        choices = ui_form.get_dropdown_items("Customer Type")
        self.assertEqual(["-- Please select a value --",
                          "Buy Side Asset Manager",
                          "Corporate Banking",
                          "Institutional Investor",
                          "Sell Side ",
                          "SME Banking"], choices)

    def test_get_dropdown_choices_errors(self) -> None:
        resp_json = read_mock_file(file_name='dropdown_test_ui.json')
        ui_form = SailUiForm(self.task_set.appian._interactor, json.loads(resp_json))
        with self.assertRaises(ComponentNotFoundException):
            ui_form.get_dropdown_items("Dropdown that DNE")
        with self.assertRaises(ComponentNotFoundException):
            ui_form.get_dropdown_items("Domicile")

    def test_empty_get_dropdown_choices(self) -> None:
        state = {'ui': [{'label': "Empty Dropdown", 'choices': [], '#t': 'DropdownField'}]}
        ui_form = SailUiForm(self.task_set.appian._interactor, state)
        self.assertEqual([], ui_form.get_dropdown_items("Empty Dropdown"))

    def test_select_multi_dropdown_success(self) -> None:
        test_form = self._setup_multi_dropdown_form()
        test_form.select_multi_dropdown_item('Regions', ["Asia", "Africa and Middle East"])
        last_request = self.custom_locust.get_request_list().pop()
        self.assertEqual('post', last_request['method'])
        self.assertEqual(self.multi_dropdown_uri, last_request['path'])
        self.assertEqual([1, 2], self._unwrap_value(last_request["data"]))

    @patch('appian_locust._interactor._Interactor.select_checkbox_item')
    def test_check_checkbox_by_label(self, mock_select_checkbox_item: MagicMock) -> None:
        test_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.checkbox_initial))
        test_context = test_form.context
        test_uuid = test_form.uuid
        test_form.check_checkbox_by_label("Label 1", [1])

        mock_select_checkbox_item.assert_called_once()
        args, _ = mock_select_checkbox_item.call_args_list[0]
        component = args[1]
        assert component.get(
            '#t') == 'CheckboxField', f"Expected component type to be 'CheckboxField', but got component type {component.get('#t')} in the following arguments: {component}"
        self.assertEqual(args[2], test_context)
        self.assertEqual(args[3], test_uuid)

    def test_fill_datetimefield_not_found(self) -> None:
        test_form = self._setup_date_form()
        with self.assertRaises(ComponentNotFoundException) as context:
            test_form.fill_datetime_field('Dt', datetime.datetime.now())
        self.assertEqual(context.exception.args[0], "No components with label 'Dt' found on page")

    def test_fill_datetimefield_success(self) -> None:
        test_form = self._setup_date_form()
        test_form.fill_datetime_field('Date Time', datetime.datetime(1990, 1, 2, 1, 30, 50))

        last_request = self.custom_locust.get_request_list().pop()
        self.assertEqual('post', last_request['method'])
        self.assertEqual(self.date_task_uri, last_request['path'])
        self.assertEqual('1990-01-02T01:30:00Z', self._unwrap_value(last_request['data']))

    @patch("appian_locust._interactor._Interactor.update_datetime_field")
    def test_fill_datetimefield_duplicate(self, mock_update_datetimefield: MagicMock) -> None:
        test_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.duplicate_date_field))

        test_form.fill_datetime_field('ASE', datetime.datetime(1990, 1, 2, 1, 30, 50), 2)

        args, _ = mock_update_datetimefield.call_args_list[0]

        self.assertEqual(args[1]["_cId"], "edd49aa24df6d7888f8cd02a818fcc0e")

    def _setup_grid_form(self) -> SailUiForm:
        uri = self.sites_task_uri
        self.custom_locust.set_response(uri, 200, self.sites_task_report_resp)
        test_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.sites_task_report_resp))
        return test_form

    def test_select_grid_row_success(self) -> None:
        test_form = self._setup_grid_form()
        test_form.select_rows_in_grid([2], "My Tasks")

        last_request = self.custom_locust.get_request_list().pop()
        self.assertEqual('post', last_request['method'])
        self.assertEqual(self.sites_task_uri, last_request['path'])

        update = json.loads(last_request['data'])['updates']['#v'][0]['value']
        self.assertEqual("GridSelection", update['#t'])
        selected_list = update['selected']
        self.assertEqual(1, len(selected_list))
        selected = selected_list[0]
        self.assertEqual("int", selected['#t'])
        self.assertEqual(268435892, selected['#v'])

    def test_multi_select_grid_row_success(self) -> None:
        test_form = self._setup_grid_form()
        test_form.select_rows_in_grid([0, 2], "My Tasks")

        last_request = self.custom_locust.get_request_list().pop()
        self.assertEqual('post', last_request['method'])
        self.assertEqual(self.sites_task_uri, last_request['path'])

        update = json.loads(last_request['data'])['updates']['#v'][0]['value']
        self.assertEqual("GridSelection", update['#t'])
        selected_list = update['selected']
        self.assertEqual(2, len(selected_list))

        first_selected = selected_list[0]
        self.assertEqual("int", first_selected['#t'])
        self.assertEqual(536871411, first_selected['#v'])

        second_selected = selected_list[1]
        self.assertEqual("int", second_selected['#t'])
        self.assertEqual(268435892, second_selected['#v'])

    def test_select_grid_row_append_success(self) -> None:
        test_form = self._setup_grid_form()
        test_form.select_rows_in_grid([0], "My Tasks", append_to_existing_selected=True)

        last_request = self.custom_locust.get_request_list().pop()
        self.assertEqual('post', last_request['method'])
        self.assertEqual(self.sites_task_uri, last_request['path'])

        update = json.loads(last_request['data'])['updates']['#v'][0]['value']
        self.assertEqual("GridSelection", update['#t'])
        selected_list = update['selected']
        self.assertEqual(2, len(selected_list))

        first_selected = selected_list[0]
        self.assertEqual("int", first_selected['#t'])
        self.assertEqual(268435892, first_selected['#v'])

        second_selected = selected_list[1]
        self.assertEqual("int", second_selected['#t'])
        self.assertEqual(536871411, second_selected['#v'])

    def test_dispatch_click_task_no_id(self) -> None:
        sites_task_report = SailUiForm(self.task_set.appian._interactor, json.loads(self.sites_task_report_resp))
        component = {'#t': PROCESS_TASK_LINK_TYPE, 'label': "my task"}
        with self.assertRaisesRegex(Exception, "No task id found for task with name 'my task'"):
            sites_task_report._dispatch_click(component, 'no label')

    def test_dispatch_click_task_with_id(self) -> None:
        sites_task_report = SailUiForm(self.task_set.appian._interactor, json.loads(self.sites_task_report_resp))
        initial_uuid = sites_task_report.uuid
        initial_context = sites_task_report.context
        task_to_accept = read_mock_file('task_accept_resp.json')
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/Bs3k2OfS55jCOcMb5D/status",
            200,
            task_to_accept
        )
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/Bs3k2OfS55jCOcMb5D/attributes",
            200,
            """{
            "isOfflineTask": false,
            "isSailTask": true,
            "isQuickTask": false,
            "taskId": "Bs3k2OfS55jCOcMb5D",
            "isAutoAcceptable": "true"
            }""")
        sites_task_report.click('Issue recommendation')

        task_to_accept_state = json.loads(task_to_accept)

        self.assertNotEqual(initial_uuid, sites_task_report.uuid)
        self.assertNotEqual(initial_context, sites_task_report.context)
        self.assertEqual(task_to_accept_state['uuid'], sites_task_report.uuid)
        self.assertEqual(task_to_accept_state['context'], sites_task_report.context)

        sites_task_report_state = sites_task_report.get_latest_state()
        self.assertIsNotNone(sites_task_report_state, "Unexpected behavior: sites_task_report_state is None")
        if sites_task_report_state is not None:
            # Assert ui state updated
            self.assertEqual('Available Case Workers',
                             find_component_by_attribute_in_dict('label', 'Available Case Workers', sites_task_report_state).get('label')
                             )

    def test_refresh_after_record_action_interaction(self) -> None:
        sail_ui_record_action_before = json.loads(self.record_action_launch_form_before_refresh)

        self.custom_locust.enqueue_response(200, self.record_action_refresh_response)

        sail_form = SailUiForm(self.task_set.appian._interactor, sail_ui_record_action_before)

        sail_form.refresh_after_record_action("Update Table 1 (Dup) (PSF)")

    @patch('appian_locust._interactor._Interactor.refresh_after_record_action')
    def test_refresh_after_record_action_interaction_by_test_label(self, mock_refresh: MagicMock) -> None:
        sail_ui_record_action_before = json.loads(self.record_action_launch_form_before_refresh)

        sail_form = SailUiForm(self.task_set.appian._interactor, sail_ui_record_action_before)

        sail_form.refresh_after_record_action("updateTable1-1", True)

        args, _ = mock_refresh.call_args_list[0]

        self.assertEqual(args[1]['label'], "Update Table 1 (Dup) (PSF)")

    def test_click_record_search_button_by_index(self) -> None:
        sail_ui_site_with_record_search_button = json.loads(self.site_with_record_search_button)

        self.custom_locust.enqueue_response(200, self.uiform_click_record_search_button_response)

        sail_form = SailUiForm(self.task_set.appian._interactor, sail_ui_site_with_record_search_button)

        sail_form.click_record_search_button_by_index()

    @patch('appian_locust.uiform.record_uiform.RecordInstanceUiForm')
    @patch('appian_locust._interactor._Interactor.click_record_link')
    def test_click_record_link(self, mock_click_rl: MagicMock, mock_summary_view: MagicMock) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        sail_form.click_record_link('')

        args, _ = mock_click_rl.call_args_list[0]

        self.assertEqual(args[1]['recordIdentifier'], '74')

    @patch('appian_locust.uiform.record_uiform.RecordInstanceUiForm')
    @patch('appian_locust._interactor._Interactor.click_record_link')
    def test_click_record_view_link(self, mock_click_rl: MagicMock, mock_summary_view: MagicMock) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        sail_form.click_record_view_link(label='Related Actions')

        args, _ = mock_click_rl.call_args_list[0]

        self.assertEqual(args[1]['recordIdentifier'], '101')

    @patch('appian_locust.uiform.record_uiform.RecordInstanceUiForm')
    @patch('appian_locust._interactor._Interactor.click_record_link')
    def test_click_record_link_by_index(self, mock_click_rl: MagicMock, mock_summary_view: MagicMock) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        sail_form.click_record_link_by_index(index=2)

        args, _ = mock_click_rl.call_args_list[0]

        self.assertEqual(args[1]['recordIdentifier'], '22')

    @patch('appian_locust.uiform.record_uiform.RecordInstanceUiForm')
    @patch('appian_locust._interactor._Interactor.click_record_link')
    def test_click_record_link_by_attribute_and_index(self, mock_click_rl: MagicMock, mock_summary_view: MagicMock) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        sail_form.click_record_link_by_attribute_and_index(attribute='pageUrlStub', attribute_value='reports', index=3)

        args, _ = mock_click_rl.call_args_list[0]

        self.assertEqual(args[1]['recordIdentifier'], '112')

    def test_click_record_link_missing_attribute(self) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.click_record_link_by_attribute_and_index(attribute='Nonexistant', attribute_value='attribute')
        self.assertEqual(context.exception.args[0], "No components with Nonexistant 'attribute' found on page")

    def test_click_record_link_missing_component(self) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.click_record_link_by_attribute_and_index(attribute='label', attribute_value='Related Actions')
        self.assertEqual(context.exception.args[0], "Type 'RecordLink' and label 'Related Actions' found, but on different components")

    def test_click_record_link_out_of_bounds_index(self) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        with self.assertRaisesRegex(Exception, "Component found but index: '100' out of range"):
            sail_form.click_record_link_by_attribute_and_index(index=100)

    def test_click_record_link_zero_index(self) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        with self.assertRaisesRegex(Exception, "Invalid index: '0'. Please enter a positive number. Indexing is 1-based to match SAIL indexing convention"):
            sail_form.click_record_link_by_index(index=0)

    def test_click_record_link_negative_index(self) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        with self.assertRaisesRegex(Exception, "Invalid index: '-1'. Please enter a positive number"):
            sail_form.click_record_link_by_index(index=-1)

    def setup_action_response_with_ui(self, file_name: str = "form_content_response.json") -> None:
        action = self.task_set.appian.actions_info.get_action_info("Create a Case", False)
        resp_json = read_mock_file(file_name)
        self.custom_locust.set_response(action['formHref'], 200, resp_json)

    def test_actions_form_example_success(self) -> None:
        # output of get_page of a form (SAIL)
        self.setup_action_response_with_ui()
        self.custom_locust.set_response('/suite/rest/a/model/latest/228/form',
                                        200,
                                        '{"context": "12345","links": [{"href": "https://instance.host.net/suite/form","rel": "update","title": "Update", \
                                        "type": "application/vnd.appian.tv.ui+json; c=2; t=START_FORM","method": "POST"}], "ui": {"#t": "UiComponentsDelta","modifiedComponents": []}, \
                                          "timers": {"#t": "Dictionary"}}')
        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        label = 'Title'
        value = "Look at me, I am filling out a form"
        button_label = 'Submit'
        latest_form = sail_form.fill_text_field(label, value).click(button_label)

        resp = latest_form.get_latest_state()
        self.assertEqual("12345", resp['context'])

    def test_actions_form_example_activity_chained(self) -> None:
        action = self.task_set.appian.actions_info.get_action_info("Create a Case", False)
        resp_json = read_mock_file("form_content_response.json")

        self.custom_locust.set_response(action['formHref'], 200, '{"mobileEnabled": "false", "empty": "true", "formType": "START_FORM"}')
        self.custom_locust.set_response(action['initiateActionHref'], 200, resp_json)
        self.custom_locust.set_response(
            '/suite/rest/a/model/latest/228/form',
            200,
            '{"context": "12345","links": [{"href": "https://instance.host.net/suite/form","rel": "update","title": "Update", \
            "type": "application/vnd.appian.tv.ui+json; c=2; t=START_FORM","method": "POST"}], "ui": {"#t": "UiComponentsDelta","modifiedComponents": []}, "timers": {"#t": "Dictionary"}}')
        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action("Create a Case")

        label = 'Title'
        value = "Look at me, I am filling out a form"
        button_label = 'Submit'
        latest_form = sail_form.fill_text_field(label, value).click(button_label)

        resp = latest_form.get_latest_state()
        self.assertEqual("12345", resp['context'])

    def test_actions_form_example_missing_field(self) -> None:
        self.setup_action_response_with_ui()
        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        value = "Look at me, I am filling out a form"
        label = "missingText"
        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.fill_text_field(label, value)
        self.assertEqual(
            context.exception.args[0], f"No components with label 'missingText' found on page")

        button_label = 'press me'
        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.click(button_label)
        self.assertEqual(
            context.exception.args[0], f"No components with label '{button_label}' found on page")

    def test_actions_form_example_bad_response(self) -> None:
        self.setup_action_response_with_ui()
        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        self.custom_locust.set_response(
            '/suite/rest/a/model/latest/228/form', 200, 'null')

        value = "Look at me, I am filling out a form"
        label = "Title"
        with self.assertRaises(Exception) as context:
            sail_form.fill_text_field(label, value)
        self.assertEqual(
            context.exception.args[0], f"No response returned when trying to update the field with 'label' = 'Title' at index '1'")

        button_label = 'Submit'
        with self.assertRaises(Exception) as context:
            sail_form.click(button_label)
        self.assertEqual(
            context.exception.args[0], f"No response returned when trying to click button with label '{button_label}'")

    def test_actions_form_dropdown_errors(self) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')

        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        dropdown_label = "missing dropdown"
        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.select_dropdown_item(dropdown_label, 'some choice')
        self.assertEqual(
            context.exception.args[0], f"No components of type DropdownField or DropdownWidget with label '{dropdown_label}' found on page")

        dropdown_label = "Name"
        with self.assertRaises(ComponentNotFoundException):
            sail_form.select_dropdown_item(dropdown_label, 'some choice')

        dropdown_label = "Customer Type"
        with self.assertRaises(ChoiceNotFoundException):
            sail_form.select_dropdown_item(dropdown_label, 'some missing choice')

    def test_actions_form_dropdown_by_index_errors(self) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')

        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        dropdown_index = 3
        with self.assertRaises(Exception) as context:
            sail_form.select_dropdown_item_by_index(dropdown_index, 'some choice')
        self.assertEqual(
            context.exception.args[0], f"Component found but index: '{str(dropdown_index)}' out of range")

        dropdown_index = 1
        with self.assertRaises(ChoiceNotFoundException):
            sail_form.select_dropdown_item_by_index(dropdown_index, 'some missing choice')

    @patch('appian_locust.uiform.SailUiForm._get_update_url_for_reeval', return_value="/mocked/re-eval/url")
    @patch('appian_locust._interactor._Interactor.send_dropdown_update')
    def test_actions_form_dropdown_success(self, mock_send_dropdown_update: MagicMock,
                                           mock_get_update_url_for_reeval: MagicMock) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')

        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)
        initial_state = sail_form.get_latest_state()

        dropdown_label = "Customer Type"
        sail_form.select_dropdown_item(dropdown_label, 'Buy Side Asset Manager')

        mock_get_update_url_for_reeval.assert_called_with(sail_form.get_latest_state())
        mock_send_dropdown_update.assert_called_once()
        args, kwargs = mock_send_dropdown_update.call_args
        self.assertEqual(args[0], "/mocked/re-eval/url")
        self.assertIsNone(kwargs["identifier"])
        self.assertNotEqual(sail_form.get_latest_state(), initial_state)

    @patch('appian_locust.uiform.SailUiForm._get_update_url_for_reeval', return_value="/mocked/re-eval/url")
    @patch('appian_locust._interactor._Interactor.send_dropdown_update')
    def test_actions_form_dropdown_by_index_success(self, mock_send_dropdown_update: MagicMock,
                                                    mock_get_update_url_for_reeval: MagicMock) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')

        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)
        initial_state = sail_form.get_latest_state()

        dropdown_index = 1
        sail_form.select_dropdown_item_by_index(dropdown_index, 'Buy Side Asset Manager')

        mock_get_update_url_for_reeval.assert_called_with(sail_form.get_latest_state())
        mock_send_dropdown_update.assert_called_once()
        args, kwargs = mock_send_dropdown_update.call_args
        self.assertEqual(args[0], "/mocked/re-eval/url")
        self.assertIsNone(kwargs["identifier"])
        self.assertNotEqual(sail_form.get_latest_state(), initial_state)

    @patch('appian_locust.uiform.SailUiForm._get_update_url_for_reeval', return_value="/mocked/re-eval/url")
    @patch('appian_locust._interactor._Interactor.send_multiple_dropdown_update')
    def test_actions_form_multiple_dropdown_success(self, mock_send_multiple_dropdown_update: MagicMock,
                                                    mock_get_update_url_for_reeval: MagicMock) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')

        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)
        initial_state = sail_form.get_latest_state()

        dropdown_label = "Regions"
        sail_form.select_multi_dropdown_item(dropdown_label, ["Asia", "Europe and Americas"])

        mock_get_update_url_for_reeval.assert_called_with(sail_form.get_latest_state())
        mock_send_multiple_dropdown_update.assert_called_once()
        args, kwargs = mock_send_multiple_dropdown_update.call_args
        self.assertEqual(args[0], "/mocked/re-eval/url")
        self.assertIsNone(kwargs["identifier"])
        self.assertNotEqual(sail_form.get_latest_state(), initial_state)

    @patch('appian_locust.uiform.SailUiForm._get_update_url_for_reeval', return_value="/mocked/re-eval/url")
    @patch('appian_locust._interactor._Interactor.send_multiple_dropdown_update')
    def test_actions_form_multiple_dropdown_by_index_success(self, mock_send_multiple_dropdown_update: MagicMock,
                                                             mock_get_update_url_for_reeval: MagicMock) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')

        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)
        initial_state = sail_form.get_latest_state()

        dropdown_index = 1
        sail_form.select_multi_dropdown_item_by_index(dropdown_index, ["Asia", "Europe and Americas"])

        mock_get_update_url_for_reeval.assert_called_with(sail_form.get_latest_state())
        mock_send_multiple_dropdown_update.assert_called_once()
        args, kwargs = mock_send_multiple_dropdown_update.call_args
        self.assertEqual(args[0], "/mocked/re-eval/url")
        self.assertIsNone(kwargs["identifier"])
        self.assertNotEqual(sail_form.get_latest_state(), initial_state)

    @patch('appian_locust._interactor._Interactor.send_multiple_dropdown_update')
    def test_multiple_dropdown_not_found(self, mock_send_multiple_dropdown_update: MagicMock) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')
        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        dropdown_label = "Regions wrong label"
        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.select_multi_dropdown_item(dropdown_label, ["Asia"])
        self.assertEqual(
            context.exception.args[0], f"No components of type MultipleDropdownField or MultipleDropdownWidget with label '{dropdown_label}' found on page")

        dropdown_label = "Regions"
        sail_form.select_multi_dropdown_item(dropdown_label, ["Asia"])
        mock_send_multiple_dropdown_update.assert_called_once()
        args, kwargs = mock_send_multiple_dropdown_update.call_args

    @patch('appian_locust._interactor._Interactor.send_multiple_dropdown_update')
    def test_multiple_dropdown_by_index_not_found(self, mock_send_multiple_dropdown_update: MagicMock) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')
        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        dropdown_index = 2
        with self.assertRaises(Exception) as context:
            sail_form.select_multi_dropdown_item_by_index(dropdown_index, ["Asia"])
        self.assertEqual(
            context.exception.args[0], f"Component found but index: '{str(dropdown_index)}' out of range")

        dropdown_index = 1
        with self.assertRaises(ChoiceNotFoundException):
            sail_form.select_multi_dropdown_item_by_index(dropdown_index, ['Asia', 'some missing choice'])

        sail_form.select_multi_dropdown_item_by_index(dropdown_index, ["Asia"])
        mock_send_multiple_dropdown_update.assert_called_once()
        args, kwargs = mock_send_multiple_dropdown_update.call_args

    @patch('appian_locust.uiform.uiform.find_component_by_attribute_and_type_in_dict')
    @patch('appian_locust._interactor._Interactor.select_radio_button')
    def test_actions_form_radio_button_by_label_success(self, mock_select_radio_button: MagicMock,
                                                        mock_find_component_by_label: MagicMock) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')

        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)
        state1 = sail_form.get_latest_state()

        button_label = "test-radio-button"
        sail_form.select_radio_button_by_test_label(button_label, 1)

        button_label = "Qualified Institutional Buyer"
        sail_form.select_radio_button_by_label(button_label, 1)

        args, kwargs = mock_find_component_by_label.call_args_list[0]
        self.assertEqual('testLabel', args[0])

        args_next_call, kwargs_next_call = mock_find_component_by_label.call_args_list[1]
        self.assertEqual('label', args_next_call[0])
        self.assertEqual(2, len(mock_select_radio_button.call_args_list))

    def test_actions_form_radio_button_by_label_error(self) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')

        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        button_label = "missing button"
        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.select_radio_button_by_test_label(button_label, 1)
        self.assertEqual(
            context.exception.args[0], f"No components with testLabel '{button_label}' found on page")

        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.select_radio_button_by_label(button_label, 1)
        self.assertEqual(
            context.exception.args[0], f"No components with label '{button_label}' found on page")

    @patch('appian_locust.uiform.uiform.find_component_by_index_in_dict')
    @patch('appian_locust._interactor._Interactor.select_radio_button')
    def test_actions_form_radio_button_by_index_success(self, mock_select_radio_button: MagicMock,
                                                        mock_find_component_by_index: MagicMock) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')
        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)
        initial_state = sail_form.get_latest_state()
        button_index = 1
        sail_form.select_radio_button_by_index(button_index, 1)

        mock_select_radio_button.assert_called_once()
        mock_find_component_by_index.assert_called_with('RadioButtonField', button_index, initial_state)
        self.assertNotEqual(sail_form.get_latest_state(), initial_state)

    def test_actions_form_radio_button_by_index_error(self) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')

        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        index_too_low = -1
        with self.assertRaises(Exception) as context:
            sail_form.select_radio_button_by_index(index_too_low, 1)
        self.assertEqual(
            context.exception.args[0], f"Invalid index: '{index_too_low}'. Please enter a positive number")

        index_too_high = 4
        with self.assertRaises(Exception) as context:
            sail_form.select_radio_button_by_index(index_too_high, 1)
        self.assertEqual(
            context.exception.args[0],
            f"Component found but index: '{index_too_high}' out of range"
        )

    def test_click_grid_rich_text_link(self) -> None:
        report_body = read_mock_file("rich_text_grid_field.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        good_response = '{"success":"Yes"}'
        self.custom_locust.set_response("/suite/rest/a/sites/latest/process-hq/pages/home/interface", 200, good_response)
        sail_form.click_grid_rich_text_link(grid_label="Processes", row_index=0, column_name="Name")

    @patch('appian_locust.uiform.SailUiForm.assert_no_validations_present')
    def test_click_grid_plaintext_link(self, validations_generic_mock: MagicMock) -> None:
        report_body = read_mock_file("plaintext_grid_field.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        self.custom_locust.set_response(
            "/suite/rest/a/sites/latest/D6JMim/page/reports/record/lIBHer_bdD8Emw8hLLETeiApBrxq-qoA49oyo6ZbfRANWNchnXIC8_QQLHMvQo3q8_3W_uY-NIUjTsvBQt9hzZiRJbsXbp75nXNb4s_IQMGZzxV/view/summary",
            200, read_mock_file("record_summary_view_response.json"))
        sail_form.click_grid_plaintext_record_link(grid_index=0, row_index=0, column_name="Customer")
        validations_generic_mock.assert_not_called()

    @patch('appian_locust._interactor._Interactor.click_generic_element')
    def test_select_date_range_user_filter(self, click_generic_mock: MagicMock) -> None:
        report_body = read_mock_file("date_range_user_filter.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)
        start_date = datetime.date(2023, 10, 18)
        end_date = datetime.date(2023, 10, 19)

        sail_form.select_date_range_user_filter("Read-only Grid-userFilterDateRange_1", start_date, end_date)

        _, kwargs = click_generic_mock.call_args_list[0]
        value = kwargs["new_value"]
        self.assertEqual(value, {
            "startDate": {"#t": "date", "#v": f"{start_date.isoformat()}Z"},
            "endDate": {"#t": "date", "#v": f"{end_date.isoformat()}Z"}
        })

    def test_select_date_range_user_filter_invalid_dates(self) -> None:
        report_body = read_mock_file("date_range_user_filter.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)
        start_date = datetime.date(2023, 10, 20)
        end_date = datetime.date(2023, 10, 19)

        with self.assertRaises(InvalidDateRangeException):
            sail_form.select_date_range_user_filter("Read-only Grid-userFilterDateRange_1", start_date, end_date)

    @patch('appian_locust._interactor._Interactor.fetch_new_cascading_pickerfield_selection')
    def test_cascading_pickerfield_select(self, fetch_choices_mock: MagicMock) -> None:
        cascading_pickerfield_ui = read_mock_file("cascading_picker.json")
        cascading_pickerfield_ui_dict = json.loads(cascading_pickerfield_ui)
        first_choices = read_mock_file_as_dict("cascading_picker_choices.json")

        sail_form = SailUiForm(interactor=self.task_set.appian._interactor, state=cascading_pickerfield_ui_dict)

        self.custom_locust.set_response(DATA_FABRIC_URI_PATH + "/explore", 200, cascading_pickerfield_ui)
        fetch_choices_mock.return_value = first_choices["#v"]

        sail_form.fill_cascading_pickerfield(label="Aggregation Field", selections=["Jira Ticket", "Jira Ticket Event", "Jira Ticket Event"])

        pickerfield_component = find_component_by_attribute_in_dict(attribute="testLabel",
                                                                    value="test-Aggregation Field",
                                                                    component_tree=cascading_pickerfield_ui_dict)

        first_payload = self.task_set.appian._interactor.initialize_cascading_pickerfield_request(
            pickerfield_component)
        first_payload = self.task_set.appian._interactor.fill_cascading_pickerfield_request(first_payload, pickerfield_component["inlineChoices"][0])
        first_choices_call, _ = fetch_choices_mock.call_args_list[0]
        self.assertEqual(first_choices_call[0], first_payload)

        second_payload = self.task_set.appian._interactor.initialize_cascading_pickerfield_request(
            pickerfield_component)
        second_payload = self.task_set.appian._interactor.fill_cascading_pickerfield_request(second_payload, first_choices["#v"][0])
        second_choices_call, _ = fetch_choices_mock.call_args_list[1]
        self.assertEqual(second_choices_call[0], second_payload)

        self.assertEqual(sail_form.get_latest_state(), cascading_pickerfield_ui_dict)

    @patch('appian_locust._interactor._Interactor.fetch_new_cascading_pickerfield_selection')
    def test_cascading_pickerfield_attribute_select(self, fetch_choices_mock: MagicMock) -> None:
        cascading_pickerfield_ui = read_mock_file("cascading_picker_attribute.json")
        cascading_pickerfield_ui_dict = json.loads(cascading_pickerfield_ui)
        first_choices = read_mock_file_as_dict("cascading_picker_choices.json")

        sail_form = SailUiForm(interactor=self.task_set.appian._interactor, state=cascading_pickerfield_ui_dict)

        self.custom_locust.set_response(DATA_FABRIC_URI_PATH + "/explore", 200, cascading_pickerfield_ui)
        fetch_choices_mock.return_value = first_choices["#v"]

        sail_form.fill_cascading_pickerfield_with_attribute(attribute="placeholder", attribute_value='Select a field',
                                                            selections=["Jira Ticket", "Jira Ticket Event",
                                                                        "Jira Ticket Event"])

        pickerfield_component = find_component_by_attribute_in_dict(attribute="placeholder",
                                                                    value='Select a field',
                                                                    component_tree=cascading_pickerfield_ui_dict)

        first_payload = self.task_set.appian._interactor.initialize_cascading_pickerfield_request(
            pickerfield_component)
        first_payload = self.task_set.appian._interactor.fill_cascading_pickerfield_request(first_payload,
                                                                                            pickerfield_component[
                                                                                                "inlineChoices"][0])
        first_choices_call, _ = fetch_choices_mock.call_args_list[0]
        self.assertEqual(first_choices_call[0], first_payload)

        second_payload = self.task_set.appian._interactor.initialize_cascading_pickerfield_request(
            pickerfield_component)
        second_payload = self.task_set.appian._interactor.fill_cascading_pickerfield_request(second_payload,
                                                                                             first_choices["#v"][0])
        second_choices_call, _ = fetch_choices_mock.call_args_list[1]
        self.assertEqual(second_choices_call[0], second_payload)

        self.assertEqual(sail_form.get_latest_state(), cascading_pickerfield_ui_dict)

    def _get_menu_layout_sail_form(self) -> SailUiForm:
        report_body = read_mock_file("menu_layout.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        return self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

    @patch('appian_locust.uiform.uiform.SailUiForm.click_link')
    def test_menu_layout_by_label_select_with_name(self, click_link_mock: MagicMock) -> None:
        # these menu layout functions are centered around calling click_link on the right menu item link testLabel
        locust_request_label = "label with name valid find"
        sail_form = self._get_menu_layout_sail_form()
        sail_form.click_menu_item_by_name(label="noDividerMenu", choice_name="Folder Contents",
                                          locust_request_label=locust_request_label)
        click_link_mock.assert_called_once_with(label="folder-contents-no-dividers-link", is_test_label=True,
                                                locust_request_label=locust_request_label)

    @patch('appian_locust.uiform.uiform.SailUiForm.click_link')
    def test_menu_layout_by_test_label_select_with_index(self, click_link_mock: MagicMock) -> None:
        # these menu layout functions are centered around calling click_link on the right menu item link testLabel
        locust_request_label = "testLabel with index valid find"
        sail_form = self._get_menu_layout_sail_form()
        # selection
        sail_form.click_menu_item_by_choice_index(label="menuWithDividers", choice_index=2, is_test_label=True,
                                                  locust_request_label=locust_request_label)
        click_link_mock.assert_called_once_with(label="folder-contents-with-dividers-link", is_test_label=True,
                                                locust_request_label=locust_request_label)

    def test_menu_layout_can_not_be_found(self) -> None:
        sail_form = self._get_menu_layout_sail_form()
        # We use regex to ensure the component exception is for the menu layout
        # Using item by index function w/ VALID testLabel that is INVALID as just a label
        with self.assertRaisesRegex(ComponentNotFoundException, ".*label.*menuWithDividers.*"):
            sail_form.click_menu_item_by_choice_index(label="menuWithDividers", choice_index=1, is_test_label=False,
                                                      locust_request_label="invalid menu layout find")
        # Using item by name function w/ VALID label that is INVALID as a testLabel
        with self.assertRaisesRegex(ComponentNotFoundException, ".*testLabel.*noDividerMenu.*"):
            sail_form.click_menu_item_by_name(label="noDividerMenu", choice_name="Folder Contents",
                                              is_test_label=True, locust_request_label="invalid menu layout find")

    def test_menu_layout_choice_name_not_found(self) -> None:
        # these menu layout functions are centered around calling click_link on the right menu item link testLabel
        sail_form = self._get_menu_layout_sail_form()
        # Using regex to ensure this exception is for the correct component
        with self.assertRaisesRegex(ComponentNotFoundException, ".*primaryText.*FAKE NAME.*"):
            sail_form.click_menu_item_by_name(label="noDividerMenu", choice_name="FAKE NAME",
                                              locust_request_label="label with name not found")

    def test_menu_layout_choice_index_not_found(self) -> None:
        sail_form = self._get_menu_layout_sail_form()
        # The actual error we're interested in is a generic 'Exception', so we use regex to make sure it's correct
        with self.assertRaisesRegex(Exception, "Component found but index.*out of range"):
            # this index is in bounds IFF menu dividers are counted, so we want to ensure it still fails
            sail_form.click_menu_item_by_choice_index(label="menuWithDividers", choice_index=4, is_test_label=True,
                                                      locust_request_label="testLabel with index valid find")

    def test_disabled_component_click(self) -> None:
        report_body = read_mock_file_as_dict("disabled_button.json")
        sail_form = SailUiForm(interactor=self.task_set.appian._interactor, state=report_body)
        with self.assertRaises(DisabledComponentException):
            sail_form.click("test")

    def test_validation_button_click_exception(self) -> None:
        sail_form = SailUiForm(interactor=self.task_set.appian._interactor, state=json.loads(self.validations_not_present))
        self.custom_locust.set_response(path=self.validations_uri, status_code=200, body=self.validations_present)
        with self.assertRaises(IgnoredValidationException):
            sail_form.click("Create")

    def test_validation_text_field_exception(self) -> None:
        sail_form = SailUiForm(interactor=self.task_set.appian._interactor, state=json.loads(self.validations_not_present))
        self.custom_locust.set_response(path=self.validations_uri, status_code=200, body=self.validations_present)
        with self.assertRaises(IgnoredValidationException):
            label = 'Phone Num'
            value = '12345678910'
            sail_form.fill_text_field(label, value)

    def test_dispatch_click_async_timer_link(self) -> None:
        gridfield_async_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.gridfield_async))
        original_state = gridfield_async_form.get_latest_state()
        self.custom_locust.client.set_response("/suite/rest/a/sites/latest/api-dashboard/pages/api-dashboard/interface", 204, None)
        async_timer_response = gridfield_async_form.click_link("async_timer")
        self.assertEqual(original_state, async_timer_response.get_latest_state(), "Unexpected state change")

    def test_reeval_async_variables_without_async(self) -> None:
        non_async_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.date_response))
        original_state = non_async_form.get_latest_state()
        non_async_form.reeval_pending_async_variables()
        self.assertEqual(original_state, non_async_form.get_latest_state(), "Unexpected state change")

    def test_reeval_async_variables(self) -> None:
        non_async_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.textfield_async))

        new_json = json.loads(self.textfield_async)

        del new_json["asyncVariableCounter"]
        self.custom_locust.client.set_response(non_async_form.form_url, 200, json.dumps(new_json))
        self.custom_locust.client.set_response("/suite/sail/async-variables/events", 200, "id: 1\nevent: asyncVariableCompleted\ndata: asdf")
        non_async_form.reeval_pending_async_variables()
        self.assertEqual(new_json, non_async_form.get_latest_state(), "Unexpected state change")

    @patch('appian_locust._interactor._Interactor.send_grouped_dropdown_update')
    def test_select_grouped_dropdown_item_by_index(self, mock_send_grouped_dropdown_update: MagicMock) -> None:
        """
        Test that select_grouped_dropdown_item_by_index selects items in a grouped dropdown
        and returns the updated form state.
        """
        test_form = SailUiForm(self.task_set.appian._interactor, json.loads(self.grouped_dropdown_initial))
        test_form_state = test_form.get_latest_state()

        grouped_dropdown_index = 1
        choice_index = [1, 2, 3]

        test_form.select_grouped_dropdown_item_by_index(grouped_dropdown_index, choice_index)

        mock_send_grouped_dropdown_update.assert_called_once()
        self.assertNotEqual(test_form.get_latest_state(), test_form_state)


if __name__ == '__main__':
    unittest.main()
