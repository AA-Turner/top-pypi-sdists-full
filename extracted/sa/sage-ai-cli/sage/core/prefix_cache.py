"""Prompt prefix caching."""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

__all__ = [
    "PrefixCacheKey",
    "PrefixCache",
    "prefix_id_for",
    "anthropic_cache_control_block",
]


def prefix_id_for(system_prompt: str, model: str, prelude_messages: list[dict] | None = None) -> str:
    h = hashlib.sha256()
    h.update(model.encode("utf-8"))
    h.update(b"\x1e")
    h.update(system_prompt.encode("utf-8"))
    h.update(b"\x1e")
    if prelude_messages:
        h.update(json.dumps(prelude_messages, sort_keys=True).encode("utf-8"))
    return h.hexdigest()[:16]


@dataclass(frozen=True)
class PrefixCacheKey:
    model: str
    prefix_id: str

    def filename(self) -> str:
        safe = self.model.replace("/", "_").replace(":", "_")
        return f"{safe}__{self.prefix_id}.bin"


class PrefixCache:
    DEFAULT_MAX_BYTES = 4 * 1024 * 1024 * 1024

    def __init__(self, root: Path | None = None, max_bytes: int = DEFAULT_MAX_BYTES):
        self.root = root or (Path.home() / ".sage" / "kv_cache")
        self.root.mkdir(parents=True, exist_ok=True)
        self.max_bytes = max_bytes
        self._index_path = self.root / "_index.json"
        self._index: dict[str, dict] = self._load_index()

    def _load_index(self) -> dict:
        if not self._index_path.exists():
            return {}
        try:
            return json.loads(self._index_path.read_text("utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_index(self) -> None:
        try:
            self._index_path.write_text(json.dumps(self._index, indent=2), "utf-8")
        except OSError:
            pass

    def get(self, key: PrefixCacheKey) -> Path | None:
        entry = self._index.get(key.filename())
        if not entry:
            return None
        path = self.root / key.filename()
        if not path.is_file():
            self._index.pop(key.filename(), None)
            self._save_index()
            return None
        entry["last_used_ts"] = time.time()
        self._save_index()
        return path

    def put(self, key: PrefixCacheKey, payload: bytes) -> Path:
        path = self.root / key.filename()
        path.write_bytes(payload)
        self._index[key.filename()] = {
            "model": key.model,
            "prefix_id": key.prefix_id,
            "bytes": len(payload),
            "created_ts": time.time(),
            "last_used_ts": time.time(),
        }
        self._save_index()
        self._evict_if_needed()
        return path

    def _evict_if_needed(self) -> None:
        total = sum(int(e.get("bytes", 0)) for e in self._index.values())
        if total <= self.max_bytes:
            return
        sorted_entries = sorted(
            self._index.items(), key=lambda kv: kv[1].get("last_used_ts", 0),
        )
        for fname, _ in sorted_entries:
            if total <= self.max_bytes:
                break
            entry = self._index.pop(fname, None)
            if entry:
                total -= int(entry.get("bytes", 0))
                try:
                    (self.root / fname).unlink(missing_ok=True)
                except OSError:
                    pass
        self._save_index()

    def stats(self) -> dict:
        total = sum(int(e.get("bytes", 0)) for e in self._index.values())
        return {
            "entries": len(self._index),
            "total_bytes": total,
            "max_bytes": self.max_bytes,
            "root": str(self.root),
        }


def anthropic_cache_control_block(text: str) -> dict[str, Any]:
    return {
        "type": "text",
        "text": text,
        "cache_control": {"type": "ephemeral"},
    }
