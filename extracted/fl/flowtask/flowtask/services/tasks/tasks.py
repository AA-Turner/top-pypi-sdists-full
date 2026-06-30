from typing import Union
import asyncio
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from navconfig.logging import logging
from ...conf import DEBUG
from ...exceptions import (
    NotSupported,
    TaskNotFound,
    TaskFailed,
    FileError,
    FileNotFound,
    DataNotFound,
)


async def launch_task(
    program_slug: str,
    task_id: str,
    loop: asyncio.AbstractEventLoop = None,
    task_uuid: str = None,
    queued: bool = False,
    no_worker: bool = False,
    priority: str = "low",
    userid: Union[int, str] = None,
    executor: str = None,
    executor_config: dict = None,
    **kwargs,
):
    """launch_task.

    Runs (or queues) a Task from Task Monitor using the executor framework.

    Args:
        program_slug: Program (tenant) name.
        task_id: Task name within the program.
        loop: Optional asyncio event loop.
        task_uuid: Unique execution UUID (generated if None).
        queued: If True, use fire-and-forget dispatch mode.
        no_worker: Deprecated. If True, resolve to local executor.
        priority: Queue priority for qworker executor.
        userid: Optional user identifier forwarded to the task.
        executor: Explicit executor name (overrides no_worker/queued).
        executor_config: Optional executor config dict (passed to ExecutorConfig.from_yaml).
        **kwargs: Additional kwargs forwarded to the executor.

    Returns:
        Tuple of (state_or_uuid, action_label, result_dict).
    """
    from flowtask.executors.resolver import resolve_executor, determine_execution_mode
    from flowtask.executors.models import ExecutorConfig
    import uuid as uuid_lib

    result: dict = {}

    if task_uuid is None:
        task_uuid = str(uuid_lib.uuid4())

    # Build a synthetic options object for the resolver
    class _Options:
        pass

    opts = _Options()
    opts.executor = executor
    opts.executor_image = None
    opts.executor_namespace = None
    opts.no_worker = no_worker
    opts.queued = queued

    # Build task definition for resolver (priority as executor config if no_worker/queued)
    if executor_config:
        task_def = {"executor": executor_config}
    elif executor:
        task_def = {"executor": executor}
    elif no_worker:
        task_def = {"executor": "local"}
    elif queued:
        task_def = {"executor": "qworker"}
    else:
        task_def = {}

    task_executor = resolve_executor(task_def, opts)

    logging.info(
        f":::: Launching Task {program_slug}.{task_id} via executor "
        f"'{task_executor.name()}': priority={priority!s}"
    )

    # Determine dispatch mode
    if queued:
        action = "Queued"
        mode = "dispatch"
    elif no_worker:
        action = "Executed"
        mode = "run"
    else:
        action = "Dispatched"
        mode = "run"

    # Build extra kwargs forwarded to the executor.
    # NOTE: do NOT forward the live navconfig ``config`` (ENV) object here.
    # The qworker executor cloudpickles the TaskWrapper, and ``config`` holds a
    # live uvloop event loop (Cython type, non-trivial ``__cinit__``, no
    # ``__reduce__``) which is unpicklable. The worker rebuilds its own
    # ``self._env = config`` inside ``Task`` anyway, so the kwarg is never read.
    exec_kwargs = {
        "userid": userid,
        "priority": priority,
        "debug": DEBUG,
        **kwargs,
    }

    try:
        if mode == "dispatch":
            handle = await task_executor.dispatch(
                program_slug, task_id, task_uuid, **exec_kwargs
            )
            result["handle"] = handle.execution_id
            result["executor"] = task_executor.name()
            return (task_uuid, action, result)
        else:
            task_result = await task_executor.run(
                program_slug, task_id, task_uuid, **exec_kwargs
            )
            if task_result.status == "failed":
                raise TaskFailed(
                    f"Task {task_id} failed: {task_result.error}"
                )
            state = task_result.result
            result["stats"] = task_result.stats
            result["result"] = state
            result["executor"] = task_executor.name()
            return (state, action, result)
    except (DataNotFound, NotSupported, TaskNotFound, FileNotFound, FileError):
        raise
    except TaskFailed:
        raise
    except Exception as exc:
        logging.error(exc)
        raise TaskFailed(f"Error: Task {task_id} failed: {exc}") from exc
