"""Best-effort local cache for known AI Watch artifacts.

The cache only avoids fingerprint lookup requests. Submit requests still reach
the backend, which remains authoritative about whether artifact content exists.
Missing, stale, corrupt, or unverifiable state is a cache miss, and every write
is best-effort so cache failures never fail a scan.

The HMAC detects changes by actors without the organization API key. Managed
deployments commonly expose that key to the same local user, so a deliberate
local process can forge cache entries. The submit-time ``has_content`` backstop
is the load-bearing control: a forged hit is evicted and resubmitted with full
content, preserving detection.

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
from collections.abc import Callable
from pathlib import Path
from typing import Any

import structlog

from runlayer_cli.paths import get_runlayer_dir

logger = structlog.get_logger(__name__)

ARTIFACT_CACHE_FILENAME = "artifact-cache.json"
ARTIFACT_CACHE_TTL_SECONDS = 7 * 24 * 60 * 60
ARTIFACT_CACHE_MAX_ENTRIES = 10_000
# Ten thousand SHA-256 identifiers serialize below 1 MiB.
ARTIFACT_CACHE_MAX_FILE_BYTES = 5 * 1024 * 1024

_CACHE_VERSION = 1
_CACHE_LOCK = threading.Lock()
_HMAC_KEY_CONTEXT = b"artifact-cache-v1"


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
        self._entries: dict[str, float] | None = None

    def contains(self, identifier: str) -> bool:
        """Return whether *identifier* has a fresh, authenticated entry."""
        try:
            with _CACHE_LOCK:
                entries = self._loaded_entries()
                recorded_at = entries.get(identifier)
                return (
                    recorded_at is not None
                    and self._now() - recorded_at <= self._ttl_seconds
                )
        except Exception:
            logger.warning(
                "artifact_cache_lookup_failed",
                identifier=identifier,
                exc_info=True,
            )
            return False

    def record(self, identifier: str) -> None:
        """Record one server-confirmed content-bearing identifier."""
        if not identifier:
            return
        try:
            with _CACHE_LOCK:
                entries = self._loaded_entries()
                now = self._now()
                entries = {
                    key: recorded_at
                    for key, recorded_at in entries.items()
                    if now - recorded_at <= self._ttl_seconds
                }
                entries[identifier] = now
                if len(entries) > self._max_entries:
                    newest = sorted(
                        entries.items(),
                        key=lambda item: item[1],
                        reverse=True,
                    )[: self._max_entries]
                    entries = dict(newest)
                self._entries = entries
                self._save_entries(entries)
        except Exception:
            logger.warning(
                "artifact_cache_save_failed",
                operation="record",
                identifier=identifier,
                exc_info=True,
            )

    def evict(self, identifier: str) -> None:
        """Remove one identifier after the backend reports missing content."""
        try:
            with _CACHE_LOCK:
                entries = self._loaded_entries()
                if identifier not in entries:
                    return
                entries = dict(entries)
                entries.pop(identifier, None)
                self._entries = entries
                self._save_entries(entries)
        except Exception:
            logger.warning(
                "artifact_cache_save_failed",
                operation="evict",
                identifier=identifier,
                exc_info=True,
            )

    def _loaded_entries(self) -> dict[str, float]:
        if self._entries is None:
            self._entries = self._load_entries()
        return self._entries

    def _unsigned_payload(self, entries: Any) -> dict[str, Any]:
        return {
            "version": _CACHE_VERSION,
            "host": self._host,
            "entries": entries,
        }

    def _signature(self, unsigned_payload: dict[str, Any]) -> str:
        canonical = json.dumps(
            unsigned_payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return hmac.new(self._hmac_key, canonical, hashlib.sha256).hexdigest()

    def _integrity_miss(self, reason: str) -> dict[str, float]:
        logger.warning("artifact_cache_integrity_mismatch", reason=reason)
        return {}

    def _load_entries(self) -> dict[str, float]:
        try:
            if self._path.stat().st_size > ARTIFACT_CACHE_MAX_FILE_BYTES:
                return self._integrity_miss("file_too_large")
            with self._path.open("rb") as handle:
                encoded = handle.read(ARTIFACT_CACHE_MAX_FILE_BYTES + 1)
            if len(encoded) > ARTIFACT_CACHE_MAX_FILE_BYTES:
                return self._integrity_miss("file_too_large")
            raw = json.loads(encoded.decode("utf-8"))
        except FileNotFoundError:
            return {}
        except ValueError:
            return self._integrity_miss("invalid_json")
        except OSError:
            logger.warning("artifact_cache_load_failed", exc_info=True)
            return {}

        if not isinstance(raw, dict):
            return self._integrity_miss("invalid_payload")
        if raw.get("version") != _CACHE_VERSION:
            return self._integrity_miss("version_mismatch")
        if raw.get("host") != self._host:
            return self._integrity_miss("host_mismatch")
        entries = raw.get("entries")
        signature = raw.get("signature")
        if not isinstance(entries, dict) or not isinstance(signature, str):
            return self._integrity_miss("invalid_payload")

        expected_signature = self._signature(self._unsigned_payload(entries))
        if not hmac.compare_digest(signature, expected_signature):
            return self._integrity_miss("signature_mismatch")

        now = self._now()
        validated: dict[str, float] = {}
        for identifier, recorded_at in entries.items():
            if (
                isinstance(identifier, str)
                and identifier
                and isinstance(recorded_at, int | float)
                and not isinstance(recorded_at, bool)
                and math.isfinite(recorded_at)
                and now - float(recorded_at) <= self._ttl_seconds
            ):
                validated[identifier] = float(recorded_at)
        return validated

    def _save_entries(self, entries: dict[str, float]) -> None:
        unsigned = self._unsigned_payload(entries)
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
