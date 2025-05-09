from __future__ import annotations

import json
import os
import platform
import signal
import sys
import time
from contextlib import contextmanager
from datetime import datetime
from typing import TYPE_CHECKING
from urllib.parse import unquote
from uuid import uuid4

import click
import multiprocess

import simpleflow.swf.mapper.exceptions
import simpleflow.swf.mapper.models
import simpleflow.swf.mapper.querysets
from simpleflow import __version__, format, log, logger
from simpleflow.download import download_binaries
from simpleflow.history import History
from simpleflow.settings import print_settings
from simpleflow.swf import helpers
from simpleflow.swf.process import decider, worker
from simpleflow.swf.stats import pretty
from simpleflow.swf.task import ActivityTask
from simpleflow.swf.utils import get_workflow_execution, set_workflow_class_name
from simpleflow.utils import import_from_module, json_dumps, serialize_complex_object
from simpleflow.workflow import Workflow

if TYPE_CHECKING:
    from typing import Any

    from simpleflow.swf.mapper.models.workflow import WorkflowType

TIMESTAMP_FORMATS = [
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%d %H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
]


def comma_separated_list(value: str) -> list[str]:
    """
    Transforms a comma-separated list into a list of strings.
    """
    return value.split(",")


class RunIdParamType(click.ParamType):
    name = "str"

    def convert(self, value: Any, param: click.Parameter | None, ctx: click.Context | None) -> str:
        if "%" not in value:
            return value
        return unquote(value)


RUN_ID = RunIdParamType()


CONTEXT_SETTINGS = dict(help_option_names=["--help", "-h"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("--format", envvar="SIMPLEFLOW_FORMAT")
@click.option("--header/--no-header", default=False)
@click.option(
    "--color",
    type=click.Choice([log.ColorModes.AUTO, log.ColorModes.ALWAYS, log.ColorModes.NEVER]),
    default=log.ColorModes.AUTO,
)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, header: bool, format: str, color: str) -> None:
    if format == "prettyjson":
        format, header = "json", True
        ctx.params["format"] = format
        ctx.params["header"] = header
    log.color_mode = color


def get_workflow_type(domain_name: str, workflow_class: type[Workflow]) -> WorkflowType:
    """
    Get or create the given workflow on SWF.
    :param domain_name:
    :param workflow_class:
    :return:
    """
    domain = simpleflow.swf.mapper.models.Domain(domain_name)
    query = simpleflow.swf.mapper.querysets.WorkflowTypeQuerySet(domain)
    return query.get_or_create(workflow_class.name, workflow_class.version)


def load_input(input_fp):
    if input_fp is None:
        input_fp = sys.stdin
    input = format.decode(input_fp.read())
    return transform_input(input)


def get_input(wf_input):
    if not wf_input:
        wf_input = sys.stdin.read()
    wf_input = format.decode(wf_input)
    return transform_input(wf_input)


def get_or_load_input(input_file, input):
    if input_file:
        return load_input(input_file)
    else:
        return get_input(input)


def transform_input(wf_input):
    if isinstance(wf_input, dict):
        return wf_input
    if isinstance(wf_input, list):
        wf_input = {
            "args": wf_input,
            "kwargs": {},
        }
    else:
        wf_input = {
            "args": [wf_input],
            "kwargs": {},
        }
    return wf_input


def run_workflow_locally(workflow_class, wf_input, middlewares):
    from .local.executor import Executor

    Executor(workflow_class, middlewares=middlewares).run(wf_input)


@click.option("--middleware-pre-execution", required=False, multiple=True)
@click.option("--middleware-post-execution", required=False, multiple=True)
@click.option(
    "--local",
    default=False,
    is_flag=True,
    required=False,
    help="Run the workflow locally without calling Amazon SWF.",
)
@click.option("--input", "-i", required=False, help="JSON input of the workflow.")
@click.option(
    "--input-file",
    required=False,
    type=click.File(),
    help="JSON file with the input of the workflow.",
)
@click.option(
    "--tags",
    type=comma_separated_list,
    required=False,
    help="Tags for the workflow execution.",
)
@click.option("--decision-tasks-timeout", required=False, help="Timeout for the decision tasks.")
@click.option(
    "--execution-timeout",
    required=False,
    help="Timeout for the whole workflow execution.",
)
@click.option("--task-list", required=False, help="Task list for decision tasks.")
@click.option("--workflow-id", required=False, help="ID of the workflow execution.")
@click.option("--domain", "-d", envvar="SWF_DOMAIN", required=False, help="Amazon SWF Domain.")
@click.argument("workflow")
@cli.command("workflow.start", help="Start the workflow defined in the WORKFLOW module.")
def start_workflow(
    workflow: str,
    domain: str | None,
    workflow_id: str | None,
    task_list: str | None,
    execution_timeout: str | None,
    tags: str | None,
    decision_tasks_timeout: str | None,
    input: str | None,
    input_file: str | None,
    local: bool,
    middleware_pre_execution: str | None,
    middleware_post_execution: str | None,
):
    workflow_class = import_from_module(workflow)

    wf_input: dict[str, Any] = {}
    if input or input_file:
        wf_input = get_or_load_input(input_file, input)

    if local:
        middlewares = {
            "pre": middleware_pre_execution,
            "post": middleware_post_execution,
        }
        run_workflow_locally(workflow_class, wf_input, middlewares)
        return

    if not domain:
        raise ValueError("*domain* must be set when not running in local mode")

    if middleware_pre_execution or middleware_post_execution:
        raise ValueError("middlewares can only be set in local mode")

    workflow_type = get_workflow_type(domain, workflow_class)
    set_workflow_class_name(wf_input, workflow_class)
    execution = workflow_type.start_execution(
        workflow_id=workflow_id,
        task_list=task_list or workflow_class.task_list,
        execution_timeout=execution_timeout,
        input=wf_input,
        tag_list=tags,
        decision_tasks_timeout=decision_tasks_timeout,
    )
    print(f"{execution.workflow_id} {execution.run_id}")
    return execution


@click.argument("run_id", type=RUN_ID, required=False)
@click.argument("workflow_id")
@click.argument(
    "domain",
    envvar="SWF_DOMAIN",
)
@cli.command(
    "workflow.terminate",
    help="Workflow associated with WORKFLOW and optionally RUN_ID.",
)
def terminate_workflow(
    domain: str,
    workflow_id: str,
    run_id: str | None,
):
    ex = helpers.get_workflow_execution(domain, workflow_id, run_id)
    if not ex:
        print(f"Execution {workflow_id} {run_id} not found" if run_id else f"Workflow {workflow_id} not found")
        sys.exit(1)
    ex.terminate()


@click.argument("run_id", type=RUN_ID, required=False)
@click.argument("workflow_id")
@click.argument(
    "domain",
    envvar="SWF_DOMAIN",
)
@cli.command(
    "workflow.restart",
    help="Workflow associated with WORKFLOW_ID and optionally RUN_ID.",
)
def restart_workflow(domain: str, workflow_id: str, run_id: str | None):
    ex = helpers.get_workflow_execution(domain, workflow_id, run_id)
    if not ex:
        print(f"Execution {workflow_id} {run_id} not found" if run_id else f"Workflow {workflow_id} not found")
        sys.exit(1)
    history = ex.history()
    ex.terminate(reason="workflow.restart")
    new_ex = ex.workflow_type.start_execution(
        ex.workflow_id,
        task_list=ex.task_list,
        execution_timeout=ex.execution_timeout,
        input=history.events[0].input,
        tag_list=ex.tag_list,
        decision_tasks_timeout=ex.decision_tasks_timeout,
    )
    print(f"{new_ex.workflow_id} {new_ex.run_id}")


def with_format(ctx):
    return pretty.formatted(
        with_header=ctx.parent.params["header"],
        fmt=ctx.parent.params["format"] or pretty.DEFAULT_FORMAT,
    )


@click.argument("run_id", type=RUN_ID, required=False)
@click.argument("workflow_id")
@click.argument(
    "domain",
    envvar="SWF_DOMAIN",
)
@cli.command("workflow.info", help="Info about a workflow execution.")
@click.pass_context
def workflow_info(ctx, domain: str, workflow_id: str, run_id: str | None):
    print(
        with_format(ctx)(helpers.show_workflow_info)(
            domain,
            workflow_id,
            run_id,
        )
    )


@click.option(
    "--nb-tasks",
    "-n",
    default=None,
    type=int,
    help="Maximum number of tasks to display.",
)
@click.argument("run_id", type=RUN_ID, required=False)
@click.argument("workflow_id")
@click.argument(
    "domain",
    envvar="SWF_DOMAIN",
)
@cli.command("workflow.profile", help="Profile of a workflow.")
@click.pass_context
def profile(ctx, domain, workflow_id, run_id, nb_tasks):
    print(
        with_format(ctx)(helpers.show_workflow_profile)(
            domain,
            workflow_id,
            run_id,
            nb_tasks,
        )
    )


# FIXME superseded by history
@click.option(
    "--nb-tasks",
    "-n",
    default=None,
    type=int,
    help="Maximum number of tasks to display.",
)
@click.argument("run_id", type=RUN_ID, required=False)
@click.argument("workflow_id")
@click.argument(
    "domain",
    envvar="SWF_DOMAIN",
)
@cli.command("workflow.tasks", help="Tasks of a workflow execution.")
@click.pass_context
def workflow_tasks(
    ctx,
    domain: str,
    workflow_id: str,
    run_id: str | None,
    nb_tasks: int | None,
) -> None:
    print(
        with_format(ctx)(helpers.show_workflow_status)(
            domain,
            workflow_id,
            run_id,
            nb_tasks,
        )
    )


# FIXME superseded by filter
@click.argument(
    "domain",
    envvar="SWF_DOMAIN",
)
@cli.command("workflow.list", help="Active workflow executions.")
@click.option(
    "--status",
    "-s",
    default="open",
    show_default=True,
    type=click.Choice(["open", "closed"]),
    help="Open/Closed",
)
@click.option("--started-since", "-d", default=30, show_default=True, help="Started since N days.")
@click.pass_context
def list_workflows(ctx, domain: str, status: str, started_since: int):
    print(
        with_format(ctx)(helpers.list_workflow_executions)(
            domain, status=status.upper(), start_oldest_date=started_since
        )
    )


_NOTSET = object()


@cli.command(
    "workflow.history",
    help="Workflow history from workflow WORKFLOW_ID [RUN_ID].",
)
@click.argument("workflow_id")
@click.argument("run_id", type=RUN_ID, required=False)
@click.option(
    "--domain",
    envvar="SWF_DOMAIN",
)
@click.option(
    "--output-format",
    "--of",
    "-o",
    required=False,
    type=click.Choice(["events", "raw", "cooked"]),
    default="raw",
    help="Output format.",
)
@click.option("--reverse-order", required=False, type=bool, default=False, help="Reverse order.")
@click.pass_context
def workflow_history(
    ctx,
    domain: str,
    workflow_id: str,
    run_id: str | None,
    output_format: str,
    reverse_order: bool = False,
) -> None:
    if ctx.parent.params["format"] != "json" or not ctx.parent.params["header"]:
        raise NotImplementedError("Only pretty JSON mode is implemented")

    from simpleflow.swf.mapper.models.history.base import History as BaseHistory

    ex = helpers.get_workflow_execution(domain, workflow_id, run_id)
    if not ex:
        print(f"Execution {workflow_id} {run_id} not found" if run_id else f"Workflow {workflow_id} not found")
        sys.exit(1)
    events = ex.history_events(
        callback=get_progression_callback("events"),
        reverse_order=reverse_order,
    )
    if output_format == "events":
        pass
    else:
        raw_history = BaseHistory.from_event_list(events)
        history = History(raw_history)
        if output_format == "raw":
            events = []
            for event in history.events[:10]:
                e = {}
                for k in ["id", "type", "state", "timestamp", "input", "control", *event.__dict__]:
                    if k.startswith("_") or k == "raw":
                        continue
                    v = getattr(event, k, _NOTSET)
                    if v is _NOTSET:
                        continue
                    e[k] = v
                events.append(e)
        elif output_format == "cooked":
            history.parse()
            events = {
                "workflow": history.workflow,
                "activities": history.activities,
                "child_workflows": history.child_workflows,
                "markers": history.markers,
                "timers": history.timers,
                "signals": history.signals,
                "signal_lists": history.signal_lists,
                "external_workflows_signaling": history.external_workflows_signaling,
                "signaled_workflows": history.signaled_workflows,
            }
        else:
            raise NotImplementedError
    print(json.dumps(events, separators=(",", ":"), default=serialize_complex_object))


@click.argument(
    "domain",
    envvar="SWF_DOMAIN",
)
@cli.command("workflow.filter", help="Filter workflow executions.")
@click.option(
    "--status",
    "-s",
    default="open",
    show_default=True,
    type=click.Choice(["open", "closed"]),
    help="Open/Closed",
)
@click.option("--tag", default=None, help="Tags (comma-separated).")  # , multiple=True
@click.option("--workflow-id", default=None, help="Workflow ID.")
@click.option("--workflow-type-name", default=None, help="Workflow Name.")
@click.option("--workflow-type-version", default=None, help="Workflow Version (name needed).")
@click.option(
    "--close-status",
    "-c",
    type=click.Choice(
        [
            case
            for state in ["COMPLETED", "FAILED", "CANCELED", "TERMINATED", "CONTINUED_AS_NEW", "TIMED_OUT"]
            for case in [state, state.lower()]
        ]
    ),
    help="Started since N days.",
)
@click.option("--started-since", "-d", default=30, show_default=True, help="Started since N days.")
@click.option("--from-date", default=None, type=click.DateTime(formats=TIMESTAMP_FORMATS), help="From datetime.")
@click.option("--to-date", default=None, type=click.DateTime(formats=TIMESTAMP_FORMATS), help="To datetime.")
@click.pass_context
def filter_workflows(
    ctx,
    domain: str,
    status: str,
    tag: str | None,
    workflow_id: str | None,
    workflow_type_name: str | None,
    workflow_type_version: str | None,
    close_status: str | None,
    started_since: int | None,
    from_date: datetime | None,
    to_date: datetime | None,
):
    status = status.upper()
    kwargs: dict[str, Any] = {}
    if status == simpleflow.swf.mapper.models.workflow.WorkflowExecution.STATUS_OPEN:
        if from_date:
            kwargs["oldest_date"] = from_date
            kwargs["latest_date"] = to_date
        else:
            kwargs["oldest_date"] = started_since
    else:
        if from_date:
            kwargs["start_oldest_date"] = from_date
            kwargs["start_latest_date"] = to_date
        else:
            kwargs["start_oldest_date"] = started_since

    if close_status and status != simpleflow.swf.mapper.models.workflow.WorkflowExecution.STATUS_CLOSED:
        raise Exception("Closed status not supported for non-closed workflows.")
    elif close_status:
        kwargs["close_status"] = close_status.upper()

    print(
        with_format(ctx)(helpers.filter_workflow_executions)(
            domain,
            status=status.upper(),
            tag=tag,
            workflow_id=workflow_id,
            workflow_type_name=workflow_type_name,
            workflow_type_version=workflow_type_version,
            callback=get_progression_callback("executionInfos"),
            **kwargs,
        )
    )


def get_progression_callback(key: str):
    if os.isatty(sys.stderr.fileno()):
        spin_marks = ["⠏", "⠛", "⠹", "⠼", "⠶", "⠧"]  # from Google's googlecloudsdk.core
        success = f"{log.GREEN}✓{log.END}" if log.color_mode != log.ColorModes.NEVER else "✓"

        class Counter:
            def __init__(self):
                self.total = 0

        counter = Counter()

        def cb(*_args, loop_number: int, response: dict[str, Any] | None, **_kwargs):
            if response:
                executions = len(response.get(key, []))
                print(f"\r{spin_marks[loop_number % len(spin_marks)]} {counter.total}", file=sys.stderr, end="")
                counter.total += executions
            else:
                print(f"\r{success} {counter.total}", file=sys.stderr)
    else:
        cb = None
    return cb


@click.argument("task_id")
@click.argument("workflow_id")
@click.argument(
    "domain",
    envvar="SWF_DOMAIN",
)
@click.option("--details/--no-details", default=False, help="Display details.")
@cli.command("task.info", help="Information on a task.")
@click.pass_context
def task_info(
    ctx,
    domain: str,
    workflow_id: str,
    task_id: str,
    details: bool,
) -> None:
    print(with_format(ctx)(helpers.get_task)(domain, workflow_id, task_id, details))


@click.option("--nb-processes", "-N", type=int)
@click.option("--log-level", "-l")
@click.option("--task-list", "-t")
@click.option("--domain", "-d", envvar="SWF_DOMAIN", required=True, help="SWF Domain")
@click.argument("workflows", nargs=-1, required=False)
@cli.command("decider.start", help="Start a decider process to manage workflow executions.")
def start_decider(
    workflows: list[str],
    domain: str,
    task_list: str,
    log_level: str,
    nb_processes: int,
) -> None:
    if log_level:
        logger.warning("Deprecated: --log-level will be removed, use LOG_LEVEL environment variable instead")
    decider.command.start(
        workflows,
        domain,
        task_list,
        None,
        nb_processes,
    )


@click.option("--middleware-pre-execution", required=False, multiple=True)
@click.option("--middleware-post-execution", required=False, multiple=True)
@click.option(
    "--poll-data",
    help="Provide a base64 encoded json dump of the SWF poll response, instead of polling SWF",
)
@click.option("--one-task", is_flag=True, help="Run only one task and shut down (no supervisor).")
@click.option(
    "--heartbeat",
    type=int,
    required=False,
    default=60,
    help="Heartbeat interval in seconds (0 to disable heartbeating).",
)
@click.option("--nb-processes", "-N", type=int)
@click.option("--log-level", "-l")
@click.option("--task-list", "-t")
@click.option("--domain", "-d", envvar="SWF_DOMAIN", required=True, help="SWF Domain")
@cli.command("worker.start", help="Start a worker process to handle activity tasks.")
def start_worker(
    domain,
    task_list,
    log_level,
    nb_processes,
    heartbeat,
    one_task,
    poll_data,
    middleware_pre_execution,
    middleware_post_execution,
):
    if log_level:
        logger.warning("Deprecated: --log-level will be removed, use LOG_LEVEL environment variable instead")

    if not task_list and not poll_data:
        raise ValueError("Please provide a --task-list or some data via --poll-data")

    middlewares = {
        "pre": middleware_pre_execution,
        "post": middleware_post_execution,
    }

    worker.command.start(
        domain=domain,
        task_list=task_list,
        middlewares=middlewares,
        nb_processes=nb_processes,
        heartbeat=heartbeat,
        one_task=one_task,
        poll_data=poll_data,
    )


def create_unique_task_list(workflow_id=""):
    task_list_id = "-" + uuid4().hex
    overflow = 256 - len(task_list_id) - len(workflow_id)
    if overflow < 0:
        truncated = workflow_id[:overflow]
        task_list = truncated + task_list_id
    else:
        task_list = workflow_id + task_list_id
    return task_list


@click.option("--middleware-pre-execution", required=False, multiple=True)
@click.option("--middleware-post-execution", required=False, multiple=True)
@click.option(
    "--heartbeat",
    type=int,
    required=False,
    default=60,
    help="Heartbeat interval in seconds (0 to disable heartbeating).",
)
@click.option(
    "--nb-workers",
    "-W",
    type=int,
    required=False,
    help="Number of parallel processes handling activity tasks.",
)
@click.option(
    "--nb-deciders",
    "-D",
    type=int,
    required=False,
    help="Number of parallel processes handling decision tasks.",
)
@click.option("--input", "-i", required=False, help="JSON input of the workflow.")
@click.option(
    "--input-file",
    required=False,
    type=click.File(),
    help="JSON file with the input of the workflow.",
)
@click.option(
    "--tags",
    type=comma_separated_list,
    required=False,
    help="Tags identifying the workflow execution.",
)
@click.option("--decision-tasks-timeout", required=False, help="Decision tasks timeout.")
@click.option(
    "--execution-timeout",
    required=False,
    help="Timeout for the whole workflow execution.",
)
@click.option("--workflow-id", required=False, help="ID of the workflow execution.")
@click.option("--domain", "-d", envvar="SWF_DOMAIN", required=True, help="SWF Domain.")
@click.option("--display-status", type=bool, required=False, help="Display execution status.")
@click.option(
    "--repair",
    type=str,
    required=False,
    help='Repair a failed workflow execution ("<workflow id>" or "<workflow id> <run id>").',
)
@click.option(
    "--force-activities",
    type=str,
    required=False,
    help="Force the re-execution of some activities in when --repair is enabled.",
)
@click.argument("workflow")
@cli.command("standalone", help="Execute a workflow with a single process.")
@click.pass_context
def standalone(
    context,
    workflow,
    domain,
    workflow_id,
    execution_timeout,
    tags,
    decision_tasks_timeout,
    input,
    input_file,
    nb_workers,
    nb_deciders,
    heartbeat,
    display_status,
    repair,
    force_activities,
    middleware_pre_execution,
    middleware_post_execution,
):
    """
    This command spawn a decider and an activity worker to execute a workflow
    with a single main process.

    """
    if force_activities and not repair:
        raise ValueError("You should only use --force-activities with --repair.")

    workflow_class = import_from_module(workflow)
    if not workflow_id:
        workflow_id = workflow_class.name

    wf_input = {}
    if input or input_file:
        wf_input = get_or_load_input(input_file, input)

    if repair:
        repair_run_id = None
        if " " in repair:
            repair, repair_run_id = repair.split(" ", 1)
        # get the previous execution history, it will serve as "default history"
        # for activities that succeeded in the previous execution
        logger.info(
            f"retrieving history of previous execution: domain={domain} workflow_id={repair} run_id={repair_run_id}"
        )
        workflow_execution = get_workflow_execution(domain, repair, run_id=repair_run_id)
        previous_history = History(workflow_execution.history())
        repair_run_id = workflow_execution.run_id
        previous_history.parse()
        # get the previous execution input if none passed
        if not input and not input_file:
            wf_input = previous_history.events[0].input
        if not tags:
            tags = workflow_execution.tag_list
    else:
        previous_history = None
        repair_run_id = None
        if not tags:
            get_tag_list = getattr(workflow_class, "get_tag_list", None)
            if get_tag_list:
                tags = get_tag_list(
                    workflow_class,
                    *wf_input.get("args", ()),
                    **wf_input.get("kwargs", {}),
                )
            else:
                tags = getattr(workflow_class, "tag_list", None)
            if tags == Workflow.INHERIT_TAG_LIST:
                tags = None

    task_list = create_unique_task_list(workflow_id)
    logger.info(f"using task list {task_list}")
    decider_proc = multiprocess.Process(
        target=decider.command.start,
        args=(
            [workflow],
            domain,
            task_list,
        ),
        kwargs={
            "nb_processes": nb_deciders,
            "repair_with": previous_history,
            "force_activities": force_activities,
            "is_standalone": True,
            "repair_workflow_id": repair or None,
            "repair_run_id": repair_run_id,
        },
    )
    decider_proc.start()

    worker_proc = multiprocess.Process(
        target=worker.command.start,
        args=(
            domain,
            task_list,
        ),
        kwargs={
            "nb_processes": nb_workers,
            "heartbeat": heartbeat,
            "middlewares": {
                "pre": middleware_pre_execution,
                "post": middleware_post_execution,
            },
        },
    )
    worker_proc.start()

    print(f"starting workflow {workflow}", file=sys.stderr)
    ex = start_workflow.callback(
        workflow,
        domain,
        workflow_id,
        task_list,
        execution_timeout,
        tags,
        decision_tasks_timeout,
        format.input(wf_input),
        None,
        local=False,
        middleware_pre_execution=None,
        middleware_post_execution=None,
    )
    while True:
        time.sleep(2)
        ex = helpers.get_workflow_execution(
            domain,
            ex.workflow_id,
            ex.run_id,
        )
        if not ex:
            print(
                f"Execution {workflow_id} {ex.run_id} not found" if ex.run_id else f"Workflow {workflow_id} not found"
            )
            sys.exit(1)
        if display_status:
            print(f"status: {ex.status}", file=sys.stderr)
        if ex.status == ex.STATUS_CLOSED:
            print(f"execution {ex.workflow_id} finished", file=sys.stderr)
            break

    os.kill(worker_proc.pid, signal.SIGTERM)
    worker_proc.join()
    os.kill(decider_proc.pid, signal.SIGTERM)
    decider_proc.join()


@click.option("--domain", envvar="SWF_DOMAIN", required=False, help="Amazon SWF Domain.")
@click.option("--workflow-id", required=True, help="ID of the workflow execution.")
@click.option("--input", "-i", required=False, help="JSON input of the workflow.")
@click.option("--run-id", type=RUN_ID, required=False, help="Run ID of the workflow execution.")
@click.option(
    "--scheduled-id",
    required=False,
    type=int,
    help="Event ID when the activity has been scheduled.",
)
@click.option(
    "--activity-id",
    required=False,
    help="Activity ID of the activity you want to replay.",
)
@cli.command("activity.rerun", help="Rerun an activity task locally.")
def activity_rerun(domain, workflow_id, run_id, input, scheduled_id, activity_id):
    # handle params
    if not activity_id and not scheduled_id:
        logger.error("Please supply --scheduled-id or --activity-id.")
        sys.exit(1)

    input_override = None
    if input:
        input_override = format.decode(input)

    # find workflow execution
    try:
        wfe = helpers.get_workflow_execution(domain, workflow_id, run_id)
    except (simpleflow.swf.mapper.exceptions.DoesNotExistError, IndexError):
        logger.error("Couldn't find execution, exiting.")
        sys.exit(1)
    logger.info(f"Found execution: workflowId={wfe.workflow_id} runId={wfe.run_id}")

    # now rerun the specified activity
    history = History(wfe.history())
    history.parse()
    task, args, kwargs, meta, params = helpers.find_activity(
        history,
        scheduled_id=scheduled_id,
        activity_id=activity_id,
        input=input_override,
    )
    kwargs["context"].update(
        {
            "workflow_id": wfe.workflow_id,
            "run_id": wfe.run_id,
        }
    )
    logger.debug("Found activity. Last execution:")
    for line in json_dumps(params, pretty=True).split("\n"):
        logger.debug(line)
    if input_override:
        logger.info("NB: input will be overridden with the passed one!")
    logger.info(f"Will re-run: {task}(*{args}, **{kwargs}) [+meta={meta}]")

    # download binaries if needed
    download_binaries(meta.get("binaries", {}))

    # execute the activity task with the correct arguments
    instance = ActivityTask(task, *args, **kwargs)
    result = instance.execute()
    if hasattr(instance, "post_execute"):
        instance.post_execute()
    logger.info(f"Result (JSON): {json_dumps(result, compact=False)}")


@click.argument(
    "sections",
    required=False,
    default="versions,settings,environment",
    type=comma_separated_list,
)
@cli.command(
    "info",
    help="Display versions, settings, and environment variables. Available sections: versions, settings, environment.",
)
def info(sections):
    @contextmanager
    def section(title):
        print(log.colorize("BLUE", f"# {title}"))
        yield
        print("")

    if "versions" in sections:
        with section("Versions"):
            print(f"simpleflow: {__version__}")
            version = platform.python_version()
            build = platform.python_compiler()
            platform_platform = platform.platform()
            print(f"python_version: {version}")
            print(f"python_build: {build}")
            print(f"platform: {platform_platform}")

    if "settings" in sections:
        with section("Settings"):
            print_settings()

    if "environment" in sections:
        with section("Environment AWS* SIMPLEFLOW*"):
            for key in sorted(os.environ.keys()):
                if not key.startswith("AWS") and not key.startswith("SIMPLEFLOW"):
                    continue
                value = os.environ[key]
                if "SECRET" in key:
                    value = "<redacted>"
                print(f"{key}={value}")


@click.argument("locations", nargs=-1)
@cli.command(
    "binaries.download",
    help="Downloads some binaries with simpleflow.download module. "
    "It expects a list of locations as <binary>=<s3_location> arguments.",
)
def binaries_download(locations):
    pool = multiprocess.Pool(5)
    pool.map(_download_binary, locations)


def _download_binary(spec):
    progname, location = spec.split("=", 2)
    download_binaries({progname: location})
