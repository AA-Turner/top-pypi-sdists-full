"""the Probe daemon's rows: default, key, who records per agent, this session's reader, its error log."""

from __future__ import annotations
from probe.cli.wizard.state.state import Capabilities


#: Lines of the daemon's device error log `doctor` shows.
DAEMON_ERROR_LINES = 5


def daemon_error_lines(limit: int = DAEMON_ERROR_LINES) -> list[str]:
    """The last lines of the daemon's device-level error log, `<state>/probe/daemon-errors.log`."""
    try:
        from probe.sdk import session_marker

        path = session_marker.state_dir() / "daemon-errors.log"
        with path.open("rb") as handle:
            handle.seek(0, 2)
            size = handle.tell()
            handle.seek(max(0, size - 16384))
            tail = handle.read().decode("utf-8", errors="replace")
    except OSError:
        return []
    return [line for line in tail.splitlines() if line.strip()][-limit:]


def _daemon_rows(caps: Capabilities | None = None) -> list[str]:
    """The Probe daemon (the `daemon` state): default, key, this session, spend,
    its AI libraries and its recent errors.

    Read-only and local. The daemon is the capture daemon's child, so capture being off is named as
    the cause rather than left for the reader to connect.
    """
    from probe.cli.commands.daemon import companion
    from probe.shared.harness import reasoning_summaries
    from probe.cli import wizard as wizard
    from probe.sdk import agent_session, session_marker

    rows = ["Probe daemon"]
    default = session_marker.default_session_state()
    set_by = session_marker.set_by_note()
    rows.append(
        _row("New sessions start", session_marker.state_label(default) + (f" ({set_by})" if set_by else ""))
    )
    rows.append(
        _row(
            "Daemon key",
            "held (read + write; deletes go to the trash only)"
            if wizard.companion_token_held()
            else "none — Who records in the wizard (switch it to the daemon, or Enter on it) approves one",
        )
    )
    rows.extend(_who_records_rows())
    for source in reasoning_summaries.SOURCES:
        if session_marker.recorder(source) == session_marker.RECORDER_DAEMON:
            label = reasoning_summaries.LABELS[source]
            rows.append(_row(f"{label}'s reasoning", reasoning_summaries.doctor_value(source)))
    session_id = agent_session.session_id_from_env()
    if session_id:
        status = session_marker.daemon_status(session_id)
        if status is not None:
            live, reason = status
            rows.append(_row("This session", "daemon" if live == session_marker.DAEMON_LIVE else f"daemon (degraded: {reason})"))
        rows.extend(_reader_rows(session_id))
    # The device's daemon token counter (`daemon/device.json`, UTC days): a meter, no fuse reads it.
    spent = companion.tokens_today()
    rows.append(_row("Model tokens today", "unreadable" if spent is None else f"{spent:,} (UTC day)"))
    read_spent = _reader_tokens_today()
    if read_spent:
        rows.append(_row("Reader tokens today", f"{read_spent:,} (UTC day)"))
    if caps is not None and caps.daemon_ai_libraries is not None:
        rows.append(
            _row(
                "AI libraries",
                "missing — Who records in the wizard (switch it to the daemon, or Enter on it) installs them"
                if caps.daemon_ai_libraries == "missing"
                else f"installed (Pydantic AI {caps.daemon_ai_libraries})",
            )
        )
    errors_seen = daemon_error_lines()
    for index, line in enumerate(errors_seen):
        rows.append(_row("Recent errors" if index == 0 else "", line[:200]))
    rows.append(_row("Diagnostic reports", _diagnostic_reports()))
    return rows


def _diagnostic_reports() -> str:
    """Whether the daemon and the Probe service send the Probe team a report
    when they misbehave (`probe.shared.reports`), and the last one sent."""
    try:
        from probe.shared import reports as report

        return report.doctor_row()
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return "unknown"


def _who_records_rows() -> list[str]:
    """One "Who records" row per coding agent set up here, and for an agent whose
    daemon profile is its package's settings entry (pi), the package's version
    against the floor the daemon needs and whether a project overrides it."""
    from pathlib import Path

    from probe.shared.harness.harnesses import pi as pi_config
    from probe.cli import wizard as wizard
    from probe.foundation.harness_registry import get_registry
    from probe.sdk import session_marker

    daemon = session_marker.RECORDER_DAEMON
    machine_daemon = any(session_marker.recorder(s) == daemon for s in wizard.RECORDER_SOURCES)
    rows: list[str] = []
    for harness in get_registry().installable():
        if harness.id not in wizard.RECORDER_SOURCES:
            continue
        by_settings = harness.lean_profile == wizard.LEAN_SETTINGS_FILTER
        profile = pi_config.entry_profile() if by_settings else None
        if by_settings and profile is None:
            continue  # pi is not set up here: nothing records for it
        who = session_marker.recorder(harness.id)
        value = wizard.RECORDER_WORDS.get(who, who)
        if profile is not None and profile not in (who, pi_config.PROFILE_TRACKING_OFF):
            value += f" (but its Probe package is on the {profile} profile: switch Who records again)"
        if machine_daemon and who != daemon:
            value += " — can use the daemon now: `probe wizard` › Who records, Enter"
        rows.append(_row(f"Who records ({harness.label})", value))
        if not by_settings or not (who == daemon or machine_daemon):
            continue
        version = pi_config.installed_package_version()
        floor = ".".join(str(part) for part in pi_config.DAEMON_MIN_PACKAGE_VERSION)
        have = ".".join(str(part) for part in version) if version else "unknown"
        ready = version is not None and version >= pi_config.DAEMON_MIN_PACKAGE_VERSION
        rows.append(_row(f"{harness.label} Probe package", have if ready else f"{have} (the daemon needs {floor}+)"))
        merged = pi_config.merged_package_entry(cwd=Path.cwd())
        if who == daemon and merged.installed and merged.scope == "project":
            rows.append(_row("", f"this folder's .pi/settings.json overrides {harness.label}'s Probe package"))
    return rows


def _reader_tokens_today() -> int:
    from probe.daemon import store as daemon_store

    try:
        return daemon_store.device_tokens_today(lane=daemon_store.LANE_READ)
    except Exception:  # noqa: BLE001 -- a diagnostic never fails on a counter
        return 0


def _reader_rows(session_id: str) -> list[str]:
    """This session's reader (daemon reads): its state as the researcher's line,
    how its turns ended and how the main agent's asks ended. Read-only: the
    store is opened read-only, the mailbox only listed."""
    import sqlite3

    from probe.shared import mailbox
    from probe.daemon.store.store import store_path

    rows: list[str] = []
    status = mailbox.read_status(session_id)
    state = status.get("state")
    if state:
        line = ("running" if state == mailbox.Status.OK else
                mailbox.researcher_line(state, reason=status.get("reason", "")))
        rows.append(_row("Reader", line or state))
    path = store_path(session_id)
    if not path.is_file():
        return rows
    try:
        db = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=1.0)
        try:
            turns = dict(db.execute("SELECT coalesce(outcome, 'running'), count(*) FROM read_turns GROUP BY 1"))
            asks = dict(db.execute("SELECT state, count(*) FROM read_asks GROUP BY 1"))
        finally:
            db.close()
    except sqlite3.Error:  # an older store has no reader tables, or it is busy
        return rows
    if turns:
        rows.append(_row("Reader turns", " · ".join(f"{n} {k}" for k, n in sorted(turns.items()))))
    if asks:
        rows.append(_row("Asks", " · ".join(f"{n} {k}" for k, n in sorted(asks.items()))))
    return rows


def _format_age(seconds: float | None) -> str:
    if seconds is None:
        return "unknown age"
    if seconds < 3600:
        return f"{int(seconds // 60)}m ago"
    if seconds < 86400:
        return f"{int(seconds // 3600)}h ago"
    return f"{int(seconds // 86400)}d ago"
from probe.cli.wizard.doctor.report import summary  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.diagnosis import _row  # noqa: E402 -- pieces need each other; the front door loads this one first
