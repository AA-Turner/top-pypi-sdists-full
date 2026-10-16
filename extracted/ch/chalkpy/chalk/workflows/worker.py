"""Serve the `@workflow`s and `@task`s defined in one Python file from a task queue.

    python -m chalk.workflows.worker [--task-queue <queue>] path/to/workflows.py

This is the process a self-hosted workflow worker runs, such as the scaling group that
`chalkcompute.deploy_workflow_worker` deploys. Connection details come from the
CHALK_WORKFLOW_ORCHESTRATOR_* environment variables (address, namespace, and whether to
skip TLS), which is how in-cluster workers reach the orchestrator directly; the task queue
defaults to CHALK_WORKFLOW_ORCHESTRATOR_TASK_QUEUE.

Tasks with an image of their own are served by a separate worker per image:

    python -m chalk.workflows.worker --tasks embed,rerank path/to/workflows.py

serves only those tasks, and CHALK_WORKFLOW_TASK_QUEUES (a JSON object of task name to
task queue) tells the worker running the workflows where to send each of them.

The file is imported under its own stem as the module name, never as `__main__`, so its
`if __name__ == "__main__":` block -- typically the code that deployed this worker and
started the workflow -- does not run again inside the worker.
"""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import logging
import os
import signal
import sys
from collections.abc import Mapping, Sequence
from typing import Any

from chalk.workflows._definitions import TASK_REGISTRY, WORKFLOW_REGISTRY, TaskDefinition, WorkflowDefinition
from chalk.workflows._remote import _TASK_QUEUE_ENV_VAR  # pyright: ignore[reportPrivateUsage]

_logger = logging.getLogger(__name__)

_TASK_QUEUES_ENV_VAR = "CHALK_WORKFLOW_TASK_QUEUES"


def load_workflow_source(path: str) -> str:
    """Import the file at `path` so its `@workflow`/`@task` decorators register.

    Returns the module name the file was imported under.
    """
    path = os.path.abspath(path)
    module_name = os.path.splitext(os.path.basename(path))[0]
    if module_name == "__main__" or not module_name.isidentifier():
        raise ValueError(f"Cannot import {path!r} as a module: {module_name!r} is not a usable module name")
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Cannot import {path!r}: not a Python source file")
    # Sibling modules next to the file must be importable, as they are under `python <file>`.
    sys.path.insert(0, os.path.dirname(path))
    module = importlib.util.module_from_spec(spec)
    # Registered before execution so the module can be found by name while it runs, as
    # importlib does for a regular import.
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module_name


def route_tasks(routes: Mapping[str, str]) -> None:
    """Send each named task to the worker polling its queue, instead of running it here.

    A route to a task this file no longer defines is skipped with a warning: it is left
    over from a deploy that did not finish, and crashing on it would leave the worker
    down until the next full deploy.
    """
    unknown = sorted(set(routes) - set(TASK_REGISTRY))
    if unknown:
        _logger.warning(
            "%s names tasks that are not defined, ignoring them: %s", _TASK_QUEUES_ENV_VAR, ", ".join(unknown)
        )
    for name, task_queue in routes.items():
        if name in TASK_REGISTRY:
            TASK_REGISTRY[name].task_queue = task_queue


def _task_routes_from_env() -> dict[str, str]:
    raw = os.getenv(_TASK_QUEUES_ENV_VAR)
    if not raw:
        return {}
    routes = json.loads(raw)
    if not isinstance(routes, dict) or not all(
        isinstance(k, str) and isinstance(v, str) and v
        for k, v in routes.items()  # pyright: ignore[reportUnknownVariableType]
    ):
        raise ValueError(f"{_TASK_QUEUES_ENV_VAR} must be a JSON object of task name to task queue")
    return routes  # pyright: ignore[reportUnknownVariableType]


def worker_definitions(
    serve_tasks: Sequence[str] | None,
) -> tuple[list[WorkflowDefinition[Any, Any]], list[TaskDefinition[Any, Any]], list[TaskDefinition[Any, Any]]]:
    """The workflows, activities, and task runners a worker registers.

    With `serve_tasks`, the worker serves only those tasks, each behind the child workflow
    that other workers route it to. Otherwise it serves every workflow and every task not
    routed elsewhere.
    """
    if serve_tasks is None:
        return list(WORKFLOW_REGISTRY.values()), [t for t in TASK_REGISTRY.values() if t.task_queue is None], []
    unknown = sorted(set(serve_tasks) - set(TASK_REGISTRY))
    if unknown:
        raise ValueError(f"--tasks names tasks that are not defined: {', '.join(unknown)}")
    tasks = [TASK_REGISTRY[name] for name in serve_tasks]
    return [], tasks, tasks


async def run_worker(task_queue: str, *, serve_tasks: Sequence[str] | None = None) -> None:
    """Poll `task_queue` until SIGTERM or SIGINT, with every registered workflow and task, or
    with only `serve_tasks`."""
    from chalk.workflows._remote import connect_orchestrator, resolve_connection_info, static_authorization
    from chalk.workflows._temporal import create_worker

    workflows, tasks, task_runners = worker_definitions(serve_tasks)
    info = resolve_connection_info(api_server=None, authorization=static_authorization(None), environment_id=None)
    # With CHALK_WORKFLOW_ORCHESTRATOR_TOKEN_FILE set, the token is re-read for as long as this
    # context is open, and the worker's polls pick up each new one.
    async with connect_orchestrator(
        info, api_server=None, authorization=static_authorization(None), environment_id=None
    ) as client:
        worker = create_worker(
            client, task_queue=task_queue, workflows=workflows, tasks=tasks, task_runners=task_runners
        )

        stop = asyncio.Event()
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, stop.set)

        _logger.info(
            "Serving %d workflow(s) and %d task(s) on task queue %r at %s",
            len(workflows),
            len(tasks),
            task_queue,
            info.address,
        )

        async def shut_down_on_signal() -> None:
            await stop.wait()
            # Shutting down stops polling and cancels in-flight activities, which Temporal then
            # retries under each task's retry policy; the workflow itself resumes on whichever
            # replica polls next.
            _logger.info("Shutting down workflow worker")
            await worker.shutdown()

        # `worker.run()` returns once `shutdown()` completes, and raises on a fatal worker error,
        # which gather propagates so the process exits nonzero and the replica is restarted.
        await asyncio.gather(worker.run(), shut_down_on_signal())


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="python -m chalk.workflows.worker",
        description="Serve the workflows and tasks defined in one Python file from a task queue.",
    )
    parser.add_argument("source", help="Python file that defines the workflows and tasks to serve")
    parser.add_argument(
        "--task-queue",
        default=os.getenv(_TASK_QUEUE_ENV_VAR),
        help=f"Orchestrator task queue to poll (default: ${_TASK_QUEUE_ENV_VAR})",
    )
    parser.add_argument(
        "--tasks",
        help="Comma-separated tasks to serve, alone, for the workers that route them here",
    )
    args = parser.parse_args(argv)
    if not args.task_queue:
        parser.error(f"--task-queue is required when {_TASK_QUEUE_ENV_VAR} is not set")
    serve_tasks = [t for t in args.tasks.split(",") if t] if args.tasks is not None else None
    if serve_tasks is not None and not serve_tasks:
        parser.error("--tasks must name at least one task")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    load_workflow_source(args.source)
    if serve_tasks is None:
        if not WORKFLOW_REGISTRY:
            raise SystemExit(f"{args.source} defines no @workflow; nothing to serve")
        route_tasks(_task_routes_from_env())
    asyncio.run(run_worker(args.task_queue, serve_tasks=serve_tasks))


if __name__ == "__main__":
    main()
