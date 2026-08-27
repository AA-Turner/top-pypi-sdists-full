"""Auto-generated stub for module: dynamic_camera_manager."""
from typing import Any, Dict, List, Optional, Tuple

from __future__ import annotations
from camera_streamer.codec_detect import normalize_codec
from camera_streamer.nvdec.nvdec_worker_manager import NVDECWorkerManager
from constants import DEFAULT_CAMERA_HEIGHT, DEFAULT_CAMERA_QUALITY, DEFAULT_CAMERA_WIDTH, DEFAULT_MEDIAMTX_PORT
from streaming_gateway_utils import InstanceStreamingGatewayUtil, _aggregate_camera_demand, _coerce_fps, resolve_publish_fps
import logging
import os
import threading

# Functions
def DynamicCameraManagerForNVDEC(nvdec_worker_manager: Any, streaming_gateway_id: str = '', session: Any = None, streaming_gateway: Any = None, instance_util: Optional[InstanceStreamingGatewayUtil] = None) -> Any: ...
    """
    Create a DynamicCameraManager configured for the NVDEC backend.
    """
def DynamicCameraManagerForWorkers(worker_manager: Any, streaming_gateway_id: str, session: Any = None, streaming_gateway: Any = None, instance_util: Optional[InstanceStreamingGatewayUtil] = None) -> Any: ...
    """
    Create a DynamicCameraManager configured for the WorkerManager backend.
    """
def build_nvdec_camera_config(camera_data: Dict[str, Any], instance_util: Optional[InstanceStreamingGatewayUtil]) -> Optional[Dict[str, Any]]: ...
    """
    Create camera config dict for NVDECWorkerManager from event data.
    
        Returns:
            Dict compatible with NVDECWorkerManager or None if failed.
    """
def build_worker_camera_config(camera_data: Dict[str, Any], instance_util: Optional[InstanceStreamingGatewayUtil]) -> Optional[Dict[str, Any]]: ...
    """
    Create camera config dict for WorkerManager from event data.
    
        Returns:
            Dict compatible with WorkerManager/AsyncCameraWorker or None if failed.
    """

# Classes
class DynamicCameraManager:
    """
    Unified dynamic camera manager for runtime camera add/update/delete.
    
        Works with any backend (NVDECWorkerManager or WorkerManager) by accepting
        a config builder callable and a stream-key extractor.
    
        Args:
            backend: Backend manager (must implement add_camera/remove_camera/
                update_camera/get_worker_statistics).
            config_builder: Callable(camera_data, instance_util) -> Optional[Dict]
            stream_key_field: Key in the built config dict that holds the stream key.
            streaming_gateway_id: ID of the streaming gateway.
            session: Session object for API calls (optional).
            streaming_gateway: StreamingGateway instance for updating mappings (optional).
            instance_util: InstanceStreamingGatewayUtil (optional).
            log_prefix: Prefix for log messages (e.g. "[NVDEC] ").
    """

    def __init__(self: Any, backend: Any, config_builder: Any, stream_key_field: str = 'stream_key', streaming_gateway_id: str = '', session: Any = None, streaming_gateway: Any = None, instance_util: Optional[InstanceStreamingGatewayUtil] = None, log_prefix: str = '') -> None: ...

    def add_camera(self: Any, camera_data: Dict[str, Any]) -> bool: ...
        """
        Add a new camera.
        
                Args:
                    camera_data: Camera configuration data from event.
        
                Returns:
                    True if camera was added successfully.
        """

    def get_camera_assignments(self: Any) -> Dict[str, int]: ...
        """
        Return mapping of camera_id to GPU/worker ID (if supported by backend).
        """

    def get_statistics(self: Any) -> Dict[str, Any]: ...
        """
        Get camera manager statistics.
        """

    def initialize_from_config(self: Any, input_streams: list) -> Any: ...
        """
        Initialize with existing input stream configurations (tracking only).
        
                Args:
                    input_streams: List of InputStream objects.
        """

    def is_running(self: Any) -> bool: ...
        """
        Check if the backend is currently running.
        """

    def on_backend_camera_failed(self: Any, camera_id: str, reason: str) -> None: ...
        """
        Drop a camera that the backend reported as silently failed.
        
                Called by the backend (e.g. NVDECWorkerManager) when a worker reports
                add_failed AFTER the manager has already returned True from add_camera.
                Does NOT call backend.remove_camera() — the backend already considers
                the camera gone; this only reconciles DCM's own bookkeeping so the
                next periodic refresh sees the camera as absent and retries.
        """

    def remove_camera(self: Any, camera_id: str) -> bool: ...
        """
        Remove a camera.
        
                Args:
                    camera_id: ID of camera to remove.
        
                Returns:
                    True if camera was removed successfully.
        """

    def remove_camera_group(self: Any, group_id: str) -> Any: ...
        """
        Remove camera group information.
        """

    def update_camera(self: Any, camera_data: Dict[str, Any]) -> bool: ...
        """
        Update an existing camera's configuration.
        
                Args:
                    camera_data: Updated camera configuration data.
        
                Returns:
                    True if camera was updated successfully.
        """

    def update_camera_group(self: Any, group_data: Dict[str, Any]) -> Any: ...
        """
        Update camera group information.
        """

    def update_camera_input_topic(self: Any, camera_id: str, topic_name: Optional[str]) -> Any: ...
        """
        Update input topic for a camera.
        """

    def update_camera_output_topic(self: Any, camera_id: str, topic_name: Optional[str]) -> Any: ...
        """
        Update output topic for a camera.
        """

    def update_cameras_in_group(self: Any, group_id: str, group_data: Dict[str, Any]) -> Any: ...
        """
        Update all cameras in a group with new default settings.
        """

