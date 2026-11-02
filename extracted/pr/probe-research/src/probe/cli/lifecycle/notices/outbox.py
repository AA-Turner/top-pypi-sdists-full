"""the every-command outbox banner: what is queued or dead, re-kick the drainer, lift a stale pause."""

from __future__ import annotations
import os

import typer
from ....sdk.settings.settings import resolve
from ....sdk import session_marker


def _utc_minute(stamp: str) -> str:
    """`2026-10-27T00:17:48.1+00:00` -> `2026-10-27 00:17 UTC` (stamps here are UTC)."""
    return f"{stamp[:16].replace('T', ' ')} UTC"


def _lift_stale_pause(status: dict) -> bool:
    """`outbox_worker.lift_stale_pause` on this command's outbox, reported to
    the backend this command uses. Never raises."""
    try:
        from ....sdk.delivery import outbox as outbox_worker
        from ....sdk.settings.settings import resolve
        from ....sdk.delivery.journal.journal import Journal

        journal = Journal(_conn.spool_dir)
        if not os.path.lexists(journal.paused_file):
            return False  # the every-command path: one stat, no config read
        base_url = resolve(base_url=_conn.base_url).base_url
        return outbox_worker.lift_stale_pause(journal, status, base_url=base_url)
    except Exception:  # noqa: BLE001 -- the banner must never break a command
        return False


def _outbox_notice(*, lift: bool = True) -> None:
    """The every-command outbox banner (2B) + drainer re-kick (3A) + the
    automatic rescue of writes stranded under a dead credential + lifting a
    pause that no longer holds.

    One stat/read of status.json, no locks, never raises: this runs before
    every command, including `probe log` inside training loops. The rescue
    check is one more stat; once per 10 minutes at most it claims its interval
    under a lock, reads the queues' status files and may start a process
    (`outbox_worker.maybe_rescue`). The lift is one more stat; only a marker
    that no longer holds costs the append lock and a report. ``lift`` False
    for `probe outbox ...`, which owns the marker and delivery itself: the
    banner only, no lift, rescue or kick (`pause` over an ended pause must
    not first start the drainer it is about to stop).
    """
    try:
        from ....sdk.delivery.journal.journal import Journal
        from ....sdk.delivery.journal.status_file import auth_blocked_since

        status = Journal.read_status(_conn.spool_dir)
        if not status:
            if lift:
                # ONE-TIME (`journal/failures/restores.py`; delete with it): an outbox with no
                # status file may still hold set-aside writes to put back. Two stats.
                from ....sdk.delivery import outbox as outbox_worker

                outbox_worker.maybe_restore(Journal(_conn.spool_dir))
            return
        failed = status.get("failed") or 0
        pending = status.get("pending") or 0
        blocked = auth_blocked_since(status)
        lifted = lift and not status.get("paused") and _lift_stale_pause(status)
        if lifted and pending and not blocked:
            # An older CLI's endless pause, or one whose end passed: said once,
            # since nothing else will say why uploads started again.
            typer.echo(f"outbox: an earlier `probe outbox pause` has ended — sending {pending} queued write(s)", err=True)
        parts: list[str] = []
        if blocked:
            parts.append(f"auth-blocked since {blocked} — sign in again ({session_marker.WIZARD_HINT})")
        if failed:
            parts.append(f"{failed} dead-lettered")
        banner = bool(parts) or bool(pending and status.get("paused"))
        if banner:
            if pending:
                parts.append(f"{pending} pending")
            if status.get("paused"):
                until = status.get("paused_until")
                parts.append(f"paused until {_utc_minute(until)}" if until else "paused")
                hint = "`probe outbox resume` sends them now"
            else:
                hint = "see `probe outbox status`"
            typer.echo(f"outbox: {'; '.join(parts)} — {hint}", err=True)
        if banner or status.get("blocked_oldest_pending"):
            # The banner's condition, plus writes one queue holds for a
            # credential nothing here has (no banner: a fresh hold clears
            # itself; `stuck_status` reports it once it is an hour old). Whatever is worth
            # interrupting a human for is worth the fleet knowing. This is the
            # only place the STANDING condition is ever observed. A worker
            # already running reports the TRANSITION into paused/auth-blocked
            # (outbox_worker exit codes 4 and 3), but `maybe_spawn` will not fork
            # again while either persists -- so without this, a queue that has
            # been wedged since yesterday is reported by nobody. Rate-limited to once per
            # STUCK_REPORT_INTERVAL_S so a training loop shelling out thousands
            # of times still costs one event.
            #
            # Its OWN try/except, inside the function's: emit_outbox_stuck never
            # raises, but the import can, and a telemetry failure that skipped
            # the _kick_drainer() below would turn reporting a stuck queue into
            # causing one.
            try:
                from ....sdk.settings.settings import resolve
                from probe import analytics as telemetry_mod

                # The RESOLVED backend, not the config file: `probe --base-url
                # https://probe.internal.corp ...` lives on `_conn.base_url` and
                # never reaches the config, so gating on the config alone let a
                # self-host invocation emit. Only reached when the queue is
                # actually stuck, so the resolve() is off the hot path.
                from ....sdk.delivery.journal.paths import default_dir

                telemetry_mod.emit_outbox_stuck(
                    status,
                    auth_blocked_since=auth_blocked_since(status),
                    spool_dir=_conn.spool_dir or str(default_dir()),
                    base_url=resolve(base_url=_conn.base_url).base_url,
                )
            except Exception:  # noqa: BLE001 -- never let a report block the kick
                pass
        if not lift:
            # `probe outbox ...` delivers (or holds) on its own: `pause` over an
            # ended pause must not start a drainer first, nor a rescue.
            return
        if not status.get("paused"):
            # Writes stranded under a dead credential of this account are
            # rescued by themselves (`outbox_worker.maybe_rescue`: one stat,
            # at most a process every 10 minutes), even with this outbox empty
            # (a distributed job's `rank-*` ones). Here, on the CLI's path,
            # never on the SDK's write path.
            from ....sdk.delivery import outbox as outbox_worker

            outbox_worker.maybe_rescue(Journal(_conn.spool_dir), status)
        if (pending or lifted) and not status.get("paused") and not blocked:
            _kick_drainer()
    except Exception:  # noqa: BLE001 -- a broken banner must never break a command
        pass
from probe.cli.connection import _conn, _kick_drainer  # noqa: E402 -- pieces need each other; the front door loads this one first
