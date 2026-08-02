"""Auto-generated stub for module: streaming_gateway."""
from typing import Any, Dict, List, Optional

from __future__ import annotations
from camera_streamer.nvdec.nvdec import DEFAULT_OUTPUT_FPS_CAP
from camera_streamer.nvdec.nvdec_worker_manager import NVDECWorkerManager, is_nvdec_available
from camera_streamer.opencv.worker_manager import WorkerManager
from constants import DEFAULT_NVDEC_NUM_SLOTS, GatewayStatus
from dynamic_camera_manager import DynamicCameraManagerForNVDEC, DynamicCameraManagerForWorkers
from instance_event_listener import InstanceEventListener
from matrice_common.diagnostics import delta, format_table, snapshot
from matrice_common.diagnostics import snapshot
from matrice_common.lifecycle import cleanup_owned_shm
from streaming_gateway_utils import InputStream, InstanceStreamingGatewayUtil, StreamingGatewayUtil, build_stream_config_for_instance, input_stream_to_camera_config
import atexit
import logging
import os
import threading
import time

# Constants
DEFAULT_OUTPUT_FPS_CAP: float
NVDEC_AVAILABLE: bool
USE_NVDEC: Any
logger: Any

# Classes
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

