"""Kimi Code's McpSlot (plugin manifest): the bearer written into its installed manifest."""

from __future__ import annotations


def _kimi_check(_source: str, _codex_auth: bool | None) -> McpCheck:
    """Kimi Code sends the bearer the wizard wrote into its installed manifest
    (`kimi_config.sync_mcp_bearer`); it has to be the token this device holds."""
    from probe.shared.harness.harnesses.kimi_code import config as kimi_config
    from probe.shared.harness.mcp_token import current_mcp_token

    try:
        sent = kimi_config.installed_mcp_bearer()
    except kimi_config.ManifestUnreadable as exc:
        return McpCheck(McpCredential.UNKNOWN, what=str(exc))
    if not sent and not kimi_config.mcp_server_same_deployment():
        return McpCheck(McpCredential.UNKNOWN,
                        what="Kimi's plugin points at another Probe deployment than this device")
    held = current_mcp_token()  # what the wizard writes (`kimi_config.sync_mcp_bearer`)
    if sent and held and sent == held:
        return McpCheck(McpCredential.PRESENT)
    return McpCheck(McpCredential.MISSING)
from probe.shared.harness.mcp import McpCheck, McpCredential  # noqa: E402 -- pieces need each other; the front door loads this one first
