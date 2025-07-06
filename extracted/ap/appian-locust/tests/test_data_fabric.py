import unittest
from unittest.mock import Mock, ANY
from requests import Response, HTTPError
from typing import Optional, Callable

from appian_locust._data_fabric import _DataFabric, DATA_FABRIC_URI_PATH, DATA_FABRIC_DASHBOARD_URI_PATH
from appian_locust._interactor import _Interactor

integration_url = ""
auth = ["fake_user", ""]


class TestDataFabric(unittest.TestCase):

    def setUp(self) -> None:
        self.interactor: _Interactor = _Interactor("", "ase")
        setup_headers_mock = unittest.mock.Mock(return_value={})
        setattr(self.interactor, 'setup_sail_headers', setup_headers_mock)
        setattr(self.interactor, 'setup_request_headers', setup_headers_mock)
        self.data_fabric_interactor: _DataFabric = _DataFabric(self.interactor)

    def mock_get_page_with_response(self, expected_response: dict, expected_uri: Optional[str] = None,
                                    raise_for_status_response: Optional[Callable[[], None]] = None) -> Mock:
        response_mock = unittest.mock.Mock(return_value=expected_response)
        response_all_ok_mock = raise_for_status_response or unittest.mock.Mock(return_value="")
        response = Response()
        setattr(response, 'json', response_mock)
        setattr(response, 'raise_for_status', response_all_ok_mock)  # ensure response.ok returns true
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, headers, label: response if uri == expected_uri or DATA_FABRIC_URI_PATH else "",
        )
        setattr(self.interactor, 'get_page', get_page_mock)
        return get_page_mock

    def test_fetch_design_json(self) -> None:
        expected_response = {"ase": "ase2"}
        get_page_mock = self.mock_get_page_with_response(expected_response)

        output = self.data_fabric_interactor.fetch_data_fabric_json()
        self.assertEqual(output, expected_response)
        get_page_mock.assert_called_once_with(DATA_FABRIC_URI_PATH, headers=ANY, label="DataFabric.Ui")

    def test_fetch_design_dashboard_not_null_uri_stub_json(self) -> None:
        expected_response = {"ase": "ase2"}
        encoded_uri_stub = "testEncodedUuid"
        expected_uri = f"{DATA_FABRIC_DASHBOARD_URI_PATH}{encoded_uri_stub}"
        get_page_mock = self.mock_get_page_with_response(expected_response, expected_uri=expected_uri)

        output = self.data_fabric_interactor.fetch_data_fabric_dashboard_json(encoded_uri_stub)
        self.assertEqual(expected_response, output)
        get_page_mock.assert_called_once_with(expected_uri, headers=ANY, label="DataFabricDashboard.Ui")

    def test_fetch_design_dashboard_null_uri_stub_json(self) -> None:
        expected_response = {"ase": "ase2"}
        expected_uri = f"{DATA_FABRIC_DASHBOARD_URI_PATH}new"
        get_page_mock = self.mock_get_page_with_response(expected_response, expected_uri=expected_uri)

        output = self.data_fabric_interactor.fetch_data_fabric_dashboard_json()
        self.assertEqual(output, {"ase": "ase2"})
        get_page_mock.assert_called_once_with(expected_uri, headers=ANY, label="DataFabricDashboard.Ui")

    def test_fetch_design_json_with_custom_label(self) -> None:
        expected_response = {"ase": "ase2"}
        get_page_mock = self.mock_get_page_with_response(expected_response)

        output = self.data_fabric_interactor.fetch_data_fabric_json(locust_request_label="CustomLabel")
        self.assertEqual(output, expected_response)
        get_page_mock.assert_called_once_with(DATA_FABRIC_URI_PATH, headers=ANY, label="CustomLabel")

    def raise_http_error(self) -> None:
        raise HTTPError()

    def test_fetch_design_json_http_error(self) -> None:
        self.mock_get_page_with_response({"ase": "ase2"},
                                         raise_for_status_response=self.raise_http_error)
        with self.assertRaises(HTTPError):
            self.data_fabric_interactor.fetch_data_fabric_json()
