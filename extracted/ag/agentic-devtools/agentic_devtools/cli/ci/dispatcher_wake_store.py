"""Best-effort durable dispatcher wakes in the existing provider cooldown variable.

Repository variables have no compare-and-swap. Read/merge/write/read-back retries
reduce lost updates but cannot guarantee exactly-once replay across processes.
Delivered tombstones suppress observed stale pending writes until their TTL ends.
Only the independent repository-variable writer credential is used.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
import uuid
from math import isfinite
from typing import TYPE_CHECKING, Any

from agentic_devtools.cli.ci.cooldown import (
    _WRITE_LOCK,
    COOLDOWN_VARIABLE,
)
from agentic_devtools.cli.ci.cooldown_document import (
    MAX_WAKE_DOCUMENT_BYTES,
    MAX_WAKE_ENTRIES,
    WAKE_TTL_SECONDS,
    _merge_payloads,
    _variable_payload,
)

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.provider import CIPlatformProvider

logger = logging.getLogger(__name__)


class DispatcherWakeStore:
    """Bounded wake records, with snapshot-checked acknowledgement and postponement.

    ``entries`` returns unexpired pending entries, including those not yet due.
    Enqueue success means the pending intent or its delivery tombstone was verified;
    it does not mean a replay was delivered. Call ``acknowledge`` only after success.
    Unknown records are retained but never replayed. Provider read failures propagate;
    malformed values produce no replay entries. Mutations return False on failure.
    """

    MAX_ENTRIES = MAX_WAKE_ENTRIES
    TTL_SECONDS = WAKE_TTL_SECONDS
    MAX_BYTES = MAX_WAKE_DOCUMENT_BYTES
    EXTENSION = "dispatcher_wakes"

    def __init__(self, provider: CIPlatformProvider) -> None:
        self.provider = provider
        self._last_refusal: str | None = None

    @property
    def last_refusal(self) -> str | None:
        """Return the last mutation's refusal reason, or None after success."""
        return self._last_refusal

    @staticmethod
    def _timestamp(value: Any) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("timestamp must be finite and non-negative")
        try:
            timestamp = float(value)
        except OverflowError as exc:
            raise ValueError("timestamp must be finite and non-negative") from exc
        if not isfinite(timestamp) or timestamp < 0:
            raise ValueError("timestamp must be finite and non-negative")
        return timestamp

    @staticmethod
    def _key(pr_number: Any, head_sha: Any, event: Any) -> str:
        if isinstance(pr_number, bool) or not isinstance(pr_number, int) or pr_number <= 0:
            raise ValueError("pr_number must be a positive integer")
        if not isinstance(head_sha, str) or not head_sha.strip() or len(head_sha) > 128:
            raise ValueError("head_sha must be a non-empty string of at most 128 characters")
        if not isinstance(event, str) or not event.strip() or len(event) > 128:
            raise ValueError("event must be a non-empty string of at most 128 characters")
        return hashlib.sha256(json.dumps([pr_number, head_sha, event], separators=(",", ":")).encode()).hexdigest()

    @classmethod
    def _valid(cls, key: str, entry: Any) -> bool:
        if not isinstance(entry, dict) or type(entry.get("version")) is not int or entry["version"] != 1:
            return False
        try:
            if cls._key(entry.get("pr_number"), entry.get("head_sha"), entry.get("event")) != key:
                return False
            created = cls._timestamp(entry.get("created_at"))
            expiry = cls._timestamp(entry.get("expires_at"))
            deadline = cls._timestamp(entry.get("resume_at"))
            return (
                created < expiry <= created + cls.TTL_SECONDS
                and deadline < expiry
                and entry.get("status") in ("pending", "delivered")
                and isinstance(entry.get("identity"), str)
                and bool(entry["identity"])
            )
        except ValueError:
            return False

    @classmethod
    def _prepare(cls, payload: dict[str, Any], now: float) -> dict[str, Any]:
        extension = payload.setdefault(cls.EXTENSION, {"version": 1, "entries": {}})
        if (
            not isinstance(extension, dict)
            or type(extension.get("version")) is not int
            or extension["version"] != 1
            or not isinstance(extension.get("entries"), dict)
        ):
            raise ValueError("Unsupported dispatcher wake schema")
        extension["entries"] = {
            key: entry
            for key, entry in extension["entries"].items()
            if not cls._valid(key, entry) or entry["expires_at"] > now
        }
        return extension["entries"]

    def _read(self) -> dict[str, Any]:
        return _variable_payload(self.provider.get_variable(COOLDOWN_VARIABLE, use_writer_token=True))

    def entries(self, now: float | None = None) -> dict[str, dict[str, Any]]:
        """Return pending entries; propagate unavailable variable reads to fail closed."""
        current = self._timestamp(time.time() if now is None else now)
        raw = self.provider.get_variable(COOLDOWN_VARIABLE, use_writer_token=True)
        try:
            records = self._prepare(_variable_payload(raw), current)
        except Exception as exc:
            logger.warning("Could not decode dispatcher wakes: %s", type(exc).__name__)
            return {}
        return {
            key: dict(entry)
            for key, entry in records.items()
            if self._valid(key, entry) and entry["status"] == "pending"
        }

    def enqueue(self, pr_number: int, head_sha: str, event: str, resume_at: float, now: float | None = None) -> bool:
        """Persist a deduplicated intent without shortening an existing deadline."""
        self._last_refusal = None
        current = self._timestamp(time.time() if now is None else now)
        deadline = self._timestamp(resume_at)
        key = self._key(pr_number, head_sha, event)
        if deadline >= current + self.TTL_SECONDS:
            self._last_refusal = "deadline-beyond-ttl"
            return False
        entry = {
            "version": 1,
            "identity": uuid.uuid4().hex,
            "pr_number": pr_number,
            "head_sha": head_sha,
            "event": event,
            "resume_at": deadline,
            "created_at": current,
            "expires_at": current + self.TTL_SECONDS,
            "status": "pending",
        }
        if not self._valid(key, entry):
            self._last_refusal = "invalid-entry"
            return False
        return self._update(key, entry, None, current)

    def acknowledge(self, key: str, expected_entry: dict, now: float | None = None) -> bool:
        """Retain a delivered tombstone only if the pending snapshot still matches."""
        self._last_refusal = None
        current = self._timestamp(time.time() if now is None else now)
        return self._change(key, expected_entry, None, current)

    def postpone(self, key: str, expected_entry: dict, resume_at: float, now: float | None = None) -> bool:
        """Monotonically postpone a matching pending snapshot, within its original TTL."""
        self._last_refusal = None
        current = self._timestamp(time.time() if now is None else now)
        return self._change(key, expected_entry, self._timestamp(resume_at), current)

    def _change(self, key: str, expected: dict, deadline: float | None, current: float) -> bool:
        if not self._valid(key, expected) or expected["status"] != "pending" or expected["expires_at"] <= current:
            self._last_refusal = "invalid-entry"
            return False
        desired = dict(expected)
        if deadline is None:
            desired["status"] = "delivered"
        elif deadline >= expected["expires_at"]:
            self._last_refusal = "deadline-beyond-expiry"
            return False
        else:
            desired["resume_at"] = max(deadline, expected["resume_at"])
        return self._update(key, desired, expected, current)

    def _update(self, key: str, desired: dict, expected: dict | None, current: float) -> bool:
        known: dict[str, Any] = {}
        with _WRITE_LOCK:
            for attempt in range(3):
                cause = None
                stage = "read"
                try:
                    observed = self._read()
                    observed_records = self._prepare(observed, current)
                    actual = observed_records.get(key)
                    if expected is not None and actual != expected and (attempt == 0 or actual != desired):
                        self._last_refusal = "snapshot-mismatch"
                        return False
                    known = _merge_payloads(known, observed)
                    records = self._prepare(known, current)
                    previous = records.get(key)
                    if expected is None and previous is not None:
                        if not self._valid(key, previous):
                            self._last_refusal = "invalid-existing"
                            return False
                        desired = dict(previous, resume_at=max(previous["resume_at"], desired["resume_at"]))
                        if desired["resume_at"] >= desired["expires_at"]:
                            self._last_refusal = "deadline-beyond-expiry"
                            return False
                    if len(records) > self.MAX_ENTRIES or (previous is None and len(records) >= self.MAX_ENTRIES):
                        self._last_refusal = "entry-capacity"
                        return False
                    records[key] = desired
                    encoded = json.dumps(known, separators=(",", ":"), sort_keys=True)
                    if len(encoded.encode()) > self.MAX_BYTES:
                        self._last_refusal = "byte-capacity"
                        return False
                    stage = "write"
                    self.provider.set_variable(COOLDOWN_VARIABLE, encoded)
                    stage = "verify-read"
                    verified = self._read()
                    verified_records = self._prepare(verified, current)
                    combined = _merge_payloads(known, verified)
                    target: Any = verified_records.get(key)
                    if combined == verified and self._valid(key, target) and (expected is None or target == desired):
                        self._last_refusal = None
                        return True
                    known = combined
                    cause = "verification-failed"
                except Exception as exc:
                    cause = f"{stage}-error:{type(exc).__name__}"
                    logger.warning("Could not persist dispatcher wake; retrying: %s", type(exc).__name__)
        self._last_refusal = cause
        return False
