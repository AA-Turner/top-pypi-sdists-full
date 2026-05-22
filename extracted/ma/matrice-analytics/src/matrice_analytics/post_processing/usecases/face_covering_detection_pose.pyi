"""Auto-generated stub for module: face_covering_detection_pose."""
from typing import Any, Dict, List, Optional, Tuple

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, PeopleCountingConfig, ZoneConfig
from ..utils import apply_category_mapping, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon
from ..utils.incident_manager_utils import IncidentManagerFactory
from .hazard_zone_entry import PostProcessingConfigClient

# Constants
LEFT_SHOULDER: int
RIGHT_SHOULDER: int

# Functions
def head_crop_from_pose(frame_shape: Tuple[int, int], box_xyxy: Tuple[float, float, float, float], kps: List[Tuple[float, float, float]]) -> Optional[Tuple[int, int, int, int]]:
    """
    Head crop in pixel coords; logic aligned with extract_faces.py.
    """
    ...

# Classes
class FaceCoveringDetectionPoseConfig:
    # Configuration for face covering detection (pose head crop + RetinaFace).

    def validate(self: Any) -> List[str]: ...

class FaceCoveringDetectionPoseUseCase:
    # Pose-guided head crops + RetinaFace for face covering / occlusion alerts.

    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def get_current_frame_count(self: Any) -> int: ...

    def get_total_count(self: Any) -> int: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def set_config_client(self: Any, client: Any) -> None: ...

