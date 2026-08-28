"""Auto-generated stub for module: overcrowding_detection."""
from typing import Any, Dict, List, Optional, Set

from ..Trackers import ConfigDrivenTracker, TrackerProfile, legacy_sort_tracker_overrides
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import ByteTrackWrapper, SORTTracker, apply_category_mapping, filter_by_confidence, point_in_polygon
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.post_processing_config_client import GEOMETRY_RETRY_INTERVAL
from ..utils.post_processing_config_client import PostProcessingConfigClient

# Functions
def lift_ai_camera_zones_into_post_processing(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fold AI-style payloads into ``postProcessing`` so denormalization and zone extraction work.
    
        Supported shapes:
    
        1. Standard Matrice document: ``{"postProcessing": {camera_id: {..., "zone_config": {...}}}}``
        2. AI export (camera id as top-level key)::
    
               {"<camera_id>": {"zone_config": {"lines": {}, "zones": {"Polygon 1": [[nx,ny],...], ...}}}}
    
           Polygon / zone labels are kept as the user defined them (e.g. ``Polygon 1``); use the same
           strings in ``count_thresholds`` / ``zone_settings`` when overriding per zone.
    
        Top-level camera blocks are merged into ``postProcessing`` only for camera ids that are not
        already present under ``postProcessing`` (no overwrite).
    """
    ...

# Classes
class OvercrowdingDetectionConfig:
    def resolve_capacity(self: Any, zone_name: str) -> int:
        """
        Resolve a zone's capacity (the overcrowding threshold).
        
                Lookup order (single source of truth = ``zone_params``):
                1. ``zone_params[<zone>]["capacity"]``
                2. ``count_thresholds[<zone>]`` (legacy)
                3. ``default_capacity``
        """
        ...

    def validate(self: Any) -> List[str]: ...

class OvercrowdingDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Count of track ids reported for the FIRST time this frame, per category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Set client used to resolve zones from deployment/camera post-processing config.
        """
        ...

