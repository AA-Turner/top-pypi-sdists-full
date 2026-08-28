"""
rtp_map.py — map inference outputs to original-video frame indices via RTP time.

The media server streams the GT file as a looping RTSP camera
(`ffmpeg -re -stream_loop -1 -i <file> -c:v copy -an -f rtsp ...`).  Every Redis
output carries `rtp_timestamp`, a uint32 counter on a 90 kHz media clock that is
locked to the source video's presentation time.  Inference processes only a
subset of source frames (e.g. every 3rd–4th), so a per-output counter cannot be
used as a frame index — but `rtp_timestamp` maps each output to its exact source
frame regardless of skipping or drops.

This module provides:

  * PtsReference   — per-frame PTS table built from the source video (ffprobe),
                     plus nearest-frame lookup.
  * LoopMapper     — stateful: feed raw rtp timestamps in arrival order, get back
                     (loop_index, src_idx, pos_ticks) and loop-boundary flags.
                     Handles uint32 wrap, loop resets (Case A) and continuous
                     rtp across loops (Case B, via the known loop span).

Both are pure-Python and unit-testable without Redis or a GPU.
"""

from __future__ import annotations

import bisect
import json
import math
import statistics
import subprocess
from dataclasses import dataclass, field

# RTP video clock rate (Hz). H.264/H.265 RTP timestamps tick at 90 kHz.
RTP_CLOCK_HZ = 90_000
# uint32 RTP timestamp wrap modulus.
RTP_WRAP = 1 << 32
# A backward rtp jump >= this many ticks is a loop reset, not packet reordering.
RESET_BACKWARD_TICKS = 3 * RTP_CLOCK_HZ  # 3 s of media


# ---------------------------------------------------------------------------
# Source video PTS reference
# ---------------------------------------------------------------------------

@dataclass
class PtsReference:
    """Per-frame presentation-time table for the original source video."""

    pts_ticks: list[int]          # tick offset per source frame, [0] == 0, ascending
    fps: float
    frame_interval_ticks: int     # representative (median) inter-frame ticks
    video_path: str = ""

    @property
    def n_frames(self) -> int:
        return len(self.pts_ticks)

    @property
    def loop_span_ticks(self) -> int:
        """Total media ticks for one loop (last frame's pts + one interval)."""
        if not self.pts_ticks:
            return 0
        return self.pts_ticks[-1] + self.frame_interval_ticks

    def nearest_index(self, pos_ticks: int) -> int:
        """Source frame index whose PTS is closest to pos_ticks (clamped 0..N-1)."""
        ticks = self.pts_ticks
        if pos_ticks <= ticks[0]:
            return 0
        if pos_ticks >= ticks[-1]:
            return len(ticks) - 1
        j = bisect.bisect_left(ticks, pos_ticks)
        before = ticks[j - 1]
        after = ticks[j]
        return j - 1 if (pos_ticks - before) <= (after - pos_ticks) else j


def _ffprobe_pts_times(video_path: str) -> list[float]:
    """Return per-frame presentation times (seconds), in display order."""
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "frame=best_effort_timestamp_time,pts_time",
        "-of", "json",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed on {video_path}:\n{result.stderr}")
    info = json.loads(result.stdout or "{}")
    times: list[float] = []
    for fr in info.get("frames", []):
        raw = fr.get("best_effort_timestamp_time")
        if raw in (None, "N/A"):
            raw = fr.get("pts_time")
        if raw in (None, "N/A"):
            continue
        try:
            times.append(float(raw))
        except (TypeError, ValueError):
            continue
    times.sort()
    return times


def build_pts_reference(video_path: str) -> PtsReference:
    """Build a PtsReference from a source video using ffprobe."""
    times = _ffprobe_pts_times(video_path)
    if len(times) < 2:
        raise RuntimeError(
            f"Could not read >=2 frame timestamps from {video_path} "
            "(is it a video file with a decodable stream?)"
        )
    t0 = times[0]
    pts_ticks = [round((t - t0) * RTP_CLOCK_HZ) for t in times]
    # Ensure strictly ascending (dedupe identical ticks from rounding).
    cleaned = [pts_ticks[0]]
    for v in pts_ticks[1:]:
        cleaned.append(v if v > cleaned[-1] else cleaned[-1] + 1)
    diffs = [b - a for a, b in zip(cleaned, cleaned[1:])]
    interval = int(round(statistics.median(diffs)))
    span_s = times[-1] - t0
    fps = round((len(times) - 1) / span_s, 6) if span_s > 0 else 0.0
    return PtsReference(
        pts_ticks=cleaned,
        fps=fps,
        frame_interval_ticks=max(interval, 1),
        video_path=video_path,
    )


def constant_fps_reference(n_frames: int, fps: float) -> PtsReference:
    """Build a PtsReference assuming constant fps (fallback when no source file)."""
    if n_frames < 2 or fps <= 0:
        raise ValueError("n_frames>=2 and fps>0 required")
    interval = round(RTP_CLOCK_HZ / fps)
    pts_ticks = [i * interval for i in range(n_frames)]
    return PtsReference(pts_ticks=pts_ticks, fps=fps, frame_interval_ticks=interval)


# ---------------------------------------------------------------------------
# Loop-aware rtp -> source-index mapper
# ---------------------------------------------------------------------------

@dataclass
class MapResult:
    loop_index: int       # 0-based loop number since the first anchored boundary
    src_idx: int          # source frame index in [0, N)
    pos_ticks: int        # media-time offset within the loop
    boundary: bool        # True if this frame begins a new loop
    mode: str             # 'reset' (Case A) or 'modulo' (Case B), or 'pre' (unanchored)
    cont_ticks: int       # continuous (uint32-unwrapped) rtp value of this frame


@dataclass
class LoopMapper:
    """
    Feed raw uint32 rtp timestamps in arrival order.  Emits a MapResult per frame.

    Modes
    -----
    'reset'  (Case A): rtp resets near 0 each loop.  A loop boundary is a large
             backward jump; loop-start == source frame 0, so mapping is exact.
    'modulo' (Case B): rtp runs continuously across loops.  Boundaries are
             synthesised from the known loop span; the absolute phase relative to
             gt-tracked.json is an unknown constant (resolve once by correlation).

    Mode is chosen automatically: if a reset occurs within `decide_after` loop
    spans it is 'reset', otherwise 'modulo'.  Pass `force_mode` to override.
    """

    ref: PtsReference
    reset_backward_ticks: int = RESET_BACKWARD_TICKS
    decide_after_spans: float = 1.5
    force_mode: str | None = None

    # internal state
    _offset: int = field(default=0, init=False)          # uint32 wrap offset
    _prev_cont: int | None = field(default=None, init=False)
    _origin_cont: int | None = field(default=None, init=False)
    _loop_start_cont: int | None = field(default=None, init=False)
    _loop_start_max: int = field(default=0, init=False)  # max cont within current loop
    loop_index: int = field(default=-1, init=False)
    mode: str | None = field(default=None, init=False)

    def _to_continuous(self, rtp_raw: int) -> int:
        """
        Undo uint32 wrap → continuous value.  A near-2**32 backward jump is a
        uint32 wrap (advance by one period).  A smaller backward jump is a real
        loop reset and is left in place so feed() can detect it.
        """
        if self._prev_cont is not None:
            d = (rtp_raw + self._offset) - self._prev_cont
            if d < -(RTP_WRAP // 2):
                self._offset += RTP_WRAP
        cont = rtp_raw + self._offset
        self._prev_cont = cont
        return cont

    def feed(self, rtp_raw: int) -> MapResult:
        cont = self._to_continuous(rtp_raw)
        if self._origin_cont is None:
            self._origin_cont = cont
        if self.force_mode:
            self.mode = self.force_mode

        span = self.ref.loop_span_ticks
        boundary = False

        if self._loop_start_cont is None:
            # First frame — anchor loop 0 here (partial loop if connected mid-stream).
            self._loop_start_cont = cont
            self._loop_start_max = cont
            self.loop_index = 0
            boundary = True
        elif cont <= self._loop_start_max - self.reset_backward_ticks:
            # Case A: rtp dropped far below this loop's max → loop reset.
            self._loop_start_cont = cont
            self._loop_start_max = cont
            self.loop_index += 1
            boundary = True
            if not self.force_mode:
                self.mode = "reset"
        else:
            self._loop_start_max = max(self._loop_start_max, cont)
            # Case B: no reset for >decide_after spans → segment by known span.
            if not self.force_mode and self.mode is None and span > 0:
                if (cont - self._origin_cont) > self.decide_after_spans * span:
                    self.mode = "modulo"
                    self._loop_start_cont = self._origin_cont
            if self.mode == "modulo" and span > 0:
                new_loop = (cont - self._loop_start_cont) // span
                if new_loop > self.loop_index:
                    self.loop_index = new_loop
                    boundary = True

        # Position within the loop.
        if self.mode == "modulo" and span > 0:
            pos = (cont - self._loop_start_cont) % span
        else:
            pos = cont - self._loop_start_cont
            if span > 0 and pos >= span:
                pos = span - 1  # clamp stragglers to the last frame

        pos = max(0, pos)
        return MapResult(
            loop_index=self.loop_index,
            src_idx=self.ref.nearest_index(pos),
            pos_ticks=pos,
            boundary=boundary,
            mode=self.mode or "pre",
            cont_ticks=cont,
        )

    @property
    def origin_ticks(self) -> int | None:
        """Continuous rtp of the first frame fed (collection anchor)."""
        return self._origin_cont
