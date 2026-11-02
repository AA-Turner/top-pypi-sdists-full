"""whether Probe's MCP works in one agent: its slot's credential check and the API's verdict on the held read token."""

from __future__ import annotations

# Read at import: MCP_RESOLVERS below is built when this module loads.
from probe.shared.harness.harnesses.codex.mcp import _codex_check
from probe.shared.harness.harnesses.kimi_code.mcp import _kimi_check
from probe.shared.harness.harnesses.pi.mcp import _pi_check
from probe.shared.harness.mcp import McpCheck, McpCredential, _token_check, cli_mcp_token


def verify_mcp_credential(*, base_url: str, token: str) -> bool | None:
    """Check the read token itself, independently of the saved API credential.

    Only an authoritative rejection prevents reuse. One short attempt keeps
    an offline install from waiting through the SDK's normal retry budget.
    Explicit settings prevent an environment API token from masking a revoked
    MCP token. The MCP surface also avoids minting local device identity during
    this read-only check.
    """
    from probe.sdk.client.client import Client
    from probe.sdk.settings.settings import Settings
    from probe.sdk.errors import AuthError, ScopeError
    from probe.foundation.request_identity.surface import Surface
    from probe.sdk.delivery.transport.transport import Transport

    try:
        settings = Settings(base_url=base_url, token=token)
        with Client(
            settings=settings,
            transport=Transport(
                settings, timeout=5.0, max_retries=0, surface=Surface.MCP.value
            ),
            async_writes=False,
            auto_drain=False,
        ) as client:
            client.me()
        return True
    except (AuthError, ScopeError):
        return False
    except Exception:  # noqa: BLE001 - an unavailable check does not invalidate a token
        return None


def _mcp_resolvers() -> dict:
    from probe.foundation.harness_registry import harness_registry as reg

    return {
        reg.MCP_PLUGIN_FILE: _token_check,
        reg.MCP_CONFIG_TOML: _codex_check,
        reg.MCP_EXTENSION_BRIDGE: _pi_check,
        reg.MCP_PLUGIN_MANIFEST: _kimi_check,
    }


#: One credential resolver per registry `mcp` kind (`test_mcp_state.py` fails
#: when a kind has none).
MCP_RESOLVERS = _mcp_resolvers()


#: The API's verdict on this device's read token, for this process:
#: (token, "ok" | "rejected" | "unreachable"), or None when nobody asked.
#: Only `probe doctor`, the wizard (`refresh_mcp_token_verdict`) and `probe
#: status --refresh` (`ask_mcp_token_verdict`, recorded only when it answers in
#: time) ask, so a status read anywhere else never touches the network.
_MCP_TOKEN_VERDICT: tuple[str, str] | None = None


def refresh_mcp_token_verdict() -> str | None:
    """Ask the API once whether the read token is still accepted (`/v1/me`, the
    check `probe mcp status` makes). None when there is no token to ask about."""
    token = cli_mcp_token()
    if not token:
        record_mcp_token_verdict(None, None)
        return None
    state = ask_mcp_token_verdict(token)
    record_mcp_token_verdict(token, state)
    return state


def ask_mcp_token_verdict(token: str) -> str:
    """The API's verdict on `token` -- ok | rejected | unreachable -- recording
    nothing. Split from `refresh_mcp_token_verdict` so a caller that bounds the
    wait (`probe status --refresh`) records only an answer that came in time."""
    from probe.cli.wizard.state.token_verify import _verify_read
    from probe.sdk.settings.settings import resolve

    try:
        state, _identity = _verify_read(token, resolve().base_url)
    except Exception:  # noqa: BLE001 - a failed check is "unknown", never "rejected"
        state = "unreachable"
    return state


def record_mcp_token_verdict(token: str | None, state: str | None) -> None:
    """What this process's `check_mcp` reads as the API's verdict on `token`."""
    global _MCP_TOKEN_VERDICT
    _MCP_TOKEN_VERDICT = (token, state) if token and state else None


def mcp_token_rejected() -> bool:
    """The API refused the token this device holds now (asked this process)."""
    token = cli_mcp_token()
    return bool(token) and _MCP_TOKEN_VERDICT == (token, "rejected")


def _sends_held_token(source: str, kind: str) -> bool:
    """Whether this agent's MCP sends the device's held read token, so a
    rejection of that token is ITS rejection. Codex may hold its own OAuth
    login instead; only its synced bearer counts."""
    from probe.foundation.harness_registry import harness_registry as reg

    if kind != reg.MCP_CONFIG_TOML:
        return True
    try:
        from probe.shared.harness.harnesses.codex import config as codex_config

        return codex_config.configured_bearer(CODEX_MCP_NAME) == cli_mcp_token()
    except Exception:  # noqa: BLE001 - unreadable config: do not claim a rejection
        return False


def check_mcp(source: str, *, codex_auth: bool | None = None) -> tuple[str | None, McpCheck | None]:
    """(registry mcp kind, credential check) for one agent. Never raises."""
    from probe.foundation.harness_registry import get_registry

    try:
        kind = get_registry().get(source).mcp
    except Exception:  # noqa: BLE001 - an unknown source offers no MCP
        return None, None
    if kind is None:
        return None, None
    try:
        check = MCP_RESOLVERS[kind](source, codex_auth)
    except Exception as exc:  # noqa: BLE001 - a status must never crash the wizard
        return kind, McpCheck(McpCredential.UNKNOWN, what=f"check failed ({type(exc).__name__})")
    if check.credential == McpCredential.PRESENT and mcp_token_rejected() and _sends_held_token(source, kind):
        return kind, McpCheck(McpCredential.REJECTED)
    return kind, check
from probe.cli.wizard.state.state import CODEX_MCP_NAME  # noqa: E402 -- pieces need each other; the front door loads this one first
