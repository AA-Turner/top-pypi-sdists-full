from __future__ import annotations

import contextlib
import sys
import threading
from collections.abc import Callable
from typing import Any

from bitfab import service_calls

WHOLE_OBJECTS_KEY = "wholeObjects"
WHOLE_SPAN_PART = "whole."
MAX_REMEMBERED_TRACES = 10_000

_lock = threading.Lock()
_claimed: dict[str, set[str]] = {}


def whole_span_name(prefix: str, kind: str) -> str:
    return f"{prefix}{WHOLE_SPAN_PART}{kind}"


def current_trace_id() -> str | None:
    client = sys.modules.get("bitfab.client")
    if client is None or not client._get_span_stack():
        return None
    root = client._trace_root_span_context()
    return str(root.get("traceId")) if root else None


def claim(kind: str, object_id: str) -> bool:
    trace_id = current_trace_id()
    if trace_id is None:
        return False
    key = f"{kind}:{object_id}"
    with _lock:
        if trace_id not in _claimed and len(_claimed) >= MAX_REMEMBERED_TRACES:
            _claimed.clear()
        taken = _claimed.setdefault(trace_id, set())
        if key in taken:
            return False
        taken.add(key)
    return True


def record(
    integration: str,
    prefix: str,
    kind: str,
    object_id: str,
    send: Callable[[], Any],
) -> Any:
    with contextlib.suppress(Exception):
        return service_calls.run(
            service_calls.ServiceCall(
                integration=integration,
                method=whole_span_name(prefix, kind),
                params={"id": object_id},
                send=send,
            )
        )
    return None


def capture(
    integration: str,
    prefix: str,
    kind: str,
    object_id: str,
    fetch: Callable[[], Any],
) -> Any:
    if not claim(kind, object_id):
        return None
    return record(integration, prefix, kind, object_id, fetch)


def wholes(state: dict[str, Any], kind: str) -> dict[str, dict[str, Any]]:
    return state.setdefault(WHOLE_OBJECTS_KEY, {}).setdefault(kind, {})


def is_whole(state: dict[str, Any], kind: str, object_id: str) -> bool:
    return object_id in wholes(state, kind)


def mark_whole(
    state: dict[str, Any], kind: str, object_id: str, details: dict[str, Any]
) -> None:
    wholes(state, kind)[object_id] = details
