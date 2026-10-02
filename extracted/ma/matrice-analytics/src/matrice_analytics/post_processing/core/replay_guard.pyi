"""Auto-generated stub for module: replay_guard."""
from typing import Any, Dict, Optional

# Constants
logger: Any

# Functions
def is_cache_replay(data: Any, stream_info: Optional[Dict[str, Any]] = None) -> bool:
    """
    Whether this frame is a cache replay and must not be counted.
    """
    ...
def note_refusal(health: Any, marker: str, camera_id: str = '') -> None:
    """
    Record a refusal on ``health`` and log the first one for this camera at WARNING.
    """
    ...
def replay_marker(data: Any, stream_info: Optional[Dict[str, Any]] = None) -> Optional[str]:
    """
    Name the marker that makes this frame a cache replay, or ``None`` if it is a real one.
    
        Returns the key rather than a bool so the caller can say *which* marker it saw. A carrier
        and a republished result arrive by different routes and mean different upstream mistakes,
        and a refusal that cannot tell them apart is one nobody can act on.
    """
    ...

# Classes
class ReplayGuardHealth:
    # How many replays the counting path was asked to consume, and from where.
    #
    #     Mirrors the shape of ``Trackers.integration.TrackerHealth`` deliberately: both answer the
    #     same question -- did this stream's counts come from every frame, or only from the ones
    #     that worked -- and a caller should not need two idioms to ask it.

    def degraded(self: Any) -> bool:
        """
        True once anything has been refused: no healthy stream reaches this seam at all.
        """
        ...

    def record(self: Any, marker: str, camera_id: str = '') -> bool:
        """
        Record one refusal. Returns whether this is the first for ``camera_id``.
        
                The return value is the rate limit. A regression here is per-route, not per-frame, so
                one loud line per camera says everything a hundred would; the count carries the rest.
        """
        ...

    def snapshot(self: Any) -> Dict[str, Any]:
        """
        A plain dict for the result payload and for tests.
        """
        ...

