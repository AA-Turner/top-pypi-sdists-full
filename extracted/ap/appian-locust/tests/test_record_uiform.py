import unittest
import json

from locust import TaskSet, Locust
from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from appian_locust import AppianTaskSet


class TestRecordUiform(unittest.TestCase):
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
        parent_task_set = TaskSet(self.custom_locust)
        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "auth", ["", ""])
        self.task_set = AppianTaskSet(parent_task_set)
        self.task_set.host = ""

        # test_on_start_auth_success is covered here.
        self.custom_locust.set_response("auth?appian_environment=tempo", 200, '{}')
        self.task_set.on_start()

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
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/page/records/nav", 200, self.records_nav)

    def tearDown(self) -> None:
        self.task_set.on_stop()

    def test_open_summary_view(self) -> None:
        record = self.task_set.appian.visitor.visit_record_instance("Commits", "Actions Page")
        record_state = record.get_latest_state()
        self.assertIsNotNone(record_state, "Unexpected behavior: record_state is None")
        if record_state is not None:
            self.assertEqual("48b34e295ac83ec011d2aeb6d51527de", record_state["_cId"])

    def test_open_header_view(self) -> None:
        record = self.task_set.appian.visitor.visit_record_instance("Commits", "Actions Page", summary_view=False)
        record_state = record.get_latest_state()
        self.assertIsNotNone(record_state, "Unexpected behavior: record_state is None")
        if record_state is not None:
            self.assertEqual("f658254dfed5a0987dd32148f2594053", record_state["_cId"])

    def test_switch_to_header_view(self) -> None:
        record = self.task_set.appian.visitor.visit_record_instance("Commits", "Actions Page")
        record.get_header_view()
        record_state = record.get_latest_state()
        self.assertIsNotNone(record_state, "Unexpected behavior: record_state is None")
        if record_state is not None:
            self.assertEqual("f658254dfed5a0987dd32148f2594053", record_state["_cId"])

    def test_switch_to_summary_view(self) -> None:
        record = self.task_set.appian.visitor.visit_record_instance("Commits", "Actions Page", summary_view=False)
        record.get_summary_view()
        record_state = record.get_latest_state()
        self.assertIsNotNone(record_state, "Unexpected behavior: record_state is None")
        if record_state is not None:
            self.assertEqual("48b34e295ac83ec011d2aeb6d51527de", record_state["_cId"])
