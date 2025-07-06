import json
import os
from requests.models import CaseInsensitiveDict
from typing import Optional, Dict, Any
import unittest
from unittest.mock import MagicMock, patch, mock_open
from datetime import date, datetime

from appian_locust import AppianTaskSet
from appian_locust._save_request_builder import save_builder
from appian_locust.utilities.helper import find_component_by_attribute_in_dict, find_component_by_index_in_dict
from appian_locust.utilities import logger
from locust import Locust, TaskSet

from .mock_client import CustomLocust
from .mock_reader import read_mock_file, read_mock_file_as_dict

log = logger.getLogger(__name__)


class TestInteractor(unittest.TestCase):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    form_content = read_mock_file("form_content_response.json")
    form_content_2 = read_mock_file("sites_record_nav.json")
    form_content_3 = read_mock_file("sites_record_recordType_resp.json")
    nested_dynamic_link_json = read_mock_file("nested_dynamic_link_response.json")
    response_with_start_process_link = read_mock_file("start_process_link_response.json")
    record_action_launch_form_before_refresh = read_mock_file("record_action_launch_form_before_refresh.json")
    record_action_refresh_response = read_mock_file("record_action_refresh_response.json")
    site_with_record_search_button = read_mock_file("site_with_record_search_button.json")
    site_with_expression_editor = read_mock_file("site_with_expression_editor.json")
    tempo_report_record_link = read_mock_file("tempo_report_record_link.json")
    cascading_picker_ui = read_mock_file_as_dict("cascading_picker.json")
    cascading_picker_ui_choices = read_mock_file_as_dict("cascading_picker_choices.json")
    default_desktop_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    default_mobile_user_agent = "AppianAndroid/24.4 (Google AOSP on IA Emulator, 9; Build 0-SNAPSHOT; AppianPhone)"
    desktop_override_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.7; rv:134.0) Gecko/20100101 Firefox/134.0"
    mobile_override_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1"
    gridfield_async = read_mock_file("gridfield_async.json")

    def setUpWithPath(self, base_path_override: Optional[str] = None) -> None:
        self.base_netloc = "test-site.net"
        self.custom_locust = CustomLocust(Locust())
        parent_task_set = TaskSet(self.custom_locust)
        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "credentials", [["", ""]])
        setattr(parent_task_set, "auth", ["", ""])
        if base_path_override:
            setattr(parent_task_set, "base_path_override", base_path_override)
            self.custom_locust.set_response(base_path_override + "/?signin=native", 200, "{}",
                                            cookies={"JSESSIONID": "a", "__appianCsrfToken": "b", "__appianMultipartCsrfToken": "c"})
            self.custom_locust.set_response(base_path_override + "/rest/a/sites/latest/locust-templates", 404, "{}")

        self.task_set = AppianTaskSet(parent_task_set)

        self.task_set.on_start()

    def setUp(self) -> None:
        self.setUpWithPath()
        self.sample_component: Dict[str, Any] = {
            "value": "some value",
            "saveInto": "weird string",
            "_cId": "other weird string",
            "label": "sample label"
        }

    def test_get_primary_button_payload(self) -> None:
        output = self.task_set.appian._interactor.get_primary_button_payload(
            json.loads(self.form_content))
        self.assertIsInstance(output, dict)

    def test_unauthed_get_page(self) -> None:
        # Given
        expected_requests = self.custom_locust.get_request_list_as_method_path_tuple()
        expected_requests.append(("get", "/suite/whatever"))
        expected_requests.append(("get", "/suite/?signin=native"))
        expected_requests.append(("post", "/suite/auth?appian_environment=tempo"))
        self.custom_locust.set_response("/suite/whatever", 200, '', cookies={'__appianCsrfToken': 'abc'})
        # When
        self.task_set.appian._interactor.get_page("/suite/whatever")
        # Then
        self.assertEqual(expected_requests, self.custom_locust.get_request_list_as_method_path_tuple())

    def test_authed_get_page(self) -> None:
        # Given
        expected_requests = self.custom_locust.get_request_list_as_method_path_tuple()
        expected_requests.append(("get", "/suite/whatever"))
        cookies = {'JSESSIONID': 'abc'}
        self.custom_locust.set_response("/suite/whatever", 200, '', cookies=cookies)
        self.custom_locust.set_response("/suite/", 200, '', cookies=cookies)
        # When
        self.task_set.appian._interactor.get_page("/suite/whatever")
        # Then
        self.assertEqual(expected_requests, self.custom_locust.get_request_list_as_method_path_tuple())

    def test_header_setup_domain(self) -> None:
        session_cookie_val = "site session"
        token_cookie_val = "site token"
        multi_token_val = "site multi token"
        test_site_prefix = "test"
        self.custom_locust.client.cookies.set("JSESSIONID", f"{test_site_prefix} {session_cookie_val}",
                                              domain=self.base_netloc)
        self.custom_locust.client.cookies.set("__appianCsrfToken", f"{test_site_prefix} {token_cookie_val}",
                                              domain=self.base_netloc)
        self.custom_locust.client.cookies.set("__appianMultipartCsrfToken", f"{test_site_prefix} {multi_token_val}",
                                              domain=self.base_netloc)

        demo_site_prefix = "demo"
        demo_domain = "demo-site.net"
        self.custom_locust.client.cookies.set("JSESSIONID", f"{demo_site_prefix} {session_cookie_val}",
                                              domain=demo_domain)
        self.custom_locust.client.cookies.set("__appianCsrfToken", f"{demo_site_prefix} {token_cookie_val}",
                                              domain=demo_domain)
        self.custom_locust.client.cookies.set("__appianMultipartCsrfToken", f"{demo_site_prefix} {multi_token_val}",
                                              domain=demo_domain)

        self.task_set.appian._interactor.host = f"http://{self.base_netloc}"
        test_site_headers = self.task_set.appian._interactor.setup_request_headers()
        expected_test_cookies_str = (
            f"JSESSIONID={test_site_prefix} {session_cookie_val}; __appianCsrfToken={test_site_prefix} {token_cookie_val}; __appianMultipartCsrfToken={test_site_prefix} {multi_token_val}")
        self.assertEqual(test_site_headers["Cookie"], expected_test_cookies_str)

        demo_site_headers = self.task_set.appian._interactor.setup_request_headers(f"http://{demo_domain}/suite/test/path")
        expected_demo_cookies_str = (
            f"JSESSIONID={demo_site_prefix} {session_cookie_val}; __appianCsrfToken={demo_site_prefix} {token_cookie_val}; __appianMultipartCsrfToken={demo_site_prefix} {multi_token_val}")
        self.assertEqual(demo_site_headers["Cookie"], expected_demo_cookies_str)
        self.task_set.appian._interactor.host = ""

    def test_500_but_still_logged_in_get_page(self) -> None:
        # Given
        expected_requests = self.custom_locust.get_request_list_as_method_path_tuple()
        expected_requests.append(("get", "/suite/500err"))
        expected_requests.append(("get", "/suite/"))
        self.custom_locust.set_response("/suite/500err", 500, '{}')
        self.custom_locust.set_response("/suite/", 200, '',
                                        cookies={'fake': 'fakeVal'})  # No appiancsrf cookie returned
        # When
        try:
            self.task_set.appian._interactor.get_page("/suite/500err")
        # Then
        except Exception as e:
            self.assertEqual(expected_requests, self.custom_locust.get_request_list_as_method_path_tuple())

    def test_base_path_override(self) -> None:
        # Given
        self.setUpWithPath('/ae')

        expected_requests = self.custom_locust.get_request_list_as_method_path_tuple()
        expected_requests.append(("get", "/ae/whatever"))
        cookies = {'JSESSIONID': 'abc'}
        self.custom_locust.set_response("/ae/whatever", 200, '', cookies=cookies)
        self.custom_locust.set_response("/ae/", 200, '', cookies=cookies)
        # When
        self.task_set.appian._interactor.get_page("/suite/whatever")
        # Then
        self.assertEqual(expected_requests, self.custom_locust.get_request_list_as_method_path_tuple())

    def test_500_and_not_logged_in_get_page(self) -> None:
        # Given
        expected_requests = self.custom_locust.get_request_list_as_method_path_tuple()
        expected_requests.append(("get", "/suite/500err"))
        expected_requests.append(("get", "/suite/"))
        expected_requests.append(("get", "/suite/?signin=native"))
        expected_requests.append(("post", "/suite/auth?appian_environment=tempo"))

        self.custom_locust.set_response("/suite/500err", 500, '{}')
        self.custom_locust.set_response("/suite/", 200, '{}', cookies={'__appianCsrfToken': 'abc'})

        # When
        try:
            self.task_set.appian._interactor.get_page("/suite/500err")
        # Then
        except Exception as e:
            self.assertEqual(expected_requests, self.custom_locust.get_request_list_as_method_path_tuple())

    @patch("builtins.open", new_callable=mock_open, read_data="ase")
    def test_upload_document_to_server_validate(self, _mock_file: MagicMock) -> None:
        expected_result = self.setup_upload_document_mocks("/suite/api/tempo/file?validateExtension=true")

        result = self.task_set.appian._interactor.upload_document_to_server(file_path="path/to/file", validate_extensions=True)

        self.assertEqual(expected_result, result)

    @patch("builtins.open", new_callable=mock_open, read_data="ase")
    def test_upload_document_to_server_validate_false(self, _mock_file: MagicMock) -> None:
        expected_result = self.setup_upload_document_mocks("/suite/api/tempo/file?validateExtension=false")

        result = self.task_set.appian._interactor.upload_document_to_server(file_path="path/to/file", validate_extensions=False)

        self.assertEqual(expected_result, result)

    @patch("builtins.open", new_callable=mock_open, read_data="ase")
    def test_upload_document_to_server_validate_portals(self, _mock_file: MagicMock) -> None:
        expected_result = self.setup_upload_document_mocks("/suite/docs/upload?validateExtension=true")

        self.task_set.appian._interactor.portals_mode = True
        result = self.task_set.appian._interactor.upload_document_to_server(file_path="path/to/file", validate_extensions=True)

        self.assertEqual(expected_result, result)

    def setup_upload_document_mocks(self, path_to_be_hit: str) -> Dict[str, Any]:
        doc_id = 1234
        doc_name = "ase"
        extension = "txt"
        size = 5678
        signature = "big 'ol confusing string"
        upload_resp = [{
            "id": doc_id,
            "name": f"{doc_name}.{extension}",
            "size": size,
            "signature": signature
        }]

        self.custom_locust.set_response(path_to_be_hit, 200, json.dumps(upload_resp))

        return {
            "doc_id": doc_id,
            "name": doc_name,
            "extension": extension,
            "size": size,
            "signature": signature
        }

    def test_click_record_link(self) -> None:
        record_link = find_component_by_attribute_in_dict("label", "Profile",
                                                          json.loads(self.form_content_2))
        self.custom_locust.set_response(
            "/suite/rest/a/sites/latest/orders/page/page_name/record/nkB0AwAXQzsQm2O6Of7dMdydaKrNT9uUisGhgFHLyZXpnCB2kjcXoiFJRK5SlL5Bt_GvQEcqlclEadcUWUJ9fCR6GnV1GcZA0cQDe2zoojxnd4W1rs06fDnxgqf" +
            "-Pa9TcPwsNOpNrv_mvgEFfGrsSLB4BALxCD8JZ--/view/summary",
            200,
            "{}")

        output = self.task_set.appian._interactor.click_record_link(
            "/suite/rest/a/sites/latest/site_name/page/page_name/recordType/record_uuid/record/some_long_record_id/view/summary", record_link, {}, "")
        self.assertEqual(output, dict())

    def test_record_link_sites_record(self) -> None:
        record_link = find_component_by_attribute_in_dict("label", "Profile",
                                                          json.loads(self.form_content_2))

        mock = unittest.mock.Mock()
        setattr(self.task_set.appian._interactor, 'get_page', mock)

        self.task_set.appian._interactor.click_record_link(
            "/suite/sites/records/page/db/record/some-record-ref/view/summary", record_link, {}, "")

        mock.assert_called_once()
        # Assert get_page() called with first argument as the correct record link url
        recordRef = record_link.get("_recordRef")
        expected_record_link_url = f"('/suite/rest/a/sites/latest/orders/page/db/record/{recordRef}/view/summary',)"

        self.assertEqual(f"{mock.call_args[0]}", expected_record_link_url)

    def test_record_link_interface_site(self) -> None:
        ui = read_mock_file("sites_page_interface.json")
        record_link = find_component_by_attribute_in_dict("testLabel", "RecordLinkTestLabel", json.loads(ui))

        mock = unittest.mock.Mock()
        setattr(self.task_set.appian._interactor, 'get_page', mock)

        self.task_set.appian._interactor.click_record_link(
            "/suite/rest/a/sites/latest/vendor-management/pages/opportunities/interface", record_link, {}, "")
        mock.assert_called_once()

        recordRef = record_link.get("_recordRef")
        expected_record_link_url = f"('/suite/rest/a/sites/latest/vendor-management/page/opportunities/record/{recordRef}/view/summary',)"
        self.assertEqual(f"{mock.call_args[0]}", expected_record_link_url)

    def test_record_link_interface_site_page_substring_of_site(self) -> None:
        ui = read_mock_file("sites_page_interface.json")
        record_link = find_component_by_attribute_in_dict("testLabel", "RecordLinkTestLabelPageSubstringOfSite", json.loads(ui))

        mock = unittest.mock.Mock()
        setattr(self.task_set.appian._interactor, 'get_page', mock)

        self.task_set.appian._interactor.click_record_link(
            "/suite/rest/a/sites/latest/requirements-management/pages/requirements/interface", record_link, {}, "")
        mock.assert_called_once()

        recordRef = record_link.get("_recordRef")
        expected_record_link_url = f"('/suite/rest/a/sites/latest/requirements-management/page/requirements/record/{recordRef}/view/summary',)"
        self.assertEqual(f"{mock.call_args[0]}", expected_record_link_url)

    def test_record_link_sites_any_page(self) -> None:
        record_link = find_component_by_attribute_in_dict("label", "DA0G-P2A6",
                                                          json.loads(self.form_content_3))

        mock = unittest.mock.Mock()
        setattr(self.task_set.appian._interactor, 'get_page', mock)

        self.task_set.appian._interactor.click_record_link(
            "/suite/rest/a/sites/latest/textcolumns/page/p.500", record_link, {}, "")

        mock.assert_called_once()
        # Assert get_page() called with first argument as the correct record link url
        recordRef = record_link.get("_recordRef")
        expected_record_link_url = f"('/suite/rest/a/sites/latest/orders/page/orders/record/{recordRef}/view/summary',)"

        self.assertEqual(f"{mock.call_args[0]}", expected_record_link_url)

    def test_record_link_tempo_report(self) -> None:
        record_link = find_component_by_attribute_in_dict("label", "Coconut",
                                                          json.loads(self.tempo_report_record_link))

        mock = unittest.mock.Mock()

        setattr(self.task_set.appian._interactor, 'get_page', mock)
        self.task_set.appian._interactor.click_record_link(
            "/suite/tempo/reports/view/oxy4ed", record_link, {}, "")

        mock.assert_called_once()
        # Assert get_page() called with first argument as the correct record link url
        recordRef = record_link.get("_recordRef")
        expected_record_link_url = f"('/suite/rest/a/sites/latest/D6JMim/page/reports/record/{recordRef}/view/summary',)"

        self.assertEqual(f"{mock.call_args[0]}", expected_record_link_url)

    def test_click_record_link_error(self) -> None:
        record_link = {"fake_component": "fake_attributes"}
        with self.assertRaises(Exception):
            self.task_set.appian._interactor.click_record_link(
                "", record_link, {}, "")

    def start_process_link_test_helper(self, is_mobile: bool = False) -> None:
        spl_component = find_component_by_attribute_in_dict("label", "Check In",
                                                            json.loads(self.response_with_start_process_link))
        mock = unittest.mock.Mock()
        process_model_opaque_id = spl_component.get("processModelOpaqueId")
        cache_key = spl_component.get("cacheKey")
        site_name = "covid-19-response-management"
        page_name = "home"

        setattr(self.task_set.appian._interactor, 'post_page', mock)
        self.task_set.appian._interactor.click_start_process_link(spl_component, process_model_opaque_id, cache_key,
                                                                  site_name, page_name, None, is_mobile)

        mock.assert_called_once()
        if not is_mobile:
            expected_spl_link_url = f"('/suite/rest/a/sites/latest/{site_name}/page/p.{page_name}/startProcess/{process_model_opaque_id}?cacheKey={cache_key}',)"
        else:
            expected_spl_link_url = f"('/suite/rest/a/model/latest/startProcess/{process_model_opaque_id}?cacheKey={cache_key}',)"
        self.assertEqual(f"{mock.call_args[0]}", expected_spl_link_url)

    def test_start_process_link(self) -> None:
        self.start_process_link_test_helper(is_mobile=False)

    def test_click_start_process_link_mobile(self) -> None:
        self.start_process_link_test_helper(is_mobile=True)

    def test_click_record_link_error_fake_uri(self) -> None:
        record_link = find_component_by_attribute_in_dict("label", "Profile",
                                                          json.loads(self.form_content_2))
        with self.assertRaises(Exception):
            self.task_set.appian._interactor.click_record_link(
                "fake_uri", record_link, {}, "")

    def test_click_dynamic_link(self) -> None:
        dyn_link = find_component_by_attribute_in_dict("label", "Settings",
                                                       json.loads(self.form_content_2))
        self.custom_locust.set_response("", 200, "{}")
        output = self.task_set.appian._interactor.click_link(
            "", dyn_link, {}, "")
        self.assertEqual(output, dict())

    def test_click_dynamic_link_error(self) -> None:
        dyn_link = {"fake_component": "fake_attributes"}
        with self.assertRaises(KeyError):
            self.task_set.appian._interactor.click_link(
                "", dyn_link, {}, "")

    def test_click_nested_dynamic_link(self) -> None:
        dyn_link = find_component_by_attribute_in_dict("label",
                                                       "I need to update my Account details",
                                                       json.loads(self.nested_dynamic_link_json))
        self.custom_locust.set_response("", 200, "{}")
        output = self.task_set.appian._interactor.click_link(
            "", dyn_link, {}, "")
        self.assertEqual(output, dict())

    def test_post_page(self) -> None:
        self.custom_locust.set_response("test/path", 200, '{"ase": "ase2"}')
        output = self.task_set.appian._interactor.post_page(
            "test/path", payload={}, headers=None)
        self.assertEqual(output.json(), {"ase": "ase2"})

    def test_change_user_to_mobile(self) -> None:
        # Given
        default_header = self.task_set.appian._interactor.setup_request_headers()
        self.assertEqual(default_header["User-Agent"], self.default_desktop_user_agent)

        # When
        self.task_set.appian._interactor.set_user_agent_to_mobile()
        new_header = self.task_set.appian._interactor.setup_request_headers()
        self.assertNotEqual(new_header, default_header)
        self.assertEqual(new_header["User-Agent"], self.default_mobile_user_agent)

    def test_change_default_user_to_desktop(self) -> None:
        # Given
        default_header = self.task_set.appian._interactor.setup_request_headers()
        self.assertEqual(default_header["User-Agent"], self.default_desktop_user_agent)

        # When
        self.task_set.appian._interactor.set_user_agent_to_desktop()
        new_header = self.task_set.appian._interactor.setup_request_headers()

        # Then
        self.assertEqual(new_header, default_header)

    def test_change_mobile_user_to_desktop(self) -> None:
        # Given
        default_header = self.task_set.appian._interactor.setup_request_headers()
        self.assertEqual(default_header["User-Agent"], self.default_desktop_user_agent)

        # Switch to mobile
        self.task_set.appian._interactor.set_user_agent_to_mobile()
        new_header = self.task_set.appian._interactor.setup_request_headers()
        self.assertNotEqual(new_header, default_header)
        self.assertEqual(new_header["User-Agent"], self.default_mobile_user_agent)

        # Switch back to desktop
        self.task_set.appian._interactor.set_user_agent_to_desktop()
        new_header = self.task_set.appian._interactor.setup_request_headers()

        # Then
        self.assertEqual(new_header, default_header)

    def test_override_default_mobile_user_agent(self) -> None:
        # Given
        default_header = self.task_set.appian._interactor.setup_request_headers()
        self.assertEqual(default_header["User-Agent"], self.default_desktop_user_agent)

        # When
        self.task_set.client.user_agent_mobile = self.mobile_override_agent
        self.task_set.appian._interactor.set_user_agent_to_mobile()
        new_header = self.task_set.appian._interactor.setup_request_headers()

        # Then
        self.assertNotEqual(new_header, default_header)
        self.assertEqual(new_header["User-Agent"], self.mobile_override_agent)

    def test_override_desktop_user_agent(self) -> None:
        # Given
        default_header = self.task_set.appian._interactor.setup_request_headers()
        self.assertEqual(default_header["User-Agent"], self.default_desktop_user_agent)

        # When
        self.task_set.client.user_agent_desktop = self.desktop_override_agent
        self.task_set.appian._interactor.set_user_agent_to_desktop()
        new_header = self.task_set.appian._interactor.setup_request_headers()

        # Then
        self.assertNotEqual(new_header, default_header)
        self.assertEqual(new_header["User-Agent"], self.desktop_override_agent)

    def test_click_record_search_button(self) -> None:
        component = find_component_by_index_in_dict("SearchBoxWidget", 1, json.loads(self.site_with_record_search_button))

        correct_resp = '{"ase": "ase2"}'
        self.custom_locust.set_response("/test/path", 200, correct_resp)
        output = self.task_set.appian._interactor.click_record_search_button("/test/path", component, {}, "my_uuid", "")
        self.assertEqual(output, json.loads(correct_resp))

    def test_login_retry(self) -> None:
        # Given
        init_cookies = {'JSESSIONID': 'abc', '__appianCsrfToken': '123'}
        cookies_no_mcsrf = {'JSESSIONID': 'abc123',
                            '__appianCsrfToken': 'different cookie'}
        cookies_mcsrf = {'JSESSIONID': 'abc123',
                         '__appianCsrfToken': 'different cookie',
                         '__appianMultipartCsrfToken': 'these cookies'}

        self.custom_locust.enqueue_response(200,
                                            '<html>A huge html blob</html>', cookies=init_cookies)
        self.custom_locust.enqueue_response(200,
                                            '<html>A huge html blob</html>', cookies=cookies_no_mcsrf)
        self.custom_locust.enqueue_response(200,
                                            '<html>A huge html blob</html>', cookies=cookies_mcsrf)

        # When
        self.task_set.appian.login(["", ""])

        # Then
        self.assertIn('__appianMultipartCsrfToken', self.task_set.appian.client.cookies.keys())

    def test_login_already_logged_in(self) -> None:
        init_cookies = {'JSESSIONID': 'abc'}

        good_resp = '{"resp": "good"}'
        self.custom_locust.set_response(f"{self.task_set.appian._interactor.host}/suite/?signin=native", 200,
                                        good_resp, cookies=init_cookies)
        self.custom_locust.set_response("/suite/auth?appian_environment=tempo", 200,
                                        '{"resp": "bad"}')

        _, resp = self.task_set.appian.login(["", ""])
        self.assertEqual(resp.json(), json.loads(good_resp))

    @patch('appian_locust._interactor._Interactor.login')
    def test_check_login_resp_csrf(self, login_mock: MagicMock) -> None:
        initial_response = self.custom_locust.client.make_response(200, "{}", headers=CaseInsensitiveDict({}), cookies={'__appianCsrfToken': "token!"})

        self.task_set.appian._interactor.check_login(initial_response)

        login_mock.assert_called_once()

    @patch('appian_locust._interactor._Interactor.login')
    def test_check_login_error_resp(self, login_mock: MagicMock) -> None:
        initial_response = self.custom_locust.client.make_response(401, "{}", headers=CaseInsensitiveDict({}),
                                                                   cookies={'__appianCsrfToken': "token!"})
        self.custom_locust.set_response("/suite/", 200, "{}", cookies={'__appianCsrfToken': "token!"})

        self.task_set.appian._interactor.check_login(initial_response)

        login_mock.assert_called_once()

    def test_upload_document_to_field_bad_doc_id(self) -> None:
        bad_value = 'abc'
        with self.assertRaisesRegex(Exception,
                                    f"Bad document id or list of document ids: {bad_value}"):
            self.task_set.appian._interactor.upload_document_to_field('fake-url', {}, {}, 'uuid', 'abc')  # type: ignore

    def test_upload_document_to_field_doc_id(self) -> None:
        doc_id = {"doc_id": 1, "size": "2", "name": "document", "extension": "jpeg"}
        upload_field = {'saveInto': 'abc', '_cId': '1123'}

        self.custom_locust.set_response("/doc-url/", 200, '{}')
        self.task_set.appian._interactor.upload_document_to_field('/doc-url/',
                                                                  upload_field, {}, 'uuid', doc_id)

        # This indexing is ridiculous, but we don't care about the rest
        last_request_body = json.loads(self.custom_locust.get_request_list().pop()['data'])
        document_update = last_request_body['updates']['#v'][0]['value']
        self.assertEqual({'#t': 'CollaborationDocument', 'id': 1}, document_update)

    def test_upload_document_to_field_list_of_doc_id(self) -> None:
        doc_infos = [
            {"doc_id": 1, "size": "2", "name": "document", "extension": "jpeg"},
            {"doc_id": 2, "size": "2", "name": "document", "extension": "jpeg"},
            {"doc_id": 3, "size": "2", "name": "document", "extension": "jpeg"}
        ]
        upload_field = {'saveInto': 'abc', '_cId': '1123'}

        self.custom_locust.set_response("/doc-url/", 200, '{}')
        self.task_set.appian._interactor.upload_document_to_field('/doc-url/',
                                                                  upload_field, {}, 'uuid', doc_infos)

        # This indexing is ridiculous, but we don't care about the rest
        last_request_body = json.loads(self.custom_locust.get_request_list().pop()['data'])
        document_update = last_request_body['updates']['#v'][0]['value']
        self.assertEqual('FileMetadata?list', document_update['#t'])
        for i, doc_info in enumerate(doc_infos):
            self.assertEqual({'clientUuid': '0', 'loadedBytes': 0, 'name': 'document',
                              'documentId': {'#t': 'CollaborationDocument', 'id': doc_info["doc_id"]},
                              'extension': 'jpeg', 'fileSizeBytes': "2"},
                             document_update['#v'][i])

    def test_click_related_action(self) -> None:
        opaque_record_id = "id"
        opaque_related_action_id = "other_id"
        record_type_stub = "stub"
        expected_response = {
            "ui": "here"
        }
        self.custom_locust.set_response(
            f"/suite/rest/a/record/latest/{record_type_stub}/{opaque_record_id}/actions/{opaque_related_action_id}",
            200,
            json.dumps(expected_response)
        )

        resp = self.task_set.appian._interactor.click_related_action(
            component={"label": "whatever"},
            record_type_stub=record_type_stub,
            opaque_record_id=opaque_record_id,
            opaque_related_action_id=opaque_related_action_id,
            open_in_a_dialog=False
        )

        self.assertEqual(resp, expected_response)

    def test_click_related_action_chained(self) -> None:
        opaque_record_id = "id"
        opaque_related_action_id = "other_id"
        expected_response = {
            "it": "worked"
        }
        self.custom_locust.enqueue_response(200, '{"empty": "true"}')
        self.custom_locust.enqueue_response(200, json.dumps(expected_response))

        resp = self.task_set.appian._interactor.click_related_action(
            component={"label": "whatever"},
            record_type_stub="",
            opaque_record_id=opaque_record_id,
            opaque_related_action_id=opaque_related_action_id,
            open_in_a_dialog=True
        )

        self.assertEqual(resp, expected_response)

    def test_click_record_list_action(self) -> None:
        pm_id = "processModelId"
        cache_key = "cacheKey"
        correct_json = '{"ase": "ase2"}'
        self.custom_locust.set_response(f"/suite/rest/a/model/latest/{pm_id}/forminternal?cacheKey={cache_key}", 200, correct_json)

        resp_json = self.task_set.appian._interactor.click_record_list_action("label", pm_id, cache_key)

        self.assertEqual(resp_json, json.loads(correct_json))

    def test_clean_filename(self) -> None:
        cleaned_str = self.task_set.appian._interactor._clean_filename("\\<>:\"/|?*")
        self.assertEqual(cleaned_str, ".........")

    @patch('appian_locust._interactor._Interactor.login')
    @patch('appian_locust._interactor._Interactor.get_page')
    def test_bad_csrf_token(self, get_page_mock: MagicMock, login_mock: MagicMock) -> None:
        initial_unauthed_response = self.custom_locust.client.make_response(401, "{}", headers=CaseInsensitiveDict({}))
        cors_ping_response = self.custom_locust.client.make_response(200, "{}", "/suite/cors/ping")
        get_page_mock.return_value = cors_ping_response

        self.task_set.appian._interactor.check_post_response_for_valid_auth(initial_unauthed_response)

        get_page_mock.assert_called_once()
        positional_args, _ = get_page_mock.call_args_list[0]
        self.assertEqual(positional_args[0], "/suite/cors/ping")
        login_mock.assert_not_called()

    @patch('appian_locust._interactor._Interactor.login')
    @patch('appian_locust._interactor._Interactor.get_page')
    def test_bad_jsession_id(self, get_page_mock: MagicMock, login_mock: MagicMock) -> None:
        initial_unauthed_response = self.custom_locust.client.make_response(401, "{}", headers=CaseInsensitiveDict({}))
        cors_ping_response = self.custom_locust.client.make_response(200, '{"authed": false}', "/suite/cors/ping")
        get_page_mock.return_value = cors_ping_response

        self.task_set.appian._interactor.check_post_response_for_valid_auth(initial_unauthed_response)

        get_page_mock.assert_called_once()
        positional_args, _ = get_page_mock.call_args_list[0]
        self.assertEqual(positional_args[0], "/suite/cors/ping")
        login_mock.assert_called_once()

    def test_fill_cascading_pickerfield_request(self) -> None:
        choice = self.cascading_picker_ui_choices["#v"][0]
        picker = find_component_by_attribute_in_dict(attribute="testLabel", value="test-Aggregation Field", component_tree=self.cascading_picker_ui)
        base_payload = self.task_set.appian._interactor.initialize_cascading_pickerfield_request(picker)

        base_payload = self.task_set.appian._interactor.fill_cascading_pickerfield_request(base_payload, choice)

        self.assertEqual(base_payload[0], "dc15939c-6a89-4ca2-afe4-1eeb102c0df8")
        self.assertEqual(base_payload[1], ["acb7bab2-8b3d-4ec2-a37c-8e0a1bca764e", "2c7aecfa-ab40-4f94-acb0-2981f57126dc"])
        self.assertEqual(base_payload[2], "jiraTicket.jiraTicketEvent")
        self.assertEqual(base_payload[11], "dc15939c-6a89-4ca2-eeee-1eeb102c0df8")

    def test_initialize_cascading_pickerfield_request(self) -> None:
        picker = find_component_by_attribute_in_dict(attribute="testLabel", value="test-Aggregation Field",
                                                     component_tree=self.cascading_picker_ui)

        payload = self.task_set.appian._interactor.initialize_cascading_pickerfield_request(pickerfield_component=picker)

        correct_picker = [
            "RECORD_TYPE_UUID_PLACEHOLDER",
            "RELATIONSHIP_PATH_PLACEHOLDER",
            "SELECTION_LABEL_PLACEHOLDER",
            None,
            picker["nestedChoicesEndpointPayload"]["relationshipTypes"],
            picker["nestedChoicesEndpointPayload"]["allowedTypes"],
            None,
            picker["nestedChoicesEndpointPayload"]["omitQueryTimeCustomFields"],
            [],
            picker["nestedChoicesEndpointPayload"]["requiredRelationshipType"],
            picker["nestedChoicesEndpointPayload"]["topRecordType"],
            "BASE_RECORD_TYPE_UUID_PLACEHOLDER",
            picker["nestedChoicesEndpointPayload"]["shouldUseFriendlyName"],
            None,
            picker["nestedChoicesEndpointPayload"]["checkAccess"],
            None,
            None,
            None,
            None
        ]

        self.assertEqual(payload, correct_picker)

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_click_component(self, post_page_mock: MagicMock) -> None:
        context = {"context": "stuff"}
        component = {
            "label": "ase",
            "link": self.sample_component
        }
        uuid = "uuid"

        expected_component = self.sample_component.copy()
        expected_component.update({"label": "ase"})

        expected_payload = (save_builder()
                            .component(expected_component)
                            .context(context)
                            .uuid(uuid)
                            .build())

        self.task_set.appian._interactor.click_component(post_url="/any/ol/url", component=component.copy(), context=context, uuid=uuid)

        _, kwargs = post_page_mock.call_args_list[0]
        self.assertEqual(expected_payload, kwargs["payload"])

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_send_dropwdown_update(self, post_page_mock: MagicMock) -> None:
        index = 3
        value = {
            "#t": "Integer",
            "#v": index
        }
        context = {"context": "stuff"}
        uuid = "uuid"
        identifier = {"its": "identified"}
        expected_payload = (save_builder()
                            .component(self.sample_component)
                            .context(context)
                            .uuid(uuid)
                            .value(value)
                            .identifier(identifier)
                            .build())

        self.task_set.appian._interactor.send_dropdown_update(
            post_url="/any/ol/url",
            dropdown=self.sample_component.copy(),
            context=context,
            uuid=uuid,
            index=index,
            identifier=identifier
        )

        _, kwargs = post_page_mock.call_args_list[0]
        self.assertEqual(expected_payload, kwargs["payload"])

    @patch('appian_locust._interactor._Interactor.send_dropdown_update')
    def test_construct_and_send_dropdown_update(self, send_dropdown_mock: MagicMock) -> None:
        component = {
            "choices": [
                "one",
                "two",
                "three"
            ]
        }

        self.task_set.appian._interactor.construct_and_send_dropdown_update(component, "two", {}, {}, "", "", "", "")

        _, kwargs = send_dropdown_mock.call_args_list[0]
        self.assertEqual(2, kwargs["index"])

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_send_multiple_dropdown_update(self, post_page_mock: MagicMock) -> None:
        index = [3, 4]
        value = {
            "#t": "Integer?list",
            "#v": index
        }
        context = {"context": "stuff"}
        uuid = "uuid"
        identifier = {"its": "identified"}
        expected_payload = (save_builder()
                            .component(self.sample_component)
                            .context(context)
                            .uuid(uuid)
                            .value(value)
                            .identifier(identifier)
                            .build())

        self.task_set.appian._interactor.send_multiple_dropdown_update(
            post_url="/any/ol/url",
            multi_dropdown=self.sample_component.copy(),
            context=context,
            uuid=uuid,
            index=index,
            identifier=identifier
        )

        _, kwargs = post_page_mock.call_args_list[0]
        self.assertEqual(expected_payload, kwargs["payload"])

    @patch('appian_locust._interactor._Interactor.send_multiple_dropdown_update')
    def test_construct_and_send_multiple_dropdown_update(self, send_multiple_dropdown_mock: MagicMock) -> None:
        component = {
            "choices": [
                "one",
                "two",
                "three"
            ]
        }

        self.task_set.appian._interactor.construct_and_send_multiple_dropdown_update(component, ["two", "three"], {}, {}, "", "", "", "")

        _, kwargs = send_multiple_dropdown_mock.call_args_list[0]
        self.assertEqual([2, 3], kwargs["index"])

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_fill_textfield(self, post_page_mock: MagicMock) -> None:
        context = {"context": "stuff"}
        uuid = "uuid"
        text = "ase"

        value = {"#t": "Text", "#v": text}
        expected_payload = (save_builder()
                            .component(self.sample_component)
                            .context(context)
                            .uuid(uuid)
                            .value(value)
                            .build())

        self.task_set.appian._interactor.fill_textfield("/any/ol/url", self.sample_component.copy(), text, context, uuid)

        _, kwargs = post_page_mock.call_args_list[0]
        self.assertEqual(expected_payload, kwargs["payload"])

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_fill_pickerfield_text(self, post_page_mock: MagicMock) -> None:
        context = {"context": "stuff"}
        uuid = "uuid"
        text = "ase"

        value = {
            "#t": "PickerData",
            "typedText": text
        }
        expected_payload = (save_builder()
                            .component(self.sample_component)
                            .context(context)
                            .uuid(uuid)
                            .value(value)
                            .build())

        self.task_set.appian._interactor.fill_pickerfield_text("/any/ol/url", self.sample_component.copy(), text, context, uuid)

        _, kwargs = post_page_mock.call_args_list[0]
        self.assertEqual(expected_payload, kwargs["payload"])

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_select_pickerfield_suggestion(self, post_page_mock: MagicMock) -> None:
        context = {"context": "stuff"}
        uuid = "uuid"
        selection = {"its": "selected"}

        value = {
            "#t": "PickerData",
            "identifiers": [selection]
        }
        expected_payload = (save_builder()
                            .component(self.sample_component)
                            .context(context)
                            .uuid(uuid)
                            .value(value)
                            .build())

        self.task_set.appian._interactor.select_pickerfield_suggestion("/any/ol/url", self.sample_component.copy(), selection, context, uuid)

        _, kwargs = post_page_mock.call_args_list[0]
        self.assertEqual(expected_payload, kwargs["payload"])

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_select_checkbox_item(self, post_page_mock: MagicMock) -> None:
        context = {"context": "stuff"}
        uuid = "uuid"
        indices = [2, 3]

        value = {
            "#t": "Integer?list",
            "#v": indices
        }
        expected_payload = (save_builder()
                            .component(self.sample_component)
                            .context(context)
                            .uuid(uuid)
                            .value(value)
                            .build())

        self.task_set.appian._interactor.select_checkbox_item("/any/ol/url", self.sample_component.copy(), context, uuid, indices)

        _, kwargs = post_page_mock.call_args_list[0]
        self.assertEqual(expected_payload, kwargs["payload"])

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_click_selected_tab(self, post_page_mock: MagicMock) -> None:
        context = {"context": "stuff"}
        uuid = "uuid"

        component = self.sample_component.copy()
        component.update({
            "tabs": [
                {
                    "label": "one"
                },
                {
                    "label": "two"
                },
                {
                    "label": "three"
                }
            ]
        })

        value = {
            "#t": "Integer",
            "#v": 2
        }
        expected_payload = (save_builder()
                            .component(component)
                            .context(context)
                            .uuid(uuid)
                            .value(value)
                            .build())

        self.task_set.appian._interactor.click_selected_tab("/any/ol/url", component, "two", context, uuid)

        _, kwargs = post_page_mock.call_args_list[0]
        self.assertEqual(expected_payload, kwargs["payload"])

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_select_radio_button(self, post_page_mock: MagicMock) -> None:
        context = {"context": "stuff"}
        uuid = "uuid"
        index = 2

        value = {
            "#t": "Integer",
            "#v": 2
        }
        expected_payload = (save_builder()
                            .component(self.sample_component)
                            .context(context)
                            .uuid(uuid)
                            .value(value)
                            .build())

        self.task_set.appian._interactor.select_radio_button("/any/ol/url", self.sample_component.copy(), context, uuid, index)

        _, kwargs = post_page_mock.call_args_list[0]
        self.assertEqual(expected_payload, kwargs["payload"])

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_update_date_field(self, post_page_mock: MagicMock) -> None:
        context = {"context": "stuff"}
        uuid = "uuid"
        date_input = date.today()

        value = {
            "#t": "date",
            "#v": f"{date_input.isoformat()}Z"
        }
        expected_payload = (save_builder()
                            .component(self.sample_component)
                            .context(context)
                            .uuid(uuid)
                            .value(value)
                            .build())

        self.task_set.appian._interactor.update_date_field("/any/ol/url", self.sample_component.copy(), date_input, context, uuid)

        _, kwargs = post_page_mock.call_args_list[0]
        self.assertEqual(expected_payload, kwargs["payload"])

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_update_datetime_field(self, post_page_mock: MagicMock) -> None:
        context = {"context": "stuff"}
        uuid = "uuid"
        datetime_input = datetime.now()

        value = {
            "#t": "dateTime",
            "#v": f"{datetime_input.replace(second=0, microsecond=0).isoformat()}Z"
        }
        expected_payload = (save_builder()
                            .component(self.sample_component)
                            .context(context)
                            .uuid(uuid)
                            .value(value)
                            .build())

        self.task_set.appian._interactor.update_datetime_field("/any/ol/url", self.sample_component.copy(), datetime_input, context, uuid)

        _, kwargs = post_page_mock.call_args_list[0]
        self.assertEqual(expected_payload, kwargs["payload"])

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_update_grid_from_sail_form(self, post_page_mock: MagicMock) -> None:
        context = {"context": "stuff"}
        uuid = "uuid"
        text = "ase"

        value = {"#t": "Text", "#v": text}
        expected_payload = (save_builder()
                            .component(self.sample_component)
                            .context(context)
                            .uuid(uuid)
                            .value(value)
                            .build())

        self.task_set.appian._interactor.update_grid_from_sail_form("/any/ol/url", self.sample_component.copy(), value, context, uuid)

        _, kwargs = post_page_mock.call_args_list[0]
        self.assertEqual(expected_payload, kwargs["payload"])

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_interact_with_record_grid(self, post_page_mock: MagicMock) -> None:
        context = {"context": "stuff"}
        uuid = "uuid"
        identifier = {"its": "identified"}

        expected_payload = (save_builder()
                            .component(self.sample_component)
                            .context(context)
                            .uuid(uuid)
                            .identifier(identifier)
                            .build())

        self.task_set.appian._interactor.interact_with_record_grid("/any/ol/url", self.sample_component.copy(), context, uuid, identifier)

        _, kwargs = post_page_mock.call_args_list[0]
        self.assertEqual(expected_payload, kwargs["payload"])

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_click_generic_element(self, post_page_mock: MagicMock) -> None:
        context = {"context": "stuff"}
        uuid = "uuid"
        text = "ase"

        value = {"#t": "Text", "#v": text}
        expected_payload = (save_builder()
                            .component(self.sample_component)
                            .context(context)
                            .uuid(uuid)
                            .value(value)
                            .build())

        self.task_set.appian._interactor.click_generic_element("/any/ol/url", self.sample_component.copy(), context, uuid, value)

        _, kwargs = post_page_mock.call_args_list[0]
        self.assertEqual(expected_payload, kwargs["payload"])

    @patch('appian_locust._interactor._Interactor.post_page')
    def test_refresh_after_record_action(self, post_page_mock: MagicMock) -> None:
        context = {"context": "stuff"}
        uuid = "uuid"
        text = "ase"

        expected_payload = (save_builder()
                            .component(self.sample_component.copy())
                            .context(context)
                            .uuid(uuid)
                            .value(dict())
                            .build())

        record_action_trigger_component = {
            "value": "some other value",
            "saveInto": "other weird string",
            "_cId": "other other weird string",
            "label": "other sample label"
        }
        record_action_trigger_payload = (save_builder()
                                         .component(record_action_trigger_component)
                                         .context(context)
                                         .uuid(uuid)
                                         .value(dict())
                                         .build())

        record_action_save_request = expected_payload["updates"]["#v"][0]
        record_action_trigger_save_request = record_action_trigger_payload["updates"]["#v"][0]

        # Update the main payload with the both save requests
        expected_payload["updates"]["#v"] = [record_action_save_request, record_action_trigger_save_request]

        self.task_set.appian._interactor.refresh_after_record_action("/any/ol/url", self.sample_component.copy(), record_action_trigger_component, context, uuid)

        _, kwargs = post_page_mock.call_args_list[0]
        self.assertEqual(expected_payload, kwargs["payload"])

    def test_click_async_timer(self) -> None:
        async_timer = find_component_by_attribute_in_dict("label", "async_timer", json.loads(self.gridfield_async))
        url = "/suite/rest/a/sites/latest/api-dashboard/pages/api-dashboard/interface"
        # Set the body to something other than None to prove that we return None as a result of the 204 error code
        self.custom_locust.set_response(url, 204, "anything")
        response = self.task_set.appian._interactor.click_async_timer(url, async_timer, {}, "")
        self.assertIsNone(response)
