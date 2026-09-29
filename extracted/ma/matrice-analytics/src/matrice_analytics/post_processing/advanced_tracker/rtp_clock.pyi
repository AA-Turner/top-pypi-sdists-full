"""Auto-generated stub for module: rtp_clock."""
from typing import Any, Optional

# Constants
RTP_CLOCK_HZ: int
RTP_WRAP: Any

# Classes
class RtpClock:
    # Stateful uint32 RTP timestamp -> seconds converter.
    #
    #     ``to_seconds`` returns seconds since the first observed timestamp, or
    #     ``None`` when the stream's clock jumped backwards (source restart, seek, a
    #     looping file). ``None`` is the caller's signal to fall back rather than feed
    #     a nonsense interval into the tracker's time base.

    def __init__(self: Any, clock_hz: int = RTP_CLOCK_HZ) -> None: ...

    def reset(self: Any) -> None:
        """
        Forget the origin; the next timestamp restarts the clock at 0.
        """
        ...

    def to_seconds(self: Any, rtp_timestamp: int) -> Optional[float]:
        """
        Convert one raw uint32 RTP timestamp to elapsed seconds.
        
                Returns ``None`` for a backwards discontinuity (which also re-bases the
                clock on the new value, so the following frame produces a usable
                interval again).
        """
        ...

