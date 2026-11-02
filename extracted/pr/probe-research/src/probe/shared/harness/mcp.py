"""McpSlot facet of HarnessIntegration, keyed by the registry's mcp kind: check the agent's MCP credential (McpCredential, McpCheck), report and repair token drift; the held read token every slot checks against."""

from __future__ import annotations
import os
from dataclasses import dataclass
from probe.foundation.compat.compat import StrEnum


class McpCredential(StrEnum):
    """What one agent's MCP credential check found (`MCP_RESOLVERS`)."""

    PRESENT = "present"
    MISSING = "missing"
    REJECTED = "rejected"  # present, and the server refused it (`probe doctor`, the wizard)
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class McpCheck:
    """One credential check: what it found, the command that fixes it, and,
    for UNKNOWN, what could not be read."""

    credential: McpCredential
    fix: str = "probe wizard"
    what: str = ""


# --- MCP credential resolvers, one per registry `mcp` kind ------------------


def cli_mcp_token() -> str | None:
    """The read token an agent's MCP sends, resolved as Claude Code's
    `bin/probe-mcp-headers` and pi's `src/core/mcpAuth.ts` resolve it:
    `PROBE_MCP_TOKEN` first, then the config's `mcp_token`."""
    env = (os.environ.get("PROBE_MCP_TOKEN") or "").strip()
    if env:
        return env
    from probe.sdk.settings.settings import load_context

    try:
        return (load_context() or {}).get("mcp_token") or None
    except Exception:  # noqa: BLE001 - an unreadable config holds no token we can name
        return None


def _token_check(_source: str, _codex_auth: bool | None) -> McpCheck:
    if cli_mcp_token():
        return McpCheck(McpCredential.PRESENT)
    return McpCheck(McpCredential.MISSING)
