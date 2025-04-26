from __future__ import annotations

import logging
import os
from collections import Counter
from contextlib import contextmanager
from typing import Any, Mapping

import jmespath
from rich.progress import Progress
from typing_extensions import Literal

from coiled.utils import COILED_LOGGER_NAME

from ..states import CombinedProcessStateEnum, get_combined_process_state

SCHEDULER_SEARCH = jmespath.compile("scheduler.instance.instance_type_id")
WORKER_SEARCH = jmespath.compile("workers[*].instance")

logger = logging.getLogger(COILED_LOGGER_NAME)


def get_worker_statuses(cluster_details) -> Counter[CombinedProcessStateEnum]:
    """Get worker status from a cluster_details response.

    Returns a Counter of the worker statuses listed in `CombinedProcessStateEnum`.
    """
    worker_statuses: Counter[CombinedProcessStateEnum] = Counter(
        get_combined_process_state(worker) for worker in cluster_details["workers"]
    )
    return worker_statuses


def get_instance_types(cluster_details: Mapping[str, Any]) -> tuple[str | None, Counter[str | None]]:
    """Get instance types from a cluster_details response.

    Returns a tuple of schduler_instance_type, Counter(worker_instance_types).
    If the instance type is still not determined, will show "Unknown".
    """
    scheduler_instance_type = SCHEDULER_SEARCH.search(cluster_details) or None
    worker_instance_types = Counter(w.get("instance_type_id", None) for w in WORKER_SEARCH.search(cluster_details))
    return scheduler_instance_type, worker_instance_types


def sniff_environment() -> Literal["notebook", "ipython_terminal", "terminal"]:
    """Heuristically determine the execution context.

    This function attempts to determine whether the execution environment is a Jupyter
    Notebook-like context, an IPython REPL context, or the standard Python context.
    The detection is not foolproof and is sensitive to the implementation details of
    the shell.
    """
    try:
        get_ipython  # type: ignore # noqa: B018
    except NameError:
        return "terminal"
    ipython = get_ipython()  # type: ignore # noqa: F821
    shell = ipython.__class__.__name__
    if "google.colab" in str(ipython.__class__) or shell == "ZMQInteractiveShell":
        return "notebook"  # Jupyter notebook or qtconsole
    elif shell == "TerminalInteractiveShell":
        return "ipython_terminal"  # Terminal running IPython
    else:
        return "terminal"  # Other type (?)


@contextmanager
def simple_progress(description: str, progress: Progress | None = None):
    if progress:
        task = progress.add_task(description=description, total=1)
        yield
        progress.advance(task)
    else:
        # Fallback to logging description when progress is not available
        logger.info(f"{description}...")
        yield


EXECUTION_CONTEXT = sniff_environment()


def in_vscode():
    return "VSCODE_PID" in os.environ


def use_rich_widget():
    # Widget doesn't work in VSCode
    # https://github.com/coiled/platform/issues/4271
    return EXECUTION_CONTEXT in ["ipython_terminal", "notebook"] and not in_vscode()
