"""pi's McpSlot (extension bridge): pi-mcp-adapter's own token or the held one."""

from __future__ import annotations
from pathlib import Path

from probe.shared.harness.harnesses import pi as pi_config


def _pi_check(_source: str, _codex_auth: bool | None) -> McpCheck:
    """pi has two providers: pi-mcp-adapter serves our manifest with ITS OWN
    OAuth login when installed (our extension stands down); otherwise our
    extension's bridge sends the CLI's read token."""
    if pi_config.mcp_adapter_installed(cwd=Path.cwd()):
        return McpCheck(McpCredential.UNKNOWN, what="served by pi-mcp-adapter, which keeps its own login")
    if pi_config.merged_package_entry(cwd=Path.cwd()).extension_filtered_out:
        # The bridge IS the extension: filtered out, nothing serves our MCP.
        return McpCheck(
            McpCredential.UNKNOWN,
            what="pi's settings filter out Probe's extension (`extensions` on probe-research-pi)",
        )
    return _token_check(_source, _codex_auth)
from probe.shared.harness.mcp import McpCheck, McpCredential, _token_check  # noqa: E402 -- pieces need each other; the front door loads this one first
