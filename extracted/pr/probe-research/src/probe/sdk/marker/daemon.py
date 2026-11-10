# ---------------------------------------------------------------------------
# THE DAEMON'S WRITE LEASE.
#
#   <sessions_dir>/<sid>.writer   JSON, written ONLY by the tap plugin's
#                                 companion worker (tap/companion_lease.py),
#                                 read here by the CLI write gate, the hooks
#                                 and the status line.
#
#   {"v": 1, "writer": "daemon", "pid": 123, "expires_at": 1790000000.0,
#    "renewed_at": 1789999940.0, "reason": null}
#
# The STATE says what the researcher wants; the LEASE says whether the daemon is
# actually doing it. `daemon` + a live lease: the daemon records and the CLI
# refuses the agent's ambient writes. `daemon` + no live lease (never started,
# crashed, hung past a cycle, out of budget, unauthorized): DEGRADED, and the
# agent records exactly as under `full` -- fall back to the agent, never to
# silence. The worker renews only when a cycle FINISHES in time, so a hung model
# call lets the lease lapse rather than holding writing hostage.
#
# UNREADABLE, MALFORMED, UNKNOWN-VERSION or EXPIRED all read as "no live lease".
# That is the fail-open direction on purpose: a broken file must hand writing
# back to the agent, never lock everybody out.
#
# The format is a CONTRACT between two packages that cannot import each other;
# tests/test_companion_lease_contract.py writes it with the worker's writer and
# reads it with this reader.
# ---------------------------------------------------------------------------

#: THE DAEMON HANDED WRITING BACK. Injected on the next prompt after the lease
#: lapses (tracking_guard) -- a dead worker cannot announce its own death, and an
#: agent told "the daemon records" has no other reason to look -- and at session
#: start when the daemon cannot run at all (version_check). `{reason}` is a
#: phrase from `DAEMON_REASON_WORDS`.
DAEMON_DEGRADED_NOTICE = (
    "Probe is in the `daemon` state, but the daemon is {reason}, so recording is back with "
    "you. Record the work as it happens, per `track-work`."
)
DAEMON_NOT_STARTED = "not-started"
DAEMON_REASON_WORDS = {
    DAEMON_NOT_STARTED: "not running",
    "expired": "not responding",
    "stopped": "stopped",
    "gateway": "unable to reach its model",
    "budget": "out of budget",
    "unauthorized": "not authorized",
    "error": "hitting an error",
    "disk_full": "out of disk space",
}


#: The worker let go of its lease to hand over (`probe.daemon.lease.REASON_HANDOVER`)
#: to a new daemon process: an update, the Probe service restarting or
#: stopping, a resumed session's worker, a session moved to the service. A
#: successor takes the lease within seconds, so nothing is back with the agent
#: and it says so: the degraded notice ("the daemon is not running, so
#: recording is back with you") was false here, and an agent that took it
#: recorded beside the daemon. One released over DAEMON_HANDOVER_STALE_S ago
#: (its `renewed_at` is the release time) had no successor: it reads as a
#: lease that lapsed (`expired`, "not responding"), and the agent records again.
#: An update holds new workers back while it runs (minutes, for a new CLI):
#: while that hold or its barrier is up the hand-over is live, and the count
#: runs from the later of the release and the hold's end (`_update_hold`).
DAEMON_HANDOVER = "handover"
DAEMON_HANDOVER_STALE_S = 120.0
DAEMON_HANDOVER_NOTICE = (
    "Probe's daemon is handing over to a new daemon process and keeps recording this session. "
    "Nothing for you to do."
)
#: In each of the Probe service's machine folders (`service_root()/<key>`):
#: the update's hold on new daemon workers (`probe.service.barrier.HOLD_NAME`),
#: stamped when it ends (`barrier.HOLD_RELEASED_NAME`), and its barrier
#: (`probe.service.paths.BARRIER_NAME`, also in the root from a service before
#: the machine key). Older than these they are stale (`barrier.HOLD_MAX_AGE_S`,
#: `barrier.MAX_AGE_S`). tests/test_daemon_hooks.py holds them equal.
UPDATE_HOLD_NAME = "workers.hold"
UPDATE_HOLD_RELEASED_NAME = "workers.released"
UPDATE_BARRIER_NAME = "update.barrier"
UPDATE_HOLD_MAX_AGE_S = 45 * 60
UPDATE_BARRIER_MAX_AGE_S = 15 * 60


def service_root() -> Path:
    """The Probe service's folders (`probe.service.paths.root_dir`):
    `~/.local/state/probe/service`, never moved by XDG_STATE_HOME; on Windows
    `%LOCALAPPDATA%\\probe\\service`."""
    if os.name == "nt":
        local = os.environ.get("LOCALAPPDATA")
        base = Path(local) if local else _home() / "AppData" / "Local"
        return base / "probe" / "service"
    return _home() / ".local" / "state" / "probe" / "service"


def _mtime(path: Path) -> "float | None":
    try:
        return path.stat().st_mtime
    except OSError:
        return None


def _update_hold(now: float) -> "tuple[bool, float]":
    """`(up, ended_at)`: is an update holding new daemon workers back (its hold
    or its barrier, fresh, in any machine folder of this user's service), and
    when did the last hold end (0 when never)? Never raises."""
    try:
        root = service_root()
        folders = [root, *(p for p in root.iterdir() if p.is_dir())]
    except (OSError, RuntimeError):
        return False, 0.0
    up, ended = False, 0.0
    for folder in folders:
        for name, max_age in ((UPDATE_HOLD_NAME, UPDATE_HOLD_MAX_AGE_S), (UPDATE_BARRIER_NAME, UPDATE_BARRIER_MAX_AGE_S)):
            at = _mtime(folder / name)
            if at is not None and now - at < max_age:
                up = True
        ended = max(ended, _mtime(folder / UPDATE_HOLD_RELEASED_NAME) or 0.0)
    return up, ended


def daemon_degraded_notice(reason: "str | None") -> str:
    if reason == DAEMON_HANDOVER:
        return DAEMON_HANDOVER_NOTICE
    return DAEMON_DEGRADED_NOTICE.format(reason=DAEMON_REASON_WORDS.get(reason or "", "not running"))


def companion_key_held(config: "dict | None" = None) -> bool:
    """Does the active context hold the daemon's own key (`companion_token`)?

    Without it the worker can never take the lease, so nothing should tell the
    agent the daemon records. Reads the same file the CLI and the tap do.
    """
    data = _read_config() if config is None else config
    contexts = data.get("contexts")
    if isinstance(contexts, dict):
        active = contexts.get(data.get("current_context") or "default")
        data = active if isinstance(active, dict) else {}
    value = data.get("companion_token")
    return isinstance(value, str) and bool(value.strip())


LEASE_SUFFIX = ".writer"
#: The once-per-change record of which handback notice was last shown; the guard
#: hook and pi's extension share it, so one change is never announced twice.
NOTIFIED_SUFFIX = ".writer-notified"
LEASE_VERSION = 1
DAEMON_LIVE = "live"
DAEMON_DEGRADED = "degraded"

#: `<sid>.worker`: what the Probe service last did about this chat's daemon worker, by wall clock, so the status
#: line, `probe statusline show` and pi can tell a worker that is starting from one that never will.
#: `{"state": "starting" | "gave_up" | "crash_loop", "at": <unix seconds>}`; the Supervisor writes it on spawn and
#: on give-up (`probe.service.sessions.workers`).
WORKER_SUFFIX = ".worker"
WORKER_STARTING = "starting"
WORKER_GAVE_UP = "gave_up"
WORKER_CRASH_LOOP = "crash_loop"
#: Any other exit (a crash before the third, a retry later): the launch it stamped is over, so it is not starting.
WORKER_EXITED = "exited"
WORKER_STATES = (WORKER_STARTING, WORKER_GAVE_UP, WORKER_CRASH_LOOP, WORKER_EXITED)
#: How long a spawned worker may go without its first lease before the line says `daemon not recording`.
DAEMON_START_GRACE_S = 120.0


def get_worker_stamp_path(session_id: str) -> Path:
    return sessions_dir() / (session_id + WORKER_SUFFIX)


def write_worker_stamp(session_id: str, state: str, now: "float | None" = None) -> bool:
    """Record what the service just did about this chat's worker. True when it landed; never raises."""
    if not valid_session_id(session_id) or state not in WORKER_STATES:
        return False
    record = {"state": state, "at": time.time() if now is None else now}
    try:
        return _publish_atomically(get_worker_stamp_path(session_id), json.dumps(record) + "\n")
    except OSError:
        return False


def read_worker_stamp(session_id: str) -> "dict | None":
    """The worker stamp when well-formed, else None (no stamp: an older service, or no worker asked for yet)."""
    if not valid_session_id(session_id):
        return None
    try:
        data = json.loads(get_worker_stamp_path(session_id).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or data.get("state") not in WORKER_STATES:
        return None
    try:
        at = float(data.get("at"))
    except (TypeError, ValueError):
        return None
    return {"state": data["state"], "at": at} if math.isfinite(at) else None


def is_worker_starting(session_id: str, now: "float | None" = None) -> "bool | None":
    """Whether a chat with no lease yet is still STARTING: True within DAEMON_START_GRACE_S of the service asking for
    its worker, False after that or once the service gave up, None with no stamp (an older service: keep today's
    rule, a held key reads as starting)."""
    stamp = read_worker_stamp(session_id)
    if stamp is None:
        return None
    if stamp["state"] != WORKER_STARTING:
        return False
    at = time.time() if now is None else now
    return 0 <= at - stamp["at"] <= DAEMON_START_GRACE_S


def is_daemon_starting(session_id: str, daemon: "tuple | None", config: "dict | None" = None) -> bool:
    """Is a daemon chat with no lease yet still STARTING (no note)? Its worker has taken no lease (`not-started`), the
    daemon's key is held (without it no worker ever can) and the service asked for it at most DAEMON_START_GRACE_S
    ago (no stamp: an older service, today's rule). One rule for the line and `probe statusline show`."""
    return (daemon is not None and daemon[1] == DAEMON_NOT_STARTED and companion_key_held(config)
            and is_worker_starting(session_id) is not False)


def lease_path(session_id: str) -> Path:
    return sessions_dir() / (session_id + LEASE_SUFFIX)


def read_lease(session_id: str) -> "dict | None":
    """The lease file's content when it is well-formed, else None. No liveness check."""
    if not valid_session_id(session_id):
        return None
    try:
        data = json.loads(lease_path(session_id).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or data.get("v") != LEASE_VERSION:
        return None
    if data.get("writer") != "daemon":
        return None
    try:
        float(data.get("expires_at"))
    except (TypeError, ValueError):
        return None
    return data


def lease_live(session_id: str, now: "float | None" = None) -> bool:
    lease = read_lease(session_id)
    if lease is None or lease.get("reason"):
        return False
    return float(lease["expires_at"]) > (time.time() if now is None else now)


def daemon_status(
    session_id: str, state: "str | None" = None, now: "float | None" = None
) -> "tuple[str, str | None] | None":
    """`(live|degraded, reason)` for a session in the `daemon` state, else None.

    `reason` is what the worker recorded when it released the lease
    (`unauthorized`, `budget`, `gateway`, `stopped`, `handover`), `expired`
    when the lease simply lapsed (or a hand-over no successor took up within
    DAEMON_HANDOVER_STALE_S of its release or of the end of the update hold it
    waited for), or `not-started` when there is no lease at all.
    """
    if state is None:
        state = session_state(session_id)
    if state != STATE_DAEMON:
        return None
    lease = read_lease(session_id)
    if lease is None:
        return (DAEMON_DEGRADED, DAEMON_NOT_STARTED)
    if lease.get("reason") == DAEMON_HANDOVER:
        try:
            released = float(lease.get("renewed_at") or lease["expires_at"])
        except (TypeError, ValueError):
            released = 0.0
        at = time.time() if now is None else now
        if at - released > DAEMON_HANDOVER_STALE_S:
            up, ended = _update_hold(at)
            if not up and at - max(released, ended) > DAEMON_HANDOVER_STALE_S:
                return (DAEMON_DEGRADED, "expired")  # no successor took it up
    if lease.get("reason"):
        return (DAEMON_DEGRADED, str(lease["reason"]))
    if float(lease["expires_at"]) <= (time.time() if now is None else now):
        return (DAEMON_DEGRADED, "expired")
    return (DAEMON_LIVE, None)


def agent_writes_freely(session_id: str, state: "str | None" = None) -> bool:
    """May the AGENT make ambient writes in this session right now?

    `full`, and `daemon` whose lease is not live (degraded). Not `read-only`,
    not `off`, not `daemon` with a live lease -- there the daemon records and the
    agent writes only what the researcher asks for (`--directed`) and what a run
    launch needs.
    """
    if state is None:
        state = session_state(session_id)
    if state == STATE_FULL:
        return True
    status = daemon_status(session_id, state)
    return status is not None and status[0] == DAEMON_DEGRADED


