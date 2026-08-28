"""Auto-generated stub for module: advanced_customer_service."""
from typing import Any, Dict, List, Optional, Set

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import CustomerServiceConfig, ZoneConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, filter_by_confidence, get_bbox_center, match_results_structure, point_in_polygon
from ..utils.geometry_utils import to_zone_test_point
from ..utils.post_processing_config_client import GEOMETRY_RETRY_INTERVAL, PostProcessingConfigClient

# Functions
def assign_person_by_area(detections: Any, _customer_areas: Any, staff_areas: Any) -> Any:
    """
    Assign 'person' detections to 'staff' or 'customer' by area polygon.
    
        .. deprecated::
            No longer used by :class:`AdvancedCustomerServiceUseCase`, which assigns
            roles from paired counter zones via ``_update_zone_membership`` -- with
            entry/exit hysteresis, bbox-centre membership, and a bounded sticky-staff
            latch, none of which this function has. Retained because it is a public
            module-level symbol (declared in the ``.pyi`` stub) and removing it would
            be a breaking change for any out-of-tree caller. Near-identical copies live
            in ``customer_service.py`` and ``car_service.py``, which still use theirs.
    
        Modifies the detection list in-place.
    
        Args:
            detections: List of detection dicts.
            _customer_areas: Unused; kept for signature compatibility.
            staff_areas: Dict of area_name -> polygon (list of [x, y]).
    """
    ...

# Classes
class AdvancedCustomerServiceUseCase:
    def __init__(self: Any) -> None:
        """
        Initialize advanced customer service use case.
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_camera_info_from_stream(self: Any, stream_info: Any) -> Any:
        """
        Extract camera_info from stream_info, matching people_counting pattern.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for advanced customer service.
        """
        ...

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Return total unique track counts per category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[dict] = None) -> Any:
        """
        Process advanced customer service analytics.
        """
        ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Set the client used to resolve zones from the post-processing API.
        """
        ...

