"""Auto-generated stub for module: frame_timestamp."""
from typing import Any, Dict, Optional, Tuple

from ..advanced_tracker.rtp_clock import RtpClock

# Constants
RTP_KEYS: Tuple[Any, ...]
RTP_ZERO_IS_ABSENT: Any
SECONDS_KEYS: Tuple[Any, ...]
logger: Any

# Classes
class FrameTimestampReader:
    # Turns one stream's ``stream_info`` into seconds of stream time.

    def __init__(self: Any) -> None: ...

    def read(self: Any, stream_info: Optional[Dict[str, Any]]) -> Optional[float]:
        """
        Pull this frame's presentation time (seconds) out of ``stream_info``.
        
                The RTP timestamp is preferred: it is the source clock the gateway forwards
                byte-identically, so it survives sampling. A seconds-valued key is accepted as-is.
                Anything unusable returns ``None``, which the tracker treats as "no time base this
                frame" and logs.
        """
        ...

    def reset(self: Any) -> None:
        """
        Forget the wrap state -- called when the tracker it feeds is reset.
        """
        ...

