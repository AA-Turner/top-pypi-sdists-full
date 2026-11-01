"""Surface attribution headers on outbound API requests: which surface (CLI, SDK, MCP) sent it,
and the MCP tool being served. Headers only, no payloads. Why a contextvar: DESIGN.md (surface.py).
"""

from __future__ import annotations

import contextvars
from collections.abc import Iterator
from contextlib import contextmanager
from enum import Enum

#: Request header naming the originating product surface (value: a ``Surface``).
SURFACE_HEADER = "X-Probe-Surface"

#: Request header naming the MCP tool being served (MCP surface only).
TOOL_HEADER = "X-Probe-Tool"

#: Who drove a request that was not the person's live session: only ``backfill`` (the importer).
#: The server stamps it ``driven_by`` so #probe-usage reads an import as one, not as SDK use.
ATTRIBUTION_HEADER = "X-Probe-Attribution"


class Surface(str, Enum):
    """Which product surface a backend request originated from."""

    CLI = "cli"
    SDK = "sdk"
    MCP = "mcp"


# The MCP tool name currently being served, or None outside an MCP tool call.
_current_tool: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "probe_mcp_tool", default=None
)


def current_tool() -> str | None:
    """The MCP tool name bound for the current call, or None."""
    return _current_tool.get()


@contextmanager
def tool_scope(name: str) -> Iterator[None]:
    """Bind ``name`` as the MCP tool being served for the duration of the block.

    Scoped to the calling context (a contextvar), so concurrent HTTP requests in
    the hosted server never see each other's tool name."""
    token = _current_tool.set(name)
    try:
        yield
    finally:
        _current_tool.reset(token)
