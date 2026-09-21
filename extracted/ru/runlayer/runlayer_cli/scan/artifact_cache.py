"""Best-effort local cache for known AI Watch artifacts.

The cache avoids fingerprint lookup requests and throttles heartbeat re-submits
of artifacts this device already delivered unchanged. The backend remains
authoritative about whether artifact content exists. Missing, stale, corrupt,
or unverifiable state is a cache miss, and every write is best-effort so cache
failures never fail a scan; a lost write only costs an extra submit.

The HMAC detects changes by actors without the organization API key. Managed
deployments commonly expose that key to the same local user, so a deliberate
local process can forge cache entries. The submit-time ``has_content`` backstop
is the load-bearing control: a forged hit is evicted and resubmitted with full
content, preserving detection. A forged submission record can only delay one
unchanged heartbeat by at most the re-submit window.

Standard-library + ``structlog`` only, so this remains importable inside the
frozen ``aiwatch`` bundle.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import math
import os
import tempfile
import threading
import time
from collections.abc import Callable, Collection, Mapping
from pathlib import Path
from typing import Any, TypedDict

import structlog

from runlayer_cli.paths import get_runlayer_dir
from runlayer_cli.safe_parse import parse_json

logger = structlog.get_logger(__name__)

ARTIFACT_CACHE_FILENAME = "artifact-cache.json"
ARTIFACT_CACHE_TTL_SECONDS = 7 * 24 * 60 * 60
# Throttled surfaces are reported incomplete, so no server staleness miss
# accrues while a skill waits; a vanished skill is missed only by the complete
# scan at each window expiry, so the server absence backstop is 3 misses x
# window (six hours at two hours, versus 45 minutes unthrottled); explicit
# removal POSTs are unaffected. Must stay well below the TTL above. Fallback
# only: the synced ``skill_resubmit_window_seconds`` (0 = throttle off) wins
# whenever the backend snapshot carries one. Presence-only entries that
# restore the 3-scan bound: PLA-1746.
SKILL_RESUBMIT_WINDOW_SECONDS = 2 * 60 * 60
# Ceiling on the synced window (mirrors the backend clamp and the parse-time
# copy in aiwatch_config_cache): the 3-miss absence backstop never lags more
# than twelve hours however the tenant tunes it.
MAX_SKILL_RESUBMIT_WINDOW_SECONDS = 4 * 60 * 60
ARTIFACT_CACHE_MAX_ENTRIES = 10_000
# Ten thousand SHA-256 identifiers serialize below 1 MiB.
ARTIFACT_CACHE_MAX_FILE_BYTES = 5 * 1024 * 1024

# Version 2 added the ``submissions`` table. The HMAC key context is independent
# of the file version so version 1 files still verify and upgrade in place.
_CACHE_VERSION = 2
_CACHE_LOCK = threading.Lock()
_HMAC_KEY_CONTEXT = b"artifact-cache-v1"


class _CacheState(TypedDict):
    entries: dict[str, float]  # server-confirmed content identifier -> recorded
    submissions: dict[str, float]  # payload key -> last submitted by this device


def _empty_state() -> _CacheState:
    return {"entries": {}, "submissions": {}}


def _is_fresh(recorded_at: float, now: float, max_age_seconds: float) -> bool:
    # A clock that moved backwards reads as stale, for both tables, so it can
    # neither suppress lookups nor suppress submits indefinitely.
    return 0 <= now - recorded_at < max_age_seconds


class ArtifactCache:
    """Best-effort, API-key-bound artifact identifier cache."""

    def __init__(
        self,
        host: str,
        api_key: str,
        *,
        cache_path: Path | None = None,
        now: Callable[[], float] = time.time,
        ttl_seconds: float = ARTIFACT_CACHE_TTL_SECONDS,
        max_entries: int = ARTIFACT_CACHE_MAX_ENTRIES,
        resubmit_window_seconds: float = SKILL_RESUBMIT_WINDOW_SECONDS,
    ) -> None:
        self._host = host
        self._hmac_key = hmac.new(
            api_key.encode("utf-8"),
            _HMAC_KEY_CONTEXT,
            hashlib.sha256,
        ).digest()
        self._path = cache_path or get_runlayer_dir() / ARTIFACT_CACHE_FILENAME
        self._now = now
        self._ttl_seconds = ttl_seconds
        self._max_entries = max_entries
        # A zero window never reads as fresh, so nothing is ever skipped.
        self._resubmit_window_seconds = resubmit_window_seconds
        self._state: _CacheState | None = None

    def contains(self, identifier: str) -> bool:
        """Return whether *identifier* has a fresh, authenticated entry."""
        try:
            with _CACHE_LOCK:
                recorded_at = self._loaded_state()["entries"].get(identifier)
                return recorded_at is not None and _is_fresh(
                    recorded_at, self._now(), self._ttl_seconds
                )
        except Exception:
            logger.warning(
                "artifact_cache_lookup_failed",
                identifier=identifier,
                exc_info=True,
            )
            return False

    def recently_submitted(self, submission_key: str) -> bool:
        """Return whether *submission_key* was submitted inside the window."""
        try:
            with _CACHE_LOCK:
                submitted_at = self._loaded_state()["submissions"].get(submission_key)
                return submitted_at is not None and _is_fresh(
                    submitted_at, self._now(), self._resubmit_window_seconds
                )
        except Exception:
            logger.warning(
                "artifact_cache_lookup_failed",
                submission_key=submission_key,
                exc_info=True,
            )
            return False

    def record(self, identifier: str, submission_key: str | None = None) -> None:
        """Record a server-confirmed identifier and, when given, the payload
        key this device just submitted, in one write."""
        if not identifier:
            return
        try:
            with _CACHE_LOCK:
                state = self._loaded_state()
                now = self._now()
                submissions = state["submissions"]
                if submission_key:
                    submissions = self._with(
                        submissions,
                        submission_key,
                        now,
                        self._resubmit_window_seconds,
                    )
                self._save_state(
                    {
                        "entries": self._with(
                            state["entries"], identifier, now, self._ttl_seconds
                        ),
                        "submissions": submissions,
                    }
                )
        except Exception:
            logger.warning(
                "artifact_cache_save_failed",
                operation="record",
                identifier=identifier,
                submission_key=submission_key,
                exc_info=True,
            )

    def retain_submissions(
        self, submission_keys: Collection[str], *, kind: str
    ) -> None:
        """Forget *kind*'s recorded submissions absent from *submission_keys*.

        Called once per scan with every ``<kind>:`` key the scan planned, so an
        artifact that vanished and came back inside the window, or changed and
        changed back, is due again instead of silently skipped.
        """
        prefix = f"{kind}:"
        try:
            with _CACHE_LOCK:
                state = self._loaded_state()
                kept = {
                    key: submitted_at
                    for key, submitted_at in state["submissions"].items()
                    if key in submission_keys or not key.startswith(prefix)
                }
                if len(kept) != len(state["submissions"]):
                    self._save_state({"entries": state["entries"], "submissions": kept})
        except Exception:
            logger.warning(
                "artifact_cache_save_failed",
                operation="retain_submissions",
                kind=kind,
                exc_info=True,
            )

    def evict(self, identifier: str) -> None:
        """Remove one identifier after the backend reports missing content."""
        try:
            with _CACHE_LOCK:
                state = self._loaded_state()
                if identifier not in state["entries"]:
                    return
                entries = dict(state["entries"])
                entries.pop(identifier, None)
                self._save_state(
                    {"entries": entries, "submissions": state["submissions"]}
                )
        except Exception:
            logger.warning(
                "artifact_cache_save_failed",
                operation="evict",
                identifier=identifier,
                exc_info=True,
            )

    def _with(
        self,
        table: Mapping[str, float],
        key: str,
        now: float,
        max_age_seconds: float,
    ) -> dict[str, float]:
        fresh = {
            existing_key: recorded_at
            for existing_key, recorded_at in table.items()
            if _is_fresh(recorded_at, now, max_age_seconds)
        }
        fresh[key] = now
        if len(fresh) > self._max_entries:
            newest = sorted(
                fresh.items(),
                key=lambda item: item[1],
                reverse=True,
            )[: self._max_entries]
            fresh = dict(newest)
        return fresh

    def _loaded_state(self) -> _CacheState:
        if self._state is None:
            self._state = self._load_state()
        return self._state

    def _unsigned_payload(self, tables: Mapping[str, Any]) -> dict[str, Any]:
        return {"version": _CACHE_VERSION, "host": self._host, **tables}

    def _signature(self, unsigned_payload: dict[str, Any]) -> str:
        canonical = json.dumps(
            unsigned_payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return hmac.new(self._hmac_key, canonical, hashlib.sha256).hexdigest()

    def _integrity_miss(self, reason: str) -> _CacheState:
        logger.warning("artifact_cache_integrity_mismatch", reason=reason)
        return _empty_state()

    def _load_state(self) -> _CacheState:
        try:
            if self._path.stat().st_size > ARTIFACT_CACHE_MAX_FILE_BYTES:
                return self._integrity_miss("file_too_large")
            with self._path.open("rb") as handle:
                encoded = handle.read(ARTIFACT_CACHE_MAX_FILE_BYTES + 1)
            if len(encoded) > ARTIFACT_CACHE_MAX_FILE_BYTES:
                return self._integrity_miss("file_too_large")
            text = encoded.decode("utf-8")
        except FileNotFoundError:
            return _empty_state()
        except ValueError:
            return self._integrity_miss("invalid_json")
        except OSError:
            logger.warning("artifact_cache_load_failed", exc_info=True)
            return _empty_state()

        outcome = parse_json(text)
        if outcome["error"] is not None:
            return self._integrity_miss("invalid_json")
        raw = outcome["value"]
        if not isinstance(raw, dict):
            return self._integrity_miss("invalid_payload")
        version = raw.get("version")
        if version not in (1, _CACHE_VERSION):
            return self._integrity_miss("version_mismatch")
        if raw.get("host") != self._host:
            return self._integrity_miss("host_mismatch")
        entries = raw.get("entries")
        signature = raw.get("signature")
        if version == 1:
            # Version 1 predates ``submissions`` and verifies on its own shape,
            # then upgrades in memory. A miss here would make every device
            # re-upload every skill in full on its next scan.
            submissions: Any = {}
            unsigned = {"version": 1, "host": self._host, "entries": entries}
        else:
            submissions = raw.get("submissions")
            unsigned = self._unsigned_payload(
                {"entries": entries, "submissions": submissions}
            )
        if (
            not isinstance(entries, dict)
            or not isinstance(submissions, dict)
            or not isinstance(signature, str)
        ):
            return self._integrity_miss("invalid_payload")
        if not hmac.compare_digest(signature, self._signature(unsigned)):
            return self._integrity_miss("signature_mismatch")

        now = self._now()
        return {
            "entries": self._validated(entries, now, self._ttl_seconds),
            "submissions": self._validated(
                submissions, now, self._resubmit_window_seconds
            ),
        }

    @staticmethod
    def _validated(
        raw: dict[Any, Any],
        now: float,
        max_age_seconds: float,
    ) -> dict[str, float]:
        validated: dict[str, float] = {}
        for key, recorded_at in raw.items():
            if (
                isinstance(key, str)
                and key
                and isinstance(recorded_at, int | float)
                and not isinstance(recorded_at, bool)
                and math.isfinite(recorded_at)
                and _is_fresh(float(recorded_at), now, max_age_seconds)
            ):
                validated[key] = float(recorded_at)
        return validated

    def _save_state(self, state: _CacheState) -> None:
        self._state = state
        unsigned = self._unsigned_payload(state)
        payload = {**unsigned, "signature": self._signature(unsigned)}

        self._path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(
            dir=str(self._path.parent),
            prefix=self._path.name,
            suffix=".tmp",
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(
                    payload,
                    handle,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(tmp_name, 0o600)
            os.replace(tmp_name, self._path)
            os.chmod(self._path, 0o600)
        except Exception:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
            raise
