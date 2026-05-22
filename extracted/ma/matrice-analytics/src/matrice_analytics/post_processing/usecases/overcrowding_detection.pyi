"""Auto-generated stub for module: overcrowding_detection."""
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import apply_category_mapping, filter_by_confidence, point_in_polygon

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
    def validate(self: Any) -> List[str]: ...

class OvercrowdingDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Set client used to resolve zones from deployment/camera post-processing config.
        """
        ...

class PostProcessingConfigClient:
    # Wrapper for Matrice post-processing config: session, stream identifiers,
    # REST fetch by app deployment, and config filtering by camera_id.

    def __init__(self: Any, session: Optional[Any] = None, access_key: Optional[str] = None, secret_key: Optional[str] = None, account_number: Optional[str] = None, logger: Optional[Any.Any] = None) -> None: ...

    def denormalize_config(self: Any, config: Union[Dict[str, Any], List[Dict[str, Any]]], width: int, height: int) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Convert normalized (0–1) line/zone coordinates to integer pixel coordinates.
        """
        ...

    def filter_configs_by_camera_id(self: Any, configs: List[Dict[str, Any]], camera_id: str) -> List[Dict[str, Any]]:
        """
        Filter config documents to those containing config for the given camera_id.
        """
        ...

    def get_config_for_camera(self: Any, camera_id: str) -> Optional[Dict[str, Any]]:
        """
        Return cached post-processing config for a camera.
        """
        ...

    def get_post_processing_configs_by_app_deployment(self: Any, app_deployment_id: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str], Optional[str]]:
        """
        Fetch all post-processing configs for an app deployment via Matrice API.
        """
        ...

    def get_resolution(self: Any, camera_id: str) -> Tuple[Optional[int], Optional[int]]:
        """
        Get frame width and height for a camera by its ID.
        """
        ...

    def get_stream_identifiers(self: Any, stream_info: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Return camera_id, application_id, and app_deployment_id from stream_info.
        """
        ...

    def session(self: Any) -> Any:
        """
        Return the matrice_common Session (read-only).
        """
        ...

    def set_config_cache_from_api(self: Any, configs: List[Dict[str, Any]]) -> None:
        """
        Populate the config cache from a list of configs (e.g. from REST API).
        """
        ...

