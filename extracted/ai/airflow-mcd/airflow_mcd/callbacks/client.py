import os
import logging

from dataclasses import dataclass, field
from typing import Optional, List, Dict

import requests
from airflow.exceptions import AirflowNotFoundException
from airflow.hooks.base import BaseHook
from dataclasses_json import dataclass_json
from pycarlo.common.retries import ExponentialBackoff
from pycarlo.core import Session, Client, Mutation
from pycarlo.lib.schema import GenericScalar
from requests import HTTPError
from sgqlc.types import Variable, non_null

from airflow_mcd.hooks import SessionHook
from airflow_mcd.hooks.gateway_session_hook import GatewaySessionHook

logger = logging.getLogger(__name__)

_ENV_MAPPINGS = {
    'env_name': [
        'AIRFLOW_ENV_NAME',                     # AWS
        'COMPOSER_ENVIRONMENT',                 # GCP Composer
        'AIRFLOW__WEBSERVER__INSTANCE_NAME',    # Astronomer
    ],
    'env_id': [
        'AIRFLOW_ENV_ID',                       # AWS
        'COMPOSER_GKE_NAME',                    # GCP Composer
        'ASTRO_DEPLOYMENT_ID',                  # Astronomer
    ],
    'version': [
        'AIRFLOW_VERSION',                      # AWS
        'MAJOR_VERSION',                        # GCP Composer
        'ASTRONOMER_RUNTIME_VERSION',           # Astronomer
    ],
    'base_url': [
        'AIRFLOW__WEBSERVER__BASE_URL',         # available in all containers
    ]
}
_INTEGRATION_GATEWAY_PATH = "/airflow/callbacks"


def _get_env_value(key: str, default_value: Optional[str] = None) -> Optional[str]:
    for env_var in _ENV_MAPPINGS[key]:
        value = os.environ.get(env_var)
        if value:
            return value
    return default_value


@dataclass_json
@dataclass
class AirflowEnv:
    # these env vars are used to get additional information about the Airflow
    # environment when running in AWS, GCP or Astronomer.
    env_name: str = ""
    env_id: Optional[str] = None
    version: Optional[str] = None
    base_url: Optional[str] = None

    def __post_init__(self):
        if not self.env_name:
            self.env_name = _get_env_value('env_name', 'airflow')
        if not self.env_id:
            self.env_id = _get_env_value('env_id')
        if not self.version:
            self.version = _get_env_value('version')
        if not self.base_url:
            self.base_url = _get_env_value('base_url')


@dataclass_json
@dataclass
class DagTaskInstanceResult:
    task_id: str
    state: str
    log_url: str
    prev_attempted_tries: int
    duration: float
    execution_date: str
    start_date: str
    end_date: str
    next_retry_datetime: Optional[str]
    max_tries: int
    try_number: int
    exception_message: Optional[str]
    inlets: Optional[List[Dict]]
    outlets: Optional[List[Dict]]
    original_dates: Optional[str]


@dataclass_json
@dataclass
class BaseDagResult:
    dag_id: str
    env: AirflowEnv = field(init=False)

    def __post_init__(self):
        self.env = AirflowEnv()


@dataclass_json
@dataclass
class BaseDagRunResult(BaseDagResult):
    run_id: str
    success: bool


@dataclass_json
@dataclass
class DagResult(BaseDagRunResult):
    tasks: Optional[List[DagTaskInstanceResult]]
    state: str
    execution_date: str
    start_date: str
    end_date: str
    reason: Optional[str]
    event_type: str = 'dag'
    original_dates: Optional[str] = None
    tags: Optional[List[str]] = None


@dataclass_json
@dataclass
class DagTaskResult(BaseDagRunResult):
    task: DagTaskInstanceResult
    event_type: str = 'task'
    tags: Optional[List[str]] = None


@dataclass_json
@dataclass
class TaskSlaMiss:
    task_id: str
    execution_date: str
    timestamp: str


@dataclass_json
@dataclass
class SlaMissesResult(BaseDagResult):
    sla_misses: List[TaskSlaMiss]
    event_type: str = 'sla_miss'


class AirflowEventsClient:
    """
    Client class used to send Airflow related events to Monte Carlo.
    """

    _UPLOAD_AIRFLOW_DAG_RESULT_OPERATION = "upload_airflow_dag_result"
    _UPLOAD_AIRFLOW_TASK_RESULT_OPERATION = "upload_airflow_task_result"
    _UPLOAD_AIRFLOW_SLA_MISSES_OPERATION = "upload_airflow_sla_misses"

    def __init__(self, mcd_session_conn_id: str, call_timeout: int, mcd_fallback_conn_id: Optional[str] = None):
        self.mcd_session_conn_id = mcd_session_conn_id
        self.mcd_fallback_conn_id = mcd_fallback_conn_id
        self.mcd_call_timeout = call_timeout

    def upload_dag_result(self, result: DagResult):
        payload = {
            'dag_id': result.dag_id,
            'run_id': result.run_id,
            'success': result.success,
            'reason': result.reason,
            'state': result.state,
            'execution_date': result.execution_date,
            'start_date': result.start_date,
            'end_date': result.end_date,
            'env': self._env_to_payload(result.env),
            'payload': Variable('payload'),
            'tags': result.tags,
        }
        self._upload_result(self._UPLOAD_AIRFLOW_DAG_RESULT_OPERATION, payload, result.to_dict())

    def upload_task_result(self, result: DagTaskResult):
        payload = {
            'dag_id': result.dag_id,
            'run_id': result.run_id,
            'task_id': result.task.task_id,
            'success': result.success,
            'state': result.task.state,
            'log_url': result.task.log_url,
            'execution_date': result.task.execution_date,
            'start_date': result.task.start_date,
            'end_date': result.task.end_date,
            'duration': result.task.duration,
            'attempt_number': result.task.prev_attempted_tries,
            'env': self._env_to_payload(result.env),
            'payload': Variable('payload'),
            'tags': result.tags,
        }
        if result.task.next_retry_datetime:
            payload['next_retry_date'] = result.task.next_retry_datetime
        if result.task.exception_message:
            payload['exception_message'] = result.task.exception_message
        self._upload_result(self._UPLOAD_AIRFLOW_TASK_RESULT_OPERATION, payload, result.to_dict())

    def upload_sla_misses(self, result: SlaMissesResult):
        payload = {
            'dag_id': result.dag_id,
            'env': self._env_to_payload(result.env),
            'payload': Variable('payload'),
        }
        self._upload_result(self._UPLOAD_AIRFLOW_SLA_MISSES_OPERATION, payload, result.to_dict())

    def _upload_result(self, operation_name: str, operation_parameters: Dict, payload_value: Dict):
        conn_id = self._get_existing_connection_id()
        mc_client = Client(self._get_session(conn_id))
        if mc_client.session_scope:
            self._upload_result_igw(mc_client, operation_name, operation_parameters, payload_value)
        else:
            self._upload_result_gql(mc_client, operation_name, operation_parameters, payload_value)

    def _upload_result_gql(
        self,
        mc_client: Client,
        operation_name: str,
        operation_parameters: Dict,
        payload_value: Dict,
    ):
        try:
            query = Mutation(payload=non_null(GenericScalar))
            attr = getattr(query, operation_name)
            attr(**operation_parameters)
            mc_client(
                query=query,
                variables={'payload': payload_value},
                retry_backoff=ExponentialBackoff(0, 0),  # disable retries
                timeout_in_seconds=self.mcd_call_timeout,
            )
        except Exception as exc:
            logger.exception(f'Failed to upload information to MC: {exc}')

    def _should_retry(self, exc: Exception) -> bool:
        """
        Determines if the exception should be retried.
        We are retrying for:
        - 408: Request Timeout
        - 429: Too Many Requests
        - 5xx: Server errors

        NOTE: For 429 errors we should consider overriding the backoff strategy to avoid
        hammering the server when we are rate limited. We should get the retry-after header
        from the response and use it to delay the next request. But this should be implemented
        in python-sdk (pycarlo) library.
        """
        return isinstance(exc, HTTPError) and (
            exc.response and (exc.response.status_code in [408, 429] or exc.response.status_code >= 500)
        )

    def _upload_result_igw(
        self,
        mc_client: Client,
        operation_name: str,
        operation_parameters: Dict,
        payload_value: Dict,
    ):
        body = {
            "airflow_operation": operation_name,
            "airflow_payload": {**operation_parameters, "payload": payload_value},
        }
        try:
            logger.info(f"Sending MC Callback information to Gateway, operation={operation_name}")
            mc_client.make_request(path=_INTEGRATION_GATEWAY_PATH, body=body, timeout_in_seconds=self.mcd_call_timeout,
                                   should_retry=self._should_retry)
        except HTTPError as exc:
            if exc.response.status_code == 401:
                logger.warning(
                    "MCD Gateway authentication failed, please check you created an "
                    "Airflow Integration Key following the docs at "
                    "https://docs.getmontecarlo.com/docs/airflow-incidents-dags-and-tasks"
                )
            logger.exception(f"Failed to upload information to MCD Gateway: {exc}")
        except Exception as exc:
            logger.exception(f"Failed to upload information to MCD Gateway: {exc}")

    def _get_existing_connection_id(self) -> Optional[str]:
        try:
            BaseHook.get_connection(self.mcd_session_conn_id)
            return self.mcd_session_conn_id
        except AirflowNotFoundException:
            pass

        if self.mcd_fallback_conn_id:
            try:
                BaseHook.get_connection(self.mcd_fallback_conn_id)
                logger.warning(f"Using fallback connection id {self.mcd_fallback_conn_id}, please consider "
                               f"switching to {self.mcd_session_conn_id}.")
                return self.mcd_fallback_conn_id
            except AirflowNotFoundException:
                raise AirflowNotFoundException(f"Connection not found, searched for {self.mcd_session_conn_id} "
                                               f"and {self.mcd_fallback_conn_id}")
        else:
            raise AirflowNotFoundException(f"Connection {self.mcd_session_conn_id} not found")

    @staticmethod
    def _get_session(connection_id: str) -> Session:
        return SessionHook(mcd_session_conn_id=connection_id).get_conn()

    @staticmethod
    def _env_to_payload(env: AirflowEnv) -> Dict:
        values = {
            'env_name': env.env_name,
        }
        if env.env_id:
            values['env_id'] = env.env_id
        if env.base_url:
            values['base_url'] = env.base_url
        if env.version:
            values['version'] = env.version

        return values
