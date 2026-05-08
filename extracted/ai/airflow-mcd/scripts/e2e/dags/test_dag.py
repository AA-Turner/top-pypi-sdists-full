"""
E2E test DAG for airflow-mcd.

Runs a single Python task that succeeds.  The dag_callbacks and task_callbacks
from airflow-mcd fire on completion and send the DAG/task result to the mock
Monte Carlo server, which captures the Airflow version from the env payload.
"""

from __future__ import annotations

import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow_mcd.callbacks import mcd_callbacks

with DAG(
    dag_id="e2e_test_dag",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule=None,  # manual trigger only
    catchup=False,
    tags=["e2e", "mcd-test"],
    default_args={**mcd_callbacks.task_callbacks},
    **mcd_callbacks.dag_callbacks,
) as dag:

    def _run():
        import airflow
        print(f"Hello from e2e_test_dag!  Airflow version: {airflow.__version__}")

    PythonOperator(
        task_id="hello",
        python_callable=_run,
    )
