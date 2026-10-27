"""The Probe service's state in PostHog: what one machine's service is doing,
with nobody asking.

    service.started   once discovery ends: its version, how the last one ended
    service.state     at start, every STATE_EVERY_S, and when something that
                      matters changes (at most once per CHANGE_MIN_S)
    service.stopped   in `Service.stop`: why, and how long it ran
    lifeboat.acted    the lifeboat rescued this machine (plan fool-proof-updates
                      B5): its `acted.json`, looked for at the first tick and
                      after each update cycle, sent once (`acted_snapshot`)
                      and then deleted; the lifeboat itself sends nothing

`snapshot` is the ONLY way state reaches an event: an allow-list of counts,
booleans, versions, ages and members of named enums. `service.status` itself
carries session ids, run names, job ids, plugin folders and update error
text, so no part of it is ever forwarded whole (`tests/test_service_statepost.py`
feeds it all of those and checks none gets out).

Consent is a machine family's (`Watch.machine_consent`): every session whose
agent runs allows it, else the login shell does; the service's own environment
is clean and never carries a person's `PROBE_TELEMETRY=off`. It is asked again
whenever the sessions change, and `service.stopped` re-reads the sessions it
has. The outbox part goes only where its writes were going: every write it
counts (queued, dead-lettered, a multipart upload, discarded), in every outbox
root, pinned to Probe's hosted service (`OUTBOX_UNPROVEN` otherwise). Each
file is read once and remembered by its size and mtime (`PinCache`).

Its own timer, never the watch's scan: the scan stops while an update hands
over, which is exactly when an update stuck half way should be seen. It looks
every few seconds until `service.started` is sent, so a service that runs for
twenty seconds is still seen. `PROBE_SERVICE_REPORTS=0` (the test suite's)
turns it off, as it does the watch.
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import platform
import re
import sys
import time
from pathlib import Path
from typing import Any, Awaitable, Callable, Mapping

from . import protocol
from .watch import (
    CREDENTIAL_KEYS,
    OUTBOX_TIMEOUT_S,
    Family,
    _count,
    _on_daemon_thread,
    decide_machine,
    reports_enabled,
)

#: How often the timer looks (cheap: in-memory `public()`s and a digest).
STATE_TICK_S = 60.0
#: Until `service.started` is sent, it looks this often.
START_TICK_S = 5.0
#: `service.state` at least this often.
STATE_EVERY_S = 3600.0
#: A change sends `service.state` at most this often.
CHANGE_MIN_S = 600.0
#: The outbox's status files are read at most this often (on a thread).
OUTBOX_EVERY_S = 300.0
#: Files `PinCache` remembers; an outbox with more is not shown to be ours.
PIN_CACHE_MAX = 200_000
#: The outbox part, when its writes' server cannot be shown to be ours.
OUTBOX_UNPROVEN = "unproven_destination"

EVENT_STARTED = "service.started"
EVENT_STATE = "service.state"
EVENT_STOPPED = "service.stopped"
EVENT_LIFEBOAT = "lifeboat.acted"
#: The only events `telemetry.emit_service_event` sends.
SERVICE_EVENTS = frozenset({EVENT_STARTED, EVENT_STATE, EVENT_STOPPED, EVENT_LIFEBOAT})


def _values(cls: type) -> frozenset:
    return frozenset(v for k, v in vars(cls).items() if k.isupper() and isinstance(v, str))


SERVICE_STATES = _values(protocol.State)
WORKER_STATES = _values(protocol.WorkerState)
STEP_STATES = _values(protocol.StepState)
UPDATE_STEPS = _values(protocol.UpdateStep)
APP_RESULTS = protocol.APP_RESULTS
STOP_REASONS = _values(protocol.StopReason)
CHECK_TRIGGERS = protocol.CHECK_TRIGGERS
DEFER_REASONS = _values(protocol.DeferReason)
FAMILIES = _values(Family)
KEY_ANSWERS = frozenset({"ok", "refused", "unknown"})
KEY_KINDS = frozenset(kind for kind, _, _ in CREDENTIAL_KEYS)
#: How the service before this one ended without stopping (`watch.last_run`).
LAST_RUN_ENDINGS = frozenset({"crashed", "unclean_exit"})
BLOCKED_REASONS = frozenset({"auth_blocked", "credential_refused", "held"})
_ERROR_KIND = re.compile(r"^[A-Z][A-Za-z0-9_]{0,63}$")
_VERSION = re.compile(r"^[0-9][0-9A-Za-z.+-]{0,31}$")
#: A lifeboat's `reason` (the hand-off's own word, `behind`, `service_down`, ...):
#: a lower-case token, never free text.
_REASON = re.compile(r"^[a-z][a-z0-9_]{0,31}$")
#: What ran it: the wrapper's triggers, or `lifeboat` (the stage-1 trigger
#: `handoff.py` records in `acted.json` for its own rescues).
LIFEBOAT_TRIGGERS = frozenset({"keeper", "session", "cli", "lifeboat"})


def _enum(value: object, allowed: frozenset) -> str | None:
    """``value`` when it is one of ``allowed``, else None: never free text."""
    return value if isinstance(value, str) and value in allowed else None


def _version(value: object) -> str | None:
    return value if isinstance(value, str) and _VERSION.fullmatch(value) else None


def _age_h(at: object, now: float) -> float | None:
    """Hours since ``at`` (epoch seconds, or an ISO stamp), else None."""
    if isinstance(at, (int, float)) and not isinstance(at, bool):
        return round(max(0.0, now - float(at)) / 3600.0, 2)
    if isinstance(at, str):
        from datetime import datetime, timezone

        try:
            parsed = datetime.fromisoformat(at)
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return round(max(0.0, now - parsed.timestamp()) / 3600.0, 2)
    return None


def _harnesses() -> frozenset:
    try:
        from probe.harness.registry import get_registry

        return frozenset(get_registry().ids())
    except Exception:  # noqa: BLE001 -- none known: every harness reads `other`
        return frozenset()


def _update(update: object, now: float) -> dict:
    update = update if isinstance(update, Mapping) else {}
    last = update.get("last_result") if isinstance(update.get("last_result"), Mapping) else {}
    steps = last.get("steps") if isinstance(last.get("steps"), Mapping) else {}
    app = update.get("app") if isinstance(update.get("app"), Mapping) else {}
    app_last = app.get("last") if isinstance(app.get("last"), Mapping) else {}
    deferred = update.get("deferred")
    return {
        "update_enabled": bool(update.get("enabled")),
        "update_in_progress": bool(update.get("in_progress")),
        "update_step": _enum(update.get("step"), UPDATE_STEPS),
        "update_last_ok": last.get("ok") if isinstance(last.get("ok"), bool) else None,
        "update_last_trigger": _enum(last.get("trigger"), CHECK_TRIGGERS),
        "update_last_steps": {
            step: _enum((state or {}).get("state") if isinstance(state, Mapping) else None, STEP_STATES)
            for step, state in steps.items() if step in UPDATE_STEPS
        } or None,
        "update_last_check_age_h": _age_h(update.get("last_check"), now),
        "update_deferred": _enum(deferred.get("reason") if isinstance(deferred, Mapping) else deferred,
                                 DEFER_REASONS),
        "update_deferred_age_h": _age_h(update.get("deferred_since"), now),
        "app_update_state": _enum(app_last.get("state"), STEP_STATES),
        "app_update_result": _enum(app_last.get("result"), APP_RESULTS),
    }


def _outbox(outbox: object, now: float) -> dict:
    """The outbox part, from `read_outbox`'s answer."""
    if not isinstance(outbox, Mapping):
        return {"outbox": None}
    if outbox.get("unproven"):
        return {"outbox": None, "outbox_omitted": OUTBOX_UNPROVEN}
    status = outbox.get("status") if isinstance(outbox.get("status"), Mapping) else {}
    census = outbox.get("discarded") if isinstance(outbox.get("discarded"), Mapping) else {}
    days = census.get("by_enqueue_day") if isinstance(census.get("by_enqueue_day"), Mapping) else {}
    refused = status.get("refused_fingerprints")
    return {
        "outbox": True,
        "outbox_pending": _count(status.get("pending")),
        "outbox_pending_mb": round(_count(status.get("pending_bytes")) / 1e6, 1),
        "outbox_dead_lettered": _count(status.get("failed")),
        "outbox_held": _count(status.get("held")),
        "outbox_paused": bool(status.get("paused")),
        "outbox_blocked_reason": _enum(status.get("blocked_reason"), BLOCKED_REASONS),
        "outbox_blocked_age_h": _age_h(status.get("blocked_oldest_pending"), now),
        "outbox_oldest_pending_age_h": _age_h(status.get("oldest_pending"), now),
        "outbox_auth_blocked": bool(outbox.get("auth_blocked")),
        "outbox_refused_credentials": len(refused) if isinstance(refused, Mapping) else 0,
        "outbox_credential_queues": _count(outbox.get("credential_queues")),
        "outbox_roots": _count(outbox.get("roots")),
        "outbox_last_error_kind": _error_kind(status.get("last_error")),
        "outbox_discarded": _count(census.get("writes")),
        "outbox_discarded_by_enqueue_day": {
            day: _count(n) for day, n in sorted(days.items(), reverse=True)[:_discard_days()]
            if isinstance(day, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", day)
        } or None,
    }


def _discard_days() -> int:
    from probe.sdk.journal import DISCARD_DAYS  # the outbox's, loaded by `read_outbox` already

    return DISCARD_DAYS


def _error_kind(last_error: object) -> str | None:
    if not isinstance(last_error, str):
        return None
    head = last_error.split(":", 1)[0].strip()
    return head if _ERROR_KIND.fullmatch(head) else None


def snapshot(status: Mapping, *, outbox: object = None, keys: Mapping | None = None, now: float | None = None) -> dict:
    """`service.state`'s properties from `service.status` (``status``), the
    outbox read (`read_outbox`) and the watch's last answer per key: counts,
    booleans, versions, ages and enum members, nothing else."""
    now = time.time() if now is None else now
    recorders = status.get("recorders") if isinstance(status.get("recorders"), list) else []
    workers = status.get("workers") if isinstance(status.get("workers"), list) else []
    background = status.get("background") if isinstance(status.get("background"), Mapping) else {}
    telemetry = background.get("telemetry") if isinstance(background.get("telemetry"), Mapping) else {}
    statusline = status.get("statusline") if isinstance(status.get("statusline"), Mapping) else {}
    notes = status.get("notes") if isinstance(status.get("notes"), Mapping) else {}
    watch = status.get("watch") if isinstance(status.get("watch"), Mapping) else {}
    hook_queue = status.get("hook_queue") if isinstance(status.get("hook_queue"), Mapping) else {}
    known = _harnesses()
    harnesses: dict = {}
    for rec in recorders:
        if isinstance(rec, Mapping):
            name = rec.get("harness") if rec.get("harness") in known else "other"
            harnesses[name] = harnesses.get(name, 0) + 1
    worker_states: dict = {}
    for worker in workers:
        if isinstance(worker, Mapping):
            state = _enum(worker.get("state"), WORKER_STATES) or "other"
            worker_states[state] = worker_states.get(state, 0) + 1
    reports: dict = {}
    for report in watch.get("reports") or []:
        if isinstance(report, Mapping):
            family = _enum(report.get("family"), FAMILIES)
            if family:
                reports[family] = reports.get(family, 0) + 1
    started = status.get("started_at")
    props: dict[str, Any] = {
        "service_version": _version(status.get("service_version")),
        "service_state": _enum(status.get("state"), SERVICE_STATES),
        "uptime_h": _age_h(started, now),
        "discovering": status.get("discovering_until") is not None,
        "os": _enum(platform.system().lower(), frozenset({"darwin", "linux", "windows"})) or "other",
        "arch": _enum(platform.machine().lower(), frozenset({"arm64", "aarch64", "x86_64", "amd64"})) or "other",
        "python": f"{sys.version_info.major}.{sys.version_info.minor}",
        "sessions": _count(status.get("sessions")),
        "app_clients": _count(status.get("app_clients")),
        "watched": _count(status.get("watched")),
        "action_running": bool((status.get("actions") or {}).get("running")) if isinstance(
            status.get("actions"), Mapping) else False,
        "recorders": len(recorders),
        "recorders_alive": sum(1 for r in recorders if isinstance(r, Mapping) and r.get("alive")),
        "recorders_recording": sum(1 for r in recorders if isinstance(r, Mapping) and r.get("recording")),
        "recorder_failures": sum(_count(r.get("failures")) for r in recorders if isinstance(r, Mapping)),
        "tap_version": next((_version(r.get("tap_version")) for r in recorders
                             if isinstance(r, Mapping) and _version(r.get("tap_version"))), None),
        "recorders_by_harness": harnesses or None,
        "workers": len(workers),
        "workers_by_state": worker_states or None,
        "worker_crashes": sum(_count(w.get("crashes")) for w in workers if isinstance(w, Mapping)),
        "worker_spawns": sum(_count(w.get("spawns")) for w in workers if isinstance(w, Mapping)),
        "run_holds": len(status.get("runs") or []) if isinstance(status.get("runs"), list) else 0,
        "imports": len(status.get("imports") or []) if isinstance(status.get("imports"), list) else 0,
        "hook_hosts": len(status.get("hook_hosts") or []) if isinstance(status.get("hook_hosts"), list) else 0,
        "hook_queue_pending": _count(hook_queue.get("pending")),
        "background_drains": len(background.get("drains") or []),
        "background_box_watchers": len(background.get("box_watchers") or []),
        "background_telemetry_dropped": _count(telemetry.get("dropped")),
        "statusline_waiting": _count(statusline.get("waiting")),
        "notes_running": bool(notes.get("running")),
        "watch_enabled": bool(watch.get("enabled")),
        "watch_waiting": _count(watch.get("waiting")),
        "watch_reports_by_family": reports or None,
        **{f"key_{kind}": _enum(answer, KEY_ANSWERS) for kind, answer in (keys or {}).items() if kind in KEY_KINDS},
        **_update(status.get("update"), now),
        **_outbox(outbox, now),
    }
    return props


def acted_snapshot(record: Mapping) -> dict:
    """`lifeboat.acted`'s properties from the lifeboat's `acted.json`: why it
    acted (a token), the versions it moved between, what ran it (an enum) and
    when (epoch seconds), nothing else."""
    reason = record.get("reason")
    at = record.get("at")
    return {
        "reason": reason if isinstance(reason, str) and _REASON.fullmatch(reason) else "other",
        "from": _version(record.get("from")),
        "to": _version(record.get("to")),
        "trigger": _enum(record.get("trigger"), LIFEBOAT_TRIGGERS) or "other",
        "at": int(at) if isinstance(at, (int, float)) and not isinstance(at, bool) and at >= 0 else None,
    }


def _read_acted() -> dict | None:
    from . import lifeboat

    return lifeboat.read_acted()


def _clear_acted() -> None:
    from . import lifeboat

    lifeboat.clear_acted()


#: What a change is judged by: state that means someone should look, not
#: counts that move all day.
_DIGEST_KEYS = (
    "service_state", "update_in_progress", "update_step", "update_last_ok", "update_deferred",
    "app_update_result", "outbox_blocked_reason", "outbox_auth_blocked", "outbox_paused",
    "watch_reports_by_family", *sorted(f"key_{kind}" for kind in KEY_KINDS),
)


def digest(props: Mapping) -> tuple:
    """A snapshot reduced to what makes a change worth a `service.state` of
    its own: an enum or flag moving, or a count crossing zero."""
    crossings = tuple(
        bool(props.get(k)) for k in ("recorders_alive", "outbox_pending", "outbox_dead_lettered",
                                       "outbox_discarded", "worker_crashes", "recorder_failures")
    )
    return tuple(repr(props.get(k)) for k in _DIGEST_KEYS) + crossings


class PinCache:
    """What each outbox file says about itself, read once: the server it is
    pinned to and the day it was queued, by path, size and mtime (a retry
    rewrites a file: then it is read again). `read_outbox` checks EVERY file
    it counts, every five minutes, at the cost of a listing and a stat once
    each file is known. Lives as long as the service; ``limit`` files at most:
    a scan that meets more is `overflow` (judged afresh every scan)."""

    #: A file gone between its listing and its read: delivered, or moved on.
    GONE = object()
    #: A file that is not an op (corrupt, or quarantined as such): no server.
    UNREADABLE = object()

    def __init__(self, limit: int = PIN_CACHE_MAX) -> None:
        self.limit = limit
        #: The last scan's files, and this scan's (what it saw, so a file
        #: gone since is forgotten and never holds a slot).
        self._known: dict[str, tuple[int, int, object, str | None]] = {}
        self._next: dict[str, tuple[int, int, object, str | None]] = {}
        self.overflow = False

    def begin(self) -> None:
        self.overflow = False
        self._next = {}

    def end(self) -> None:
        self._known, self._next = self._next, {}

    def get(self, entry: os.DirEntry) -> tuple[object, str | None]:
        """(server, day) of the op file ``entry``: the server is a URL, None
        (an op with no pin), `GONE` or `UNREADABLE`. Past ``limit`` nothing
        more is read (`overflow`: the answer is unproven anyway)."""
        from probe.sdk.journal import _read_op_file, op_base_url, op_day

        try:
            st = entry.stat()
        except FileNotFoundError:
            return self.GONE, None
        except OSError:
            return self.UNREADABLE, None
        if len(self._next) >= self.limit:
            self.overflow = True
            return self.UNREADABLE, None
        known = self._known.get(entry.path)
        if known is not None and known[:2] == (st.st_size, st.st_mtime_ns):
            self._next[entry.path] = known
            return known[2], known[3]
        path = Path(entry.path)
        op = _read_op_file(path)
        if op is None and not path.exists():
            return self.GONE, None
        server = op_base_url(op) if isinstance(op, dict) else self.UNREADABLE
        found = (server, op_day(op) or time.strftime("%Y-%m-%d", time.gmtime(st.st_mtime)))
        self._next[entry.path] = (st.st_size, st.st_mtime_ns, *found)
        return found


#: Folders whose writes could still be sent; one there that is not a readable,
#: hosted-pinned op makes the outbox unproven. Elsewhere (dead letters,
#: discards) a corrupt file is sent nowhere and only counted.
_SENDABLE = frozenset({"ops"})


def read_outbox(root: object = None, cache: PinCache | None = None) -> dict:
    """The outbox part's facts, on a thread: the status of this user's every
    outbox root, folded; the discards they keep (a receipt namespace's
    tombstones and a half-pruned queue's included), by the day each was
    queued; and whether every write counted -- queued, dead-lettered, a
    multipart upload, discarded -- is pinned to Probe's hosted service. Fails
    closed: a folder it cannot list, an op with no pin, a queued file it
    cannot read, or more files than `PinCache` holds make it unproven.
    Blocking: status files and listings, and each op file once (``cache``)."""
    from probe.sdk import _telemetry_core as core
    from probe.sdk import outbox_worker
    from probe.sdk.journal import (
        CREDENTIAL_NAMESPACE,
        DELIVERY_NAMESPACE,
        Journal,
        auth_blocked_since,
        credential_queue_dirs,
        default_root,
    )

    cache = cache if cache is not None else PinCache()
    cache.begin()
    base = Journal(str(root) if root is not None else str(default_root()))
    roots = outbox_worker._rescue_roots(base)
    statuses = [Journal.read_status(str(one.dir)) or {} for one in roots]
    status = _fold(statuses)
    servers: set = set()
    days: dict[str, int] = {}
    discarded = queues = 0
    for one in roots:
        dirs = credential_queue_dirs(one.dir)
        queues += len(dirs)
        try:
            leftovers = [p for p in (one.dir / CREDENTIAL_NAMESPACE).iterdir() if p.name.startswith(".pruned-")]
        except OSError:
            leftovers = []
        folders = [p / "discarded" for p in leftovers]
        for queue in [one.dir, *dirs]:
            for space in (queue, queue / DELIVERY_NAMESPACE):
                folders += [space / "ops", space / "failed", space / "multipart" / "ops", space / "discarded"]
        for folder in folders:
            try:
                with os.scandir(folder) as entries:
                    listed = [e for e in entries if e.name.endswith(".json") and not e.name.startswith(".")]
            except FileNotFoundError:
                continue
            except OSError:
                servers.add(None)  # cannot look: cannot say where it goes
                continue
            sendable = folder.name in _SENDABLE
            for entry in listed:
                server, day = cache.get(entry)
                if server is PinCache.GONE:
                    continue  # delivered or moved on meanwhile: not counted
                if server is PinCache.UNREADABLE:
                    if sendable or cache.overflow:
                        servers.add(None)
                else:
                    servers.add(server)
                if folder.name == "discarded":
                    discarded += 1
                    if day:
                        days[day] = days.get(day, 0) + 1
    cache.end()
    proven = not cache.overflow and all(url and core.hosted_base_url(url) for url in servers)
    return {
        "unproven": not proven,
        "status": status,
        "auth_blocked": any(auth_blocked_since(one) for one in statuses),
        "credential_queues": queues,
        "roots": len(roots),
        "discarded": {"writes": discarded, "by_enqueue_day": days},
    }


def _fold(statuses: list) -> dict:
    """Every root's status as one: counts added up, the oldest stamps kept,
    and the longest-standing block (a distributed job's `rank-*` roots and
    the fallback outbox are the machine's backlog too)."""
    out: dict = {}
    for one in statuses:
        for field in ("pending", "pending_bytes", "failed", "held"):
            out[field] = _count(out.get(field)) + _count(one.get(field))
        refused = one.get("refused_fingerprints")
        if isinstance(refused, Mapping) and refused:
            out["refused_fingerprints"] = {**(out.get("refused_fingerprints") or {}), **refused}
        out["paused"] = bool(out.get("paused") or one.get("paused"))
        for stamp in ("oldest_pending", "blocked_oldest_pending"):
            if one.get(stamp) and (not out.get(stamp) or str(one[stamp]) < str(out[stamp])):
                out[stamp] = one[stamp]
                if stamp == "blocked_oldest_pending":
                    out["blocked_reason"] = one.get("blocked_reason")
        out["last_error"] = out.get("last_error") or one.get("last_error")
    return out


def _voter_key(voters: list) -> tuple:
    """What a session's consent is read from, for every session: a change
    asks the consent again."""
    return tuple(sorted(
        (str(getattr(v, "sid", "")), repr(sorted((getattr(v, "hosted_env", None) or {}).items())),
         repr(getattr(v, "report_env", None)))
        for v in voters
    ))


#: The first minute it looks every START_TICK_S: a service that runs for
#: seconds is still seen.
FAST_FOR_S = 60.0
#: A read of the CLI config, the key answers, a send: past this, given up on.
SIDE_TIMEOUT_S = 10.0


class StatePost:
    """Sends the service's state (module docstring). The server owns one;
    every read is a daemon thread's and every send the sender's, never the
    loop's."""

    def __init__(
        self,
        *,
        log: Callable[[str], None],
        status: Callable[[], Mapping],
        consent: Callable[[], Awaitable[tuple[bool, str | None]]],
        voters: Callable[[], list],
        login_env: Callable[[], Mapping | None] = lambda: None,
        login_reader: Callable[[], Awaitable[object]] | None = None,
        keys: Callable[[], Mapping] = dict,
        outbox: Callable[[PinCache], dict] = lambda cache: read_outbox(cache=cache),
        emit: Callable[..., bool] | None = None,
        clock: Callable[[], float] = time.time,
        monotonic: Callable[[], float] = time.monotonic,
        tick_s: float | None = None,
        read_acted: Callable[[], Mapping | None] = _read_acted,
        clear_acted: Callable[[], None] = _clear_acted,
    ) -> None:
        self.log = log
        self.status = status
        self.consent = consent
        self.voters = voters
        self.login_env = login_env
        #: Reads the login shell's answer (cached by the watch) for `prime`.
        self.login_reader = login_reader
        self._primes: set = set()
        self.keys = keys
        self.outbox = outbox
        self.emit = emit if emit is not None else _emit
        self.clock = clock
        self.monotonic = monotonic
        self.tick_s = tick_s if tick_s is not None else STATE_TICK_S
        self.enabled = reports_enabled()
        #: How the service before this one ended without stopping (`watch.last_run`), if it did.
        self.crashed: str | None = None
        self._born = monotonic()
        self._task: asyncio.Task | None = None
        self._started_sent = False
        self._sent_at: float | None = None
        self._digest: tuple | None = None
        self._outbox_at: float | None = None
        self._outbox: dict | None = None
        self._outbox_busy = False
        self._pins = PinCache()
        #: The consent last asked, and the sessions it was asked for.
        self._consent: tuple[bool, str | None] | None = None
        self._consent_for: tuple | None = None
        self._consent_at = 0.0
        self._closed = False
        #: The lifeboat's record (`acted.json`): read and deleted here once sent.
        self.read_acted = read_acted
        self.clear_acted = clear_acted
        #: Look for one at the next tick: at the first, and after each update cycle.
        self._acted_due = True

    def look_for_acted(self) -> None:
        """An update cycle ended: the next tick looks for the lifeboat's record."""
        self._acted_due = True

    def start(self) -> None:
        if self.enabled and self._task is None and not self._closed:
            self._task = asyncio.ensure_future(self._run())

    async def _run(self) -> None:
        while not self._closed:
            fast = self.monotonic() - self._born < FAST_FOR_S and not self._started_sent
            await asyncio.sleep(min(self.tick_s, START_TICK_S) if fast else self.tick_s)
            try:
                await self.tick()
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001 -- one bad tick never stops the next
                self.log(f"statepost: {exc!r}")

    async def _read_outbox(self) -> None:
        """At most every OUTBOX_EVERY_S, on a daemon thread of its own (a hung
        mount is left behind, never joined at exit), and none while the last
        one still runs, however long."""
        mono = self.monotonic()
        if self._outbox_busy or (self._outbox_at is not None and mono - self._outbox_at < OUTBOX_EVERY_S):
            return
        self._outbox_busy = True
        self._outbox_at = mono

        def read() -> dict:
            try:
                return self.outbox(self._pins)
            finally:
                self._outbox_busy = False

        try:
            self._outbox = await _on_daemon_thread(read, OUTBOX_TIMEOUT_S)
        except RuntimeError as exc:  # no thread could start: nothing holds the read
            self._outbox_busy = False
            self.log(f"statepost: reading the outbox failed: {exc!r}")
            self._outbox = None
        except asyncio.TimeoutError:
            self.log("statepost: reading the outbox did not finish in time")
            self._outbox = None
        except Exception as exc:  # noqa: BLE001 -- unread: the part is left out
            self.log(f"statepost: reading the outbox failed: {exc!r}")
            self._outbox = None

    async def _allowed(self, *, fresh: bool = False) -> tuple[bool, str | None]:
        """The consent: asked again when the sessions changed since it was, at
        least every STATE_EVERY_S, and right before a send (``fresh``: the
        sessions, the login shell's last answer and the config as they are)."""
        key = _voter_key(list(self.voters()))
        mono = self.monotonic()
        if (fresh or self._consent is None or key != self._consent_for
                or mono - self._consent_at >= STATE_EVERY_S):
            try:
                allowed, base_url = await self.consent()
            except Exception:  # noqa: BLE001 -- cannot be asked: no, this time; asked again next tick
                # Never cached: the config was not READ, which is not "unset" (the
                # hosted default), and `stopped` must not take a backend from it.
                return False, None
            self._consent, self._consent_for = (bool(allowed), _hosted_default(base_url)), key
            self._consent_at = mono
        return self._consent

    async def tick(self) -> None:
        """Looks once: `service.started` when discovery has ended, and
        `service.state` when it is due, with the machine's consent asked again
        right before either is sent."""
        if not self.enabled:
            return
        allowed, _ = await self._allowed()
        if not allowed:
            return
        await self._read_outbox()
        try:
            keys = await _on_daemon_thread(self.keys, SIDE_TIMEOUT_S)
        except Exception:  # noqa: BLE001 -- unread: no key part
            keys = {}
        props = snapshot(self.status(), outbox=self._outbox, keys=keys, now=self.clock())
        if props["discovering"]:
            return  # the sessions are still coming back: neither event yet
        if self._acted_due:
            self._acted_due = False
            await self._acted()
        mono = self.monotonic()
        current = digest(props)
        due = (
            self._sent_at is None
            or mono - self._sent_at >= STATE_EVERY_S
            or (current != self._digest and mono - self._sent_at >= CHANGE_MIN_S)
        )
        if self._started_sent and not due:
            return
        allowed, base_url = await self._allowed(fresh=True)  # a session may have joined meanwhile
        if not allowed:
            return
        if not self._started_sent:
            self._started_sent = True
            await self._send(EVENT_STARTED, {
                "service_version": props["service_version"],
                "crashed_last_run": self.crashed is not None,
                "last_run_ended": _enum(self.crashed, LAST_RUN_ENDINGS),
                "os": props["os"],
            }, base_url)
        if due:
            self._sent_at, self._digest = mono, current
            await self._send(EVENT_STATE, props, base_url)

    async def _acted(self) -> None:
        """`lifeboat.acted`, once, with the machine's consent asked right
        before; the record is deleted once it was handed to the sender. Not
        allowed: it stays, for the next look (the lifeboat's reader drops one
        older than a week). Never raises."""
        try:
            record = await _on_daemon_thread(self.read_acted, SIDE_TIMEOUT_S)
        except Exception:  # noqa: BLE001 -- unread: looked for after the next cycle
            return
        if not isinstance(record, Mapping):
            return
        allowed, base_url = await self._allowed(fresh=True)
        if not allowed:
            return
        props = acted_snapshot(record)
        try:
            sent = await _on_daemon_thread(lambda: self.emit(EVENT_LIFEBOAT, props, base_url), SIDE_TIMEOUT_S)
        except Exception as exc:  # noqa: BLE001 -- observability never costs the service
            self.log(f"statepost: {EVENT_LIFEBOAT} not sent: {exc!r}")
            return
        if sent:
            with contextlib.suppress(Exception):
                await _on_daemon_thread(self.clear_acted, SIDE_TIMEOUT_S)

    async def _send(self, event: str, props: Mapping, base_url: str | None) -> None:
        try:
            await _on_daemon_thread(lambda: self.emit(event, props, base_url), SIDE_TIMEOUT_S)
        except Exception as exc:  # noqa: BLE001 -- observability never costs the service
            self.log(f"statepost: {event} not sent: {exc!r}")

    def prime(self) -> None:
        """No session runs any more (the service's grace began): read the
        login shell's answer now, so `stopped` has one to ask (it never
        starts a shell itself). Never raises."""
        if not self.enabled or self._closed or self.login_reader is None:
            return
        with contextlib.suppress(Exception):
            task = asyncio.ensure_future(self.login_reader())
            self._primes.add(task)
            task.add_done_callback(self._primes.discard)

    def stopped(self, reason: str, *, uptime_s: float | None) -> None:
        """`service.stopped`, from `Service.stop` on the loop: hands one record
        to the sender. Its consent is the sessions' as they are NOW (in
        memory), else the login shell's as last read; with neither, nothing is
        sent (unknown is no), and nothing is started at exit."""
        if not self.enabled or self._consent is None:
            return
        _, base_url = self._consent
        voters = list(self.voters())
        login = None if voters else self.login_env()
        if not voters and login is None:
            return
        try:
            allowed, _ = decide_machine(voters, base_url, login)
        except Exception:  # noqa: BLE001 -- cannot be asked: no
            return
        if not allowed:
            return
        with contextlib.suppress(Exception):
            self.emit(EVENT_STOPPED, {
                "reason": _enum(reason, STOP_REASONS) or "other",
                "uptime_h": round(max(0.0, uptime_s) / 3600.0, 2) if isinstance(uptime_s, (int, float)) else None,
            }, base_url)

    def close(self) -> None:
        self._closed = True
        if self._task is not None:
            self._task.cancel()


def _hosted_default(base_url: str | None) -> str:
    """The backend a client with no `base_url` configured talks to."""
    if base_url:
        return base_url
    from probe.sdk._telemetry_core import DEFAULT_BASE

    return DEFAULT_BASE


def _emit(event: str, props: Mapping, base_url: str | None) -> bool:
    from probe._shared import telemetry
    from probe.sdk import _telemetry_core as core

    from .background import TELEMETRY_HOST_ENV

    host = os.environ.get(TELEMETRY_HOST_ENV)
    if host:
        core.POSTHOG_HOST = host  # test-only, as `background._post`: the service sends nothing else through it
    return telemetry.emit_service_event(event, dict(props), base_url=base_url)


__all__ = ["PinCache", "StatePost", "acted_snapshot", "digest", "read_outbox", "snapshot"]
