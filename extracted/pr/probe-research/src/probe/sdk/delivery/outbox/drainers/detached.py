"""`maybe_spawn`: ask the Probe service to drain a queue when work is queued and nobody holds its lease
(plan D8, task 19), with the credentials its writes need (D11). No fork, no local drain: with no
service the journal waits for the next ask. The name stays: callers across the CLI kick through it."""

from __future__ import annotations

import os
import time

from probe.sdk.delivery.outbox.lease import _lease_is_free
from probe.sdk.delivery.outbox.linger import _has_queued_op
from probe.sdk.delivery.status_fields import StatusField

#: How long an auth block suppresses new workers before ONE re-probe: credentials come back
#: (re-login, rotation), and delivery must resume on its own; one try per cooldown is no zombie.
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
        at = datetime.fromisoformat(str(status.get(StatusField.HELD_AT) or ""))
    except ValueError:
        return False
    if at.tzinfo is None:
        at = at.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - at).total_seconds() < _HELD_RESPAWN_SECONDS


def kick_side_queues(journal) -> bool:
    """`maybe_spawn` for the queues beside a root that its own worker may not deliver: the
    receipt namespace, this process's env credential's queue and the adopted ones. True when a
    worker was spawned for one."""
    from ...ops.ops import CREDENTIAL_NAMESPACE
    from ...journal.journal import Journal

    child_spawned = False
    if journal.receipt_enabled:
        return False
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
    return child_spawned


#: While a worker holds the root's lease, how often a write still starts the side queues'
#: workers (`kick_side_queues`, review of #3785, I15): each costs a status read.
SIDE_KICK_SECONDS = 1.0
#: After a side kick spawned a worker, how much longer the next one waits: a cold interpreter's
#: start before it holds the lease (slow imports on a busy box).
SIDE_SPAWN_GRACE_SECONDS = 5.0


def maybe_spawn(directory: str | None = None, *, credential_env: dict | None = None) -> bool:
    """Ask the service to drain the queue when there is work and nobody owns its lease.

    Cheap checks first: status.json plus one lock probe, never the op files, plus for adopted
    credential queues one stat and (with adoptions) one listing (`_adopted_credential_queues`).
    When status.json reads zero it also lists ``ops/`` to the first op (`_has_queued_op`).
    ``credential_env``: a token the caller holds only in code, sent with the request into that
    drain's environment alone (plan D11; R5, #2041). Blocks while the service starts (at most
    `handoff.START_WAIT_S`): a training loop asks from `ServiceDrainer`'s thread, never its own.
    Returns True when the service started a drain for it.
    """
    from ...journal.journal import Journal

    journal = Journal(directory)
    child_spawned = kick_side_queues(journal)
    status = Journal.read_status(directory, include_receipts=False) or {}
    # `waiting` comes from LISTING the waiting room, not status.json: an older worker rewrites
    # status.json from `ops/` alone and would read zero.
    waiting = int(status.get(StatusField.WAITING) or 0)
    # Plan (g): multipart uploads sit in their own queue, which status.json (rewritten by
    # older releases from `ops/` alone) never counts. Listed.
    from ..drain.lanes import _multipart_pending_count

    uploads = _multipart_pending_count(journal)
    from ..held import has_due_held

    if (
        not status.get(StatusField.PENDING)
        and not _has_queued_op(journal)
        and not waiting
        and not uploads
        and not journal.recovery_file.exists()
        # A write set aside after its run stalled is let out hourly by a worker (R9).
        and not has_due_held(journal.dir)
    ) or status.get(StatusField.PAUSED):
        return child_spawned
    if _auth_block_is_fresh(status.get(StatusField.AUTH_BLOCKED_SINCE)) and not waiting:
        # Suppressed, but not forever -- see _AUTH_RETRY_COOLDOWN_SECONDS.
        return child_spawned
    held = int(status.get(StatusField.HELD) or 0)
    if (
        held
        and int(status.get(StatusField.PENDING) or 0) <= held
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
        # A drain owns delivery, maybe an OLDER release's that never looks in the waiting room.
        # Waiting uploads still need a promoter: the service's drain finds the drain lock taken
        # and only promotes (see `run`).
        if not (waiting and _lease_is_free(journal, str(journal.promote_lease))):
            return child_spawned
    from probe.foundation.service_api.vocabularies import BackgroundState

    return request_drain(journal, credential_env) == BackgroundState.STARTED or child_spawned


#: An `outbox.drain` ask's answer, at most (the service answers within its own 2 s).
DRAIN_ASK_S = 5.0


def request_drain(journal, credential_env: dict | None = None) -> str | None:
    """Ask the service to drain `journal`'s folder (`outbox.drain`, plan D8): its answer's state
    (`BackgroundState`), or None when no service took it (none could start, a refusal): the
    journal waits for the next ask. Its environment: this process's settings and credentials
    (`_drain_env`, plus `credential_env`), into that drain's environment only (D11). Never raises."""
    from probe.foundation.service_api import handoff
    from probe.foundation.service_api.wire import Method

    from probe.foundation.service_api.vocabularies import BackgroundRefusal

    folder = os.path.abspath(str(journal.dir))
    parameters = {"dir": folder, "env": {**_drain_env(), **(credential_env or {})}}
    _PROMISED_AT.pop(folder, None)
    try:
        answer = handoff.request(Method.OUTBOX_DRAIN, parameters, timeout=DRAIN_ASK_S)
    except Exception:  # noqa: BLE001 -- no service (or a broken one): the journal waits on disk
        return None
    is_accepted = isinstance(answer, dict) and answer.get("accepted") is True
    if is_accepted or (isinstance(answer, dict) and answer.get("reason") == BackgroundRefusal.BUSY):
        _PROMISED_AT[folder] = time.monotonic()
    if is_accepted:
        note_key_handed(credential_env)
        return answer.get("state")
    return None


#: How long a service's last answer for a folder stands (each ask renews it).
PROMISE_FRESH_S = 10.0
#: Folders a service lately said it drains (accepted: started, or running) or will once a slot frees
#: (BUSY: every one of its `MAX_DRAINS` slots taken): monotonic time of that answer.
_PROMISED_AT: dict[str, float] = {}


def is_drain_promised(directory) -> bool:
    """A service answered `directory`'s last drain ask lately with a drain or a full house: a sender exists,
    however slowly its worker starts on a loaded node, so a wait keeps asking (W23: eight producers on one
    node, a ninth gave its writes up as "no sender" while the service was busy)."""
    at = _PROMISED_AT.get(os.path.abspath(str(directory)))
    return at is not None and time.monotonic() - at < PROMISE_FRESH_S


#: In-code keys a service took (an accepted `outbox.drain` carrying one, or `credentials.hold`):
#: fingerprint -> which start of the service took it (`handoff.get_start_id`). A service that
#: restarted since lost it from memory (M5); a close whose key never got there says so (D21).
_HANDED_KEYS: dict = {}


def note_key_handed(credential_env: dict | None) -> None:
    from probe.foundation.service_api import handoff

    from ..drain.credentials import credential_fingerprint

    if credential_env:
        fingerprint = credential_fingerprint(credential_env.get("PROBE_TOKEN"), credential_env.get("PROBE_INGEST_TOKEN"))
        if fingerprint:
            _HANDED_KEYS[fingerprint] = handoff.get_start_id()


def key_handed(credential_env: dict | None) -> bool:
    """Whether the service as it runs now (its start id) holds the key `credential_env` holds (no
    key: True)."""
    from probe.foundation.service_api import handoff

    from ..drain.credentials import credential_fingerprint

    if not credential_env:
        return True
    fingerprint = credential_fingerprint(credential_env.get("PROBE_TOKEN"), credential_env.get("PROBE_INGEST_TOKEN"))
    return fingerprint is None or (
        fingerprint in _HANDED_KEYS and _HANDED_KEYS[fingerprint] == handoff.get_start_id())


#: `credentials.hold`'s answer, at most (it starts the service where none runs).
HOLD_ASK_S = 10.0


def hold_key(credential_env: dict | None) -> bool:
    """Hand an in-code key to the service (`credentials.hold`, plan D21): held in its memory for
    its queue's drains, also after this process exits. True when it took it. Never raises."""
    from probe.foundation.service_api import handoff
    from probe.foundation.service_api.wire import Method

    from ..drain.credentials import credential_fingerprint

    env = {k: v for k, v in (credential_env or {}).items() if k in ("PROBE_TOKEN", "PROBE_INGEST_TOKEN", "PROBE_BASE_URL")}
    fingerprint = credential_fingerprint(env.get("PROBE_TOKEN"), env.get("PROBE_INGEST_TOKEN"))
    if fingerprint is None:
        return False
    try:
        answer = handoff.request(Method.CREDENTIALS_HOLD, {"fingerprint": fingerprint, "env": env}, timeout=HOLD_ASK_S)
    except Exception:  # noqa: BLE001 -- no service: the next ask carries the key again
        return False
    if isinstance(answer, dict) and answer.get("held") is True:
        _HANDED_KEYS[fingerprint] = handoff.get_start_id()
        return True
    return False


def _drain_env() -> dict:
    """What the service's drain needs of this process's environment (`_worker_env`'s rules for
    credentials): its settings by `runtime_env_name`, without what would change the service's
    own interpreter (PYTHON*, LD_*, DYLD_*, a venv or conda's), and its Probe credentials."""
    from .....foundation.service_api.env import CREDENTIAL_ENV, runtime_env_name

    own = ("PYTHON", "LD_", "DYLD_", "VIRTUAL_ENV", "CONDA_")
    return {
        name: value
        for name, value in _worker_env().items()
        if (name in CREDENTIAL_ENV or (runtime_env_name(name) and not name.startswith(own)))
        and value and "\0" not in value
    }


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
    credential inherits: the only way the worker can hold it. Its events say this
    process's worker surface (`sdk`, or a worker's own when a worker starts one, S4)."""
    from ..... import analytics as telemetry
    from ....agent_session import EVENT_AT_ENV, RUN_PROCESS_ENV
    from ..drain.credentials import credential_fingerprint
    from ...transport.transport import _IDEMPOTENCY_ENV

    env = {**os.environ, "PROBE_OUTBOX_WORKER": "1",
           telemetry.WORKER_SURFACE_ENV: telemetry.get_worker_surface().value}
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


def spawn_past_a_kill(directory: str, *, wait: float) -> bool:
    """`maybe_spawn` for a Ray trial's actor at exit. The drain is the service's child, which Ray's
    kill of the actor's own children never reaches, so there is no lease to wait for (`wait`
    is kept for its callers)."""
    return maybe_spawn(directory)
