"""Which door a slow-dataset start comes through: ``chat`` (an agent turn) or ``ui`` (a purposeful screen).

Owner ruling (2026-10-16): structured datasets (20 s - 25 min) are never started inside chat or by an agent
unless a person purposefully asked, on a screen. Fast reads (social API, advanced reader, plain web read) are fine.
One signal, read from the request's app context, shared by every agent-reachable dataset door.
"""

from __future__ import annotations

from typing import Any

DATA_LIBRARY_PATH = "/data/library"
SCREEN_RUN_ORIGIN = "screen_run"  # == aidream.services.action_requests.spend_ask.SCREEN_RUN_ORIGIN


def is_chat_door(app_ctx: Any | None = None, *, unknown_is_chat: bool) -> bool:
    """True when a dataset must NOT be started from here.

    Purposeful (``ui``): the context says ``door="ui"`` or ``tool_origin="screen_run"``.
    Chat: ``door="chat"``, or any run attached to a conversation. Anything else is ``unknown_is_chat``
    (an agent tool fails closed; a screen-side caller without a conversation does not).
    """
    if app_ctx is None:
        from matrx_ai.context.app_context import try_get_app_context

        app_ctx = try_get_app_context()
    if app_ctx is None:
        return unknown_is_chat
    meta = getattr(app_ctx, "metadata", None) or {}
    door = str(meta.get("door") or "")
    if door in ("chat", "ui"):
        return door == "chat"
    if str(meta.get("tool_origin") or "") == SCREEN_RUN_ORIGIN:
        return False
    if getattr(app_ctx, "conversation_id", None):
        return True
    return unknown_is_chat


def slower_dataset_line(what: str | None = None) -> str:
    """The ONE line a chat turn gets instead of a dataset start."""
    subject = f" for {what}" if what else ""
    return (
        f"A slower dataset exists{subject}, but it is not started from chat. Tell the person they can start it "
        f"from the Data Library ({DATA_LIBRARY_PATH}); for a quick answer now, use web with action='read' on the page URL."
    )
