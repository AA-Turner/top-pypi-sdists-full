"""
Monte Carlo callbacks module.

You can use the provided helper dictionaries to install MC callbacks, for example
for dags, you can use `dag_callbacks` to install MC callbacks:
::
    from airflow_mcd.callbacks import mcd_callbacks

    dag = DAG(
        'name',
        **mcd_callbacks.dag_callbacks,
    )


For tasks, you can use `task_callbacks` to install MC callbacks in all your tasks using `default_args`:
::
    dag = DAG(
        'name',
        default_args={
            **mcd_callbacks.task_callbacks,
        }
    )

You can also install callbacks on a per-task basis:
::
    task = BashOperator(
        task_id='print_date',
        bash_command='command',
        dag=dag,
        **mcd_callbacks.task_callbacks,
    )

If you have your own callbacks, you can call MC callbacks manually from your code:
::
    def dag_success_alert(context):
        #processing code

        #invoke MC event processing
        mcd_callbacks.mcd_dag_success_callback(context)

Configuring the connection to Monte Carlo: you need to create an HTTP connection in Airflow with name
`mcd_default_session` and the following attributes:

* login: your mcd_id value
* password: your mcd_token value
* or using extra attributes: {"mcd_id": "ID", "mcd_token": "Token"}

If you set the connection name to something that is not the default value ("mcd_default_session")
you need to specify the connection name as a DAG parameter with name `mcd_session_conn_id`, like:
::
    dag = DAG(
        'name',
        params={'mcd_connection_id': 'my_connection_id'}
        **mcd_callbacks.dag_callbacks,
    )
"""

import logging
from typing import Dict

from airflow_mcd.callbacks.utils import AirflowEventsClientUtils

logger = logging.getLogger(__name__)


def mcd_dag_success_callback(context: Dict):
    """
    Callback function that sends the DAG success event to Monte Carlo, it must be configured as
    `on_success_callback` in a DAG object.
    You can also manually invoke this function from your own callback code passing the same context you received.
    :param context: The Airflow DAG success context.
    """
    try:
        AirflowEventsClientUtils.mcd_post_dag_result(context)
    except Exception as ex:
        logger.exception(f'Failed to post dag result to MCD: {ex}')


def mcd_dag_failure_callback(context: Dict):
    """
    Callback function that sends the DAG failure event to Monte Carlo, it must be configured as
    `on_failure_callback` in a DAG object.
    You can also manually invoke this function from your own callback code passing the same context you received.
    :param context: The Airflow DAG failure context.
    """
    try:
        AirflowEventsClientUtils.mcd_post_dag_result(context)
    except Exception as ex:
        logger.exception(f'Failed to post dag failure result to MCD: {ex}')


def mcd_task_success_callback(context: Dict):
    """
    Callback function that sends the Task success event to Monte Carlo, it must be configured as
    `on_success_callback` in a Task object.
    You can also manually invoke this function from your own callback code passing the same context you received.
    :param context: The Airflow Task success context.
    """
    try:
        AirflowEventsClientUtils.mcd_post_task_result(context)
    except Exception as ex:
        logger.exception(f'Failed to post task result to MCD: {ex}')


def mcd_task_execute_callback(context: Dict):
    """
    Callback function that sends the Task execution event to Monte Carlo, it must be configured as
    `on_execute_callback` in a Task object.
    You can also manually invoke this function from your own callback code passing the same context you received.
    :param context: The Airflow Task execution context.
    """
    try:
        AirflowEventsClientUtils.mcd_post_task_result(context)
    except Exception as ex:
        logger.exception(f'Failed to post task result to MCD: {ex}')


def mcd_task_failure_callback(context: Dict):
    """
    Callback function that sends the Task failure event to Monte Carlo, it must be configured as
    `on_failure_callback` in a Task object.
    You can also manually invoke this function from your own callback code passing the same context you received.
    :param context: The Airflow Task failure context.
    """
    try:
        AirflowEventsClientUtils.mcd_post_task_result(context)
    except Exception as ex:
        logger.exception(f'Failed to post task failure result to MCD: {ex}')


def mcd_task_retry_callback(context: Dict):
    """
    Callback function that sends the Task retry event to Monte Carlo, it must be configured as
    `on_retry_callback` in a Task object.
    You can also manually invoke this function from your own callback code passing the same context you received.
    :param context: The Airflow Task retry context.
    """
    try:
        AirflowEventsClientUtils.mcd_post_task_result(context)
    except Exception as ex:
        logger.exception(f'Failed to post task retry result to MCD: {ex}')


def mcd_sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    """
    Callback function that sends the SLA misses event to Monte Carlo, it must be configured as
    `sla_miss_callback` in a DAG object.
    You can also manually invoke this function from your own callback code passing the same arguments
    you received.
    """
    try:
        AirflowEventsClientUtils.mcd_post_sla_misses(dag=dag, sla_misses=slas)
    except Exception as ex:
        logger.exception(f'Failed to post SLA misses result to MCD: {ex}')


task_callbacks = {
    'on_success_callback': mcd_task_success_callback,
    'on_failure_callback': mcd_task_failure_callback,
    'on_retry_callback': mcd_task_retry_callback,
    'on_execute_callback': mcd_task_execute_callback,
}

dag_callbacks = {
    'on_failure_callback': mcd_dag_failure_callback,
    'on_success_callback': mcd_dag_success_callback,
    'sla_miss_callback': mcd_sla_miss_callback,
}
