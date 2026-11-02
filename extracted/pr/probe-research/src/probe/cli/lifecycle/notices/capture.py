"""start capture when tracking says one should be running (never fails a command)."""

from __future__ import annotations
import os
from ....sdk import agent_session


def _ensure_capture_notice(invoked_command: str | None) -> None:
    """Start capture if tracking says one should be running. Never fails a command.

    `invoked_command` comes from the root Typer context, not argv: this runs
    before dispatch, and `_invoked_command()`'s argv scan answers for the
    PROCESS (which is `pytest` under the test runner and any wrapper in
    production), not for the command about to run.

    The `session` group is skipped because it owns its own capture decision:
    `status`, `track` and `toggle` heal with the cwd they resolved, and
    `initialize` deliberately abstains (see `_capture_block`). Firing here as
    well would both double the work and OVERRULE that abstention -- the pi
    extension calls `session initialize` immediately before its own spawn.
    """
    if invoked_command == "session":
        return
    try:
        from probe.cli.capture import state as capture_state  # noqa: PLC0415
        from probe.sdk import agent_session  # noqa: PLC0415

        session_id = agent_session.session_id_from_env()
        if session_id:
            capture_state.ensure_capture(session_id, os.getcwd())
    except Exception:  # noqa: BLE001 - a heal must never break a CLI command
        pass
