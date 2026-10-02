from airflow.exceptions import AirflowException
from airflow.providers.anomalo.hooks.anomalo import AnomaloHook
from airflow.sensors.base import BaseSensorOperator


class AnomaloJobCompleteSensor(BaseSensorOperator):
    """
    Wait for an Anomalo job to complete. At least one of `job_id` or `xcom_job_id_task` must be specified.

    :param anomalo_conn_id: (Optional) The connection ID used to connect to Anomalo.
    :param job_id: (Optional) The job id of the job to check.
    :param xcom_job_id_task: (Optional) The id of task that wrote the job id to check into xcom.
    :param xcom_job_id_key: (Optional) The xcom key under which the job id was written to.
        Defaults to the return value of the task.
    """

    def __init__(
        self,
        anomalo_conn_id="anomalo_default",
        job_id=None,
        xcom_job_id_task=None,
        xcom_job_id_key="return_value",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if not job_id and not xcom_job_id_task:
            AirflowException(
                "Must include a job_id or a reference to a task to find the job id from"
            )
        self.anomalo_conn_id = anomalo_conn_id
        self.job_id = job_id
        self.xcom_job_id_task = xcom_job_id_task
        self.xcom_job_id_key = xcom_job_id_key

    def poke(self, context):
        api_client = AnomaloHook(anomalo_conn_id=self.anomalo_conn_id).get_client()
        job_id = self.job_id or self.xcom_pull(
            context=context, task_ids=self.xcom_job_id_task, key=self.xcom_job_id_key
        )

        self.log.info(f"checking state of Anomalo job {job_id}")

        run_result = api_client.get_run_result(job_id)

        try:
            next(c for c in run_result["check_runs"] if c["results_pending"])
            self.log.info(f"at least one check still pending for job {job_id}")
            return False
        except StopIteration:
            return True
