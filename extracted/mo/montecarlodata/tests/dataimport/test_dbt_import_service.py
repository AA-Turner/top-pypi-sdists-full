from unittest import TestCase
from unittest.mock import Mock, patch
from uuid import uuid4

import click
from box import Box
from pycarlo.features.dbt import DbtImporter
from pycarlo.features.exceptions import MultipleResourcesFoundException

from montecarlodata.dataimport.dbt import DbtImportService


class DbtImportServiceTests(TestCase):
    project_name = "default-project"
    job_name = "default-job"
    manifest_path = "./manifest.json"
    run_results_path = "./run_results.json"
    logs_path = "./logs.txt"

    def setUp(self):
        self.mock_config = Mock()
        self.mock_mc_client = Mock()
        self.mock_user_service = Mock()
        self.mock_pii_service = Mock()
        self.mock_pii_service.get_pii_filters_config.return_value = None

        self.service = DbtImportService(
            config=self.mock_config,
            command_name="test",
            mc_client=self.mock_mc_client,
            user_service=self.mock_user_service,
            pii_service=self.mock_pii_service,
        )

    @patch.object(DbtImporter, "import_run")
    def test_import_run_with_no_connection_id(self, mock_import_run: Mock):
        # given
        connection_id = None

        # when
        self.service.import_run(
            project_name=self.project_name,
            job_name=self.job_name,
            manifest_path=self.manifest_path,
            run_results_path=self.run_results_path,
            logs_path=self.logs_path,
            connection_id=connection_id,
        )

        # then
        self.mock_user_service.get_warehouse_for_connection.assert_not_called()
        mock_import_run.assert_called_once_with(
            project_name=self.project_name,
            job_name=self.job_name,
            manifest_path=self.manifest_path,
            run_results_path=self.run_results_path,
            logs_path=self.logs_path,
            resource_id=None,
        )

    @patch.object(click, "echo")
    @patch.object(DbtImporter, "import_run")
    def test_import_run_with_no_connection_id_and_multiple_warehouses(
        self, mock_import_run: Mock, mock_echo: Mock
    ):
        # given
        connection_id = None
        mock_import_run.side_effect = MultipleResourcesFoundException()

        # when
        with self.assertRaises(click.Abort):
            self.service.import_run(
                project_name=self.project_name,
                job_name=self.job_name,
                manifest_path=self.manifest_path,
                run_results_path=self.run_results_path,
                logs_path=self.logs_path,
                connection_id=connection_id,
            )

        # then
        self.mock_user_service.get_warehouse_for_connection.assert_not_called()
        mock_import_run.assert_called_once_with(
            project_name=self.project_name,
            job_name=self.job_name,
            manifest_path=self.manifest_path,
            run_results_path=self.run_results_path,
            logs_path=self.logs_path,
            resource_id=None,
        )
        mock_echo.assert_called_once_with(
            "Error - Multiple resources found, please specify a connection id.",
            err=True,
        )

    @patch.object(click, "echo")
    @patch.object(DbtImporter, "import_run")
    def test_import_run_with_invalid_connection_id(self, mock_import_run: Mock, mock_echo: Mock):
        # given
        connection_id = uuid4()
        self.mock_user_service.get_warehouse_for_connection.return_value = None

        # when
        with self.assertRaises(click.Abort):
            self.service.import_run(
                project_name=self.project_name,
                job_name=self.job_name,
                manifest_path=self.manifest_path,
                run_results_path=self.run_results_path,
                logs_path=self.logs_path,
                connection_id=connection_id,
            )

        # then
        self.mock_user_service.get_warehouse_for_connection.assert_called_once_with(connection_id)
        mock_import_run.assert_not_called()
        mock_echo.assert_called_once_with(
            f"Error - Could not find a connection with id: {connection_id}", err=True
        )

    @patch.object(DbtImporter, "import_run")
    def test_import_run_with_valid_connection_id(self, mock_import_run: Mock):
        # given
        connection_id = uuid4()
        resource_id = str(uuid4())
        self.mock_user_service.get_warehouse_for_connection.return_value = Box(
            {"uuid": resource_id}
        )

        # when
        self.service.import_run(
            project_name=self.project_name,
            job_name=self.job_name,
            manifest_path=self.manifest_path,
            run_results_path=self.run_results_path,
            logs_path=self.logs_path,
            connection_id=connection_id,
        )

        # then
        self.mock_user_service.get_warehouse_for_connection.assert_called_once_with(connection_id)
        mock_import_run.assert_called_once_with(
            project_name=self.project_name,
            job_name=self.job_name,
            manifest_path=self.manifest_path,
            run_results_path=self.run_results_path,
            logs_path=self.logs_path,
            resource_id=resource_id,
        )
