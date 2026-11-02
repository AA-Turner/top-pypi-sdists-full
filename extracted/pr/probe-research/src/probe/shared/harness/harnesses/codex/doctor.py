"""Codex's diagnosis: the Codex hooks section and a read token it holds that this device replaced."""

from __future__ import annotations
from probe.shared.harness.harnesses.codex import config as codex_config
from probe.cli.wizard.state.state import Capabilities


def codex_hook_rows(caps: Capabilities) -> list[str]:
    """The "Codex hooks" section when Codex is installed (asks Codex, ~0.2s), else none.

    Codex skips a hook it has not approved without a word, and a Probe update
    that changes a hooks.json entry needs that approval again: the one failure
    no other row can see, because nothing of Probe's runs to report it.
    """
    # Whenever Codex is installed, whichever agent this report is for: a plain
    # terminal reports for Claude Code, and that is where someone checks.
    if not caps.codex_available:
        return []
    from probe.shared.harness.harnesses.codex import hooks as codex_hooks
    from probe.sdk import session_marker

    lines = codex_hooks.rows(codex_hooks.status(), _row)
    # A state this terminal sets, which Codex's hooks will not see (issue 3620).
    if codex_hooks.launch_env_unreadable() and session_marker.state_env_override() is not None:
        lines.append(_row("Session state", codex_hooks.ENV_WARNING))
    return lines


def stale_codex_token_warning() -> str | None:
    """Codex holding a read token this device has already replaced.

    `codex mcp list` reports `bearer_token` for ANY header, so Codex's own
    status cannot tell a current credential from a revoked one -- it says
    authenticated either way, and every call 401s. Comparing the configured
    header against the token we hold is the only local signal there is.

    Silent whenever either side is unknown: no entry, no stored token, or an
    unreadable config is not evidence of drift.
    """
    from probe.cli.wizard.state.state import CODEX_MCP_NAME

    configured = codex_config.configured_bearer(CODEX_MCP_NAME)
    if not configured:
        return None
    from probe.shared.harness.mcp_token import current_mcp_token

    held = current_mcp_token()
    if not held or configured == held:
        return None
    # NAME THE OUTCOME, NOT ONE COMMAND. The first version of this line said
    # "re-run `probe wizard` to re-point it" while the wizard could not: its
    # repair sat behind two gates that both close in exactly this state (see
    # the work-list entry in main.py). The wizard does it now, and the wording
    # below stays true even if the repair moves again, because it says what
    # will happen rather than which command owns it.
    return (
        "the Codex MCP is using an older read token than this device holds; "
        "run `probe wizard` to re-point it"
    )
from probe.shared.harness.diagnosis import _row  # noqa: E402 -- pieces need each other; the front door loads this one first
