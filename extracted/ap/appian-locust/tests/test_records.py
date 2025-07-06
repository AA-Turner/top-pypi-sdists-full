import json
import unittest
from typing import Any
from unittest import mock

from appian_locust.utilities import logger
from appian_locust.uiform import SailUiForm
from appian_locust._interactor import _Interactor
from appian_locust._records import _Records
from locust import Locust, TaskSet

from requests.exceptions import HTTPError
from tests.mock_client import CustomLocust
from tests.mock_reader import read_mock_file
from appian_locust._records import RECORDS_INTERFACE_PATH

log = logger.getLogger(__name__)


class TestRecords(unittest.TestCase):
    record_types = read_mock_file("record_types_response.json")
    # Record Instance List for a specific RecordType
    records = read_mock_file("records_response.json")
    grid_records = read_mock_file("records_grid_response.json")
    # Record Summary dashboard response for a specific Record Instance
    record_summary_view = read_mock_file("record_summary_view_response.json")
    record_instance_name = "Actions Page"
    records_interface = read_mock_file("records_interface.json")
    records_nav = read_mock_file("records_nav.json")

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(Locust())
        setattr(self.custom_locust.client, "feature_flag", "")
        setattr(self.custom_locust.client, "feature_flag_extended", "")

        # test_on_start_auth_success is covered here.
        self.custom_locust.set_response("auth?appian_environment=tempo", 200, '{}')
        self.interactor = _Interactor(self.custom_locust.client, "")
        self.interactor.login(["", ""])
        self.record_interactor = _Records(self.interactor)

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
            "/suite/rest/a/sites/latest/D6JMim/page/p.records/record/lQB0K7YxC0UQ2Fhx4pmY1F49C_MjItD4hbtRdKDmOo6V3MOBxI47ipGa_bJKZf86CLtvOCp1cfX-sa2O9hp6WTKZpbGo5MxRaaTwMkcYMeDl8kN8Hg/view/summary",
            200,
            self.record_summary_view)
        self.custom_locust.set_response(RECORDS_INTERFACE_PATH, 200, self.records_interface)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/page/p.records/nav", 200, self.records_nav)

    def test_records_get_all(self) -> None:
        all_records = self.record_interactor.get_all()
        self.assertIsInstance(all_records, dict)

    def test_records_get_all_http_error(self) -> None:
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/commit", 500,
                                        self.records)
        with self.assertLogs(level="WARN") as msg:
            self.record_interactor.get_all()
        self.assertIn("500 Server Error", msg.output[0])

    def test_records_get_all_bad_response(self) -> None:

        # setting up bad response
        temp_record_types = self.record_types.replace(
            '"rel":"x-web-bookmark"', '"rel":"bad_x-web-bookmark_bad"'
        ).replace(
            '"#t":"CardLayout"', '"#t":"bad_CardLayout_bad"'
        )
        self.custom_locust.set_response("/suite/rest/a/applications/latest/app/records/view/all", 200,
                                        temp_record_types)
        with (self.assertRaisesRegex(Exception, "Unexpected response on Get call of All Records")):
            self.record_interactor.get_all()

    def test_records_get_corrupt_records(self) -> None:
        # setting up bad response
        corrupt_records = self.records.replace('"_recordRef": "lQB0K7YxC0UQ2Fhx4pmY1F49C_MjItD4hbtRdKDmOo6V3MOBxI47ipGa_bJKZf86CLtvOCp1cfX-sa2O9hu7mTKKv82PEWF9q1lBcroZD_VQpwcQDs"',
                                               '"corrupt_recordRef": "lQB0K7YxC0UQ2Fhx4pmY1F49C_MjItD4hbtRdKDmOo6V3MOBxI47ipGa_bJKZf86CLtvOCp1cfX-sa2O9hu7mTKKv82PEWF9q1lBcroZD_VQpwcQDs"')
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/commit", 200,
                                        corrupt_records)
        self.record_interactor.get_all_record_types()
        all_commit_records = self.record_interactor.get_all_records_of_record_type('Commits')
        self.assertTrue("ERROR::1" in str(all_commit_records))
        self.assertTrue(self.record_interactor._errors == 1)

    def test_records_get_all_mobile(self) -> None:
        mobile_record_interactor = _Records(self.interactor, is_mobile_client=True)
        all_records = self.record_interactor.get_all()
        self.assertIsInstance(all_records, dict)

    def test_records_get_by_type(self) -> None:
        # Given
        record_type = 'Customer Service Requests'
        self.record_interactor.get_all_record_types()

        # When
        all_records = self.record_interactor.get_all_records_of_record_type(record_type)

        # Then
        self.assertIsInstance(all_records, dict)

    def test_records_get_by_type_and_column(self) -> None:
        # Given
        record_type = 'Customer Service Requests'
        self.record_interactor.get_all_record_types()

        # When
        all_customer_service_request_records = self.record_interactor.get_all_records_of_record_type(record_type, 0)
        all_customer_service_request_records_dict = all_customer_service_request_records['Customer Service Requests']
        first_row_key = 'I49K-V46X::lIBHer_bdD8Emw8hLPETeiApJ24AA5ZJilzpBmewf--PdHDSUx022ZVdk6bhtcs5w_3twr_z1drDBwn8DKfhPp90o_A4GrZbDSh09DYkh5Mfq48'
        last_row_key = '6L5P-GCEE::lIBHer_bdD8Emw8hLPETeiApJ24AA5ZJilzpBmewf--PdHDSUx022ZVdk6bhtcs5w_3twr_z1drDBwn_zmfhFySF7_Fv1bKeyNOM2BWVFmfhruJ'
        wrong_column_key = 'Alcubierre Taxi Service::lIBHer_bdD8Emw8hLLETeiApBrxq-qoA49oyo6ZbfRANWNchnXIC8_QQLHMvQo3q8_3W_uY-NIUjTsvBQ19h-2W6cjGnZIXyKpKm91T6bH_IGdY'
        # Then
        self.assertIsInstance(all_customer_service_request_records, dict)
        # asserting first and last row of correct column
        self.assertTrue(
            first_row_key in all_customer_service_request_records_dict)
        self.assertTrue(
            last_row_key in all_customer_service_request_records_dict)
        # asserting list of entries to ensure no extra ones are returned
        self.assertEqual(len(all_customer_service_request_records_dict.keys()), 25)
        # asserting that a record link that does not belong to the given column is not returned
        self.assertFalse(wrong_column_key in all_customer_service_request_records_dict)

    def test_records_get_by_type_and_column_index_out_of_bounds(self) -> None:
        record_type = 'Customer Service Requests'
        self.record_interactor.get_all_record_types()
        with self.assertRaises(Exception) as e:
            self.record_interactor.get_all_records_of_record_type(record_type, 1000)

    def test_records_get_by_type_mobile(self) -> None:
        # Given
        record_type = 'Commits'
        mobile_record_interactor = _Records(self.interactor, is_mobile_client=True)
        mobile_record_interactor.get_all_record_types()

        # When
        all_records = mobile_record_interactor.get_all_records_of_record_type(record_type)

        # Then
        self.assertIsInstance(all_records, dict)

    def test_records_fetch_record_instance(self) -> None:
        record = self.record_interactor.fetch_record_instance(
            "Commits", self.record_instance_name, False)
        self.assertIsInstance(record, dict)

    def test_records_fetch_record_instance_no_record_type(self) -> None:
        with self.assertRaisesRegex(Exception,
                                    "There is no record type with name .* in the system under test"):
            self.record_interactor.fetch_record_instance("something else 1", self.record_instance_name, False)

    def test_records_fetch_record_instance_missing(self) -> None:
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/commit?searchTerm=something%20else", 200,
                                        self.records)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/BE5pSw?searchTerm=something%20else", 200,
                                        self.grid_records)
        with self.assertRaisesRegex(Exception,
                                    "There is no record with name .* found in record type .*"):
            self.record_interactor.fetch_record_instance("Commits", "something else", False)

    def test_records_fetch_record_instance_needs_search(self) -> None:
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/commit?searchTerm=Fake%20Record", 200,
                                        self.grid_records)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/BE5pSw?searchTerm=Fake%20Record", 200,
                                        self.grid_records)
        with self.assertRaisesRegex(Exception,
                                    "There is no record with name .* found in record type .*"):
            self.record_interactor.fetch_record_instance("Commits", "Fake Record", False)

    def test_records_fetch_record_type(self) -> None:
        self.record_interactor.get_all()
        output = self.record_interactor.fetch_record_type("Commits")
        self.assertIsInstance(output, dict)

    def test_records_fetch_record_type_recaching(self) -> None:
        self.record_interactor._record_types = dict()  # Resetting the cache.
        output = self.record_interactor.fetch_record_type("Commits")
        self.assertIsInstance(output, dict)

    def test_records_fetch_record_type_missing_record_type(self) -> None:
        with self.assertRaisesRegex(Exception,
                                    "There is no record type with name .* in the system under test"):
            self.record_interactor.fetch_record_type("something else")

    def test_records_visit(self) -> None:
        output_json = self.record_interactor.visit_record_instance(
            "Commits", self.record_instance_name, exact_match=False, locust_request_label='')
        self.assertIsInstance(output_json, dict)

    def test_records_visit_random_success(self) -> None:
        self.custom_locust.set_default_response(200, self.record_summary_view)
        output_json = self.record_interactor.visit_record_instance(locust_request_label='')
        self.assertIsInstance(output_json, dict)

    def test_records_visit_random_of_selected_record_type_success(self) -> None:
        self.custom_locust.set_default_response(200, self.record_summary_view)
        output_json = self.record_interactor.visit_record_instance(record_type="Commits", locust_request_label='')
        self.assertIsInstance(output_json, dict)

    def test_records_visit_random_no_record_type_failure(self) -> None:
        with self.assertRaisesRegex(Exception,
                                    "If record_name parameter is specified, record_type must also be included"):
            self.record_interactor.visit_record_instance(record_name=self.record_instance_name, exact_match=False)

    def test_records_visit_with_urlstub(self) -> None:
        output_json = self.record_interactor.visit_record_instance(
            "Commits", self.record_instance_name, "summary", exact_match=False, locust_request_label='')
        self.assertIsInstance(output_json, dict)

    def test_record_types_visit(self) -> None:
        output_json = self.record_interactor.visit_record_type(
            "Commits")
        self.assertIsInstance(output_json, dict)

    def test_record_type_visit_random_success(self) -> None:
        self.custom_locust.set_default_response(200, self.records)
        output_json = self.record_interactor.visit_record_type()
        self.assertIsInstance(output_json, dict)
        self.assertEqual(output_json.get("#t"), "UiConfig")

    def test_record_type_visit_failure(self) -> None:
        with self.assertRaises(Exception) as e:
            self.record_interactor.visit_record_type(record_type="fake type")

    def test_get_random_record(self) -> None:
        self.record_interactor._record_types = dict()
        self.record_interactor._records = dict()
        record_type, record_name = self.record_interactor._get_random_record_instance()
        self.assertTrue(record_type == 'Commits' or record_type == 'Customer Service Requests')
        self.assertIn(record_name, list(self.record_interactor._records[record_type].keys()))

    def test_get_random_record_get_all(self) -> None:
        mock_get_all = mock.Mock()
        setattr(self.record_interactor, 'get_all', mock_get_all)
        with self.assertRaises(Exception):
            self.record_interactor._get_random_record_instance()
            mock_get_all.assert_called_once()


if __name__ == '__main__':
    unittest.main()
