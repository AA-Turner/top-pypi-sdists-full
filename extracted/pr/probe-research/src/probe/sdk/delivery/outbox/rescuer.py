"""Rescuer: now and then, adopt and drain the writes that dead credentials left queued."""

from __future__ import annotations

import os
import time
from ....foundation.durable import durable
from probe.sdk.delivery.outbox.drainers.detached import _env_fingerprints, _spawn_detached, _worker_env, maybe_spawn


# -- rescuing writes stranded under a dead credential ------------------------
#
# A job run with its own PROBE_TOKEN queues writes only that token may send (#2035). Revoke
# the token and they wait forever: 9,061 on a customer's Mac (2026-10-23).
# `journal.rescue_stranded` hands them to the stored login when it is the same team and user;
# the CLI's every-command check runs it (`maybe_rescue`). Never from `maybe_spawn`, which a
# training loop calls on every write.

#: Killswitch: `PROBE_OUTBOX_RESCUE=off` never rescues by itself (`probe outbox adopt` still
#: does, on request).
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
    """A multipart upload queued in ``queue_dir`` this long ago or more (status.json counts
    `ops/` alone)."""
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
    """The outbox roots one rescue looks at: ``journal`` and every other outbox of this user
    on this machine (`Journal.discover`: `rank-*`, the $TMPDIR fallback), so a distributed
    job's queues are rescued too."""
    from ..journal.journal import Journal

    roots = [journal]
    try:
        roots += [Journal(d) for d in Journal.discover() if d != journal.dir]
    except Exception:  # noqa: BLE001 -- the main outbox alone, then
        pass
    return roots


def _writes_held_back(journal, status: dict) -> bool:
    """Whether some queue under the outbox roots holds writes back: a root's last pass held or
    saw refused ones, or a credential queue this process does not hold has had writes waiting
    a while (nothing else may look in it; a sign-in clears what a pass recorded)."""
    from ..journal.journal import Journal
    from ..journal.paths import _credential_queue_dirs

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
    """The CLI's every-command check (`cli.main._outbox_notice`): at most once per
    `RESCUE_EVERY_SECONDS` per outbox root (`RESCUE_IDLE_SECONDS` after a rescue with nothing
    to send), and only when writes are held back or a credential queue holds discards, start
    `rescue` in a process of its own. One stat when not due; the interval is claimed under a
    lock so concurrent commands start one. Never raises; True when one started."""
    if not rescue_enabled() or os.environ.get("PROBE_OUTBOX_WORKER"):
        return False
    stamp = _rescue_stamp(journal)
    if not _rescue_due(stamp):
        return False
    try:
        from ..journal.item_locks import _try_lock
        from ..journal.journal import now_iso

        with _try_lock(journal.dir / ".rescue-claim.lock") as claimed:
            if not claimed or not _rescue_due(stamp):
                return False
            durable.write_text_atomic(stamp, now_iso() + "\n", mode=0o600)
        if not _writes_held_back(journal, status) and not _discards_held_in_queues(journal):
            return False
    except Exception:  # noqa: BLE001 -- the every-command path never raises
        return False
    return spawn_rescuer(journal)


def lift_stale_pause(journal, status: dict, *, base_url: str | None, wait: bool = True) -> bool:
    """Delete the outbox's pause marker when it no longer holds (`Journal.lift_stale_pause`:
    its end passed, or an older CLI's endless one), forget the rescue's paused-time look as
    `probe outbox resume` does, and report `outbox.pause_lifted` with what it held
    (``status``, read before; ``base_url`` None reports nothing). The caller starts the
    drainer: the CLI's every-command check and the Probe service (`server._keep_outbox`).
    Never raises; True when one was lifted."""
    try:
        if not journal.lift_stale_pause(wait=wait):
            return False
        _rescue_stamp(journal).unlink(missing_ok=True)
        from .... import analytics as telemetry

        telemetry.emit_outbox_pause_lifted(status, base_url=base_url)
        return True
    except Exception:  # noqa: BLE001 -- the every-command path never raises
        return False


def _discards_held_in_queues(journal) -> bool:
    """Whether a credential queue under some outbox root holds discards: they are deleted with
    the queue once it idles, by this release's cleanup and every older one's (an older SDK in
    a job's environment included), so the rescuer moves them to the root
    (`journal.relocate_discards`). Listings."""
    from ..journal.failures.discards import discards_to_relocate

    return any(discards_to_relocate(root.dir) for root in _rescue_roots(journal))


def _rescuer_env() -> dict:
    """The rescuer's environment: a worker's, with no environment credential (it sends
    adopted writes with the stored login only; the kicking process's PROBE_TOKEN is not its
    to use) and none of the kicking command's identity: a daemon command's
    PROBE_IDEMPOTENCY_KEY numbers its own writes and the rescuer's would reuse those keys for
    other writes (the server refuses a reused key, 422)."""
    from ..transport.transport import _IDEMPOTENCY_ENV

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


#: How long the rescuer waits for a drain lock another drainer holds.
_RESCUE_LOCK_TIMEOUT_SECONDS = 60.0


def drain_adopted(queues: set, *, lock_timeout: float):
    """One foreground pass over just the queues that hold adopted writes: a credential queue
    whole, the root without the other credential queues (never a live job's queue: its lock,
    uploads, status). Needs no worker lease, so an older worker holding a queue does not stop
    it. Returns (delivered, dead_lettered, remaining, lock_busy)."""
    from ..ops.ops import CREDENTIAL_NAMESPACE
    from ..journal.journal import Journal
    from .drain.drain import drain

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
    (`journal.rescue_stranded`) in this outbox and every other of this user's
    (`_rescue_roots`), deliver the adopted writes in one foreground pass (`drain_adopted`),
    then let workers take over. First it moves every credential queue's discards to its root
    (`journal.relocate_discards`; reports `outbox.discarded`, reason `relocated`). One
    rescuer at a time per user (`journal.rescue_lock_path`); one finding nothing to send, and
    nothing put off, defers the next look by `RESCUE_IDLE_SECONDS`. Prints to drainer.log;
    reports `outbox.rescued`."""
    from ..journal.failures.discards import (
        DiscardCounts,
        relocate_discards)
    from ..journal.journal import (
        Journal,
        now_iso)
    from .drain.credentials import _stored_login_fingerprint
    from ..journal.item_locks import _try_lock
    from .drain.adoption import (
        rescue_lock_path,
        rescue_stranded)

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
            # Discards out of the credential queues first, paused or not: a queue's cleanup
            # deletes them, an older release's included.
            try:
                relocated.merge(relocate_discards(one.dir))
            except Exception as exc:  # noqa: BLE001 -- one root never stops the rest
                print(f"moving discards skipped {one.dir}: {type(exc).__name__}", flush=True)
        if relocated.writes:
            from .... import analytics as telemetry

            print(f"moved {relocated.writes} discarded write(s) to the outbox root ({now_iso()})", flush=True)
            telemetry.emit_outbox_discarded(relocated, reason=telemetry.DiscardReason.RELOCATED)
        if root.paused:
            # Nothing is rescued from a paused outbox; look again much later (its discards
            # are moved: nothing left to start a rescuer for).
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
            from .... import analytics as telemetry

            telemetry.emit_outbox_rescued(
                base_url=endpoints.pop() if len(endpoints) == 1 else None,
                credentials=len(rescued),
                writes=sum(rescued.values()),
                delivered=delivered,
                dead_lettered=dead,
                remaining=remaining,
            )
        if not rescued and not delivered and not busy and not deferred:
            # Nothing to send and nothing put off: what is held is not this login's (another
            # account's, none recorded). Look again much later.
            _look_again_later(root)
    for queue in queues:
        try:
            maybe_spawn(str(queue))  # adopted writes queued from now on
        except Exception:  # noqa: BLE001
            pass
    return 0


def _look_again_later(root) -> None:
    """The next rescue look waits `RESCUE_IDLE_SECONDS` (the stamp's mtime is when it is due
    again; one is written now if a rescue ran without a claim)."""
    stamp = _rescue_stamp(root)
    later = time.time() + RESCUE_IDLE_SECONDS
    try:
        stamp.touch(mode=0o600, exist_ok=True)
        os.utime(stamp, (later, later))
    except OSError:
        pass
