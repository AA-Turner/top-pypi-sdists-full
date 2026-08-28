"""Auto-generated stub for module: post_processing_config_client."""
from typing import Any, Dict, List, Optional, Tuple, Union

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from .location_name_cache import LocationNameCache

# Constants
GEOMETRY_RETRY_INTERVAL: int

# Functions
def is_null_object_id(value: Any) -> bool:
    """
    Return True for the all-zero placeholder ObjectId (unset location).
    """
    ...
def is_resolvable_location_id(value: Any) -> bool:
    """
    Return True when ``value`` is a real location ObjectId worth API lookup.
    """
    ...
def looks_like_object_id(value: Any) -> bool:
    """
    Return True when ``value`` looks like a MongoDB ObjectId (24 hex chars).
    """
    ...
def normalize_location_id(value: Any) -> str:
    """
    Return a stripped location id, or empty for unset / null ObjectId placeholders.
    """
    ...

# Classes
class PostProcessingConfigClient:
    # Wrapper for Matrice post-processing config: session, stream identifiers,
    # REST fetch by app deployment, and config filtering by camera_id.

    def __init__(self: Any, session: Optional[Any] = None, access_key: Optional[str] = None, secret_key: Optional[str] = None, account_number: Optional[str] = None, logger: Optional[Any.Any] = None) -> None: ...

    def denormalize_config(self: Any, config: Union[Dict[str, Any], List[Dict[str, Any]]], width: int, height: int) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Convert normalized (0–1) line/zone coordinates to integer pixel coordinates.
        """
        ...

    def fetch_location_name(self: Any, location_id: str) -> str:
        """
        Resolve a human-readable location name from a location ObjectId.
        """
        ...

    def filter_configs_by_camera_id(self: Any, configs: List[Dict[str, Any]], camera_id: str) -> List[Dict[str, Any]]:
        """
        Filter config documents to those containing config for the given camera_id.
        """
        ...

    def get_camera_metadata(self: Any, camera_id: str) -> Dict[str, str]:
        """
        Look up human-readable camera fields by id via CameraManagement API.
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

