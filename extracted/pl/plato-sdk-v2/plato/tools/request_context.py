"""Request context helpers for world-hosted MCP tools."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar
from threading import RLock

from pydantic import BaseModel, Field

_current_request_context: ContextVar[ToolRequestContext | None] = ContextVar(
    "plato_tool_request_context",
    default=None,
)
_registered_client_contexts: dict[str, ToolRequestContext] = {}
_registered_client_contexts_lock = RLock()


class ToolRequestContext(BaseModel):
    """Identity and execution metadata for the current MCP tool call."""

    client_id: str = Field(
        description="Canonical caller identifier for the MCP request.",
    )
    hostname: str | None = Field(
        default=None,
        description="SSH-reachable hostname or IP of the agent VM.",
    )
    display_name: str | None = Field(
        default=None,
        description="Human-readable label for the current agent run.",
    )
    instruction: str | None = Field(
        default=None,
        description="Current instruction being executed when registered by the runner.",
    )
    session_id: str | None = Field(
        default=None,
        description="Optional world/session identifier for the caller.",
    )
    image: str | None = Field(
        default=None,
        description="Agent image/package for the current run when available.",
    )
    attempt: int | None = Field(
        default=None,
        description="1-based execution attempt number for continuation runs.",
    )


def get_request_context() -> ToolRequestContext | None:
    """Return the current MCP tool request context, if any."""
    return _current_request_context.get()


def register_client_context(request_context: ToolRequestContext) -> None:
    """Register execution metadata for a client ID handled by a world MCP server."""
    with _registered_client_contexts_lock:
        _registered_client_contexts[request_context.client_id] = request_context


def get_registered_client_context(client_id: str) -> ToolRequestContext | None:
    """Return the registered execution metadata for a client ID, if any."""
    with _registered_client_contexts_lock:
        return _registered_client_contexts.get(client_id)


def unregister_client_context(client_id: str) -> None:
    """Remove execution metadata for a client ID when the run finishes."""
    with _registered_client_contexts_lock:
        _registered_client_contexts.pop(client_id, None)


@contextmanager
def set_request_context(
    request_context: ToolRequestContext | None,
) -> Generator[ToolRequestContext | None, None, None]:
    """Temporarily set the current MCP tool request context."""
    token = _current_request_context.set(request_context)
    try:
        yield request_context
    finally:
        _current_request_context.reset(token)
