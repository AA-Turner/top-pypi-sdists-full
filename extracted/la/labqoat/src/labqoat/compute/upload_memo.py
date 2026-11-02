"""Remember archives a service already holds so unchanged publications skip registration round trips."""

from __future__ import annotations

import hashlib
import json
import os
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path

from labqoat._generated.asset_record import AssetRecord
from labqoat.json_document import JsonDocument


@dataclass(frozen=True)
class UploadMemo:
    """Keep a bounded per-service map from archive hash to its accepted asset identity."""

    path: Path
    capacity: int = 64

    @classmethod
    def for_service(cls, base_url: str, environment: str) -> UploadMemo:
        """Separate every endpoint and execution environment under the user's cache directory."""
        base = Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache")))
        scope = hashlib.sha256(f"{base_url}\n{environment}".encode()).hexdigest()[:32]
        return cls(base / "labqoat" / "uploads" / f"{scope}.json")

    def find(self, sha256: str) -> AssetRecord | None:
        """Return a remembered identity; unreadable or malformed state means nothing is known."""
        try:
            entry = self._entries().get(sha256)
            return None if entry is None else AssetRecord.from_dict(JsonDocument.expect_dict(entry))
        except (KeyError, TypeError, ValueError):
            return None

    def remember(self, record: AssetRecord, *aliases: str) -> None:
        """Retain the most recent identities, also under other names for the same bytes; failures never matter."""
        entries = self._entries()
        for key in (record.sha256, *aliases):
            entries.pop(key, None)
            entries[key] = record.to_dict()
        recent = dict(list(entries.items())[-self.capacity :])
        with suppress(OSError):
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(recent), encoding="utf-8")

    def forget(self) -> None:
        """Drop everything after the service reports that a remembered archive is gone."""
        with suppress(OSError):
            self.path.unlink()

    def _entries(self) -> JsonDocument:
        """Read the retained map, treating absent or damaged files as empty."""
        try:
            return JsonDocument.expect_dict(json.loads(self.path.read_text(encoding="utf-8")))
        except (OSError, ValueError, TypeError):
            return JsonDocument()
