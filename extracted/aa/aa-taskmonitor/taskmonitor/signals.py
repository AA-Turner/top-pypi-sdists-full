"""Celery signal bindings.

This module is kept intentionally small, since it is difficult to test signals directly.
"""

# pylint: skip-file

from celery import signals

from taskmonitor.core import task_logs


@signals.task_received.connect
def task_received_handler(request=None, **kw):
    task_logs.task_received_handler_2(request)


@signals.task_prerun.connect
def task_prerun_handler(task_id=None, **kw):
    task_logs.task_prerun_handler_2(task_id)


@signals.task_retry.connect
def task_retry_handler(sender=None, request=None, reason=None, **kw):
    task_logs.task_retry_handler_2(sender=sender, request=request, reason=reason)


@signals.task_success.connect
def task_success_handler(sender=None, result=None, **kw):
    task_logs.task_success_handler_2(sender=sender, result=result)


@signals.task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, **kw):
    task_logs.task_failure_handler_2(sender, task_id, exception)


@signals.task_internal_error.connect
def task_internal_error_handler(
    sender=None, task_id=None, request=None, exception=None, **kw
):
    task_logs.task_internal_error_handler_2(sender, task_id, request, exception)
