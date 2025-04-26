import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
from unittest import TestCase
from unittest.mock import create_autospec, patch, ANY

from airflow.models import DagRun, TaskInstance, SlaMiss, DAG, BaseOperator, DagTag
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
        self._test_upload_dag_result(True, mock_client_upload_result, set_dates=True, set_end_date=False)

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

    def test_task_instance_with_no_task(self):
        # simulate a task instance with no task in Airflow >= 2.9.0
        task = create_autospec(BaseOperator)
        task.executor = None
        task.task_id = "1"
        task.queue = "q1"
        task.pool_slots = 1
        task.run_as_user = None
        task.executor_config = {}
        task.retries = 0
        task_instance = TaskInstance(task=task)
        task_instance.task = None
        task_instance.end_date = datetime.utcnow()
        self.assertIsNone(AirflowEventsClientUtils._get_next_retry_datetime(task_instance))
        self.assertIsNone(AirflowEventsClientUtils._get_lineage_list(task_instance, "inlets"))

    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_task_result_success_with_tags(self, mock_client_upload_result):
        tags = ["tag1", "tag2"]
        self._test_upload_task_result("running", mock_client_upload_result, tags=tags)


    @patch("airflow_mcd.callbacks.client.AirflowEventsClient._upload_result")
    def test_upload_sla_misses(self, mock_client_upload_result):
        utils = AirflowEventsClientUtils()

        dag = create_autospec(DAG)
        dag.dag_id = "dag_123"
        dag.params = {}

        sla_miss_1 = create_autospec(SlaMiss)
        sla_miss_1.task_id = "task_123"
        sla_miss_1.execution_date = datetime.now(tz=timezone.utc) - timedelta(seconds=10)
        sla_miss_1.timestamp = datetime.now(tz=timezone.utc)

        sla_miss_2 = create_autospec(SlaMiss)
        sla_miss_2.task_id = "task_234"
        sla_miss_2.execution_date = datetime.now(tz=timezone.utc) - timedelta(seconds=10)
        sla_miss_2.timestamp = datetime.now(tz=timezone.utc)

        sla_misses = [
            sla_miss_1,
            sla_miss_2,
        ]
        utils.mcd_post_sla_misses(dag, sla_misses)

        mock_client_upload_result.assert_called()
        mock_client_upload_result.assert_called_with(
            AirflowEventsClient._UPLOAD_AIRFLOW_SLA_MISSES_OPERATION,
            {
                "dag_id": dag.dag_id,
                "env": self._get_graphql_env(),
                "payload": EqVariable("payload"),
            },
            {
                "event_type": "sla_miss",
                "dag_id": dag.dag_id,
                "env": self._get_env(),
                "sla_misses": [
                    {
                        "task_id": m.task_id,
                        "execution_date": m.execution_date.isoformat(),
                        "timestamp": m.timestamp.isoformat(),
                    }
                    for m in sla_misses
                ]
            }
        )

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
        expected_body = {
            "airflow_operation": AirflowEventsClient._UPLOAD_AIRFLOW_DAG_RESULT_OPERATION,
            "airflow_payload": {
                "dag_id": dag.dag_id,
                "run_id": dag_context["run_id"],
                "success": True,
                "reason": dag_context.get("reason"),
                "state": dag_run.state,
                "execution_date": dag_run.execution_date.isoformat(),
                "start_date": dag_run.start_date.isoformat(),
                "end_date": dag_run.end_date.isoformat(),
                "env": self._get_graphql_env(),
                "tags": [],
                "payload": {
                    "dag_id": dag.dag_id,
                    "env": self._get_env(),
                    "run_id": dag_context["run_id"],
                    "success": True,
                    "tasks": [
                        self._get_dag_task_instance_result(ti, set_dates=True)
                        for ti in task_instances
                    ],
                    "state": dag_run.state,
                    "execution_date": dag_run.execution_date.isoformat(),
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
        now_isoformat = datetime.now(tz=timezone.utc).isoformat()
        if not set_end_date:
            mock_client_upload_result.assert_not_called()
            return
        mock_client_upload_result.assert_called()
        mock_client_upload_result.assert_called_with(
            AirflowEventsClient._UPLOAD_AIRFLOW_DAG_RESULT_OPERATION,
            {
                "dag_id": dag.dag_id,
                "run_id": dag_context["run_id"],
                "success": success,
                "reason": dag_context.get("reason"),
                "state": dag_run.state,
                "execution_date": dag_run.execution_date.isoformat() if set_dates else now_isoformat,
                "start_date": dag_run.start_date.isoformat() if set_dates else now_isoformat,
                "end_date": dag_run.end_date.isoformat() if set_dates else now_isoformat,
                "env": self._get_graphql_env(),
                "payload": EqVariable("payload"),
                "tags": tags,
            },
            {
                "dag_id": dag.dag_id,
                "env": self._get_env(),
                "run_id": dag_context["run_id"],
                "success": success,
                "tasks": [
                    self._get_dag_task_instance_result(ti, set_dates=set_dates) for ti in task_instances
                ],
                "state": dag_run.state,
                "execution_date": dag_run.execution_date.isoformat() if set_dates else now_isoformat,
                "start_date": dag_run.start_date.isoformat() if set_dates else now_isoformat,
                "end_date": dag_run.end_date.isoformat() if set_dates else now_isoformat,
                "reason": dag_context.get("reason"),
                "event_type": "dag",
                "original_dates": ANY,
                "tags": tags,
            }
        )

    def _upload_dag_result(
        self, success: bool, set_dates: bool = True, set_end_date: bool = True, tags: Optional[List[str]] = [],
    ) -> Tuple[Dict, DAG, DagRun, List[TaskInstance]]:
        state = "success" if success else "failed"
        dag_context = self._create_dag_context(state, set_dates=set_dates, set_end_date=set_end_date, tags=tags)
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
        dag = create_autospec(DAG)
        dag.dag_id = "dag_123"
        dag.params = {}
        dag.tags = tags
        dag_run = create_autospec(DagRun)
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

        if set_end_date:
            dag_run.end_date = datetime.now(tz=timezone.utc)
        else:
            dag_run.end_date = None

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
        exception_message: str = (error_message or "task failed") if state == "failed" else None
        if state == "failed":
            dag_context["exception"] = Exception(exception_message)
        dag: DAG = dag_context["dag"]
        dag_run: DagRun = dag_context["dag_run"]
        task_instances: List[TaskInstance] = dag_run.get_task_instances()
        task_instance = task_instances[0]
        task_instance.state = state
        dag_context["task_instance"] = task_instance
        utils = AirflowEventsClientUtils()
        utils.mcd_post_task_result(dag_context)

        now_isoformat = datetime.now(tz=timezone.utc).isoformat()
        expected_graphql_payload = {
            "dag_id": dag.dag_id,
            "run_id": dag_context["run_id"],
            "task_id": task_instance.task_id,
            "success": state == "success",
            "env": self._get_graphql_env(),
            "state": state,
            "log_url": f"http://airflow.com/{dag.dag_id}/{task_instance.task_id}/log",
            "execution_date": task_instance.execution_date.isoformat() if set_dates else now_isoformat,
            'start_date': task_instance.start_date.isoformat() if set_dates else now_isoformat,
            'end_date': task_instance.end_date.isoformat() if set_dates else now_isoformat,
            'duration': task_instance.duration or 0,
            'attempt_number': task_instance.prev_attempted_tries,
            "payload": EqVariable("payload"),
            "tags": tags,
        }
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
                "task": self._get_dag_task_instance_result(
                    task_instance,
                    expected_exception_message,
                    set_dates=set_dates
                ),
                "event_type": "task",
                "tags": tags,
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
        return {
            "task_id": task_instance.task_id,
            "state": task_instance.state,
            "log_url": task_instance.log_url,
            "prev_attempted_tries": task_instance.prev_attempted_tries,
            "duration": task_instance.duration or 0,
            "execution_date": task_instance.execution_date.isoformat() if set_dates else now_isoformat,
            "start_date": task_instance.start_date.isoformat() if set_dates else now_isoformat,
            "end_date": task_instance.end_date.isoformat() if set_dates else now_isoformat,
            "next_retry_datetime": None,
            "max_tries": task_instance.max_tries,
            "try_number": task_instance.try_number,
            "exception_message": exception_message,
            "inlets": [],
            "outlets": [],
            "original_dates": ANY,
        }

