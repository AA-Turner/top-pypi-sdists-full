"""Bounded bookkeeping for the long-lived per-camera face-recognition state.

A face-recognition use case lives as long as its camera stream, so every map it
keys by track id or person id must forget entries that stopped appearing.
:class:`IdleEvictionIndex` remembers when each key was last touched and names the
keys to drop; the owner removes them from its own maps, which can therefore stay
plain dicts.
"""

from __future__ import annotations

import threading
import time
from collections import OrderedDict, deque
from contextvars import ContextVar
from typing import Any, Callable, Deque, Dict, List, Mapping

# Identity state per tracker id. A track is refreshed on every frame it appears in,
# so only tracks that left the scene age out. The cap bounds a crowded scene: each
# track holds up to `history_size` embeddings.
FACE_TRACK_MAX = 512
FACE_TRACK_TTL_S = 300.0

# Recent sightings per recognised person.
PERSON_SIGHTINGS_MAX_PERSONS = 4096
PERSON_SIGHTINGS_PER_PERSON = 16
PERSON_SIGHTINGS_TTL_S = 3600.0

# Sightings recorded by the frame being processed, per person. A context variable, so
# frames processed concurrently on other asyncio tasks or threads never mix.
_FRAME_SIGHTINGS: ContextVar[Dict[str, List[Dict[str, str]]] | None] = ContextVar(
    "face_reg_frame_sightings", default=None
)


class IdleEvictionIndex:
    """Last-touch times per key, with an idle TTL and an LRU cap.

    ``touch`` refreshes a key and returns the keys that must now be dropped: any
    key idle for longer than ``ttl_s`` (monotonic clock), and the least recently
    touched keys beyond ``max_entries``. The key just touched is never returned.
    Each call costs O(1 + number of evicted keys).
    """

    def __init__(
        self,
        max_entries: int,
        ttl_s: float,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.max_entries = max(1, int(max_entries))
        self.ttl_s = float(ttl_s)
        self._clock = clock
        self._last_seen: "OrderedDict[Any, float]" = OrderedDict()
        self._lock = threading.Lock()

    def __len__(self) -> int:
        return len(self._last_seen)

    def __contains__(self, key: Any) -> bool:
        return key in self._last_seen

    def touch(self, key: Any) -> List[Any]:
        now = self._clock()
        evicted: List[Any] = []
        with self._lock:
            self._last_seen[key] = now
            self._last_seen.move_to_end(key)
            while len(self._last_seen) > self.max_entries:
                evicted.append(self._last_seen.popitem(last=False)[0])
            if self.ttl_s > 0:
                cutoff = now - self.ttl_s
                while self._last_seen:
                    oldest, seen = next(iter(self._last_seen.items()))
                    if seen >= cutoff:
                        break
                    self._last_seen.popitem(last=False)
                    evicted.append(oldest)
        return evicted


def idle_index(owner: Any, attr: str, max_entries: int, ttl_s: float) -> IdleEvictionIndex:
    """Return the index stored on ``owner`` under ``attr``, creating it on first use."""
    index = owner.__dict__.get(attr)
    if not isinstance(index, IdleEvictionIndex):
        index = IdleEvictionIndex(max_entries, ttl_s)
        setattr(owner, attr, index)
    return index


def touch_and_prune(index: IdleEvictionIndex, key: Any, *maps: Dict[Any, Any]) -> None:
    """Refresh ``key`` and drop every evicted key from ``maps``."""
    for stale in index.touch(key):
        for state in maps:
            state.pop(stale, None)


def prune_track_state(owner: Any, track_id: Any, *maps: Dict[Any, Any]) -> None:
    """Refresh ``track_id`` in ``owner``'s per-track index and drop idle tracks from ``maps``."""
    index = idle_index(owner, "_track_state_index", FACE_TRACK_MAX, FACE_TRACK_TTL_S)
    touch_and_prune(index, track_id, *maps)


def begin_frame() -> None:
    """Start collecting the current frame's sightings; earlier frames' are no longer reported."""
    _FRAME_SIGHTINGS.set({})


def record_sighting(owner: Any, person_id: str, record: Dict[str, str]) -> None:
    """Append one sighting to ``owner.person_tracking``.

    Keeps at most PERSON_SIGHTINGS_PER_PERSON sightings per person and forgets
    persons not seen for PERSON_SIGHTINGS_TTL_S or beyond PERSON_SIGHTINGS_MAX_PERSONS.
    """
    tracking: Dict[str, Deque[Dict[str, str]]] = owner.person_tracking
    index = idle_index(owner, "_person_index", PERSON_SIGHTINGS_MAX_PERSONS, PERSON_SIGHTINGS_TTL_S)
    touch_and_prune(index, person_id, tracking)
    history = tracking.get(person_id)
    if not isinstance(history, deque):
        history = deque(history or (), maxlen=PERSON_SIGHTINGS_PER_PERSON)
        tracking[person_id] = history
    history.append(record)
    frame = _FRAME_SIGHTINGS.get()
    if frame is not None:
        frame.setdefault(person_id, []).append(record)


def sightings_summary(
    tracking: Mapping[str, Any],
    frame_counts: Mapping[str, int] | None = None,
) -> Dict[str, List[Dict[str, str]]]:
    """``{person_id: [sighting, ...]}`` in the historical shape.

    With ``frame_counts`` (the persons counted in the current frame) only the
    sightings recorded since the last :func:`begin_frame` are returned, for those
    persons, so the per-frame payload is bounded by the frame's detections rather
    than by uptime. A person counted without a sighting this frame is left out.
    """
    if frame_counts is None:
        return {pid: list(history) for pid, history in tracking.items()}
    frame = _FRAME_SIGHTINGS.get() or {}
    return {pid: list(frame[pid]) for pid in frame_counts if frame.get(pid)}
