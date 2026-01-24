import logging
import traceback
from airflow_metaplane.hooks.metaplane_hook import MetaplaneHook


logger = logging.getLogger(__name__)


def task_execute_callback(context):
    try:
        hook = MetaplaneHook(context)
        hook.upload_task_execute(context)
    except Exception as e:
        logger.warn(
            f"Failed to send callback to Metaplane: {e}\n{traceback.format_exc()}"
        )


def task_success_callback(context):
    try:
        hook = MetaplaneHook(context)
        hook.upload_task_success(context)
    except Exception as e:
        logger.warn(
            f"Failed to send callback to Metaplane: {e}\n{traceback.format_exc()}"
        )


def task_failure_callback(context):
    try:
        hook = MetaplaneHook(context)
        hook.upload_task_failure(context)
    except Exception as e:
        logger.warn(
            f"Failed to send callback to Metaplane: {e}\n{traceback.format_exc()}"
        )


def task_retry_callback(context):
    try:
        hook = MetaplaneHook(context)
        hook.upload_task_retry(context)
    except Exception as e:
        logger.warn(
            f"Failed to send callback to Metaplane: {e}\n{traceback.format_exc()}"
        )


def dag_success_callback(context):
    try:
        hook = MetaplaneHook(context)
        hook.upload_dag_success(context)
    except Exception as e:
        logger.warn(
            f"Failed to send callback to Metaplane: {e}\n{traceback.format_exc()}"
        )


def dag_failure_callback(context):
    try:
        hook = MetaplaneHook(context)
        hook.upload_dag_failure(context)
    except Exception as e:
        logger.warn(
            f"Failed to send callback to Metaplane: {e}\n{traceback.format_exc()}"
        )


def dag_sla_miss_callback(context):
    try:
        hook = MetaplaneHook(context)
        hook.upload_dag_sla_miss(context)
    except Exception as e:
        logger.warn(
            f"Failed to send callback to Metaplane: {e}\n{traceback.format_exc()}"
        )


task_callbacks = {
    "on_execute_callback": task_execute_callback,
    "on_failure_callback": task_failure_callback,
    "on_success_callback": task_success_callback,
    "on_retry_callback": task_retry_callback,
}

dag_callbacks = {
    "on_success_callback": dag_success_callback,
    "on_failure_callback": dag_failure_callback,
    "sla_miss_callback": dag_sla_miss_callback,
}
