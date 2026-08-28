"""Auto-generated stub for module: rtp_map."""
from typing import Any

# Constants
RESET_BACKWARD_TICKS: Any
RTP_CLOCK_HZ: int
RTP_WRAP: Any

# Functions
def build_pts_reference(video_path: str) -> Any:
    """
    Build a PtsReference from a source video using ffprobe.
    """
    ...
def constant_fps_reference(n_frames: int, fps: float) -> Any:
    """
    Build a PtsReference assuming constant fps (fallback when no source file).
    """
    ...

# Classes
class LoopMapper:
    # Feed raw uint32 rtp timestamps in arrival order.  Emits a MapResult per frame.
    #
    # Modes
    # -----
    # 'reset'  (Case A): rtp resets near 0 each loop.  A loop boundary is a large
    #          backward jump; loop-start == source frame 0, so mapping is exact.
    # 'modulo' (Case B): rtp runs continuously across loops.  Boundaries are
    #          synthesised from the known loop span; the absolute phase relative to
    #          gt-tracked.json is an unknown constant (resolve once by correlation).
    #
    # Mode is chosen automatically: if a reset occurs within `decide_after` loop
    # spans it is 'reset', otherwise 'modulo'.  Pass `force_mode` to override.

    def feed(self: Any, rtp_raw: int) -> Any: ...

    def origin_ticks(self: Any) -> int | None:
        """
        Continuous rtp of the first frame fed (collection anchor).
        """
        ...

class MapResult:
    ...
class PtsReference:
    # Per-frame presentation-time table for the original source video.

    def loop_span_ticks(self: Any) -> int:
        """
        Total media ticks for one loop (last frame's pts + one interval).
        """
        ...

    def n_frames(self: Any) -> int: ...

    def nearest_index(self: Any, pos_ticks: int) -> int:
        """
        Source frame index whose PTS is closest to pos_ticks (clamped 0..N-1).
        """
        ...

