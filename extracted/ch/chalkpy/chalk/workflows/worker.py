"""Serve the `@workflow`s and `@task`s defined in one Python file from a task queue.

    python -m chalk.workflows.worker [--task-queue <queue>] path/to/workflows.py

This is the process a self-hosted workflow worker runs, such as the scaling group that
`chalkcompute.deploy_workflow_worker` deploys. Connection details come from the
CHALK_WORKFLOW_ORCHESTRATOR_* environment variables (address, namespace, and whether to
skip TLS), which is how in-cluster workers reach the orchestrator directly; the task queue
defaults to CHALK_WORKFLOW_ORCHESTRATOR_TASK_QUEUE.

The file is imported under its own stem as the module name, never as `__main__`, so its
`if __name__ == "__main__":` block -- typically the code that deployed this worker and
started the workflow -- does not run again inside the worker.
"""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import logging
import os
import signal
import sys
from collections.abc import Sequence

from chalk.workflows._definitions import TASK_REGISTRY, WORKFLOW_REGISTRY
from chalk.workflows._remote import _TASK_QUEUE_ENV_VAR  # pyright: ignore[reportPrivateUsage]

_logger = logging.getLogger(__name__)


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


async def run_worker(task_queue: str) -> None:
    """Poll `task_queue` with every registered workflow and task until SIGTERM or SIGINT."""
    from chalk.workflows._remote import resolve_connection_info
    from chalk.workflows._temporal import connect_workflow_orchestrator, create_worker

    info = resolve_connection_info(api_server=None, bearer_token=None, environment_id=None)
    client = await connect_workflow_orchestrator(
        info.address,
        info.temporal_namespace,
        use_tls=info.use_tls,
        bearer_token=None,
        environment_id=None,
    )
    worker = create_worker(client, task_queue=task_queue)

    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, stop.set)

    _logger.info(
        "Serving %d workflow(s) and %d task(s) on task queue %r at %s",
        len(WORKFLOW_REGISTRY),
        len(TASK_REGISTRY),
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
    args = parser.parse_args(argv)
    if not args.task_queue:
        parser.error(f"--task-queue is required when {_TASK_QUEUE_ENV_VAR} is not set")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    load_workflow_source(args.source)
    if not WORKFLOW_REGISTRY:
        raise SystemExit(f"{args.source} defines no @workflow; nothing to serve")
    asyncio.run(run_worker(args.task_queue))


if __name__ == "__main__":
    main()
