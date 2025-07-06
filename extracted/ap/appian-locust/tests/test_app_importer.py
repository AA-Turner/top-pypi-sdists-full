from locust import TaskSet, User
from appian_locust.utilities.helper import ENV
from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from appian_locust import AppianTaskSet

import os
import unittest

CURR_FILE_PATH = os.path.dirname(os.path.realpath(__file__))


# Set these values to an integration endpoint for etoe testing,
integration_url = ""
auth = ["a", "b"]


class TestAppImport(unittest.TestCase):
    def setUp(self) -> None:
        record_mode = True if integration_url else False
        self.custom_locust = CustomLocust(User(ENV), integration_url=integration_url, record_mode=record_mode)
        parent_task_set = TaskSet(self.custom_locust)
        setattr(parent_task_set, "host", integration_url)
        setattr(parent_task_set, "auth", auth)
        setattr(self.custom_locust, "record_mode", True)
        self.task_set = AppianTaskSet(parent_task_set)

        ENV.stats.clear_all()

    def test_app_importer_e_to_e(self) -> None:
        self.task_set.on_start()

        path_to_file = os.path.join(CURR_FILE_PATH, "resources", "Constant Test App.zip")
        if not os.path.exists(path_to_file):
            raise Exception(f"file not found {path_to_file}")

        # Order of execution is, navigate to /design, click import, upload doc, fill upload field, click import again
        if not integration_url:
            self.custom_locust.enqueue_response(200, read_mock_file("design_landing_page.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_click_import_button_resp_init.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_soap_app_upload_response.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_upload_to_file_upload_field_doc_resp.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_click_import_button_resp_final.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_landing_page.json"))

        self.task_set.appian.visitor.visit_design().import_application(path_to_file)

    def test_app_importer_e_to_e_for_inspect_and_import(self) -> None:
        self.task_set.on_start()

        path_to_file = os.path.join(CURR_FILE_PATH, "resources", "Constant Test App.zip")
        if not os.path.exists(path_to_file):
            raise Exception(f"file not found {path_to_file}")

        # Order of execution is, navigate to /design, click import, upload doc, fill upload field, click import again
        if not integration_url:
            self.custom_locust.enqueue_response(200, read_mock_file("design_landing_page.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_click_import_button_resp_init.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_soap_app_upload_response.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_upload_to_file_upload_field_doc_resp.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_inspection_results_resp.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_click_import_button_resp_final.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_landing_page.json"))

        self.task_set.appian.visitor.visit_design().import_application(app_file_path=path_to_file, inspect_and_import=True)

    def test_app_importer_e_to_e_with_cust_file(self) -> None:
        self.task_set.on_start()

        path_to_app = os.path.join(CURR_FILE_PATH, "resources", "Constant Test App.zip")
        path_to_cust_file = os.path.join(CURR_FILE_PATH, "resources", "Constant Test App.properties")

        for path_to_file in [path_to_app, path_to_cust_file]:
            if not os.path.exists(path_to_file):
                raise Exception(f"file not found {path_to_file}")

        if not integration_url:
            self.custom_locust.enqueue_response(200, read_mock_file("design_landing_page.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_click_import_button_resp_init.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_soap_app_upload_response.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_upload_to_file_upload_field_doc_resp.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_check_import_cust_box.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_constant_props_upload_response.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_upload_to_file_upload_field_doc_resp.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_click_import_button_resp_final.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_landing_page.json"))

        self.task_set.appian.visitor.visit_design().import_application(path_to_app, customization_file_path=path_to_cust_file)

    def test_app_importer_e_to_e_with_cust_file_error(self) -> None:
        self.task_set.on_start()

        path_to_app = os.path.join(CURR_FILE_PATH, "resources", "Constant Test App.zip")
        path_to_cust_file = os.path.join(CURR_FILE_PATH, "resources", "Constant Test App.properties")

        for path_to_file in [path_to_app, path_to_cust_file]:
            if not os.path.exists(path_to_file):
                raise Exception(f"file not found {path_to_file}")
        if not integration_url:
            self.custom_locust.enqueue_response(200, read_mock_file("design_landing_page.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_click_import_button_resp_init.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_soap_app_upload_response.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_upload_to_file_upload_field_doc_resp.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_check_import_cust_box.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_constant_props_upload_response.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_upload_to_file_upload_field_doc_resp.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_click_import_failed_validation.json"))
            self.custom_locust.enqueue_response(200, read_mock_file("design_landing_page.json"))

        with self.assertRaises(Exception) as e:
            self.task_set.appian.visitor.visit_design().import_application(path_to_app, customization_file_path=path_to_cust_file)


if __name__ == '__main__':
    unittest.main()
