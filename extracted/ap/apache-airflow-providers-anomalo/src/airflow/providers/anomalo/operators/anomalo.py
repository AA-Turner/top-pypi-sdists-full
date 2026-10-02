from datetime import date, timedelta
from typing import Callable, Mapping, Optional

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.providers.anomalo.hooks.anomalo import AnomaloHook


def anomalo_today() -> date:
    return date.today() - timedelta(1)


class AnomaloCheckRunResultOperator(BaseOperator):
    """
    Check the results of the most recent job that ran on a table.

    :param table_name: the full name of the table in Anomalo.
    :param status_checker: A function that takes in a run result and returns True if this check should pass and False otherwise.
    :param job_id: (Optional) The job id of the job to evaluate.
    :param xcom_job_id_task: (Optional) The id of task that wrote the job id to check into xcom.
    :param xcom_job_id_key: (Optional) The xcom key under which the job id was written to.
    :param run_date: (Optional) The run date of the checks to evaluate.
    :param anomalo_conn_id: (Optional) The connection ID used to connect to Anomalo.

    There are three optional ways to specify which checks to evaluate for pass/fail.
    If more than one is specified, only the first will be used in the following order of preference:
      1. job_id
      2. xcom_job_id_task (and optional xcom_job_id_key)
      3. run_date
    If none are specified, defaults to evaluating the current day of checks.
    """

    def __init__(
        self,
        table_name,
        status_checker: Callable[[Mapping], bool],
        job_id=None,
        xcom_job_id_task=None,
        xcom_job_id_key="return_value",
        run_date: Optional[date] = None,
        anomalo_conn_id="anomalo_default",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.anomalo_conn_id = anomalo_conn_id
        self.table_name = table_name
        self.status_checker = status_checker
        self.job_id = job_id
        self.xcom_job_id_task = xcom_job_id_task
        self.xcom_job_id_key = xcom_job_id_key
        self.run_date = run_date

    def execute(self, context):
        self.api_client = AnomaloHook(anomalo_conn_id=self.anomalo_conn_id).get_client()
        my_job_id = (
            self.job_id
            or self._get_job_id_from_xcom(context)
            or self._get_job_id_from_run_date()
        )
        results = self.api_client.get_run_result(job_id=my_job_id)

        if not self.status_checker(results):
            raise AirflowException("Anomolo Job did not pass status check")

        return results

    def _get_job_id_from_xcom(self, context):
        if not self.xcom_job_id_task:
            return None
        job_id = self.xcom_pull(
            context=context, task_ids=self.xcom_job_id_task, key=self.xcom_job_id_key
        )
        return job_id

    def _get_job_id_from_run_date(self):
        run_date = (
            self.run_date.strftime("%Y-%m-%d")
            if self.run_date
            else anomalo_today().strftime("%Y-%m-%d")
        )
        table_id = self.api_client.get_table_information(table_name=self.table_name)[
            "id"
        ]
        job_id = self.api_client.get_check_intervals(
            table_id=table_id, start=run_date, end=None
        )[0]["latest_run_checks_job_id"]
        return job_id


class AnomaloPassFailOperator(AnomaloCheckRunResultOperator):
    """
    Validate whether checks on a given table pass or fail.

    :param table_name: the full name of the table in Anomalo.
    :param must_pass: (Optional) A list of checks that must pass for this task to succeed.
    :param job_id: (Optional) The job id of the job to evaluate.
    :param xcom_job_id_task: (Optional) The id of task that wrote the job id to check into xcom.
    :param xcom_job_id_key: (Optional) The xcom key under which the job id was written to.
    :param run_date: (Optional) The run date of the checks to evaluate.
    :param anomalo_conn_id: (Optional) The connection ID used to connect to Anomalo.

    There are three optional ways to specify which checks to evaluate for pass/fail.
    If more than one is specified, only the first will be used in the following order of preference:
      1. job_id
      2. xcom_job_id_task (and optional xcom_job_id_key)
      3. run_date
    If none are specified, defaults to evaluating the current day of checks.
    """

    def __init__(
        self,
        table_name,
        must_pass,
        job_id=None,
        xcom_job_id_task=None,
        xcom_job_id_key="return_value",
        run_date: date = None,
        anomalo_conn_id="anomalo_default",
        *args,
        **kwargs,
    ):
        self.must_pass = must_pass
        super().__init__(
            table_name=table_name,
            status_checker=self.status_checker,
            job_id=job_id,
            xcom_job_id_task=xcom_job_id_task,
            xcom_job_id_key=xcom_job_id_key,
            run_date=run_date,
            anomalo_conn_id=anomalo_conn_id,
            *args,
            **kwargs,
        )

    def status_checker(self, results: Mapping) -> bool:
        check_runs = results["check_runs"]
        failed_check_types = {
            check_type
            for check_run in check_runs
            if (check_type := check_run["run_config"]["_metadata"]["check_type"])
            in self.must_pass
            and not (check_run["results"]["success"])
        }

        if failed_check_types:
            self.log.error(
                f"check type(s): {', '.join(failed_check_types)} for table {self.table_name} did not pass"
            )
            return False
        else:
            return True


class AnomaloRunCheckOperator(BaseOperator):
    """
    Triggers a job that runs checks on a given table.
    Execution returns the job id of the run.

    :param table_name: the full name of the table in Anomalo.
    :param run_date: (Optional) the day to run the checks on. If not specified, checks will run for the current day.
    :param check_ids: (Optional) the ids of the checks to run. If not specified, all checks will be run, except DataFreshness and DataVolume.
    :param anomalo_conn_id: (Optional) The connection ID used to connect to Anomalo.
    """

    def __init__(
        self,
        table_name,
        run_date: date = None,
        check_ids=None,
        anomalo_conn_id="anomalo_default",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.anomalo_conn_id = anomalo_conn_id
        self.table_name = table_name
        self.run_date = run_date
        self.check_ids = check_ids

    def execute(self, context):
        api_client = AnomaloHook(anomalo_conn_id=self.anomalo_conn_id).get_client()

        run_date_str = (
            self.run_date.strftime("%Y-%m-%d")
            if self.run_date
            else anomalo_today().strftime("%Y-%m-%d")
        )

        table_id = api_client.get_table_information(table_name=self.table_name)["id"]
        run = api_client.run_checks(
            table_id=table_id, interval_id=run_date_str, check_ids=self.check_ids
        )
        self.log.info(f"Triggered Anomalo checks for {self.table_name}")
        return run["run_checks_job_id"]
