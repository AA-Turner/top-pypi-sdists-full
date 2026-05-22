"""Auto-generated stub for module: footfall."""
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, LineConfig, ZoneConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, calculate_iou, match_results_structure
from ..utils.counting_utils import ABLineCounter, PolygonCounter, parse_line_config, polygon_offset_inward
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon

# Classes
class ByteTrackWrapper:
    # Wraps ultralytics ``BYTETracker`` so it accepts / returns pipeline
    #     detection dicts (``List[Dict]``) instead of raw numpy / Boxes objects.
    #
    #     Follows the same tracking flow as the reference ``people_counter.py``:
    #
    #     1. Convert detection dicts → ``_MockResults`` (mimics ultralytics Boxes).
    #     2. Call ``BYTETracker.update(det, img, feats)`` exactly like the reference.
    #     3. Build **new** detection dicts from the tracker output – tracked
    #        (Kalman-filtered) bounding boxes replace the raw detections, and every
    #        dict carries a ``track_id`` assigned by ByteTrack.
    #
    #     Only *confirmed* tracks are returned; untracked / low-confidence detections
    #     that ByteTrack has not yet promoted to active tracks are dropped (standard
    #     ByteTrack behaviour).

    def __init__(self: Any, track_high_thresh: float = 0.4, track_low_thresh: float = 0.1, new_track_thresh: float = 0.4, track_buffer: int = 60, match_thresh: float = 0.8, fuse_score: bool = True, frame_rate: int = 30) -> None: ...

    def update(self: Any, detections: List[Dict]) -> List[Dict]:
        """
        Run one tracking step.
        
                Parameters
                ----------
                detections : list[dict]
                    Pipeline detection dicts.  Each must contain ``bounding_box``
                    (``{xmin, ymin, xmax, ymax}`` **or** ``{x1, y1, x2, y2}``)
                    and ``confidence``.
        
                Returns
                -------
                list[dict]
                    One dict per **confirmed track** with Kalman-filtered bounding
                    boxes, ``track_id``, ``confidence``, ``category`` and
                    ``category_id``.
        """
        ...

class FootFallConfig:
    # Configuration for Footfall use case (same schema as people tracking).

    def validate(self: Any) -> List[str]:
        """
        Validate people tracking configuration.
        
                Geometry (line_a, line_b, outer_polygon, inner_polygon) may be empty at load time
                when it will be resolved from API via stream_info + config_client in process().
                At use time (_get_or_create_counter), missing geometry raises if not resolved.
        """
        ...

class FootFallUseCase:
    # Footfall use case with polygon/abline counting, zone analysis and alerting (same logic as people tracking).

    def __init__(self: Any) -> None:
        """
        Initialize footfall use case.
        """
        ...

    def clear_current_frame_tracking(self: Any) -> int:
        """
        MANUAL USE ONLY: Clear only current frame tracking data while preserving cumulative totals.
        
         This method is NOT called automatically anywhere in the code.
        
        This is the SAFE method to use for manual clearing of stale/expired current frame data.
        The cumulative total (self._total_count) is always preserved.
        
        In streaming scenarios, you typically don't need to call this at all.
        
        Returns:
            Number of current frame tracks cleared
        """
        ...

    def clear_expired_tracks(self: Any, max_age_seconds: float = 300.0) -> int: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_all_zone_counts(self: Any) -> Dict[str, Dict[str, int]]: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def get_current_frame_count(self: Any) -> int:
        """
        Get the count of people in the current frame.
        """
        ...

    def get_frame_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about frame processing and global frame offset.
        """
        ...

    def get_global_frame_id(self: Any, local_frame_id: str) -> str:
        """
        Convert local frame ID to global frame ID.
        """
        ...

    def get_global_frame_offset(self: Any) -> int:
        """
        Get the current global frame offset.
        """
        ...

    def get_total_count(self: Any) -> int:
        """
        Get the total count of unique people tracked across all calls.
        """
        ...

    def get_total_frames_processed(self: Any) -> int:
        """
        Get the total number of frames processed across all calls.
        """
        ...

    def get_track_ids_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about track IDs.
        """
        ...

    def get_tracking_debug_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed debugging information about tracking state.
        """
        ...

    def get_zone_current_count(self: Any, zone_name: str) -> int: ...

    def get_zone_total_count(self: Any, zone_name: str) -> int: ...

    def get_zone_tracking_info(self: Any) -> Dict[str, Dict[str, Any]]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Process a single frame of detections and return agg_summary with in/out counts.
                Args:
                    data: Raw model output (detection or tracking format)
                    config: People counting configuration
                    context: Processing context
                    stream_info: Stream information containing frame details (optional)
        
                Returns:
                    ProcessingResult: Processing result with standardized agg_summary structure
        """
        ...

    def reset_frame_counter(self: Any) -> None: ...

    def reset_tracking_state(self: Any) -> None:
        """
        WARNING: This completely resets ALL tracking data including cumulative totals!
        
        This should ONLY be used when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        
        For clearing expired/stale tracks, use clear_current_frame_tracking() instead.
        """
        ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Set the PostProcessingConfigClient used to resolve lines/zones from API (by_app_deployment, camera_id).
        """
        ...

    def set_global_frame_offset(self: Any, offset: int) -> None:
        """
        Set the global frame offset for video chunk processing.
        """
        ...

    def update_global_frame_offset(self: Any, frames_in_chunk: int) -> None:
        """
        Update global frame offset after processing a chunk.
        """
        ...

class PostProcessingConfigClient:
    # Wrapper for Matrice post-processing config: session, stream identifiers,
    # REST fetch by app deployment, and config filtering by camera_id.

    def __init__(self: Any, session: Optional[Any] = None, access_key: Optional[str] = None, secret_key: Optional[str] = None, account_number: Optional[str] = None, logger: Optional[Any.Any] = None) -> None:
        """
        Create client with optional session or credentials (from args or env).
        
                Credentials are loaded in order: constructor args, then env vars
                (MATRICE_ACCESS_KEY_ID, MATRICE_SECRET_ACCESS_KEY, MATRICE_ACCOUNT_NUMBER).
                If session is provided, it is used and credentials are taken from it when needed for RPC.
        
                Parameters
                ----------
                session : object, optional
                    Matrice session (e.g. from matrice_common.session.Session). If None, one is
                    created from access_key/secret_key/account_number (args or env).
                access_key : str, optional
                    Matrice API access key. Default from MATRICE_ACCESS_KEY_ID.
                secret_key : str, optional
                    Matrice API secret key. Default from MATRICE_SECRET_ACCESS_KEY.
                account_number : str, optional
                    Account number. Default from MATRICE_ACCOUNT_NUMBER (default "").
                logger : logging.Logger, optional
                    Logger to use. Defaults to module logger.
        """
        ...

    def denormalize_config(self: Any, config: Union[Dict[str, Any], List[Dict[str, Any]]], width: int, height: int) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Convert normalized (0–1) line/zone coordinates to integer pixel coordinates.
        
                Takes the same structure returned by get_post_processing_configs_by_app_deployment
                (single doc or list of docs) and converts every coordinate in postProcessing
                .<camera_id>.zone_config.lines and .zones to pixels using:
                  pixel_x = round(norm_x * width),  pixel_y = round(norm_y * height).
        
                Parameters
                ----------
                config : dict or list of dict
                    One config document or list of configs (with postProcessing, _id, etc.).
                width : int
                    Frame width in pixels (e.g. from get_resolution).
                height : int
                    Frame height in pixels (e.g. from get_resolution).
        
                Returns
                -------
                dict or list of dict
                    New config(s) with the same structure and integer coordinates.
        """
        ...

    def filter_configs_by_camera_id(self: Any, configs: List[Dict[str, Any]], camera_id: str) -> List[Dict[str, Any]]:
        """
        Filter a list of config documents to those that contain config for the given camera_id.
        
                Each config item has ``postProcessing`` keyed by camera ID; this returns
                only items whose ``postProcessing`` has an entry for `camera_id`.
        
                Parameters
                ----------
                configs : list of dict
                    List of config objects (e.g. from get_post_processing_configs_by_app_deployment).
                camera_id : str
                    Camera ID to filter by.
        
                Returns
                -------
                list of dict
                    Configs that have postProcessing[camera_id].
        """
        ...

    def get_config_for_camera(self: Any, camera_id: str) -> Optional[Dict[str, Any]]:
        """
        Return the current post-processing config for a camera from the cache.
        
                The cache is populated by set_config_cache_from_api (REST load).
        
                Parameters
                ----------
                camera_id : str
                    Camera ID.
        
                Returns
                -------
                dict or None
                    Cached config for this camera, or None if not present.
        """
        ...

    def get_post_processing_configs_by_app_deployment(self: Any, app_deployment_id: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str], Optional[str]]:
        """
        Fetch all post-processing configs for an app deployment via Matrice API.
        
                Uses: GET /v1/inference/post_processing_configs/by_app_deployment/:appDeploymentId
        
                Parameters
                ----------
                app_deployment_id : str
                    Application deployment ID.
        
                Returns
                -------
                tuple of (data, error, message)
                    - data: List of config objects, or None on failure.
                    - error: Error string or None on success.
                    - message: API message string.
        """
        ...

    def get_resolution(self: Any, camera_id: str) -> Tuple[Optional[int], Optional[int]]:
        """
        Get frame width and height for a camera by its ID.
        
                Fetches camera streams via CameraManagement and reads customStreamSettings.
                Return order is (width, height) as requested for use with denormalize_config.
        
                Parameters
                ----------
                camera_id : str
                    Camera ID (as returned by get_stream_identifiers or API).
        
                Returns
                -------
                tuple of (width, height)
                    Pixel dimensions, or (None, None) if not found or on error.
        """
        ...

    def get_stream_identifiers(self: Any, stream_info: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Return camera_id, application_id, and app_deployment_id from stream_info.
        
                application_id and app_deployment_id come from base via self._deployment_id_helper
                (ids = self._deployment_id_helper.extract_deployment_ids(stream_info)).
                camera_id follows face_recognition-style extraction (topic, camera_info, frame_id).
        
                Returns
                -------
                dict
                    Keys: ``camera_id``, ``application_id``, ``app_deployment_id``.
                    Values are strings (empty if not found).
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
        
                For each config doc, each key in postProcessing is treated as a camera_id
                and stored in the cache.
        
                Parameters
                ----------
                configs : list of dict
                    List of config objects from get_post_processing_configs_by_app_deployment.
        """
        ...

