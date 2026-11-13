"""The deployment's priority callback.

The `priority` section of langgraph.json names a `Priority` object, whose
`@priority.assign` function sets a thread's priority settings at the thread's
first run. A lower priority runs first, from -5 to 5.
"""

from __future__ import annotations

import functools
import importlib.util
import sys
from typing import TYPE_CHECKING, Any, TypedDict

import structlog
from langgraph_sdk import Auth
from starlette.exceptions import HTTPException

from langgraph_api import timing
from langgraph_api.auth.noop import UnauthenticatedUser
from langgraph_api.config import LANGGRAPH_PRIORITY
from langgraph_api.timing import profiled_import
from langgraph_api.utils import get_auth_ctx

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Mapping

    from langgraph_sdk import Priority, PriorityContext, PrioritySettings

    PriorityCallback = Callable[[PriorityContext], Awaitable[PrioritySettings | None]]

logger = structlog.stdlib.get_logger(__name__)

PRIORITY_MIN = -5
PRIORITY_MAX = 5
DEFAULT_PRIORITY = 0
DEFAULT_FAIRNESS_GROUP = "default"
# Fairness ordering will put group names in Redis key names, so their length is bounded.
FAIRNESS_GROUP_MAX_LENGTH = 256


class ThreadPrioritySettings(TypedDict):
    """A thread's priority settings."""

    priority: int
    fairness_group: str


@functools.lru_cache(maxsize=1)
def get_priority_callback() -> PriorityCallback | None:
    """The deployment's `@priority.assign` function, or None without a `priority` section."""
    if not LANGGRAPH_PRIORITY:
        return None
    path = LANGGRAPH_PRIORITY["path"]
    priority = _load_priority_obj(path)
    if priority._assign_handler is None:
        raise ValueError(
            f"The Priority object at {path} has no @priority.assign function"
        )
    logger.info(f"Loaded priority callback from path {path}")
    return priority._assign_handler


@timing.timer(
    message="Loading priority callback {priority_path}",
    metadata_fn=lambda priority_path: {"priority_path": priority_path},
    warn_threshold_secs=5,
    warn_message="Loading priority callback '{priority_path}' took longer than expected",
    error_threshold_secs=10,
)
def _load_priority_obj(path: str) -> Priority:
    """Load a Priority object from "./path/to/file.py:name" or "module:name"."""
    if ":" not in path:
        raise ValueError(
            f"Invalid priority path format: {path}. "
            "Must be in format: './path/to/file.py:name' or 'module:name'"
        )

    module_name, object_name = path.rsplit(":", 1)
    module_name = module_name.rstrip(":")

    if module_name.endswith((".js", ".mjs", ".ts")):
        raise ValueError(
            "A JavaScript priority callback is not supported. "
            f"Please use a Python module instead: {module_name}"
        )

    try:
        with profiled_import(path):
            if "/" in module_name or ".py" in module_name:
                modname = f"dynamic_module_{hash(module_name)}"
                modspec = importlib.util.spec_from_file_location(modname, module_name)
                if modspec is None or modspec.loader is None:
                    raise ValueError(f"Could not load file: {module_name}")
                module = importlib.util.module_from_spec(modspec)
                sys.modules[modname] = module
                modspec.loader.exec_module(module)
            else:
                module = importlib.import_module(module_name)

        loaded = getattr(module, object_name, None)
        if loaded is None:
            raise ValueError(
                f"Could not find priority '{object_name}' in module: {module_name}"
            )
        from langgraph_sdk import Priority as PriorityClass  # noqa: PLC0415

        if not isinstance(loaded, PriorityClass):
            raise ValueError(f"Expected a Priority instance, got {type(loaded)}")
        return loaded

    except ImportError as e:
        e.add_note(f"Could not import module:\n{module_name}\n\n")
        raise
    except FileNotFoundError as e:
        raise ValueError(f"Could not find file: {module_name}") from e


def _invalid(problem: str) -> HTTPException:
    return HTTPException(
        status_code=500, detail=f"The priority callback returned {problem}"
    )


def _int_in_range(
    result: Mapping[str, Any], key: str, low: int, high: int, default: int
) -> int:
    value = result.get(key)
    if value is None:
        return default
    # bool is an int subclass; a True priority is a bug, not 1.
    if isinstance(value, bool) or not isinstance(value, int):
        raise _invalid(f"{key}={value!r}, not an integer")
    if not low <= value <= high:
        raise _invalid(f"{key}={value}, outside {low}..{high}")
    return value


def validate_priority_settings(result: Any) -> ThreadPrioritySettings:
    """The settings to store for the callback's result, with defaults for what it left out.
    An empty fairness_group is the default group, like a missing one, and a fairness_weight
    is dropped with a warning.

    Raises:
        HTTPException(500): the result isn't a dict or None, has an unknown key, or has a
            value of the wrong type or out of range. The detail names the problem.
    """
    if result is None:
        result = {}
    if not isinstance(result, dict):
        raise _invalid(f"a {type(result).__name__}, not a dict or None")
    if "fairness_weight" in result:
        # langgraph-sdk 0.4.9 to 0.4.11 type the result with a fairness_weight, which the
        # server never stores, so callbacks written against them may still return it.
        result = {
            key: value for key, value in result.items() if key != "fairness_weight"
        }
        logger.warning(
            "Priority callback returned fairness_weight, which has no effect and is"
            " ignored; remove it from the callback's result"
        )
    unknown = sorted(set(result) - set(ThreadPrioritySettings.__annotations__))
    if unknown:
        raise _invalid(f"unknown keys {unknown}")

    group = result.get("fairness_group")
    if group is None or group == "":
        group = DEFAULT_FAIRNESS_GROUP
    elif not isinstance(group, str):
        raise _invalid(f"fairness_group={group!r}, not a string")
    elif len(group) > FAIRNESS_GROUP_MAX_LENGTH:
        raise _invalid(
            f"a fairness_group of {len(group)} characters, longer than"
            f" {FAIRNESS_GROUP_MAX_LENGTH}"
        )

    return ThreadPrioritySettings(
        priority=_int_in_range(
            result, "priority", PRIORITY_MIN, PRIORITY_MAX, DEFAULT_PRIORITY
        ),
        fairness_group=group,
    )


async def assign_priority_settings(
    callback: PriorityCallback,
    *,
    thread_id: str | None,
    thread_metadata: dict[str, Any],
    assistant_id: str,
    graph_id: str,
    assistant_metadata: dict[str, Any],
    run_metadata: dict[str, Any],
    run_kwargs: Mapping[str, Any],
) -> ThreadPrioritySettings:
    """Call the priority callback for a thread's first run and validate its result.

    The user and permissions come from the request's auth context; for a cron fire that is
    the cron owner's stored user. The cron id comes from the run's configurable, which
    create_valid_run fills only from the scheduler's argument.

    Raises:
        HTTPException: as the callback raised it, or 500 for any other error or for an
            invalid result; both 500s are logged. Nothing is stored, so the next run calls
            the callback again.
    """
    from langgraph_sdk import PriorityContext  # noqa: PLC0415

    auth_ctx = get_auth_ctx()
    configurable = (run_kwargs.get("config") or {}).get("configurable") or {}
    ctx = PriorityContext(
        user=auth_ctx.user if auth_ctx is not None else UnauthenticatedUser(),
        permissions=list(auth_ctx.permissions) if auth_ctx is not None else [],
        thread_id=thread_id,
        thread_metadata=thread_metadata,
        assistant_id=assistant_id,
        graph_id=graph_id,
        assistant_metadata=assistant_metadata,
        run_metadata=run_metadata,
        cron_id=configurable.get("cron_id"),
    )
    try:
        result = await callback(ctx)
    except Auth.exceptions.HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
            headers=dict(e.headers) if e.headers else None,
        ) from e
    except HTTPException:
        raise
    except Exception as e:
        await logger.aexception(
            "Priority callback failed", thread_id=thread_id, graph_id=graph_id
        )
        raise HTTPException(
            status_code=500, detail=f"The priority callback failed: {e!r}"
        ) from e
    try:
        return validate_priority_settings(result)
    except HTTPException as e:
        await logger.aerror(
            "Priority callback returned invalid settings",
            detail=e.detail,
            thread_id=thread_id,
            graph_id=graph_id,
        )
        raise
