"""Auto-generated stub for module: bounded_state."""
from typing import Any, Callable, Dict, List

# Constants
FACE_TRACK_MAX: int
FACE_TRACK_TTL_S: float
PERSON_SIGHTINGS_MAX_PERSONS: int
PERSON_SIGHTINGS_PER_PERSON: int
PERSON_SIGHTINGS_TTL_S: float

# Functions
def begin_frame() -> None:
    """
    Start collecting the current frame's sightings; earlier frames' are no longer reported.
    """
    ...
def idle_index(owner: Any, attr: str, max_entries: int, ttl_s: float) -> Any:
    """
    Return the index stored on ``owner`` under ``attr``, creating it on first use.
    """
    ...
def prune_track_state(owner: Any, track_id: Any, *maps: Any) -> None:
    """
    Refresh ``track_id`` in ``owner``'s per-track index and drop idle tracks from ``maps``.
    """
    ...
def record_sighting(owner: Any, person_id: str, record: Dict[str, str]) -> None:
    """
    Append one sighting to ``owner.person_tracking``.
    
        Keeps at most PERSON_SIGHTINGS_PER_PERSON sightings per person and forgets
        persons not seen for PERSON_SIGHTINGS_TTL_S or beyond PERSON_SIGHTINGS_MAX_PERSONS.
    """
    ...
def sightings_summary(tracking: Any[str, Any], frame_counts: Any[str, int] | None = None) -> Dict[str, List[Dict[str, str]]]:
    """
    ``{person_id: [sighting, ...]}`` in the historical shape.
    
        With ``frame_counts`` (the persons counted in the current frame) only the
        sightings recorded since the last :func:`begin_frame` are returned, for those
        persons, so the per-frame payload is bounded by the frame's detections rather
        than by uptime. A person counted without a sighting this frame is left out.
    """
    ...
def touch_and_prune(index: Any, key: Any, *maps: Any) -> None:
    """
    Refresh ``key`` and drop every evicted key from ``maps``.
    """
    ...

# Classes
class IdleEvictionIndex:
    # Last-touch times per key, with an idle TTL and an LRU cap.
    #
    #     ``touch`` refreshes a key and returns the keys that must now be dropped: any
    #     key idle for longer than ``ttl_s`` (monotonic clock), and the least recently
    #     touched keys beyond ``max_entries``. The key just touched is never returned.
    #     Each call costs O(1 + number of evicted keys).

    def __init__(self: Any, max_entries: int, ttl_s: float, clock: Callable[[], float] = time.monotonic) -> None: ...

    def touch(self: Any, key: Any) -> List[Any]: ...

