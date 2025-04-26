import os
import subprocess
from unittest import TestCase
from unittest.mock import Mock, patch

from airflow.exceptions import AirflowException
from airflow.utils.context import Context

from airflow_mcd.operators.dbt import DbtOperator


class DbtOperatorTests(TestCase):

    @patch("airflow_mcd.operators.dbt.subprocess")
    @patch("airflow_mcd.operators.dbt.open")
    @patch("airflow_mcd.operators.dbt.DbtImporter")
    @patch("airflow_mcd.operators.dbt.Client")
    @patch("airflow_mcd.operators.dbt.SessionHook")
    @patch.dict(os.environ, {}, clear=True)
    def test_operator_with_minimal_args(
            self,
            mock_mc_session_hook: Mock,
            mock_mc_client: Mock,
            mock_dbt_importer: Mock,
            mock_open: Mock,
            mock_subprocess: Mock,
    ):
        # given
        mock_stdout = Mock()
        mock_stdout.readline.side_effect = [b"logging...\n"]
        mock_process = Mock()
        mock_process.returncode = 0
        mock_process.stdout = mock_stdout
        mock_subprocess.Popen.return_value = mock_process
        mock_subprocess.PIPE = subprocess.PIPE
        mock_subprocess.STDOUT = subprocess.STDOUT

        mock_log_file = Mock()
        mock_open.return_value = mock_log_file

        mock_mc_session = Mock()
        mock_mc_session_hook_instance = Mock()
        mock_mc_session_hook_instance.get_conn.return_value = mock_mc_session
        mock_mc_session_hook.return_value = mock_mc_session_hook_instance

        mock_mc_client_instance = Mock()
        mock_mc_client.return_value = mock_mc_client_instance

        mock_dbt_importer_instance = Mock()
        mock_dbt_importer.return_value = mock_dbt_importer_instance

        operator = DbtOperator(
            task_id="test-operator",
            command="run",
            project_name="test-project",
            job_name="test-job",
            mc_conn_id="mc-connection",
            mc_include_logs=True,
        )

        # when
        operator.execute(Context())

        # verify expected call to submit dbt command
        mock_subprocess.Popen.assert_called_once_with(
            ["dbt", "run"],
            env={},
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=".",
            close_fds=True,
        )

        # verify expected call to open local log file
        mock_open.assert_called_once_with(
            "./dbt.log",
            "w",
        )

        # verify expected calls to write to local log file
        mock_log_file.write.assert_called_once_with("logging...\n")
        mock_log_file.close.assert_called_once_with()

        # verify expected call to wait for dbt command to complete
        mock_process.wait.assert_called_once_with()

        # verify expected call to create MC SessionHook
        mock_mc_session_hook.assert_called_once_with(
            mcd_session_conn_id="mc-connection"
        )

        # verify expected call to create MC API client
        mock_mc_client.assert_called_once_with(
            session=mock_mc_session
        )

        # verify expected call to create MC DbtImporter
        mock_dbt_importer.assert_called_once_with(
            mc_client=mock_mc_client_instance
        )

        # verify expected call to import dbt run results to MC
        mock_dbt_importer_instance.import_run.assert_called_once_with(
            manifest_path="./target/manifest.json",
            run_results_path="./target/run_results.json",
            logs_path="./dbt.log",
            project_name="test-project",
            job_name="test-job",
            resource_id=None,
        )

    @patch("airflow_mcd.operators.dbt.subprocess")
    @patch("airflow_mcd.operators.dbt.open")
    @patch("airflow_mcd.operators.dbt.DbtImporter")
    @patch("airflow_mcd.operators.dbt.Client")
    @patch("airflow_mcd.operators.dbt.SessionHook")
    @patch.dict(os.environ, {}, clear=True)
    def test_operator_with_full_args(
            self,
            mock_mc_session_hook: Mock,
            mock_mc_client: Mock,
            mock_dbt_importer: Mock,
            mock_open: Mock,
            mock_subprocess: Mock,
    ):
        # given
        mock_stdout = Mock()
        mock_stdout.readline.side_effect = [b"logging...\n"]
        mock_process = Mock()
        mock_process.returncode = 0
        mock_process.stdout = mock_stdout
        mock_subprocess.Popen.return_value = mock_process
        mock_subprocess.PIPE = subprocess.PIPE
        mock_subprocess.STDOUT = subprocess.STDOUT

        mock_log_file = Mock()
        mock_open.return_value = mock_log_file

        mock_mc_session = Mock()
        mock_mc_session_hook_instance = Mock()
        mock_mc_session_hook_instance.get_conn.return_value = mock_mc_session
        mock_mc_session_hook.return_value = mock_mc_session_hook_instance

        mock_mc_client_instance = Mock()
        mock_mc_client.return_value = mock_mc_client_instance

        mock_dbt_importer_instance = Mock()
        mock_dbt_importer.return_value = mock_dbt_importer_instance

        operator = DbtOperator(
            task_id="test-operator",
            command="run",
            project_name="test-project",
            job_name="test-job",
            mc_conn_id="mc-connection",
            mc_resource_id="resource-id",
            mc_include_logs=True,
            dir="/usr/local/dbt/project",
            dbt_bin="/usr/bin/dbt",
            env={"TEST": "ING"},
            profiles_dir="/usr/local/dbt/profiles",
            target_path="/usr/local/dbt/target",
            target="prod",
            vars={"foo": "bar"},
            models="some_model",
            exclude="excluded_model",
            select="selected_model",
            warn_error=True,
            full_refresh=True,
            data=True,
            schema=True,
        )

        # when
        operator.execute(Context())

        # verify expected call to submit dbt command
        mock_subprocess.Popen.assert_called_once_with(
            [
                "/usr/bin/dbt",
                "--warn-error",
                "run",
                "--profiles-dir",
                "/usr/local/dbt/profiles",
                "--target",
                "prod",
                "--vars",
                "{\"foo\": \"bar\"}",
                "--models",
                "some_model",
                "--exclude",
                "excluded_model",
                "--select",
                "selected_model",
                "--full-refresh",
                "--data",
                "--schema",
            ],
            env={
                "TEST": "ING",
            },
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd="/usr/local/dbt/project",
            close_fds=True,
        )

        # verify expected call to open local log file
        mock_open.assert_called_once_with(
            "/usr/local/dbt/project/dbt.log",
            "w",
        )

        # verify expected calls to write to local log file
        mock_log_file.write.assert_called_once_with("logging...\n")
        mock_log_file.close.assert_called_once_with()

        # verify expected call to wait for dbt command to complete
        mock_process.wait.assert_called_once_with()

        # verify expected call to create MC SessionHook
        mock_mc_session_hook.assert_called_once_with(
            mcd_session_conn_id="mc-connection"
        )

        # verify expected call to create MC API client
        mock_mc_client.assert_called_once_with(
            session=mock_mc_session
        )

        # verify expected call to create MC DbtImporter
        mock_dbt_importer.assert_called_once_with(
            mc_client=mock_mc_client_instance
        )

        # verify expected call to import dbt run results to MC
        mock_dbt_importer_instance.import_run.assert_called_once_with(
            manifest_path="/usr/local/dbt/target/manifest.json",
            run_results_path="/usr/local/dbt/target/run_results.json",
            logs_path="/usr/local/dbt/project/dbt.log",
            project_name="test-project",
            job_name="test-job",
            resource_id="resource-id",
        )

    @patch("airflow_mcd.operators.dbt.subprocess")
    @patch("airflow_mcd.operators.dbt.open")
    @patch("airflow_mcd.operators.dbt.DbtImporter")
    @patch("airflow_mcd.operators.dbt.Client")
    @patch("airflow_mcd.operators.dbt.SessionHook")
    @patch.dict(os.environ, {}, clear=True)
    def test_operator_with_failed_dbt_command(
            self,
            mock_mc_session_hook: Mock,
            mock_mc_client: Mock,
            mock_dbt_importer: Mock,
            mock_open: Mock,
            mock_subprocess: Mock,
    ):
        # given
        mock_stdout = Mock()
        mock_stdout.readline.side_effect = [b"logging...\n"]
        mock_process = Mock()
        mock_process.returncode = 1
        mock_process.stdout = mock_stdout
        mock_subprocess.Popen.return_value = mock_process
        mock_subprocess.PIPE = subprocess.PIPE
        mock_subprocess.STDOUT = subprocess.STDOUT

        mock_log_file = Mock()
        mock_open.return_value = mock_log_file

        mock_mc_session = Mock()
        mock_mc_session_hook_instance = Mock()
        mock_mc_session_hook_instance.get_conn.return_value = mock_mc_session
        mock_mc_session_hook.return_value = mock_mc_session_hook_instance

        mock_mc_client_instance = Mock()
        mock_mc_client.return_value = mock_mc_client_instance

        mock_dbt_importer_instance = Mock()
        mock_dbt_importer.return_value = mock_dbt_importer_instance

        operator = DbtOperator(
            task_id="test-operator",
            command="run",
            project_name="test-project",
            job_name="test-job",
            mc_conn_id="mc-connection",
            mc_include_logs=True,
        )

        # when
        with self.assertRaises(AirflowException) as context:
            operator.execute(Context())

        # verify expected exception
        self.assertEqual("dbt command failed", str(context.exception))

        # verify expected call to submit dbt command
        mock_subprocess.Popen.assert_called_once_with(
            ["dbt", "run"],
            env={},
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=".",
            close_fds=True,
        )

        # verify expected call to open local log file
        mock_open.assert_called_once_with(
            "./dbt.log",
            "w",
        )

        # verify expected calls to write to local log file
        mock_log_file.write.assert_called_once_with("logging...\n")
        mock_log_file.close.assert_called_once_with()

        # verify expected call to wait for dbt command to complete
        mock_process.wait.assert_called_once_with()

        # verify expected call to create MC SessionHook
        mock_mc_session_hook.assert_called_once_with(
            mcd_session_conn_id="mc-connection"
        )

        # verify expected call to create MC API client
        mock_mc_client.assert_called_once_with(
            session=mock_mc_session
        )

        # verify expected call to create MC DbtImporter
        mock_dbt_importer.assert_called_once_with(
            mc_client=mock_mc_client_instance
        )

        # verify expected call to import dbt run results to MC
        mock_dbt_importer_instance.import_run.assert_called_once_with(
            manifest_path="./target/manifest.json",
            run_results_path="./target/run_results.json",
            logs_path="./dbt.log",
            project_name="test-project",
            job_name="test-job",
            resource_id=None,
        )


    @patch("airflow_mcd.operators.dbt.subprocess")
    @patch("airflow_mcd.operators.dbt.open")
    @patch("airflow_mcd.operators.dbt.DbtImporter")
    @patch("airflow_mcd.operators.dbt.Client")
    @patch("airflow_mcd.operators.dbt.SessionHook")
    @patch.dict(os.environ, {}, clear=True)
    def test_operator_with_mc_disabled(
            self,
            mock_mc_session_hook: Mock,
            mock_mc_client: Mock,
            mock_dbt_importer: Mock,
            mock_open: Mock,
            mock_subprocess: Mock,
    ):
        # given
        mock_stdout = Mock()
        mock_stdout.readline.side_effect = [b"logging...\n"]
        mock_process = Mock()
        mock_process.returncode = 0
        mock_process.stdout = mock_stdout
        mock_subprocess.Popen.return_value = mock_process
        mock_subprocess.PIPE = subprocess.PIPE
        mock_subprocess.STDOUT = subprocess.STDOUT

        mock_log_file = Mock()
        mock_open.return_value = mock_log_file

        operator = DbtOperator(
            task_id="test-operator",
            command="run",
            project_name="test-project",
            job_name="test-job",
            mc_conn_id="mc-connection",
            mc_include_logs=True,
            mc_enabled=False,
        )

        # when
        operator.execute(Context())

        # verify expected call to submit dbt command
        mock_subprocess.Popen.assert_called_once_with(
            ["dbt", "run"],
            env={},
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=".",
            close_fds=True,
        )

        # verify expected call to open local log file
        mock_open.assert_called_once_with(
            "./dbt.log",
            "w",
        )

        # verify expected calls to write to local log file
        mock_log_file.write.assert_called_once_with("logging...\n")
        mock_log_file.close.assert_called_once_with()

        # verify expected call to wait for dbt command to complete
        mock_process.wait.assert_called_once_with()

        # verify no calls to MC APIs
        mock_mc_session_hook.assert_not_called()
        mock_mc_client.assert_not_called()
        mock_dbt_importer.assert_not_called()

    @patch("airflow_mcd.operators.dbt.subprocess")
    @patch("airflow_mcd.operators.dbt.open")
    @patch("airflow_mcd.operators.dbt.DbtImporter")
    @patch("airflow_mcd.operators.dbt.Client")
    @patch("airflow_mcd.operators.dbt.SessionHook")
    @patch.dict(os.environ, {}, clear=True)
    def test_operator_with_failed_import_and_mc_success_not_required(
            self,
            mock_mc_session_hook: Mock,
            mock_mc_client: Mock,
            mock_dbt_importer: Mock,
            mock_open: Mock,
            mock_subprocess: Mock,
    ):
        # given
        mock_stdout = Mock()
        mock_stdout.readline.side_effect = [b"logging...\n"]
        mock_process = Mock()
        mock_process.returncode = 0
        mock_process.stdout = mock_stdout
        mock_subprocess.Popen.return_value = mock_process
        mock_subprocess.PIPE = subprocess.PIPE
        mock_subprocess.STDOUT = subprocess.STDOUT

        mock_log_file = Mock()
        mock_open.return_value = mock_log_file

        mock_mc_session = Mock()
        mock_mc_session_hook_instance = Mock()
        mock_mc_session_hook_instance.get_conn.return_value = mock_mc_session
        mock_mc_session_hook.return_value = mock_mc_session_hook_instance

        mock_mc_client_instance = Mock()
        mock_mc_client.return_value = mock_mc_client_instance

        mock_dbt_importer_instance = Mock()
        mock_dbt_importer_instance.import_run.side_effect = Exception("uh oh")
        mock_dbt_importer.return_value = mock_dbt_importer_instance

        operator = DbtOperator(
            task_id="test-operator",
            command="run",
            project_name="test-project",
            job_name="test-job",
            mc_conn_id="mc-connection",
            mc_include_logs=True,
        )

        # when (no exception should be raised)
        operator.execute(Context())

        # verify expected call to submit dbt command
        mock_subprocess.Popen.assert_called_once_with(
            ["dbt", "run"],
            env={},
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=".",
            close_fds=True,
        )

        # verify expected call to open local log file
        mock_open.assert_called_once_with(
            "./dbt.log",
            "w",
        )

        # verify expected calls to write to local log file
        mock_log_file.write.assert_called_once_with("logging...\n")
        mock_log_file.close.assert_called_once_with()

        # verify expected call to wait for dbt command to complete
        mock_process.wait.assert_called_once_with()

        # verify expected call to create MC SessionHook
        mock_mc_session_hook.assert_called_once_with(
            mcd_session_conn_id="mc-connection"
        )

        # verify expected call to create MC API client
        mock_mc_client.assert_called_once_with(
            session=mock_mc_session
        )

        # verify expected call to create MC DbtImporter
        mock_dbt_importer.assert_called_once_with(
            mc_client=mock_mc_client_instance
        )

        # verify expected call to import dbt run results to MC
        mock_dbt_importer_instance.import_run.assert_called_once_with(
            manifest_path="./target/manifest.json",
            run_results_path="./target/run_results.json",
            logs_path="./dbt.log",
            project_name="test-project",
            job_name="test-job",
            resource_id=None,
        )

    @patch("airflow_mcd.operators.dbt.subprocess")
    @patch("airflow_mcd.operators.dbt.open")
    @patch("airflow_mcd.operators.dbt.DbtImporter")
    @patch("airflow_mcd.operators.dbt.Client")
    @patch("airflow_mcd.operators.dbt.SessionHook")
    @patch.dict(os.environ, {}, clear=True)
    def test_operator_with_failed_import_and_mc_success_required(
            self,
            mock_mc_session_hook: Mock,
            mock_mc_client: Mock,
            mock_dbt_importer: Mock,
            mock_open: Mock,
            mock_subprocess: Mock,
    ):
        # given
        mock_stdout = Mock()
        mock_stdout.readline.side_effect = [b"logging...\n"]
        mock_process = Mock()
        mock_process.returncode = 0
        mock_process.stdout = mock_stdout
        mock_subprocess.Popen.return_value = mock_process
        mock_subprocess.PIPE = subprocess.PIPE
        mock_subprocess.STDOUT = subprocess.STDOUT

        mock_log_file = Mock()
        mock_open.return_value = mock_log_file

        mock_mc_session = Mock()
        mock_mc_session_hook_instance = Mock()
        mock_mc_session_hook_instance.get_conn.return_value = mock_mc_session
        mock_mc_session_hook.return_value = mock_mc_session_hook_instance

        mock_mc_client_instance = Mock()
        mock_mc_client.return_value = mock_mc_client_instance

        mock_dbt_importer_instance = Mock()
        mock_dbt_importer_instance.import_run.side_effect = Exception("uh oh")
        mock_dbt_importer.return_value = mock_dbt_importer_instance

        operator = DbtOperator(
            task_id="test-operator",
            command="run",
            project_name="test-project",
            job_name="test-job",
            mc_conn_id="mc-connection",
            mc_success_required=True,
            mc_include_logs=True,
        )

        # when
        with self.assertRaises(Exception) as context:
            operator.execute(Context())

        # verify expected exception
        self.assertEqual("uh oh", str(context.exception))

        # verify expected call to submit dbt command
        mock_subprocess.Popen.assert_called_once_with(
            ["dbt", "run"],
            env={},
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=".",
            close_fds=True,
        )

        # verify expected call to open local log file
        mock_open.assert_called_once_with(
            "./dbt.log",
            "w",
        )

        # verify expected calls to write to local log file
        mock_log_file.write.assert_called_once_with("logging...\n")
        mock_log_file.close.assert_called_once_with()

        # verify expected call to wait for dbt command to complete
        mock_process.wait.assert_called_once_with()

        # verify expected call to create MC SessionHook
        mock_mc_session_hook.assert_called_once_with(
            mcd_session_conn_id="mc-connection"
        )

        # verify expected call to create MC API client
        mock_mc_client.assert_called_once_with(
            session=mock_mc_session
        )

        # verify expected call to create MC DbtImporter
        mock_dbt_importer.assert_called_once_with(
            mc_client=mock_mc_client_instance
        )

        # verify expected call to import dbt run results to MC
        mock_dbt_importer_instance.import_run.assert_called_once_with(
            manifest_path="./target/manifest.json",
            run_results_path="./target/run_results.json",
            logs_path="./dbt.log",
            project_name="test-project",
            job_name="test-job",
            resource_id=None,
        )
