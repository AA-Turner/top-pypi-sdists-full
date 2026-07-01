from __future__ import annotations

import typing as t

try:
    from dbt.adapters.events import types
    from dbt_common.events.functions import fire_event as dbt_fire_event
    from dbt_common.events.event_manager import IEventManager
    from dbt_common.events.base_types import EventMsg as EventMsg
except ImportError:
    from dbt.events import types
    from dbt.events.functions import fire_event as dbt_fire_event  # type: ignore[import-untyped]
    from dbt.events.eventmgr import IEventManager  # type: ignore[import-untyped]
    from dbt.events.base_types import EventMsg as EventMsg  # type: ignore[import-untyped]


ADAPTER_NAME = "State"
CALLBACKS_BY_ID: t.Dict[str, t.Callable[[EventMsg], None]] = {}


def _get_event_manager() -> IEventManager:
    try:
        from dbt_common.events.event_manager_client import get_event_manager

        return get_event_manager()
    except ImportError:
        # dbt 1.7
        from dbt.events.functions import EVENT_MANAGER  # ty: ignore[unresolved-import]

        return EVENT_MANAGER


class AdapterErrorDowngrader:
    """Context manager that temporarily downgrades AdapterEventError events to debug level.

    On enter, replaces the EventManager's ``fire_event`` with a version that
    converts ``AdapterEventError`` into ``AdapterEventDebug``.  On exit, the
    original ``fire_event`` is restored.

    Used during clone SQL execution to prevent expected adapter errors
    (e.g., BigQuery's exception_handler firing AdapterEventError via
    AdapterLogger.error) from being surfaced as real errors by external tools
    like Dagster.
    """

    def __init__(self, manager: IEventManager) -> None:
        self._manager = manager
        self._original_fire_event: t.Any = None

    def __enter__(self) -> AdapterErrorDowngrader:
        self._original_fire_event = self._manager.fire_event
        original = self._original_fire_event

        def _filtered_fire_event(e: t.Any, *args: t.Any, **kwargs: t.Any) -> None:
            if isinstance(e, types.AdapterEventError):  # ty: ignore[unresolved-attribute]
                downgraded = types.AdapterEventDebug(  # ty: ignore[unresolved-attribute]
                    name=getattr(e, "name", ADAPTER_NAME),
                    base_msg=getattr(e, "base_msg", ""),
                    args=list(getattr(e, "args", [])),
                )
                return original(downgraded, *args, **kwargs)
            return original(e, *args, **kwargs)

        self._manager.fire_event = _filtered_fire_event  # type: ignore[method-assign]
        return self

    def __exit__(self, *exc: t.Any) -> None:
        self._manager.fire_event = self._original_fire_event  # type: ignore[method-assign]


def downgrade_adapter_error_events() -> AdapterErrorDowngrader:
    """Return a context manager that downgrades AdapterEventError to debug level."""
    return AdapterErrorDowngrader(_get_event_manager())


def fire_info_event(base_msg: str, *args: t.Any) -> None:
    dbt_fire_event(types.AdapterEventInfo(name=ADAPTER_NAME, base_msg=base_msg, args=list(args)))  # ty: ignore[unresolved-attribute]


def fire_warn_event(base_msg: str, *args: t.Any) -> None:
    dbt_fire_event(types.AdapterEventWarning(name=ADAPTER_NAME, base_msg=base_msg, args=list(args)))  # ty: ignore[unresolved-attribute]


_CONTINUING_WITHOUT_CACHE_SUFFIX = " Continuing without state"
_SUBOPTIMAL_BEHAVIOR_SUFFIX = " This will result in suboptimal state behavior"


def fire_warn_event_with_cache_bypass(base_msg: str, *args: t.Any) -> None:
    if base_msg and base_msg[-1] != ".":
        base_msg += "."
    fire_warn_event(base_msg + _CONTINUING_WITHOUT_CACHE_SUFFIX, *args)


def fire_warn_event_suboptimal(base_msg: str, *args: t.Any) -> None:
    if base_msg and base_msg[-1] != ".":
        base_msg += "."
    fire_warn_event(base_msg + _SUBOPTIMAL_BEHAVIOR_SUFFIX, *args)


def fire_error_event(base_msg: str, *args: t.Any) -> None:
    dbt_fire_event(types.AdapterEventError(name=ADAPTER_NAME, base_msg=base_msg, args=list(args)))  # ty: ignore[unresolved-attribute]


def fire_debug_event(base_msg: str, *args: t.Any) -> None:
    dbt_fire_event(types.AdapterEventDebug(name=ADAPTER_NAME, base_msg=base_msg, args=list(args)))  # ty: ignore[unresolved-attribute]


def fire_event(level: str, base_msg: str, *args: t.Any) -> None:
    level = level.lower()
    if level == "info":
        fire_info_event(base_msg, *args)
    elif level in ("warn", "warning"):
        fire_warn_event(base_msg, *args)
    elif level == "error":
        fire_error_event(base_msg, *args)
    elif level == "debug":
        fire_debug_event(base_msg, *args)
    else:
        raise ValueError(f"Unknown event level: {level}")


def register_callback(id: str, callback: t.Callable[[EventMsg], None]) -> None:
    """Register a callback to dbt's event manager.

    If a callback with the same :id has already been registered before, it is un-registered first
    """
    manager = _get_event_manager()

    if existing_callback := CALLBACKS_BY_ID.pop(id, None):
        try:
            manager.callbacks.remove(existing_callback)
        except ValueError:
            # if the callback was not actually registered, remove() will raise an error
            pass

    CALLBACKS_BY_ID[id] = callback

    # note: EventManager.add_callback() does not exist in dbt 1.7
    manager.callbacks.append(callback)
