"""Auto-generated stub for module: fire_detection."""
from typing import Any, Dict, Optional, Tuple

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_confidence, match_results_structure
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.stream_time_utils import force_wallclock_stream_time, wallclock_fire_timestamp

# Classes
class FireSmokeConfig:
    ...
class FireSmokeUseCase:
    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def get_current_frame_counts(self: Any) -> Dict[str, int]: ...

    def get_duration_seconds(self: Any, start_time: Any, end_time: Any) -> Any: ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]: ...

    def get_total_counts(self: Any) -> Dict[str, int]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

class IncidentIdTracker:
    # Tracks severity-level progression across frames to produce monotonically
    # increasing incident/alert IDs. Preserves the original numeric thresholds
    # (7 frames to advance a level; 130 empty frames to close an incident).

    def __init__(self: Any) -> None: ...

    def advance(self: Any, sev_level: str, current_ts: str) -> Tuple[int, int]:
        """
        Feed a severity level ("" if no detection). Returns (rank_id, alert_id).
        """
        ...

