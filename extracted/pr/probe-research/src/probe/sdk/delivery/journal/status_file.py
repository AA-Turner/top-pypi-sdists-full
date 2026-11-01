"""StatusFile: status.json -- write the queue's banner counts, read them back with auth blocks and refusals."""

from __future__ import annotations
import os
from pathlib import Path
from typing import Any


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
from probe.sdk.delivery.outbox.drain.accounts import _read_records  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.adoption import _adoptions_path  # noqa: E402 -- pieces need each other; the front door loads this one first
