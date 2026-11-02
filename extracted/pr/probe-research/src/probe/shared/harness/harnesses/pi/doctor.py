"""pi's diagnosis: the two ways doctor can see pi capture silent."""

from __future__ import annotations
import os


def _pi_capture_rows() -> list[str]:
    """Why capture may be silent on pi, in the two ways doctor can actually see.

    THE FILTER IS THE CONDITION THAT COST A CUSTOMER SIX TRANSCRIPTS. pi's
    `packages` entry takes an `extensions` filter, and a filter that does not
    name our entry point loads the package's skills and its MCP manifest but
    not `index.ts` -- so the skills appear, the MCP tools answer, `probe
    session status` says tracking is on, and nothing ever spawns a daemon.
    Every other signal on the machine reads healthy. This row is the only
    place that condition is visible, which is the whole reason it exists.

    `PI_SESSION_ID` is read directly rather than through
    `agent_session.session_id_from_env()`, which is the resolver everywhere
    else. That resolver answers for whichever agent it DETECTS, and this
    function has already been narrowed to pi by the caller -- so on a machine
    where `PROBE_AGENT=pi` is exported into a Claude Code shell it would hand
    back a Claude Code session id, and the row beneath would report pi's
    capture state for a session pi never had. Naming pi's own variable here
    cannot attribute another agent's session to pi; it can only fall silent,
    which is the safe direction for a row about a session that is not running.

    Fail-soft like every other helper in this module: a diagnostic must never
    be the thing that breaks, so an unreadable settings file or an unaskable
    daemon question drops its row rather than raising through the report.
    """
    import os

    from probe.cli.capture import state as capture_state
    from probe.shared.harness.harnesses import pi as pi_config

    rows: list[str] = []
    try:
        # The session's cwd, so a PROJECT-scope filter is reported exactly as a
        # global one is -- pi applies both, and reporting only the global file
        # would name the wrong file to edit.
        entry = pi_config.merged_package_entry(cwd=os.getcwd())
    except Exception:  # noqa: BLE001 -- diagnostics must never fail the report
        entry = None
    if entry is not None and entry.installed and entry.extension_filtered_out:
        rows.append(
            _row(
                "pi extension",
                f"filtered out in {entry.scope} settings.json; "
                "capture relies on the CLI fallback",
            )
        )

    session_id = os.environ.get("PI_SESSION_ID", "")
    if session_id:
        try:
            state = capture_state.session_capture_state(session_id, "pi")
        except Exception:  # noqa: BLE001 -- see above
            state = None
        if state is not None:
            rows.append(_row("Capture (this session)", state.reason))
    return rows
from probe.shared.harness.diagnosis import _row  # noqa: E402 -- pieces need each other; the front door loads this one first
