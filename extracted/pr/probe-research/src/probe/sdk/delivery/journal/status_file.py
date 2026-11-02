"""StatusFile: status.json -- write the queue's banner counts, read them back with auth blocks and refusals."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from probe.foundation.durable.durable import SYNC_FULL, file_lock, now_iso, write_text_atomic


def auth_blocked_since(status: dict | None, fingerprints=None) -> str | None:
    """When delivery was last refused a credential (401/403), from a status.json dict, or None.
    Either the queue-wide block (`auth_blocked_since`: writes of a release stamping no
    credential) or, since #2041, a credential the drain set aside (`refused_fingerprints`,
    fingerprint -> when), which is how every write a current release queues is refused, so the
    queue-wide field alone no longer shows a revoked token. ``fingerprints`` limits the second
    to those credentials (a client's own). Both stamps are rewritten at each refusal (the
    credential cooldown counts from the latest): this is the LATEST refusal, not the first."""
    if not isinstance(status, dict):
        return None
    blocked = status.get("auth_blocked_since") or None
    refused = status.get("refused_fingerprints")
    if not blocked and isinstance(refused, dict) and refused:
        # An adopted credential's writes go out with the login now: its old token's refusal
        # blocks nothing (`probe outbox adopt`, the rescue).
        adopted = _read_records(_adoptions_path())
        stamps = sorted(
            str(at)
            for fp, at in refused.items()
            if at and (fingerprints is None or fp in fingerprints) and fp not in adopted
        )
        blocked = stamps[0] if stamps else None
    return blocked


def _status_count(value: Any) -> int:
    """A status.json count, 0 for one that is not a number."""
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError, OverflowError):
        return 0


def _forget_idle_refusals(status: dict, queue: Path) -> None:
    """A refusal stops writes; once a queue holds none it stops nothing. Its record outlives
    them when they go any other way than delivery (a discard, an older release's cleanup) and
    then said "auth-blocked" on every command and reported a stuck queue every six hours for an
    empty queue. So a queue with no write pending (count 0 and neither `ops/` nor
    `multipart/ops/` holds one) reads with no refusal and nothing held. The file keeps what the
    drain wrote: a credential that queues again is refused at most once more."""
    if _status_count(status.get("pending")) > 0:
        return
    if not (status.get("refused_fingerprints") or status.get("auth_blocked_since") or status.get("held")):
        return
    # The count is the last write's; the folders are the truth (a failed status write leaves a
    # stale 0 beside writes still queued).
    for folder in (queue / "ops", queue / "multipart" / "ops"):
        try:
            if any(n.endswith(".json") for n in os.listdir(folder)):
                return
        except FileNotFoundError:
            continue
        except OSError:
            return
    status["refused_fingerprints"] = {}
    status["auth_blocked_since"] = None
    status["held"] = 0
    status["close_held"] = 0


def _blocked_marker(status: dict) -> dict:
    """One queue's own status.json as `blocked_oldest_pending` (its oldest write) and
    `blocked_reason`, when what it holds waits on a credential: `auth_blocked` (an older
    client's queue-wide block), `credential_refused` (writes held with a credential the API
    refused) or `held` (writes held for a credential nothing here has). A close held for its
    run's writes in another queue is not (`close_held`). Judged per queue, so `read_status`'s
    fold never pairs one queue's old backlog with another's fresh hold."""
    pending, oldest = _status_count(status.get("pending")), status.get("oldest_pending")
    held = _status_count(status.get("held")) - _status_count(status.get("close_held"))
    refused = status.get("refused_fingerprints")
    if pending <= 0 or not oldest:
        reason = None
    elif status.get("auth_blocked_since"):
        reason = "auth_blocked"
    elif held > 0:
        reason = "credential_refused" if isinstance(refused, dict) and refused else "held"
    else:
        reason = None
    return {"blocked_oldest_pending": oldest if reason else None, "blocked_reason": reason}


def _older_block(status: dict, child: dict) -> dict:
    """Of two folded queues' blocks (`_blocked_marker`), the one blocked longest."""
    mine, theirs = status.get("blocked_oldest_pending"), child.get("blocked_oldest_pending")
    if theirs and (not mine or str(theirs) < str(mine)):
        return {"blocked_oldest_pending": theirs, "blocked_reason": child.get("blocked_reason")}
    return {"blocked_oldest_pending": mine or None, "blocked_reason": status.get("blocked_reason") if mine else None}


class StatusFileMixin:
    """Part of Journal: its methods run with `self` the Journal; fold_parts() copies them into Journal."""

    # -- status -------------------------------------------------------------
    @staticmethod
    def _count_dir(directory: Path) -> tuple[int, str | None]:
        """(count, first filename) without parsing op bodies. Runs on EVERY append, so it must
        stay O(directory listing), not O(total bytes queued) (perf review: a training loop
        enqueuing offline was O(N^2))."""
        if not directory.exists():
            return 0, None
        names = sorted(n for n in os.listdir(directory) if n.endswith(".json"))
        return len(names), names[0] if names else None

    def _write_status_locked(
        self,
        *,
        unstaged_low_disk: int = 0,
        recount: bool = True,
        pending_delta: int = 0,
        pending_bytes_delta: int = 0,
        enqueued_at: str | None = None,
        set_pending: int | None = None,
        known: dict | None = None,
        sync: str = SYNC_FULL,
        new_dead_letters: list | None = None,
        torn_delta: int = 0,
        **extra: Any,
    ) -> int:
        """Rewrite status.json; returns the pending count written. An append carries its own delta
        (``recount=False``, ``set_pending``); a drain recounts, parsing only ops ``known`` misses (plan
        1.9). Banner-grade: briefly off after a hard kill is accepted."""
        previous: dict = {}
        try:
            previous = json.loads(self.status_file.read_text())
        except (OSError, json.JSONDecodeError):
            pass
        if recount:
            names = (
                sorted(n for n in os.listdir(self.ops_dir) if n.endswith(".json"))
                if self.ops_dir.exists()
                else []
            )
            pending_count = len(names)
            failed_count, _ = self._count_dir(self.failed_dir)
            pending_bytes = 0
            oldest = None
            for index, name in enumerate(names):
                meta = (known or {}).get(name)
                if meta is None:
                    try:
                        meta = _meta_of(json.loads((self.ops_dir / name).read_text()))
                    except (OSError, json.JSONDecodeError, ValueError, AttributeError):
                        meta = (0, None)
                pending_bytes += meta[0]
                if index == 0:
                    oldest = meta[1]
        else:
            pending_count = (
                max(0, set_pending)
                if set_pending is not None
                else max(0, int(previous.get("pending") or 0) + pending_delta)
            )
            failed_count = int(previous.get("failed") or 0)
            pending_bytes = max(0, int(previous.get("pending_bytes") or 0) + pending_bytes_delta)
            oldest = previous.get("oldest_pending")
            if pending_count == 0:
                oldest = None
            elif not oldest and pending_delta > 0:
                # First op onto an empty queue: this append IS the oldest.
                oldest = enqueued_at
        status = {
            "schema": SCHEMA,
            "updated_at": now_iso(),
            "pending": pending_count,
            "pending_bytes": pending_bytes,
            "failed": failed_count,
            "oldest_pending": oldest,
            "paused": self.paused,
            "auth_blocked_since": previous.get("auth_blocked_since"),
            # Per-credential refusals (#2041 review): fingerprint -> when the API last refused it.
            # Carried like the block above.
            "refused_fingerprints": previous.get("refused_fingerprints") or {},
            # Ops the last drain pass had to leave held (another credential, a refused one, a close
            # waiting on another queue) and when: a kick adding nothing deliverable need not fork a
            # worker (#2041 round 3). Carried like the fields around it.
            "held": int(previous.get("held") or 0),
            # Of those, closes waiting on their run's writes in another queue
            # (at most CLOSE_HOLD_MAX_SECONDS): held, but not stuck.
            "close_held": int(previous.get("close_held") or 0),
            "held_at": previous.get("held_at"),
            "last_error": previous.get("last_error"),
            # Monotonic tally of uploads that DEGRADED to unstaged for want of disk headroom,
            # carried forward like the fields above. Counting by scanning ops would make every
            # append O(queue), the regression the O(1) status rewrite fixed.
            "unstaged_low_disk": (
                int(previous.get("unstaged_low_disk") or 0) + int(unstaged_low_disk)
            ),
            # Tally of torn op files moved to failed/ (plan T6), carried like the one above.
            "torn": int(previous.get("torn") or 0) + int(torn_delta),
        }
        status.update(extra)
        # scanning disabled: if recount or extra:
            # An APPEND's status carries only numbers, timestamps this module minted and fields
            # copied from the previous status.json, scrubbed when written: scrubbing again was one
            # of four full scrubs per `log()` (plan 1.3). New text arrives only through `extra` or
            # a drain's recount.
            # scanning disabled: status = default_scrub(status)
        if new_dead_letters:
            self._record_dead_letters(new_dead_letters)
        # Compact: `indent=` takes json's pure-Python encoder and every append rewrites this
        # file (review of #2055).
        write_text_atomic(
            self.status_file, json.dumps(status, separators=(",", ":")) + "\n", mode=0o600,
            sync=sync
        )
        return pending_count

    def write_status(self, **extra: Any) -> None:
        self._ensure()
        with file_lock(self.append_lock):
            self._write_status_locked(**extra)

    @staticmethod
    def read_status(
        directory: str | Path | None = None,
        *,
        include_receipts: bool = True,
        credential_queues: bool = True,
        keep_idle_refusals: bool = False,
        _pause: bool = True,
    ) -> dict | None:
        """Banner-grade counts, including the fenced delivery namespace and (``credential_queues``)
        every credential queue under this root. A queue holding no writes reads with no refusal and
        nothing held (`_forget_idle_refusals`), each judged on its own before any is folded in.
        ``keep_idle_refusals``: the file as written, for the drain, whose cooldowns count from
        those stamps. ``_pause``: read the pause marker (outermost call only; folded queues' copy
        is never used)."""
        root = Path(directory).expanduser() if directory else default_dir()
        path = root / "status.json"
        try:
            status = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError, ValueError):
            status = None
        if isinstance(status, dict):
            if not keep_idle_refusals:
                _forget_idle_refusals(status, root)
            status.update(_blocked_marker(status))
        if include_receipts and root.name != DELIVERY_NAMESPACE:
            child = Journal.read_status(root / DELIVERY_NAMESPACE, include_receipts=False, _pause=False)
            if child:
                status = dict(status or {})
                for field in ("pending", "pending_bytes", "failed", "held"):
                    status[field] = int(status.get(field) or 0) + int(child.get(field) or 0)
                status.update(_older_block(status, child))
                status["delivery_pending"] = int(child.get("pending") or 0)
                status["delivery_failed"] = int(child.get("failed") or 0)
                status["delivery_pending_bytes"] = int(child.get("pending_bytes") or 0)
                status["delivery_paused"] = _pause and _pause_marker(root / DELIVERY_NAMESPACE) is not None
                status["delivery_last_error"] = child.get("last_error")
                status["auth_blocked_since"] = status.get("auth_blocked_since") or child.get(
                    "auth_blocked_since"
                )
        if root.name != DELIVERY_NAMESPACE:
            waiting = Journal.count_waiting(root)
            if waiting or status is not None:
                status = dict(status or {})
                status["waiting"] = waiting
        if (
            include_receipts
            and credential_queues
            and root.name != DELIVERY_NAMESPACE
            and root.parent.name != CREDENTIAL_NAMESPACE
        ):
            # The credential queues (#2035) count toward the root's banner.
            for path in _credential_queue_dirs(root):
                child = Journal.read_status(path, include_receipts=True, _pause=False)
                if not child:
                    continue
                status = dict(status or {})
                # `held`: writes a drain set aside for a credential nothing here can send; a held
                # queue under an empty root is still a backlog.
                for field in ("pending", "pending_bytes", "failed", "waiting", "held"):
                    status[field] = int(status.get(field) or 0) + int(child.get(field) or 0)
                oldest = [v for v in (status.get("oldest_pending"), child.get("oldest_pending")) if v]
                status["oldest_pending"] = min(oldest) if oldest else None
                status.update(_older_block(status, child))
                status["auth_blocked_since"] = status.get("auth_blocked_since") or child.get(
                    "auth_blocked_since"
                )
                child_refused = child.get("refused_fingerprints")
                if isinstance(child_refused, dict) and child_refused:
                    # A refused credential's queue is the one holding its writes: the root's banner
                    # must see it (`auth_blocked_since`).
                    merged = dict(status.get("refused_fingerprints") or {})
                    for fp, at in child_refused.items():
                        merged[fp] = min(str(at), str(merged[fp])) if merged.get(fp) else at
                    status["refused_fingerprints"] = merged
                status["last_error"] = status.get("last_error") or child.get("last_error")
        if status is not None and _pause:
            # From the marker, never status.json: a pause that ran out is over, whatever the last
            # status write saw.
            pause = _pause_in_effect(root)
            status["paused"] = pause is not None
            status["paused_until"] = pause["until"] if pause else None
            if "delivery_paused" in status:
                status["delivery_paused"] = bool(status["delivery_paused"] or pause)
        return status

from probe.sdk.delivery.outbox.drain.accounts import _read_records  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.adoption import _adoptions_path  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import CREDENTIAL_NAMESPACE  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import DELIVERY_NAMESPACE  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.journal import Journal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import SCHEMA  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.paths import _credential_queue_dirs  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _meta_of  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.failures.pause import _pause_in_effect  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.failures.pause import _pause_marker  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.paths import default_dir  # noqa: E402 -- pieces need each other; the front door loads this one first
