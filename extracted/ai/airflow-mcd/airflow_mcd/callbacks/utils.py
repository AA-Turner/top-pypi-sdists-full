import logging
from copy import deepcopy

from pycarlo.common.utils import truncate_string
from airflow.models import TaskInstance, SlaMiss, DagRun, DAG
from attr import asdict
from datetime import datetime, timezone

from airflow_mcd.callbacks.client import DagResult, DagTaskResult, AirflowEventsClient, DagTaskInstanceResult, \
    SlaMissesResult, TaskSlaMiss
from typing import Dict, List, Any, Optional


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
        if not cls._validate_dag_callback_context(context=context):
            return

        dag: DAG = context['dag']
        dag_run: DagRun = context['dag_run']
        dag_tags = [tag for tag in dag.tags]
        task_instances = dag_run.get_task_instances()
        result = DagResult(
            dag_id=dag.dag_id,
            run_id=context['run_id'],
            success=dag_run.state in _SUCCESS_STATES,
            reason=context['reason'],
            tasks=[cls._get_task_instance_result(ti) for ti in task_instances],
            state=dag_run.state,
            execution_date=cls._get_datetime_isoformat(dag_run.execution_date),
            start_date=cls._get_datetime_isoformat(dag_run.start_date),
            end_date=cls._get_datetime_isoformat(dag_run.end_date),
            original_dates=cls._get_original_dates(dag_run.execution_date, dag_run.start_date, dag_run.end_date),
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
    def mcd_post_sla_misses(cls, dag: DAG, sla_misses: List[SlaMiss]):
        result = SlaMissesResult(
            dag_id=dag.dag_id,
            sla_misses=[
                TaskSlaMiss(
                    task_id=sla_miss.task_id,
                    execution_date=cls._get_datetime_isoformat(sla_miss.execution_date),
                    timestamp=cls._get_datetime_isoformat(sla_miss.timestamp),
                ) for sla_miss in sla_misses
            ]
        )
        cls._get_events_client(dag).upload_sla_misses(result)

    @classmethod
    def _get_task_instance_result(
            cls,
            ti: TaskInstance,
            exception_message: Optional[str] = None
    ) -> DagTaskInstanceResult:
        return DagTaskInstanceResult(
            task_id=ti.task_id,
            state=ti.state,
            log_url=ti.log_url,
            prev_attempted_tries=ti.prev_attempted_tries,
            duration=ti.duration or 0,
            execution_date=cls._get_datetime_isoformat(ti.execution_date),
            start_date=cls._get_datetime_isoformat(ti.start_date),
            end_date=cls._get_datetime_isoformat(ti.end_date),
            next_retry_datetime=cls._get_next_retry_datetime(ti),
            max_tries=ti.max_tries,
            try_number=ti.try_number,
            exception_message=exception_message,
            inlets=cls._get_lineage_list(ti, 'inlets'),
            outlets=cls._get_lineage_list(ti, 'outlets'),
            original_dates=cls._get_original_dates(ti.execution_date, ti.start_date, ti.end_date),
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
        if hasattr(param_value, "value") and isinstance(param_value.value, str):
            mcd_session_conn_id = param_value.value
        elif isinstance(param_value, str):
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
        return cls._get_optional_datetime_isoformat(ti.next_retry_datetime())

    @classmethod
    def _get_lineage_dict(cls, o: Any) -> Dict:
        attrs = deepcopy(asdict(o))
        attrs['type'] = str(type(o))
        return attrs

    @classmethod
    def _get_lineage_list(cls, ti: TaskInstance, attr: str) -> Optional[List[Dict]]:
        if not hasattr(ti, "task") or not ti.task:
            return None
        lineage_list = getattr(ti.task, attr)
        if not lineage_list:
            return None
        return [
            cls._get_lineage_dict(lineage_object) for lineage_object in lineage_list
        ]
