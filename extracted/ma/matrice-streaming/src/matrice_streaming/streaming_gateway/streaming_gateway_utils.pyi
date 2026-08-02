"""Auto-generated stub for module: streaming_gateway_utils."""
from typing import Any, Dict, List, Optional, Union

from __future__ import annotations
from constants import DEFAULT_CAMERA_FPS, DEFAULT_CAMERA_HEIGHT, DEFAULT_CAMERA_QUALITY, DEFAULT_CAMERA_WIDTH, DEFAULT_OUTPUT_FPS_CAP, DEFAULT_STREAM_WH
from dataclasses import dataclass
from matrice_common.session import Session
from matrice_streaming.streaming_gateway.camera_streamer.codec_detect import normalize_codec
from metrics_reporter import HeartbeatReporter
import logging
import os
import time

# Constants
UNKNOWN_CAMERA: str
UNKNOWN_CAMERA_GROUP: str
UNKNOWN_CAMERA_LOCATION: str
logger: Any

# Functions
def build_stream_config_for_instance(instance_util: Any, service_id: str, stream_maxlen: Optional[int] = None) -> Dict: ...
    """
    Build stream_config dict from instance-based Redis connection info.
    
        Args:
            instance_util: InstanceStreamingGatewayUtil instance
            service_id: Streaming gateway ID (used as service_id)
            stream_maxlen: Maximum entries per Redis stream (approximate mode)
    
        Returns:
            Dict with connection configuration for WorkerManager
    """
def input_stream_to_camera_config(input_stream: Any) -> Dict: ...
    """
    Convert InputStream dataclass to camera_config dict for WorkerManager.
    
        This adapter function converts the InputStream configuration format used by
        StreamingGateway to the dictionary format expected by WorkerManager and
        AsyncCameraWorker.
    
        Args:
            input_stream: InputStream dataclass instance
    
        Returns:
            Dict compatible with WorkerManager/AsyncCameraWorker
    """
def resolve_operator_default_fps() -> float: ...
    """
    Resolve the operator-facing default publish rate, in FPS.
    
        ``MATRICE_OUTPUT_FPS`` overrides ``DEFAULT_OUTPUT_FPS_CAP`` (10). A value of
        ``0`` (or negative) means "cap disabled" and is returned as ``0.0`` —
        callers must treat 0 as "no ceiling", matching
        ``nvdec._resolve_output_interval_ns``, which returns interval 0 for the same
        input. A missing or malformed value falls back to the default rather than
        silently disabling the cap.
    """
def resolve_publish_fps(demand_fps: float, camera_fps: float) -> float: ...
    """
    Resolve a camera's PUBLISH rate from app demand and the camera's rate.
    
        The rule, single-sourced here so no code path can drift:
    
        * ``demand_fps > 0`` — the aggregated ``max(minFps)`` across the apps
          consuming this camera wins outright, even when it exceeds the operator
          default. That is the F08 contract: an app that declares it needs 15 fps
          gets 15 fps.
        * otherwise (no demand declared, malformed, or the lookup failed) —
          ``min(operator_default, camera_fps)``. Falling back to ``camera_fps``
          alone is what broke the cap; falling back to the operator default alone
          would "cap" a 5 fps camera at 10, which is a no-op.
    
        ``camera_fps <= 0`` (unknown source rate) yields the operator default.
        A disabled cap (``MATRICE_OUTPUT_FPS=0``) yields ``camera_fps``, i.e. publish
        every decoded frame, and ``0.0`` when the source rate is also unknown —
        which the publish gate reads as "cap disabled".
    """

# Classes
class ConnectionAuthError(RuntimeError):
    """
    Raised when the control plane permanently rejects a connection-info
        request with an auth error (HTTP 401/403).
    
        Distinguishing this from a transient outage lets the pollers fail closed
        on revoked/invalid credentials instead of silently retrying until timeout
        (which masks the real, security-relevant reason for the failure).
    """

    pass
class InputStream:
    """
    Configuration for input sources.
    """

    pass
class InstanceStreamingGatewayUtil:
    """
    Instance-based streaming gateway utility.
    
        Uses compute instance_id as the primary key for all API calls,
        replacing the old streaming_gateway_id-based flow. A single
        get_consuming_topics() call replaces the old cameras + groups + topics calls.
    """

    def __init__(self: Any, session: Session, instance_id: str, action_id: Optional[str] = None, instance_string_id: Optional[str] = None) -> None: ...

    def get_and_wait_for_redis_connection_info(self: Any, connection_timeout: int = 300) -> Dict: ...
        """
        Get Redis connection info by instance ID, polling until ready.
        
                Supports Redis Sentinel — if the API response includes sentinelHosts,
                the returned dict will contain sentinel_hosts and master_name.
        
                Args:
                    connection_timeout: Timeout in seconds (default: 300)
        
                Returns:
                    Dict with host, port, password, username, db, connection_timeout,
                    and optionally sentinel_hosts and master_name
        
                Raises:
                    RuntimeError: If timeout is reached
        """

    def get_camera_instance_ips(self: Any, camera_ids: List[str]) -> Dict[str, str]: ...
        """
        Resolve camera IDs to their hosting instance IPs.
        
                Args:
                    camera_ids: List of camera IDs to resolve
        
                Returns:
                    Dict mapping camera_id to instance IP address
        """

    def get_consuming_topics(self: Any) -> List[dict]: ...
        """
        Get all consuming topics (input+output) for this instance in a single API call.
        
                Returns:
                    List of CameraStreamTopicResponse dicts with keys:
                    cameraId, topicName, appDeploymentId, serverId, serverType,
                    ipAddress, port, cameraFPS, streamingGatewayId, topicType, isActive
        """

    def get_input_streams(self: Any, mediamtx_host: str = 'localhost', mediamtx_port: int = 8554) -> List[InputStream]: ...
        """
        Get camera input streams from consuming topics for this instance.
        
                Args:
                    mediamtx_host: MediaMTX RTSP server hostname (fallback if IP resolution fails)
                    mediamtx_port: MediaMTX RTSP server port
        
                Returns:
                    List[InputStream] configurations
        """

    def get_nvdec_input_streams(self: Any, mediamtx_host: str = 'localhost', mediamtx_port: int = 8554) -> List[InputStream]: ...
        """
        Get camera input streams with codec detection for NVDEC hardware decode.
        
                Same as get_input_streams() but adds per-camera codec detection.
        
                Args:
                    mediamtx_host: MediaMTX RTSP server hostname (fallback if IP resolution fails)
                    mediamtx_port: MediaMTX RTSP server port
        
                Returns:
                    List[InputStream] configurations with codec info
        """

    def get_output_topics_by_app_deployment(self: Any, app_deployment_id: str) -> List[dict]: ...
        """
        Get output topics filtered by app deployment + instance.
        """

    def start_streaming(self: Any, gateway_id: str) -> Optional[Dict]: ...
        """
        Start the streaming gateway by gateway ID.
        """

    def stop_streaming(self: Any, gateway_id: str) -> None: ...
        """
        Stop the streaming gateway by gateway ID.
        """

    def update_status(self: Any, gateway_id: str, status: str) -> None: ...
        """
        Update the status of the streaming gateway by gateway ID.
        """

class StreamingGatewayUtil:
    def __init__(self: Any, session: Session, streaming_gateway_id: str, server_id: Optional[str] = None, action_id: Optional[str] = None) -> None: ...

    def get_and_wait_for_connection_info(self: Any, server_type: Optional[str] = None, server_id: Optional[str] = None, connection_timeout: int = 300) -> Dict: ...
        """
        Get and wait for connection information for the streaming gateway.
        
                Args:
                    server_type: Type of server ('kafka' or 'redis'). Required.
                    server_id: ID of the server. If not provided, uses self.server_id.
                    connection_timeout: Timeout in seconds to wait for connection info (default: 300).
        
                Returns:
                    Dict: Connection configuration
        
                Raises:
                    ValueError: If server_type or server_id is not provided
                    RuntimeError: If timeout is reached while waiting for connection info
        """

    def get_streaming_gateway_by_id(self: Any) -> Any: ...

    def send_heartbeat(self: Any, camera_config: Optional[Dict] = None) -> bool: ...
        """
        Send a heartbeat to the streaming gateway via Kafka.
        
        Args:
            camera_config: Camera configuration data to include in heartbeat
                           Should contain 'cameras' list and 'stats' dict
        
        Returns:
            bool: True if heartbeat sent successfully, False otherwise
        """

    def start_streaming(self: Any) -> Optional[Dict]: ...
        """
        Start the streaming gateway.
        
        Returns:
            Dict: API response data or None if failed
        """

    def stop_streaming(self: Any) -> None: ...
        """
        Stop the streaming gateway.
        
        Returns:
            Dict: API response data or None if failed
        """

    def update_status(self: Any, status: str) -> None: ...
        """
        Update the status of the streaming gateway.
        
        Args:
            status: New status (active, inactive, starting, stopped, etc.)
        
        Returns:
            Dict: API response data or None if failed
        """

