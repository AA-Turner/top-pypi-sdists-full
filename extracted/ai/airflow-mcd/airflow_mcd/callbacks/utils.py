import json
import logging
from copy import deepcopy
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

import airflow
from pycarlo.common.utils import truncate_string

from airflow_mcd import airflow_major_version
from airflow_mcd.callbacks.client import (
    AirflowEventsClient,
    DagResult,
    DagTaskInstanceResult,
    DagTaskResult,
    SlaMissesResult,
    TaskSlaMiss,
)
from airflow.models import DAG, DagRun, TaskInstance

if airflow_major_version() < 3:
    from airflow.models import SlaMiss
else:
    SlaMiss = None


logger = logging.getLogger(__name__)

_DEFAULT_CALL_TIMEOUT = 10
_SUCCESS_STATES = ['success', 'skipped']
_EXCEPTION_MSG_LIMIT = 10 * 1024  # 10kb

_DEFAULT_CONNECTION_ID = "mcd_gateway_default_session"
_FALLBACK_CONNECTION_ID = "mcd_default_session"


class AirflowEventsClientUtils:
    @classmethod
    def mcd_post_dag_result(
            cls,
            context: Dict,
    ):
        dag_run: DagRun = context['dag_run']

        # Create a context dictionary that includes all required fields for validation
        validation_context = {
            'dag': context['dag'],
            'run_id': context['run_id'],
            'dag_run': dag_run,
            'reason': context['reason'],
        }
        
        if not cls._validate_dag_callback_context(context=validation_context):
            logger.error("DAG callback validation failed")
            return

        dag: DAG = context['dag']
        dag_tags = [tag for tag in dag.tags]

        # In Airflow 3 the task instances are not available in the context
        # and we cannot use dag_run.get_task_instances() as it is no longer allowed
        task_instances = dag_run.get_task_instances() if airflow_major_version() < 3 else []

        # In Airflow 3 the execution_date was replaced by logical_date
        # Check here for more details: https://airflow.apache.org/docs/apache-airflow/stable/faq.html#what-does-execution-date-mean
        execution_date = (
            getattr(dag_run, 'execution_date', None) or
            getattr(dag_run, 'logical_date', None) or
            datetime.now(tz=timezone.utc)
        )
        
        
        # Create result with actual task instances
        result = DagResult(
            dag_id=dag.dag_id,
            run_id=context['run_id'],
            success=dag_run.state in _SUCCESS_STATES,
            reason=context['reason'],
            tasks=[cls._get_task_instance_result(ti) for ti in task_instances],
            state=dag_run.state,
            execution_date=cls._get_datetime_isoformat(execution_date),
            start_date=cls._get_datetime_isoformat(dag_run.start_date),
            end_date=cls._get_datetime_isoformat(dag_run.end_date),
            original_dates=cls._get_original_dates(execution_date, dag_run.start_date, dag_run.end_date),
            tags=dag_tags,
        )
        cls._get_events_client(dag).upload_dag_result(result)

    @staticmethod
    def _validate_dag_callback_context(context: Dict) -> bool:
        error_message: Optional[str] = None
        if 'dag' not in context or 'run_id' not in context or 'dag_run' not in context:
            error_message = 'dag, run_id and dag_run are expected'
        else:
            dag_run: DagRun = context['dag_run']
            if not dag_run.end_date:
                error_message = 'no dag_run.end_date set, it looks like the dag is still running'
            elif 'reason' not in context:
                error_message = 'no reason set, it looks like the dag is still running'

        if error_message:
            logger.error(f'Invalid context received in MCD dag callback: {error_message}. '
                         'Please check your callbacks are configured properly.')
            return False
        return True

    @classmethod
    def mcd_post_task_result(cls, context: Dict):
        if 'dag' not in context or 'run_id' not in context or 'task_instance' not in context:
            logger.error('Invalid context received in MCD task callback: dag, run_id and task_instance are expected')
            return

        dag = context['dag']
        dag_tags = [tag for tag in dag.tags]
        ti = context['task_instance']
        
        exception_message = truncate_string(
            str(context['exception']),
            _EXCEPTION_MSG_LIMIT,
        ) if 'exception' in context else None
        task_instance_result = cls._get_task_instance_result(ti, exception_message)

        result = DagTaskResult(
            dag_id=dag.dag_id,
            run_id=context['run_id'],
            success=task_instance_result.state in _SUCCESS_STATES,
            task=task_instance_result,
            tags=dag_tags,
        )
        cls._get_events_client(dag).upload_task_result(result)

    @classmethod
    def mcd_post_sla_misses(cls, dag: DAG, sla_misses: List):
        # Do nothing we are removing the support for SLA Miss
        return 

    @classmethod
    def _get_task_instance_result(
            cls,
            ti: TaskInstance,
            exception_message: Optional[str] = None
    ) -> DagTaskInstanceResult:
        # Check Airflow version once for all compatibility handling
        if airflow_major_version() >= 3:
            # In Airflow 3, RuntimeTaskInstance doesn't have prev_attempted_tries
            # Use try_number - 1 as a reasonable approximation
            prev_attempted_tries = getattr(ti, 'try_number', 1) - 1
            date_now = datetime.now(tz=timezone.utc)
            
            # In Airflow 3, RuntimeTaskInstance doesn't have duration attribute
            # Calculate duration from start_date and end_date if available
            # This is being fixed in this PR: 
            # https://github.com/apache/airflow/pull/52729
            duration = 0
            # Get start_date and end_date for duration calculation
            start_date = getattr(ti, 'start_date', None)
            end_date = getattr(ti, 'end_date', date_now)
            
            if getattr(ti, 'duration', None) is not None and ti.duration > 0:
                duration = ti.duration
            elif start_date and end_date:
                duration = (end_date - start_date).total_seconds()
            # In Airflow 3, RuntimeTaskInstance might not have execution_date
            # Use start_date as a fallback, or current time if start_date is not available
            execution_date = (
                getattr(ti, 'execution_date', None) or
                getattr(ti, 'logical_date', None) or
                start_date or
                date_now
            )
        else:
            # In Airflow 1 and 2, all attributes are available
            prev_attempted_tries = ti.prev_attempted_tries
            duration = ti.duration or 0
            execution_date = ti.execution_date
            start_date = ti.start_date
            end_date = ti.end_date
            
        return DagTaskInstanceResult(
            task_id=ti.task_id,
            state=ti.state,
            log_url=ti.log_url,
            prev_attempted_tries=prev_attempted_tries,
            duration=duration,
            execution_date=cls._get_datetime_isoformat(execution_date),
            start_date=cls._get_datetime_isoformat(start_date),
            end_date=cls._get_datetime_isoformat(end_date),
            next_retry_datetime=cls._get_next_retry_datetime(ti),
            max_tries=ti.max_tries,
            try_number=ti.try_number,
            exception_message=exception_message,
            inlets=cls._get_lineage_list(ti, 'inlets'),
            outlets=cls._get_lineage_list(ti, 'outlets'),
            original_dates=cls._get_original_dates(execution_date, start_date, end_date),
        )

    @staticmethod
    def _get_datetime_isoformat(d: Optional[datetime]) -> str:
        return d.isoformat() if d else datetime.now(tz=timezone.utc).isoformat()

    @staticmethod
    def _get_original_dates(
            execution_date: Optional[datetime],
            start_date: Optional[datetime],
            end_date: Optional[datetime]
    ) -> str:
        return f"execution={str(execution_date)}, start_date={str(start_date)}, end_date={str(end_date)}"

    @staticmethod
    def _get_optional_datetime_isoformat(d: Optional[datetime]) -> Optional[str]:
        return d.isoformat() if d else None

    @classmethod
    def _get_events_client(cls, dag: DAG) -> AirflowEventsClient:
        dag_params = dag.params or {}
        mcd_session_conn_id = _DEFAULT_CONNECTION_ID
        mcd_fallback_conn_id: Optional[str] = _FALLBACK_CONNECTION_ID

        param_value = dag_params.get('mcd_connection_id')
        # in Airflow 2.2.x we're getting a Param object while in Airflow 2.6.x we're getting a string object
        # but we cannot import Param as it was added in Airflow v2 and not present in Airflow v1
        if param_value is not None and hasattr(param_value, "value") and isinstance(param_value.value, str):
            mcd_session_conn_id = param_value.value
        elif param_value is not None and isinstance(param_value, str):
            mcd_session_conn_id = param_value
        elif param_value is not None:  # don't log a warning when the parameter was not specified at all
            logger.warning(f"Ignoring mcd_connection_id parameter value: {param_value}, using {mcd_session_conn_id}")

        if mcd_session_conn_id != _DEFAULT_CONNECTION_ID:
            # don't fallback to the old connection id when the value was specifically set
            mcd_fallback_conn_id = None

        return AirflowEventsClient(
            mcd_session_conn_id=mcd_session_conn_id,
            mcd_fallback_conn_id=mcd_fallback_conn_id,
            call_timeout=_DEFAULT_CALL_TIMEOUT,
        )

    @classmethod
    def _get_next_retry_datetime(cls, ti: TaskInstance) -> Optional[str]:
        if not hasattr(ti, "task") or not ti.task or not ti.end_date:
            return None
        
        # Handle Airflow 3.2 compatibility where RuntimeTaskInstance doesn't have next_retry_datetime method
        if airflow_major_version() >= 3:
            # In Airflow 3, RuntimeTaskInstance doesn't have next_retry_datetime method
            # Return None as we cannot determine the next retry datetime
            return None
        else:
            # In Airflow 1 and 2, use the next_retry_datetime method
            return cls._get_optional_datetime_isoformat(ti.next_retry_datetime())

    @classmethod
    def _get_lineage_dict(cls, o: Any) -> Dict:
        """Convert a lineage object to a dictionary representation.
        
        Handles both dataclass and non-dataclass objects gracefully.
        """
        # Determine the source of attributes based on object type
        if is_dataclass(o):
            attrs = asdict(o)
        elif isinstance(o, dict):
            attrs = o
        elif hasattr(o, '__dict__'):
            attrs = o.__dict__
        else:
            attrs = {'value': str(o)}
        
        # Add type information and return deep copy
        return {**deepcopy(attrs), 'type': str(type(o))}

    @classmethod
    def _get_lineage_list(cls, ti: TaskInstance, attr: str) -> List[Dict]:
        if not hasattr(ti, "task") or not ti.task:
            return []
        lineage_list = getattr(ti.task, attr, None)
        if not lineage_list:
            return []
        return [
            cls._get_lineage_dict(lineage_object) for lineage_object in lineage_list
        ]
