"""Exact PTS -> RTP-timestamp correlation for the GStreamer RTSP demuxer.

Deliberately free of any ``gi``/GStreamer import so the logic is unit-testable
(and counts toward coverage) on hosts without PyGObject — which includes CI, where
``PyGObject`` is not a declared dependency and every test that
``importorskip("gi")`` is skipped. It also lives here, in ``camera_streamer/``
rather than in ``camera_streamer/nvdec/`` beside its only caller, because
``pyproject``'s ``[tool.coverage.run] omit`` excludes ``*/camera_streamer/nvdec/*``
as hardware/GPU decode paths — a pure dict is not a hardware path, and the
correctness of every published timestamp depends on it.

Why this exists at all
----------------------
The SG publishes ``rtp_timestamp`` into the ring-buffer header, and the media
server's extract-by-RTP uses it as a primary key. A value that is merely *close*
returns the wrong stored frame, so the only acceptable outputs are the frame's
true timestamp or "unknown".

The previous implementation extrapolated: it captured a single session anchor
(``first_pts -> first_rtp``) and derived every later timestamp from the PTS delta.
The anchor was built by pairing the current depay-output buffer's PTS with
``_timestamp_queue[0]`` — a peek at the OLDEST completed frame. Because the
depay-sink probe runs upstream of the depay-source probe, k>=1 frames had already
completed by the time the first output buffer was probed, so the anchor bound
``first_pts`` to frame 0's RTP while the PTS belonged to frame k. Every published
timestamp was therefore ``true_rtp - k * frame_ticks`` (observed as
``rtp - 2 * 6000`` at 15 fps), and k varied with scheduler timing.

This module replaces the extrapolation with an exact per-frame lookup. Each
frame's RTP timestamp is recorded under the PTS that GStreamer stamped on the
frame's first RTP packet; the depayloader propagates that PTS to the access unit
and h264parse/h265parse preserve it, so the appsink sample carries the identical
value.

Keyed on PTS rather than FIFO-popped on purpose: the appsink runs with
``drop=true``, so samples can be dropped. A FIFO queue would hand every later
frame its predecessor's timestamp after a single drop, turning a bounded error
into unbounded drift. A keyed lookup is drop-immune.
"""

from __future__ import annotations

import threading
from collections import OrderedDict
from typing import Optional, Tuple

# ``Gst.CLOCK_TIME_NONE`` — GStreamer's "no timestamp" sentinel (G_MAXUINT64).
# Hardcoded so this module never imports gi; asserted against the real value by
# test_rtp_true_timestamp.py when gi IS available.
GST_CLOCK_TIME_NONE = 0xFFFFFFFFFFFFFFFF

# Upper bound on the in-flight map. One entry per frame between the depay-sink
# probe and the appsink pull, so a few dozen covers any realistic jitterbuffer +
# appsink queue depth. Oldest entries evict first, so a permanent PTS mismatch
# degrades to "no timestamp" instead of unbounded memory growth.
DEFAULT_MAX_ENTRIES = 256


def is_valid_pts(pts: Optional[int]) -> bool:
    """True if ``pts`` can be used as a correlation key.

    Rejects ``None``, the GStreamer sentinel, and negatives. A frame without a
    usable PTS is simply not recorded — there is nothing to key it on, and
    guessing is what this module exists to eliminate.
    """
    if pts is None:
        return False
    if pts == GST_CLOCK_TIME_NONE:
        return False
    return pts >= 0


class RtpPtsCorrelator:
    """Bounded, thread-safe ``PTS -> RTP timestamp`` map for one demuxer session.

    Thread-safe because ``record`` runs on the GStreamer streaming thread (inside
    a pad probe) while ``lookup`` runs on the thread driving ``demux()``.
    """

    def __init__(self, max_entries: int = DEFAULT_MAX_ENTRIES):
        if max_entries < 1:
            raise ValueError("max_entries must be >= 1")
        self._max_entries = max_entries
        self._map: "OrderedDict[int, int]" = OrderedDict()
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

    def record(self, pts: Optional[int], rtp_ts: int) -> bool:
        """Associate a completed frame's PTS with its true RTP timestamp.

        Returns True if the entry was stored. A frame with an unusable PTS is
        dropped rather than stored under a placeholder key.
        """
        if not is_valid_pts(pts):
            return False
        with self._lock:
            # move_to_end keeps insertion order == recency, so a repeated PTS
            # refreshes rather than stacking up entries.
            self._map[pts] = rtp_ts
            self._map.move_to_end(pts)
            while len(self._map) > self._max_entries:
                self._map.popitem(last=False)
        return True

    def lookup(self, pts: Optional[int]) -> int:
        """Return the true RTP timestamp for ``pts``, or ``0`` if unknown.

        Never approximates. ``0`` is the established "no timestamp" signal:
        ``nvdec._compute_gst_timestamp_ns`` treats a non-positive RTP timestamp as
        "no RTP timestamp from the camera", warns rate-limited, and publishes
        ``capture_timestamp_ns=0``. So a miss costs one frame's timestamp and can
        never produce a wrong one.

        Consumes the entry on a hit: each appsink sample is pulled exactly once,
        and dropping it keeps the map to genuinely in-flight frames.
        """
        rtp_ts = None
        if is_valid_pts(pts):
            with self._lock:
                rtp_ts = self._map.pop(pts, None)

        with self._lock:
            if rtp_ts is None:
                self._misses += 1
            else:
                self._hits += 1
        return 0 if rtp_ts is None else rtp_ts

    def clear(self) -> None:
        """Drop all pending entries — required on RTSP reconnect.

        A new session restarts GStreamer's PTS clock, so a stale key could collide
        with a fresh one and hand a frame the previous session's timestamp.
        Counters are intentionally preserved so the miss rate stays a
        whole-of-life diagnostic across reconnects.
        """
        with self._lock:
            self._map.clear()

    @property
    def stats(self) -> Tuple[int, int]:
        """``(hits, misses)``."""
        with self._lock:
            return self._hits, self._misses

    @property
    def miss_ratio(self) -> float:
        """Fraction of lookups that missed, 0.0 when there have been none."""
        with self._lock:
            total = self._hits + self._misses
            return (self._misses / total) if total else 0.0

    def __len__(self) -> int:
        with self._lock:
            return len(self._map)

    def pending(self) -> dict:
        """Snapshot of the in-flight map. Diagnostics/tests only."""
        with self._lock:
            return dict(self._map)
