"""The service's watch: what fails here reaches the Probe team as one automatic report (plan B2, rev 5).

    the subsystems ──note(family, reason, sid, facts, env)──> a counter per family
                     (recorders, workers, hooks.run,           (and session), over a
                     the hook queue, background work,          15-min window: at its
                     the loop and threads, the updater,        threshold, an incident
                     the tap's load)
    the start      ──note(service_crash)────────────────────> the last service died
                     (`last_run`: service.run against         without a stop record on
                     last-stop.json and the boot id)          this boot, or crashed
    the loop, at once ──> each new incident takes a snapshot of the sessions whose
                     agent runs AT THAT MOMENT (`voters`: the registered ones,
                     including one switched to mode off -- a session that STARTS
                     off never registers, so it is not among them), the very
                     next turn of the loop after its note, whatever the report
                     slot is doing; with the environment it happened in (a
                     session's, a hook event's, an SDK caller's) they decide:
                     any one that says no drops it, now and for good
    every SCAN_S   ──> the update barrier (read here only, never where a note comes from)
                   ──> every SLOW_CHECK_S (the first scan too), the same on two runs:
                       one outbox queue holding writes nothing here will send
                       without a person (`outbox_stuck`), live sessions' transcripts
                       waiting CAPTURE_STALL_S past their last receipt (one
                       `capture_stalled` for the machine), either dropped while it
                       waits for a retry once a check no longer sees it; and,
                       beside the scan and with the consent its report would need,
                       each key the CLI config holds not answered within
                       CREDENTIAL_CHECK_S (`watch.json` keeps when), asked once
                       (`credential_refused`, once per key)
                   ──> for the sessions the service does not supervise: their daemon
                       lease released with `error`/`gateway`/`unauthorized`, or
                       expired (`hung` / `not_running`); a hosted recorder whose
                       beat is STALL_S old (`stalled`); a `tap watch` session whose
                       heartbeat is GONE_S old (`gone`): each the same on two scans
                       in a row, its agent still running, and never in the
                       WAKE_GRACE_S after the machine slept (wall time ran ahead of
                       monotonic time between two scans)
                   ──> a rejected release in guard.json, once per version
                   ──> the oldest incident waiting for the slot:
    one child      ──`probe.core.run report` (a READ, `children.run_read`), at
                     most one at a time, killed at REPORT_TIMEOUT_S, never an
                     action (an action takes the one slot and holds updates off);
                     what it answered goes to service.log and `service.status`
                     (`public`); a report is settled only by `sent`, `deduped`
                     or `disabled:*` (`deduped` not after a failed try: that is
                     its own claim), else (but for `unauthorized` and
                     `too_large`: the child kept its claim) tried again every
                     RETRY_S for RETRY_FOR_S, each try asking the sessions of
                     ITS moment too;
                     a once-ever one (a rejected version, a tap that would not
                     load, a failing update streak) is then never noted again

Consent is `probe._shared.report_policy`'s rule: a session family asks that
session -- the environment its recorder or worker runs with, else what its
registrant said (`session.register`'s `report_env`, a bool the registrant
computed, taken as said), else no; a machine family asks every session whose
agent runs and the environment it happened in, and only an incident noted with
no session at all asks the login shell (its variables) and the CLI config. The
report child then checks only what it is handed: a session's own variables, or
for every other report `{}` and the CLI config's backend.

Never while discovering (the sessions are still coming back: an incident noted
then is decided once they are, by the sessions of its moment AND those back by
then -- one whose consent was not yet known at its moment is asked then), and
never while an update cycle runs, drains
the workers or holds its barrier: a hand-over is no failure, so what fails
meanwhile is not counted, and nothing is sent until it is over.

`last_run` and `record_crash` keep the service's own record (`service.run`,
`last-crash.json`); the keeper reads the sessions from disk with
`sessions_on_disk` and decides as a machine family does (`decide_machine`).

Stdlib only at import (the start path; plan S1): the consent rule and the
CLI config are read on a thread, when there is something to send.
"""

from __future__ import annotations

import asyncio
import collections
import contextlib
import json
import os
import re
import subprocess
import sys
import threading
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

from . import paths


class Family:
    """The report families (the API contract's table, rev 5): the `family` slug a report carries."""

    SERVICE_CRASH = "service_crash"
    SERVICE_ERROR = "service_error"
    UPDATE_REJECTED = "update_rejected"
    UPDATE_FAILED = "update_failed"
    TAP_LOAD = "tap_load"
    SERVICE_DOWN = "service_down"
    RECORDER = "recorder"
    WORKER = "worker"
    HOOK_HOST = "hook_host"
    HOOK = "hook"
    BACKGROUND = "background"
    #: The machine's outbox holds writes nothing here will send without a person
    #: (a refused credential, writes held for one), its oldest OUTBOX_STUCK_S old.
    OUTBOX_STUCK = "outbox_stuck"
    #: The API refuses a key the CLI config holds (the sign-in, the daemon's
    #: key, the MCP key), asked once every CREDENTIAL_CHECK_S.
    CREDENTIAL_REFUSED = "credential_refused"
    #: A live session's transcript waits CAPTURE_STALL_S past its last receipt.
    CAPTURE_STALLED = "capture_stalled"


#: About one session (`sid`); every other family is about the machine.
SESSION_FAMILIES = frozenset({Family.RECORDER, Family.WORKER})
#: Events in WINDOW_S that make an incident (absent: the first one does).
THRESHOLDS = {Family.SERVICE_ERROR: 3, Family.RECORDER: 3, Family.HOOK_HOST: 3, Family.HOOK: 3}
WINDOW_S = 15 * 60.0
#: Kept while an update drains or holds its barrier: they are not a hand-over's doing.
KEPT_WHILE_UPDATING = frozenset({Family.SERVICE_CRASH, Family.UPDATE_REJECTED, Family.UPDATE_FAILED, Family.TAP_LOAD})
#: `update_failed`: this many update cycles in a row ended `ok: false`.
UPDATE_FAILED_STREAK = 3
#: The read the child runs (`probe.core.run report`, PR 2a), and its bounds.
REPORT_READ = "report"
REPORT_TIMEOUT_S = 60.0
#: A (family, session) reported, or declined, is not asked about again for this
#: long: the child's own dedupe window, so no child starts only to say `deduped`.
DEDUPE_S = 6 * 3600.0
#: Incidents waiting at once (the oldest goes).
MAX_PENDING = 16
#: A report the child did not take (offline, the server, killed...) is tried
#: again this often, for this long after its first try.
RETRY_S = 30 * 60.0
RETRY_FOR_S = 24 * 3600.0
#: The facts of an incident: each text cut to this (a traceback keeps its END),
#: the whole to MAX_FACTS_BYTES (the contract's 64 KiB), the last KEEP_EVENTS
#: events of a counted family.
MAX_FACT_TEXT = 4096
MAX_FACTS_BYTES = 64 * 1024
KEEP_EVENTS = 3
#: How often the watch looks (and sends what waits for the slot).
SCAN_S = 15.0
#: A daemon lease past its expiry by more than this, on two scans, is a lapsed worker.
LEASE_GRACE_S = 60.0
#: Lease reasons that are failures (`tap/companion_lease.py`); `stopped`,
#: `budget` and `handover` are on purpose.
LEASE_FAILURES = frozenset({"error", "gateway", "unauthorized"})
#: A hosted recorder's beat (`tap.hosted.Controls.beat`, every pass and every
#: second between) this old while its agent runs: `stalled`.
STALL_S = 300.0
#: A `tap watch` session's registration (its link re-registers every 20 s)
#: this old while its agent runs: `gone`.
GONE_S = 90.0
#: How often the slower checks run (the outbox, receipts), on the first scan too.
SLOW_CHECK_S = 5 * 60.0
#: The outbox's oldest write this old, with the queue refused or held: stuck.
OUTBOX_STUCK_S = 3600.0
#: A live session's transcript waiting this long past its last receipt: stalled.
CAPTURE_STALL_S = 3600.0
#: Each key the CLI config holds is asked whether the API takes it this often
#: (`watch.json` keeps when each was answered, so a restarted service does not
#: ask again).
CREDENTIAL_CHECK_S = 24 * 3600.0
#: One ask's timeout, and the whole check's: no retry ever starts past it.
CREDENTIAL_TIMEOUT_S = 5.0
CREDENTIAL_DEADLINE_S = 20.0
#: The CLI config's keys, by the kind a report names (never a key itself), and
#: the door that asks: `me` (`GET /v1/me`, which counts as the key's use) or
#: `capture` (`POST /v1/device-state`'s capture part, which records nothing:
#: a daemon key asked daily must not read as used on an idle machine).
CREDENTIAL_KEYS = (("login", "token", "me"), ("daemon_key", "companion_token", "capture"),
                   ("mcp_key", "mcp_token", "me"))
#: A key with no answer (offline, a timeout, a server error) is asked again
#: after this, not at every slow check.
CREDENTIAL_RETRY_S = 3600.0
#: The outbox's status files on a hung mount: given up on past this.
OUTBOX_TIMEOUT_S = 30.0
#: A capture stall names at most this many of its sessions.
CAPTURE_MAX_SESSIONS = 8
#: A report the server's rate limit refused is tried again after this.
RATE_LIMITED_RETRY_S = 2 * 3600.0
#: Between two scans, wall time ran ahead of monotonic time by more than this
#: (a sleep), or the scans were this far apart: everything measured in time
#: waits WAKE_GRACE_S (a worker renews its lease within its TTL, 240 s).
WAKE_SLACK_S = 30.0
WAKE_GAP_S = 120.0
WAKE_GRACE_S = 300.0
#: A guard record older than this is not news.
GUARD_FRESH_S = 24 * 3600.0
#: The login shell's variables are asked at most this often.
LOGIN_CACHE_S = 600.0
#: The variables a report's consent reads (`report_policy`), never more of an environment.
CONSENT_VARS = ("PROBE_TELEMETRY", "PROBE_DIAGNOSTICS", "PROBE_BASE_URL")
#: Test-only overrides (API v1, "Lifecycle"). Nothing in production sets them.
#: "0": no automatic report from this service or its keeper (the test suite's
#: services: a person's opt-outs are PROBE_TELEMETRY and PROBE_DIAGNOSTICS).
REPORTS_ENV = "PROBE_SERVICE_REPORTS"
SCAN_ENV = "PROBE_SERVICE_WATCH_S"
#: The watch's own record: the incidents reported once ever (a rejected
#: version, a tap that would not load, an update cycle's streak).
STATE_NAME = "watch.json"
MAX_ONCE = 64
#: The service's record of itself (`last_run`), and of a crash (`record_crash`).
RUN_NAME = "service.run"
LAST_CRASH_NAME = "last-crash.json"
MAX_TRACEBACK = 16 * 1024
#: Two boot readings within this many seconds are one boot (Windows: from the uptime).
BOOT_SLACK_S = 120.0
#: Windows: no SIGTERM handler, and a logoff ends the service with no stop
#: record while the uptime-based boot id survives it, so a missing stop record
#: says nothing there; only a recorded crash (`last-crash.json`) is one.
WINDOWS = os.name == "nt"
#: `service_error`'s tracebacks in service.log: this many per (site, exception
#: type) in WINDOW_S, one line each after that (the log rotates only at start).
TRACEBACKS_PER_WINDOW = 3
#: The last reports `public` names.
RECENT = 5
#: What the `report` read takes for `sid` (its parser refuses anything else,
#: and the whole report with it): any other session id rides in the facts.
_UUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


def reports_enabled() -> bool:
    return os.environ.get(REPORTS_ENV, "1") != "0"


def _env_float(name: str, default: float) -> float:
    try:
        value = float(os.environ.get(name) or default)
    except ValueError:
        return default
    return value if value > 0 else default


# -- small files --------------------------------------------------------------


def read_json(path: Path, limit: int = 1024 * 1024) -> object:
    """A small JSON file's value, or None (missing, too big, unreadable)."""
    try:
        with open(path, "rb") as handle:
            raw = handle.read(limit + 1)
    except OSError:
        return None
    if len(raw) > limit:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None


def write_json(path: Path, value: object) -> bool:
    """0600, whole or not at all. False when it could not be written (a full
    disk, a read-only folder). Never raises."""
    tmp = path.with_name(f"{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    try:
        with open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as handle:
            json.dump(value, handle)
        os.replace(tmp, path)
        return True
    except OSError:
        return False
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)


def bounded(value: object, depth: int = 0, *, key: str = "") -> object:
    """`value` as JSON can carry it: texts cut to MAX_FACT_TEXT (a traceback,
    by its key, keeps its END: the exception is its last line), at most 64 keys
    and 32 items a level, 6 levels deep."""
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return value[-MAX_FACT_TEXT:] if "traceback" in key else value[:MAX_FACT_TEXT]
    if depth >= 6:
        return "..."
    if isinstance(value, Mapping):
        return {str(k)[:64]: bounded(v, depth + 1, key=str(k)) for k, v in list(value.items())[:64]}
    if isinstance(value, (list, tuple, set, frozenset, collections.deque)):
        return [bounded(v, depth + 1, key=key) for v in list(value)[:32]]
    return repr(value)[:MAX_FACT_TEXT]


def bounded_facts(facts: Mapping | None) -> dict:
    """The facts a report carries, within MAX_FACTS_BYTES."""
    out = bounded(dict(facts or {}))
    assert isinstance(out, dict)
    if len(json.dumps(out)) > MAX_FACTS_BYTES:
        return {"truncated": True, "keys": sorted(out)[:64]}
    return out


class TracebackGate:
    """At most TRACEBACKS_PER_WINDOW full tracebacks per key in WINDOW_S
    (`log_traceback`'s `gate`). Thread-safe."""

    def __init__(self, monotonic: Callable[[], float] = time.monotonic) -> None:
        self.monotonic = monotonic
        self._lock = threading.Lock()
        self._seen: dict = {}

    def allow(self, key: object) -> bool:
        now = self.monotonic()
        with self._lock:
            for old in [k for k, times in self._seen.items() if not times or now - times[-1] > WINDOW_S]:
                del self._seen[old]
            times = self._seen.setdefault(key, collections.deque())
            while times and now - times[0] > WINDOW_S:
                times.popleft()
            if len(times) >= TRACEBACKS_PER_WINDOW:
                return False
            times.append(now)
            return True


def log_traceback(
    log: Callable[[str], None], header: str, text: str, *, gate: TracebackGate | None = None, key: object = None,
) -> None:
    """`header`, then the traceback a line at a time, each with the service's
    prefix (the report keeps only the service's own lines of service.log). With
    `gate`: past its TRACEBACKS_PER_WINDOW for `key`, the header alone."""
    if gate is not None and text and not gate.allow(key):
        log(f"{header} (its traceback was logged {TRACEBACKS_PER_WINDOW} times in the last 15 min)")
        return
    log(header)
    for line in (text or "").rstrip().splitlines()[-200:]:
        log(f"  {line}")


# -- consent ------------------------------------------------------------------


def consent_env(env: object) -> dict:
    """The variables of `env` the consent reads (CONSENT_VARS), and nothing else."""
    if not isinstance(env, Mapping):
        return {}
    return {name: env[name] for name in CONSENT_VARS if isinstance(env.get(name), str)}


def config_base_url() -> str | None:
    """The CLI config's backend (its active context), or None. Blocking (a file
    read, and `probe.sdk`'s telemetry core: ~70 ms the first time): a thread."""
    try:
        from probe.sdk._telemetry_core import read_cli_config

        value = read_cli_config().get("base_url")
    except Exception:  # noqa: BLE001 -- no config: the hosted default
        return None
    return value if isinstance(value, str) and value else None


def env_allows(env: Mapping | None, base_url: str | None) -> bool:
    """`report_policy.allowed` for `env`'s consent variables; False when it
    cannot be asked (fail closed). Blocking the first time (its lazy import)."""
    try:
        from probe._shared import report_policy

        return report_policy.allowed(consent_env(env or {}), base_url)
    except Exception:  # noqa: BLE001
        return False


@dataclass
class Live:
    """A session whose agent runs, as consent sees it: the environment its
    recorder runs with (hosted), else what its registrant said (`report_env`)."""

    sid: str
    hosted_env: dict | None = None
    report_env: bool | None = None


def decide_session(live: Live | None, env: dict | None, base_url: str | None) -> tuple[bool, str, dict]:
    """A session family's consent: `(allowed, why, the env the child gets)`.
    `env`: the consent variables noted with the incident (the recorder's or
    worker's own environment), which come first."""
    if env is None and live is not None and live.hosted_env is not None:
        env = consent_env(live.hosted_env)
    if env is not None:
        ok = env_allows(env, base_url)
        return ok, "its environment allows reports" if ok else "its environment turns reports off", env
    if live is not None and live.report_env is not None:
        return live.report_env, f"its registrant said report_env {str(live.report_env).lower()}", {}
    return False, "nothing says this session allows reports", {}


def decide_machine(live: list, base_url: str | None, login: dict | None) -> tuple[bool, str]:
    """A machine family's consent: every session whose agent runs allows it;
    with none, `login` (the login shell's variables) and the CLI config's
    backend; unknown is no."""
    if live:
        for session in live:
            ok, _, _ = decide_session(session, None, base_url)
            if not ok:
                return False, f"session {session.sid} does not allow reports"
        return True, f"every session ({len(live)}) allows reports"
    if login is None:
        return False, "no session, and the login environment could not be read"
    if env_allows(login, base_url):
        return True, "no session; the login environment allows reports"
    return False, "no session; the login environment turns reports off"


async def login_env() -> dict | None:
    """The login shell's consent variables (`loginenv`), or None when it cannot
    be asked (no shell, Windows)."""
    from . import loginenv

    found = await loginenv.read(names=CONSENT_VARS)
    return None if found is None else consent_env(found[1])


# -- the service's own record ---------------------------------------------------


def previous_holder() -> tuple[int, str] | None:
    """`(pid, start)` the lock file names (`server._name_holder`): the service
    before this one. Read BEFORE this one names itself there. Never raises."""
    try:
        text = paths.lock_path().read_text(encoding="utf-8")
    except (OSError, ValueError):
        return None
    pid_s, _, start = text.strip().partition(" ")
    try:
        pid = int(pid_s)
    except ValueError:
        return None
    return (pid, start.strip()) if pid > 1 else None


def boot_id() -> str | None:
    """This boot's id: Linux's `boot_id`, macOS's `kern.boottime`, Windows' boot
    time from the uptime (best effort). None when unknown. Never raises."""
    try:
        if sys.platform.startswith("linux"):
            return Path("/proc/sys/kernel/random/boot_id").read_text(encoding="utf-8").strip() or None
        if sys.platform == "darwin":
            out = subprocess.run(  # noqa: S603 -- a fixed system binary, no shell
                ["/usr/sbin/sysctl", "-n", "kern.boottime"], capture_output=True, text=True, timeout=2, check=False,
            ).stdout
            found = re.search(r"sec\s*=\s*(\d+)", out)
            return f"boottime:{found.group(1)}" if found else None
        if os.name == "nt":
            import ctypes

            tick = ctypes.windll.kernel32.GetTickCount64  # type: ignore[attr-defined]
            tick.restype = ctypes.c_ulonglong
            return f"boottime:{round(time.time() - tick() / 1000.0)}"
    except Exception:  # noqa: BLE001 -- unknown: never called a reboot
        return None
    return None


def same_boot(a: object, b: object) -> bool | None:
    """Do two `boot_id` readings name one boot? None when either is unknown."""
    if not isinstance(a, str) or not isinstance(b, str) or not a or not b:
        return None
    if a.startswith("boottime:") and b.startswith("boottime:"):
        try:
            return abs(float(a[9:]) - float(b[9:])) <= BOOT_SLACK_S
        except ValueError:
            return a == b
    return a == b


def _same_process(pid: object, start: object, other_pid: object, other_start: object) -> bool:
    if not isinstance(pid, int) or pid != other_pid:
        return False
    if start and other_start:
        return str(start) == str(other_start)
    return True


def last_run(previous: tuple[int, str] | None, version: str) -> dict | None:
    """At start, holding the lock: how the service before this one ended, when
    that was a crash -- `{"reason": "crashed" | "unclean_exit", ...facts}` for
    `service_crash` -- else None. Then this one's own record, `service.run`
    (0600: pid, start, boot, version). A crash: `last-crash.json` names it
    (written on the way out, with its traceback), or (not on Windows: WINDOWS)
    it left no stop record (`last-stop.json`, written by every deliberate stop)
    and the boot is the same (a reboot or a shutdown's kill is not a crash; an
    unknown boot is never called a reboot). Never raises."""
    try:
        return _last_run(previous, version)
    except Exception:  # noqa: BLE001 -- the service starts whatever its record says
        return None


def _last_run(previous: tuple[int, str] | None, version: str) -> dict | None:
    from . import guard, procid

    folder = paths.service_dir()
    run = read_json(folder / RUN_NAME)
    run = run if isinstance(run, dict) else {}
    stop = guard.last_stop() or {}
    crash = read_json(folder / LAST_CRASH_NAME)
    crash = crash if isinstance(crash, dict) else {}
    boot = boot_id()
    own = procid.start_time(os.getpid())
    write_json(folder / RUN_NAME, {"pid": os.getpid(), "start": own, "boot": boot, "version": version, "at": time.time()})
    if previous is None and isinstance(run.get("pid"), int):
        previous = (run["pid"], str(run.get("start") or ""))
    if previous is None:
        return None
    pid, start = previous
    if _same_process(pid, start, os.getpid(), own):
        return None
    prior = run if _same_process(run.get("pid"), run.get("start"), pid, start) else {}
    facts = {
        "previous": {"version": prior.get("version"), "started_at": prior.get("at")},
        "last_stop": {k: stop.get(k) for k in ("reason", "version", "at")} if stop else None,
    }
    if _same_process(crash.get("pid"), crash.get("start"), pid, start):
        with contextlib.suppress(OSError):
            (folder / LAST_CRASH_NAME).unlink()
        return {"reason": "crashed", **facts, "error": crash.get("error"), "traceback": crash.get("traceback"),
                "crashed_at": crash.get("at")}
    if WINDOWS:
        return None  # a logoff ends it with no stop record: that says nothing there
    if stop and _same_process(stop.get("pid"), stop.get("start"), pid, start):
        return None
    if same_boot(prior.get("boot"), boot) is False:
        return None  # a reboot (or the shutdown's kill): no crash
    return {"reason": "unclean_exit", **facts, "boot_known": same_boot(prior.get("boot"), boot) is not None}


def record_crash(error: str, text: str) -> None:
    """The service is exiting on an exception (`run_service`): what the next
    one reports (`last_run`). Never raises."""
    try:
        from . import procid

        start = procid.start_time(os.getpid())
    except Exception:  # noqa: BLE001
        start = None
    write_json(paths.service_dir() / LAST_CRASH_NAME, {
        "pid": os.getpid(), "start": start, "error": str(error)[:500], "traceback": (text or "")[-MAX_TRACEBACK:],
        "at": time.time(),
    })


# -- the keeper's view (no service to ask) ------------------------------------


def sessions_on_disk(now: float | None = None) -> list[Live]:
    """Every session whose agent runs, as the files say: `recorders.json`'s
    hosted sessions (with their environment) and `sessions.json`'s
    registrations, mode off included (with their `report_env`). For a process
    with no service to ask (the keeper). Never raises."""
    from . import procid
    from .registry import HEARTBEAT_TTL_S

    now = time.time() if now is None else now
    found: dict = {}
    recorded = read_json(paths.service_dir() / "recorders.json")
    for raw in (recorded.get("sessions") or []) if isinstance(recorded, dict) else []:
        if not isinstance(raw, dict) or not isinstance(raw.get("sid"), str):
            continue
        owner = raw.get("owner")
        try:
            if not isinstance(owner, dict) or procid.alive(int(owner["pid"]), str(owner["start_time"])) is False:
                continue
        except (KeyError, TypeError, ValueError):
            continue
        found[raw["sid"]] = Live(raw["sid"], hosted_env=consent_env(raw.get("env")) if isinstance(raw.get("env"), dict)
                                 else {})
    registered = read_json(paths.registry_path())
    for raw in (registered.get("sessions") or []) if isinstance(registered, dict) else []:
        if not isinstance(raw, dict) or not isinstance(raw.get("sid"), str) or raw["sid"] in found:
            continue
        owner = raw.get("owner")
        try:
            if owner is None:
                alive = now - float(raw.get("heartbeat_at") or 0) < HEARTBEAT_TTL_S
            else:
                alive = procid.alive(int(owner["pid"]), str(owner["start_time"])) is not False
        except (KeyError, TypeError, ValueError):
            continue
        if alive:
            value = raw.get("report_env")
            found[raw["sid"]] = Live(raw["sid"], report_env=value if isinstance(value, bool) else None)
    return list(found.values())


def _windowless() -> dict:
    """Windows: the keeper runs as pythonw, with no console at all, so a
    python.exe child would open a console window of its own for up to 60 s:
    it gets one with no window (`subprocess.CREATE_NO_WINDOW`, a Windows-only
    name). The service's children need no flag: the service itself runs in a
    console with no window (`client._DETACHED`), which they share."""
    return {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}


def report_blocking(params: dict, *, timeout: float = REPORT_TIMEOUT_S) -> tuple[int | None, object]:
    """`probe.core.run report` from a process with no event loop (the keeper):
    `(exit status, its one JSON value)`, `(None, None)` when killed at
    `timeout`. Raises OSError when it could not start."""
    from . import children

    try:
        done = subprocess.run(  # noqa: S603 -- the CLI's own interpreter, our own module
            children.core_argv(REPORT_READ), input=json.dumps(params).encode("utf-8"), capture_output=True,
            timeout=timeout, cwd=str(paths.home()), check=False, **_windowless(),
        )
    except subprocess.TimeoutExpired:
        return None, None
    try:
        value = json.loads(done.stdout.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        value = None
    return done.returncode, value


def outcome(code: int | None, value: object) -> str:
    """One line for service.log: what the report child answered."""
    if code is None:
        return f"killed after {REPORT_TIMEOUT_S:.0f} s"
    if isinstance(value, dict):
        if value.get("sent"):
            return f"sent {value.get('id')}"
        if value.get("skipped"):
            return f"not sent: {value.get('skipped')}" + (f" (local copy {value['path']})" if value.get("path") else "")
    return f"failed (exit {code})"


#: `skipped` words the report child answers keeping its claim of the window.
KEPT_CLAIM = frozenset({"unauthorized", "too_large"})


def taken(value: object) -> bool:
    """Did the report child settle it: `sent`, or skipped as `deduped` or
    `disabled:*` (asking again would answer the same)?"""
    if not isinstance(value, dict):
        return False
    skipped = value.get("skipped")
    return bool(value.get("sent")) or skipped == "deduped" or (isinstance(skipped, str) and skipped.startswith("disabled:"))


# -- what the slower checks read --------------------------------------------------


def _age_s(stamp: object, now: float) -> float | None:
    """Seconds since an ISO stamp (a journal's `oldest_pending`), or None."""
    if not isinstance(stamp, str) or not stamp:
        return None
    try:
        from datetime import datetime, timezone

        parsed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return max(0.0, now - parsed.timestamp())


def outbox_condition(now: float, root: Path | None = None) -> tuple[str, dict] | None:
    """The machine's outbox (`journal.default_root`, its delivery and
    credential queues folded in) as `(reason, facts)` when one queue holds
    writes nothing here will send without a person, that queue's oldest
    OUTBOX_STUCK_S old (`blocked_oldest_pending`, judged per queue: another
    queue's old backlog never makes this one's fresh hold read as stuck):
    `auth_blocked` (an older client's queue-wide block), `credential_refused`
    (a credential the API refused, #2041) or `held` (writes set aside for a
    credential nothing here holds; a run close waiting on its data is not).
    A paused outbox is someone's switch. Counts only, never a fingerprint.
    Blocking (status files and one listing, never the op files): a thread."""
    try:
        from probe.sdk.journal import Journal, default_root

        status = Journal.read_status(default_root() if root is None else root)
    except Exception:  # noqa: BLE001 -- no outbox, or one this release cannot read: nothing to say
        return None
    if not isinstance(status, dict) or status.get("paused"):
        return None
    reason = status.get("blocked_reason")
    oldest = _age_s(status.get("blocked_oldest_pending"), now)
    if not isinstance(reason, str) or oldest is None or oldest < OUTBOX_STUCK_S:
        return None
    refused = status.get("refused_fingerprints")
    return reason, {"pending": _count(status.get("pending")), "oldest_pending_h": round(oldest / 3600.0, 1),
                    "held": _count(status.get("held")),
                    "refused_credentials": len(refused) if isinstance(refused, dict) else 0,
                    "dead_lettered": _count(status.get("failed"))}


def _count(value: object) -> int:
    """A status file's count, or 0 for one that is not a number."""
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def _ask_me(base_url: str, token: str, timeout: float) -> str:
    """`GET /v1/me` with one key: `ok`, `refused` (401/403) or `unknown`
    (offline, a timeout, a redirect, anything else). One try, no retry."""
    import urllib.error
    import urllib.request

    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        """A redirect is answered (a 3xx: `unknown`), never followed: urllib
        would carry the key's `Authorization` header wherever it points
        (another host, plain HTTP)."""

        def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001, ARG002
            return None

    try:
        from probe.sdk.tls import ssl_context

        context = ssl_context()
    except Exception:  # noqa: BLE001 -- urllib's default trust
        context = None
    opener = urllib.request.build_opener(_NoRedirect, urllib.request.HTTPSHandler(context=context))
    request = urllib.request.Request(
        base_url.rstrip("/") + "/v1/me",
        headers={"Authorization": f"Bearer {token}", "User-Agent": "probe-service-watch"},
    )
    try:
        with opener.open(request, timeout=timeout) as response:
            return "ok" if 200 <= response.status < 300 else "unknown"
    except urllib.error.HTTPError as exc:
        # Only a 401: a 403 is a proxy's or a scope's, not a dead key.
        return "refused" if exc.code == 401 else "unknown"
    except Exception:  # noqa: BLE001 -- offline is no refusal
        return "unknown"


def _ask_capture(base_url: str, token: str, timeout: float) -> str:
    """`POST /v1/device-state` with a capture key in its body and no bearer:
    the server's own verdict (`ok`, `rejected`: refused), which records no use
    of the key. Anything else (an older server, offline) is `unknown`."""
    import urllib.error
    import urllib.request

    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001, ARG002
            return None

    try:
        from probe.sdk.tls import ssl_context

        context = ssl_context()
    except Exception:  # noqa: BLE001 -- urllib's default trust
        context = None
    try:
        from probe.harness.registry import get_registry

        # Any agent's source id: the door judges a capture key the same for each.
        source = get_registry().captured()[0].id
    except Exception:  # noqa: BLE001 -- no registry: no verdict
        return "unknown"
    opener = urllib.request.build_opener(_NoRedirect, urllib.request.HTTPSHandler(context=context))
    request = urllib.request.Request(
        base_url.rstrip("/") + "/v1/device-state", method="POST",
        data=json.dumps({"capture_tokens": {source: token}}).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "probe-service-watch"},
    )
    try:
        with opener.open(request, timeout=timeout) as response:
            body = json.loads(response.read(64 * 1024) or b"{}")
    except Exception:  # noqa: BLE001 -- offline, an older server: no verdict
        return "unknown"
    verdict = (body.get("capture") or {}).get(source) if isinstance(body, dict) else None
    return {"ok": "ok", "rejected": "refused"}.get(verdict, "unknown") if isinstance(verdict, str) else "unknown"


def _ask(base_url: str, token: str, timeout: float, door: str) -> str:
    return (_ask_capture if door == "capture" else _ask_me)(base_url, token, timeout)


def _may_carry_keys(base_url: str) -> bool:
    """HTTPS, or plain HTTP to this machine only: a key never crosses a
    network in the clear for a check."""
    from urllib.parse import urlsplit

    try:
        parts = urlsplit(base_url)
    except ValueError:
        return False
    if parts.scheme == "https":
        return True
    return parts.scheme == "http" and parts.hostname in ("127.0.0.1", "localhost", "::1")


def _credential_id(base_url: str, kind: str, token: str) -> str:
    """A key's name in `watch.json`: its backend, kind and value hashed, so a
    replaced key or another context is asked afresh. Never the key."""
    import hashlib

    return hashlib.sha256(f"{base_url}\0{kind}\0{token}".encode()).hexdigest()[:16]


def credential_verdicts(
    *, due: Callable[[str], bool] = lambda ident: True,
    ask: Callable[[str, str, float, str], str] = _ask, monotonic: Callable[[], float] = time.monotonic,
) -> dict[str, tuple[str, str]]:
    """`{kind: (id, ok|refused|unknown)}` for each key the CLI config's
    active context holds (CREDENTIAL_KEYS) whose id (`_credential_id`) is
    `due`, asked one at a time within CREDENTIAL_DEADLINE_S in all: a key not
    asked before it is `unknown`, and no ask starts past it
    (`hints.HintFetcher`'s rule, not `alertpoll._get`'s retry past its
    deadline). Each key goes to its own context's backend only (never
    `PROBE_BASE_URL`: `alertpoll.endpoint`'s rule), and only over HTTPS
    (`_may_carry_keys`). Blocking: a thread."""
    try:
        from probe.sdk._telemetry_core import DEFAULT_BASE, read_cli_config

        config = read_cli_config()
        base_url = str(config.get("base_url") or DEFAULT_BASE).rstrip("/")
    except Exception:  # noqa: BLE001 -- no config: nothing to ask about
        return {}
    if not base_url or not _may_carry_keys(base_url):
        return {}
    deadline = monotonic() + CREDENTIAL_DEADLINE_S
    found: dict[str, tuple[str, str]] = {}
    for kind, key, door in CREDENTIAL_KEYS:
        token = config.get(key)
        if not isinstance(token, str) or not token:
            continue
        ident = _credential_id(base_url, kind, token)
        if not due(ident):
            continue
        left = deadline - monotonic()
        if left <= 0:
            found[kind] = (ident, "unknown")
            continue
        found[kind] = (ident, ask(base_url, token, min(CREDENTIAL_TIMEOUT_S, left), door))
    return found


def capture_conditions(receipts: Mapping, now: float, still: dict | None = None) -> dict[str, dict]:
    """`{sid: facts}` for each session whose transcript has waited
    CAPTURE_STALL_S past its last receipt, not finalized: complete lines (or,
    not yet counted, bytes) or a staged batch waiting. Its age is
    `received_at`'s; a receipt without one (a tap before 0.10.6, or a session
    none of whose batches ever landed) is aged from when `still` (the
    caller's, kept across calls: sid -> (`received_bytes`, since when)) first
    saw its cursor where it is now. A trailing line with no newline yet is
    not waiting."""
    still = {} if still is None else still
    found = {}
    for sid in [s for s in still if s not in receipts]:
        del still[sid]
    for sid, receipt in receipts.items():
        if not isinstance(receipt, Mapping) or receipt.get("finalized"):
            still.pop(sid, None)
            continue
        lines = receipt.get("pending_lines")
        waiting = (lines > 0 if isinstance(lines, int) else int(receipt.get("pending_bytes") or 0) > 0) \
            or bool(receipt.get("pending_batch"))
        if not waiting:
            still.pop(sid, None)
            continue
        cursor = receipt.get("received_bytes")
        seen = still.get(sid)
        if seen is None or seen[0] != cursor:
            seen = still[sid] = (cursor, now)
        received_at = receipt.get("received_at")
        stamped = isinstance(received_at, (int, float))
        since = received_at if stamped else seen[1]
        if now - since < CAPTURE_STALL_S:
            continue
        found[sid] = {"received_h": round((now - since) / 3600.0, 1),
                      "receipt": "received_at" if stamped else "unmoved",
                      "pending_bytes": receipt.get("pending_bytes"), "pending_lines": lines,
                      "pending_batch": bool(receipt.get("pending_batch")), "retrying": bool(receipt.get("retrying"))}
    return found


async def _no_receipts() -> dict:
    return {}


#: A slow check's read that did not answer (timed out, or still stuck).
_UNREAD = object()


async def _on_daemon_thread(work: Callable[[], object], timeout: float) -> object:
    """`work()` on a daemon thread of its own, waited for at most `timeout`
    (asyncio.TimeoutError past it): a call stuck on a slow server is left
    behind, and neither the loop nor a stopping service waits for it (the
    default executor's threads are joined at exit; `receipts.ReceiptCache`'s rule)."""
    loop = asyncio.get_running_loop()
    result: asyncio.Future = loop.create_future()

    def run() -> None:
        try:
            value, error = work(), None
        except Exception as exc:  # noqa: BLE001 -- handed to the waiter
            value, error = None, exc

        def settle() -> None:
            if result.done():
                return
            if error is not None:
                result.set_exception(error)
            else:
                result.set_result(value)

        with contextlib.suppress(RuntimeError):  # the loop is closed: the service went first
            loop.call_soon_threadsafe(settle)

    threading.Thread(target=run, name="probe-watch-check", daemon=True).start()
    return await asyncio.wait_for(result, timeout)


# -- the watch ------------------------------------------------------------------


@dataclass
class Incident:
    family: str
    reason: str
    sid: str | None
    facts: dict
    #: The consent variables of each event's own environment, where it had one.
    envs: list
    #: Reported once ever: the key `watch.json` keeps once it was.
    once: str | None
    at: float
    #: The sessions whose agent ran when it was noted (None: not yet looked at).
    voters: list | None = None
    #: Looked at while discovering: those sessions are joined by the ones back
    #: once the window is over (`merge_voters`).
    partial: bool = False
    #: Its consent: `(allowed, why, the env the child gets)`; asked again at a retry.
    verdict: tuple | None = None
    #: Not sent before this (wall): a report tried again later.
    not_before: float = 0.0
    #: When it was first tried and did not land (a retry follows), else None.
    first_try: float | None = None

    @property
    def key(self) -> tuple:
        return self.family, self.sid


def _unknown(live: Live) -> bool:
    """Says nothing yet: no environment of its recorder's, no `report_env`."""
    return live.hosted_env is None and live.report_env is None


def merge_voters(then: list, now: list) -> list:
    """Every session of either moment: one that ran then counts as it was
    (it ended or not); one whose consent was not yet known then (a hosted
    session restored before its recorder resumed) is asked as it is now."""
    merged = {v.sid: v for v in then}
    for live in now:
        if live.sid not in merged or _unknown(merged[live.sid]):
            merged[live.sid] = live
    return list(merged.values())


async def _run_report(params: dict) -> tuple[int | None, object]:
    from . import children

    return await children.run_read(REPORT_READ, params, timeout=REPORT_TIMEOUT_S)


def _never() -> bool:
    return False


class Watch:
    """`note` from any thread (it reads nothing from disk); the rest on the service's loop."""

    def __init__(
        self,
        *,
        log: Callable[[str], None],
        loop_getter: Callable[[], asyncio.AbstractEventLoop | None],
        voters: Callable[[], list],
        updating: Callable[[], bool] = _never,
        barrier_up: Callable[[], bool] = _never,
        discovering: Callable[[], bool] = _never,
        sessions: Callable[[], list] = list,
        hosted_env: Callable[[str], dict | None] = lambda sid: None,
        supervised: Callable[[str], bool] = lambda sid: False,
        recorders: Callable[[], list] = list,
        receipts: Callable[[], object] = _no_receipts,
        outbox: Callable[[float], tuple | None] = outbox_condition,
        credentials: Callable[..., dict] = credential_verdicts,
        run_report: Callable[[dict], object] = _run_report,
        login: Callable[[], object] = login_env,
        clock: Callable[[], float] = time.time,
        monotonic: Callable[[], float] = time.monotonic,
        scan_s: float | None = None,
    ) -> None:
        self.log = log
        self._loop_getter = loop_getter
        #: An update cycle runs or applies (`Service._updating`): cheap, from any thread.
        self.updating = updating
        #: The update barrier or the workers' hold is up: reads files (and may
        #: run `ps` on macOS), so only the scan asks, on a thread.
        self.barrier_up = barrier_up
        self.discovering = discovering
        #: The live registered sessions (`registry.Session`s).
        self.sessions = sessions
        #: Every registered session whose agent runs (one switched to mode off
        #: included), as `Live`s: whose consent a report needs. Required: a
        #: default of "none" would let every machine report out.
        self.voters = voters
        #: A hosted session's environment (its recorder's), or None.
        self.hosted_env = hosted_env
        #: Is the session's daemon worker supervised here (`workers.WorkerHost`)?
        self.supervised = supervised
        #: Each hosted recorder inside `hosted.record`: `{sid, beat_age_s, owner}`.
        self.recorders = recorders
        #: The delivery receipts of the sessions whose agent runs, `{sid:
        #: receipts or None}` (`receipts.ReceiptCache`), awaited on the loop.
        self.receipts = receipts
        #: The outbox's stuck condition (`outbox_condition`), on a thread.
        self.outbox = outbox
        #: Each key's verdict (`credential_verdicts`), on a thread.
        self.credentials = credentials
        self.run_report = run_report
        self.login = login
        self.clock = clock
        self.monotonic = monotonic
        self.scan_s = scan_s if scan_s is not None else _env_float(SCAN_ENV, SCAN_S)
        self.enabled = reports_enabled()
        self._lock = threading.Lock()
        #: (family, sid) -> deque of (monotonic, facts, consent env or None): the events in the window.
        self._seen: dict = {}
        #: Incidents noted and not yet looked at by the loop (consent fixed there).
        self._fresh: list = []
        #: (family, sid) -> Incident, looked at, waiting for the slot (oldest first).
        self._pending: dict = {}
        #: (family, sid) -> when (wall) a report child last ran for it, or it was declined.
        self._settled: dict = {}
        #: Keys of `watch.json` (`once`), oldest first, read on first use.
        self._once: set | None = None
        self._once_order: list = []
        #: (family, sid) -> the condition seen at the last scan (two in a row make an incident).
        self._cond_last: dict = {}
        #: What the last scan read of the barrier (`barrier_up`).
        self._barrier = False
        #: The last scan's (wall, monotonic), and when (monotonic) a sleep was seen.
        self._tick: tuple | None = None
        self._woke_at: float | None = None
        self._last_scan: float | None = None
        self._recent: collections.deque = collections.deque(maxlen=RECENT)
        self._child: asyncio.Future | None = None
        self._sending = False
        self._timer: asyncio.TimerHandle | None = None
        self._tasks: set = set()
        self._login_cache: tuple[float, dict | None] | None = None
        #: When (monotonic) the slower checks last ran; None: on the next scan.
        self._slow_at: float | None = None
        #: The slower checks' conditions seen at their last run (two in a row make one).
        self._slow_last: dict = {}
        #: Each key's id (`_credential_id`) -> when (wall) it was last answered
        #: (`watch.json`), read on first use.
        self._credentials_at: dict = {}
        #: The credential check running in the background, if one is.
        self._credential_task: asyncio.Future | None = None
        #: Each key's id -> when (wall) it was last asked and not answered.
        self._credentials_tried: dict = {}
        #: The outbox read, while one is still on its thread.
        self._outbox_busy = False
        #: The key check's thread, while one is still running (it may outlive
        #: its deadline: a server trickling its answer), and when (wall) the
        #: next may start after one was given up on.
        self._credentials_busy = False
        self._credentials_after = 0.0
        #: Serializes `watch.json`'s writes (snapshot to file), from any thread.
        self._state_write = threading.Lock()
        #: sid -> (receipt cursor, since when it has not moved) (`capture_conditions`).
        self._capture_still: dict = {}
        self._closed = False
        self.reports = 0

    # -- noting ----------------------------------------------------------------

    def note(
        self,
        family: str,
        reason: str,
        sid: str | None = None,
        facts: Mapping | None = None,
        *,
        env: Mapping | None = None,
        once: str | None = None,
        threshold: int | None = None,
    ) -> None:
        """One event of `family` (`reason`, a slug) from anywhere: at the
        family's threshold within WINDOW_S (or `threshold`) an incident, whose
        consent the loop fixes at once. `env`: the environment it happened in
        (a session's, a hook event's, an SDK caller's): its opt-out counts.
        `once`: report this key once ever. Reads no file. Never raises."""
        try:
            self._note(family, reason, sid, facts, env, once, threshold)
        except Exception as exc:  # noqa: BLE001 -- the watch never costs its caller anything
            with contextlib.suppress(Exception):
                self.log(f"watch: noting {family} failed: {exc!r}")

    def _note(self, family, reason, sid, facts, env, once, threshold) -> None:
        if self._closed or not self.enabled:
            return
        if family not in KEPT_WHILE_UPDATING and self._quiet():
            return  # an update's hand-over: what fails meanwhile is its doing
        key = (family, sid if family in SESSION_FAMILIES else None)
        # A condition two scans confirmed (`threshold`: `stalled`, `gone`, a
        # lease) is counted on its own: never with the family's other events.
        counter = key if threshold is None else (*key, reason)
        threshold = threshold if threshold is not None else THRESHOLDS.get(family, 1)
        now = self.monotonic()
        with self._lock:
            if once is not None and once in self._load_state():
                return
            seen = self._seen.setdefault(counter, collections.deque())
            seen.append((now, bounded_facts(facts), consent_env(env) if env is not None else None))
            while seen and now - seen[0][0] > WINDOW_S:
                seen.popleft()
            if len(seen) < threshold:
                return
            events = list(seen)
            seen.clear()
            settled = self._settled.get(key)
            if settled is not None and 0 <= self.clock() - settled < DEDUPE_S:
                return
            if len(events) > 1:
                detail = {"count": len(events), "window_s": WINDOW_S, "events": [f for _, f, _ in events[-KEEP_EVENTS:]]}
            else:
                detail = events[-1][1]
            envs = [e for _, _, e in events if e is not None]
            self._fresh.append(Incident(family, reason, key[1], detail, envs, once, self.clock()))
            del self._fresh[:-MAX_PENDING]
        self._kick()

    def _quiet(self) -> bool:
        """An update's hand-over is under way: the cycle (asked now, cheap) or
        the barrier (as the last scan read it)."""
        if self._barrier:
            return True
        try:
            return bool(self.updating())
        except Exception:  # noqa: BLE001 -- unknown: not quiet
            return False

    def _load_state(self) -> set:
        """`watch.json`, read once (under the lock): the once-ever keys, which
        it returns, and when each key was last answered (`_credentials_at`)."""
        if self._once is None:
            data = read_json(paths.service_dir() / STATE_NAME)
            keys = data.get("once") if isinstance(data, dict) else None
            self._once_order = [k for k in keys if isinstance(k, str)] if isinstance(keys, list) else []
            self._once = set(self._once_order)
            asked = data.get("credentials_at") if isinstance(data, dict) else None
            self._credentials_at = {
                k: float(v) for k, v in asked.items() if isinstance(k, str) and isinstance(v, (int, float))
            } if isinstance(asked, dict) else {}
        return self._once

    def _write_state(self) -> None:
        """`watch.json`: the once-ever keys and when each key was last answered.
        Snapshot and write under one lock of their own: two writers (a
        once-ever mark, a credential check) on two threads never land an older
        snapshot last."""
        with self._state_write:
            with self._lock:
                self._load_state()
                state = {"v": 1, "once": list(self._once_order)}
                if self._credentials_at:
                    state["credentials_at"] = dict(self._credentials_at)
            write_json(paths.service_dir() / STATE_NAME, state)

    def _mark_once(self, key: str) -> None:
        with self._lock:
            keys = self._load_state()
            if key in keys:
                return
            self._once_order = (self._once_order + [key])[-MAX_ONCE:]
            self._once = set(self._once_order)
        self._write_state()

    # -- the loop side -----------------------------------------------------------

    def start(self) -> None:
        """Arm the scan (the service calls it once it serves), having read what
        a note must know from the first: the once-ever record (never read under
        the lock on the loop later) and the barrier (else unknown until the
        first scan, SCAN_S away)."""
        if not self.enabled:
            return
        with self._lock:
            self._load_state()
        try:
            self._barrier = bool(self.barrier_up())
        except Exception:  # noqa: BLE001 -- unknown: not up
            self._barrier = False
        self._arm()

    def _arm(self) -> None:
        loop = self._loop_getter()
        if loop is None or self._closed:
            return
        self._timer = loop.call_later(self.scan_s, self._tick_scan)

    def _tick_scan(self) -> None:
        self._timer = None
        self._spawn(self._scan())

    def _spawn(self, coro) -> None:
        task = asyncio.ensure_future(coro)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    def _kick(self) -> None:
        """From any thread: on the loop's next turn, the new incident's
        sessions are taken (`_triage`) -- whatever the report slot is doing
        meanwhile (a child running, a login shell asked) -- and a send is tried."""
        loop = self._loop_getter()
        if loop is None or loop.is_closed() or self._closed:
            return
        with contextlib.suppress(RuntimeError):
            loop.call_soon_threadsafe(self._kicked)

    def _kicked(self) -> None:
        self._triage()
        self._spawn(self._send_next())

    def _triage(self) -> None:
        """On the loop: each new incident gets the sessions whose agent runs
        NOW, the moment it is looked at (its consent is theirs and its own
        environment's). While discovering too, marked `partial`: those are
        joined, when it is decided, by the sessions back by then."""
        with self._lock:
            fresh, self._fresh = self._fresh, []
        if not fresh:
            return
        voters = list(self.voters())
        partial = bool(self.discovering())
        for incident in fresh:
            if incident.family not in KEPT_WHILE_UPDATING and self._quiet():
                continue  # an update began before it was looked at
            incident.voters, incident.partial = voters, partial
            with self._lock:
                self._pending.pop(incident.key, None)
                self._pending[incident.key] = incident
                while len(self._pending) > MAX_PENDING:
                    self._pending.pop(next(iter(self._pending)))

    def _sense_wake(self) -> None:
        """Wall time ran ahead of monotonic time since the last scan (a sleep,
        which monotonic time does not count), or the scans were far apart:
        every condition measured in time starts again, after WAKE_GRACE_S."""
        wall, mono = self.clock(), self.monotonic()
        if self._tick is not None:
            last_wall, last_mono = self._tick
            if (wall - last_wall) - (mono - last_mono) > WAKE_SLACK_S or mono - last_mono > max(
                WAKE_GAP_S, 4 * self.scan_s
            ):
                self._woke_at = mono
                self._cond_last = {}
                self.log("watch: the machine slept (or the scans stalled): what is measured in time waits "
                         f"{WAKE_GRACE_S:.0f} s")
        self._tick = (wall, mono)

    def _timed(self) -> bool:
        """May a condition measured in time count now (not just after a wake)?"""
        return self._woke_at is None or self.monotonic() - self._woke_at >= WAKE_GRACE_S

    def _prune(self) -> None:
        """Counts past their window and reports past their dedupe window go."""
        mono, wall = self.monotonic(), self.clock()
        with self._lock:
            for key, seen in list(self._seen.items()):
                while seen and mono - seen[0][0] > WINDOW_S:
                    seen.popleft()
                if not seen:
                    del self._seen[key]
            for key, at in list(self._settled.items()):
                if wall - at >= DEDUPE_S:
                    del self._settled[key]

    async def _scan(self) -> None:
        try:
            self._last_scan = self.clock()
            self._sense_wake()
            self._prune()
            try:
                self._barrier = bool(await asyncio.to_thread(self.barrier_up))
            except Exception:  # noqa: BLE001 -- unknown: not up
                self._barrier = False
            if self.discovering() or self._quiet():
                return
            sessions = list(self.sessions())
            daemon = [
                (s.sid, s.state_dir) for s in sessions
                if getattr(s, "mode", None) == "daemon" and getattr(s, "state_dir", None) and not self.supervised(s.sid)
            ]
            # A `tap watch` session (its own recorder, not this service's): its
            # link's registration is its heartbeat; only with an agent that runs.
            heartbeats = [
                (s.sid, s.heartbeat_at) for s in sessions
                if getattr(s, "owner", None) is not None and getattr(s, "owner_live", False)
                and self.hosted_env(s.sid) is None and isinstance(getattr(s, "heartbeat_at", None), (int, float))
            ]
            beats = list(self.recorders())
            leases, stalled, record = await asyncio.to_thread(self._look, daemon, beats)
            self._conditions(leases, stalled, heartbeats)
            self._guard(record)
            await self._slow_checks()
            await self._send_next()
        except Exception as exc:  # noqa: BLE001 -- one bad scan never stops the next
            self.log(f"watch: scan failed: {exc!r}")
        finally:
            self._arm()

    def _look(self, daemon: list, beats: list) -> tuple[dict, dict, dict | None]:
        """On a thread (a session's state folder may be a slow mount, an
        owner's check runs `ps` on macOS): each unsupervised daemon session's
        lease condition, each hosted recorder stalled while its agent runs,
        and guard.json."""
        from . import guard, procid

        now = self.clock()
        leases = {}
        for sid, state_dir in daemon:
            found = lease_condition(state_dir, sid, now)
            if found is not None:
                leases[sid] = found
        stalled = {}
        for beat in beats:
            age, owner = beat.get("beat_age_s"), beat.get("owner")
            if not isinstance(age, (int, float)) or age <= STALL_S or not isinstance(owner, dict):
                continue
            try:
                running = procid.alive(int(owner["pid"]), str(owner["start_time"])) is not False
            except (KeyError, TypeError, ValueError):
                running = False
            if running:
                stalled[beat["sid"]] = {"beat_s": round(age)}
        return leases, stalled, guard.read()

    def _conditions(self, leases: dict, stalled: dict, heartbeats: list) -> None:
        """A failing condition on two scans in a row: one event (its family's
        threshold met). A condition measured in time waits out a wake."""
        timed = self._timed()
        found: dict = {}
        for sid, (cond, facts) in leases.items():
            if cond in ("hung", "not_running") and not timed:
                continue
            found[(Family.WORKER, sid)] = (cond, {**facts, "source": "lease"})
        if timed:
            for sid, facts in stalled.items():
                found[(Family.RECORDER, sid)] = ("stalled", facts)
            now = self.clock()
            for sid, heartbeat_at in heartbeats:
                if now - heartbeat_at > GONE_S:
                    found[(Family.RECORDER, sid)] = ("gone", {"heartbeat_s": round(now - heartbeat_at)})
        last, self._cond_last = self._cond_last, {key: cond for key, (cond, _) in found.items()}
        for (family, sid), (cond, facts) in found.items():
            if last.get((family, sid)) == cond:
                self.note(family, cond, sid, facts, threshold=1)

    async def _slow_checks(self) -> None:
        """Every SLOW_CHECK_S (and on the first scan): the outbox and each live
        session's receipts, a condition on two runs in a row making one event;
        every CREDENTIAL_CHECK_S, each key the CLI config holds. Measured in
        time, so never just after a wake."""
        mono = self.monotonic()
        if self._slow_at is not None and mono - self._slow_at < SLOW_CHECK_S:
            return
        self._slow_at = mono
        if not self._timed():
            self._slow_last = {}
            return
        now = self.clock()
        found: dict = {}
        #: The families whose read this time answered (a read given up on is
        #: no news either way: nothing it waits on is dropped).
        read: set = set()
        stuck = await self._read_outbox(now)
        if stuck is not _UNREAD:
            read.add(Family.OUTBOX_STUCK)
            if stuck is not None:
                found[(Family.OUTBOX_STUCK, None)] = stuck
        try:
            receipts = await self.receipts()
        except Exception as exc:  # noqa: BLE001 -- no receipts this time: nothing said about them
            self.log(f"watch: reading receipts failed: {exc!r}")
            receipts = None
        if isinstance(receipts, Mapping):
            read.add(Family.CAPTURE_STALLED)
        receipts = receipts if isinstance(receipts, Mapping) else {}
        stalled = capture_conditions(receipts, now, self._capture_still)
        if stalled:
            # One report for the machine, naming its sessions: an hour-long
            # stall of the server's ingestion stalls every session at once,
            # and that is one report per machine, not one per session.
            oldest = sorted(stalled, key=lambda sid: -stalled[sid]["received_h"])
            found[(Family.CAPTURE_STALLED, None)] = ("waiting", {
                "count": len(stalled), "sessions": {sid: stalled[sid] for sid in oldest[:CAPTURE_MAX_SESSIONS]}})
        last, self._slow_last = self._slow_last, {key: reason for key, (reason, _) in found.items()}
        for (family, sid), (reason, facts) in found.items():
            if last.get((family, sid)) == reason:
                self.note(family, reason, sid, facts, threshold=1)
        self._drop_cleared(found, read)
        if self._credential_task is None or self._credential_task.done():
            # Beside the scan, never in it: a server trickling its answer holds
            # this check (CREDENTIAL_DEADLINE_S at most), never the next scan.
            self._credential_task = asyncio.ensure_future(self._credential_check(now))
            self._tasks.add(self._credential_task)
            self._credential_task.add_done_callback(self._tasks.discard)

    async def _read_outbox(self, now: float) -> object:
        """`outbox_condition` on a thread of its own, given up past
        OUTBOX_TIMEOUT_S (a hung home mount), then `_UNREAD`; none started
        while the last one is still stuck there."""
        if self._outbox_busy:
            return _UNREAD
        self._outbox_busy = True

        def read() -> tuple | None:
            try:
                return self.outbox(now)
            finally:
                self._outbox_busy = False

        try:
            return await _on_daemon_thread(read, OUTBOX_TIMEOUT_S)
        except asyncio.TimeoutError:
            self.log("watch: reading the outbox did not finish in time")
            return _UNREAD

    def _drop_cleared(self, found: dict, read: set) -> None:
        """An outbox or capture incident still waiting (a retry) whose
        condition this check read and no longer sees is no longer news: it
        goes."""
        with self._lock:
            cleared = [key for key in self._pending
                       if key[0] in (Family.OUTBOX_STUCK, Family.CAPTURE_STALLED) and key[0] in read
                       and key not in found]
            for key in cleared:
                del self._pending[key]
        for family, _ in cleared:
            self.log(f"watch: {family} cleared before it was reported; dropped")

    async def _may_ask_keys(self) -> bool:
        """The consent a `credential_refused` report would need (a machine
        family's: every session whose agent runs, else the login shell, and
        the CLI config's backend), asked before the keys are: a check whose
        answer could not be reported is not made."""
        base_url = await asyncio.to_thread(config_base_url)
        voters = list(self.voters())
        login = None if voters else await self._login_env()
        allowed, _ = await asyncio.to_thread(decide_machine, voters, base_url, login)
        return allowed

    async def _credential_check(self, now: float) -> None:
        """Each key not answered within CREDENTIAL_CHECK_S, asked once (and
        one with no answer, offline or a timeout, again CREDENTIAL_RETRY_S
        later); a refused one is `credential_refused`, reported once for that
        key (a key replaced is a new one)."""
        try:
            if self._credentials_busy or now < self._credentials_after:
                return
            if not self.enabled or not await self._may_ask_keys():
                return
            with self._lock:
                self._load_state()
                answered = dict(self._credentials_at)
            tried = dict(self._credentials_tried)

            def due(ident: str) -> bool:
                at, missed = answered.get(ident), tried.get(ident)
                if missed is not None and 0 <= now - missed < CREDENTIAL_RETRY_S:
                    return False
                return at is None or not 0 <= now - at < CREDENTIAL_CHECK_S

            def ask() -> dict:
                try:
                    return self.credentials(due=due)
                finally:
                    self._credentials_busy = False

            self._credentials_busy = True
            try:
                verdicts = await _on_daemon_thread(ask, CREDENTIAL_DEADLINE_S + CREDENTIAL_TIMEOUT_S)
            except RuntimeError:  # no thread could start: nothing holds the guard
                self._credentials_busy = False
                raise
            except asyncio.TimeoutError:
                self._credentials_after = now + CREDENTIAL_RETRY_S
                self.log("watch: the credential check did not finish in time")
                return
            for ident, verdict in verdicts.values():
                if verdict == "unknown":
                    self._credentials_tried[ident] = now
                else:
                    self._credentials_tried.pop(ident, None)
            settled = {ident: now for ident, verdict in verdicts.values() if verdict != "unknown"}
            if settled:
                with self._lock:
                    kept = {k: v for k, v in self._credentials_at.items() if 0 <= now - v < 2 * CREDENTIAL_CHECK_S}
                    self._credentials_at = {**kept, **settled}
                await asyncio.to_thread(self._write_state)
            refused = sorted(kind for kind, (_, verdict) in verdicts.items() if verdict == "refused")
            if refused:
                unknown = sorted(kind for kind, (_, verdict) in verdicts.items() if verdict == "unknown")
                idents = ",".join(sorted(verdicts[kind][0] for kind in refused))
                self.note(Family.CREDENTIAL_REFUSED, "refused", None, {"refused": refused, "unknown": unknown},
                          once=f"credential_refused:{idents}")
                await self._send_next()  # it finished after the scan's own send
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 -- one bad check never stops the watch
            self.log(f"watch: the credential check failed: {exc!r}")

    def _guard(self, record: dict | None) -> None:
        """A switch-back the guard recorded lately (`guard.json` `ok: false`):
        one `update_rejected`, once per rejected version."""
        if not isinstance(record, dict) or record.get("ok") is not False:
            return
        rejected, at = record.get("to"), record.get("at")
        if not isinstance(rejected, str) or not isinstance(at, (int, float)) or self.clock() - at > GUARD_FRESH_S:
            return
        facts = {"rejected_version": rejected, **{k: record.get(k) for k in ("from", "reason", "rollback", "active",
                                                                            "answering", "at")}}
        self.note(Family.UPDATE_REJECTED, "switched_back", None, facts, once=f"update_rejected:{rejected}")

    async def _send_next(self) -> None:
        """The oldest incident due, as one report child (one at a time); one
        whose consent says no is dropped."""
        if self._closed or self._sending or self._child is not None:
            return
        # Taken before the first await: a scan and a note's kick may both ask.
        self._sending = True
        try:
            self._triage()
            if self.discovering() or self._quiet():
                return
            now = self.clock()
            with self._lock:
                waiting = [i for i in self._pending.values() if i.not_before <= now]
            if not waiting:
                return
            base_url = await asyncio.to_thread(config_base_url)
            for incident in waiting:
                if incident.verdict is None:
                    incident.verdict = await self._consent(incident, base_url)
                allowed, why, env = incident.verdict
                if not allowed:
                    self._drop(incident, why)
                    continue
                self._start_child(incident, env)
                return
        finally:
            self._sending = False

    async def _consent(self, incident: Incident, base_url: str | None) -> tuple[bool, str, dict]:
        """From what it was noted with: the environments it happened in, and
        the sessions whose agent ran then (or, with none, the login shell).
        Looked at while discovering, or tried again after a failed try: the
        sessions of THIS moment are asked too (`merge_voters`)."""
        voters = list(incident.voters or [])
        if incident.partial or incident.first_try is not None:
            voters = merge_voters(voters, list(self.voters()))
        for env in incident.envs:
            if not await asyncio.to_thread(env_allows, env, base_url):
                return False, "the environment it happened in turns reports off", {}
        if incident.family in SESSION_FAMILIES:
            if incident.envs:
                return True, "its environment allows reports", dict(incident.envs[-1])
            own = next((v for v in voters if v.sid == incident.sid), None)
            return await asyncio.to_thread(decide_session, own, None, base_url)
        login = None
        if not voters:
            login = await self._login_env()
        allowed, why = await asyncio.to_thread(decide_machine, voters, base_url, login)
        return allowed, why, {}

    async def _login_env(self) -> dict | None:
        cached = self._login_cache
        if cached is not None and self.monotonic() - cached[0] < LOGIN_CACHE_S:
            return cached[1]
        try:
            found = await self.login()
        except Exception:  # noqa: BLE001 -- unknown: no
            found = None
        self._login_cache = (self.monotonic(), found if isinstance(found, dict) else None)
        return self._login_cache[1]

    def _drop(self, incident: Incident, why: str) -> None:
        with self._lock:
            # A newer event of the same key noted meanwhile goes with it: settled.
            self._pending.pop(incident.key, None)
            self._settled[incident.key] = self.clock()
        sid = f" (session {incident.sid})" if incident.sid else ""
        self.log(f"watch: {incident.family} ({incident.reason}){sid} not reported: {why}")

    def _start_child(self, incident: Incident, env: dict) -> None:
        with self._lock:
            self._pending.pop(incident.key, None)
            self._settled[incident.key] = self.clock()
        sid, facts = incident.sid, incident.facts
        if sid is not None and not _UUID.match(sid):
            # The `report` read would refuse the whole report over it.
            sid, facts = None, {**facts, "session": incident.sid}
        params = {"auto": True, "family": incident.family, "reason": incident.reason, "sid": sid,
                  "env": dict(env), "facts": facts}
        self._child = asyncio.ensure_future(self._report(incident, params))

    async def _report(self, incident: Incident, params: dict) -> None:
        sid = f" (session {incident.sid})" if incident.sid else ""
        tried = self.clock()
        try:
            value = None
            try:
                code, value = await self.run_report(params)
            except OSError as exc:
                said = f"could not start: {exc}"
            else:
                said = outcome(code, value)
            self.reports += 1
            self._recent.append({"family": incident.family, "reason": incident.reason, "sid": incident.sid,
                                 "answer": said, "at": tried})
            settled = taken(value)
            if settled and incident.first_try is not None and isinstance(value, dict) \
                    and value.get("skipped") == "deduped":
                settled = False  # the failed try's own claim of the window, not a report
            # Refused for its credentials, or too large: the child kept its claim
            # of the window (`report.RELEASED_ON`), so a retry would only answer
            # `deduped`. Not retried and not settled once-ever: the next window tries.
            kept = isinstance(value, dict) and value.get("skipped") in KEPT_CLAIM
            if not settled and not kept:
                # Tried again later, once-ever or not: a failed send (offline,
                # the server, killed) is no report, and settling it would hold
                # a recurring family back for DEDUPE_S with nothing sent.
                first = incident.first_try if incident.first_try is not None else tried
                if self.clock() - first < RETRY_FOR_S:
                    # Its consent is asked again then, of that moment's sessions too.
                    wait = RATE_LIMITED_RETRY_S if isinstance(value, dict) and value.get("skipped") == "rate_limited" \
                        else RETRY_S
                    incident.first_try, incident.not_before, incident.verdict = first, self.clock() + wait, None
                    with self._lock:
                        self._pending.setdefault(incident.key, incident)
                    said += f"; again in {wait / 60:.0f} min"
            self.log(f"watch: report {incident.family} ({incident.reason}){sid}: {said}")
            if incident.once is not None and settled:
                await asyncio.to_thread(self._mark_once, incident.once)
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001
            self.log(f"watch: report {incident.family}{sid} failed: {exc!r}")
        finally:
            self._child = None
            if not self._closed:
                self._spawn(self._send_next())

    def public(self) -> dict:
        """`service.status`'s `watch`: what `probe doctor` and the debug log show."""
        with self._lock:
            waiting = len(self._fresh) + len(self._pending)
        return {"enabled": self.enabled, "last_scan": self._last_scan, "waiting": waiting,
                "reports": list(self._recent)}

    def close(self) -> None:
        self._closed = True
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None


def lease_condition(state_dir: str, sid: str, now: float) -> tuple[str, dict] | None:
    """A failing daemon lease (`<state>/sessions/<sid>.writer`, the tap's and the
    worker's format), as `(condition, facts)`: `lease_<reason>` when released
    with a failure's reason, `hung` / `not_running` when it expired past
    LEASE_GRACE_S with the worker lock still held / not. None otherwise (no
    lease, a healthy one, a stop on purpose). Blocking: a thread."""
    data = read_json(Path(state_dir) / "sessions" / f"{sid}.writer", limit=64 * 1024)
    if not isinstance(data, dict) or data.get("writer") != "daemon":
        return None
    reason, expires = data.get("reason"), data.get("expires_at")
    if reason in LEASE_FAILURES:
        return f"lease_{reason}", {"lease_reason": reason, "released_at": data.get("renewed_at")}
    if reason is None and isinstance(expires, (int, float)) and now - expires > LEASE_GRACE_S:
        try:
            from .workers import lock_held, safe_sid

            held = lock_held(Path(state_dir) / "daemon" / f"{safe_sid(sid)}.lock")
        except Exception:  # noqa: BLE001 -- no flock here (Windows): lapsed, cause unknown
            held = False
        return ("hung" if held else "not_running"), {"expired_s": round(now - expires)}
    return None


__all__ = [
    "Family",
    "Live",
    "TracebackGate",
    "Watch",
    "decide_machine",
    "decide_session",
    "last_run",
    "previous_holder",
    "record_crash",
    "sessions_on_disk",
]
