from __future__ import annotations

import uuid
from typing import Any


def resolve_runtime_root_execution_id(ctx: Any | None) -> str | None:
    if ctx is None:
        return None
    meta = getattr(ctx, "metadata", None) or {}
    if not isinstance(meta, dict):
        return None
    value = meta.get("runtime_root_execution_id")
    return str(value) if value else None


#: ``chat.request.execution_kind`` of a provider call paid by a runtime spine execution that is not a
#: workflow / scheduled run: ``execution_id`` is that ``runtime.global_execution.id``.
SPINE_EXECUTION_KIND = "global_execution"

#: Metadata keys that carry the spine execution paying for a call, nearest first: the internal run's own
#: execution (its per-call meter), the current nesting parent, then the conversation root. All are stamped
#: by the host and only READ here, never resolved (context-is-carried-never-rebuilt).
_SPINE_EXECUTION_KEYS = (
    "runtime_settle_metered_execution",
    "runtime_execution_id",
    "runtime_root_execution_id",
)


def resolve_request_execution_attribution(ctx: Any | None) -> tuple[str | None, str | None]:
    """``(execution_kind, execution_id)`` a ``chat.request`` row is stamped with.

    An explicit attribution on the context (workflow_run, sch_run, ...) always wins. Otherwise the row
    names the spine execution the context carries, so every provider row points at the run that paid for
    it. ``(None, None)`` only when no execution is carried at all (the pair is set together or not at all).
    """
    if ctx is None:
        return None, None
    kind = getattr(ctx, "execution_kind", None)
    execution_id = getattr(ctx, "execution_id", None)
    if kind or execution_id:
        return kind, execution_id
    meta = getattr(ctx, "metadata", None)
    if not isinstance(meta, dict):
        return None, None
    for key in _SPINE_EXECUTION_KEYS:
        value = meta.get(key)
        if not value:
            continue
        try:
            return SPINE_EXECUTION_KIND, str(uuid.UUID(str(value)))
        except ValueError:
            continue  # the column is a uuid: a non-uuid stamp is skipped, never written
    return None, None


def format_request_tracking_lines(
    *,
    request_id: str | None,
    conversation_id: str | None = None,
    runtime_root_execution_id: str | None = None,
    prefix: str = " - ",
) -> list[str]:
    """Operator-facing identity during cx_user_request → runtime cutover.

    ``request_id`` is one UUID shared by ``runtime.global_request.id`` and the
    retiring ``cx_user_request.id``. ``runtime_root_execution_id`` is the
    conversation-root ``runtime.global_execution.id`` (stamped on /v2).
    """
    rid = request_id or "—"
    root = runtime_root_execution_id or "— (not on spine)"
    lines: list[str] = []
    if conversation_id is not None:
        lines.append(f"{prefix}Conversation ID: {conversation_id}")
    lines.append(
        f"{prefix}Request ID: {rid}  (= runtime.global_request · retiring cx_user_request)"
    )
    lines.append(f"{prefix}Runtime root execution: {root}")
    return lines


def format_request_tracking_label(request_id: str | None) -> str:
    rid = request_id or "—"
    return f"{rid} (= runtime.global_request · retiring cx_user_request)"
