"""Hand a training process's background work to the Probe service (plan Q5).

Beside a training loop the SDK forks detached processes of its own -- the
outbox's drainer (`outbox_worker.maybe_spawn`) and the box watcher
(`probe.box.spawn`) -- and its telemetry sender POSTs from a thread. When a
Probe service runs on this machine (an agent session or the desktop app
started it), each goes to the service instead: one supervisor for all of
them, and a training process that exits without waiting on PostHog. When it
cannot, the SDK does exactly what it did before, at once:

    no service, Windows, a frozen interpreter     fork / POST as before
    an older service (no such method or client)   as before; not asked again for 10 min
    a refusal (busy, failing, sandboxed, ...)      as before
    no answer within the budget                    as before; not asked again for 60 s

NEVER BLOCKS A TRAINING LOOP. ONE deadline, `client.HANDOFF_BUDGET_S` (0.25 s)
from the moment a hand-off is tried, covers everything: this machine's key
(which names the socket: a file read on Linux, a system call on macOS that may
wait), the socket folder's checks, the connect (a path lookup, which a stalled
home mount can hang), the request and its answer. All of it runs on a thread of
its own; the caller waits for that thread until the deadline and no longer,
and while one such thread is still out (hung on a mount) no second one starts:
the caller does it itself. The service is never started from here: only one
that already runs is asked.

NEVER A CREDENTIAL. A process whose environment holds one (`PROBE_TOKEN` and
the like, `protocol.secret_env`) keeps forking its own drainer and watcher:
they need it, and it never crosses the socket. The service's children deliver
with the stored login the queued ops already name (`journal.py`: ops pin a
context and an endpoint, never a token), so they do what the detached worker
this process would have forked does with the same environment and folder.

TELEMETRY ONCE. Each batch carries an id, and each of its entries a `uuid`
(PostHog collapses events that share one). A batch counts as handed off only
on an explicit `accepted`; when the request went out and no answer came back
(a timeout, a closed connection) it is sent again under the same id, which
the service takes once and acknowledges again. A refusal, or no answer after
TELEMETRY_TRIES, and this process POSTs it itself: the uuids make a copy the
service sent too collapse into one.

Stdlib only, and `probe.service` is not imported until a hand-off is tried.
"""

from __future__ import annotations

import os
import sys
import threading
import time
import uuid

#: After an answer that was not one (an older service, an error answer).
UNSUPPORTED_QUIET_S = 600.0
#: After no answer in time, or a broken one.
SLOW_QUIET_S = 60.0
#: After a sandbox refusal: this process's sandbox does not go away.
SANDBOX_QUIET_S = 3600.0
#: After the service refused this process's PROBE_BASE_URL (plan D10).
ENDPOINT_QUIET_S = 600.0
#: A telemetry batch is offered this many times while it goes unanswered.
TELEMETRY_TRIES = 3
#: What a new request waits, at most, for the one still out to finish.
INFLIGHT_WAIT_S = 0.05
#: Any of these set and telemetry is sent by this process itself: the
#: service's sender has its own network (no proxy, the default trust) and the
#: default PostHog host, which would then differ from this process's.
NETWORK_ENV = (
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
    "SSL_CERT_FILE",
    "SSL_CERT_DIR",
    "REQUESTS_CA_BUNDLE",
    "CURL_CA_BUNDLE",
    "PROBE_TELEMETRY_HOST",
)
#: `_quiet`'s key for every method at once.
_ALL = "*"


class Outcome:
    """What one request to the service came to (`_call`)."""

    ANSWERED = "answered"  # an answer (accepted or refused) is in hand
    NOT_SENT = "not_sent"  # it never went out: no service, no time, a thread still out
    UNANSWERED = "unanswered"  # it went out (or may have), and no answer came back
    ERROR = "error"  # an error answer: a service from before the method


_lock = threading.Lock()
#: method (or _ALL) -> until when (monotonic) the service is not asked.
_quiet_until: dict[str, float] = {}
#: The one request thread out at a time (a mount that hangs holds it), and its deadline.
_inflight: threading.Thread | None = None
_inflight_deadline = 0.0
#: `_call`'s NOT_SENT value when a request thread still out holds the way:
#: past its deadline it is hung, and the service is not asked for a while.
STUCK = object()


def _reset_after_fork() -> None:
    # A thread holding the lock at a fork (a DataLoader worker, say) would leave
    # the child's copy held for good, and its first enqueue would hang on it.
    # The request thread is the parent's: the child has none out.
    global _lock, _inflight
    _lock = threading.Lock()
    _inflight = None


if hasattr(os, "register_at_fork"):  # POSIX only
    os.register_at_fork(after_in_child=_reset_after_fork)


def reset(*, wait: float = 0.0) -> None:
    """Forget every back-off, after waiting up to `wait` for a request thread
    still out (tests)."""
    thread = _inflight
    if wait > 0 and thread is not None:
        thread.join(wait)
    with _lock:
        _quiet_until.clear()


def _quiet(key: str, seconds: float) -> None:
    with _lock:
        _quiet_until[key] = max(_quiet_until.get(key, 0.0), time.monotonic() + seconds)


def _quieted(method: str) -> bool:
    now = time.monotonic()
    with _lock:
        return _quiet_until.get(_ALL, 0.0) > now or _quiet_until.get(method, 0.0) > now


def _platform_ok() -> bool:
    """POSIX and a real interpreter file to start children on."""
    if os.name != "posix" or getattr(sys, "frozen", False):
        return False
    return bool(sys.executable) and os.path.isabs(sys.executable)


def env_credential() -> bool:
    """Whether this process's environment holds a Probe credential."""
    from probe.service.protocol import secret_env

    return any(value and secret_env(name) for name, value in os.environ.items())


def runtime_env() -> dict | None:
    """This process's environment as the service's child gets it
    (`protocol.runtime_env_name`), or None when it does not fit the request.
    An empty PROBE_BASE_URL is unset, as `config.resolve` reads it."""
    from probe.service.protocol import MAX_HOOK_ENV, MAX_HOOK_ENV_VALUE, runtime_env_name

    env = {}
    for name, value in os.environ.items():
        if not runtime_env_name(name) or (name == "PROBE_BASE_URL" and not value):
            continue
        if len(value) > MAX_HOOK_ENV_VALUE or "\0" in value:
            return None  # the child would miss it: fork as before
        env[name] = value
    return env if len(env) <= MAX_HOOK_ENV else None


def _cwd() -> str | None:
    try:
        return os.getcwd()
    except OSError:  # deleted under us: the service's default folder
        return None


def _version() -> str:
    try:
        from probe import __version__

        return str(__version__)
    except Exception:  # noqa: BLE001
        return "unknown"


def _call(send, deadline: float) -> tuple[str, object]:
    """`send(client, deadline, on_sent)` on a thread of its own, waited for
    until `deadline` (monotonic) and no longer: `(Outcome, answer or error)`.

    Everything that may block runs on that thread: this machine's key, the
    socket folder's checks, the connect. A thread still out from an earlier
    call (a home mount that hangs) means no second one: NOT_SENT."""
    global _inflight
    from probe.service import client, paths

    box: dict = {}
    sent = threading.Event()

    def run() -> None:
        try:
            paths.machine_key()  # cached after the first; may wait on macOS
            if time.monotonic() >= deadline:
                box["outcome"] = (Outcome.NOT_SENT, None)
                return
            answer = send(client, deadline, sent.set)
            box["outcome"] = (Outcome.ANSWERED, answer)
        except client.ServiceError as exc:
            box["outcome"] = (Outcome.ERROR, exc)
        except client.Unanswered as exc:
            box["outcome"] = (Outcome.UNANSWERED, exc)
        except Exception as exc:  # noqa: BLE001 -- no service, no time, a foreign folder: never the caller's
            box["outcome"] = (Outcome.UNANSWERED if sent.is_set() else Outcome.NOT_SENT, exc)

    global _inflight_deadline
    earlier = _inflight
    if earlier is not None and earlier.is_alive():
        if time.monotonic() >= _inflight_deadline + INFLIGHT_WAIT_S:
            return Outcome.NOT_SENT, STUCK  # past its own deadline: hung, not finishing
        # Its own deadline is behind it or near (every step it takes is
        # bounded by it, a hung mount aside): a moment for it to finish.
        earlier.join(max(0.0, min(INFLIGHT_WAIT_S, deadline - time.monotonic())))
    with _lock:
        if _inflight is not None and _inflight.is_alive():
            # Another request of this process, still within its deadline (a
            # telemetry batch beside a drain kick): this one is done here, and
            # nothing is backed off. Past its deadline: hung.
            return Outcome.NOT_SENT, (STUCK if time.monotonic() >= _inflight_deadline else None)
        thread = threading.Thread(target=run, name="probe-service-handoff", daemon=True)
        try:
            thread.start()
        except RuntimeError:  # no thread at this moment: do it ourselves
            return Outcome.NOT_SENT, None
        _inflight, _inflight_deadline = thread, deadline
    thread.join(max(0.0, deadline - time.monotonic()))
    if "outcome" in box:
        return box["outcome"]
    return (Outcome.UNANSWERED if sent.is_set() else Outcome.NOT_SENT), None


def _ask(method: str, send, *, budget: float | None = None, resend: bool = False) -> tuple[str, dict | None]:
    """One offer of `method` to the service, all within one budget:
    `(Outcome, its answer when ANSWERED and accepted, else None)`. The
    back-offs (module docstring) are kept here; a `resend` of a request that
    went unanswered is not held back by the one that set."""
    if not resend and _quieted(method):
        return Outcome.NOT_SENT, None
    try:
        from probe.service import client
        from probe.service.protocol import BackgroundRefusal
    except Exception:  # noqa: BLE001 -- an install without it forks as before
        _quiet(_ALL, UNSUPPORTED_QUIET_S)
        return Outcome.NOT_SENT, None
    deadline = time.monotonic() + (client.HANDOFF_BUDGET_S if budget is None else budget)
    outcome, value = _call(send, deadline)
    if outcome == Outcome.ERROR:
        _quiet(method, UNSUPPORTED_QUIET_S)
        return outcome, None
    if outcome == Outcome.NOT_SENT:
        if value is not None and not isinstance(value, (FileNotFoundError, ConnectionRefusedError)):
            _quiet(_ALL, SLOW_QUIET_S)  # a foreign folder, no time: not again for a while
        elif value is None and time.monotonic() >= deadline:
            _quiet(_ALL, SLOW_QUIET_S)  # the thread is still out (preparing): too slow
        return outcome, None
    if outcome == Outcome.UNANSWERED:
        _quiet(_ALL, SLOW_QUIET_S)
        return outcome, None
    answer = value
    if not isinstance(answer, dict):
        _quiet(method, UNSUPPORTED_QUIET_S)
        return Outcome.ERROR, None
    if answer.get("accepted") is True:
        return Outcome.ANSWERED, answer
    reason = answer.get("reason")
    if reason == BackgroundRefusal.SANDBOXED:
        _quiet(_ALL, SANDBOX_QUIET_S)
    elif reason == BackgroundRefusal.UNKNOWN_ENDPOINT:
        _quiet(method, ENDPOINT_QUIET_S)
    return Outcome.ANSWERED, None


def _background_env() -> dict | None:
    """The env for a child, when this process may hand one off at all."""
    if not _platform_ok() or env_credential():
        return None
    return runtime_env()


def drain(directory: str) -> str | None:
    """Ask the service to drain the outbox folder `directory`. Its answer's
    state (`protocol.BackgroundState`: STARTED, a child starts; RUNNING, a
    drainer holds the outbox's lease or is starting), or None: not taken,
    fork as before (a request that went unanswered too: two drainers meet at
    the lease, and one steps aside). Never raises."""
    try:
        env = _background_env()
        if env is None:
            return None
        from probe.sdk.agent_session import EVENT_AT_ENV, RUN_PROCESS_ENV
        from probe.service.protocol import Method

        # A drainer sends every writer's ops, each with its own date and origin
        # (`journal._delivery_scope`), so it inherits neither from this process
        # (`outbox_worker._worker_env`).
        env.pop(EVENT_AT_ENV, None)
        env.pop(RUN_PROCESS_ENV, None)
        path, cwd = os.path.abspath(str(directory)), _cwd()
        _, answer = _ask(Method.OUTBOX_DRAIN, lambda c, deadline, sent: c.drain_outbox(
            path, sys.executable, env, cwd=cwd, deadline=deadline, on_sent=sent, client_version=_version()))
        return answer.get("state") if answer else None
    except Exception:  # noqa: BLE001 -- a hand-off may never break an enqueue
        return None


def box_watch(directory: str | None = None) -> str | None:
    """Ask the service to run the watcher (`python -m probe.box`) of the box
    registry `directory` (default: the one this process registers in). Its
    answer's state, or None: not taken, spawn as before. Never raises."""
    try:
        env = _background_env()
        if env is None:
            return None
        from probe.box import registry

        env["PROBE_BOX_DIR"] = os.path.abspath(str(directory if directory is not None else registry.default_dir()))
        from probe.service.protocol import Method

        cwd = _cwd()
        _, answer = _ask(Method.BOX_WATCH, lambda c, deadline, sent: c.watch_box(
            sys.executable, env, cwd=cwd, deadline=deadline, on_sent=sent, client_version=_version()))
        return answer.get("state") if answer else None
    except Exception:  # noqa: BLE001 -- the watcher is never the run's problem
        return None


def stamp(entries: list) -> list:
    """Give each telemetry entry a `uuid` of its own (kept if it has one):
    PostHog collapses events that share one, so a batch both this process and
    the service send counts once."""
    for entry in entries:
        if isinstance(entry, dict):
            entry.setdefault("uuid", str(uuid.uuid4()))
    return entries


def telemetry(entries: list) -> bool:
    """Ask the service to POST one batch of telemetry entries this process
    built (`stamp` them first). True only when the service said it has it;
    False and the caller POSTs it itself. Each try has its own budget; the
    batch's id is the same on every try (module docstring)."""
    try:
        if not entries or not _platform_ok() or any(os.environ.get(name) for name in NETWORK_ENV):
            return False
        from probe.service.protocol import MAX_TELEMETRY_ENTRIES, Method

        if len(entries) > MAX_TELEMETRY_ENTRIES:
            return False
        batch_id = uuid.uuid4().hex
        for attempt in range(TELEMETRY_TRIES):
            outcome, answer = _ask(Method.TELEMETRY_SEND, lambda c, deadline, sent: c.send_telemetry(
                entries, batch_id=batch_id, deadline=deadline, on_sent=sent, client_version=_version()),
                resend=attempt > 0)
            if outcome != Outcome.UNANSWERED:
                return answer is not None
        return False
    except Exception:  # noqa: BLE001 -- observability must never become observable
        return False
