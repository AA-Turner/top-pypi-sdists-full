"""The detached outbox drainer: wake on enqueue, drain until empty, exit.

Model (eng review 2026-07-29, 3A): the FIRST enqueue forks one detached
worker; later enqueues see the live flock lease and skip, so a training loop
queueing hundreds of writes forks once per idle period, not per write. The
worker loops with capped backoff until the journal is empty, then exits --
there is no daemon to install or forget.

Hard stops, so this can never become the tap's zombie-uploader pitfall:
  * 401/403 -> the drain reports auth-blocked; ops stay queued untouched
    -- EXCEPT a workspace-write refusal (403 `workspace_write_denied`),
    which is per-DESTINATION rather than per-credential: that op
    dead-letters and the queue keeps flowing. See
    `errors.WorkspaceLockedError` for why parking there would be wrong.
    (T2-A) and the worker EXITS -- it never retries with rejected credentials.
    The suppression is a COOLDOWN, not a permanent stop: one re-probe is
    allowed every `_AUTH_RETRY_COOLDOWN_SECONDS`, so a rotated or re-issued
    credential resumes delivery on its own instead of requiring someone to
    notice and run `probe outbox retry`. One attempt per five minutes is not a
    zombie uploader; forever-silence with a growing queue was worse.
  * `probe outbox pause` -> exits at the next loop turn. This is the outbox's
    OWN switch; it is deliberately not the capture-consent killswitch.

A worker that dies (crash, reboot) is re-kicked by the next probe command of
any kind; `probe run end` remains the synchronous, run-scoped barrier.

When a Probe service runs on the machine, the fork goes to it (plan Q5,
`service_handoff`): the service starts this same module on the kicking
process's interpreter as its own child, and the lease, the exit guard and
every hard stop below are unchanged. Credential queues, processes holding a
credential in their environment, Windows and no service all fork as before.

Lives in the SDK (parity F1, docs/2026-08-04-outbox-miles-parity.md) so both
CLI commands and ``Client(async_writes=True)`` writers kick the same worker;
``probe.cli.outbox_worker`` stays behind as a runnable shim because workers
spawned by older releases exec that module path.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from probe._compat import StrEnum

from .._shared import oscompat
from . import durable
from . import safe_warn as _diagnostics


class OutboxOutcome(StrEnum):
    """Why a drain episode ended — the worker's exit codes, given names.

    Lives here rather than in `cli.telemetry` (where the other event
    vocabularies sit) because the worker is the only producer, and the SDK must
    not import the CLI to name its own states. `emit_outbox_drained` takes it
    as a plain str, so there is exactly one definition either way.

    DRAINED is the only member that means the queue is empty. The other three
    all mean "ops are still queued", and they stay apart because they need
    different fixes: STALLED is the server or the network and heals itself,
    AUTH_BLOCKED needs a credential, PAUSED is someone's deliberate switch.
    Folding them into one "failed" would bury the state a human must act on
    behind the two that resolve on their own.
    """

    DRAINED = "drained"  # exit 0
    AUTH_BLOCKED = "auth_blocked"  # exit 3
    PAUSED = "paused"  # exit 4
    #: Not an exit code: the loop does not return while it is retrying, so this
    #: is reported from INSIDE the loop, once, when backoff reaches its cap.
    STALLED = "stalled"
    #: exit 0 with ops still queued: a newer producer asked for a worker that
    #: knows its op kinds (plan 1.11); its next kick spawns one.
    REPLACED = "replaced"


#: The one backoff shape for every durable retry in this SDK, so a drain, an
#: agent turn and a backfill unit wait the same way. Kept as module names
#: because this file reads them in several places and a tuple index reads worse.
_BACKOFF_START_SECONDS, _BACKOFF_CAP_SECONDS = durable.RETRY_BACKOFF

#: How long an auth block suppresses new workers before ONE re-probe is allowed.
#:
#: The hard stop above is right about the zombie-uploader pitfall and wrong about
#: permanence: `auth_blocked_since` used to suppress every future spawn forever,
#: so a token that expired or rotated mid-run left a training loop queueing for
#: hours with no delivery, no retry and no signal -- recoverable only by someone
#: noticing and running `probe outbox retry`. Credentials come back (a re-login,
#: a rotated service token, a remounted secret), and when they do delivery must
#: resume on its own.
#:
#: One attempt per cooldown is not a zombie uploader: it is two orders of
#: magnitude slower than the backoff loop, and a still-rejected credential just
#: re-stamps the block and goes quiet again.
_AUTH_RETRY_COOLDOWN_SECONDS = 300.0
#: Longer than Client._drainer_kick_interval, so an op whose kick the writer's
#: throttle swallowed is seen by the lingering worker before it exits.
_EXIT_GRACE_SECONDS = 1.5
_LOG_NAME = "drainer.log"
#: How many looks, `_EXIT_GRACE_SECONDS` apart (~30 s in all), a worker takes at
#: uploads still in the waiting room -- or at ops held back behind one -- before
#: it exits and leaves them to the next promoter.
_WAITING_PASSES = 20


def _promote_only(journal) -> None:
    """Promote waiting uploads under the promote lease, then return."""
    from .journal import _try_lock

    try:
        with _try_lock(journal.promote_lease) as held:
            if held:  # else another promoter is at it
                journal.promote_waiting()
    except OSError:
        return


def _auth_block_is_fresh(stamped_at: str | None) -> bool:
    """Whether an auth block is still inside its cooldown.

    An unparseable or absent stamp answers False -- suppression has to be
    something we can positively justify, because the failure mode of getting it
    wrong is silence: a queue that never drains and never says why.
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
    # A stamp from the future (a clock step) reads as fresh, deliberately: it
    # expires on its own once the clock catches up, and re-probing every kick in
    # the meantime is the pitfall this guard exists to prevent.
    return age < _AUTH_RETRY_COOLDOWN_SECONDS


def _lease_path(journal) -> str:
    # The WORKER lease, distinct from the per-pass .drain.lock: a worker holds
    # this for its whole life, so the between-passes gap never looks "free" to
    # maybe_spawn and forks a duplicate.
    return str(journal.dir / ".worker.lock")


# -- queue format versioning (plan 1.11) ------------------------------------
#
# A worker holds its lease for as long as the queue has work, which during an
# outage is hours, and an upgrade of the SDK does not replace it. A newer
# producer sharing the outbox must therefore not queue an op kind the LIVE
# worker cannot deliver: releases before 1.11 dead-letter an unknown kind as
# permanent. So each worker advertises what it can deliver in a caps file
# beside its lease, a producer asks `ready_for(kind)` before queueing a new
# kind, and when the answer is no it leaves a stop file that a 1.11+ worker
# obeys between passes: it exits, and the producer's next kick spawns a worker
# of its own version. From 1.11 on, a worker that meets an unknown kind holds
# it (`journal.OP_KINDS`) instead of dead-lettering it, so a rollback strands
# nothing either.


def _caps_path(journal):
    return journal.dir / ".worker-caps.json"


def _stop_path(journal):
    return journal.dir / ".worker-stop"


def _write_caps(journal) -> None:
    """Advertise what this worker delivers. Best-effort: without the file a
    producer assumes the oldest caps and asks for a restart, which is safe."""
    import json

    from .journal import OP_KINDS

    try:
        import probe

        version = str(getattr(probe, "__version__", "") or "")
    except Exception:  # noqa: BLE001
        version = ""
    try:
        durable.write_text_atomic(
            _caps_path(journal),
            json.dumps(
                {"schema": 1, "version": version, "kinds": sorted(OP_KINDS), "pid": os.getpid()}
            )
            + "\n",
            mode=0o600,
        )
    except OSError:
        pass


def _drop_caps(journal) -> None:
    """Remove the caps file on the way out, if it is still this worker's."""
    import json

    try:
        caps = json.loads(_caps_path(journal).read_text())
        if caps.get("pid") == os.getpid():
            _caps_path(journal).unlink(missing_ok=True)
    except (OSError, ValueError, AttributeError):
        pass


def _pid_alive(pid: object) -> bool:
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        oscompat.probe_pid(pid)
    except ProcessLookupError:
        return False
    except OSError:
        return True  # exists, not ours to signal
    return True


#: What every worker that predates caps files delivers: anything else it
#: dead-letters.
_LEGACY_KINDS = frozenset({"http", "upload", "rejected_http"})


def live_worker_kinds(directory: str | None = None) -> frozenset | None:
    """The op kinds the worker delivering ``directory`` can handle, or None
    when no worker is running (the next kick spawns one of this version)."""
    import json

    from .journal import Journal

    journal = Journal(directory)
    try:
        journal._ensure()
    except OSError:
        return _LEGACY_KINDS
    if _lease_is_free(journal):
        return None
    try:
        caps = json.loads(_caps_path(journal).read_text())
    except (OSError, ValueError):
        return _LEGACY_KINDS  # a worker that predates caps
    if not isinstance(caps, dict) or not _pid_alive(caps.get("pid")):
        return _LEGACY_KINDS  # a stale file; the lease holder is someone else
    kinds = caps.get("kinds")
    return frozenset(k for k in kinds if isinstance(k, str)) if isinstance(kinds, list) else (
        _LEGACY_KINDS
    )


def ready_for(kind: str, directory: str | None = None) -> bool:
    """Whether an op of ``kind`` may be queued in ``directory`` now: the live
    worker (if any) can deliver it. When it cannot, a stop file asks that
    worker to exit after its current pass so the next kick starts one of this
    version; the caller then waits, or uses an older op shape meanwhile."""
    import json

    from .journal import Journal

    kinds = live_worker_kinds(directory)
    if kinds is None or kind in kinds:
        return True
    journal = Journal(directory)
    try:
        wanted = set()
        try:
            wanted = set(json.loads(_stop_path(journal).read_text()).get("kinds") or ())
        except (OSError, ValueError, AttributeError):
            pass
        durable.write_text_atomic(
            _stop_path(journal),
            json.dumps({"kinds": sorted(wanted | {kind})}) + "\n",
            mode=0o600,
        )
    except OSError:
        pass
    return False


def _work_arrived(journal, fresh: dict) -> bool:
    """The exit guard's question: did anything arrive after the pass that found
    the queue empty? status.json's `pending`, a crash-recovery marker -- and the
    multipart queue (plan (g)), which status.json never counts. Missing that last
    one stranded a > 64 MiB upload queued in the worker's final stretch: the
    producer's kick saw the lease held, and the worker exited `drained`."""
    from .journal import _multipart_pending_count

    return bool(
        fresh.get("pending")
        # status.json is bookkeeping: on a full volume the op lands and its
        # count does not (#2090), so a worker trusting the count alone exited
        # with the op still queued -- and every later write of that run was
        # dropped behind it (7-day soak, 0.200.2). The listing stops at the
        # first op, so an idle queue costs one listing of an empty directory.
        or any(_has_queued_op(q) for q in journal.own_namespaces())
        or _multipart_pending_count(journal)
        or any(q.recovery_file.exists() for q in journal.own_namespaces())
    )


def _asked_to_stop(journal) -> bool:
    """A producer left a stop file (see `ready_for`). Exit only if this worker
    lacks a kind it names; either way the request is consumed, so the worker
    that replaces this one does not exit on it too."""
    import json

    from .journal import OP_KINDS

    path = _stop_path(journal)
    try:
        raw = path.read_text()
    except OSError:
        return False
    try:
        kinds = set(json.loads(raw).get("kinds") or ())
    except (ValueError, AttributeError):
        kinds = {"?"}  # unreadable: assume we are the old one
    path.unlink(missing_ok=True)
    return not kinds <= OP_KINDS


def _lease_is_free(journal, path: str | None = None) -> bool:
    """Non-blocking probe of the worker lease (or another lease `path`). True
    when nobody holds it. The journal directory is known to exist."""
    try:
        handle = open(path or _lease_path(journal), "a+")
    except OSError:
        return False
    try:
        oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
        return True
    except BlockingIOError:
        return False
    finally:
        handle.close()


def _env_fingerprints() -> set:
    """The fingerprints this process's environment credential goes by: its
    `PROBE_TOKEN`'s, and its `PROBE_INGEST_TOKEN`'s alone (an ingest-only
    job's queue is named by it, `Client._credential_queue_name`)."""
    from .journal import credential_fingerprint

    token = os.environ.get("PROBE_TOKEN") or None
    ingest = os.environ.get("PROBE_INGEST_TOKEN") or None
    return {fp for fp in (credential_fingerprint(token, None), credential_fingerprint(None, ingest)) if fp}


def env_fingerprints() -> set:
    """The fingerprints of this process's environment credentials."""
    return _env_fingerprints()


def _holds_the_queues_credential(journal) -> bool:
    """Whether ``journal`` is a credential queue (#2035) this process holds
    the credential of: then what another drainer recorded as held there is
    this process's to send, and its kick must not be suppressed."""
    from .journal import CREDENTIAL_NAMESPACE

    return journal.dir.parent.name == CREDENTIAL_NAMESPACE and journal.dir.name in _env_fingerprints()


def _own_credential_queue(journal):
    """This process's environment credential's queue under a root, if it has
    one (`PROBE_TOKEN` / `PROBE_INGEST_TOKEN`). Env only: O(1) on the kick path."""
    from .journal import CREDENTIAL_NAMESPACE

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
    """The credential queues under a root whose credential was adopted
    (`probe outbox adopt`, the rescue): their writes go out with the stored
    login, which any worker can build, so any kick may start theirs. On the
    kick path: one stat of the adoptions record (parsed only when it
    changed), then -- only when there are adoptions -- one listing of the
    credential queues, however many adoptions the machine ever made."""
    from .journal import CREDENTIAL_NAMESPACE, _adoptions_path, _read_records

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


def _has_queued_op(journal) -> bool:
    """Whether ``ops/`` holds an op the drain has never yet attempted, from a
    listing that stops at the first such name.

    Asked only when status.json says nothing is pending. That count is
    bookkeeping written after each op lands, and a volume too full to rewrite
    it (the append still succeeds: the op is queued, #2090) -- or a crash
    between an op and its status write -- leaves it at zero while an op waits.
    Trusting it spawned no worker, so the op stranded and kept its run's lane
    non-empty: under a full disk every later write was then dropped instead of
    sent directly (7-day soak, 0.200.2).

    A name alone is not enough: an op the drain already tried once and set
    aside -- held for another credential, refused (#2041), backing off -- also
    sits in ``ops/`` with status.json's held/refused bookkeeping just as
    exposed to the same full-disk write failure. Treating IT as "work arrived"
    would spawn (`maybe_spawn`) or keep alive (`_work_arrived`) a worker for an
    op the live drain loop then backs off on forever (`LaneBackoff` never
    exits for a permanently refused credential -- review of this fix, red
    team). `attempts` is written to the OP FILE itself on every drain attempt
    (`journal.py` ~5036, before the credential-refusal branch), a write
    unrelated to status.json's, so it survives that corruption and tells the
    two cases apart without a network call: 0 means the drain has never seen
    this op, which is exactly the race this check exists to catch; any higher
    number means the drain already has an opinion about it, current status.json
    or not. On an idle queue this is one listing of an empty directory, and it
    is asked only when the count already reads zero, so reading op files at all
    means the count is wrong."""
    import json

    try:
        with os.scandir(journal.ops_dir) as entries:
            for entry in entries:
                if not entry.name.endswith(".json"):
                    continue
                try:
                    attempts = json.loads((journal.ops_dir / entry.name).read_text()).get("attempts")
                except (OSError, json.JSONDecodeError, AttributeError):
                    return True  # unreadable: assume it is new rather than spin silently
                try:
                    attempts = int(attempts or 0)
                except (TypeError, ValueError):
                    attempts = 0
                if attempts <= 0:
                    return True
    except OSError:
        return False
    return False


def maybe_spawn(directory: str | None = None) -> bool:
    """Fork a detached worker when there is work and nobody owns the lease.

    O(1) by requirement, not aspiration: this runs after every enqueue and on
    every CLI invocation (including `probe log` in training loops), so it
    reads ONLY status.json plus one lock probe -- never the op files
    themselves (perf review: the old pending() call parsed the whole queue)
    -- plus, for adopted credential queues, one stat and (with adoptions) one
    listing (`_adopted_credential_queues`).
    Returns True when a worker was spawned. (When status.json reads zero it
    also lists ``ops/`` up to the first op: `_has_queued_op`.)
    """
    from .journal import CREDENTIAL_NAMESPACE, Journal

    journal = Journal(directory)
    child_spawned = False
    if not journal.receipt_enabled:
        child = Journal.for_receipts(journal.dir)
        if child.dir.exists():
            # An older root worker may hold its own lease. It cannot enumerate
            # this namespace, and its lease must not suppress the capable worker.
            child_spawned = maybe_spawn(str(child.dir))
        # Of the credential queues (#2035), THIS process's own -- a worker
        # spawned here carries this environment, which holds that credential
        # and no other -- and the adopted ones, whose writes go out with the
        # stored login any worker can build. The rest are kicked by their own
        # writers.
        own = _own_credential_queue(journal)
        if own is not None:
            child_spawned = maybe_spawn(str(own)) or child_spawned
        global _ADOPTED_KICKED_AT
        if (
            journal.dir.parent.name != CREDENTIAL_NAMESPACE
            and time.monotonic() - _ADOPTED_KICKED_AT >= _ADOPTED_KICK_SECONDS
        ):
            # At most every 30 s per process, counted on the ROOT's kicks
            # only (a credential queue's kick has no adopted queues under
            # it, and must not spend the interval): while a worker lives the
            # caller's own throttle never arms, and this ran on every write.
            _ADOPTED_KICKED_AT = time.monotonic()
            for adopted in _adopted_credential_queues(journal):
                if adopted != own:
                    child_spawned = maybe_spawn(str(adopted)) or child_spawned
    status = Journal.read_status(directory, include_receipts=False) or {}
    # `waiting` comes from LISTING the waiting room, not from status.json: an
    # older worker rewrites status.json from `ops/` alone and would read zero.
    waiting = int(status.get("waiting") or 0)
    # Plan (g): multipart uploads sit in their own queue, which status.json
    # (rewritten by older releases from `ops/` alone) never counts. Listed.
    from .journal import _multipart_pending_count

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
        # Everything queued is what the last pass had to leave held (another
        # credential's writes, a refused one's): nothing new to deliver, so no
        # worker. Forking one per kick cost ~0.9 CPU-s each (#2041 round 3).
        # A new op raises `pending` past `held` and spawns as usual.
        return child_spawned
    if journal.paused:
        return child_spawned
    if not _lease_is_free(journal):
        # A worker owns delivery -- maybe an OLDER release that never looks in
        # the waiting room. Waiting uploads still need a promoter: the child
        # finds the drain lease taken and only promotes (see `run`).
        if not (waiting and _lease_is_free(journal, str(journal.promote_lease))):
            return child_spawned
    else:
        # A Probe service runs here and starts this worker as its own child
        # (plan Q5): the same module, on this interpreter, in this folder, with
        # this environment but no credential. The lease stays the one-worker
        # guard. STARTED is a spawn (the caller's kick throttle arms on it);
        # RUNNING is a drainer at the lease, as the held branch above. With no
        # service, an older one or a refusal, fork as before.
        handed = _hand_to_service(journal)
        if handed is not None:
            from probe.service.protocol import BackgroundState

            if handed == BackgroundState.STARTED:
                return True
            if handed == BackgroundState.RUNNING:
                return child_spawned
    # PROBE_* env credentials inherit (T4 decision), except a copy of the
    # stored login (`_worker_env`). PROBE_OUTBOX_WORKER marks the worker: its
    # clients print no delivery notices (plan 1.7) and give no Kubernetes
    # notice (1.5) into drainer.log. Then no worker: the next kick, or `probe
    # outbox drain`, delivers.
    child = _spawn_detached(journal, [str(journal.dir)], _worker_env())
    if child is False:
        return child_spawned
    return _spawn_took(child, journal) or child_spawned


def _spawn_detached(journal, args: list, env: dict):
    """`python -m probe.sdk.outbox_worker <args>`, detached, its output to
    ``journal``'s drainer.log; what Popen returned, or False when it could
    not start.
    0o600 explicitly: the log carries drain errors and tracebacks, and the
    journal's everything-0o600 invariant must not depend on the umask.
    O_NOFOLLOW: a `drainer.log` that is a symlink (planted in a shared
    directory) must not send the output somewhere else (review of #2054)."""
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
            # Survives the parent CLI's exit, and its Ctrl-C: a new session on
            # POSIX, a detached new process group on Windows.
            **oscompat.DETACHED,
            close_fds=True,
            env=env,
        )
    except OSError:
        return False
    finally:
        os.close(log_fd)


#: Fingerprints of env tokens a client in THIS process found to be copies of
#: the stored login when it started (`note_copied_login`). After a re-login
#: the copy no longer equals the login, but it is still a copy, and a worker
#: this process starts must not inherit it.
_COPIED_LOGINS: set = set()


def note_copied_login(fingerprint: str | None) -> None:
    """A client in this process runs with an env token that IS the stored
    login (`Client._is_the_stored_login`): its workers never inherit it."""
    if fingerprint:
        _COPIED_LOGINS.add(fingerprint)


def is_copied_login(fingerprint: str | None) -> bool:
    """Whether a client of this process found ``fingerprint`` to be a copy of
    the stored login (`note_copied_login`)."""
    return bool(fingerprint) and fingerprint in _COPIED_LOGINS


def _worker_env() -> dict:
    """The environment a spawned worker runs with: this one, marked as a
    worker, minus a `PROBE_TOKEN` / `PROBE_INGEST_TOKEN` that only copies the
    stored login of this context for the same server -- now, or when a client
    of this process started (`note_copied_login`). The worker reads that login
    itself, which is the same token today, and follows a re-login tomorrow;
    inherited, the copy was matched first on every pass
    (`journal._settings_for_op`) and a dead one held the job's writes for good
    (a customer's Mac, 2026-10-23). Any other env credential inherits: it is
    the only way the worker can hold it."""
    from .journal import credential_fingerprint
    from .transport import _IDEMPOTENCY_ENV

    env = {**os.environ, "PROBE_OUTBOX_WORKER": "1"}
    # A daemon command's PROBE_IDEMPOTENCY_KEY numbers ITS writes; a worker
    # numbering its replays from the same base reuses those keys for other
    # writes, which the server refuses (422) and the drain dead-letters.
    env.pop(_IDEMPOTENCY_ENV, None)
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
        from .journal import was_login

        try:
            from . import config as config_module

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
        from . import config as config_module

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


# -- rescuing writes stranded under a dead credential ------------------------
#
# A job that ran with its own PROBE_TOKEN queues writes only that token may
# send (#2035). Revoke the token and they wait forever: 9,061 on a customer's
# Mac (2026-10-23). `journal.rescue_stranded` hands them to the stored login
# when it is the same team and user; the CLI's every-command check runs it by
# itself (`maybe_rescue`), so nobody has to. Never from `maybe_spawn`, which
# a training loop calls on every write.

#: Killswitch: `PROBE_OUTBOX_RESCUE=off` never rescues by itself (`probe
#: outbox adopt` still does, on request).
RESCUE_ENV = "PROBE_OUTBOX_RESCUE"
#: How often the CLI may look for stranded writes, per outbox root.
RESCUE_EVERY_SECONDS = 600.0
#: After a rescue that found nothing to send, the next look waits this long.
RESCUE_IDLE_SECONDS = 6 * 3600.0
#: Writes queued in a credential's own queue for this long are worth a look.
_RESCUE_WAITING_SECONDS = 600.0


def rescue_enabled() -> bool:
    """Whether stranded writes may be rescued by themselves (`RESCUE_ENV`)."""
    return (os.environ.get(RESCUE_ENV) or "").strip().lower() not in ("0", "off", "false", "no")


def _rescue_stamp(journal):
    return journal.dir / ".rescue-at"


def _multipart_waiting_since(queue_dir, now: float) -> bool:
    """A multipart upload queued in ``queue_dir`` this long ago or more
    (status.json counts `ops/` alone)."""
    try:
        with os.scandir(queue_dir / "multipart" / "ops") as entries:
            return any(
                e.name.endswith(".json") and now - e.stat().st_mtime >= _RESCUE_WAITING_SECONDS
                for e in entries
            )
    except OSError:
        return False


def _waiting_since(status: dict, now: float) -> bool:
    from datetime import datetime

    if not int(status.get("pending") or 0):
        return False
    try:
        oldest = datetime.fromisoformat(str(status.get("oldest_pending") or "")).timestamp()
    except ValueError:
        return False
    return now - oldest >= _RESCUE_WAITING_SECONDS


def _rescue_roots(journal) -> list:
    """The outbox roots one rescue looks at: ``journal`` and every other outbox
    of this user on this machine (`Journal.discover`: `rank-*`, the $TMPDIR
    fallback), so a distributed job's queues are rescued too."""
    from .journal import Journal

    roots = [journal]
    try:
        roots += [Journal(d) for d in Journal.discover() if d != journal.dir]
    except Exception:  # noqa: BLE001 -- the main outbox alone, then
        pass
    return roots


def _writes_held_back(journal, status: dict) -> bool:
    """Whether some queue under the outbox roots holds writes back: a root's
    last pass held or saw refused ones, or a credential queue this process
    does not hold has had writes waiting a while (nothing else may look in
    it, and a sign-in clears what a pass recorded)."""
    from .journal import Journal, _credential_queue_dirs

    if int(status.get("held") or 0) or status.get("refused_fingerprints"):
        return True
    now = time.time()
    mine = _env_fingerprints()
    for root in _rescue_roots(journal):
        if root is not journal:
            other = Journal.read_status(str(root.dir), include_receipts=False) or {}
            if int(other.get("held") or 0) or other.get("refused_fingerprints"):
                return True
        for path in _credential_queue_dirs(root.dir):
            if path.name in mine:
                continue
            child = (
                Journal.read_status(str(path), include_receipts=False, credential_queues=False)
                or {}
            )
            if (
                int(child.get("held") or 0)
                or child.get("refused_fingerprints")
                or _waiting_since(child, now)
                or _multipart_waiting_since(path, now)
            ):
                return True
    return False


def _rescue_due(stamp) -> bool:
    try:
        return time.time() - stamp.stat().st_mtime >= RESCUE_EVERY_SECONDS
    except FileNotFoundError:
        return True
    except OSError:
        return False


def maybe_rescue(journal, status: dict) -> bool:
    """The CLI's every-command check (`cli.main._outbox_notice`): at most once
    per `RESCUE_EVERY_SECONDS` per outbox root (or `RESCUE_IDLE_SECONDS`
    after a rescue that had nothing to send), and only when writes are held
    back or a credential queue holds discards, start `rescue` in a process of
    its own. One stat when not due; the
    interval is claimed under a lock, so concurrent commands start one.
    Never raises; True when one started."""
    if not rescue_enabled() or os.environ.get("PROBE_OUTBOX_WORKER"):
        return False
    stamp = _rescue_stamp(journal)
    if not _rescue_due(stamp):
        return False
    try:
        from .journal import _try_lock, now_iso

        with _try_lock(journal.dir / ".rescue-claim.lock") as claimed:
            if not claimed or not _rescue_due(stamp):
                return False
            durable.write_text_atomic(stamp, now_iso() + "\n", mode=0o600)
        if not _writes_held_back(journal, status) and not _discards_held_in_queues(journal):
            return False
    except Exception:  # noqa: BLE001 -- the every-command path never raises
        return False
    return spawn_rescuer(journal)


def _discards_held_in_queues(journal) -> bool:
    """Whether a credential queue under some outbox root holds discards: they
    are deleted with the queue once it idles, by this release's cleanup and
    every older one's (an older SDK in a job's environment included), so the
    rescuer moves them to the root (`journal.relocate_discards`). Listings."""
    from .journal import discards_to_relocate

    return any(discards_to_relocate(root.dir) for root in _rescue_roots(journal))


def _rescuer_env() -> dict:
    """The rescuer's environment: a worker's, with no environment credential
    at all -- it sends adopted writes with the stored login and nothing else;
    the kicking process's PROBE_TOKEN is not its to use -- and none of the
    kicking command's identity: a daemon command's PROBE_IDEMPOTENCY_KEY
    numbers its own writes, and the rescuer's would reuse those keys for
    other writes (the server refuses a key reused, 422)."""
    from .transport import _IDEMPOTENCY_ENV

    env = _worker_env()
    for var in ("PROBE_TOKEN", "PROBE_INGEST_TOKEN", _IDEMPOTENCY_ENV):
        env.pop(var, None)
    return env


def spawn_rescuer(journal) -> bool:
    """Start `rescue` for the outbox root ``journal`` in a detached process.
    Never raises; True when one was started."""
    try:
        child = _spawn_detached(journal, ["--rescue", str(journal.dir)], _rescuer_env())
    except Exception:  # noqa: BLE001
        return False
    if child is False:
        return False
    try:
        return child.poll() in (None, 0)
    except Exception:  # noqa: BLE001 -- a liveness probe never fails the spawn
        return True


def worker_holder(queue) -> "tuple[object, str] | None":
    """(pid, release) of the live worker holding ``queue``'s lease, from its
    caps file, or None when the lease is free."""
    import json

    if _lease_is_free(queue):
        return None
    try:
        caps = json.loads(_caps_path(queue).read_text())
    except (OSError, ValueError):
        caps = {}
    return caps.get("pid"), str(caps.get("version") or "")


#: How long the rescuer waits for a drain lock another drainer holds.
_RESCUE_LOCK_TIMEOUT_SECONDS = 60.0


def drain_adopted(queues: set, *, lock_timeout: float):
    """One foreground pass over just the queues that hold adopted writes:
    a credential queue whole, the root without the other credential queues
    (never a live job's queue: its lock, its uploads, its status). Needs no
    worker lease, so an older worker holding a queue does not stop it.
    Returns (delivered, dead_lettered, remaining, lock_busy)."""
    from .journal import CREDENTIAL_NAMESPACE, Journal, drain

    delivered = dead = remaining = 0
    busy = False
    for directory in sorted(queues):
        queue = Journal(directory)
        if queue.dir.parent.name == CREDENTIAL_NAMESPACE:
            part = drain(queue, lock_timeout=lock_timeout)
        else:
            part = drain(queue, lock_timeout=lock_timeout, credential_queues=False)
        delivered += part.delivered
        dead += part.dead_lettered
        remaining += part.remaining
        busy = busy or part.lock_busy
    return delivered, dead, remaining, busy


def rescue(directory: str) -> int:
    """Adopt what is stranded under a dead credential of the logged-in account
    (`journal.rescue_stranded`) in this outbox and every other one of this
    user's (`_rescue_roots`), deliver the adopted writes in one foreground
    pass (`drain_adopted`), then let workers take over. First it moves
    every credential queue's discards to its root (`journal.relocate_discards`;
    reports `outbox.discarded` with reason `relocated`). One rescuer at a
    time per user (`journal.rescue_lock_path`); one that finds nothing to
    send, and nothing it put off, puts the next look off by
    `RESCUE_IDLE_SECONDS`. Prints to drainer.log; reports `outbox.rescued`."""
    from .journal import (
        DiscardCounts,
        Journal,
        _stored_login_fingerprint,
        _try_lock,
        now_iso,
        relocate_discards,
        rescue_lock_path,
        rescue_stranded,
    )

    root = Journal(directory)
    lock = rescue_lock_path()
    lock.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with _try_lock(lock) as mine:
        if not mine:
            return 0  # another rescuer is at it
        login = _stored_login_fingerprint(None)
        here: set = {login} if login else set()
        rescued: dict = {}
        queues: set = set()
        endpoints: set = set()
        deferred = 0
        relocated = DiscardCounts()
        for one in _rescue_roots(root):
            # Discards out of the credential queues first, paused or not: a
            # queue's cleanup deletes them, an older release's included.
            try:
                relocated.merge(relocate_discards(one.dir))
            except Exception as exc:  # noqa: BLE001 -- one root never stops the rest
                print(f"moving discards skipped {one.dir}: {type(exc).__name__}", flush=True)
        if relocated.writes:
            from .._shared import telemetry

            print(f"moved {relocated.writes} discarded write(s) to the outbox root ({now_iso()})", flush=True)
            telemetry.emit_outbox_discarded(relocated, reason=telemetry.DiscardReason.RELOCATED)
        if root.paused:
            # Nothing is rescued from a paused outbox; look again much later
            # (its discards are moved: nothing left to start a rescuer for).
            _look_again_later(root)
            return 0
        for one in _rescue_roots(root):
            try:
                if one.paused:
                    continue
                report = rescue_stranded(one, here=here)
            except Exception as exc:  # noqa: BLE001 -- one root never stops the rest
                print(f"rescue skipped {one.dir}: {type(exc).__name__}", flush=True)
                deferred += 1
                continue
            deferred += report.deferred
            rescued.update(report.rescued)
            queues |= report.queues
            if report.base_url:
                endpoints.add(report.base_url)
            for fp, writes in report.rescued.items():
                print(
                    f"rescued credential {fp}: {writes} write(s) go out with the stored login, "
                    f"the same team and user ({now_iso()})",
                    flush=True,
                )
            for fp, why in report.refused.items():
                print(f"credential {fp} is dead and cannot be rescued here: {why}", flush=True)
        delivered = dead = remaining = 0
        busy = False
        if queues:
            delivered, dead, remaining, busy = drain_adopted(
                queues, lock_timeout=_RESCUE_LOCK_TIMEOUT_SECONDS
            )
            print(
                f"rescue pass: delivered {delivered}; {dead} dead-lettered; {remaining} remaining"
                + ("; another drain held a lock" if busy else ""),
                flush=True,
            )
        if rescued:
            from .._shared import telemetry

            telemetry.emit_outbox_rescued(
                base_url=endpoints.pop() if len(endpoints) == 1 else None,
                credentials=len(rescued),
                writes=sum(rescued.values()),
                delivered=delivered,
                dead_lettered=dead,
                remaining=remaining,
            )
        if not rescued and not delivered and not busy and not deferred:
            # Nothing to send and nothing put off: what is held is not this
            # login's (another account's, no account recorded). Look again
            # much later.
            _look_again_later(root)
    for queue in queues:
        try:
            maybe_spawn(str(queue))  # adopted writes queued from now on
        except Exception:  # noqa: BLE001
            pass
    return 0


def _look_again_later(root) -> None:
    """The next rescue look waits `RESCUE_IDLE_SECONDS` (the stamp's mtime is
    when it is due again; one written now if a rescue ran without a claim)."""
    stamp = _rescue_stamp(root)
    later = time.time() + RESCUE_IDLE_SECONDS
    try:
        stamp.touch(mode=0o600, exist_ok=True)
        os.utime(stamp, (later, later))
    except OSError:
        pass


def _hand_to_service(journal) -> str | None:
    """The running Probe service's answer when it took this queue's drain
    (`service_handoff.drain`: "started" or "running"), else None. A
    credential queue (#2035), or a folder inside one, never goes: its worker
    needs the environment credential that named it, which never crosses the
    socket; nor does a worker's own kick. Never raises; bounded
    (`client.HANDOFF_BUDGET_S`)."""
    from .journal import CREDENTIAL_NAMESPACE

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
    """`maybe_spawn` for a process whose own workers were just SIGKILLed: a
    Ray trial's actor at exit, after Ray's core worker killed its direct
    children (`fluent._arm_ray_trial_exit`).

    A SIGKILLed worker holds its lease until the kernel has torn it down,
    which takes a CPU slot and the unmapping of its memory, and `maybe_spawn`
    reads a held lease as a worker delivering the queue. The exit kick ran a
    fraction of a millisecond after the kill, inside that window, so it
    started nothing and the run's close stayed queued (cli 0.201.3 release
    gate). So wait up to ``wait`` seconds for the lease to be let go, then
    kick. A lease still held at the end is a live worker's -- a sibling
    trial's, delivering this same queue -- and `maybe_spawn` leaves delivery
    to it, as always."""
    from .journal import Journal

    journal = Journal(directory)
    if journal.dir.is_dir():
        deadline = time.monotonic() + wait
        while not _lease_is_free(journal) and time.monotonic() < deadline:
            time.sleep(_KILLED_LEASE_POLL_SECONDS)
    return maybe_spawn(directory)


def _pinned_base_url(journal, limit: int = 20) -> str | None:
    """The single base_url every queued op targets, or None if that is not one
    value we can prove.

    Returns None -- which disables the report -- when the queue is empty, when an
    op carries no pin, or when two ops disagree. All three mean "cannot prove
    which backend this is", and the egress contract makes that a no-send rather
    than a guess. Bounded at `limit` ops because this runs at worker start, on
    the same path a training loop kicks.
    """
    try:
        seen: set[str] = set()
        for _path, op in journal.pending()[:limit]:
            pinned = ((op or {}).get("context") or {}).get("base_url")
            if not pinned:
                return None
            seen.add(str(pinned).rstrip("/"))
            if len(seen) > 1:
                return None
        return next(iter(seen)) if seen else None
    except Exception:  # noqa: BLE001 -- an unreadable journal proves nothing
        return None


#: The pause between passes that delivered while some run is backing off.
_LANE_REPASS_SECONDS = 0.5

#: How often a worker whose remaining ops all belong to runs backing off looks
#: for ops from OTHER runs (plan 1.6). A look lists the queue's names and
#: parses only files it has not seen, never the whole queue.
_LANE_LOOK_SECONDS = 2.0


def _queued_names(journal) -> set:
    """Every queued op file name, per namespace. Names only."""
    names: set = set()
    for queue in journal.own_namespaces():
        try:
            names.update((str(queue.dir), n) for n in os.listdir(queue.ops_dir))
        except OSError:
            continue
    return names


def _wake_stamp(journal) -> float:
    """When `Journal.clear_auth_block` (a sign-in, `probe outbox
    resume`) last asked this queue's worker to look again, or 0."""
    try:
        return (journal.dir / ".wake").stat().st_mtime
    except OSError:
        return 0.0


def _sleep_until_new_work(journal, seen: set, lanes, seconds: float) -> None:
    """Sleep up to ``seconds``, waking early when an op of a run NOT backing
    off is queued (one not in ``seen``, the names before the last pass), or
    when a sign-in asks (`_wake_stamp`: held writes may go now)."""
    import json

    from .journal import _lane_of

    deadline = time.monotonic() + seconds
    woken_at = _wake_stamp(journal)
    while True:
        left = deadline - time.monotonic()
        if left <= 0:
            return
        time.sleep(min(left, _LANE_LOOK_SECONDS))
        if journal.paused or _stop_path(journal).exists():
            return
        if _wake_stamp(journal) != woken_at:
            return
        skip = lanes.skip()
        for queue in journal.own_namespaces():
            try:
                names = os.listdir(queue.ops_dir)
            except OSError:
                continue
            for name in names:
                key = (str(queue.dir), name)
                if not name.endswith(".json") or key in seen:
                    continue
                seen.add(key)
                try:
                    op = json.loads((queue.ops_dir / name).read_text())
                except (OSError, ValueError):
                    return  # unreadable or gone: a pass will sort it out
                # By LANE, as the backoff is kept: a multipart upload waiting
                # on the server's verifier backs off in its own lane (plan
                # (g)), and a new op of its run must still wake the loop.
                if not isinstance(op, dict) or _lane_of(op) not in skip:
                    return


def run(directory: str | None = None) -> int:
    """The worker loop. Exit codes: 0 empty (or asked to stop by a newer
    producer, plan 1.11), 3 auth-blocked, 4 paused."""
    from .journal import Journal

    journal = Journal(directory)
    journal._ensure()
    own = _own_credential_queue(journal)
    if own is not None:
        # The root's worker leaves credential queues to their own workers; this
        # environment's is one it can serve, beside the root (#2041 round 3).
        try:
            maybe_spawn(str(own))
        except Exception:  # noqa: BLE001 -- best-effort, like every kick
            pass
    lease = open(_lease_path(journal), "a+")
    try:
        oscompat.flock(lease.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
    except BlockingIOError:
        lease.close()
        # Another worker owns delivery. Promote whatever is waiting for its
        # credential scan -- the owner may be an older release that cannot --
        # and leave delivery to it: its next pass reads the new ops.
        _promote_only(journal)
        return 0
    _write_caps(journal)
    try:
        return _run_leased(journal)
    finally:
        _drop_caps(journal)


def _run_leased(journal) -> int:
    """`run`, while holding the lease (its handle stays open in `run`)."""
    from . import journal as journal_module
    from . import redaction
    from .journal import Journal, LaneBackoff, drain

    # The scrub cache, as in the training process that spawned this worker.
    # The drain re-scrubs every op it sends, and a fresh worker with the cache
    # off scanned each point's constant keys and values ("key", "kind",
    # "loss", ...) again for every point: 180k scans, 7.1 s of CPU for 2,002
    # coalesced one-step writes, which `finish()` waited out behind the drain
    # lock (0.9 s with it). The cache stays off in multi-tenant processes
    # (redaction.py); this one drains one OS user's own outbox.
    redaction.enable_scrub_cache()

    # The backend this journal's ops actually target, resolved ONCE before the
    # first drain pass while the ops still exist. The worker delivers each op to
    # the base_url pinned ON THAT OP (journal.drain reads `context.base_url`), so
    # gating the report on the ambient config would let a worker draining to a
    # self-host endpoint report to the vendor. None disables the report entirely
    # -- outbox_context fails closed on an unknown backend.
    _gate_base_url = _pinned_base_url(journal)
    if not journal.receipt_enabled and journal.dir.parent.name != journal_module.CREDENTIAL_NAMESPACE:
        try:  # the root's worker tidies away idle credential queues (#2041 round 3)
            relocated = journal_module.DiscardCounts()
            journal_module.prune_credential_queues(journal.dir, counts=relocated)
            from .._shared import telemetry as _telemetry

            _telemetry.emit_outbox_discarded(relocated, reason=_telemetry.DiscardReason.RELOCATED)
        except Exception:  # noqa: BLE001 -- housekeeping never stops delivery
            pass
    # Every wait comes from the ONE backoff helper (plan 0.6), restarted after
    # any pass that made progress.
    delays = durable.backoff_delays(None)
    # Per-run waits (plan 1.6): a run whose head op keeps failing backs off on
    # its own while every other run on the machine keeps delivering.
    lanes = LaneBackoff(ceiling=_BACKOFF_CAP_SECONDS)
    woken_at = _wake_stamp(journal)
    started = time.monotonic()
    delivered = dead_lettered = passes = waiting_passes = 0
    remaining = 0
    stalled_reported = False

    def _report(outcome: str) -> None:
        """Tell the fleet how this episode ended. Never raises, never blocks
        the exit path: telemetry is a bystander to delivery, not a step in it."""
        try:
            from probe._shared import telemetry

            telemetry.emit_outbox_drained(
                base_url=_gate_base_url,
                outcome=outcome,
                delivered=delivered,
                dead_lettered=dead_lettered,
                remaining=remaining,
                passes=passes,
                duration_s=time.monotonic() - started,
            )
        except Exception:  # noqa: BLE001 -- a broken pipe must not strand the queue
            pass

    while True:
        if _asked_to_stop(journal):
            # A newer SDK needs a worker that knows an op kind this one does
            # not (plan 1.11). Exit between passes; its next kick spawns one.
            print("stop requested by a newer producer; exiting", flush=True)
            _report(OutboxOutcome.REPLACED)
            return 0
        if journal.paused:
            if passes == 0:
                # Exiting before any drain pass, so the tally is still 0 and a
                # `remaining` breakdown would show every paused queue as EMPTY --
                # inverting the state a human is meant to act on. Read the depth
                # the worker already has on disk instead of reporting a zero we
                # never measured.
                remaining = (Journal.read_status(str(journal.dir), credential_queues=False) or {}).get("pending") or 0
            _report(OutboxOutcome.PAUSED)
            return 4
        # Waits on the per-pass drain lock: a concurrent foreground
        # `probe outbox drain` finishes, then this pass sees what remains.
        before = _queued_names(journal)
        if _wake_stamp(journal) != woken_at:
            # A sign-in since the last pass: runs held for a credential
            # are tried again now, not when their backoff ends (#2041 round 5:
            # 57 s, up to 300 s).
            woken_at = _wake_stamp(journal)
            lanes = LaneBackoff(ceiling=_BACKOFF_CAP_SECONDS)
        report = drain(journal, skip_runs=lanes.skip(), credential_queues=False)
        lanes.record(report)
        passes += 1
        delivered += report.delivered
        dead_lettered += report.dead_lettered
        remaining = report.remaining
        if report.auth_stopped:
            # A refusal of an unstamped op (an older release queued it) stops
            # the queue: nothing tells its credential apart from the rest.
            print(
                f"auth-blocked; {report.remaining} op(s) kept queued ({journal_module.now_iso()})",
                flush=True,
            )
            _report(OutboxOutcome.AUTH_BLOCKED)
            return 3
        if report.remaining == 0:
            # Exit-race guard (red team): an enqueue during this final stretch
            # saw our lease held and skipped its spawn. Re-read status while
            # still holding the lease; anything new means another pass, not an
            # exit that strands the tail op until some future CLI command.
            fresh = Journal.read_status(str(journal.dir), credential_queues=False) or {}
            if _work_arrived(journal, fresh):
                continue
            if fresh.get("waiting") and waiting_passes < _WAITING_PASSES:
                # An upload mid-enqueue (its item is locked while it copies), or
                # one that could not be promoted this pass. Look again shortly;
                # never spin, and never outlive a stuck item -- the next kick,
                # barrier or CLI command promotes it.
                waiting_passes += 1
                time.sleep(_EXIT_GRACE_SECONDS)
                continue
            # Grace pass (prod smoke 2026-08-06): a writer's LAST op can land
            # after that re-read, and if the writer dies a moment later there
            # is no next command to re-kick anything. Linger one beat -- wider
            # than the client's kick throttle -- and look once more.
            time.sleep(_EXIT_GRACE_SECONDS)
            fresh = Journal.read_status(str(journal.dir), credential_queues=False) or {}
            if _work_arrived(journal, fresh):
                continue
            if fresh.get("waiting") and waiting_passes < _WAITING_PASSES:
                # An upload that arrived during the grace sleep, perhaps being
                # scanned by a promote-only child that will not deliver it.
                waiting_passes += 1
                continue
            _report(OutboxOutcome.DRAINED)
            return 0
        if (
            (report.credential_held or report.credential_refused or report.close_held)
            and not (
                report.delivered
                or report.dead_lettered
                or report.held_back
                or report.stopped_transient
            )
            and lanes.next_wake() is None
        ):
            # Held ops of a RUN stall its lane, and the branch below backs that
            # run off while this worker stays up for the rest (no fork per
            # kick). What is left here names no run: nothing to back off.
            # Everything left was queued with a credential this worker does not
            # hold (#2035) -- another job's PROBE_TOKEN, say -- or one the API
            # refused (set aside until a new login or the cooldown). Re-draining
            # cannot change that, so leave; the process that holds it delivers them.
            print(
                f"{report.credential_held} op(s) wait for the credential that queued them "
                f"({journal_module.now_iso()})",
                flush=True,
            )
            _report(OutboxOutcome.STALLED)  # ops still queued; the next kick resumes
            return 0
        if report.held_back and not (report.delivered or report.dead_lettered):
            # Everything left waits on an upload another process is scanning.
            # Look again shortly rather than re-draining in a tight loop, and
            # never outlive a stuck item. A pass that also skipped runs backing
            # off does not count: exiting would throw their backoff away
            # (review of #2051).
            if not lanes.skip():
                waiting_passes += 1
            if waiting_passes >= _WAITING_PASSES:
                _report(OutboxOutcome.STALLED)  # ops still queued; the next kick resumes
                return 0
            time.sleep(_EXIT_GRACE_SECONDS)
            continue
        if report.delivered or report.dead_lettered or report.in_progress:
            # Progress -- a slice of a multipart upload's parts included (plan
            # (g)): after one, the worker must not sleep to some other lane's
            # backoff, or a 64-part upload crawls. Straight into the next pass. Runs that stalled wait out
            # their own backoff through `skip_runs`; the rest keep flowing --
            # paced while some run is backing off, so a trickle of new writes
            # cannot turn the loop into a pass per write (review of #2051).
            delays = durable.backoff_delays(None)
            if lanes.skip():
                time.sleep(_LANE_REPASS_SECONDS)
            continue
        wake = lanes.next_wake()
        if wake is not None and not report.unreachable:
            # Nothing moved, and what is left belongs to runs backing off:
            # sleep until the soonest of them may be tried again.
            backoff = min(wake, _BACKOFF_CAP_SECONDS)
            why = report.errors[-1] if report.errors else next(
                (stall.error for stall in report.stalled_runs.values()), "?"
            )
            print(
                f"{len(lanes.skip())} run(s) backing off, {report.remaining} left; "
                f"next try in {backoff:.0f}s: {why}",
                flush=True,
            )
            # ...unless another run queues something meanwhile: that must not
            # wait out a stalled run's backoff (up to five minutes).
            _sleep_until_new_work(journal, before, lanes, max(backoff, 0.05))
            if lanes.at_ceiling() and not stalled_reported:
                stalled_reported = True
                _report(OutboxOutcome.STALLED)
            continue
        if report.stopped_transient:
            # At least as long as the server asked (`Retry-After` on a 503 or
            # 429), never past the cap.
            backoff = durable.honor_retry_after(
                next(delays), report.retry_after, ceiling=_BACKOFF_CAP_SECONDS
            )
            print(
                f"transient failure, {report.remaining} left; retrying in "
                f"{backoff:.0f}s: {report.errors[-1] if report.errors else '?'}",
                flush=True,
            )
            time.sleep(backoff)
            # A worker retrying at the CAP has been failing for minutes and may
            # never exit, so it would otherwise report nothing at all. Report
            # once per worker, on the way INTO that state -- the alternative
            # (reporting each capped pass) turns one wedged queue into a beacon.
            if backoff >= _BACKOFF_CAP_SECONDS and not stalled_reported:
                stalled_reported = True
                _report(OutboxOutcome.STALLED)
        else:
            # Progress was made (e.g. dead letters moved aside); reset backoff.
            delays = durable.backoff_delays(None)


def _spawn_took(child, journal) -> bool:
    """Whether the child is actually alive, not merely forked.

    `Popen` succeeding says the fork worked, not that a worker is running: a
    frozen or embedded interpreter, a `sys.executable` whose environment cannot
    `import probe`, or an ImportError under PyInstaller all exit immediately and
    still returned True here. The caller then armed its kick throttle on that
    True, so the journal grew while nothing drained and the only evidence was a
    traceback in drainer.log -- the exact failure the queue exists to prevent.

    Deliberately cheap and deliberately optimistic: one non-blocking poll, and a
    single short grace only if the child has already died. A live worker takes
    the lease within milliseconds, but waiting on that would put a sleep on the
    enqueue path, so "not dead yet" counts as spawned.
    """
    try:
        if child.poll() is None:
            return True
        # It exited already. Give the lease a beat to appear anyway -- a fast,
        # successful drain-and-exit is indistinguishable from a failed start at
        # this instant, and calling that a failure would warn on healthy runs.
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


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--rescue":
        sys.exit(rescue(sys.argv[2]))
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else None))
