"""CLI handler for the /feedback slash command."""

from __future__ import annotations

from typing import Any


async def handle_feedback_command(
    description: str,
    include_history: bool,
    config: Any,
    db: Any,
    *,
    conversation_id: str | None = None,
    conversation_messages: list[dict[str, Any]] | None = None,
    active_space: dict[str, Any] | None = None,
    tool_registry: Any | None = None,
    mcp_manager: Any | None = None,
) -> str:
    """Handle /feedback command.  Returns a user-facing display message."""
    from ..services.feedback import submit_feedback

    messages: list[dict[str, Any]] | None = None
    if include_history and conversation_messages:
        max_msgs = config.feedback.max_history_messages
        messages = conversation_messages[-max_msgs:]

    result = await submit_feedback(
        description,
        config,
        db,
        conversation_id=conversation_id,
        conversation_messages=messages,
        active_space=active_space,
        tool_registry=tool_registry,
        mcp_manager=mcp_manager,
    )

    status = result.get("status", "failed")
    if status == "sent":
        return f"Feedback submitted via reporter '{result.get('reporter', '')}'."
    if status == "saved_locally":
        return f"No reporter configured. Bundle saved to: {result.get('path', '')}"
    return f"Feedback failed: {result.get('error', 'unknown error')}"
