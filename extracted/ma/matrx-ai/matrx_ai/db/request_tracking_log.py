from __future__ import annotations

from typing import Any


def resolve_runtime_root_execution_id(ctx: Any | None) -> str | None:
    if ctx is None:
        return None
    meta = getattr(ctx, "metadata", None) or {}
    if not isinstance(meta, dict):
        return None
    value = meta.get("runtime_root_execution_id")
    return str(value) if value else None


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
