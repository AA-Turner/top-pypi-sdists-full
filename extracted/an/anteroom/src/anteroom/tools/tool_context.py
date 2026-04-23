"""Shared helper for building the ``_extra_context`` dict passed to
:meth:`anteroom.tools.ToolRegistry.call_tool` from interface callers.

The CLI REPL (``cli/repl.py``) and the web chat router (``routers/chat.py``)
each assemble the same dict of unprefixed keys (``bg_manager``,
``detach_manager``, ``conversation_id``, ``db``, ``config``, ``user_id``,
``tool_call_id``)
that ``call_tool`` then translates into the underscore-prefixed kwargs
individual tools declare (``_db``, ``_config``, ``_user_id``, ...).

Extracting the assembly keeps the two interface-specific sites in lock-step
and gives tests a pin point for verifying the dict shape — including the
``config`` / ``user_id`` threading added in #217 for the ``save_memory``
tool's promotion-pipeline context.
"""

from __future__ import annotations

from typing import Any


def build_tool_extra_context(
    *,
    bg_manager: Any | None,
    detach_manager: Any | None,
    conversation_id: str | None,
    db: Any,
    config: Any,
    tool_call_id: str | None = None,
) -> dict[str, Any]:
    """Assemble the ``_extra_context`` dict for a built-in tool call.

    CLI REPL variant: derives ``user_id`` from the ``config.identity``
    singleton loaded at REPL start-up.
    """
    user_id = config.identity.user_id if getattr(config, "identity", None) else None
    return {
        "bg_manager": bg_manager,
        "detach_manager": detach_manager,
        "conversation_id": conversation_id,
        "db": db,
        "config": config,
        "user_id": user_id,
        "tool_call_id": tool_call_id,
    }


def build_tool_extra_context_web(
    *,
    bg_manager: Any | None,
    detach_manager: Any | None,
    conversation_id: str | None,
    db: Any,
    config: Any,
    user_id: str | None,
    tool_call_id: str | None = None,
) -> dict[str, Any]:
    """Web chat router variant.

    ``user_id`` is resolved per-request from the session identity
    (``ToolExecutorContext.uid``) rather than from ``config.identity``,
    so the caller passes it explicitly.
    """
    return {
        "bg_manager": bg_manager,
        "detach_manager": detach_manager,
        "conversation_id": conversation_id,
        "db": db,
        "config": config,
        "user_id": user_id,
        "tool_call_id": tool_call_id,
    }
