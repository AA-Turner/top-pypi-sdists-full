"""Loss-resistant documents shared by cooldown and dispatcher wake writers."""

from __future__ import annotations

import json
import time
from math import isfinite
from typing import TYPE_CHECKING, Any

from agentic_devtools.cli.shared.retry import DEFAULT_RATE_LIMIT_MAX_DELAY

if TYPE_CHECKING:
    from agentic_devtools.cli.ci.cooldown import CooldownRecord

MAX_WAKE_ENTRIES = 64
WAKE_TTL_SECONDS = 24 * 60 * 60
MAX_WAKE_DOCUMENT_BYTES = 46000

_WAKE_FIELDS = (
    "version",
    "identity",
    "pr_number",
    "head_sha",
    "event",
    "created_at",
    "expires_at",
    "resume_at",
    "status",
)


def _merge_payloads(
    left: dict[str, Any],
    right: dict[str, Any],
    *,
    _path: tuple[str, ...] = (),
    now: float | None = None,
) -> dict[str, Any]:
    """Union documents; only explicit cooldown path/time merges repair invalid deadlines."""
    merged = dict(left)
    for key, value in right.items():
        previous = merged.get(key)
        if (
            now is not None
            and len(_path) == 2
            and _path[0] == "provider_cooldowns"
            and key == "resume_at"
            and key in left
        ):
            previous_valid, incoming_valid = (
                isinstance(deadline, (int, float))
                and not isinstance(deadline, bool)
                and now < deadline <= now + DEFAULT_RATE_LIMIT_MAX_DELAY
                and isfinite(deadline)
                for deadline in (previous, value)
            )
            if incoming_valid:
                merged[key] = max(previous, value) if previous_valid else value
            continue
        if isinstance(previous, dict) and isinstance(value, dict):
            merged[key] = (
                _merge_wake_entry(previous, value)
                if _path == ("dispatcher_wakes", "entries")
                else _merge_payloads(previous, value, _path=(*_path, key), now=now if _path else None)
            )
        elif key in {"resume_at", "expires_at"} and (
            isinstance(previous, (int, float))
            and not isinstance(previous, bool)
            and isinstance(value, (int, float))
            and not isinstance(value, bool)
        ):
            merged[key] = max(previous, value)
        elif key == "status" and previous == "delivered":
            continue
        else:
            merged[key] = value
    return merged


def _merge_wake_entry(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    """Merge one wake generation, or select a coherent terminal/longest intent."""
    merged = _merge_payloads(left, right)
    if not all(
        type(entry.get("version")) is int
        and entry["version"] == 1
        and isinstance(entry.get("identity"), str)
        and bool(entry["identity"])
        for entry in (left, right)
    ):
        return merged
    if not all(field in left and field in right for field in _WAKE_FIELDS):
        return merged
    if not all(
        type(entry[field]) in (int, float)
        for entry in (left, right)
        for field in ("created_at", "expires_at", "resume_at")
    ):
        return merged
    envelope = ("identity", "pr_number", "head_sha", "event", "created_at", "expires_at")
    if any(left[field] != right[field] for field in envelope):
        winner = max(
            (left, right),
            key=lambda entry: (
                entry["status"] == "delivered",
                entry["resume_at"],
                entry["expires_at"],
                entry["created_at"],
                entry["identity"],
            ),
        )
        merged.update({field: winner[field] for field in _WAKE_FIELDS})
    return merged


def _variable_payload(raw: str | None) -> dict[str, Any]:
    """Decode an existing object without silently destroying invalid stored data."""
    if raw is None:
        return {}
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("Repository variable must contain a JSON object")
    return payload


def _validate_wake_document(payload: dict[str, Any], encoded: str) -> None:
    """Reject oversized known wake documents without evicting any stored intent."""
    extension = payload.get("dispatcher_wakes")
    if (
        not isinstance(extension, dict)
        or type(extension.get("version")) is not int
        or extension["version"] != 1
        or not isinstance(extension.get("entries"), dict)
    ):
        return
    if len(extension["entries"]) > MAX_WAKE_ENTRIES:
        raise ValueError("Dispatcher wake capacity exceeded")
    if len(encoded.encode()) > MAX_WAKE_DOCUMENT_BYTES:
        raise ValueError("Dispatcher wake document size exceeded")


def serialize_cooldowns(records: dict[str, CooldownRecord], *, raw: str | None = None, now: float | None = None) -> str:
    """Serialize cooldowns, repairing matching invalid deadlines and preserving metadata."""
    current = time.time() if now is None else float(now)
    payload = _variable_payload(raw)
    existing = payload.get("provider_cooldowns", {})
    if not isinstance(existing, dict):
        raise ValueError("provider_cooldowns must contain an object")
    payload["provider_cooldowns"] = _merge_payloads(
        existing,
        {key: record.as_dict() for key, record in sorted(records.items())},
        _path=("provider_cooldowns",),
        now=current,
    )
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    _validate_wake_document(payload, encoded)
    return encoded


def _preserves_cooldown_records(
    expected: dict[str, CooldownRecord],
    actual: dict[str, CooldownRecord],
) -> bool:
    """Return whether a verified write retained every expected active record."""
    return all(
        (observed := actual.get(key)) is not None and observed.resume_at >= record.resume_at
        for key, record in expected.items()
    )
