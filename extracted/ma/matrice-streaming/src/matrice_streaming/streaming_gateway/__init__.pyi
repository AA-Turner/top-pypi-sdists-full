"""Stub file for streaming_gateway directory."""
from typing import Any, Dict, List, Optional, Tuple, Union

from __future__ import annotations
from camera_streamer.codec_detect import normalize_codec
from camera_streamer.nvdec.nvdec import DEFAULT_OUTPUT_FPS_CAP
from camera_streamer.nvdec.nvdec_worker_manager import NVDECWorkerManager
from camera_streamer.nvdec.nvdec_worker_manager import NVDECWorkerManager, is_nvdec_available
from camera_streamer.opencv.worker_manager import WorkerManager
from concurrent.futures import ThreadPoolExecutor, as_completed
from constants import DEFAULT_CAMERA_FPS, DEFAULT_CAMERA_HEIGHT, DEFAULT_CAMERA_QUALITY, DEFAULT_CAMERA_WIDTH, DEFAULT_OUTPUT_FPS_CAP, DEFAULT_STREAM_WH
from constants import DEFAULT_CAMERA_HEIGHT, DEFAULT_CAMERA_QUALITY, DEFAULT_CAMERA_WIDTH, DEFAULT_MEDIAMTX_PORT
from constants import DEFAULT_NVDEC_NUM_SLOTS, GatewayStatus
from constants import GatewayStatus
from dataclasses import dataclass
from dynamic_camera_manager import DynamicCameraManagerForNVDEC, DynamicCameraManagerForWorkers
from enum import Enum
from instance_event_listener import InstanceEventListener
from matrice_common.diagnostics import delta, format_table, snapshot
from matrice_common.diagnostics import snapshot
from matrice_common.lifecycle import cleanup_owned_shm
from matrice_common.rpc import RPC
from matrice_common.session import Session
from matrice_common.stream import EventListener
from matrice_streaming.streaming_gateway.camera_streamer.codec_detect import normalize_codec
from metrics import HeartbeatReporter, MetricsCalculator, MetricsCollector, MetricsConfig, MetricsManager, MetricsReporter
from metrics_reporter import HeartbeatReporter
from metrics_reporter import MetricsConfig, MetricsManager
from streaming_gateway import USE_NVDEC, StreamingGateway
from streaming_gateway_utils import InputStream, InstanceStreamingGatewayUtil, StreamingGatewayUtil, build_stream_config_for_instance, input_stream_to_camera_config
from streaming_gateway_utils import InstanceStreamingGatewayUtil, StreamingGatewayUtil
from streaming_gateway_utils import InstanceStreamingGatewayUtil, _aggregate_camera_demand, _coerce_fps, resolve_publish_fps
from streaming_status_listener import StreamingStatusListener
import atexit
import logging
import os
import threading
import time

# Constants
DEFAULT_CAMERA_FPS: int = ...  # From constants
DEFAULT_CAMERA_HEIGHT: int = ...  # From constants
DEFAULT_CAMERA_QUALITY: int = ...  # From constants
DEFAULT_CAMERA_WIDTH: int = ...  # From constants
DEFAULT_CONNECTION_TIMEOUT: int = ...  # From constants
DEFAULT_IPC_COMMAND_QUEUE_MAXSIZE: int = ...  # From constants
DEFAULT_IPC_RESULT_QUEUE_MAXSIZE: int = ...  # From constants
DEFAULT_IPC_STATUS_QUEUE_MAXSIZE: int = ...  # From constants
DEFAULT_MEDIAMTX_PORT: int = ...  # From constants
DEFAULT_NVDEC_NUM_SLOTS: int = ...  # From constants
DEFAULT_OPENCV_OPTIMIZATION_MODE: str = ...  # From constants
DEFAULT_OUTPUT_FPS_CAP: float = ...  # From constants
DEFAULT_STREAM_FPS: Any = ...  # From constants
DEFAULT_STREAM_WH: Tuple[Any, ...] = ...  # From constants
DEFAULT_WORKER_STOP_TIMEOUT: float = ...  # From constants
PERIODIC_CIRCUIT_COOLDOWN_CAP_SEC: float = ...  # From instance_event_listener
PHANTOM_GRACE_SEC: float = ...  # From instance_event_listener
logger: Any = ...  # From streaming_action
DEFAULT_OUTPUT_FPS_CAP: float = ...  # From streaming_gateway
NVDEC_AVAILABLE: bool = ...  # From streaming_gateway
USE_NVDEC: Any = ...  # From streaming_gateway
logger: Any = ...  # From streaming_gateway
UNKNOWN_CAMERA: str = ...  # From streaming_gateway_utils
UNKNOWN_CAMERA_GROUP: str = ...  # From streaming_gateway_utils
UNKNOWN_CAMERA_LOCATION: str = ...  # From streaming_gateway_utils
logger: Any = ...  # From streaming_gateway_utils

# Functions
# From dynamic_camera_manager
def DynamicCameraManagerForNVDEC(nvdec_worker_manager: Any, streaming_gateway_id: str = '', session: Any = None, streaming_gateway: Any = None, instance_util: Optional[InstanceStreamingGatewayUtil] = None) -> Any: ...
    """
    Create a DynamicCameraManager configured for the NVDEC backend.
    """

# From dynamic_camera_manager
def DynamicCameraManagerForWorkers(worker_manager: Any, streaming_gateway_id: str, session: Any = None, streaming_gateway: Any = None, instance_util: Optional[InstanceStreamingGatewayUtil] = None) -> Any: ...
    """
    Create a DynamicCameraManager configured for the WorkerManager backend.
    """

# From dynamic_camera_manager
def build_nvdec_camera_config(camera_data: Dict[str, Any], instance_util: Optional[InstanceStreamingGatewayUtil]) -> Optional[Dict[str, Any]]: ...
    """
    Create camera config dict for NVDECWorkerManager from event data.
    
        Returns:
            Dict compatible with NVDECWorkerManager or None if failed.
    """

# From dynamic_camera_manager
def build_worker_camera_config(camera_data: Dict[str, Any], instance_util: Optional[InstanceStreamingGatewayUtil]) -> Optional[Dict[str, Any]]: ...
    """
    Create camera config dict for WorkerManager from event data.
    
        Returns:
            Dict compatible with WorkerManager/AsyncCameraWorker or None if failed.
    """

# From streaming_gateway_utils
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

# From streaming_gateway_utils
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

# From streaming_gateway_utils
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

# From streaming_gateway_utils
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
# From constants
class GatewayStatus(str, Enum):
    """
    Status values for the streaming gateway lifecycle.
    """

    INITIALIZED: str
    RUNNING: str
    STOPPED: str
    STOPPING: str

    pass

# From dynamic_camera_manager
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


# From instance_event_listener
class InstanceEventListener:
    """
    Refresh-based listener for instance-specific streaming events.
    
        Subscribes to:
        - {instance_id}_streaming_gateway_event
    
        On any message received, re-fetches the full camera list from the
        consuming topics API and diffs against the current camera manager state.
    
        Also runs a periodic auto-refresh timer as a safety net.
    """

    def __init__(self: Any, session: Session, instance_id: str, camera_manager: Any, instance_util: Any, auto_refresh_interval: float = 60.0) -> None: ...
        """
        Initialize instance event listener.
        
                Args:
                    session: Session object for authentication
                    instance_id: Compute instance ID
                    camera_manager: DynamicCameraManager variant instance
                    instance_util: InstanceStreamingGatewayUtil instance for API calls
                    auto_refresh_interval: Seconds between periodic auto-refreshes
                        (default 60s). Acts as a safety-net backstop in case a Kafka
                        event is missed. With 1K+ cameras, polling more often would
                        hammer the consuming-topics API for no benefit — Kafka events
                        drive the fast-path; periodic refresh is just for resilience.
        """

    def get_statistics(self: Any) -> dict: ...
        """
        Get event listener statistics.
        """

    def handle_event(self: Any, event: Dict[str, Any]) -> Any: ...
        """
        Handle any instance event by triggering a refresh.
        
                All events on instance topics are treated as refresh triggers.
                The actual camera list is always re-fetched from the API.
        
                Args:
                    event: Event dict (structure varies, but we only use it for logging)
        """

    def is_listening(self: Any) -> bool: ...
        """
        Check if listener is active.
        """

    def start(self: Any) -> bool: ...
        """
        Start listening to instance events and periodic refresh.
        
                Returns:
                    bool: True if started successfully
        """

    def stop(self: Any) -> Any: ...
        """
        Stop listening and periodic refresh.
        """


# From streaming_action
class StreamingAction:
    """
    High-level orchestrator for streaming gateway lifecycle management.
    
    This class automates the entire streaming process:
    1. Fetches configuration from API using streaming_gateway_id
    2. Sets up StreamingGateway with proper configuration
    3. Starts streaming with status updates to API
    4. Monitors streaming health
    5. Periodically checks if action ID matches streaming gateway's actionRecordID
    6. Automatically stops if action ID mismatch is detected
    7. Handles errors and recovery
    8. Provides clean shutdown
    
    Example usage:
        orchestrator = StreamingAction(
            session=session,
            action_id="your_action_id",
            action_id_check_interval=30.0,  # Check every 30 seconds
        )
    
        # Start streaming (auto-fetches config, sets up, and starts)
        if orchestrator.start():
            logger.info("Streaming started successfully!")
    
            # Monitor for a while
            time.sleep(60)
    
            # Stop when done
            orchestrator.stop()
        else:
            logger.error("Failed to start streaming")
    """

    def __init__(self: Any, session: Session, action_id: str, enable_intelligent_transmission: bool = True, monitoring_interval: float = 30.0, auto_restart: bool = True, max_restart_attempts: int = 3, action_id_check_interval: float = 600.0, enable_event_listening: bool = True, allow_empty_start: bool = True) -> None: ...
        """
        Initialize StreamingAction.
        
                Args:
                    session: Session object for authentication
                    action_id: ID of the action to manage
                    enable_intelligent_transmission: Whether to enable intelligent frame transmission
                    monitoring_interval: Interval in seconds between health checks and heartbeats (default: 30 seconds)
                    auto_restart: Whether to automatically restart on failures
                    max_restart_attempts: Maximum number of restart attempts before giving up
                    action_id_check_interval: Interval in seconds between checks to verify action ID matches streaming gateway
                    enable_event_listening: Enable dynamic event listening for configuration updates
                    allow_empty_start: Allow starting with zero cameras (default True). Cameras can be added dynamically.
        """

    def check_action_id_matches(self: Any) -> bool: ...
        """
        Check if the current action ID matches the streaming gateway's actionRecordID.
        
        Handles transient errors gracefully:
        - 502 Bad Gateway: Skip check, continue streaming (server temporarily unavailable)
        - 404 Not Found: Stop streaming (gateway may be deleted)
        - Other API errors: Skip check, continue streaming (don't stop on transient issues)
        
        Returns:
            bool: True if action ID matches or check should be skipped, False if mismatch or gateway deleted
        """

    def get_status(self: Any) -> Dict: ...
        """
        Get current orchestrator status and statistics.
        
        Returns:
            Dict: Complete status information
        """

    def is_healthy(self: Any) -> bool: ...
        """
        Check if the orchestrator is healthy.
        
        Returns:
            bool: True if healthy, False otherwise
        """

    def restart(self: Any) -> bool: ...
        """
        Restart the streaming orchestrator.
        
        Returns:
            bool: True if restarted successfully, False otherwise
        """

    def start(self: Any, block: bool = True) -> bool: ...
        """
        Start the streaming orchestrator.
        
        This method:
        1. Fetches streaming configuration from API
        2. Creates and configures StreamingGateway
        3. Starts streaming with API status updates
        4. Starts health monitoring
        
        Args:
            block: Whether to block the thread until the streaming gateway is started (default: True)
        
        Returns:
            bool: True if started successfully, False otherwise
        """

    def stop(self: Any) -> bool: ...
        """
        Stop the streaming orchestrator.
        
        Returns:
            bool: True if stopped successfully, False otherwise
        """

    def update_status(self: Any, step_code: str, status: str, status_description: str) -> None: ...
        """
        Update the status of the data processing job.
        """


# From streaming_gateway
class KafkaConsumerWatchdog:
    """
    Restarts the gateway's event listener when its Kafka consumer goes silent.
    
        The underlying ``EventListener`` exposes ``last_poll_monotonic`` (advanced on
        every poll, even empty ones). If it stops advancing past ``stale_threshold``
        while the listener still claims to be active, the consumer was silently evicted
        from its group (e.g. after a backend/broker outage) and will never rejoin on
        its own — so we stop and restart the listener (full close + re-subscribe). This
        is the supervisor that was missing during the 2026-06-03 61h gateway outage,
        where the consumer left its group and camera discovery stayed dead for 61h.
    """

    def __init__(self: Any, event_listener: Any, is_active_fn: Any, check_interval_sec: Any = 60.0, stale_threshold_sec: Any = 300.0) -> None: ...

    def start(self: Any) -> None: ...

    def stop(self: Any) -> None: ...


# From streaming_gateway
class StreamingGateway:
    """
    Simplified streaming gateway for managing camera streams.
    """

    def __init__(self: Any, session: Any, streaming_gateway_id: Optional[str] = None, instance_id: Optional[str] = None, instance_string_id: Optional[str] = None, server_id: Optional[str] = None, server_type: Optional[str] = None, inputs_config: Optional[List[InputStream]] = None, video_codec: Optional[str] = None, force_restart: bool = False, enable_event_listening: bool = True, action_id: Optional[str] = None, num_workers: Optional[int] = None, max_cameras_per_worker: int = 50, allow_empty_start: bool = True, use_nvdec: bool = USE_NVDEC, nvdec_gpu_id: int = 0, nvdec_num_gpus: int = 0, nvdec_pool_size: int = 8, nvdec_burst_size: Optional[int] = None, nvdec_frame_width: int = 0, nvdec_frame_height: int = 0, nvdec_num_slots: int = DEFAULT_NVDEC_NUM_SLOTS, nvdec_target_fps: int = 0, nvdec_output_fps_cap: float = DEFAULT_OUTPUT_FPS_CAP, shm_slot_count: int = 1000) -> None: ...
        """
        Initialize StreamingGateway.
        
                Args:
                    session: Session object for authentication
                    streaming_gateway_id: ID of the streaming gateway
                    server_id: ID of the server (Kafka/Redis)
                    server_type: Type of server (kafka or redis)
                    inputs_config: List of InputStream configurations
                    video_codec: Video codec (h264 or h265)
                    force_restart: Force stop existing streams and restart
                    enable_event_listening: Enable dynamic event listening for configuration updates
                    action_id: Optional action ID to pass in API requests
                    num_workers: Number of worker processes for async flow
                    max_cameras_per_worker: Maximum cameras per worker process
                    allow_empty_start: Allow starting with zero cameras (default True)
                    use_nvdec: Use NVDEC hardware decode with CUDA IPC output (requires CuPy, PyNvVideoCodec)
                    nvdec_gpu_id: Primary/starting GPU device ID for round-robin camera assignment
                    nvdec_num_gpus: Number of GPUs to use (0=auto-detect all available GPUs)
                    nvdec_pool_size: Number of NVDEC decoders per GPU
                    nvdec_burst_size: Frames per stream before rotating to next stream.
                                      None (default) = auto-tier by per-decoder stream
                                      count (<=10 -> 1, 11-50 -> 2, >50 -> 4). Env var
                                      MATRICE_NVDEC_BURST_SIZE forces an explicit value.
                    nvdec_frame_width: Default output frame width (used if camera config doesn't specify)
                    nvdec_frame_height: Default output frame height (used if camera config doesn't specify)
                    nvdec_num_slots: Ring buffer slots per camera (named by camera_id)
                    nvdec_target_fps: Global FPS override (0=use per-camera FPS from camera config)
                    nvdec_output_fps_cap: Per-camera publish (output) FPS cap, default
                        DEFAULT_OUTPUT_FPS_CAP (10). Env MATRICE_OUTPUT_FPS overrides it
                        per deployment (0 disables the cap). Separate from the decode pacer.
                    shm_slot_count: Number of frame slots per camera ring buffer for SHM mode (default: 300)
        """

    def active_worker_manager(self: Any) -> Any: ...
        """
        Return whichever worker backend is in use (NVDEC or OpenCV WorkerManager).
        """

    def get_camera_id_for_stream_key(self: Any, stream_key: str) -> Optional[str]: ...
        """
        Get camera_id for a given stream_key.
        """

    def get_config(self: Any) -> Dict: ...
        """
        Get current configuration.
        """

    def get_statistics(self: Any) -> Dict: ...
        """
        Get streaming statistics.
        """

    def start_streaming(self: Any) -> bool: ...
        """
        Start streaming.
        
                Returns:
                    bool: True if streaming started successfully, False otherwise
        """

    def stop_streaming(self: Any) -> None: ...
        """
        Stop all streaming operations.
        """


# From streaming_gateway_utils
class ConnectionAuthError(RuntimeError):
    """
    Raised when the control plane permanently rejects a connection-info
        request with an auth error (HTTP 401/403).
    
        Distinguishing this from a transient outage lets the pollers fail closed
        on revoked/invalid credentials instead of silently retrying until timeout
        (which masks the real, security-relevant reason for the failure).
    """

    pass

# From streaming_gateway_utils
class InputStream:
    """
    Configuration for input sources.
    """

    pass

# From streaming_gateway_utils
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


# From streaming_gateway_utils
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


# From streaming_status_listener
class StreamingStatusListener:
    """
    Listener for streaming gateway status events from Kafka.
    
        This class listens to the Streaming_Events_Status topic and triggers
        a callback when a stop command is received for this gateway.
    """

    def __init__(self: Any, session: Session, streaming_gateway_id: str, action_id: str, on_stop_callback: Any) -> None: ...
        """
        Initialize status listener.
        
                Args:
                    session: Session object for authentication
                    streaming_gateway_id: ID of streaming gateway to filter events
                    action_id: ID of action record to filter events
                    on_stop_callback: Callback function to invoke when stop event is received
        """

    def get_statistics(self: Any) -> dict: ...
        """
        Get statistics.
        """

    def handle_event(self: Any, event: dict) -> Any: ...
        """
        Handle status event.
        
                Args:
                    event: Status event dict with eventType, streamingGatewayId, timestamp
        """

    def is_listening(self: Any) -> bool: ...
        """
        Check if listener is active.
        """

    def start(self: Any) -> bool: ...
        """
        Start listening to status events.
        
                Returns:
                    bool: True if started successfully
        """

    def stop(self: Any) -> Any: ...
        """
        Stop listening.
        """


from . import constants, dynamic_camera_manager, instance_event_listener, metrics_reporter, streaming_action, streaming_gateway, streaming_gateway_utils, streaming_status_listener