"""after a write exited 0: the owed-summary reminder and the session's status-line label."""

from __future__ import annotations
import os
from ...sdk import agent_session, session_marker


def _remind_summary(args: list[str], *, offline: bool = False) -> None:
    """After a write exited 0: a create or a conclusion makes a summary owed
    (`owed.after_write`), FIRST, so a Ctrl-C during the reads below cannot lose
    it; the first write of a session landing on a project or experiment whose
    summary it has not checked out says so, once (`summary_cli.remind`); and
    the first one landing on an entity prints its note's opening
    (`first_touch.show`) -- not when the write was only queued (`offline`):
    Probe did not answer it, and would not answer the read."""
    from ..commands.notes import first_touch
    from ...shared.notes import owed
    from ...shared.notes.summary.first_write import remind

    for step in (lambda: owed.after_write(args), lambda: remind(args),
                 lambda: None if offline else first_touch.show(args)):
        try:
            step()
        except (Exception, KeyboardInterrupt):  # noqa: BLE001 -- a reminder
            return


def _label_session() -> str | None:
    """This agent session, when its status line shows a project: the cheap checks
    first, so a shell with no session or no status line imports nothing more. Not
    under the daemon: it stamps its own commands after their logbook line."""
    if os.environ.get("PROBE_DAEMON_SESSION"):
        return None
    session_id = agent_session.session_id_from_env()
    if not session_id or not session_marker.valid_session_id(session_id):
        return None
    return session_id if session_marker.marker_path(session_id).is_file() else None


def _label_status_line(args: list[str]) -> None:
    """The agent's own write -- inline mode, `--directed`, a session the daemon
    does not record -- names its project on the status line, as the daemon's do
    (`probe.daemon.session.scope`). Never raises into the command's exit, Ctrl-C during
    the lookup included: the command already did its job."""
    session_id = _label_session()
    if session_id is None:
        return
    try:
        from probe.daemon.session import scope

        scope.stamp_from_cli(args, session_id, lambda: _client(raise_permanent=False))
    except (Exception, KeyboardInterrupt):  # noqa: BLE001 -- a label
        pass


def _label_status_line_soon(ref: str | None) -> None:
    """`exec`'s run is open and its job may run for hours: name the run's project
    now, on a thread the job's process keeps alive, not when the job exits."""
    session_id = _label_session()
    if session_id is None or not ref:
        return

    def label() -> None:
        try:
            from probe.daemon.session import scope

            scope.stamp_ref_from_cli(session_id, ref, lambda: _client(raise_permanent=False))
        except Exception:  # noqa: BLE001 -- a label
            pass

    import threading

    threading.Thread(target=label, name="probe-status-line-label", daemon=True).start()
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
