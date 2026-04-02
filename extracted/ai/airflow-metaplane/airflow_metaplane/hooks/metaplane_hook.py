import logging
from datetime import timedelta
import requests
from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook
from cattrs.preconf.json import make_converter


from airflow_metaplane.hooks.models import (
    MPDag,
    MPDagContext,
    MPDagRun,
    MPTask,
    MPTaskInstance,
)

logger = logging.getLogger(__name__)


class MetaplaneHook(BaseHook):
    conn_name_attr = "metaplane_conn_id"
    default_conn_name = "metaplane_default"
    conn_type = "metaplane"
    hook_name = "Metaplane"

    def __init__(self, context) -> None:
        super().__init__()
        metaplane_conn_id = self.default_conn_name
        custom_conn_name = context["dag"].params.get("metaplane_connection_id")
        custom_host = context["dag"].params.get("metaplane_host")
        if custom_conn_name is not None:
            if isinstance(custom_conn_name, str):
                metaplane_conn_id = custom_conn_name
            else:
                logging.warn(
                    f"unrecognized value for custom metaplane connection {custom_conn_name}"
                )

        conn = self.get_connection(metaplane_conn_id)
        self.api_key = conn.password
        self.host = "dev.api.metaplane.dev" if custom_host is None else custom_host
        self.mp_airflow_connection_id = conn.extra_dejson["mp_airflow_connection_id"]
        self.converter = make_converter()
        self.converter.register_unstructure_hook(
            timedelta, lambda v: v.total_seconds() if v else None
        )

        if self.api_key is None:
            raise AirflowException("missing api key")

    def _build_task_instance(self, ti):
        return MPTaskInstance(
            task_id=ti.task_id,
            dag_id=ti.dag_id,
            run_id=ti.run_id,
            start_date=ti.start_date,
            end_date=ti.end_date,
            execution_date=ti.execution_date,
            duration=ti.duration,
            state=ti.state,
            try_number=ti.try_number,
            max_tries=ti.max_tries,
            job_id=ti.job_id,
            operator=ti.operator,
            queued_dttm=ti.queued_dttm,
            queued_by_job_id=ti.queued_by_job_id,
            test_mode=ti.test_mode,
        )

    def _serialize_to_json(self, context):
        dag = context["dag"]
        dag_run = context["dag_run"]
        dag_context = MPDagContext(
            connection_id=self.mp_airflow_connection_id,
            dag=MPDag(
                dag_id=dag.dag_id,
                description=dag.description,
                start_date=dag.start_date,
                end_date=dag.end_date,
                tags=dag.tags,
                tasks=[
                    MPTask(
                        task_id=task.task_id,
                        owner=task.owner,
                        retries=task.retries,
                        retry_delay=task.retry_delay,
                        max_retry_delay=task.max_retry_delay,
                        sla=task.sla,
                        execution_timeout=task.execution_timeout,
                        operator_class=task.operator_class.__name__,
                        upstream_task_ids=task.upstream_task_ids,
                        downstream_task_ids=task.downstream_task_ids,
                    )
                    for task in dag.tasks
                ],
            ),
            dag_run=MPDagRun(
                id=dag_run.id,
                dag_id=dag_run.dag_id,
                queued_at=dag_run.queued_at,
                execution_date=dag_run.execution_date,
                start_date=dag_run.start_date,
                end_date=dag_run.end_date,
                state=dag_run.state,
                run_id=dag_run.run_id,
                external_trigger=dag_run.external_trigger,
                run_type=dag_run.run_type,
                task_instances=[
                    self._build_task_instance(ti) for ti in dag_run.get_task_instances()
                ],
            ),
            task_instance=self._build_task_instance(context["task_instance"]),
            reason=context["reason"] if "reason" in context else None,
            exception=str(context["exception"]) if "exception" in context else None,
            run_id=context["run_id"],
            test_mode=context["test_mode"],
        )
        return self.converter.dumps(dag_context)

    def _post_request(self, path: str, context):
        res = requests.post(
            f"https://{self.host}/{path}",
            data=self._serialize_to_json(context),
            headers={"Authorization": self.api_key, "Content-Type": "application/json"},
            timeout=10,
        )
        res.raise_for_status()
        return res

    def upload_dag_success(self, context):
        self._post_request("airflow/dag-success", context)

    def upload_dag_failure(self, context):
        self._post_request("airflow/dag-failure", context)

    def upload_dag_sla_miss(self, context):
        self._post_request("airflow/dag-sla-miss", context)

    def upload_task_execute(self, context):
        self._post_request("airflow/task-execute", context)

    def upload_task_success(self, context):
        self._post_request("airflow/task-success", context)

    def upload_task_failure(self, context):
        self._post_request("airflow/task-failure", context)

    def upload_task_retry(self, context):
        self._post_request("airflow/task-retry", context)

    @classmethod
    def get_connection_form_widgets(cls):
        """Return connection widgets to add to connection form."""
        from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import StringField

        return {
            "mp_airflow_connection_id": StringField(
                lazy_gettext("Metaplane Airflow connection ID"),
                widget=BS3TextFieldWidget(),
                description="The ID of the Airflow connection created in Metaplane",
            ),
        }

    @classmethod
    def get_ui_field_behaviour(cls):
        """Return custom field behaviour."""
        return {
            "hidden_fields": [
                "schema",
                "host",
                "login",
                "port",
                "extra",
                "description",
            ],
            "relabeling": {"password": "API key"},
        }
