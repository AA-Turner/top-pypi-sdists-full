from __future__ import annotations

import copy
import getpass
import json
import os
import socket
import sys
from typing import TYPE_CHECKING

import psutil

import simpleflow.swf.mapper.exceptions
import simpleflow.swf.mapper.models
import simpleflow.swf.mapper.querysets
from simpleflow.dispatch import dynamic_dispatcher
from simpleflow.utils import json_dumps

from .stats import pretty

if TYPE_CHECKING:
    from simpleflow.swf.mapper.models.workflow import WorkflowExecution


__all__ = [
    "list_workflow_executions",
    "show_workflow_profile",
    "show_workflow_status",
    "swf_identity",
]


def get_workflow_execution(domain_name: str, workflow_id: str, run_id: str | None = None) -> WorkflowExecution | None:
    def filter_execution(*args, **kwargs):
        if "workflow_status" in kwargs:
            kwargs["status"] = kwargs.pop("workflow_status")
        filtered_executions = query.filter(*args, **kwargs)
        return filtered_executions[0] if filtered_executions else None

    domain = simpleflow.swf.mapper.models.Domain(domain_name)
    query = simpleflow.swf.mapper.querysets.WorkflowExecutionQuerySet(domain)

    action = filter_execution
    keywords = {
        "workflow_id": workflow_id,
    }
    if run_id:
        action = query.get
        keywords["run_id"] = run_id

    try:
        workflow_execution = action(**keywords)
    except (simpleflow.swf.mapper.exceptions.DoesNotExistError, IndexError):
        keywords["workflow_status"] = simpleflow.swf.mapper.models.WorkflowExecution.STATUS_CLOSED
        workflow_execution = action(**keywords)

    return workflow_execution


def show_workflow_info(domain_name, workflow_id, run_id=None):
    workflow_execution = get_workflow_execution(
        domain_name,
        workflow_id,
        run_id,
    )
    if not workflow_execution:
        print(f"Execution {workflow_id} {run_id} not found" if run_id else f"Workflow {workflow_id} not found")
        sys.exit(1)
    return pretty.info(workflow_execution)


def show_workflow_profile(domain_name, workflow_id, run_id=None, nb_tasks=None):
    workflow_execution = get_workflow_execution(
        domain_name,
        workflow_id,
        run_id,
    )
    if not workflow_execution:
        print(f"Execution {workflow_id} {run_id} not found" if run_id else f"Workflow {workflow_id} not found")
        sys.exit(1)
    return pretty.profile(workflow_execution, nb_tasks)


def show_workflow_status(domain_name: str, workflow_id: str, run_id: str | None = None, nb_tasks: int | None = None):
    workflow_execution = get_workflow_execution(
        domain_name,
        workflow_id,
        run_id,
    )
    if not workflow_execution:
        print(f"Execution {workflow_id} {run_id} not found" if run_id else f"Workflow {workflow_id} not found")
        sys.exit(1)
    return pretty.status(workflow_execution, nb_tasks)


def list_workflow_executions(domain_name, *args, **kwargs):
    domain = simpleflow.swf.mapper.models.Domain(domain_name)
    query = simpleflow.swf.mapper.querysets.WorkflowExecutionQuerySet(domain)
    executions = query.all(*args, **kwargs)

    return pretty.list_executions(executions)


def filter_workflow_executions(
    domain_name,
    status,
    tag,
    workflow_id,
    workflow_type_name,
    workflow_type_version,
    *args,
    callback=None,
    **kwargs,
):
    domain = simpleflow.swf.mapper.models.Domain(domain_name)
    query = simpleflow.swf.mapper.querysets.WorkflowExecutionQuerySet(domain)
    executions = query.filter(
        status,
        tag,
        workflow_id,
        workflow_type_name,
        workflow_type_version,
        *args,
        callback=callback,
        **kwargs,
    )

    return pretty.list_details(executions)


def find_activity(history, scheduled_id=None, activity_id=None, input=None):
    """
    Finds an activity in a given workflow execution and returns a callable,
    some args and some kwargs so we can re-execute it.

    :type history: simpleflow.history.History
    :type scheduled_id: str
    :type activity_id: str
    :type input: Optional[dict[str, Any]]
    """
    found_activity = None
    for params in history.activities.values():
        if params["scheduled_id"] == scheduled_id:
            found_activity = params
        if params["id"] == activity_id:
            found_activity = params

    if not found_activity:
        raise ValueError("Couldn't find activity.")

    # get the activity
    activity_str = found_activity["name"]
    dispatcher = dynamic_dispatcher.Dispatcher()
    activity = dispatcher.dispatch_activity(activity_str)

    # get the input
    input_ = input or found_activity["input"]
    if input_ is None:
        input_ = {}
    args = input_.get("args", ())
    kwargs = input_.get("kwargs", {})
    meta = input_.get("meta", {})

    kwargs["context"] = {
        "name": activity_str,
        "version": None,  # not stored in the activity dict
        "activity_id": found_activity["id"],
        "input": copy.deepcopy(input_),
    }

    # return everything
    return activity, args, kwargs, meta, found_activity


def get_task(
    domain_name: str,
    workflow_id: str,
    task_id: str,
    details: bool,
):
    workflow_execution = get_workflow_execution(
        domain_name,
        workflow_id,
    )
    if not workflow_execution:
        print(f"Workflow {workflow_id} not found")
        sys.exit(1)
    return pretty.get_task(workflow_execution, task_id, details)


def swf_identity():
    # basic identity
    pid = os.getpid()
    identity = {
        "user": getpass.getuser(),  # system's user
        "hostname": socket.gethostname(),  # main hostname
        "pid": pid,  # current pid
        "exe": psutil.Process(pid).exe(),  # executable path
    }

    # adapt with extra keys from env
    if "SIMPLEFLOW_IDENTITY" in os.environ:
        try:
            extra_keys = json.loads(os.environ["SIMPLEFLOW_IDENTITY"])
        except Exception:
            extra_keys = {}
        for key, value in extra_keys.items():
            identity[key] = value

    # remove null values
    identity = {k: v for k, v in identity.items() if v is not None}

    # serialize the result
    return json_dumps(identity)
