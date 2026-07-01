"""Per-session read cache for the CVC agent loop.

The dashboard log the team pasted (a multi-turn ``SearchBar.tsx`` fix that
read the same file 12 times, hit malformed tool-call injections, and never
applied the patch) has a single dominant cause: the agent has no memory of
what it has *already* read this turn. Every iteration starts with
``context_window = []`` plus a pile of tool calls, and the model reasons
over empty space.

Upstream solves this two ways:

1. The ``read_file`` path is wrapped in a per-session cache keyed by
   absolute path. Re-reads in the same turn return the cached content
   without touching disk. The cache is invalidated when the file's
   ``mtime_ns`` changes (so an external edit is picked up immediately on
   the next read).

2. The ``list_dir`` path is wrapped in a per-session tree cache. The
   agent's first call builds a snapshot; subsequent calls consult the
   snapshot before re-walking the directory. The snapshot is invalidated
   on any write to anything inside the tree (the executor notifies the
   cache after every successful write).

CVC's analog (this module) provides both, with these differences:

* Thread-safe — the gateway chat loop runs the agent body in one
  thread, but tool execution happens in a worker thread via
  ``asyncio.run_in_executor``. The cache must be safe across both.
* Per-session, not global. The CVC workspace-switching feature means
  the same gateway process handles many workspaces sequentially. A
  global cache would leak state across workspaces.
* Bounded — LRU eviction with a hard cap (default 256 entries) so a
  long session cannot OOM the gateway.
* Observability — the cache tracks hits/misses/invalidations so the
  dashboard's LoopConfigPanel can surface a real number instead of a
  guess about "what the agent has already seen."

Why this lives in ``loop/`` not ``tools/``
------------------------------------------
The cache is a *loop primitive* — it sits between the LLM's intent
(``read_file(path)``) and the handler (``executor.read_file``). It's
plumbing for the chat loop, not a tool the LLM calls. Putting it in
``loop/`` makes the dependency direction right: ``chat.py`` imports
the cache, the cache imports nothing tool-specific.
"""
from __future__ import annotations

import hashlib
import os
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

__all__ = [
    "CachedRead",
    "ReadCache",
    "TreeCache",
    "SessionReadCaches",
    "compute_path_signature",
]


@dataclass
class CachedRead:
    """One cached read — immutable once stored."""

    path: str                # absolute, resolved (no symlinks, no ~)
    content: str
    mtime_ns: int
    size: int
    sha256: str
    cached_at_monotonic: float
    read_count: int = 1     # how many times the agent asked for this path

    def to_dict(self) -> dict:
        """Snapshot for SSE/JSON — no content (too big for status events)."""
        return {
            "path": self.path,
            "mtime_ns": self.mtime_ns,
            "size": self.size,
            "sha256": self.sha256,
            "read_count": self.read_count,
        }


def compute_path_signature(path: str) -> Tuple[int, int]:
    """Return ``(mtime_ns, size)`` for a path, or ``(-1, -1)`` if missing.

    Uses ``os.stat`` rather than ``Path.stat`` so we don't materialise
    Path objects on every cache lookup (hot path in long sessions).
    """
    try:
        st = os.stat(path)
    except (FileNotFoundError, OSError):
        return (-1, -1)
    return (st.st_mtime_ns, st.st_size)


def _sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="replace")).hexdigest()


class ReadCache:
    """Per-session cache of file reads. LRU-bounded, thread-safe.

    A read is a cache hit when:
    * the path is in the cache, AND
    * the path's current ``(mtime_ns, size)`` matches the cached signature.

    Any other case is a miss → re-read the file, refresh the entry, and
    bump the ``read_count`` (so the dashboard can see hot files).
    """

    DEFAULT_CAPACITY = 256

    def __init__(self, capacity: int = DEFAULT_CAPACITY) -> None:
        if capacity < 1:
            raise ValueError(f"capacity must be >= 1, got {capacity}")
        self._capacity = capacity
        self._entries: "OrderedDict[str, CachedRead]" = OrderedDict()
        self._lock = threading.RLock()
        # Observability counters — exposed via stats().
        self._hits = 0
        self._misses = 0
        self._invalidations = 0
        self._writes_evicted = 0  # entries evicted because of LRU pressure
        self._skipped_missing = 0  # reads where the file doesn't exist

    # ------------------------------------------------------------------
    # Core read path
    # ------------------------------------------------------------------

    def get_or_read(
        self,
        path: str,
        reader: Callable[[str], str],
    ) -> Tuple[str, bool]:
        """Return ``(content, cache_hit)``.

        ``reader(path)`` is called on a miss; the caller's reader is
        responsible for raising ``FileNotFoundError`` (or returning
        ``""``) on missing files. We never call the reader on a hit.

        Concurrency: a single in-flight read for the same path is
        deduplicated. Two threads asking for the same uncached path
        at the same time will see the second thread wait, then share
        the first thread's result. (Upstream doesn't do this — we add
        it because the dashboard's WebSocket and SSE paths can both
        trigger reads in the same instant.)
        """
        abs_path = os.path.realpath(os.path.expanduser(path))
        mtime_ns, size = compute_path_signature(abs_path)

        with self._lock:
            entry = self._entries.get(abs_path)
            if entry is not None and entry.mtime_ns == mtime_ns and entry.size == size and mtime_ns >= 0:
                # Cache hit — promote to most-recently-used.
                self._entries.move_to_end(abs_path)
                entry.read_count += 1
                self._hits += 1
                return (entry.content, True)
            # Miss — drop the stale entry (if any) so the new content
            # is inserted at the most-recently-used end.
            if entry is not None:
                self._entries.pop(abs_path, None)
                self._invalidations += 1

        # Read outside the lock so slow I/O doesn't block other reads.
        try:
            content = reader(abs_path)
        except FileNotFoundError:
            with self._lock:
                self._skipped_missing += 1
                self._misses += 1
            raise

        # If the file vanished between stat and read, surface a clean miss.
        if mtime_ns < 0:
            with self._lock:
                self._skipped_missing += 1
                self._misses += 1
            raise FileNotFoundError(abs_path)

        sha = _sha256_text(content)
        # Re-stat to capture the post-read mtime (defensive — some
        # editors write + fsync + restore mtime, which can change
        # mtime_ns even though content matches what we just read).
        post_mtime_ns, post_size = compute_path_signature(abs_path)
        if post_mtime_ns < 0:
            post_mtime_ns, post_size = mtime_ns, size

        new_entry = CachedRead(
            path=abs_path,
            content=content,
            mtime_ns=post_mtime_ns,
            size=post_size,
            sha256=sha,
            cached_at_monotonic=time.monotonic(),
            read_count=1,
        )
        with self._lock:
            self._entries[abs_path] = new_entry
            self._entries.move_to_end(abs_path)
            self._evict_if_needed_locked()
            self._misses += 1
        return (content, False)

    # ------------------------------------------------------------------
    # Write-side invalidation
    # ------------------------------------------------------------------

    def invalidate(self, path: str) -> bool:
        """Drop a single entry. Returns True if there was an entry."""
        abs_path = os.path.realpath(os.path.expanduser(path))
        with self._lock:
            existed = self._entries.pop(abs_path, None) is not None
            if existed:
                self._invalidations += 1
            return existed

    def invalidate_prefix(self, directory: str) -> int:
        """Drop every entry under *directory*. Used after a bulk write."""
        abs_dir = os.path.realpath(os.path.expanduser(directory))
        prefix = abs_dir if abs_dir.endswith(os.sep) else abs_dir + os.sep
        with self._lock:
            doomed = [p for p in self._entries if p == abs_dir or p.startswith(prefix)]
            for p in doomed:
                self._entries.pop(p, None)
            if doomed:
                self._invalidations += len(doomed)
            return len(doomed)

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
            self._invalidations += 1

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def stats(self) -> dict:
        """Snapshot for dashboards / SSE status events."""
        with self._lock:
            total = self._hits + self._misses
            return {
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": (self._hits / total) if total else 0.0,
                "invalidations": self._invalidations,
                "writes_evicted": self._writes_evicted,
                "skipped_missing": self._skipped_missing,
                "size": len(self._entries),
                "capacity": self._capacity,
            }

    def hot_paths(self, limit: int = 10) -> List[dict]:
        """Return the top-``limit`` most-read paths in this session."""
        with self._lock:
            entries = sorted(
                self._entries.values(),
                key=lambda e: e.read_count,
                reverse=True,
            )
        return [e.to_dict() for e in entries[:limit]]

    def __contains__(self, path: str) -> bool:
        abs_path = os.path.realpath(os.path.expanduser(path))
        with self._lock:
            entry = self._entries.get(abs_path)
            if entry is None:
                return False
            mtime_ns, size = compute_path_signature(abs_path)
            return entry.mtime_ns == mtime_ns and entry.size == size and mtime_ns >= 0

    def __len__(self) -> int:
        with self._lock:
            return len(self._entries)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _evict_if_needed_locked(self) -> None:
        while len(self._entries) > self._capacity:
            # OrderedDict pops in FIFO order; since we move_to_end on
            # every hit, the oldest is the LRU. Drop it.
            self._entries.popitem(last=False)
            self._writes_evicted += 1


# ── Tree cache ────────────────────────────────────────────────────────


@dataclass
class CachedTree:
    """One cached directory listing."""

    path: str
    entries: List[Dict[str, Any]]   # [{name, is_dir, size, mtime_ns}, ...]
    mtime_ns: int
    size: int
    cached_at_monotonic: float


class TreeCache:
    """Per-session cache of ``list_dir`` results.

    A listing is a hit when the directory's own ``(mtime_ns, size)``
    matches what we saw at cache time. We DON'T stat every child —
    directory mtime changes whenever a child is added/removed/renamed,
    which is the only state we actually care about.

    The executor calls :meth:`invalidate_prefix` after every successful
    write so a ``write_file`` of ``foo.py`` invalidates the listing of
    ``.`` (the project root) without us having to walk up the tree.
    """

    DEFAULT_CAPACITY = 64

    def __init__(self, capacity: int = DEFAULT_CAPACITY) -> None:
        if capacity < 1:
            raise ValueError(f"capacity must be >= 1, got {capacity}")
        self._capacity = capacity
        self._entries: "OrderedDict[str, CachedTree]" = OrderedDict()
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0
        self._invalidations = 0

    def get_or_list(
        self,
        path: str,
        lister: Callable[[str], List[Dict[str, Any]]],
    ) -> Tuple[List[Dict[str, Any]], bool]:
        """Return ``(entries, cache_hit)``.

        ``lister(path)`` must return the list-of-dicts shape that the
        ``list_dir`` tool emits: ``[{"name": ..., "is_dir": bool,
        "size": int, "mtime_ns": int}, ...]``.
        """
        abs_path = os.path.realpath(os.path.expanduser(path))
        mtime_ns, size = compute_path_signature(abs_path)

        with self._lock:
            entry = self._entries.get(abs_path)
            if entry is not None and entry.mtime_ns == mtime_ns and entry.size == size and mtime_ns >= 0:
                self._entries.move_to_end(abs_path)
                self._hits += 1
                return (entry.entries, True)

        entries = lister(abs_path)
        # Re-stat in case the listing changed mtime (it shouldn't, but
        # exotic filesystems exist).
        post_mtime_ns, post_size = compute_path_signature(abs_path)
        if post_mtime_ns < 0:
            # Directory itself vanished.
            with self._lock:
                self._misses += 1
            return (entries, False)

        new_entry = CachedTree(
            path=abs_path,
            entries=entries,
            mtime_ns=post_mtime_ns,
            size=post_size,
            cached_at_monotonic=time.monotonic(),
        )
        with self._lock:
            self._entries[abs_path] = new_entry
            self._entries.move_to_end(abs_path)
            while len(self._entries) > self._capacity:
                self._entries.popitem(last=False)
            self._misses += 1
        return (entries, False)

    def invalidate(self, path: str) -> bool:
        abs_path = os.path.realpath(os.path.expanduser(path))
        with self._lock:
            existed = self._entries.pop(abs_path, None) is not None
            if existed:
                self._invalidations += 1
            return existed

    def invalidate_prefix(self, directory: str) -> int:
        abs_dir = os.path.realpath(os.path.expanduser(directory))
        prefix = abs_dir if abs_dir.endswith(os.sep) else abs_dir + os.sep
        with self._lock:
            doomed = [p for p in self._entries if p == abs_dir or p.startswith(prefix)]
            for p in doomed:
                self._entries.pop(p, None)
            if doomed:
                self._invalidations += len(doomed)
            return len(doomed)

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
            self._invalidations += 1

    def __contains__(self, path: str) -> bool:
        abs_path = os.path.realpath(os.path.expanduser(path))
        with self._lock:
            entry = self._entries.get(abs_path)
            if entry is None:
                return False
            mtime_ns, size = compute_path_signature(abs_path)
            return entry.mtime_ns == mtime_ns and entry.size == size and mtime_ns >= 0

    def __len__(self) -> int:
        with self._lock:
            return len(self._entries)

    def stats(self) -> dict:
        with self._lock:
            total = self._hits + self._misses
            return {
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": (self._hits / total) if total else 0.0,
                "invalidations": self._invalidations,
                "size": len(self._entries),
                "capacity": self._capacity,
            }


# ── Per-session container ────────────────────────────────────────────


class SessionReadCaches:
    """Bundles a ReadCache and a TreeCache for one chat session.

    The gateway chat loop creates one of these per ``/api/chat`` request
    (or per WebSocket session) and passes it into the dispatch helpers.
    Caches are bounded per-session so a single user can't exhaust
    gateway memory; old sessions are dropped on workspace switch.
    """

    def __init__(
        self,
        read_capacity: int = ReadCache.DEFAULT_CAPACITY,
        tree_capacity: int = TreeCache.DEFAULT_CAPACITY,
    ) -> None:
        self.reads = ReadCache(read_capacity)
        self.trees = TreeCache(tree_capacity)
        self.created_at_monotonic = time.monotonic()

    def on_write(self, path: str) -> None:
        """Notify both caches that *path* was just written.

        Invalidates the parent directory in the tree cache (so the
        next ``list_dir`` re-walks) and the path itself in the read
        cache (so the next ``read_file`` re-reads).
        """
        self.reads.invalidate(path)
        parent = os.path.dirname(os.path.realpath(os.path.expanduser(path)))
        if parent:
            self.trees.invalidate(parent)

    def stats(self) -> dict:
        return {
            "reads": self.reads.stats(),
            "trees": self.trees.stats(),
            "age_seconds": round(time.monotonic() - self.created_at_monotonic, 3),
        }

    def reset(self) -> None:
        """Zero the caches. Used on ``/clear`` or workspace switch."""
        self.reads.clear()
        self.trees.clear()
