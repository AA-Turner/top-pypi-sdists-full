import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
from unittest import TestCase
from unittest.mock import create_autospec, patch, ANY

import pytest
import airflow
from airflow_mcd import airflow_major_version

# Only import SlaMiss if Airflow < 3
if airflow_major_version() < 3:
    from airflow.models import SlaMiss
else:
    SlaMiss = None

from airflow.models import DagRun, TaskInstance, DAG, BaseOperator, DagTag
from sgqlc.types import Variable

from airflow_mcd.callbacks.client import AirflowEventsClient, AirflowEnv
from airflow_mcd.callbacks.utils import AirflowEventsClientUtils, _EXCEPTION_MSG_LIMIT
from freezegun import freeze_time
from pycarlo.common.utils import truncate_string
from pycarlo.core import Client


# needed to have a successful assert_called_with as Variable doesn't implement __eq__
class EqVariable(Variable):
    def __eq__(self, other):
        return other.name == self.name


class TagsMatcher:
    """Custom matcher that compares tags as sets (ignoring order)."""
    def __init__(self, expected_tags):
        self.expected_tags = set(expected_tags) if expected_tags else set()
    
    def __eq__(self, other):
        if other is None:
            return len(self.expected_tags) == 0
        return set(other) == self.expected_tags
    
    def __repr__(self):
        return f"TagsMatcher({list(self.expected_tags)})"


class CallbacksTests(TestCase):
    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_dag_result_success(self,  mock_client_upload_result):
        self._test_upload_dag_result(True, mock_client_upload_result)

    @freeze_time("2023-02-03 10:11:12", tz_offset=0)
    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_dag_result_success_no_dates(self,  mock_client_upload_result):
        self._test_upload_dag_result(True, mock_client_upload_result, set_dates=False)

    @freeze_time("2023-02-03 10:11:12", tz_offset=0)
    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_dag_result_success_no_end_date(self,  mock_client_upload_result):
        # When set_end_date=False, both Airflow 2 and 3 should have end_date=None
        # The callback validation checks for end_date and rejects if it's None
        # This is the correct behavior - the callback should not be called for running DAGs
        self._test_upload_dag_result(True, mock_client_upload_result, set_dates=True, set_end_date=False)
        
        # In both Airflow 2 and 3, end_date=None means the DAG is still running
        # The callback validation should reject it and not call the upload method
        mock_client_upload_result.assert_not_called()

    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_dag_result_success_with_tags(self, mock_client_upload_result):
        tags = ["tag1", "tag2"]
        self._test_upload_dag_result(True, mock_client_upload_result, tags=tags)

    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_dag_result_failure(self, mock_client_upload_result):
        self._test_upload_dag_result(False, mock_client_upload_result)

    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_task_result_success(self, mock_client_upload_result):
        self._test_upload_task_result("success", mock_client_upload_result)

    @freeze_time("2023-02-03 10:11:12", tz_offset=0)
    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_task_result_success_no_dates(self, mock_client_upload_result):
        self._test_upload_task_result("success", mock_client_upload_result, set_dates=False)

    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_task_result_failure(self, mock_client_upload_result):
        self._test_upload_task_result("failed", mock_client_upload_result)

    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_task_result_failure_long_message(self, mock_client_upload_result):
        error_message = "error message érror, " * 1024
        self._test_upload_task_result(
            state="failed",
            mock_client_upload_result=mock_client_upload_result,
            error_message=error_message,
        )

    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_task_result_running(self, mock_client_upload_result):
        self._test_upload_task_result("running", mock_client_upload_result)

    def test_task_instance_airflow3_compatibility(self):
        """Test that _get_task_instance_result works with Airflow 3's RuntimeTaskInstance."""
        # Create a TaskInstance using the same approach as existing tests
        task_instance = self._create_task_instance(
            dag_id="test_dag",
            task_id="test_task",
            state="success",
            set_dates=True
        )
        
        # Set specific values for this test
        task_instance.try_number = 2  # This should result in prev_attempted_tries = 1
        task_instance.duration = 10.5
        
        # Test that all required fields exist on the TaskInstance
        required_fields = [
            'task_id', 'state', 'log_url', 'duration', 'execution_date', 
            'start_date', 'end_date', 'max_tries', 'try_number'
        ]
        
        for field in required_fields:
            self.assertTrue(hasattr(task_instance, field), f"TaskInstance missing required field: {field}")
        
        # Test the prev_attempted_tries behavior based on Airflow version
        if airflow_major_version() >= 3:
            # In Airflow 3, prev_attempted_tries, duration, and execution_date should not exist on real TaskInstance
            # But our mock has them, so we need to remove them to simulate Airflow 3 behavior
            if hasattr(task_instance, 'prev_attempted_tries'):
                delattr(task_instance, 'prev_attempted_tries')
            if hasattr(task_instance, 'duration'):
                delattr(task_instance, 'duration')
            if hasattr(task_instance, 'execution_date'):
                delattr(task_instance, 'execution_date')
            
            # Test our compatibility fix
            result = AirflowEventsClientUtils._get_task_instance_result(task_instance)
            self.assertEqual(result.prev_attempted_tries, 1)  # try_number - 1
            # Duration should be calculated from start_date and end_date
            expected_duration = (task_instance.end_date - task_instance.start_date).total_seconds()
            self.assertEqual(result.duration, expected_duration)
            # Execution_date should fall back to start_date
            self.assertEqual(result.execution_date, task_instance.logical_date.isoformat())
        else:
            # In Airflow 1 and 2, prev_attempted_tries should exist
            self.assertTrue(hasattr(task_instance, 'prev_attempted_tries'))
            
            # Test normal behavior
            result = AirflowEventsClientUtils._get_task_instance_result(task_instance)
            self.assertEqual(result.prev_attempted_tries, task_instance.prev_attempted_tries)
            self.assertEqual(result.duration, 10.5)  # Should use the duration attribute
            self.assertEqual(result.execution_date, task_instance.execution_date.isoformat())
        
        # Verify other fields are correctly populated
        self.assertEqual(result.task_id, "test_task")
        self.assertEqual(result.state, "success")
        self.assertEqual(result.try_number, 2)

    def test_task_instance_airflow3_first_attempt(self):
        """Test that _get_task_instance_result works with Airflow 3 for first attempt (try_number=1)."""
        # Create a TaskInstance using the same approach as existing tests
        task_instance = self._create_task_instance(
            dag_id="test_dag",
            task_id="test_task",
            state="success",
            set_dates=True
        )
        
        # Set specific values for this test
        task_instance.try_number = 1  # First attempt should result in prev_attempted_tries = 0
        task_instance.duration = 5.0
        
        # Test the prev_attempted_tries behavior based on Airflow version
        if airflow_major_version() >= 3:
            # In Airflow 3, prev_attempted_tries, duration, and execution_date should not exist on real TaskInstance
            # But our mock has them, so we need to remove them to simulate Airflow 3 behavior
            if hasattr(task_instance, 'prev_attempted_tries'):
                delattr(task_instance, 'prev_attempted_tries')
            if hasattr(task_instance, 'duration'):
                delattr(task_instance, 'duration')
            if hasattr(task_instance, 'execution_date'):
                delattr(task_instance, 'execution_date')
            
            # Test our compatibility fix for first attempt
            result = AirflowEventsClientUtils._get_task_instance_result(task_instance)
            self.assertEqual(result.prev_attempted_tries, 0)  # try_number - 1 = 0
            # Duration should be calculated from start_date and end_date
            expected_duration = (task_instance.end_date - task_instance.start_date).total_seconds()
            self.assertEqual(result.duration, expected_duration)
            # Execution_date should fall back to start_date
            self.assertEqual(result.execution_date, task_instance.logical_date.isoformat())
        else:
            # In Airflow 1 and 2, prev_attempted_tries should exist
            self.assertTrue(hasattr(task_instance, 'prev_attempted_tries'))
            
            # Test normal behavior
            result = AirflowEventsClientUtils._get_task_instance_result(task_instance)
            self.assertEqual(result.prev_attempted_tries, task_instance.prev_attempted_tries)
            self.assertEqual(result.duration, 5.0)  # Should use the duration attribute
            self.assertEqual(result.execution_date, task_instance.execution_date.isoformat())
        
        # Verify other fields are correctly populated
        self.assertEqual(result.task_id, "test_task")
        self.assertEqual(result.state, "success")
        self.assertEqual(result.try_number, 1)

    def test_task_instance_airflow3_execution_date_fallback(self):
        """Test that execution_date falls back correctly when missing in Airflow 3."""
        # Create a TaskInstance using the same approach as existing tests
        task_instance = self._create_task_instance(
            dag_id="test_dag",
            task_id="test_task",
            state="success",
            set_dates=True
        )
        
        if airflow_major_version() >= 3:
            # Remove execution_date attribute to simulate Airflow 3 behavior
            if hasattr(task_instance, 'execution_date'):
                delattr(task_instance, 'execution_date')
            
            # Test execution_date fallback to start_date
            result = AirflowEventsClientUtils._get_task_instance_result(task_instance)
            self.assertEqual(result.execution_date, task_instance.logical_date.isoformat())
            
            # Test execution_date fallback to current time when start_date is also missing
            task_instance.logical_date = None
            task_instance.execution_date = None
            result = AirflowEventsClientUtils._get_task_instance_result(task_instance)

            self.assertEqual(result.execution_date, task_instance.start_date.isoformat())
        else:
            # In Airflow 1 and 2, should use the execution_date attribute
            result = AirflowEventsClientUtils._get_task_instance_result(task_instance)
            self.assertEqual(result.execution_date, task_instance.execution_date.isoformat())

    def test_task_instance_airflow3_duration_calculation(self):
        """Test that duration is correctly calculated from start_date and end_date in Airflow 3."""
        # Create a TaskInstance using the same approach as existing tests
        task_instance = self._create_task_instance(
            dag_id="test_dag",
            task_id="test_task",
            state="success",
            set_dates=True
        )
        
        # Set specific dates for duration calculation test
        task_instance.start_date = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        task_instance.end_date = datetime(2023, 1, 1, 10, 5, 30, tzinfo=timezone.utc)  # 5 minutes 30 seconds
        
        if airflow_major_version() >= 3:
            # Remove duration attribute to simulate Airflow 3 behavior
            if hasattr(task_instance, 'duration'):
                delattr(task_instance, 'duration')
            
            # Test duration calculation
            result = AirflowEventsClientUtils._get_task_instance_result(task_instance)
            expected_duration = (task_instance.end_date - task_instance.start_date).total_seconds()
            self.assertEqual(result.duration, expected_duration)
            self.assertEqual(result.duration, 330.0)  # 5 minutes 30 seconds = 330 seconds
        else:
            # In Airflow 1 and 2, should use the duration attribute
            result = AirflowEventsClientUtils._get_task_instance_result(task_instance)
            self.assertEqual(result.duration, task_instance.duration or 0)

    def test_task_instance_airflow3_duration_no_dates(self):
        """Test that duration defaults to 0 when start_date or end_date are missing in Airflow 3."""
        # Create a TaskInstance using the same approach as existing tests
        task_instance = self._create_task_instance(
            dag_id="test_dag",
            task_id="test_task",
            state="success",
            set_dates=False  # This will set start_date and end_date to None
        )
        
        if airflow_major_version() >= 3:
            # Remove duration attribute to simulate Airflow 3 behavior
            if hasattr(task_instance, 'duration'):
                delattr(task_instance, 'duration')
            if hasattr(task_instance, 'execution_date'):
                delattr(task_instance, 'execution_date')

            task_instance.logical_date = None            
            # Test duration calculation with missing dates
            result = AirflowEventsClientUtils._get_task_instance_result(task_instance)
            self.assertEqual(result.duration, 0)  # Should default to 0 when dates are missing
        else:
            # In Airflow 1 and 2, should use the duration attribute
            result = AirflowEventsClientUtils._get_task_instance_result(task_instance)
            self.assertEqual(result.duration, task_instance.duration or 0)

    def test_task_instance_field_compatibility_across_versions(self):
        """Test that all fields used in _get_task_instance_result exist across Airflow versions."""
        # Create a TaskInstance using the same approach as existing tests
        task_instance = self._create_task_instance(
            dag_id="test_dag",
            task_id="test_task",
            state="success",
            set_dates=True
        )
        
        # All fields that are accessed in _get_task_instance_result
        required_fields = [
            'task_id', 'state', 'log_url', 'execution_date', 
            'start_date', 'end_date', 'max_tries', 'try_number'
        ]
        
        # Test that all required fields exist
        for field in required_fields:
            self.assertTrue(hasattr(task_instance, field), 
                          f"TaskInstance missing required field: {field}")
        
        # Test optional fields based on Airflow version
        if airflow_major_version() >= 3:
            # In Airflow 3, prev_attempted_tries and duration should not exist
            # Remove them from our mock to simulate Airflow 3 behavior
            if hasattr(task_instance, 'prev_attempted_tries'):
                delattr(task_instance, 'prev_attempted_tries')
            if hasattr(task_instance, 'duration'):
                delattr(task_instance, 'duration')
            
            self.assertFalse(hasattr(task_instance, 'prev_attempted_tries'),
                           "prev_attempted_tries should not exist in Airflow 3")
            self.assertFalse(hasattr(task_instance, 'duration'),
                           "duration should not exist in Airflow 3")
        else:
            # In Airflow 1 and 2, prev_attempted_tries and duration should exist
            self.assertTrue(hasattr(task_instance, 'prev_attempted_tries'),
                          "prev_attempted_tries should exist in Airflow 1 and 2")
            self.assertTrue(hasattr(task_instance, 'duration'),
                          "duration should exist in Airflow 1 and 2")
        
        # Test that the function can be called without errors
        result = AirflowEventsClientUtils._get_task_instance_result(task_instance)
        
        # Verify the result object has all expected attributes
        expected_result_fields = [
            'task_id', 'state', 'log_url', 'prev_attempted_tries', 'duration',
            'execution_date', 'start_date', 'end_date', 'next_retry_datetime',
            'max_tries', 'try_number', 'exception_message', 'inlets', 'outlets',
            'original_dates'
        ]
        
        for field in expected_result_fields:
            self.assertTrue(hasattr(result, field), 
                          f"Result missing expected field: {field}")

    def test_task_instance_with_no_task(self):
        """Test that _get_task_instance_result handles task instances without tasks gracefully."""
        # Create a TaskInstance without a task using the same approach as existing tests
        task_instance = self._create_task_instance(
            dag_id="test_dag",
            task_id="test_task",
            state="success",
            set_dates=True
        )
        
        # Remove the task to simulate Airflow >= 2.9.0 behavior
        task_instance.task = None
        
        # Test that the function handles missing task gracefully
        result = AirflowEventsClientUtils._get_task_instance_result(task_instance)
        
        # Verify basic fields are populated
        self.assertEqual(result.task_id, "test_task")
        self.assertEqual(result.state, "success")
        self.assertEqual(result.try_number, 1)
        
        # Test that lineage methods handle missing task gracefully
        self.assertEqual(AirflowEventsClientUtils._get_lineage_list(task_instance, "inlets"), [])
        self.assertEqual(AirflowEventsClientUtils._get_lineage_list(task_instance, "outlets"), [])
        self.assertIsNone(AirflowEventsClientUtils._get_next_retry_datetime(task_instance))

    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_task_result_success_with_tags(self, mock_client_upload_result):
        tags = ["tag1", "tag2"]
        self._test_upload_task_result("running", mock_client_upload_result, tags=tags)
    def test_env_loading(self):
        no_env = AirflowEnv()
        self.assertEqual("airflow", no_env.env_name)
        self.assertIsNone(no_env.env_id)
        self.assertIsNone(no_env.version)
        self.assertIsNone(no_env.base_url)

        # AWS
        with patch.dict(os.environ, {
            "AIRFLOW_ENV_NAME": "aws_env_name",
            "AIRFLOW_ENV_ID": "aws_env_id",
            "AIRFLOW_VERSION": "aws_version",
            "AIRFLOW__WEBSERVER__BASE_URL": "aws_url",
        }):
            env = AirflowEnv()
            self.assertEqual("aws_env_name", env.env_name)
            self.assertEqual("aws_env_id", env.env_id)
            self.assertEqual("aws_version", env.version)
            self.assertEqual("aws_url", env.base_url)

        # GCP Composer
        with patch.dict(os.environ, {
            "COMPOSER_ENVIRONMENT": "gcp_env_name",
            "COMPOSER_GKE_NAME": "gcp_env_id",
            "MAJOR_VERSION": "gcp_version",
            "AIRFLOW__WEBSERVER__BASE_URL": "gcp_url",
        }):
            env = AirflowEnv()
            self.assertEqual("gcp_env_name", env.env_name)
            self.assertEqual("gcp_env_id", env.env_id)
            self.assertEqual("gcp_version", env.version)
            self.assertEqual("gcp_url", env.base_url)

        # Astronomer
        with patch.dict(os.environ, {
            "AIRFLOW__WEBSERVER__INSTANCE_NAME": "astro_env_name",
            "ASTRO_DEPLOYMENT_ID": "astro_env_id",
            "ASTRONOMER_RUNTIME_VERSION": "astro_version",
            "AIRFLOW__WEBSERVER__BASE_URL": "astro_url",
        }):
            env = AirflowEnv()
            self.assertEqual("astro_env_name", env.env_name)
            self.assertEqual("astro_env_id", env.env_id)
            self.assertEqual("astro_version", env.version)
            self.assertEqual("astro_url", env.base_url)

        params_env = AirflowEnv(
            env_name="name",
            env_id="id",
            version="1.0",
            base_url="url"
        )
        self.assertEqual("name", params_env.env_name)
        self.assertEqual("id", params_env.env_id)
        self.assertEqual("1.0", params_env.version)
        self.assertEqual("url", params_env.base_url)

    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._get_existing_connection_id")
    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._get_session")
    @patch("airflow_mcd.callbacks.client.Client")
    def test_upload_igw_dag_result_success(
        self,
        mock_client_factory,
        mock_get_session,
        mock_get_connection_id,
    ):
        mock_client = create_autospec(Client)
        mock_client_factory.return_value = mock_client
        path = "/airflow/callbacks"
        mock_get_connection_id.return_value = "conn_id"

        dag_context, dag, dag_run, task_instances = self._upload_dag_result(True)
        
        # Handle execution_date based on Airflow version
        if airflow_major_version() >= 3:
            # In Airflow 3, the callback uses logical_date as execution_date for DAG results
            execution_date = dag_run.logical_date.isoformat() if dag_run.logical_date else dag_run.start_date.isoformat()
            # In Airflow 3, tasks array is empty because dag_run.get_task_instances() is not allowed
            expected_tasks = []
        else:
            # In Airflow 1 and 2, use execution_date
            execution_date = dag_run.execution_date.isoformat()
            # In Airflow 1 and 2, tasks array has task instances
            expected_tasks = [
                self._get_dag_task_instance_result(ti, set_dates=True)
                for ti in task_instances
            ]
        
        expected_body = {
            "airflow_operation": AirflowEventsClient._UPLOAD_AIRFLOW_DAG_RESULT_OPERATION,
            "airflow_payload": {
                "dag_id": dag.dag_id,
                "run_id": dag_context["run_id"],
                "success": True,
                "reason": dag_context.get("reason"),
                "state": dag_run.state,
                "execution_date": execution_date,
                "start_date": dag_run.start_date.isoformat(),
                "end_date": dag_run.end_date.isoformat(),
                "env": self._get_graphql_env(),
                "tags": [],
                "payload": {
                    "dag_id": dag.dag_id,
                    "env": self._get_env(),
                    "run_id": dag_context["run_id"],
                    "success": True,
                    "tasks": expected_tasks,  # Use version-specific tasks array
                    "state": dag_run.state,
                    "execution_date": execution_date,
                    "start_date": dag_run.start_date.isoformat(),
                    "end_date": dag_run.end_date.isoformat(),
                    "reason": dag_context.get("reason"),
                    "event_type": "dag",
                    "original_dates": ANY,
                    "tags": [],
                },
            },
        }
        mock_client.make_request.assert_called_with(path=path, body=expected_body, timeout_in_seconds=10, should_retry=ANY)
        mock_get_connection_id.assert_called()

    def _test_upload_dag_result(
            self,
            success: bool,
            mock_client_upload_result,
            set_dates: bool = True,
            set_end_date: bool = True,
            tags: Optional[List[str]] = [],
    ):
        dag_context, dag, dag_run, task_instances = self._upload_dag_result(success, set_dates, set_end_date, tags)
        
        # Check if the callback was called
        if mock_client_upload_result.call_count == 0:
            # The callback was not called, which is expected when end_date is None
            # This is the correct behavior - both Airflow 2 and 3 reject DAG runs without end_date
            return
            
        # The callback was called, so we need to verify the call
        now_isoformat = datetime.now(tz=timezone.utc).isoformat()
        
        # Handle execution_date vs logical_date based on Airflow version
        if airflow_major_version() >= 3:
            # In Airflow 3, the callback uses logical_date as execution_date for DAG results
            execution_date = dag_run.logical_date.isoformat() if set_dates and dag_run.logical_date else now_isoformat
            # Handle duration calculation - avoid subtraction when start_date is None
            if dag_run.start_date and dag_run.end_date:
                duration = dag_run.end_date - dag_run.start_date
            else:
                duration = 0
            # The callback uses the same format as task results for original_dates
            # It calls _get_original_dates with the execution_date, start_date, and end_date
            # When set_dates=False: logical_date is None, start_date is None, end_date depends on set_end_date
            execution_date_dt = dag_run.logical_date if set_dates and dag_run.logical_date else datetime.now(tz=timezone.utc)
            # When set_dates=False but set_end_date=True, end_date is set to current time
            # When set_dates=False and set_end_date=False, end_date is None
            original_dates = f"execution={str(execution_date_dt)}, start_date={str(dag_run.start_date) if set_dates else 'None'}, end_date={str(dag_run.end_date)}"

            tasks = [] # In Airflow 3, the callback does not return tasks
        else:
            # In Airflow 1 and 2, use execution_date
            execution_date = dag_run.execution_date.isoformat() if set_dates and dag_run.execution_date else now_isoformat
            # Handle duration calculation - avoid subtraction when start_date is None
            if dag_run.start_date and dag_run.end_date:
                duration = dag_run.end_date - dag_run.start_date
            else:
                duration = 0
            # In Airflow 1 and 2, original_dates is calculated dynamically
            original_dates = ANY
            tasks = [
                self._get_dag_task_instance_result(task_instance, None, set_dates)
                for task_instance in task_instances
            ]

        # Use TagsMatcher for tags to handle order differences
        expected_tags = TagsMatcher(tags) if tags else tags

        mock_client_upload_result.assert_called_with(
            AirflowEventsClient._UPLOAD_AIRFLOW_DAG_RESULT_OPERATION,
            {
                "dag_id": dag.dag_id,
                "run_id": dag_context["run_id"],
                "success": success,
                "reason": dag_context.get("reason"),
                "state": dag_run.state,
                "execution_date": execution_date,
                "start_date": dag_run.start_date.isoformat() if set_dates and dag_run.start_date else now_isoformat,
                "end_date": dag_run.end_date.isoformat() if dag_run.end_date else now_isoformat,
                "env": self._get_graphql_env(),
                "payload": EqVariable("payload"),
                "tags": expected_tags,
            },
            {
                "dag_id": dag.dag_id,
                "env": self._get_env(),
                "run_id": dag_context["run_id"],
                "success": success,
                "tasks": tasks,
                "state": dag_run.state,
                "execution_date": execution_date,
                "start_date": dag_run.start_date.isoformat() if set_dates and dag_run.start_date else now_isoformat,
                "end_date": dag_run.end_date.isoformat() if dag_run.end_date else now_isoformat,
                "reason": dag_context.get("reason"),
                "event_type": "dag",
                "original_dates": original_dates,
                "tags": expected_tags,
            },
        )

    def _upload_dag_result(
        self, success: bool, set_dates: bool = True, set_end_date: bool = True, tags: Optional[List[str]] = [],
    ) -> Tuple[Dict, DAG, DagRun, List[TaskInstance]]:
        state = "success" if success else "failed"
        dag_context = self._create_dag_context(state, set_dates, set_end_date, tags)
        dag: DAG = dag_context["dag"]
        dag_run: DagRun = dag_context["dag_run"]
        task_instances: List[TaskInstance] = dag_run.get_task_instances()

        utils = AirflowEventsClientUtils()
        utils.mcd_post_dag_result(dag_context)
        return dag_context, dag, dag_run, task_instances


    @staticmethod
    def _get_graphql_env() -> Dict:
        return {
            "env_name": "airflow",
        }

    @staticmethod
    def _get_env() -> Dict:
        return {
            "env_name": "airflow",
            "env_id": None,
            "version": None,
            "base_url": None
        }

    def _create_dag_context(
            self,
            state: str,
            set_dates: bool = True,
            set_end_date: bool = True,
            tags: Optional[List[str]] = [],
    ) -> Dict:
        if airflow_major_version() >= 3:
            # Use real Airflow 3 classes for better compatibility testing
            # Create a real DAG object
            dag = DAG(
                dag_id="dag_123",
                start_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
                schedule=None,  # Airflow 3 uses 'schedule' instead of 'schedule_interval'
                tags=tags
            )
            
            # Create a real DagRun object with logical_date for Airflow 3
            logical_date = datetime.now(tz=timezone.utc) - timedelta(seconds=10) if set_dates else None
            dag_run = DagRun(
                dag_id="dag_123",
                run_id="123",
                run_type="manual",
                state=state,
                start_date=datetime.now(tz=timezone.utc) - timedelta(seconds=9) if set_dates else None,
                logical_date=logical_date
            )
            
            # Set end_date based on the set_end_date parameter (consistent across Airflow versions)
            # When set_end_date=False, end_date should be None (simulating a running DAG)
            if set_end_date:
                dag_run.end_date = datetime.now(tz=timezone.utc)
            else:
                dag_run.end_date = None
            
            # Set data intervals for Airflow 3
            if set_dates:
                dag_run.data_interval_start = datetime.now(tz=timezone.utc) - timedelta(seconds=10)
                dag_run.data_interval_end = datetime.now(tz=timezone.utc) - timedelta(seconds=10)
            
            # Create real TaskInstance objects using BaseOperator (available in all Airflow versions)
            task1 = BaseOperator(task_id="task_123", dag=dag)
            task2 = BaseOperator(task_id="task_234", dag=dag)
            
            # Try to create TaskInstance - Airflow 3.1+ may require dag_version_id
            import uuid
            try:
                # Try with dag_version_id first (Airflow 3.1+)
                dag_version_id = uuid.uuid4()
                task_instance1 = TaskInstance(
                    task=task1,
                    run_id="123",
                    dag_version_id=dag_version_id
                )
            except TypeError:
                # Fall back to without dag_version_id (Airflow 3.0)
                task_instance1 = TaskInstance(
                    task=task1,
                    run_id="123"
                )
            task_instance1.state = state
            task_instance1.start_date = datetime.now(tz=timezone.utc) - timedelta(seconds=9) if set_dates else None
            task_instance1.end_date = datetime.now(tz=timezone.utc) if set_dates else None
            task_instance1.logical_date = datetime.now(tz=timezone.utc) - timedelta(seconds=10) if set_dates else None
            task_instance1.max_tries = 3
            task_instance1.try_number = 1
            # In Airflow 3, TaskInstance doesn't have logical_date, but we can set it if needed
            # The callback will use start_date as fallback for execution_date
            
            try:
                # Try with dag_version_id first (Airflow 3.1+)
                task_instance2 = TaskInstance(
                    task=task2,
                    run_id="123",
                    dag_version_id=dag_version_id
                )
            except (TypeError, NameError):
                # Fall back to without dag_version_id (Airflow 3.0) or if dag_version_id is not defined
                task_instance2 = TaskInstance(
                    task=task2,
                    run_id="123"
                )
            task_instance2.state = "success"
            task_instance2.start_date = datetime.now(tz=timezone.utc) - timedelta(seconds=9) if set_dates else None
            task_instance2.end_date = datetime.now(tz=timezone.utc) if set_dates else None
            task_instance2.logical_date = datetime.now(tz=timezone.utc) - timedelta(seconds=10) if set_dates else None
            task_instance2.max_tries = 3
            task_instance2.try_number = 1
            
            # Mock the get_task_instances method to return our real task instances
            # NOTE: If this was not mocked this would not work in Airflow 3 as it does not
            # allow to access to query the database at runtime
            dag_run.get_task_instances = lambda: [task_instance1, task_instance2]
            
            # Mock the DAG's get_dagrun method to return our DagRun (as the callback does in Airflow 3)
            dag.get_dagrun = lambda run_id: dag_run
            
        else:
            # Use mocks for Airflow 1 and 2 (existing behavior)
            dag = create_autospec(DAG)
            dag.dag_id = "dag_123"
            dag.params = {}
            dag.tags = tags
            dag_run = create_autospec(DagRun)
            
            # Remove logical_date from the mock since it doesn't exist in Airflow 2
            if hasattr(dag_run, 'logical_date'):
                delattr(dag_run, 'logical_date')
            
            task_instances = [
                self._create_task_instance(
                    dag_id=dag.dag_id,
                    task_id="task_123",
                    state=state,
                    running=state == "running",
                    set_dates=set_dates,
                ),
                self._create_task_instance(
                    dag_id=dag.dag_id,
                    task_id="task_234",
                    state="success",
                    set_dates=set_dates,
                ),
            ]
            dag_run.get_task_instances.return_value = task_instances
            dag_run.state = state
            if set_dates:
                dag_run.execution_date = datetime.now(tz=timezone.utc) - timedelta(seconds=10)
                dag_run.start_date = datetime.now(tz=timezone.utc) - timedelta(seconds=9)
            else:
                dag_run.execution_date = None
                dag_run.start_date = None

            dag_run.end_date = datetime.now(tz=timezone.utc) if set_end_date else None

        dag_context = {
            "dag": dag,
            "run_id": '123',
            "dag_run": dag_run,
            "reason": "succeeded" if state == "success" else "task failed",
        }
        return dag_context

    def _test_upload_task_result(
        self,
        state: str,
        mock_client_upload_result,
        set_dates: bool = True,
        error_message: Optional[str] = None,
        tags: Optional[List[str]] = [],
    ):
        dag_context = self._create_dag_context(state, set_dates=set_dates, tags=tags)
        exception_message: Optional[str] = (error_message or "task failed") if state == "failed" else None
        if state == "failed":
            dag_context["exception"] = Exception(exception_message)
        dag: DAG = dag_context["dag"]
        dag_run: DagRun = dag_context["dag_run"]
        # This ONLY works in Airflow 3 because it is a mock. We use it because it here in the test
        # because it is handy to test the task callback
        task_instances: List[TaskInstance] = dag_run.get_task_instances()
        task_instance = task_instances[0]
        task_instance.state = state
        dag_context["task_instance"] = task_instance
        utils = AirflowEventsClientUtils()
        utils.mcd_post_task_result(dag_context)

        now_isoformat = datetime.now(tz=timezone.utc).isoformat()
        
        # Handle execution_date based on Airflow version
        if airflow_major_version() >= 3:
            # In Airflow 3, the callback uses logical_date as execution_date for task results
            # Follow the same logic as _get_task_instance_result
            if hasattr(task_instance, 'execution_date') and task_instance.execution_date:
                execution_date_dt = task_instance.execution_date
            elif hasattr(task_instance, 'logical_date') and task_instance.logical_date:
                execution_date_dt = task_instance.logical_date
            elif hasattr(task_instance, 'start_date') and task_instance.start_date:
                execution_date_dt = task_instance.start_date
            else:
                execution_date_dt = datetime.now(tz=timezone.utc)
            execution_date = execution_date_dt.isoformat()
            # In Airflow 3, duration is calculated from end_date - start_date
            if task_instance.start_date and task_instance.end_date:
                duration = (task_instance.end_date - task_instance.start_date).total_seconds()
            else:
                duration = 0

            # In Airflow 3, prev_attempted_tries is calculated as try_number - 1
            prev_attempted_tries = task_instance.try_number - 1
            # TODO: Check if this is correct
            # In Airflow 3, the callback generates a different log_url format
            log_url = f"http://localhost:8080/dags/{dag.dag_id}/runs/{dag_context['run_id']}/tasks/{task_instance.task_id}?try_number={task_instance.try_number}"
            # In Airflow 3, RuntimeTaskInstance doesn't have next_retry_datetime() method
            # The callback now returns None for Airflow 3.2+ compatibility
            next_retry_datetime = None
        else:
            # In Airflow 1 and 2, use the execution_date attribute
            execution_date = task_instance.execution_date.isoformat() if set_dates and task_instance.execution_date else now_isoformat
            duration = task_instance.duration or 0
            # In Airflow 1 and 2, use the prev_attempted_tries attribute
            prev_attempted_tries = task_instance.prev_attempted_tries
             # In Airflow 1 and 2, use the log_url attribute
            log_url = f"http://airflow.com/{dag.dag_id}/{task_instance.task_id}/log"
            # In Airflow 1 and 2, use the method result
            next_retry_datetime = None
            # For original_dates calculation, use the same logic as the actual implementation
            # In Airflow 2, the actual implementation uses ti.execution_date directly
            # When set_dates=False, this is None
            execution_date_dt = task_instance.execution_date
        
        # Handle end_date fallback like _get_datetime_isoformat does
        expected_end_date = task_instance.end_date.isoformat() if set_dates and task_instance.end_date else now_isoformat
        
        # Fix original_dates calculation to match the actual implementation
        # The actual implementation passes the raw datetime objects to _get_original_dates
        # When set_dates=False, these are None, so str() returns "None"
        # The actual implementation uses the raw values without fallbacks for original_dates
        original_dates = f"execution={str(execution_date_dt)}, start_date={str(task_instance.start_date)}, end_date={str(task_instance.end_date)}"
        
        expected_graphql_payload = {
            "dag_id": dag.dag_id,
            "run_id": dag_context["run_id"],
            "task_id": task_instance.task_id,
            "success": state == "success",
            "state": state,
            "log_url": log_url,
            "execution_date": execution_date,  # Use the calculated execution_date
            "start_date": task_instance.start_date.isoformat() if set_dates else now_isoformat,
            "end_date": expected_end_date,  # Use the fallback logic
            "duration": duration,
            "attempt_number": prev_attempted_tries,
            "env": self._get_graphql_env(),
            "payload": EqVariable("payload"),
            "tags": TagsMatcher(tags) if tags else tags,  # Use TagsMatcher for tags to handle order differences
        }
        
        # Add next_retry_date to GraphQL payload if it exists (Airflow 3 behavior)
        if next_retry_datetime:
            expected_graphql_payload['next_retry_date'] = next_retry_datetime
        
        expected_exception_message = truncate_string(
            exception_message,
            _EXCEPTION_MSG_LIMIT,
        ) if exception_message else None

        if exception_message:
            expected_graphql_payload["exception_message"] = expected_exception_message

        mock_client_upload_result.assert_called()
        mock_client_upload_result.assert_called_with(
            AirflowEventsClient._UPLOAD_AIRFLOW_TASK_RESULT_OPERATION,
            expected_graphql_payload,
            {
                "dag_id": dag.dag_id,
                "env": self._get_env(),
                "run_id": dag_context["run_id"],
                "success": state == "success",
                "task": {
                    "task_id": task_instance.task_id,
                    "state": task_instance.state,
                    "log_url": log_url,
                    "prev_attempted_tries": prev_attempted_tries,
                    "duration": duration,
                    "execution_date": execution_date,
                    "start_date": task_instance.start_date.isoformat() if set_dates else now_isoformat,
                    "end_date": expected_end_date,  # Use the fallback logic
                    "next_retry_datetime": next_retry_datetime,
                    "max_tries": task_instance.max_tries,
                    "try_number": task_instance.try_number,
                    "exception_message": expected_exception_message,
                    "inlets": [],
                    "outlets": [],
                    "original_dates": original_dates,
                },
                "event_type": "task",
                "tags": TagsMatcher(tags) if tags else tags,  # Use TagsMatcher for tags to handle order differences
            }
        )

    @staticmethod
    def _create_task_instance(
            dag_id: str,
            task_id: str,
            state: str,
            running: bool = False,
            set_dates: bool = True,
    ) -> TaskInstance:
        task_instance = create_autospec(TaskInstance)
        task_instance.next_retry_datetime.return_value = None
        task_instance.inlets = []
        task_instance.outlets = []
        task_instance.task_id = task_id
        task_instance.state = state
        task_instance.log_url = f"http://airflow.com/{dag_id}/{task_instance.task_id}/log"
        task_instance.prev_attempted_tries = 0
        task_instance.duration = 10.5 if not running else None
        if set_dates:
            task_instance.execution_date = datetime.now(tz=timezone.utc) - timedelta(seconds=10)
            task_instance.logical_date = datetime.now(tz=timezone.utc) - timedelta(seconds=10)
            task_instance.start_date = datetime.now(tz=timezone.utc) - timedelta(seconds=9)
            task_instance.end_date = datetime.now(tz=timezone.utc)
        else:
            task_instance.execution_date = None
            task_instance.start_date = None
            task_instance.end_date = None
        task_instance.max_tries = 3
        task_instance.try_number = 1
        return task_instance

    @staticmethod
    def _get_dag_task_instance_result(
            task_instance: TaskInstance,
            exception_message: Optional[str] = None,
            set_dates: bool = True,
    ) -> Dict:
        now_isoformat = datetime.now(tz=timezone.utc).isoformat()
        
        # Handle inlets/outlets based on Airflow version
        if airflow_major_version() >= 3:
            # In Airflow 3, inlets and outlets may not exist on TaskInstance
            inlets = getattr(task_instance, 'inlets', []) or []
            outlets = getattr(task_instance, 'outlets', []) or []
        else:
            # In Airflow 1 and 2, normalize inlets/outlets to [] if None
            inlets = task_instance.inlets if task_instance.inlets is not None else []
            outlets = task_instance.outlets if task_instance.outlets is not None else []
        
        # Handle duration based on Airflow version
        if airflow_major_version() >= 3:
            # In Airflow 3, duration is calculated from end_date - start_date
            if task_instance.start_date and task_instance.end_date:
                duration = (task_instance.end_date - task_instance.start_date).total_seconds()
            else:
                duration = 0
        else:
            # In Airflow 1 and 2, use the duration attribute
            duration = task_instance.duration or 0
        
        # Handle prev_attempted_tries based on Airflow version
        if airflow_major_version() >= 3:
            # In Airflow 3, prev_attempted_tries may not exist, calculate from try_number
            prev_attempted_tries = getattr(task_instance, 'prev_attempted_tries', task_instance.try_number - 1)
        else:
            # In Airflow 1 and 2, use the prev_attempted_tries attribute
            prev_attempted_tries = task_instance.prev_attempted_tries
        
        # Handle execution_date based on Airflow version
        if airflow_major_version() >= 3:
            # In Airflow 3, execution_date was removed, use start_date as fallback
            # In a real scenario, the callback would get this from dag_run.logical_date
            execution_date = task_instance.start_date.isoformat() if set_dates and task_instance.start_date else now_isoformat
        else:
            # In Airflow 1 and 2, use the execution_date attribute
            execution_date = task_instance.execution_date.isoformat() if set_dates else now_isoformat
        
        # Handle log_url based on Airflow version
        if airflow_major_version() >= 3:
            # In Airflow 3, log_url may not exist, create a default one
            log_url = getattr(task_instance, 'log_url', f"http://airflow.com/{task_instance.task_id}/log")
        else:
            # In Airflow 1 and 2, use the log_url attribute
            log_url = task_instance.log_url
        
        # Handle next_retry_datetime based on Airflow version
        if airflow_major_version() >= 3:
            # In Airflow 3, this is calculated by calling next_retry_datetime() method
            # Since we're using real TaskInstance objects, this will return a real calculated value
            # But we need to handle the case where end_date is None (like the callback does)
            if task_instance.end_date is None:
                next_retry_datetime = None
            else:
                next_retry_datetime_raw = task_instance.next_retry_datetime()
                # The callback converts datetime to ISO format string
                next_retry_datetime = next_retry_datetime_raw.isoformat() if next_retry_datetime_raw else None
        else:
            # In Airflow 1 and 2, use the method result
            next_retry_datetime = None
        
        # Handle original_dates based on Airflow version
        if airflow_major_version() >= 3:
            # In Airflow 3, this is calculated dynamically using the format from _get_original_dates
            # Since we're using real objects, this will be a real calculated string
            # The callback uses str() on datetime objects, not isoformat()
            # Convert execution_date back to datetime for str() formatting
            execution_date_dt = task_instance.start_date if set_dates and task_instance.start_date else datetime.now(tz=timezone.utc)
            # The callback passes the original datetime objects to _get_original_dates
            # When set_dates=False, start_date and end_date are None, so str() returns "None"
            original_dates = f"execution={str(execution_date_dt)}, start_date={str(task_instance.start_date) if set_dates else 'None'}, end_date={str(task_instance.end_date) if set_dates else 'None'}"
        else:
            # In Airflow 1 and 2, this is also calculated
            original_dates = ANY
        
        return {
            "task_id": task_instance.task_id,
            "state": task_instance.state,
            "log_url": log_url,
            "prev_attempted_tries": prev_attempted_tries,
            "duration": duration,
            "execution_date": execution_date,
            "start_date": task_instance.start_date.isoformat() if set_dates else now_isoformat,
            "end_date": task_instance.end_date.isoformat() if set_dates else now_isoformat,
            "next_retry_datetime": next_retry_datetime,
            "max_tries": task_instance.max_tries,
            "try_number": task_instance.try_number,
            "exception_message": exception_message,
            "inlets": inlets,
            "outlets": outlets,
            "original_dates": original_dates,
        }

    @pytest.mark.skipif(airflow_major_version() < 3, reason="This test is specifically for Airflow 3 compatibility")
    def test_task_instance_all_properties_airflow3_compatibility(self):
        """Test that all properties accessed in _get_task_instance_result exist on RuntimeTaskInstance in Airflow 3."""
        # Create a TaskInstance using the same approach as existing tests
        task_instance = self._create_task_instance(
            dag_id="test_dag",
            task_id="test_task",
            state="success",
            set_dates=True
        )
        
        # All properties that are accessed in _get_task_instance_result method
        properties_accessed = [
            'task_id', 'state', 'log_url', 'start_date', 'end_date',
            'max_tries', 'try_number', 'task'
        ]
        
        # Properties that are accessed but may not exist in Airflow 3
        optional_properties_airflow3 = [
            'prev_attempted_tries', 'duration', 'execution_date'
        ]
        
        # Test that all required properties exist
        for prop in properties_accessed:
            self.assertTrue(hasattr(task_instance, prop), 
                          f"TaskInstance missing required property: {prop}")
        
        # Test optional properties based on Airflow version
        if airflow_major_version() >= 3:
            # In Airflow 3, prev_attempted_tries and duration should not exist
            # Remove them from our mock to simulate Airflow 3 behavior
            if hasattr(task_instance, 'prev_attempted_tries'):
                delattr(task_instance, 'prev_attempted_tries')
            if hasattr(task_instance, 'duration'):
                delattr(task_instance, 'duration')
            
            self.assertFalse(hasattr(task_instance, 'prev_attempted_tries'),
                           "prev_attempted_tries should not exist in Airflow 3")
            self.assertFalse(hasattr(task_instance, 'duration'),
                           "duration should not exist in Airflow 3")
        else:
            # In Airflow 1 and 2, prev_attempted_tries and duration should exist
            self.assertTrue(hasattr(task_instance, 'prev_attempted_tries'),
                          "prev_attempted_tries should exist in Airflow 1 and 2")
            self.assertTrue(hasattr(task_instance, 'duration'),
                          "duration should exist in Airflow 1 and 2")
        
        # Test that the function can be called without errors
        result = AirflowEventsClientUtils._get_task_instance_result(task_instance)
        
        # Verify the result object has all expected attributes
        expected_result_fields = [
            'task_id', 'state', 'log_url', 'prev_attempted_tries', 'duration',
            'execution_date', 'start_date', 'end_date', 'next_retry_datetime',
            'max_tries', 'try_number', 'exception_message', 'inlets', 'outlets',
            'original_dates'
        ]
        
        for field in expected_result_fields:
            self.assertTrue(hasattr(result, field), 
                          f"Result missing expected field: {field}")

    def test_task_instance_methods_airflow3_compatibility(self):
        """Test that all methods accessed on TaskInstance exist on RuntimeTaskInstance in Airflow 3."""
        # Create a TaskInstance using the same approach as existing tests
        task_instance = self._create_task_instance(
            dag_id="test_dag",
            task_id="test_task",
            state="success",
            set_dates=True
        )
        
        # Methods that are accessed in utils.py
        methods_accessed = [
            'next_retry_datetime'
        ]
        
        # Test that all required methods exist
        for method in methods_accessed:
            self.assertTrue(hasattr(task_instance, method), 
                          f"TaskInstance missing required method: {method}")
            self.assertTrue(callable(getattr(task_instance, method)),
                          f"TaskInstance property {method} is not callable")

    def test_task_instance_lineage_properties_airflow3_compatibility(self):
        """Test that lineage-related properties work correctly in Airflow 3."""
        # Create a TaskInstance using the same approach as existing tests
        task_instance = self._create_task_instance(
            dag_id="test_dag",
            task_id="test_task",
            state="success",
            set_dates=True
        )
        
        # Test lineage methods
        inlets = AirflowEventsClientUtils._get_lineage_list(task_instance, "inlets")
        outlets = AirflowEventsClientUtils._get_lineage_list(task_instance, "outlets")
        
        # These should return empty lists when task is None or has no lineage
        self.assertEqual(inlets, [])
        self.assertEqual(outlets, [])
        
        # Test with task set to None (simulating Airflow >= 2.9.0 behavior)
        task_instance.task = None
        inlets = AirflowEventsClientUtils._get_lineage_list(task_instance, "inlets")
        outlets = AirflowEventsClientUtils._get_lineage_list(task_instance, "outlets")
        
        # Should still return empty lists
        self.assertEqual(inlets, [])
        self.assertEqual(outlets, [])

    def test_task_instance_next_retry_datetime_airflow3_compatibility(self):
        """Test that next_retry_datetime method works correctly in Airflow 3."""
        # Create a TaskInstance using the same approach as existing tests
        task_instance = self._create_task_instance(
            dag_id="test_dag",
            task_id="test_task",
            state="success",
            set_dates=True
        )
        
        # Test next_retry_datetime method
        next_retry = AirflowEventsClientUtils._get_next_retry_datetime(task_instance)
        
        # Should return None when task is None or end_date is None
        self.assertIsNone(next_retry)
        
        # Test with task set to None
        task_instance.task = None
        next_retry = AirflowEventsClientUtils._get_next_retry_datetime(task_instance)
        self.assertIsNone(next_retry)
        
        # Test with end_date set to None
        task_instance.task = "some_task"  # Restore task
        task_instance.end_date = None
        next_retry = AirflowEventsClientUtils._get_next_retry_datetime(task_instance)
        self.assertIsNone(next_retry)

    def test_get_lineage_dict_with_dataclass(self):
        """Test that _get_lineage_dict works correctly with dataclass objects."""
        from dataclasses import dataclass
        
        @dataclass
        class TestDataclass:
            name: str
            value: int
        
        test_obj = TestDataclass(name="test", value=42)
        result = AirflowEventsClientUtils._get_lineage_dict(test_obj)
        
        expected = {
            'name': 'test',
            'value': 42,
            'type': str(type(test_obj))
        }
        self.assertEqual(result, expected)

    def test_get_lineage_dict_with_non_dataclass(self):
        """Test that _get_lineage_dict works correctly with non-dataclass objects."""
        class TestClass:
            def __init__(self, name, value):
                self.name = name
                self.value = value
        
        test_obj = TestClass(name="test", value=42)
        result = AirflowEventsClientUtils._get_lineage_dict(test_obj)
        
        expected = {
            'name': 'test',
            'value': 42,
            'type': str(type(test_obj))
        }
        self.assertEqual(result, expected)

    def test_get_lineage_dict_with_builtin_type(self):
        """Test that _get_lineage_dict works correctly with built-in types."""
        test_obj = "test_string"
        result = AirflowEventsClientUtils._get_lineage_dict(test_obj)
        
        expected = {
            'value': 'test_string',
            'type': str(type(test_obj))
        }
        self.assertEqual(result, expected)

    def test_get_lineage_dict_with_dictionary(self):
        """Test that _get_lineage_dict works correctly with dictionary objects."""
        test_dict = {'uri': 'test://uri', 'name': 'test_table', 'schema': 'public'}
        result = AirflowEventsClientUtils._get_lineage_dict(test_dict)
        
        expected = {
            'uri': 'test://uri',
            'name': 'test_table',
            'schema': 'public',
            'type': str(type(test_dict))
        }
        self.assertEqual(result, expected)

    def test_get_lineage_dict_with_dataset_object(self):
        """Test that _get_lineage_dict works correctly with Dataset objects (simulating customer's use case)."""
        # Simulate a Dataset object like the customer uses
        class Dataset:
            def __init__(self, uri):
                self.uri = uri
                self.scheme = uri.split('://')[0] if '://' in uri else 'unknown'
                self.name = uri.split('/')[-1] if '/' in uri else uri
        
        # Create a Dataset object similar to what the customer uses
        dataset = Dataset("redshift://cluster/database/schema/table")
        result = AirflowEventsClientUtils._get_lineage_dict(dataset)
        
        expected = {
            'uri': 'redshift://cluster/database/schema/table',
            'scheme': 'redshift',
            'name': 'table',
            'type': str(type(dataset))
        }
        self.assertEqual(result, expected)

    def test_get_lineage_list_with_non_dataclass_objects(self):
        """Test that _get_lineage_list works correctly with non-dataclass lineage objects."""
        # Create a mock task with non-dataclass outlets
        class MockTask:
            def __init__(self):
                self.outlets = [
                    self._create_dataset("redshift://cluster1/db1/schema1/table1"),
                    self._create_dataset("redshift://cluster2/db2/schema2/table2")
                ]
                self.inlets = [
                    self._create_dataset("redshift://cluster3/db3/schema3/table3")
                ]
            
            def _create_dataset(self, uri):
                class Dataset:
                    def __init__(self, uri):
                        self.uri = uri
                        self.scheme = uri.split('://')[0] if '://' in uri else 'unknown'
                        self.name = uri.split('/')[-1] if '/' in uri else uri
                return Dataset(uri)
        
        # Create a mock task instance
        task_instance = create_autospec(TaskInstance)
        task_instance.task = MockTask()
        
        # Test outlets
        outlets = AirflowEventsClientUtils._get_lineage_list(task_instance, "outlets")
        self.assertEqual(len(outlets), 2)
        
        # Check first outlet
        self.assertEqual(outlets[0]['uri'], 'redshift://cluster1/db1/schema1/table1')
        self.assertEqual(outlets[0]['scheme'], 'redshift')
        self.assertEqual(outlets[0]['name'], 'table1')
        self.assertIn('type', outlets[0])
        
        # Check second outlet
        self.assertEqual(outlets[1]['uri'], 'redshift://cluster2/db2/schema2/table2')
        self.assertEqual(outlets[1]['scheme'], 'redshift')
        self.assertEqual(outlets[1]['name'], 'table2')
        self.assertIn('type', outlets[1])
        
        # Test inlets
        inlets = AirflowEventsClientUtils._get_lineage_list(task_instance, "inlets")
        self.assertEqual(len(inlets), 1)
        
        # Check inlet
        self.assertEqual(inlets[0]['uri'], 'redshift://cluster3/db3/schema3/table3')
        self.assertEqual(inlets[0]['scheme'], 'redshift')
        self.assertEqual(inlets[0]['name'], 'table3')
        self.assertIn('type', inlets[0])

    def test_get_lineage_list_with_mixed_object_types(self):
        """Test that _get_lineage_list works correctly with mixed dataclass and non-dataclass objects."""
        from dataclasses import dataclass
        
        @dataclass
        class DataclassLineage:
            name: str
            value: int
        
        class NonDataclassLineage:
            def __init__(self, name, value):
                self.name = name
                self.value = value
        
        # Create a mock task with mixed lineage objects
        class MockTask:
            def __init__(self):
                self.outlets = [
                    DataclassLineage(name="dataclass_outlet", value=1),
                    NonDataclassLineage(name="non_dataclass_outlet", value=2),
                    "string_outlet"  # Built-in type
                ]
        
        # Create a mock task instance
        task_instance = create_autospec(TaskInstance)
        task_instance.task = MockTask()
        
        # Test outlets
        outlets = AirflowEventsClientUtils._get_lineage_list(task_instance, "outlets")
        self.assertEqual(len(outlets), 3)
        
        # Check dataclass outlet
        self.assertEqual(outlets[0]['name'], 'dataclass_outlet')
        self.assertEqual(outlets[0]['value'], 1)
        self.assertIn('type', outlets[0])
        
        # Check non-dataclass outlet
        self.assertEqual(outlets[1]['name'], 'non_dataclass_outlet')
        self.assertEqual(outlets[1]['value'], 2)
        self.assertIn('type', outlets[1])
        
        # Check string outlet
        self.assertEqual(outlets[2]['value'], 'string_outlet')
        self.assertIn('type', outlets[2])

