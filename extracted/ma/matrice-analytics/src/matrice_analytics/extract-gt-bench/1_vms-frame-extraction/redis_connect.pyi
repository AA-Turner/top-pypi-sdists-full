"""Auto-generated stub for module: redis_connect."""
from typing import Any, Callable

# Constants
BLOCK_MS: int
IDLE_NOTIFY_INTERVAL: float
IDLE_WARN_THRESHOLD: float
READ_COUNT: int
STALE_THRESHOLD_S: float
STATS_INTERVAL: float
log: Any

# Functions
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
def prediction_output_stream_key(camera_id: str, app_deployment_id: str) -> str: ...
