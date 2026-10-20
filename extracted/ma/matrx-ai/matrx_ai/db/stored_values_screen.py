"""THE STORED-VALUES SCREEN — what a run's values look like on a row the browser can read.

Two durable rows this package writes are client-readable (and in the host's realtime feed):
``chat.conversation.variables`` (written once, when the conversation is created, from
``AppContext.initial_variables``) and ``chat.user_request.metadata`` (the run context's
``metadata``, merged at finalize). A host may keep some runs' values off those rows — the
aidream host keeps a MANDATE run's provision values in a server-only store and lets the
browser see only names and sizes (provision audit 2026-10-18, stage 3).

matrx-ai never knows which runs those are or where the values go. The host registers ONE
synchronous step with :func:`set_stored_values_screen`::

    def screen(kind: str, row_id: str | None, values: dict, ctx) -> dict

``kind`` is :data:`CONVERSATION_VARIABLES`, :data:`USER_REQUEST_METADATA` or
:data:`MESSAGE_MODEL_CONTEXT`; the step returns what is written in place of ``values`` (it may keep
the originals for its own store).

WHICH RUN IS THIS? The host reads the context's ``metadata`` and, under an execution, the metadata
of the request being executed (:func:`active_request_metadata`) — a door that names its run only
on its request (a held code call, a NamedAgent) is seen before its conversation row is created.
A door marks a run whose values the host keeps off client rows with :func:`mark_mandate_values`
(THE mark, on the context's or the request's metadata); the host may also recognise its own stamps.
Unconfigured: values are written as given (a standalone install has no server-only store).
A host step that raises is logged loudly and the values are written as given — a run is never
lost to a screening fault, and the host's own guard reports the leak.

Called at exactly the write points: the conversation gate's create paths
(``create_new_conversation``, ``ensure_conversation_exists``), ``persistence``'s
finalize of the user request's metadata, and the lift of a message's ``model_context``
(``persistence.lift_promoted_message_columns`` — both message write sites).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from matrx_utils import vcprint

#: ``kind`` for ``chat.conversation.variables`` at conversation creation.
CONVERSATION_VARIABLES = "conversation_variables"
#: ``kind`` for ``chat.user_request.metadata`` at finalize.
USER_REQUEST_METADATA = "user_request_metadata"
#: ``kind`` for ``chat.message.model_context`` (the per-turn context record) as a message is written.
MESSAGE_MODEL_CONTEXT = "message_model_context"

#: THE MARK: a metadata key saying "this run's values are kept off client rows" (value
#: ``{"door": <door>}``). Set with :func:`mark_mandate_values`, never by hand.
MANDATE_VALUES_MARK_KEY = "mandate_values_held"


def mark_mandate_values(metadata: dict[str, Any], *, door: str) -> dict[str, Any]:
    """Mark ``metadata`` (a context's or a request's) as a run whose values the host keeps off
    client-readable rows. Mutates and returns ``metadata``. Set it BEFORE the run's conversation
    is created — the screen applies at the insert."""
    metadata[MANDATE_VALUES_MARK_KEY] = {"door": str(door or "")}
    return metadata


def active_request_metadata() -> dict[str, Any] | None:
    """The metadata of the request the current execution runs (``None`` outside an execution)."""
    try:
        from matrx_ai.orchestrator.execution_state import try_get_execution_state

        state = try_get_execution_state()
    except Exception:  # noqa: BLE001 — an unreadable state is "no request", never a fault
        return None
    found = getattr(state, "request_metadata", None) if state is not None else None
    return found if isinstance(found, dict) else None

StoredValuesScreen = Callable[[str, "str | None", dict[str, Any], Any], dict[str, Any]]

_SCREEN: StoredValuesScreen | None = None


def set_stored_values_screen(screen: StoredValuesScreen | None) -> None:
    """Register (or clear, with ``None``) the host's screening step."""
    global _SCREEN
    _SCREEN = screen


def screen_stored_values(kind: str, row_id: Any, values: Any, ctx: Any) -> Any:
    """``values`` as they may be written on a client-readable row (see module docstring)."""
    screen = _SCREEN
    if screen is None or not isinstance(values, dict) or not values:
        return values
    try:
        out = screen(kind, str(row_id) if row_id else None, values, ctx)
    except Exception as exc:  # noqa: BLE001 — a screening fault never loses the run
        vcprint(
            f"[stored_values_screen] host screen failed for {kind} {row_id}: {type(exc).__name__}: {exc} "
            "— values written as given",
            color="red",
        )
        return values
    return out if isinstance(out, dict) else values


__all__ = [
    "CONVERSATION_VARIABLES",
    "MANDATE_VALUES_MARK_KEY",
    "MESSAGE_MODEL_CONTEXT",
    "USER_REQUEST_METADATA",
    "StoredValuesScreen",
    "active_request_metadata",
    "mark_mandate_values",
    "screen_stored_values",
    "set_stored_values_screen",
]
