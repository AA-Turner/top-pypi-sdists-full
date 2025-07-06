import unittest
import json
from appian_locust.uiform import ApplicationUiForm, DesignUiForm

from locust import TaskSet, Locust
from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from appian_locust import AppianTaskSet


class TestDesignUiform(unittest.TestCase):
    design_landing_page = read_mock_file("design_landing_page.json")

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

    def test_click_application(self) -> None:
        self.custom_locust.set_response("/suite/rest/a/applications/latest/app/design", 200, self.design_landing_page)
        design = self.task_set.appian.visitor.visit_design()
        result_state = '{"ase": "ase"}'
        self.custom_locust.set_response("/suite/rest/a/applications/latest/app/design", 200, result_state)
        application = design.click_application("Appian CMF")
        self.assertEqual(type(application), ApplicationUiForm)
        self.assertEqual(application.get_latest_state(), json.loads(result_state))

    def test_create_app_and_record_type(self) -> None:
        app_landing_page = read_mock_file("design_app_landing_page.json")

        create_object_modal = read_mock_file("design_new_object_modal.json")
        security_page = read_mock_file("design_security_page.json")

        def prepare_create_object() -> None:
            self.custom_locust.enqueue_response(200, create_object_modal)
            self.custom_locust.enqueue_response(200, create_object_modal)
            self.custom_locust.enqueue_response(200, security_page)
        self.custom_locust.enqueue_response(200, self.design_landing_page)
        prepare_create_object()
        self.custom_locust.enqueue_response(200, app_landing_page)
        prepare_create_object()
        self.custom_locust.enqueue_response(200, app_landing_page)
        prepare_create_object()
        self.custom_locust.enqueue_response(200, app_landing_page)

        app_form = self.task_set.appian.visitor.visit_design().create_application('locust app')
        app_form.create_record_type('my record type')
        app_form.create_report('my report')
