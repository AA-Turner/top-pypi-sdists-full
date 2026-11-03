"""StatusField, WrittenStatus, QueueStatus: status.json's keys, defined once (writer: `journal/status_file.py`).
Older releases write the file too, so any key can be missing: read with `.get(...)`. Kept out of `journal/`,
whose front door loads every piece, so `maybe_spawn`'s module can import it at no cost."""

from __future__ import annotations

from typing import TypedDict

from probe.foundation.compat.compat import StrEnum


class StatusField(StrEnum):
    """A key of status.json (`_write_status_locked`) or of what `Journal.read_status` folds in.
    Equal to its on-disk spelling (`StatusField.PENDING == "pending"`), so the file is unchanged."""

    # Written by `_write_status_locked`.
    SCHEMA = "schema"
    UPDATED_AT = "updated_at"
    PENDING = "pending"
    PENDING_BYTES = "pending_bytes"
    FAILED = "failed"
    OLDEST_PENDING = "oldest_pending"
    PAUSED = "paused"
    AUTH_BLOCKED_SINCE = "auth_blocked_since"
    REFUSED_FINGERPRINTS = "refused_fingerprints"
    HELD = "held"
    CLOSE_HELD = "close_held"
    HELD_AT = "held_at"
    LAST_ERROR = "last_error"
    UNSTAGED_LOW_DISK = "unstaged_low_disk"
    TORN = "torn"
    # Added by `read_status`, never on disk.
    BLOCKED_OLDEST_PENDING = "blocked_oldest_pending"
    BLOCKED_REASON = "blocked_reason"
    WAITING = "waiting"
    PAUSED_UNTIL = "paused_until"
    DELIVERY_PENDING = "delivery_pending"
    DELIVERY_FAILED = "delivery_failed"
    DELIVERY_PENDING_BYTES = "delivery_pending_bytes"
    DELIVERY_PAUSED = "delivery_paused"
    DELIVERY_LAST_ERROR = "delivery_last_error"


class WrittenStatus(TypedDict, total=False):
    """status.json as `_write_status_locked` writes it (an older release's file may lack any key)."""

    schema: str
    updated_at: str
    pending: int
    pending_bytes: int
    #: Dead letters in `failed/`.
    failed: int
    #: The oldest queued write's `enqueued_at`.
    oldest_pending: str | None
    paused: bool
    #: A release stamping no credential: the queue-wide 401/403 stamp.
    auth_blocked_since: str | None
    #: Credential fingerprint -> when the API last refused it (#2041).
    refused_fingerprints: dict[str, str]
    held: int
    #: Of `held`, closes waiting on their run's writes in another queue.
    close_held: int
    held_at: str | None
    last_error: str | None
    unstaged_low_disk: int
    torn: int


class QueueStatus(WrittenStatus, total=False):
    """What `Journal.read_status` returns: the file, folded with its delivery and credential queues."""

    blocked_oldest_pending: str | None
    #: "auth_blocked", "credential_refused" or "held" (`_blocked_marker`).
    blocked_reason: str | None
    #: Uploads in `waiting/`, from a listing.
    waiting: int
    paused_until: str | None
    delivery_pending: int
    delivery_failed: int
    delivery_pending_bytes: int
    delivery_paused: bool
    delivery_last_error: str | None
