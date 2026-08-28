"""Auto-generated stub for module: pipe_gas_leak_detection."""
from typing import Any, Dict, List, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_categories, filter_by_confidence, match_results_structure
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory

# Constants
logger: Any

# Classes
class PipeGasLeakDetectionConfig:
    def __init__(self: Any, usecase: str = 'gas_leak_detection', category: str = 'industrial', confidence_threshold: float = 0.25, target_categories: Optional[List[str]] = None, enable_analytics: bool = True, enable_spatial_merge: bool = True, iou_merge_threshold: float = 0.3, containment_threshold: float = 0.5, activation_frames: int = 4, deactivation_frames: int = 30, alert_cooldown_seconds: int = 30, index_to_category: Optional[Dict[int, str]] = None, alert_config: Optional[Any] = None, **kwargs: Any) -> None: ...

    def validate(self: Any) -> List[str]: ...

class PipeGasLeakDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Dict[str, int]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any: ...

