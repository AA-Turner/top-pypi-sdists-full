"""
Tests for Airflow 3.x compatibility issues.

These tests are specifically designed to catch compatibility issues that arise
when TaskInstance or other Airflow objects change between versions.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone

from airflow_mcd.callbacks.utils import AirflowEventsClientUtils
from airflow_mcd.callbacks.mcd_callbacks import mcd_task_success_callback


def airflow_major_version():
    """Get the major version of Airflow."""
    try:
        from airflow import __version__
        return int(__version__.split('.')[0])
    except Exception:
        return 2


class Airflow3CompatibilityTests(unittest.TestCase):
    """Test compatibility with Airflow 3.x breaking changes."""

    @unittest.skipIf(airflow_major_version() < 3, "Only run on Airflow 3+")
    def test_next_retry_datetime_not_accessed_on_runtime_task_instance(self):
        """
        Test that we don't access next_retry_datetime() on RuntimeTaskInstance in Airflow 3.
        
        This test specifically checks for the bug where RuntimeTaskInstance in Airflow 3
        doesn't have the next_retry_datetime() method that was available in Airflow 2.
        """
        # Create a mock that behaves like RuntimeTaskInstance (no next_retry_datetime method)
        mock_ti = Mock()
        mock_ti.task_id = "test_task"
        mock_ti.dag_id = "test_dag"
        mock_ti.run_id = "test_run"
        mock_ti.try_number = 1
        mock_ti.max_tries = 3
        mock_ti.state = "success"
        mock_ti.start_date = datetime.now(tz=timezone.utc)
        mock_ti.end_date = datetime.now(tz=timezone.utc)
        mock_ti.execution_date = datetime.now(tz=timezone.utc)
        mock_ti.task = Mock()
        mock_ti.log_url = "http://test"
        
        # Explicitly remove next_retry_datetime to simulate RuntimeTaskInstance
        # In Airflow 3, RuntimeTaskInstance doesn't have this method
        if hasattr(mock_ti, 'next_retry_datetime'):
            delattr(mock_ti, 'next_retry_datetime')
        
        # This should NOT raise AttributeError
        try:
            result = AirflowEventsClientUtils._get_next_retry_datetime(mock_ti)
            # In Airflow 3, this should return None since the method doesn't exist
            self.assertIsNone(result, "next_retry_datetime should return None for Airflow 3")
        except AttributeError as e:
            self.fail(f"_get_next_retry_datetime raised AttributeError: {e}")

    @unittest.skipIf(airflow_major_version() < 3, "Only run on Airflow 3+")
    def test_get_task_instance_result_handles_missing_attributes(self):
        """
        Test that _get_task_instance_result gracefully handles missing attributes.
        
        This tests the specific method that was failing in production.
        """
        # Create a mock task instance without next_retry_datetime
        mock_ti = Mock()
        mock_ti.task_id = "test_task"
        mock_ti.dag_id = "test_dag"
        mock_ti.run_id = "test_run"
        mock_ti.try_number = 1
        mock_ti.max_tries = 3
        mock_ti.state = "success"
        mock_ti.start_date = datetime.now(tz=timezone.utc)
        mock_ti.end_date = datetime.now(tz=timezone.utc)
        mock_ti.execution_date = datetime.now(tz=timezone.utc)
        mock_ti.task = Mock()
        mock_ti.task.inlets = []
        mock_ti.task.outlets = []
        mock_ti.log_url = "http://test"
        
        # Remove next_retry_datetime and duration to avoid Mock comparison issues
        if hasattr(mock_ti, 'next_retry_datetime'):
            delattr(mock_ti, 'next_retry_datetime')
        if hasattr(mock_ti, 'duration'):
            del mock_ti.duration
        
        # This should work without crashing
        try:
            result = AirflowEventsClientUtils._get_task_instance_result(mock_ti)
            
            # Verify the result has the expected structure
            self.assertIsNotNone(result)
            self.assertEqual(result.task_id, "test_task")
            self.assertTrue(hasattr(result, 'next_retry_datetime'))
            # In Airflow 3, next_retry_datetime should be None
            if airflow_major_version() >= 3:
                self.assertIsNone(result.next_retry_datetime, 
                                "next_retry_datetime should be None in Airflow 3")
        except AttributeError as e:
            if 'next_retry_datetime' in str(e):
                self.fail(f"_get_task_instance_result crashed accessing next_retry_datetime: {e}")
            else:
                raise

    def test_next_retry_datetime_returns_none_for_airflow3(self):
        """
        Test that _get_next_retry_datetime returns None for Airflow 3.x.
        
        This test works across all Airflow versions and verifies the version check.
        """
        # Create a mock task instance
        mock_ti = Mock()
        mock_ti.task = Mock()
        mock_ti.end_date = datetime.now(tz=timezone.utc)
        
        if airflow_major_version() >= 3:
            # In Airflow 3, should return None regardless of whether method exists
            result = AirflowEventsClientUtils._get_next_retry_datetime(mock_ti)
            self.assertIsNone(result, 
                            "Should return None for Airflow 3+ even if method exists")
        else:
            # In Airflow 2, if the method exists, it should be called
            mock_ti.next_retry_datetime = Mock(return_value=datetime.now(tz=timezone.utc))
            result = AirflowEventsClientUtils._get_next_retry_datetime(mock_ti)
            # Should return a datetime string or None
            self.assertTrue(isinstance(result, (str, type(None))))

    @unittest.skipIf(airflow_major_version() < 3, "Only run on Airflow 3+")
    def test_airflow3_task_instance_serialization(self):
        """
        Test that task instance serialization works in Airflow 3.
        
        This ensures that all the fields we try to access exist and can be serialized.
        """
        mock_ti = Mock()
        mock_ti.task_id = "test_task"
        mock_ti.dag_id = "test_dag"
        mock_ti.run_id = "test_run"
        mock_ti.try_number = 1
        mock_ti.max_tries = 3
        mock_ti.state = "success"
        mock_ti.start_date = datetime.now(tz=timezone.utc)
        mock_ti.end_date = datetime.now(tz=timezone.utc)
        mock_ti.execution_date = datetime.now(tz=timezone.utc)
        mock_ti.task = Mock()
        mock_ti.task.inlets = []
        mock_ti.task.outlets = []
        mock_ti.log_url = "http://test"
        
        # For Airflow 3, explicitly remove duration to avoid Mock comparison issues
        if hasattr(mock_ti, 'duration'):
            del mock_ti.duration
        
        # Try to get all the attributes we need
        result = AirflowEventsClientUtils._get_task_instance_result(mock_ti)
        
        # Verify all expected fields exist (result is a dataclass/Pydantic model)
        expected_fields = [
            'task_id', 'state', 'log_url', 'prev_attempted_tries', 'duration',
            'execution_date', 'start_date', 'end_date', 'next_retry_datetime',
            'max_tries', 'try_number', 'exception_message', 'inlets', 'outlets'
        ]
        
        for field in expected_fields:
            self.assertTrue(hasattr(result, field), f"Missing field '{field}' in task instance result")


if __name__ == '__main__':
    unittest.main()

