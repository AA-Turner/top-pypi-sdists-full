"""Read a frame's presentation time out of ``stream_info`` (F26 S6 item 3).

SG-24 gave ``AdvancedTracker`` a per-frame time base: ``update(timestamp=...)`` in seconds
of stream time, instead of the wall-clock spacing between calls.  Under sampling those two
are not the same number, and the difference is the loss SG-24 measured and removed.

The stamp arrives on ``stream_info``, and until now only ``AdvancedTrackerAdapter`` knew how
to read it -- which meant the use cases that hold a bare ``AdvancedTracker`` from
``get_shared_tracker`` (110 of them, by the seam's own docstring) could not reach the
mechanism at all.  This is that reader, extracted so there is exactly one of it: two
implementations is how a tracker and its adapter come to disagree about what time it is.

Stateful by necessity.  An RTP timestamp is a 32-bit counter that wraps roughly every 13
hours at 90 kHz, so turning ticks into monotonically increasing seconds needs the per-stream
:class:`~matrice_analytics.post_processing.advanced_tracker.rtp_clock.RtpClock` -- one reader
per stream, not a module-level function.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from ..advanced_tracker.rtp_clock import RtpClock

logger = logging.getLogger(__name__)

#: ``stream_info`` keys carrying a frame presentation time already in SECONDS.
SECONDS_KEYS = ("frame_timestamp", "frame_time", "pts_seconds", "timestamp")
#: ``stream_info`` keys carrying a raw uint32 RTP timestamp (90 kHz clock).
#: ``rtp_number`` is the key the canonical ``build_stream_info`` emits.
RTP_KEYS = ("rtp_timestamp", "rtp_ts", "rtp_number")
#: RTP keys where ``0`` means "not stamped" rather than tick zero. The canonical
#: builder writes ``rtp_number`` as ``""`` when the worker had none, and producers
#: that coerce a missing value to an integer send ``0``.
RTP_ZERO_IS_ABSENT = frozenset({"rtp_number"})


class FrameTimestampReader:
    """Turns one stream's ``stream_info`` into seconds of stream time."""

    def __init__(self) -> None:
        self._rtp_clock = RtpClock()

    def reset(self) -> None:
        """Forget the wrap state -- called when the tracker it feeds is reset."""
        self._rtp_clock.reset()

    def read(self, stream_info: Optional[Dict[str, Any]]) -> Optional[float]:
        """Pull this frame's presentation time (seconds) out of ``stream_info``.

        The RTP timestamp is preferred: it is the source clock the gateway forwards
        byte-identically, so it survives sampling. A seconds-valued key is accepted as-is.
        Anything unusable returns ``None``, which the tracker treats as "no time base this
        frame" and logs.
        """
        if not stream_info:
            return None

        for key in RTP_KEYS:
            raw = stream_info.get(key)
            if raw is None or raw == "":
                continue
            try:
                ticks = int(raw)
            except (TypeError, ValueError):
                logger.warning("FrameTimestampReader: ignoring non-integer %s=%r", key, raw)
                return None
            if ticks == 0 and key in RTP_ZERO_IS_ABSENT:
                continue
            return self._rtp_clock.to_seconds(ticks)

        for key in SECONDS_KEYS:
            raw = stream_info.get(key)
            if raw is None:
                continue
            try:
                return float(raw)
            except (TypeError, ValueError):
                logger.warning("FrameTimestampReader: ignoring non-numeric %s=%r", key, raw)
                return None

        return None
