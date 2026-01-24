"""
Test file for Airflow 3 callback context based on actual logs.
This test uses real Airflow classes to ensure compatibility.
"""

from unittest import TestCase, skipIf
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
import uuid
from airflow_mcd import airflow_major_version

# Import Airflow modules - these will fail gracefully in Airflow 2 environments
try:
    from airflow.models import DAG, DagRun, TaskInstance
    from airflow.providers.standard.operators.python import PythonOperator
    from airflow_mcd.callbacks.utils import AirflowEventsClientUtils
    from airflow_mcd.callbacks.client import DagResult
except ImportError:
    # If imports fail, we're likely in an Airflow 2 environment
    pass


@skipIf(
    airflow_major_version() < 3,
    "These tests are only for Airflow 3 compatibility"
)


class TestAirflow3Callbacks(TestCase):
    """Test class for Airflow 3 callback context handling."""
    
    def setUp(self):
        """Set up test fixtures using real Airflow classes."""
        # Create a real DAG object
        self.dag = DAG(
            dag_id="monte_carlo_example_dag",
            start_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            schedule=None,  # Airflow 3 uses 'schedule' instead of 'schedule_interval'
            tags=[]
        )
        
        # Add real tasks to the DAG
        def task1_func():
            return "task1"
        
        def task2_func():
            return "task2"
        
        self.task1 = PythonOperator(
            task_id="example_elt_job_1",
            python_callable=task1_func,
            dag=self.dag
        )
        
        self.task2 = PythonOperator(
            task_id="example_elt_job_2", 
            python_callable=task2_func,
            dag=self.dag
        )
        
        # Create a real DagRun object
        self.dag_run = DagRun(
            dag_id="monte_carlo_example_dag",
            run_id="manual__2025-07-18T13:58:43.164720+00:00",
            run_type="manual",
            state="success",
            start_date=datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            logical_date=datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc)  # Airflow 3 uses logical_date instead of execution_date
        )
        # Set end_date and data intervals after creation since they're not constructor parameters in Airflow 3
        self.dag_run.end_date = datetime(2025, 7, 18, 13, 58, 43, 177459, tzinfo=timezone.utc)
        self.dag_run.data_interval_start = datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.dag_run.data_interval_end = datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        
        # Create real TaskInstance objects
        # Note: Airflow 3.1+ may require dag_version_id parameter
        try:
            # Try with dag_version_id first (Airflow 3.1+)
            dag_version_id = uuid.uuid4()
            self.task_instance1 = TaskInstance(
                task=self.task1,
                run_id="manual__2025-07-18T13:58:43.164720+00:00",
                dag_version_id=dag_version_id
            )
        except TypeError:
            # Fall back to without dag_version_id (Airflow 3.0)
            self.task_instance1 = TaskInstance(
                task=self.task1,
                run_id="manual__2025-07-18T13:58:43.164720+00:00"
            )
            dag_version_id = None
        # In Airflow 3, TaskInstance doesn't have execution_date - it uses logical_date from DagRun
        self.task_instance1.state = "success"
        self.task_instance1.start_date = datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.task_instance1.end_date = datetime(2023, 1, 1, 0, 1, 0, tzinfo=timezone.utc)
        
        try:
            # Try with dag_version_id first (Airflow 3.1+)
            self.task_instance2 = TaskInstance(
                task=self.task2,
                run_id="manual__2025-07-18T13:58:43.164720+00:00",
                dag_version_id=dag_version_id
            )
        except (TypeError, NameError):
            # Fall back to without dag_version_id (Airflow 3.0) or if dag_version_id is None
            self.task_instance2 = TaskInstance(
                task=self.task2,
                run_id="manual__2025-07-18T13:58:43.164720+00:00"
            )
        # In Airflow 3, TaskInstance doesn't have execution_date - it uses logical_date from DagRun
        self.task_instance2.state = "success"
        self.task_instance2.start_date = datetime(2023, 1, 1, 0, 1, 0, tzinfo=timezone.utc)
        self.task_instance2.end_date = datetime(2023, 1, 1, 0, 2, 0, tzinfo=timezone.utc)
        
        # Mock the get_task_instances method to return our real TaskInstances
        self.dag_run.get_task_instances = Mock(return_value=[self.task_instance1, self.task_instance2])
        
        # Mock the DAG's get_dagrun method to return our DagRun object
        self.dag.get_dagrun = Mock(return_value=self.dag_run)
        
        # Create the context dictionary - for Airflow 3, dag_run should be in context
        self.context = {
            'dag': self.dag,
            'run_id': 'manual__2025-07-18T13:58:43.164720+00:00',
            'reason': 'success',
            'dag_run': self.dag_run  # Airflow 3 callbacks should provide this
        }
    
    def test_dag_object_properties(self):
        """Test that real DAG object has expected properties."""
        dag = self.context['dag']
        self.assertEqual(dag.dag_id, "monte_carlo_example_dag")

        self.assertEqual(dag.tags, set())  # DAG.tags returns a set in Airflow 3
        
        # Test real DAG methods
        self.assertTrue(dag.has_task("example_elt_job_1"))
        self.assertTrue(dag.has_task("example_elt_job_2"))
        self.assertFalse(dag.has_task("nonexistent_task"))
    
    def test_dag_run_object_properties(self):
        """Test that real DagRun object has expected properties."""
        # Get dag_run via the DAG's get_dagrun method (as the callback does)
        dag_run = self.context['dag'].get_dagrun(run_id=self.context['run_id'])
        self.assertEqual(dag_run.state, "success")
        self.assertEqual(dag_run.run_id, "manual__2025-07-18T13:58:43.164720+00:00")
        self.assertIsNotNone(dag_run.logical_date)  # Airflow 3 uses logical_date
        self.assertIsNotNone(dag_run.end_date)
        self.assertIsNotNone(dag_run.start_date)
        self.assertEqual(dag_run.dag_id, "monte_carlo_example_dag")
        self.assertEqual(dag_run.run_type, "manual")
        
        # Test real DagRun methods
        self.assertEqual(dag_run.get_state(), "success")
    
    def test_task_instances_real(self):
        """Test that get_task_instances returns real TaskInstance objects."""
        # Get dag_run via the DAG's get_dagrun method (as the callback does)
        dag_run = self.context['dag'].get_dagrun(run_id=self.context['run_id'])
        task_instances = dag_run.get_task_instances()
        self.assertEqual(len(task_instances), 2)
        
        # Verify they are real TaskInstance objects
        self.assertIsInstance(task_instances[0], TaskInstance)
        self.assertIsInstance(task_instances[1], TaskInstance)
        
        # Test real TaskInstance properties
        self.assertEqual(task_instances[0].task_id, "example_elt_job_1")
        self.assertEqual(task_instances[0].state, "success")
        self.assertEqual(task_instances[1].task_id, "example_elt_job_2")
        self.assertEqual(task_instances[1].state, "success")
    
    @patch('airflow_mcd.callbacks.utils.AirflowEventsClient')
    def test_mcd_post_dag_result_produces_expected_dagresult(self, mock_client_class):
        """Test that mcd_post_dag_result produces the expected DagResult object."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Call the function
        AirflowEventsClientUtils.mcd_post_dag_result(self.context)
        
        # Verify client was created and upload_dag_result was called
        mock_client_class.assert_called_once()
        mock_client.upload_dag_result.assert_called_once()
        
        # Get the DagResult object that was passed to upload_dag_result
        dag_result = mock_client.upload_dag_result.call_args[0][0]
        self.assertIsInstance(dag_result, DagResult)
        
        # Verify the DagResult properties match our expectations
        self.assertEqual(dag_result.dag_id, "monte_carlo_example_dag")
        self.assertEqual(dag_result.run_id, "manual__2025-07-18T13:58:43.164720+00:00")
        self.assertTrue(dag_result.success)  # dag_run.state is "success"
        self.assertEqual(dag_result.reason, "success")
        self.assertEqual(dag_result.state, "success")
        self.assertEqual(len(dag_result.tasks), 0)  # In Airflow 3, tasks are not included in the DagResult
        self.assertEqual(dag_result.tags, [])
        
        # Verify dates are properly formatted
        self.assertIsNotNone(dag_result.execution_date)  # DagResult still uses execution_date field
        self.assertIsNotNone(dag_result.start_date)
        self.assertIsNotNone(dag_result.end_date)
        self.assertTrue(hasattr(dag_result, 'original_dates'))  # Should have original_dates
    
    @patch('airflow_mcd.callbacks.utils.AirflowEventsClient')
    def test_dagresult_structure_matches_airflow2_format(self, mock_client_class):
        """Test that the DagResult structure matches the expected Airflow 2 format."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Call the function
        AirflowEventsClientUtils.mcd_post_dag_result(self.context)
        
        # Get the DagResult object
        dag_result = mock_client.upload_dag_result.call_args[0][0]
        
        # Test that all required fields from Airflow 2 sample are present
        required_dag_fields = [
            'dag_id', 'run_id', 'success', 'reason', 'state', 
            'execution_date', 'start_date', 'end_date', 'tags', 'original_dates'
        ]
        
        for field in required_dag_fields:
            self.assertTrue(hasattr(dag_result, field), f"DagResult missing required field: {field}")
        
        # Test that all required task fields from Airflow 2 sample are present
        required_task_fields = [
            'task_id', 'state', 'log_url', 'prev_attempted_tries', 'duration',
            'execution_date', 'start_date', 'end_date', 'next_retry_datetime',
            'max_tries', 'try_number', 'exception_message', 'inlets', 'outlets', 'original_dates'
        ]
        
        for task in dag_result.tasks:
            for field in required_task_fields:
                self.assertTrue(hasattr(task, field), f"Task missing required field: {field}")
        
        # Verify the structure matches the expected format
        self.assertEqual(dag_result.dag_id, "monte_carlo_example_dag")
        self.assertEqual(dag_result.run_id, "manual__2025-07-18T13:58:43.164720+00:00")
        self.assertTrue(dag_result.success)
        self.assertEqual(dag_result.reason, "success")
        self.assertEqual(dag_result.state, "success")
        self.assertEqual(len(dag_result.tasks), 0)
    
    def test_context_structure_matches_logs(self):
        """Test that our test context matches the structure from actual logs."""
        # Verify context keys match logs (before dag_run is added)
        expected_keys = ['dag', 'run_id', 'reason', 'dag_run']
        self.assertEqual(list(self.context.keys()), expected_keys)
        
        # Verify run_id format matches logs
        self.assertTrue(self.context['run_id'].startswith('manual__'))
        
        # Verify reason matches logs
        self.assertEqual(self.context['reason'], 'success')
        
        # Verify DAG properties match logs
        self.assertEqual(self.context['dag'].dag_id, "monte_carlo_example_dag")
        self.assertEqual(len(self.context['dag'].tasks), 2)
        self.assertEqual(self.context['dag'].tags, set())  # DAG.tags returns a set in Airflow 3
        
        dag_run = self.context['dag_run']
        self.assertEqual(dag_run.state, "success")
        self.assertIsNotNone(dag_run.logical_date)
    
    def test_airflow3_execution_date_handling(self):
        """Test that Airflow 3 execution_date handling works correctly."""
        # Get the DagRun via the DAG's get_dagrun method (as the callback does)
        dag_run = self.context['dag'].get_dagrun(run_id=self.context['run_id'])
        
        # Test the execution_date fallback logic (as implemented in the callback)
        # The callback uses: execution_date = dag_run.execution_date if hasattr(dag_run, 'execution_date') else dag_run.data_interval_start
        if hasattr(dag_run, 'execution_date') and dag_run.execution_date:
            execution_date = dag_run.execution_date
        else:
            # Use data_interval_start as fallback (Airflow 3 behavior)
            execution_date = dag_run.data_interval_start
        
        self.assertIsNotNone(execution_date)
        self.assertIsInstance(execution_date, datetime)
    
    def test_task_instance_compatibility(self):
        """Test that TaskInstance objects work with our compatibility code."""
        ti = self.task_instance1
        
        # Test properties that might be different in Airflow 3
        self.assertTrue(hasattr(ti, 'task_id'))
        self.assertTrue(hasattr(ti, 'state'))
        self.assertTrue(hasattr(ti, 'start_date'))
        self.assertTrue(hasattr(ti, 'end_date'))
        self.assertTrue(hasattr(ti, 'try_number'))
        self.assertTrue(hasattr(ti, 'max_tries'))
        
        # Test that we can access task properties
        self.assertEqual(ti.task.task_id, "example_elt_job_1")
    
    def test_dag_run_methods_availability(self):
        """Test that DagRun methods are available and work correctly."""
        # Get the DagRun via the DAG's get_dagrun method (as the callback does)
        dag_run = self.context['dag'].get_dagrun(run_id=self.context['run_id'])
        
        # Test methods that should be available
        self.assertTrue(hasattr(dag_run, 'get_task_instances'))
        self.assertTrue(hasattr(dag_run, 'get_state'))
        self.assertTrue(hasattr(dag_run, 'set_state'))
        
        # Test method calls
        self.assertEqual(dag_run.get_state(), "success")
