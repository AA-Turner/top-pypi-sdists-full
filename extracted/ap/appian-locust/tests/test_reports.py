from requests import Response, Request
from .mock_reader import read_mock_file
from appian_locust._interactor import _Interactor
from appian_locust._reports import ALL_REPORTS_URI, _Reports
import unittest
from unittest import mock
import json


class TestReports(unittest.TestCase):
    reports = read_mock_file("reports_response.json")
    reports_modified = read_mock_file("reports_response_modified.json")
    reports_interface = read_mock_file("reports_interface.json")
    reports_nav = read_mock_file("reports_nav.json")

    def setUp(self) -> None:
        self.interactor: _Interactor = _Interactor("", "ase")
        setup_headers_mock = unittest.mock.Mock(return_value={})
        setattr(self.interactor, 'setup_sail_headers', setup_headers_mock)
        setattr(self.interactor, 'setup_request_headers', setup_headers_mock)
        self.reports_interactor: _Reports = _Reports(self.interactor)

    def test_reports_get(self) -> None:
        response_mock = unittest.mock.Mock(return_value=json.loads(self.reports))
        response = Response()
        setattr(response, 'json', response_mock)
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, label: response if uri == ALL_REPORTS_URI else Response()
        )
        setattr(self.interactor, 'get_page', get_page_mock)

        report = self.reports_interactor.get_report("RTE Basic Test Report")
        self.assertEqual("RTE Basic Test Report", report['title'].strip())

    def test_reports_get_first_of_multiple(self) -> None:
        response_mock = unittest.mock.Mock(return_value=json.loads(self.reports))
        response = Response()
        setattr(response, 'json', response_mock)
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, label: response if uri == ALL_REPORTS_URI else Response()
        )
        setattr(self.interactor, 'get_page', get_page_mock)

        report = self.reports_interactor.get_report("Barcode", exact_match=False)
        self.assertEqual("Barcode Field Tester", report['title'].strip())

    def test_reports_get_corrupt_report(self) -> None:
        corrupt_reports = self.reports.replace('"title": "!!SAIL test charts"', '"corrupt_title": "!!SAIL test charts"')
        response_mock = unittest.mock.Mock(return_value=json.loads(corrupt_reports))
        response = Response()
        setattr(response, 'json', response_mock)
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, label: response if uri == ALL_REPORTS_URI else Response()
        )
        setattr(self.interactor, 'get_page', get_page_mock)

        all_reports = self.reports_interactor.get_all()
        self.assertTrue("ERROR::1" in str(all_reports))
        self.assertEqual(1, self.reports_interactor._errors)

    def test_reports_zero_reports(self) -> None:
        corrupt_reports = self.reports.replace('"entries"', '"nonexistent_entries"')
        response_mock = unittest.mock.Mock(return_value=json.loads(corrupt_reports))
        response = Response()
        setattr(response, 'json', response_mock)
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, label: response if uri == ALL_REPORTS_URI else Response()
        )
        setattr(self.interactor, 'get_page', get_page_mock)

        all_reports = self.reports_interactor.get_all()
        self.assertTrue(all_reports == {})

    def test_reports_get_missing_report(self) -> None:
        response_mock = unittest.mock.Mock(return_value=json.loads(self.reports))
        response = Response()
        setattr(response, 'json', response_mock)
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, label: response if uri == ALL_REPORTS_URI else Response()
        )
        setattr(self.interactor, 'get_page', get_page_mock)

        with self.assertRaisesRegex(Exception, "There is no report with name .* in the system under test.*"):
            self.reports_interactor.get_report("some random word", False)

    def test_reports_fetch_report_json(self) -> None:
        response_mock = unittest.mock.Mock(return_value={"ase": "ase2"})
        response_all_ok_mock = unittest.mock.Mock(return_value="")
        response = Response()
        setattr(response, 'json', response_mock)
        setattr(response, 'raise_for_status', response_all_ok_mock)  # ensure response.ok returns true
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, headers, label: response if uri == "some_url" else Response(),
        )
        setattr(self.interactor, 'get_page', get_page_mock)
        get_form_uri_mock = unittest.mock.Mock(return_value="some_url")
        setattr(self.reports_interactor, "get_report_form_uri", get_form_uri_mock)

        output = self.reports_interactor.fetch_report_json("RTE Basic Test Report::qdjDPA")
        self.assertEqual(output, {"ase": "ase2"})

    def test_reports_get_form_uri(self) -> None:
        response_mock = unittest.mock.Mock(return_value=json.loads(self.reports))
        response = Response()
        setattr(response, 'json', response_mock)
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, label: response if uri == ALL_REPORTS_URI else Response()
        )

        setattr(self.interactor, 'get_page', get_page_mock)
        output = self.reports_interactor.get_report_form_uri("RTE Basic Test Report")
        self.assertEqual(output, "/suite/rest/a/sites/latest/D6JMim/pages/p.reports/report/qdjDPA/reportlink")

    def test_reports_get_report_requires_search(self) -> None:
        response_mock = unittest.mock.Mock(return_value=json.loads(self.reports))
        response = Response()
        setattr(response, 'json', response_mock)

        valid_response_mock = unittest.mock.Mock(return_value=json.loads(self.reports_modified))
        valid_response = Response()
        setattr(valid_response, 'json', valid_response_mock)

        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, label: response if uri == ALL_REPORTS_URI else valid_response
        )
        setattr(self.interactor, 'get_page', get_page_mock)
        self.reports_interactor.get_report("ASE", False)


if __name__ == '__main__':
    unittest.main()
