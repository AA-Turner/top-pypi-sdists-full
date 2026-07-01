"""
MCP bridge — wrappers around CVC's MCP tools (cvc_*).

These are called from the /api/ops/* and /api/mcp/* routers in the
new gateway. The real implementation lives in `cvc.mcp_server` —
specifically `_handle_tool_call(tool_name, arguments)` which dispatches
to cvc_status, cvc_commit, cvc_branch, cvc_merge, etc.

This module is a thin async wrapper: it always calls the real engine,
never falls back to a stub, and never logs spurious ModuleNotFoundErrors.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

logger = logging.getLogger("cvc.gateway.mcp_bridge")


async def call_mcp(tool: str, **kwargs) -> dict[str, Any]:
    """Call a CVC MCP tool by name (cvc_status, cvc_commit, ...)."""
    try:
        from cvc.mcp_server import _handle_tool_call

        loop = asyncio.get_running_loop()
        # _handle_tool_call is sync; offload to a thread to avoid blocking
        # the event loop on large workspace scans.
        result = await loop.run_in_executor(
            None, lambda: _handle_tool_call(tool, kwargs)
        )
        return result if isinstance(result, dict) else {"result": result}
    except Exception as e:  # pragma: no cover — defensive
        logger.exception("MCP call %s failed", tool)
        return {"error": f"cvc_mcp call failed: {e}"}


def _get_workspace_from_mcp_context() -> str | None:
    """Best-effort: return the active workspace path.

    Used by event-spine capture calls in the ops router — they need
    to tag the event with the workspace the user is acting on, but
    the MCP bridge runs in an executor and doesn't carry the request
    ContextVar.

    Strategy: read the persisted workspace registry
    (~/.cvc/workspaces.json) and return whichever is marked
    last_active. Falls back to None if registry is missing/corrupt.
    """
    try:
        from pathlib import Path as _P
        import json as _json
        registry = _P.home() / ".cvc" / "workspaces.json"
        if not registry.exists():
            return None
        data = _json.loads(registry.read_text())
        if not isinstance(data, list):
            return None
        # Registry entries may have different shapes; find the active one.
        for entry in data:
            if isinstance(entry, dict):
                if entry.get("active") or entry.get("is_active"):
                    return entry.get("path")
        # Fallback: first entry
        if data and isinstance(data[0], dict):
            return data[0].get("path")
    except Exception:
        pass
    return None
