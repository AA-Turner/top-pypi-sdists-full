"""Auto-generated stub for module: redis_gt_collect."""
from typing import Any

# Constants
log: Any

# Functions
def parse_payload(values: dict) -> dict | None:
    """
    Extract the fields we align/save from one stream entry.
    """
    ...
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
def run_collection(messages: Any, ref: Any, out_dir: Any.Any, loops: int = 1, mode: str = 'auto', max_frames: int | None = None, log_every: int = 100) -> dict:
    """
    Drive the mapper over an iterable of parsed payloads, saving aligned frames.
    
    `messages` yields dicts from parse_payload.  Returns a report dict and writes
    `meta.json` into out_dir.  Stops after `loops` full loops of media time (or
    max_frames).  Pure — no Redis dependency, so the replay test reuses it.
    """
    ...
def stream_key(camera_id: str, app_deployment_id: str) -> str: ...
