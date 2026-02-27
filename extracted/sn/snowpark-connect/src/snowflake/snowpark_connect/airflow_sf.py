from datetime import datetime, timedelta, date
import airflow
from airflow import DAG
import sys
sys.path.append('/usr/local/airflow/dags/dnaplatform/')
from platformhelper import call_remote_script

with DAG(
  dag_id = 'ds_fndn_snwpk_ods_core_setup_entity_data_snap',
  default_args = {
    'owner': 'airflow',
    'email': ["arun.vijay@salesforce.com"],
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'email_on_retry': True
  },
  description = 'DAG to execute the Snowpark job from DET MWAA',
  tags=['airflow-fndn-snwpk-poc', 'snowpark'],
  start_date = datetime(2025, 7, 15),
  catchup=False
) as dag:
  ods_core_setup_entity_data_snap = call_remote_script(
    task_id = 'tsk_ods_core_setup_entity_data_snap',
    ssh_conn_id = 'ssh_ora-etlap',
    command = "/home/sfdc_ops/python/bin/python3 /etl/sfdc_ops/edw/src/btdna_foundations/bin/ods_core_setup_entity_data_snap_icb_SPARK.py",
  )