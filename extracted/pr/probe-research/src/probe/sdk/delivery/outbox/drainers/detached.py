"""DetachedWorker (Drainer): fork `python -m probe.sdk.delivery.outbox` when work is queued and nobody holds the lease, with the credential env it needs."""

from __future__ import annotations

import os
import subprocess
import sys
import time

from ....._shared import oscompat
from .....foundation.safe_warn import safe_warn as _diagnostics
from probe.sdk.delivery.outbox.lease import _lease_is_free
from probe.sdk.delivery.outbox.linger import _has_queued_op

#: How long an auth block suppresses new workers before ONE re-probe is allowed.
#:
#: The zombie-uploader hard stop is right but was permanent: `auth_blocked_since` suppressed
#: every future spawn forever, so a token that expired or rotated mid-run left a training
#: loop queueing for hours with no delivery, retry or signal, recoverable only by someone
#: running `probe outbox retry`. Credentials come back (re-login, rotated service token,
#: remounted secret) and delivery must resume on its own.
#:
#: One attempt per cooldown is not a zombie uploader: two orders of magnitude slower than
#: the backoff loop, and a still-rejected credential just re-stamps the block.
_AUTH_RETRY_COOLDOWN_SECONDS = 300.0
_LOG_NAME = "drainer.log"


def _auth_block_is_fresh(stamped_at: str | None) -> bool:
    """Whether an auth block is still inside its cooldown. An unparseable or absent stamp
    answers False: suppression must be positively justified, because getting it wrong is
    silence (a queue that never drains and never says why).
    """
    if not stamped_at:
        return False
    from datetime import datetime, timezone

    try:
        blocked_at = datetime.fromisoformat(str(stamped_at))
    except (TypeError, ValueError):
        return False
    if blocked_at.tzinfo is None:
        blocked_at = blocked_at.replace(tzinfo=timezone.utc)
    try:
        age = (datetime.now(timezone.utc) - blocked_at).total_seconds()
    except (OverflowError, OSError, ValueError):
        return False
    # A stamp from the future (a clock step) reads as fresh, deliberately: it expires once
    # the clock catches up, and re-probing every kick meanwhile is the pitfall guarded.
    return age < _AUTH_RETRY_COOLDOWN_SECONDS


def _env_fingerprints(environ=None) -> set:
    """The fingerprints this process's environment credential goes by: its `PROBE_TOKEN`'s
    and its `PROBE_INGEST_TOKEN`'s alone (an ingest-only job's queue is named by it,
    `Client._credential_queue_name`). ``environ``: another process's variables."""
    from ..drain.credentials import credential_fingerprint

    env = os.environ if environ is None else environ
    token = env.get("PROBE_TOKEN") or None
    ingest = env.get("PROBE_INGEST_TOKEN") or None
    return {fp for fp in (credential_fingerprint(token, None), credential_fingerprint(None, ingest)) if fp}


def env_fingerprints(environ=None) -> set:
    """The fingerprints of this process's environment credentials (``environ``: another
    process's, as the Probe daemon host reads one session's)."""
    return _env_fingerprints(environ)


def _holds_the_queues_credential(journal) -> bool:
    """Whether ``journal`` is a credential queue (#2035) whose credential this process holds:
    what another drainer recorded as held there is this process's to send, so its kick must
    not be suppressed."""
    from ...ops.ops import CREDENTIAL_NAMESPACE

    return journal.dir.parent.name == CREDENTIAL_NAMESPACE and journal.dir.name in _env_fingerprints()


def _own_credential_queue(journal):
    """This process's environment credential's queue under a root, if any (`PROBE_TOKEN`/
    `PROBE_INGEST_TOKEN`). Env only: O(1) on the kick path."""
    from ...ops.ops import CREDENTIAL_NAMESPACE

    if journal.receipt_enabled or journal.dir.parent.name == CREDENTIAL_NAMESPACE:
        return None
    for fingerprint in sorted(_env_fingerprints()):
        queue = journal.dir / CREDENTIAL_NAMESPACE / fingerprint
        if queue.is_dir():
            return queue
    return None


#: How often one process kicks the adopted credential queues (`maybe_spawn`).
_ADOPTED_KICK_SECONDS = 30.0
_ADOPTED_KICKED_AT = float("-inf")


def _adopted_credential_queues(journal) -> list:
    """The credential queues under a root whose credential was adopted (`probe outbox adopt`,
    the rescue): their writes go with the stored login, which any worker can build, so any
    kick may start theirs. On the kick path: one stat of the adoptions record (parsed only
    when changed) and, only with adoptions, one listing of the credential queues."""
    from ...ops.ops import CREDENTIAL_NAMESPACE
    from ..drain.adoption import _adoptions_path
    from ..drain.accounts import _read_records

    if journal.receipt_enabled or journal.dir.parent.name == CREDENTIAL_NAMESPACE:
        return []
    adopted = _read_records(_adoptions_path())
    if not adopted:
        return []
    try:
        present = os.listdir(journal.dir / CREDENTIAL_NAMESPACE)
    except OSError:
        return []
    return [
        journal.dir / CREDENTIAL_NAMESPACE / name for name in sorted(present) if name in adopted
    ]


#: How long a recorded "everything left is held" suppresses new workers.
_HELD_RESPAWN_SECONDS = 300.0


def _held_is_fresh(status: dict) -> bool:
    from datetime import datetime, timezone

    try:
        at = datetime.fromisoformat(str(status.get("held_at") or ""))
    except ValueError:
        return False
    if at.tzinfo is None:
        at = at.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - at).total_seconds() < _HELD_RESPAWN_SECONDS


def maybe_spawn(directory: str | None = None) -> bool:
    """Fork a detached worker when there is work and nobody owns the lease.

    O(1) by requirement: this runs after every enqueue and every CLI invocation (`probe log`
    in training loops), so it reads ONLY status.json plus one lock probe, never the op files
    (perf review: the old pending() parsed the whole queue), plus for adopted credential
    queues one stat and (with adoptions) one listing (`_adopted_credential_queues`). When
    status.json reads zero it also lists ``ops/`` to the first op (`_has_queued_op`).
    Returns True when a worker was spawned.
    """
    from ...ops.ops import CREDENTIAL_NAMESPACE
    from ...journal.journal import Journal

    journal = Journal(directory)
    child_spawned = False
    if not journal.receipt_enabled:
        child = Journal.for_receipts(journal.dir)
        if child.dir.exists():
            # An older root worker may hold its own lease; it cannot enumerate this namespace
            # and its lease must not suppress the capable worker.
            child_spawned = maybe_spawn(str(child.dir))
        # Of the credential queues (#2035): THIS process's own (a worker spawned here carries
        # this environment, which holds that credential and no other) and the adopted ones
        # (stored login, any worker can build). The rest are kicked by their own writers.
        own = _own_credential_queue(journal)
        if own is not None:
            child_spawned = maybe_spawn(str(own)) or child_spawned
        global _ADOPTED_KICKED_AT
        if (
            journal.dir.parent.name != CREDENTIAL_NAMESPACE
            and time.monotonic() - _ADOPTED_KICKED_AT >= _ADOPTED_KICK_SECONDS
        ):
            # At most every 30 s per process, counted on the ROOT's kicks only (a credential
            # queue's kick has no adopted queues and must not spend the interval): while a
            # worker lives the caller's own throttle never arms, and this ran on every write.
            _ADOPTED_KICKED_AT = time.monotonic()
            for adopted in _adopted_credential_queues(journal):
                if adopted != own:
                    child_spawned = maybe_spawn(str(adopted)) or child_spawned
    status = Journal.read_status(directory, include_receipts=False) or {}
    # `waiting` comes from LISTING the waiting room, not status.json: an older worker rewrites
    # status.json from `ops/` alone and would read zero.
    waiting = int(status.get("waiting") or 0)
    # Plan (g): multipart uploads sit in their own queue, which status.json (rewritten by
    # older releases from `ops/` alone) never counts. Listed.
    from ..drain.lanes import _multipart_pending_count

    uploads = _multipart_pending_count(journal)
    if (
        not status.get("pending")
        and not _has_queued_op(journal)
        and not waiting
        and not uploads
        and not journal.recovery_file.exists()
    ) or status.get("paused"):
        return child_spawned
    if _auth_block_is_fresh(status.get("auth_blocked_since")) and not waiting:
        # Suppressed, but not forever -- see _AUTH_RETRY_COOLDOWN_SECONDS.
        return child_spawned
    held = int(status.get("held") or 0)
    if (
        held
        and int(status.get("pending") or 0) <= held
        and not waiting
        and not uploads
        and _held_is_fresh(status)
        and not _holds_the_queues_credential(journal)
    ):
        # Everything queued is what the last pass had to leave held (another credential's
        # writes, a refused one's): nothing new to deliver, so no worker. A fork per kick cost
        # ~0.9 CPU-s each (#2041 round 3). A new op raises `pending` past `held`: spawns.
        return child_spawned
    if journal.paused:
        return child_spawned
    if not _lease_is_free(journal):
        # A worker owns delivery, maybe an OLDER release that never looks in the waiting room.
        # Waiting uploads still need a promoter: the child finds the drain lock taken and only
        # promotes (see `run`).
        if not (waiting and _lease_is_free(journal, str(journal.promote_lease))):
            return child_spawned
    else:
        # A Probe service runs here and starts this worker as its own child (plan Q5): same
        # module, interpreter, folder and environment but no credential. The lease stays the
        # one-worker guard. STARTED is a spawn (the caller's kick throttle arms on it);
        # RUNNING is a drainer at the lease, as the held branch above. With no service, an
        # older one or a refusal, fork as before.
        handed = _hand_to_service(journal)
        if handed is not None:
            from probe.service.protocol import BackgroundState

            if handed == BackgroundState.STARTED:
                return True
            if handed == BackgroundState.RUNNING:
                return child_spawned
    # PROBE_* env credentials inherit (T4 decision), except a copy of the stored login
    # (`_worker_env`). PROBE_OUTBOX_WORKER marks the worker: its clients print no delivery
    # notices (plan 1.7) and no Kubernetes notice (1.5) into drainer.log. Then no worker:
    # the next kick, or `probe outbox drain`, delivers.
    child = _spawn_detached(journal, [str(journal.dir)], _worker_env())
    if child is False:
        return child_spawned
    return _spawn_took(child, journal) or child_spawned


def _spawn_detached(journal, args: list, env: dict):
    """`python -m probe.sdk.delivery.outbox <args>`, detached, output to ``journal``'s
    drainer.log; what Popen returned, or False when it could not start. 0o600 explicitly:
    the log carries drain errors and tracebacks and the journal's everything-0o600 invariant
    must not depend on the umask. O_NOFOLLOW: a `drainer.log` symlink (planted in a shared
    directory) must not redirect the output (review of #2054)."""
    try:
        log_fd = os.open(
            journal.dir / _LOG_NAME,
            os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0),
            0o600,
        )
    except OSError:
        return False
    try:
        return subprocess.Popen(  # noqa: S603 -- our own interpreter, our own module
            [sys.executable, "-m", "probe.sdk.outbox_worker", *args],
            stdin=subprocess.DEVNULL,
            stdout=log_fd,
            stderr=log_fd,
            # Survives the parent CLI's exit and Ctrl-C: a new session on POSIX, a detached new
            # process group on Windows.
            **oscompat.DETACHED,
            close_fds=True,
            env=env,
        )
    except OSError:
        return False
    finally:
        os.close(log_fd)


#: Fingerprints of env tokens a client in THIS process found to be copies of the stored login
#: at start (`note_copied_login`). After a re-login the copy no longer equals the login but
#: is still a copy: a worker this process starts must not inherit it.
_COPIED_LOGINS: set = set()


def note_copied_login(fingerprint: str | None) -> None:
    """A client in this process runs with an env token that IS the stored login
    (`Client._is_the_stored_login`): its workers never inherit it."""
    if fingerprint:
        _COPIED_LOGINS.add(fingerprint)


def is_copied_login(fingerprint: str | None) -> bool:
    """Whether a client of this process found ``fingerprint`` a copy of the stored login
    (`note_copied_login`)."""
    return bool(fingerprint) and fingerprint in _COPIED_LOGINS


def _worker_env() -> dict:
    """The environment a spawned worker runs with: this one, marked as a worker, minus a
    `PROBE_TOKEN`/`PROBE_INGEST_TOKEN` that only copies this context's stored login for the
    same server (now, or when a client of this process started: `note_copied_login`). The
    worker reads that login itself: the same token today, a re-login's tomorrow. Inherited,
    the copy was matched first on every pass (`journal._settings_for_op`) and a dead one
    held the job's writes for good (a customer's Mac, 2026-10-23). Any other env
    credential inherits: the only way the worker can hold it."""
    from ....agent_session import EVENT_AT_ENV, RUN_PROCESS_ENV
    from ..drain.credentials import credential_fingerprint
    from ...transport.transport import _IDEMPOTENCY_ENV

    env = {**os.environ, "PROBE_OUTBOX_WORKER": "1"}
    # A daemon command's PROBE_IDEMPOTENCY_KEY numbers ITS writes; a worker numbering its
    # replays from the same base reuses those keys for other writes, which the server
    # refuses (422) and the drain dead-letters.
    env.pop(_IDEMPOTENCY_ENV, None)
    # Its PROBE_EVENT_AT dates ITS work: a worker dates each op by its own queue time and a
    # request outside an op must not inherit the command's.
    env.pop(EVENT_AT_ENV, None)
    # Likewise a run process's mark: each op says whether a run made it (R41).
    env.pop(RUN_PROCESS_ENV, None)
    if not (env.get("PROBE_TOKEN") or env.get("PROBE_INGEST_TOKEN")):
        return env
    for var, fingerprint in (
        ("PROBE_TOKEN", credential_fingerprint(env.get("PROBE_TOKEN"), None)),
        ("PROBE_INGEST_TOKEN", credential_fingerprint(None, env.get("PROBE_INGEST_TOKEN"))),
    ):
        if fingerprint and fingerprint in _COPIED_LOGINS:
            del env[var]
    token = env.get("PROBE_TOKEN")
    if token:
        from ..drain.accounts import was_login

        try:
            from ....settings import settings as config_module

            name = config_module.current_context_name() or None
            stored = config_module.load_context(name)
            base = (
                env.get("PROBE_BASE_URL")
                or stored.get("base_url")
                or config_module.DEFAULT_BASE_URL
            )
            identity = stored.get("identity") or {}
            account = (identity.get("customer_id"), identity.get("user_id"))
        except Exception:  # noqa: BLE001
            base, account = None, (None, None)
        if (
            base
            and all(account)
            and was_login(credential_fingerprint(token, None), base.rstrip("/"), account=account)
        ):
            del env["PROBE_TOKEN"]  # an earlier login of this account's, copied
    try:
        from ....settings import settings as config_module

        name = config_module.current_context_name() or None
        stored = config_module.load_context(name)
        stored_base = stored.get("base_url") or config_module.DEFAULT_BASE_URL
        base = env.get("PROBE_BASE_URL") or stored_base
    except Exception:  # noqa: BLE001 -- an unreadable config: inherit, as before
        return env
    if base.rstrip("/") != stored_base.rstrip("/"):
        return env
    for var, field in (("PROBE_TOKEN", "token"), ("PROBE_INGEST_TOKEN", "ingest_token")):
        if env.get(var) and env[var] == stored.get(field):
            del env[var]
    return env


def _hand_to_service(journal) -> str | None:
    """The running Probe service's answer when it took this queue's drain
    (`service_handoff.drain`: "started" or "running"), else None. A credential queue (#2035)
    or a folder inside one never goes: its worker needs the environment credential that
    named it, which never crosses the socket; nor does a worker's own kick. Never raises;
    bounded (`client.HANDOFF_BUDGET_S`)."""
    from ...ops.ops import CREDENTIAL_NAMESPACE

    if CREDENTIAL_NAMESPACE in journal.dir.parts or os.environ.get("PROBE_OUTBOX_WORKER"):
        return None
    try:
        from . import service_handoff

        return service_handoff.drain(str(journal.dir))
    except Exception:  # noqa: BLE001 -- a hand-off may never break an enqueue
        return None


#: How often `spawn_past_a_kill` looks at the lease while a killed worker goes.
_KILLED_LEASE_POLL_SECONDS = 0.005


def spawn_past_a_kill(directory: str, *, wait: float) -> bool:
    """`maybe_spawn` for a process whose own workers were just SIGKILLed: a Ray trial's actor
    at exit, after Ray's core worker killed its direct children
    (`fluent._arm_ray_trial_exit`).

    A SIGKILLed worker holds its lease until the kernel has torn it down (a CPU slot and
    unmapping its memory), and `maybe_spawn` reads a held lease as a worker delivering. The
    exit kick ran a fraction of a millisecond after the kill, inside that window, started
    nothing, and the run's close stayed queued (cli 0.201.3 release gate). So wait up to
    ``wait`` seconds for the lease to be let go, then kick. A lease still held at the end is
    a live worker's (a sibling trial delivering this queue): `maybe_spawn` leaves delivery
    to it, as always."""
    from ...journal.journal import Journal

    journal = Journal(directory)
    if journal.dir.is_dir():
        deadline = time.monotonic() + wait
        while not _lease_is_free(journal) and time.monotonic() < deadline:
            time.sleep(_KILLED_LEASE_POLL_SECONDS)
    return maybe_spawn(directory)


def _spawn_took(child, journal) -> bool:
    """Whether the child is actually alive, not merely forked.

    `Popen` succeeding says the fork worked, not that a worker runs: a frozen or embedded
    interpreter, a `sys.executable` that cannot `import probe`, or an ImportError under
    PyInstaller all exit at once yet returned True. The caller armed its kick throttle on
    that, so the journal grew while nothing drained and the only evidence was a traceback in
    drainer.log: the failure the queue exists to prevent.

    Cheap and optimistic: one non-blocking poll, and a short grace only if the child already
    died. A live worker takes the lease within milliseconds but waiting on that would put a
    sleep on the enqueue path, so "not dead yet" counts as spawned.
    """
    try:
        if child.poll() is None:
            return True
        # It exited already. Give the lease a beat to appear: a fast, successful
        # drain-and-exit looks like a failed start at this instant, and calling that a failure
        # would warn on healthy runs.
        time.sleep(0.05)
        if not _lease_is_free(journal):
            return True
        _diagnostics.warn(
            "probe: the outbox worker exited immediately "
            f"(rc={child.returncode}); queued writes are not being delivered. "
            f"See {journal.dir / _LOG_NAME}, or run `probe outbox drain`."
        )
        return False
    except Exception:  # noqa: BLE001 -- a liveness probe may never break enqueue
        return True
