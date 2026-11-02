"""Codex's McpSlot (config.toml): its own OAuth login or a static bearer."""

from __future__ import annotations


def _codex_check(_source: str, codex_auth: bool | None) -> McpCheck:
    if codex_auth is None:
        return McpCheck(McpCredential.UNKNOWN, what="`codex mcp list` did not answer")
    if not codex_auth:
        return McpCheck(McpCredential.MISSING)
    # `codex mcp list` answers `bearer_token` for ANY header, a dead one too:
    # a bearer this device has since replaced is a login needed, not "on".
    from probe.shared.harness.harnesses.codex.mcp_auth import codex_mcp_token_drifted

    if codex_mcp_token_drifted():
        return McpCheck(McpCredential.MISSING)
    return McpCheck(McpCredential.PRESENT)
from probe.shared.harness.mcp import McpCheck, McpCredential  # noqa: E402 -- pieces need each other; the front door loads this one first
