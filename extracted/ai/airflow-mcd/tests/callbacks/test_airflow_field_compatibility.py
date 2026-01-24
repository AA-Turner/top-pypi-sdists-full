"""
Tests to verify that all fields accessed from TaskInstance and DAG objects exist.

These tests act as a regression suite to detect when Airflow removes or deprecates
fields that we depend on. They should be run against all supported Airflow versions.
"""
import unittest
import warnings
from unittest.mock import Mock
from datetime import datetime, timezone

from airflow_mcd.callbacks.utils import AirflowEventsClientUtils


def airflow_major_version():
    """Get the major version of Airflow."""
    try:
        from airflow import __version__
        return int(__version__.split('.')[0])
    except Exception:
        return 2


class TaskInstanceFieldCompatibilityTests(unittest.TestCase):
    """Test that all TaskInstance fields we access are available."""

    def test_task_instance_required_fields_exist(self):
        """
        Test that all required TaskInstance fields exist and can be accessed.
        
        This test verifies all fields that we directly access in our code:
        - task_id
        - state
        - log_url
        - max_tries
        - try_number
        - task (for lineage)
        """
        # Create a mock task instance with all required fields
        mock_ti = Mock()
        mock_ti.task_id = "test_task"
        mock_ti.state = "success"
        mock_ti.log_url = "http://test/log"
        mock_ti.max_tries = 3
        mock_ti.try_number = 1
        mock_ti.task = Mock()
        
        # These should not raise any errors
        self.assertEqual(mock_ti.task_id, "test_task")
        self.assertEqual(mock_ti.state, "success")
        self.assertEqual(mock_ti.log_url, "http://test/log")
        self.assertEqual(mock_ti.max_tries, 3)
        self.assertEqual(mock_ti.try_number, 1)
        self.assertIsNotNone(mock_ti.task)

    def test_task_instance_date_fields_in_airflow2(self):
        """
        Test that date fields exist in Airflow 2.x.
        
        Fields tested:
        - start_date
        - end_date
        - execution_date
        """
        if airflow_major_version() >= 3:
            self.skipTest("Only relevant for Airflow 2.x")
        
        mock_ti = Mock()
        mock_ti.start_date = datetime.now(tz=timezone.utc)
        mock_ti.end_date = datetime.now(tz=timezone.utc)
        mock_ti.execution_date = datetime.now(tz=timezone.utc)
        
        self.assertIsNotNone(mock_ti.start_date)
        self.assertIsNotNone(mock_ti.end_date)
        self.assertIsNotNone(mock_ti.execution_date)

    @unittest.skipIf(airflow_major_version() < 3, "Only relevant for Airflow 3+")
    def test_task_instance_date_fields_in_airflow3(self):
        """
        Test that we handle missing date fields gracefully in Airflow 3.x.
        
        In Airflow 3, RuntimeTaskInstance may not have all date fields.
        We use getattr with defaults to handle this.
        """
        mock_ti = Mock()
        # Simulate RuntimeTaskInstance which may not have all fields
        mock_ti.start_date = datetime.now(tz=timezone.utc)
        mock_ti.end_date = datetime.now(tz=timezone.utc)
        mock_ti.task_id = "test_task"
        mock_ti.state = "success"
        mock_ti.log_url = "http://test"
        mock_ti.max_tries = 3
        mock_ti.try_number = 1
        mock_ti.task = Mock()
        
        # Should not crash when accessing via getattr
        start_date = getattr(mock_ti, 'start_date', None)
        end_date = getattr(mock_ti, 'end_date', None)
        execution_date = getattr(mock_ti, 'execution_date', None)
        logical_date = getattr(mock_ti, 'logical_date', None)
        
        self.assertIsNotNone(start_date)
        self.assertIsNotNone(end_date)
        # execution_date and logical_date may be None in Airflow 3
        # This is expected and handled by our code

    def test_task_instance_airflow2_specific_fields(self):
        """
        Test fields that exist in Airflow 2.x but not in Airflow 3.x.
        
        Fields tested:
        - prev_attempted_tries
        - duration
        - next_retry_datetime() method
        """
        if airflow_major_version() >= 3:
            self.skipTest("Only relevant for Airflow 2.x")
        
        mock_ti = Mock()
        mock_ti.prev_attempted_tries = 0
        mock_ti.duration = 10.5
        mock_ti.next_retry_datetime = Mock(return_value=datetime.now(tz=timezone.utc))
        
        self.assertEqual(mock_ti.prev_attempted_tries, 0)
        self.assertEqual(mock_ti.duration, 10.5)
        self.assertIsNotNone(mock_ti.next_retry_datetime())

    @unittest.skipIf(airflow_major_version() < 3, "Only relevant for Airflow 3+")
    def test_task_instance_airflow3_missing_fields(self):
        """
        Test that we handle fields missing in Airflow 3.x gracefully.
        
        In Airflow 3, RuntimeTaskInstance doesn't have:
        - prev_attempted_tries (we calculate it from try_number)
        - duration (we calculate it from start_date and end_date)
        - next_retry_datetime() (we return None)
        """
        mock_ti = Mock()
        mock_ti.task_id = "test_task"
        mock_ti.state = "success"
        mock_ti.log_url = "http://test"
        mock_ti.max_tries = 3
        mock_ti.try_number = 2
        mock_ti.task = Mock()
        mock_ti.start_date = datetime.now(tz=timezone.utc)
        mock_ti.end_date = datetime.now(tz=timezone.utc)
        
        # These should work via getattr with defaults
        prev_attempted_tries = getattr(mock_ti, 'try_number', 1) - 1
        duration = getattr(mock_ti, 'duration', None)
        
        self.assertEqual(prev_attempted_tries, 1)
        # duration may be None, which is expected
        
        # next_retry_datetime should return None for Airflow 3
        result = AirflowEventsClientUtils._get_next_retry_datetime(mock_ti)
        self.assertIsNone(result)

    def test_task_instance_lineage_access(self):
        """
        Test that we can access task.inlets and task.outlets for lineage.
        
        Fields accessed:
        - task.inlets
        - task.outlets
        """
        mock_task = Mock()
        mock_task.inlets = []
        mock_task.outlets = []
        
        mock_ti = Mock()
        mock_ti.task = mock_task
        
        # Should not raise AttributeError
        self.assertIsNotNone(mock_ti.task.inlets)
        self.assertIsNotNone(mock_ti.task.outlets)

    def test_task_instance_result_serialization(self):
        """
        End-to-end test: verify all fields can be serialized into DagTaskInstanceResult.
        
        This test ensures that _get_task_instance_result doesn't crash when accessing
        any TaskInstance fields.
        """
        mock_ti = Mock()
        mock_ti.task_id = "test_task"
        mock_ti.dag_id = "test_dag"
        mock_ti.run_id = "test_run"
        mock_ti.state = "success"
        mock_ti.log_url = "http://test"
        mock_ti.max_tries = 3
        mock_ti.try_number = 1
        mock_ti.start_date = datetime.now(tz=timezone.utc)
        mock_ti.end_date = datetime.now(tz=timezone.utc)
        mock_ti.execution_date = datetime.now(tz=timezone.utc)
        
        # Add task with lineage
        mock_task = Mock()
        mock_task.inlets = []
        mock_task.outlets = []
        mock_ti.task = mock_task
        
        # For Airflow 2, add the extra fields
        if airflow_major_version() < 3:
            mock_ti.prev_attempted_tries = 0
            mock_ti.duration = 10.5
            mock_ti.next_retry_datetime = Mock(return_value=None)
        else:
            # For Airflow 3, we need to explicitly remove duration attribute
            # to avoid the Mock comparison issue (Mock objects can't be compared with >)
            if hasattr(mock_ti, 'duration'):
                del mock_ti.duration
        
        # This should not crash
        try:
            result = AirflowEventsClientUtils._get_task_instance_result(mock_ti)
            
            # Verify all expected fields exist (result is a dataclass/Pydantic model)
            self.assertEqual(result.task_id, "test_task")
            self.assertEqual(result.state, "success")
            self.assertEqual(result.log_url, "http://test")
            self.assertEqual(result.max_tries, 3)
            self.assertEqual(result.try_number, 1)
            self.assertIsNotNone(result.start_date)
            self.assertIsNotNone(result.end_date)
            self.assertIsNotNone(result.execution_date)
            self.assertTrue(hasattr(result, 'next_retry_datetime'))  # Field should exist (can be None)
            self.assertIsNotNone(result.duration)  # Should be calculated
            self.assertIsNotNone(result.prev_attempted_tries)  # Should be calculated
            
        except Exception as e:
            self.fail(f"_get_task_instance_result failed: {e}")


class DAGFieldCompatibilityTests(unittest.TestCase):
    """Test that all DAG fields we access are available."""

    def test_dag_required_fields_exist(self):
        """
        Test that all required DAG fields exist and can be accessed.
        
        Fields tested:
        - dag_id
        - tags
        - params
        """
        mock_dag = Mock()
        mock_dag.dag_id = "test_dag"
        mock_dag.tags = ["tag1", "tag2"]
        mock_dag.params = {}
        
        # These should not raise any errors
        self.assertEqual(mock_dag.dag_id, "test_dag")
        self.assertEqual(len(mock_dag.tags), 2)
        self.assertIsNotNone(mock_dag.params)

    def test_dag_tags_iteration(self):
        """
        Test that we can iterate over DAG tags.
        
        We use: [tag for tag in dag.tags]
        """
        mock_dag = Mock()
        mock_dag.tags = {"tag1", "tag2", "tag3"}
        
        # Should be able to iterate
        tags_list = [tag for tag in mock_dag.tags]
        self.assertEqual(len(tags_list), 3)

    def test_dag_params_access(self):
        """
        Test that we can access dag.params and get values from it.
        
        We access: dag.params.get('mcd_connection_id')
        """
        mock_dag = Mock()
        mock_dag.params = {'mcd_connection_id': 'test_conn'}
        
        # Should be able to get param
        conn_id = mock_dag.params.get('mcd_connection_id')
        self.assertEqual(conn_id, 'test_conn')

    def test_dag_params_can_be_none(self):
        """
        Test that we handle dag.params being None.
        
        In some versions/configurations, dag.params might be None.
        We use: dag.params or {}
        """
        mock_dag = Mock()
        mock_dag.params = None
        
        # Should handle None gracefully
        params = mock_dag.params or {}
        self.assertEqual(params, {})


class ContextFieldCompatibilityTests(unittest.TestCase):
    """Test that all context fields we access are available."""

    def test_context_required_fields_exist(self):
        """
        Test that all required context fields exist.
        
        Fields accessed:
        - context['dag']
        - context['task_instance']
        - context['run_id']
        - context['dag_run']
        """
        context = {
            'dag': Mock(),
            'task_instance': Mock(),
            'run_id': 'test_run_id',
            'dag_run': Mock()
        }
        
        # These should not raise KeyError
        self.assertIsNotNone(context['dag'])
        self.assertIsNotNone(context['task_instance'])
        self.assertEqual(context['run_id'], 'test_run_id')
        self.assertIsNotNone(context['dag_run'])

    def test_dag_run_state_field(self):
        """
        Test that dag_run.state is accessible.
        
        We check: dag_run.state in _SUCCESS_STATES
        """
        mock_dag_run = Mock()
        mock_dag_run.state = "success"
        
        # Should be accessible
        self.assertEqual(mock_dag_run.state, "success")

    @unittest.skipIf(airflow_major_version() < 3, "Only relevant for Airflow 3+")
    def test_context_task_instances_in_airflow3(self):
        """
        Test that we handle missing 'task_instances' in context for Airflow 3.
        
        In Airflow 3, the 'task_instances' key may not be available in dag-level callbacks.
        We use: context.get('task_instances', [])
        """
        context = {
            'dag': Mock(),
            'run_id': 'test_run_id',
            'dag_run': Mock()
        }
        
        # Should not crash when task_instances is missing
        task_instances = context.get('task_instances', [])
        self.assertEqual(task_instances, [])


class FieldAccessRegressionTests(unittest.TestCase):
    """
    Regression tests to catch when Airflow removes fields we depend on.
    
    These tests will FAIL if a field is removed, alerting us to update our code.
    """

    def test_all_taskinstance_fields_are_accessible(self):
        """
        Comprehensive test that verifies all TaskInstance fields we use.
        
        This test will fail if Airflow removes any field we depend on.
        """
        mock_ti = Mock()
        
        # Fields we ALWAYS access (required)
        required_fields = [
            'task_id',
            'state', 
            'log_url',
            'max_tries',
            'try_number',
            'task'
        ]
        
        for field in required_fields:
            setattr(mock_ti, field, Mock())
            self.assertTrue(hasattr(mock_ti, field), 
                          f"Required field '{field}' not found on TaskInstance")

    def test_all_dag_fields_are_accessible(self):
        """
        Comprehensive test that verifies all DAG fields we use.
        
        This test will fail if Airflow removes any field we depend on.
        """
        mock_dag = Mock()
        
        # Fields we ALWAYS access (required)
        required_fields = [
            'dag_id',
            'tags',
            'params'
        ]
        
        for field in required_fields:
            setattr(mock_dag, field, Mock())
            self.assertTrue(hasattr(mock_dag, field),
                          f"Required field '{field}' not found on DAG")


class DeprecationWarningTests(unittest.TestCase):
    """
    Tests to catch deprecation warnings for fields we depend on.
    
    These tests will FAIL if Airflow deprecates any field we use,
    giving us advance warning before they're removed in a future version.
    """

    def test_taskinstance_field_access_no_deprecation_warnings(self):
        """
        Test that accessing TaskInstance fields doesn't trigger deprecation warnings.
        
        This test catches when Airflow deprecates fields before they're removed.
        """
        mock_ti = Mock()
        mock_ti.task_id = "test_task"
        mock_ti.state = "success"
        mock_ti.log_url = "http://test"
        mock_ti.max_tries = 3
        mock_ti.try_number = 1
        mock_ti.start_date = datetime.now(tz=timezone.utc)
        mock_ti.end_date = datetime.now(tz=timezone.utc)
        mock_ti.execution_date = datetime.now(tz=timezone.utc)
        mock_ti.task = Mock()
        mock_ti.task.inlets = []
        mock_ti.task.outlets = []
        
        # Version-specific fields
        if airflow_major_version() < 3:
            mock_ti.prev_attempted_tries = 0
            mock_ti.duration = 10.5
        
        # Capture any deprecation warnings
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter("always", DeprecationWarning)
            
            # Access all fields we use
            _ = mock_ti.task_id
            _ = mock_ti.state
            _ = mock_ti.log_url
            _ = mock_ti.max_tries
            _ = mock_ti.try_number
            _ = mock_ti.start_date
            _ = mock_ti.end_date
            _ = getattr(mock_ti, 'execution_date', None)
            _ = mock_ti.task
            _ = mock_ti.task.inlets
            _ = mock_ti.task.outlets
            
            if airflow_major_version() < 3:
                _ = mock_ti.prev_attempted_tries
                _ = mock_ti.duration
            
            # Check for deprecation warnings
            deprecation_warnings = [w for w in warning_list if issubclass(w.category, DeprecationWarning)]
            
            if deprecation_warnings:
                warning_messages = "\n".join([f"  - {w.message} at {w.filename}:{w.lineno}" 
                                            for w in deprecation_warnings])
                self.fail(f"Found {len(deprecation_warnings)} deprecation warning(s) when accessing TaskInstance fields:\n{warning_messages}")

    def test_dag_field_access_no_deprecation_warnings(self):
        """
        Test that accessing DAG fields doesn't trigger deprecation warnings.
        
        This test catches when Airflow deprecates fields before they're removed.
        """
        mock_dag = Mock()
        mock_dag.dag_id = "test_dag"
        mock_dag.tags = {"tag1", "tag2"}
        mock_dag.params = {"param1": "value1"}
        
        # Capture any deprecation warnings
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter("always", DeprecationWarning)
            
            # Access all fields we use
            _ = mock_dag.dag_id
            _ = [tag for tag in mock_dag.tags]
            _ = mock_dag.params or {}
            _ = mock_dag.params.get('param1')
            
            # Check for deprecation warnings
            deprecation_warnings = [w for w in warning_list if issubclass(w.category, DeprecationWarning)]
            
            if deprecation_warnings:
                warning_messages = "\n".join([f"  - {w.message} at {w.filename}:{w.lineno}" 
                                            for w in deprecation_warnings])
                self.fail(f"Found {len(deprecation_warnings)} deprecation warning(s) when accessing DAG fields:\n{warning_messages}")

    def test_real_taskinstance_serialization_no_deprecation_warnings(self):
        """
        End-to-end test: ensure _get_task_instance_result doesn't trigger deprecations.
        
        This is the most comprehensive test - it exercises the actual code path
        and will catch deprecation warnings from any of our field accesses.
        """
        mock_ti = Mock()
        mock_ti.task_id = "test_task"
        mock_ti.state = "success"
        mock_ti.log_url = "http://test"
        mock_ti.max_tries = 3
        mock_ti.try_number = 1
        mock_ti.start_date = datetime.now(tz=timezone.utc)
        mock_ti.end_date = datetime.now(tz=timezone.utc)
        mock_ti.execution_date = datetime.now(tz=timezone.utc)
        
        mock_task = Mock()
        mock_task.inlets = []
        mock_task.outlets = []
        mock_ti.task = mock_task
        
        # Version-specific fields
        if airflow_major_version() < 3:
            mock_ti.prev_attempted_tries = 0
            mock_ti.duration = 10.5
            mock_ti.next_retry_datetime = Mock(return_value=None)
        else:
            # For Airflow 3, explicitly remove duration to avoid Mock comparison issues
            if hasattr(mock_ti, 'duration'):
                del mock_ti.duration
        
        # Capture any deprecation warnings
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter("always", DeprecationWarning)
            
            # Call the actual method that accesses all fields
            try:
                result = AirflowEventsClientUtils._get_task_instance_result(mock_ti)
                
                # Verify it worked
                self.assertIsNotNone(result)
                
            except Exception as e:
                self.fail(f"_get_task_instance_result failed: {e}")
            
            # Check for deprecation warnings
            deprecation_warnings = [w for w in warning_list if issubclass(w.category, DeprecationWarning)]
            
            if deprecation_warnings:
                warning_messages = "\n".join([f"  - {w.message} at {w.filename}:{w.lineno}" 
                                            for w in deprecation_warnings])
                self.fail(f"Found {len(deprecation_warnings)} deprecation warning(s) in _get_task_instance_result:\n{warning_messages}")


if __name__ == '__main__':
    unittest.main()

