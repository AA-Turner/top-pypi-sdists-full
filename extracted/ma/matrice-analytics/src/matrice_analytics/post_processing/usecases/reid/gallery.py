"""In-RAM person embedding gallery holding the most recent N identities.

Pure numpy -- no torch, no cv2, no optional dependency -- so the matching
logic is unit-testable on any machine, with or without a model.

Design notes that are load-bearing:

* **Capacity-bounded, not time-bounded.** The gallery holds the ``capacity``
  most recently seen identities and nothing else. When a new identity needs
  a row and the table is full, the least-recently-seen entry is evicted.
  There is no clock: an identity leaves only because ``capacity`` other
  people were seen more recently than it.

  This is a deliberate change from the earlier time-windowed design, and it
  is the better fit for the problem. A fixed window is wrong in both
  directions at once: on a quiet camera it forgets someone who is still the
  most recent person seen, and on a busy one it retains hundreds of
  identities whose rows are only ever noise in the ratio test. "The last 100
  people" is both the stable memory footprint *and* the honest description
  of what the matcher can actually discriminate between.

* **Preallocated matrix, never grown.** ``vstack``-per-insert is O(n) copying
  and makes memory a function of traffic; a fixed ``(capacity, dim)`` block
  makes RAM constant from construction. At the default capacity this is
  100 x 512 x 4 B = 200 KB per stream, flat from startup to hour ten.
  Freed rows are recycled through a free list.

* **Bias to missing, never to merging.** A missed re-identification
  over-counts by one and is recoverable. A false merge under-counts by one
  *and* poisons the prototype, which cascades into further bad merges. Hence
  the ratio test, the live-elsewhere mask and the minimum-absence gate --
  each of which can only ever *reject* a candidate.

Privacy: entries hold an embedding, an opaque canonical id and timestamps.
No image, no crop, no name, no external key. An identity is displaced by
newer traffic rather than persisting until some clock says otherwise, so a
gallery is at most ``capacity`` anonymous "same person as before" tokens.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set

import numpy as np

__all__ = ["GalleryMatch", "ReIDGallery"]


@dataclass
class GalleryMatch:
    """Outcome of a gallery query."""

    canonical_id: str
    score: float
    runner_up: float = 0.0


def l2_normalize(v: np.ndarray) -> np.ndarray:
    """Return ``v`` scaled to unit L2 norm; a zero vector is returned as-is."""
    v = np.asarray(v, dtype=np.float32).reshape(-1)
    n = float(np.linalg.norm(v))
    if n <= 1e-12:
        return v
    return (v / n).astype(np.float32)


class ReIDGallery:
    """The ``capacity`` most recently seen person embeddings, for one stream.

    Not internally locked: a single instance belongs to one use-case instance
    (one stream), and every mutation happens on the frame path. The worker
    thread never touches this object -- it returns embeddings, and the frame
    path does the matching. That keeps the concurrency story trivial.
    """

    def __init__(
        self,
        dim: int,
        capacity: int = 100,
        match_threshold: float = 0.67,
        margin: float = 0.06,
        min_absence_s: float = 3.0,
    ) -> None:
        if dim <= 0:
            raise ValueError(f"dim must be positive, got {dim}")
        if capacity <= 0:
            raise ValueError(f"capacity must be positive, got {capacity}")
        self.dim = int(dim)
        self.capacity = int(capacity)
        self.match_threshold = float(match_threshold)
        self.margin = float(margin)
        self.min_absence_s = float(min_absence_s)

        # One preallocated slab. Row i holds the embedding for ``ids[i]``,
        # last seen at ``last_seen[i]``. Rows are reused via ``_free_rows``
        # and reclaimed least-recently-seen-first when the table is full.
        self._matrix = np.zeros((self.capacity, self.dim), dtype=np.float32)
        self._ids: List[Optional[str]] = [None] * self.capacity
        self._last_seen = np.zeros(self.capacity, dtype=np.float64)
        self._n_used = 0
        self._free_rows: List[int] = []
        self._row_of_id: Dict[str, int] = {}

        self._inserts = 0
        self._evictions = 0

    # -- writes -----------------------------------------------------------
    def _claim_row(self, now: float) -> int:
        """A row for a new identity, evicting the stalest one if needed."""
        if self._free_rows:
            return self._free_rows.pop()
        if self._n_used < self.capacity:
            row = self._n_used
            self._n_used += 1
            return row
        # Full: the gallery holds the most recent `capacity` identities, so
        # the one seen longest ago is the one that leaves. Never grow.
        row = int(np.argmin(self._last_seen[: self._n_used]))
        old = self._ids[row]
        if old is not None:
            self._row_of_id.pop(old, None)
        self._evictions += 1
        return row

    def insert(self, canonical_id: str, embedding: np.ndarray, now: float) -> None:
        """Add or overwrite ``canonical_id``'s prototype."""
        vec = l2_normalize(embedding)
        if vec.shape[0] != self.dim:
            raise ValueError(f"embedding dim {vec.shape[0]} != gallery dim {self.dim}")
        row = self._row_of_id.get(canonical_id)
        if row is None:
            row = self._claim_row(now)
            self._row_of_id[canonical_id] = row
            self._inserts += 1
        self._matrix[row] = vec
        self._ids[row] = canonical_id
        self._last_seen[row] = now

    def touch(self, canonical_id: str, now: float) -> None:
        """Mark an identity as seen, so eviction reclaims someone else first.

        This is what makes the bound *recency*-based rather than
        insertion-order-based: a person who keeps being seen keeps their row
        however many others pass through.
        """
        row = self._row_of_id.get(canonical_id)
        if row is not None:
            self._last_seen[row] = now

    def similarity(self, canonical_id: str, embedding: np.ndarray) -> Optional[float]:
        """Cosine similarity of ``embedding`` against a stored prototype.

        ``None`` when the identity is not held (it may have been evicted by
        newer traffic) or the dimensions disagree.
        """
        row = self._row_of_id.get(canonical_id)
        if row is None:
            return None
        q = l2_normalize(embedding)
        if q.shape[0] != self.dim:
            return None
        return float(self._matrix[row] @ q)

    def update_prototype(
        self, canonical_id: str, embedding: np.ndarray, now: float, weight: float = 0.3
    ) -> None:
        """Blend a fresh observation into an existing prototype.

        ``weight`` is capped so a single long sighting cannot dominate an
        identity's stored appearance. A ``weight`` of 0 is a pure touch --
        it refreshes recency without letting a doubtful crop move the
        prototype at all.
        """
        vec = l2_normalize(embedding)
        w = min(max(float(weight), 0.0), 0.5)
        row = self._row_of_id.get(canonical_id)
        if row is None:
            self.insert(canonical_id, vec, now)
            return
        self._matrix[row] = l2_normalize((1.0 - w) * self._matrix[row] + w * vec)
        self._last_seen[row] = now

    # -- reads ------------------------------------------------------------
    def match(
        self,
        query: np.ndarray,
        now: float,
        exclude_ids: Optional[Set[str]] = None,
        require_absence: bool = True,
    ) -> Optional[GalleryMatch]:
        """Best identity for ``query``, or ``None`` when nothing is safe enough.

        Applies, in order: the live-elsewhere mask (a person cannot be in two
        places at once), the minimum-absence gate, the absolute threshold and
        the ratio test. Every one of these can only reject.

        ``require_absence=False`` drops the minimum-absence gate. That gate
        exists to stop a tracked person being re-matched to themselves during
        a momentary dropout, and it is correct whenever a tracker supplies
        continuity across frames. When the caller has no tracker -- ids that
        are unique per frame -- appearance is the *only* continuity, so a
        person visible right now must be matchable to the entry made for them
        a frame ago. Keeping the gate there rejects every match and mints a
        fresh identity per frame. The live-elsewhere mask still prevents two
        simultaneous detections collapsing into one identity.
        """
        q = l2_normalize(query)
        if q.shape[0] != self.dim or self._n_used == 0:
            return None
        exclude = exclude_ids or set()

        # One GEMV over the used rows; no copying, no per-row python maths.
        sims = self._matrix[: self._n_used] @ q

        best_id: Optional[str] = None
        best_score = -2.0
        runner_up = -2.0
        for row in range(self._n_used):
            cid = self._ids[row]
            if cid is None or cid in exclude:
                continue
            if require_absence and now - float(self._last_seen[row]) < self.min_absence_s:
                continue
            sc = float(sims[row])
            if sc > best_score:
                runner_up = best_score
                best_score, best_id = sc, cid
            elif sc > runner_up:
                runner_up = sc

        if best_id is None or best_score < self.match_threshold:
            return None
        # Ratio test: a lone high score in a crowded gallery is far less
        # trustworthy than one clearly separated from the runner-up. This is
        # the guard that stops a false merge cascading.
        if runner_up > -2.0 and (best_score - runner_up) < self.margin:
            return None
        return GalleryMatch(canonical_id=best_id, score=best_score, runner_up=max(runner_up, 0.0))

    # -- introspection ----------------------------------------------------
    def __len__(self) -> int:
        return len(self._row_of_id)

    @property
    def size(self) -> int:
        """Identities currently retained. Never exceeds ``capacity``."""
        return len(self._row_of_id)

    def stats(self) -> Dict[str, Any]:
        return {
            "size": self.size,
            "capacity": self.capacity,
            "inserts": self._inserts,
            "evictions": self._evictions,
            "bytes": int(self._matrix.nbytes),
        }

    def clear(self) -> None:
        self._matrix[: self._n_used] = 0.0
        for i in range(len(self._ids)):
            self._ids[i] = None
        self._last_seen[:] = 0.0
        self._n_used = 0
        self._free_rows.clear()
        self._row_of_id.clear()
