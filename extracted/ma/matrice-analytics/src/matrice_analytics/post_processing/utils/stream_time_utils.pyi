"""Auto-generated stub for module: stream_time_utils."""
from typing import Any, Callable, Optional

# Constants
ENV_FLAG: str
FIRE_TIMESTAMP_FMT: str
INCIDENT_STREAM_TIME_FMT: str

# Functions
def force_wallclock_stream_time() -> bool:
    """
    True when ``MATRICE_FORCE_WALLCLOCK_STREAM_TIME`` is set to a truthy value.
    """
    ...
def set_wallclock_now_provider(provider: Optional[Callable[[], Any]]) -> None:
    """
    Override the wall-clock source. Pass ``None`` to restore the real clock.
    
        Intended for tests that need a deterministic "now"; production leaves it at
        the default (:func:`datetime.now`).
    """
    ...
def wallclock_fire_timestamp() -> str:
    """
    Wall-clock timestamp in the fire-detection human-text format.
    """
    ...
def wallclock_incident_stream_time() -> str:
    """
    Wall-clock stream_time in the incident-message format.
    """
    ...
def wallclock_now() -> Any:
    """
    Return the current wall-clock time from the (possibly injected) source.
    """
    ...
