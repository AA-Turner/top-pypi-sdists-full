"""Turn a stream's per-frame RTP timestamp into monotonic seconds.

The gateway forwards the source RTP timestamp byte-identically and never
rewrites it, so it is the one time base that survives sampling: the interval
between two delivered frames is exactly ``(rtp_now - rtp_prev) / 90000`` seconds
whatever the sampler dropped in between. A rate averaged over recent ``update()``
calls cannot see that — between two frames 2 s apart it reports the mean spacing,
which is precisely the gap that breaks association.

The raw value is a uint32 on a 90 kHz media clock, so it wraps roughly every
13.3 hours. ``RtpClock`` undoes that wrap (a near-full-range backward jump is a
wrap, anything smaller is a genuine discontinuity — the same convention as
``extract-gt-bench/1_vms-frame-extraction/rtp_map.py``) and reports seconds
elapsed since the first frame it saw.
"""

from __future__ import annotations

from typing import Optional

#: RTP media clock for video, in ticks per second.
RTP_CLOCK_HZ = 90_000
#: uint32 RTP timestamp wrap modulus.
RTP_WRAP = 1 << 32


class RtpClock:
    """Stateful uint32 RTP timestamp -> seconds converter.

    ``to_seconds`` returns seconds since the first observed timestamp, or
    ``None`` when the stream's clock jumped backwards (source restart, seek, a
    looping file). ``None`` is the caller's signal to fall back rather than feed
    a nonsense interval into the tracker's time base.
    """

    def __init__(self, clock_hz: int = RTP_CLOCK_HZ) -> None:
        if clock_hz <= 0:
            raise ValueError(f"clock_hz must be positive, got {clock_hz}")
        self.clock_hz = float(clock_hz)
        self._prev_raw: Optional[int] = None
        self._ticks: int = 0

    def reset(self) -> None:
        """Forget the origin; the next timestamp restarts the clock at 0."""
        self._prev_raw = None
        self._ticks = 0

    def to_seconds(self, rtp_timestamp: int) -> Optional[float]:
        """Convert one raw uint32 RTP timestamp to elapsed seconds.

        Returns ``None`` for a backwards discontinuity (which also re-bases the
        clock on the new value, so the following frame produces a usable
        interval again).
        """
        raw = int(rtp_timestamp) & 0xFFFFFFFF

        if self._prev_raw is None:
            self._prev_raw = raw
            self._ticks = 0
            return 0.0

        # Forward delta modulo the wrap. A "forward" jump of more than half the
        # range is really a backward jump, i.e. a discontinuity, not a wrap.
        delta = (raw - self._prev_raw) % RTP_WRAP
        self._prev_raw = raw
        if delta >= RTP_WRAP // 2:
            return None

        self._ticks += delta
        return self._ticks / self.clock_hz
