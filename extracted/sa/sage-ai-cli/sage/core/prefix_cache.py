"""Prompt prefix caching.

Sage's system prompt is huge (the SAGE_TRAIN_SYSTEM_PROMPT alone is several
thousand tokens, plus project context, plus RAG, plus few-shot). Re-encoding
the same prefix on every call wastes tokens AND time, especially on local
models where prefill latency dominates response latency.

Strategy:
  1. Hash (system_prompt + first_few_user_turns) → prefix_id
  2. For llama-cpp: persist KV cache to disk via Llama.save_state()/load_state()
  3. For Ollama: use the keep_alive option to preserve in-memory state across
     calls; tag it with a prefix_id and reuse when the prefix matches
  4. For cloud providers: pass `cache_control: {"type": "ephemeral"}` for
     Anthropic-style; OpenAI auto-caches >1024 tokens since 2024-Q4

This module is a thin facade — providers opt in by checking the cache before
encoding. Cache lives at ~/.sage/kv_cache/<prefix_hash>.bin.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

__all__ = [
    "PrefixCacheKey",
    "PrefixCache",
    "prefix_id_for",
    "anthropic_cache_control_block",
]


def prefix_id_for(system_prompt: str, model: str, prelude_messages: list[dict] | None = None) -> str:
    """Deterministic id for a prompt prefix. Same inputs → same id."""
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
        # Slash-safe model id
        safe = self.model.replace("/", "_").replace(":", "_")
        return f"{safe}__{self.prefix_id}.bin"


@dataclass
class PrefixCacheEntry:
    key: PrefixCacheKey
    path: Path
    bytes: int
    created_ts: float
    last_used_ts: float


class PrefixCache:
    """On-disk KV-cache store for llama_cpp prefixes.

    The cache is bounded by total bytes (default 4 GiB) — when exceeded,
    least-recently-used entries are evicted. KV caches for big models can
    be hundreds of MB each, so this matters.
    """

    DEFAULT_MAX_BYTES = 4 * 1024 * 1024 * 1024  # 4 GiB

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
        """Return path to cached state file, or None if missing."""
        entry = self._index.get(key.filename())
        if not entry:
            return None
        path = self.root / key.filename()
        if not path.is_file():
            self._index.pop(key.filename(), None)
            self._save_index()
            return None
        # Touch
        entry["last_used_ts"] = time.time()
        self._save_index()
        return path

    def put(self, key: PrefixCacheKey, payload: bytes) -> Path:
        """Persist KV-cache bytes; evicts LRU entries if over budget."""
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
        # LRU: sort by last_used_ts ascending and drop until under budget
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
    """Wrap a text block so the Anthropic API caches it (>=1024 tokens)."""
    return {
        "type": "text",
        "text": text,
        "cache_control": {"type": "ephemeral"},
    }
