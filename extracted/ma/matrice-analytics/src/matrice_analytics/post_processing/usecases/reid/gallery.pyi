"""Auto-generated stub for module: gallery."""
from typing import Any, Dict, Optional, Set

# Functions
def l2_normalize(v: Any.Any) -> Any.Any:
    """
    Return ``v`` scaled to unit L2 norm; a zero vector is returned as-is.
    """
    ...

# Classes
class GalleryMatch:
    # Outcome of a gallery query.

    ...
class ReIDGallery:
    # The ``capacity`` most recently seen person embeddings, for one stream.
    #
    #     Not internally locked: a single instance belongs to one use-case instance
    #     (one stream), and every mutation happens on the frame path. The worker
    #     thread never touches this object -- it returns embeddings, and the frame
    #     path does the matching. That keeps the concurrency story trivial.

    def __init__(self: Any, dim: int, capacity: int = 100, match_threshold: float = 0.67, margin: float = 0.06, min_absence_s: float = 3.0) -> None: ...

    def clear(self: Any) -> None: ...

    def insert(self: Any, canonical_id: str, embedding: Any.Any, now: float) -> None:
        """
        Add or overwrite ``canonical_id``'s prototype.
        """
        ...

    def match(self: Any, query: Any.Any, now: float, exclude_ids: Optional[Set[str]] = None, require_absence: bool = True) -> Optional[Any]:
        """
        Best identity for ``query``, or ``None`` when nothing is safe enough.
        
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
        ...

    def similarity(self: Any, canonical_id: str, embedding: Any.Any) -> Optional[float]:
        """
        Cosine similarity of ``embedding`` against a stored prototype.
        
                ``None`` when the identity is not held (it may have been evicted by
                newer traffic) or the dimensions disagree.
        """
        ...

    def size(self: Any) -> int:
        """
        Identities currently retained. Never exceeds ``capacity``.
        """
        ...

    def stats(self: Any) -> Dict[str, Any]: ...

    def touch(self: Any, canonical_id: str, now: float) -> None:
        """
        Mark an identity as seen, so eviction reclaims someone else first.
        
                This is what makes the bound *recency*-based rather than
                insertion-order-based: a person who keeps being seen keeps their row
                however many others pass through.
        """
        ...

    def update_prototype(self: Any, canonical_id: str, embedding: Any.Any, now: float, weight: float = 0.3) -> None:
        """
        Blend a fresh observation into an existing prototype.
        
                ``weight`` is capped so a single long sighting cannot dominate an
                identity's stored appearance. A ``weight`` of 0 is a pure touch --
                it refreshes recency without letting a doubtful crop move the
                prototype at all.
        """
        ...

