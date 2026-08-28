"""Stub file for extract-gt-bench.1_vms-frame-extraction directory."""
from typing import Any, Callable

# Constants
BLOCK_MS: int = ...  # From redis_connect
IDLE_NOTIFY_INTERVAL: float = ...  # From redis_connect
IDLE_WARN_THRESHOLD: float = ...  # From redis_connect
READ_COUNT: int = ...  # From redis_connect
STALE_THRESHOLD_S: float = ...  # From redis_connect
STATS_INTERVAL: float = ...  # From redis_connect
log: Any = ...  # From redis_connect
log: Any = ...  # From redis_gt_collect
RESET_BACKWARD_TICKS: Any = ...  # From rtp_map
RTP_CLOCK_HZ: int = ...  # From rtp_map
RTP_WRAP: Any = ...  # From rtp_map
RESET_BACKWARD_TICKS: Any = ...  # From rtp_probe
RTP_CLOCK_HZ: int = ...  # From rtp_probe
RTP_WRAP: Any = ...  # From rtp_probe

# Functions
# From prepare_gt_video
def main() -> int: ...

# From redis_connect
def consume_output_stream(r: Any.Any, camera_id: str, app_deployment_id: str, write_pred: Callable[[dict], None], stop_event: Any = None) -> None:
    """
    Blocking loop that reads from the Redis prediction stream and calls
    write_pred(msg) for every live, non-stale message.
    
    Parameters
    ----------
    r               : connected redis.Redis client
    camera_id       : camera identifier
    app_deployment_id: deployment identifier
    write_pred      : callback(dict) — called for every outgoing message
    stop_event      : optional threading.Event; loop exits when set
    """
    ...

# From redis_connect
def prediction_output_stream_key(camera_id: str, app_deployment_id: str) -> str: ...

# From redis_gt_collect
def parse_payload(values: dict) -> dict | None:
    """
    Extract the fields we align/save from one stream entry.
    """
    ...

# From redis_gt_collect
def redis_messages(r: Any, key: str, max_seconds: float, start_id: str = '$') -> Any:
    """
    Yield parsed payloads from a live Redis stream until max_seconds elapse.
    
        start_id="$"  -> only NEW outputs (default; src_idx is rotated by an unknown S in Case B).
        start_id="0"  -> from the OLDEST retained entry. If you START the collector within the
                         stream's history window (~MAXLEN entries, ~12s) of (re)starting the file
                         camera, the first output is ~source frame 0, so the resulting src_idx is
                         absolute (S ~= 0) with NO phase guessing needed.
    """
    ...

# From redis_gt_collect
def run_collection(messages: Any, ref: Any, out_dir: Any.Any, loops: int = 1, mode: str = 'auto', max_frames: int | None = None, log_every: int = 100) -> dict:
    """
    Drive the mapper over an iterable of parsed payloads, saving aligned frames.
    
    `messages` yields dicts from parse_payload.  Returns a report dict and writes
    `meta.json` into out_dir.  Stops after `loops` full loops of media time (or
    max_frames).  Pure — no Redis dependency, so the replay test reuses it.
    """
    ...

# From redis_gt_collect
def stream_key(camera_id: str, app_deployment_id: str) -> str: ...

# From rtp_map
def build_pts_reference(video_path: str) -> Any:
    """
    Build a PtsReference from a source video using ffprobe.
    """
    ...

# From rtp_map
def constant_fps_reference(n_frames: int, fps: float) -> Any:
    """
    Build a PtsReference assuming constant fps (fallback when no source file).
    """
    ...

# From rtp_probe
def gcd_of(values: list[int], round_to: int = 100) -> int:
    """
    GCD of values, rounding each to the nearest `round_to` first so that ±1-tick
    RTP jitter (e.g. 11999/12000/12001) does not collapse the grid to 1.
    """
    ...

# From rtp_probe
def main() -> int: ...

# From rtp_probe
def parse_message(values: dict) -> dict | None:
    """
    Extract the fields we care about from one stream entry's `result` JSON.
    """
    ...

# From rtp_probe
def probe(rows: list[dict]) -> dict:
    """
    Analyse collected rows; returns a report dict.
    """
    ...

# From rtp_probe
def stream_key(camera_id: str, app_deployment_id: str) -> str: ...

# From rtp_probe
def unwrap_rtp(rtp_values: list[int]) -> list[int]:
    """
    Convert a list of raw uint32 rtp timestamps into a continuous monotone
    sequence, undoing 2**32 wrap.  A genuine loop reset (large backward jump
    that is NOT a near-2**32 wrap) is left in place so it can be detected.
    """
    ...

# Classes
# From rtp_map
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


# From rtp_map
class MapResult:
    ...

# From rtp_map
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


from . import prepare_gt_video, redis_connect, redis_gt_collect, rtp_map, rtp_probe