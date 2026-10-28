"""Probe staff changed a setting on this machine: apply it once (research-os control/074).

Staff can set ONE setting on ONE device, once, and only toward quieter. v1 has one,
`session_default`, the machine's default for new sessions, to `off` or `read`. The
server answers this device's CLI token with `X-Probe-Settings-Requested`, whichever
of our clients gets that answer leaves the mark (`probe._shared.settings_request`),
and `apply_pending`, run before a `probe` command (`probe.cli.main.
_settings_request_notice`), acts on it:

    lock        one process at a time (`LOCK_NAME`, non-blocking: held -> skip)
    fetch       `GET /v1/client/settings-request` {requested_at, setting, value};
                404 (none open for this token and device) -> the mark goes
    once        `APPLIED_NAME` already names this `requested_at` -> re-send its
                report only, never apply again (so a lost answer cannot undo a
                change the person made since)
    allow-list  a setting or value this CLI does not know (`ALLOWED`), or one that
                is not quieter than `on`, is reported `unsupported` and settled:
                a server bug or a stolen staff login cannot turn recording on
    default     `session_marker.lower_default_state`: under the config lock, the
                stored default moves only if that is quieter than it is (a machine
                already `off` asked for `read` stays `off`), recording
                `set_by: probe-staff`. An unreadable config writes nothing and
                keeps the mark (the next window tries again)
    claim       `APPLIED_NAME` names this `requested_at` BEFORE anything changes;
                when it cannot be written nothing is changed (`FAILED`), so a
                change is never made that a later window could make again
    sessions    every session whose switch is louder than the value moves to it
                (`session_marker.lower_session_state`: compared and written under
                the session's own lock, an explicit choice, so a reload keeps it
                and a switch the person moves at that moment is never made
                louder). One whose write fails is kept `pending` and retried on
                the next windows, at most `MAX_ATTEMPTS` in all, before the report
                goes without it; sessions that moved are never touched again
    record      the report (and what is pending) once the moves are done; then,
                for `off`, the Probe service is told (`capture_switched`) for the
                newest `MAX_SWITCH_CALLS` within `SWITCH_BUDGET_S`; it looks at
                the rest on its own poll
    report      `POST /v1/client/settings-request/applied`; 200 or 404 clears the
                mark, anything else keeps it (next window: report only). When the
                server has nothing open any more (staff canceled it, it expired),
                a report that never landed is sent once all the same: the server
                closes that row `applied`, so it says what happened

The record keeps a phase (claimed, default, done): a window stopped after the
claim applies afresh (nothing changed), one stopped after the default moves the
sessions, one done only re-sends.

`PROBE_SESSION_STATE` (or the older `PROBE_SESSION_TRACKING`) set here outranks the
file: the file is still written and the report says `env_shadowed`.

Sessions the person turns back on afterwards stay on: nothing applies twice.
"""

from __future__ import annotations

import contextlib
import json
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any

from probe._compat import UTC, StrEnum
from probe.sdk import session_marker

#: Where the machine fetches the open request.
FETCH_PATH = "/v1/client/settings-request"
#: Where it reports what it did; the report closes the request.
APPLIED_PATH = "/v1/client/settings-request/applied"
#: Held while one process applies (beside the mark, in the state folder).
LOCK_NAME = "remote-settings.lock"
#: The last request applied here and its report: a retry re-sends, never re-applies.
APPLIED_NAME = "remote-settings-applied.json"
#: The Probe service is told about at most this many switched sessions ...
MAX_SWITCH_CALLS = 64
#: ... within this long in all; it looks at the rest on its own poll.
SWITCH_BUDGET_S = 5.0
#: The most session ids one report carries (the server keeps as many).
MAX_REPORTED_SESSIONS = 2000
#: Windows a session whose switch could not be written is retried in, before the
#: report goes without it.
MAX_ATTEMPTS = 3


class Setting(StrEnum):
    """What staff may change. The server's `app/client_version/settings_requests.py::
    Setting` is the same list (`tests/unit/test_settings_requests.py`)."""

    SESSION_DEFAULT = "session_default"


#: Per setting, the values this CLI applies, as the switch's words: only ever
#: quieter than `on`. Anything else the server sends is `unsupported`.
ALLOWED: dict[Setting, tuple[str, ...]] = {
    Setting.SESSION_DEFAULT: ("off", "read"),
}


@dataclass
class Report:
    """What `APPLIED_PATH` is told."""

    requested_at: str
    default_changed: bool = False
    sessions_moved: int = 0
    moved_sessions: list[str] = field(default_factory=list)
    env_shadowed: bool = False
    unsupported: bool = False


class Outcome(StrEnum):
    """What one `apply_pending` call did (the tests read it). RESENT and
    UNSUPPORTED say nothing about whether the report landed: the mark does."""

    NONE = "none"  # no fresh mark, or the lock was held
    NOT_OPEN = "not_open"  # the server has nothing open for this machine
    UNREACHED = "unreached"  # no answer; the mark stays
    APPLIED = "applied"  # applied now and reported
    APPLIED_UNREPORTED = "applied_unreported"  # applied now; the report did not land
    PENDING = "pending"  # a session's switch could not be written yet; retried, not reported
    RESENT = "resent"  # applied before; the report was sent again
    UNSUPPORTED = "unsupported"  # outside the allow-list; reported
    FAILED = "failed"  # nothing could be recorded or written; nothing changed


def _state_dir():
    from probe import version_policy

    return version_policy.state_dir()


@contextlib.contextmanager
def _locked():
    """True inside when this process holds the apply lock, False when another does."""
    from probe._shared import oscompat

    path = _state_dir() / LOCK_NAME
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a+b") as handle:
        try:
            oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        except OSError:
            yield False
            return
        try:
            yield True
        finally:
            with contextlib.suppress(OSError):
                oscompat.flock(handle.fileno(), oscompat.LOCK_UN)


def _applied_record() -> dict | None:
    try:
        data = json.loads((_state_dir() / APPLIED_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) and isinstance(data.get("report"), dict) else None


#: Where an apply got to, in `APPLIED_NAME`: the claim (nothing changed yet), the
#: default written, every session tried.
PHASE_CLAIMED = "claimed"
PHASE_DEFAULT = "default"
PHASE_DONE = "done"


def _record(report: Report, *, phase: str, pending: list[str] | None = None, attempts: int = 1,
            reported: bool = False, moving_since: float | None = None) -> bool:
    """Save the request's record: True when it is on disk. Never raises.
    `moving_since` (the default phase): when the sessions started to be moved."""
    try:
        from probe import version_policy

        return bool(version_policy.atomic_write_json(
            _state_dir() / APPLIED_NAME,
            {"requested_at": report.requested_at, "report": asdict(report), "phase": phase,
             "pending": list(pending or []), "attempts": attempts, "reported": reported,
             "moving_since": moving_since},
        ))
    except Exception:  # noqa: BLE001
        return False


def _forget_claim() -> None:
    with contextlib.suppress(OSError):
        (_state_dir() / APPLIED_NAME).unlink()


def _allowed_state(setting: object, value: object) -> str | None:
    """The stored state staff's `value` names, when this CLI applies it; else None."""
    try:
        picked = Setting(str(setting))
    except ValueError:
        return None
    if not isinstance(value, str) or value not in ALLOWED[picked]:
        return None
    state = session_marker.state_for_label(value)
    return state if state in (session_marker.STATE_OFF, session_marker.STATE_READ_ONLY) else None


def _tell_service(state: str, session_ids: list[str]) -> None:
    """For `off`, the Probe service looks at these switches now
    (`capture_switched`), newest first, within MAX_SWITCH_CALLS and
    SWITCH_BUDGET_S; its own poll finds the rest. `read` never stopped capture,
    so there is nothing to tell. Never raises."""
    if state != session_marker.STATE_OFF or not session_ids:
        return
    with contextlib.suppress(Exception):
        from probe.cli import service_calls

        deadline = time.monotonic() + SWITCH_BUDGET_S
        for sid in session_ids[:MAX_SWITCH_CALLS]:
            if time.monotonic() >= deadline:
                return
            if service_calls.capture_switched(sid, off=True) is None:
                return  # no service answers: nothing records these sessions here now


def move_sessions(state: str, session_ids: list[str] | None = None) -> tuple[list[str], list[str]]:
    """Switch every session louder than `state` to it (`lower_session_state`),
    newest first, or only `session_ids`: (the ids that moved, those whose write
    failed)."""
    moved: list[str] = []
    failed: list[str] = []
    for sid in session_marker.decided_sessions() if session_ids is None else session_ids:
        result = session_marker.lower_session_state(sid, state)
        if result is True:
            moved.append(sid)
        elif result is False:
            failed.append(sid)
    return moved, failed


def _send(client: Any, report: Report) -> bool | None:
    """True: the server took it; None: it has nothing open (closed or replaced);
    False: no answer."""
    from probe.sdk.errors import NotFoundError

    try:
        client.transport.post(APPLIED_PATH, asdict(report))
        return True
    except NotFoundError:
        return None
    except Exception:  # noqa: BLE001 -- no answer: the next window re-sends the report
        return False


def _switch_written(session_id: str) -> float:
    """When the session's switch file was last written (0 when it has none)."""
    newest = 0.0
    for suffix in (".state", ".tracking", ".off"):
        with contextlib.suppress(OSError):
            newest = max(newest, (session_marker.sessions_dir() / (session_id + suffix)).stat().st_mtime)
    return newest


def _report_from(done: dict) -> Report:
    return Report(**{k: v for k, v in done["report"].items() if k in Report.__dataclass_fields__})


def _apply(answer: dict, now: datetime) -> tuple[Report, list[str]] | None:
    """Apply the fetched request, once: (its report, sessions still pending), or
    None when nothing could be changed or recorded (the mark stays)."""
    report = Report(requested_at=str(answer["requested_at"]))
    state = _allowed_state(answer.get("setting"), answer.get("value"))
    if state is None:
        report.unsupported = True
        return (report, []) if _record(report, phase=PHASE_DONE) else None
    if not _record(report, phase=PHASE_CLAIMED):  # before anything changes
        return None
    try:
        _before, report.default_changed = session_marker.lower_default_state(
            state, by=session_marker.SET_BY_STAFF, at=now.astimezone(UTC).isoformat().replace("+00:00", "Z")
        )
    except Exception:  # noqa: BLE001 -- an unreadable config: nothing changed, so nothing is claimed
        _forget_claim()
        return None
    except BaseException:  # a Ctrl-C while the config lock waits: nothing changed either
        _forget_claim()
        raise
    _record(report, phase=PHASE_DEFAULT, moving_since=time.time())
    return _move_all(report, state)


def _move_all(report: Report, state: str, untouched_since: float | None = None) -> tuple[Report, list[str]]:
    """Every session louder than `state`, moved; the report recorded, then the
    Probe service told. With `untouched_since`, only sessions whose switch was
    last written before then: one written since was either moved by the window
    that stopped, or moved by the person, and neither is moved again."""
    sessions = None
    if untouched_since is not None:
        sessions = [sid for sid in session_marker.decided_sessions() if _switch_written(sid) < untouched_since]
    moved, failed = move_sessions(state, sessions)
    report.moved_sessions = list(dict.fromkeys(report.moved_sessions + moved))[:MAX_REPORTED_SESSIONS]
    report.sessions_moved += len(moved)
    report.env_shadowed = session_marker.state_env_override() is not None
    if not _record(report, phase=PHASE_DONE, pending=failed):
        failed = []  # nothing on disk to retry from: report what moved
    _tell_service(state, moved)
    return report, failed


def _resume(answer: dict, done: dict) -> tuple[Report, list[str]] | None:
    """A matching record from an earlier window. Claimed only: nothing changed,
    apply afresh (None). Default written: the window stopped while (or before)
    moving the sessions; move those whose switch nobody has written since it
    began. Done: retry only sessions whose switch could not be written (the ones
    that moved stay as the person has them since)."""
    phase = done.get("phase", PHASE_DONE)
    if phase == PHASE_CLAIMED:
        _forget_claim()
        return None
    report = _report_from(done)
    state = _allowed_state(answer.get("setting"), answer.get("value"))
    if state is None:
        return report, []
    if phase == PHASE_DEFAULT:
        since = done.get("moving_since")
        return _move_all(report, state, float(since) if isinstance(since, (int, float)) else 0.0)
    pending = [sid for sid in done.get("pending") or [] if isinstance(sid, str)]
    if not pending:
        return report, []
    moved, failed = move_sessions(state, pending)
    report.moved_sessions = (report.moved_sessions + moved)[:MAX_REPORTED_SESSIONS]
    report.sessions_moved += len(moved)
    attempts = int(done.get("attempts") or 1) + 1
    if attempts >= MAX_ATTEMPTS or not _record(report, phase=PHASE_DONE, pending=failed, attempts=attempts):
        _record(report, phase=PHASE_DONE, attempts=attempts)
        failed = []
    _tell_service(state, moved)
    return report, failed


def _report_and_clear(client: Any, report: Report) -> bool | None:
    """Send the report; when the server took it (or has nothing open), forget the
    mark and remember it was sent."""
    from probe._shared import settings_request

    sent = _send(client, report)
    if sent is not False:
        settings_request.clear()
        done = _applied_record() or {}
        _record(report, phase=PHASE_DONE, attempts=int(done.get("attempts") or 1), reported=True)
    return sent


def _send_unreported(client: Any) -> None:
    """The server has nothing open for this machine any more (staff canceled it,
    it expired, or it was closed): a change this machine made whose report never
    landed is sent once, so the row says what happened (the server closes a
    canceled or expired row `applied` for the requested_at it was fetched with)."""
    done = _applied_record()
    if done is None or done.get("reported") or done.get("phase", PHASE_DONE) == PHASE_CLAIMED:
        return
    report = _report_from(done)
    _send(client, report)
    _record(report, phase=done.get("phase", PHASE_DONE), attempts=int(done.get("attempts") or 1), reported=True)


def apply_pending(client: Any, *, base_url: str | None = None, now: datetime | None = None) -> Outcome:
    """Apply staff's open settings request for this machine, once, and report it.
    `client` is a signed-in `probe` client of this machine's own token. Never
    raises."""
    from probe._shared import settings_request
    from probe.sdk.errors import NotFoundError

    if not settings_request.fresh():
        return Outcome.NONE
    with _locked() as held:
        if not held:
            return Outcome.NONE
        try:
            # One try: the next window is the retry, and a command must not wait
            # out a back-off for a request it never asked about.
            answer = client.transport.request("GET", FETCH_PATH, idempotent=False).json()
        except NotFoundError:
            _send_unreported(client)
            settings_request.clear()
            return Outcome.NOT_OPEN
        except Exception:  # noqa: BLE001 -- no answer, a 5xx, a refusal: the next window retries
            return Outcome.UNREACHED
        if not isinstance(answer, dict) or not answer.get("requested_at"):
            return Outcome.UNREACHED
        done = _applied_record()
        if done is not None and done.get("requested_at") == answer["requested_at"]:
            resumed = _resume(answer, done)
            if resumed is not None:
                report, pending = resumed
                if pending:
                    return Outcome.PENDING
                _report_and_clear(client, report)
                return Outcome.RESENT
        applied = _apply(answer, now or datetime.now(UTC))
        if applied is None:
            return Outcome.FAILED
        report, pending = applied
        _tell_person(answer, report)
        if pending:
            _emit(report, answer, False, base_url)
            return Outcome.PENDING
        sent = _report_and_clear(client, report)
        _emit(report, answer, sent, base_url)
        if report.unsupported:
            return Outcome.UNSUPPORTED
        return Outcome.APPLIED if sent is not False else Outcome.APPLIED_UNREPORTED


def _tell_person(answer: dict, report: Report) -> None:
    """One stderr line, only when someone is watching (a terminal): a command a
    hook runs in the background has nobody to read it, and `probe session
    default` / `probe doctor` say who set the default anyway."""
    if report.unsupported or not (report.default_changed or report.sessions_moved):
        return
    with contextlib.suppress(Exception):
        if not sys.stderr.isatty():
            return
        word = str(answer.get("value"))
        parts = []
        if report.default_changed and report.env_shadowed:
            variable = "PROBE_SESSION_STATE" if os.environ.get("PROBE_SESSION_STATE") else "PROBE_SESSION_TRACKING"
            parts.append(f"the default for new sessions is now {word}, but {variable} still decides here")
        elif report.default_changed:
            parts.append(f"new sessions on this machine start {word}")
        if report.sessions_moved:
            parts.append(f"{report.sessions_moved} session(s) switched to {word}")
        print(
            f"Probe staff changed this machine's Probe setting: {'; '.join(parts)}. "
            "Change it any time: `probe session default on`, `probe session state on`.",
            file=sys.stderr,
        )


def _emit(report: Report, answer: dict, sent: bool | None, base_url: str | None) -> None:
    with contextlib.suppress(Exception):
        from probe._shared import telemetry

        telemetry.emit_settings_remote_applied(
            setting=str(answer.get("setting")),
            value=str(answer.get("value")),
            default_changed=report.default_changed,
            sessions_moved=report.sessions_moved,
            env_shadowed=report.env_shadowed,
            unsupported=report.unsupported,
            reported=sent is not False,
            base_url=base_url,
        )


__all__ = [
    "ALLOWED",
    "APPLIED_NAME",
    "APPLIED_PATH",
    "FETCH_PATH",
    "LOCK_NAME",
    "MAX_ATTEMPTS",
    "Outcome",
    "Report",
    "Setting",
    "apply_pending",
    "move_sessions",
]
