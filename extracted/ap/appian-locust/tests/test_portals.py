import json
import unittest
from unittest import mock

from requests import Response
from requests.exceptions import HTTPError

from appian_locust.utilities import logger
from appian_locust._interactor import _Interactor
from appian_locust._portals import _Portals

from tests.mock_reader import read_mock_file

log = logger.getLogger(__name__)


class TestRecords(unittest.TestCase):

    portal_page_dummy_response = {"portals": "hello"}

    def setUp(self) -> None:
        self.interactor: _Interactor = _Interactor("", "ase", portals_mode=True)
        setup_headers_mock = unittest.mock.Mock(return_value={})
        setattr(self.interactor, 'setup_sail_headers', setup_headers_mock)
        setattr(self.interactor, 'setup_request_headers', setup_headers_mock)
        self.portals_interactor: _Portals = _Portals(self.interactor)

    def test_portals_fetch_page_json(self) -> None:
        http_success_status_code = 200
        response_mock = unittest.mock.Mock(return_value=self.portal_page_dummy_response)
        response = Response()
        setattr(response, 'json', response_mock)
        setattr(response, 'status_code', http_success_status_code)
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, label, check_login: response if uri == "/performance-test/_/ui/page/one" else ""
        )
        setattr(self.interactor, 'get_page', get_page_mock)
        setattr(self.interactor, 'client', Client())

        output = self.portals_interactor.fetch_page_json("performance-test", "one")

        self.assertIsInstance(output, dict)
        self.assertDictEqual(output, self.portal_page_dummy_response)

    def test_portals_fetch_page_json_server_error(self) -> None:
        http_error_status_code = 500
        response_mock = unittest.mock.Mock(return_value=self.portal_page_dummy_response)
        response = Response()
        setattr(response, 'json', response_mock)
        setattr(response, 'status_code', http_error_status_code)
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, label, check_login: response if uri == "/performance-test/_/ui/page/one" else ""
        )
        setattr(self.interactor, 'get_page', get_page_mock)
        setattr(self.interactor, 'client', Client())

        with self.assertRaises(HTTPError):
            self.portals_interactor.fetch_page_json("performance-test", "one")

    def test_portals_get_full_url(self) -> None:
        full_url_expected_result = "/performance-test/_/ui/page/one"

        result = self.portals_interactor.get_full_url("performance-test", "one")

        self.assertEqual(result, full_url_expected_result)


class Client:
    base_path_override = "nothing"
