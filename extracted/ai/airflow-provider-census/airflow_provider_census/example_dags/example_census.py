from airflow_provider_census.operators.census import CensusOperator
from airflow_provider_census.sensors.census import CensusSensor

from airflow import DAG
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.today() - timedelta(days=1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('census', max_active_runs=1, default_args=default_args)

sync = CensusOperator(
    task_id='sync',
    census_conn_id='census_default',
    sync_id=4895,
    dag=dag,
)

sensor = CensusSensor(
    task_id='sensor',
    sync_run_id="{{ ti.xcom_pull(task_ids = 'sync') }}",
    census_conn_id='census_default',
    dag=dag,
)

sync >> sensor
