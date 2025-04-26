"""
Example circuit breaker dag using rule UUIDs from the test.snow dev account.

See README-dev.md for details on how to run locally.
"""

from datetime import datetime, timedelta

from airflow import DAG

try:
    from airflow.operators.bash import BashOperator
except ImportError:
    # For airflow versions <= 2.0.0. This module was deprecated in 2.0.0.
    from airflow.operators.bash_operator import BashOperator

from airflow_mcd.operators import SimpleCircuitBreakerOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
        'sample-dag',
        default_args=default_args,
        start_date=datetime(2022, 2, 8),
        catchup=False,
        schedule_interval=timedelta(1)
) as dag:
    mcd_connection_id = 'mcd_default_session'

    task1 = BashOperator(
        task_id='example_elt_job_1',
        bash_command='echo I am transforming a very important table!',
    )
    breaker1 = SimpleCircuitBreakerOperator(
        task_id='circuit_breaker_1',
        mcd_session_conn_id=mcd_connection_id,
        rule_uuid='58dcbf8a-056f-4d25-9675-0b7f0d08d218'  # A rule that should always breach
    )
    breaker2 = SimpleCircuitBreakerOperator(
        task_id='circuit_breaker_2',
        mcd_session_conn_id=mcd_connection_id,
        rule_name='monitor_as_code_rule_that_should_never_breach',  # A rule that should never breach
        namespace='monitor_as_code_rules'
    )
    breaker3 = SimpleCircuitBreakerOperator(
        task_id='circuit_breaker_3',
        mcd_session_conn_id=mcd_connection_id,
        rule_name='rule_created_in_the_ui_that_should_never_breach',  # A rule that should never breach
    )
    task2 = BashOperator(
        task_id='example_elt_job_2',
        bash_command='echo I am building a very important dashboard from the table created in task1!',
        trigger_rule='none_failed'
    )

    task1 >> [breaker1, breaker2, breaker3] >> task2
