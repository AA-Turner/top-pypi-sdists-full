"""Auto-generated stub for module: nvdec_worker_manager."""
from typing import Any, Dict, List, Optional, Set, Tuple

from matrice_common.diagnostics import format_table, snapshot
from matrice_common.stream.cuda_shm_ring_buffer import GlobalFrameCounter
from matrice_common.stream.device_topology import topology
from matrice_common.stream.gpu_camera_map import GpuCameraMap
from nvdec import CUPY_AVAILABLE, DEFAULT_OUTPUT_FPS_CAP, ORIN_NVDEC_AVAILABLE, PYNVCODEC_AVAILABLE, RING_BUFFER_AVAILABLE, StreamConfig, nvdec_pool_process
from nvdec import _get_nv12_resize_kernel
from shm_liveness import camera_has_live_shm
from shm_liveness import held_shm_paths, is_shm_path_live
import cupy as _cp
import cupy as cp
import glob
import hashlib
import json as _json
import logging
import multiprocessing as mp
import os
import signal as _sig
import threading
import time
import urllib.request

# Constants
CIRCUIT_BREAKER_COOLDOWN_SEC: Any
CIRCUIT_BREAKER_MAX_RESTARTS: Any
CIRCUIT_BREAKER_WARN_INTERVAL_SEC: Any
CIRCUIT_BREAKER_WINDOW_SEC: Any
FRAME_STALL_THRESHOLD_SEC: Any
HANDLER_STALE_SEC: Any
HOTADD_MAX_ATTEMPTS: Any
HOTADD_RETRY_BACKOFF_SEC: Any
PRODUCER_READY_TIMEOUT_SEC: Any
REMOVE_ACK_TIMEOUT_SEC: Any
logger: Any

# Functions
def get_available_gpu_count() -> int: ...
    """
    Detect the number of available CUDA GPUs.
    
        Returns:
            Number of available GPUs, or 1 if detection fails.
    """
def is_nvdec_available() -> bool: ...
    """
    Check if NVDEC backend is available.
    
        On desktop/Thor: Requires CuPy, PyNvVideoCodec, ring buffer.
        On Orin (MATRICE_PLATFORM=orin): Requires CuPy, gst-launch-1.0, ring buffer.
        PyNvVideoCodec is NOT needed on Orin (CUVID API unavailable).
    """

# Classes
class NVDECWorkerManager:
    """
    Manager for NVDEC worker processes - fully dynamic camera configuration.
    
        This manager wraps the existing nvdec_pool_process function to integrate
        with StreamingGateway. Key features:
    
        - Fully dynamic camera configuration (add, remove, update at runtime)
        - Smart per-GPU restarts: only restarts workers for GPUs whose cameras changed
        - Debounced batching: rapid successive changes are batched into a single restart
        - Stable GPU assignment: cameras are assigned to GPUs via consistent hashing,
          so add/remove of one camera doesn't shuffle other cameras across GPUs
        - Outputs to CUDA IPC ring buffers (not Redis/Kafka)
        - NV12 format output (50% smaller than RGB)
        - One worker process per GPU
    """

    def __init__(self: Any, camera_configs: List[Dict[str, Any]], stream_config: Dict[str, Any], gpu_id: int = 0, num_gpus: int = 0, nvdec_pool_size: int = 0, nvdec_burst_size: Optional[int] = None, frame_width: int = 0, frame_height: int = 0, num_slots: int = 64, target_fps: int = 0, duration_sec: float = 0, demuxer_type: str = 'nvc', restart_delay: float = 1.0, optimizer_config: Optional[Dict[str, Any]] = None, output_fps_cap: float = DEFAULT_OUTPUT_FPS_CAP) -> None: ...
        """
        Initialize NVDEC Worker Manager.
        
                Args:
                    camera_configs: List of camera configuration dicts with keys:
                        - camera_id or stream_key: Unique identifier (used for ring buffer naming)
                        - source: Video file path or RTSP URL
                        - width: Optional frame width (default: frame_width)
                        - height: Optional frame height (default: frame_height)
                        - fps: FPS limit for this camera (used by default)
                    stream_config: Stream configuration (unused, for interface consistency)
                    gpu_id: Primary GPU device ID (starting GPU for round-robin assignment)
                    num_gpus: Number of GPUs to use (0 = auto-detect all available GPUs)
                    nvdec_pool_size: Number of NVDEC decoders per GPU
                    nvdec_burst_size: Frames per stream before rotating to next.
                                      None (default) = auto-tier by per-decoder camera
                                      count (<=10 -> 1, 11-50 -> 2, >50 -> 4). Env var
                                      MATRICE_NVDEC_BURST_SIZE forces an explicit value.
                    frame_width: Default output frame width (used if camera config doesn't specify)
                    frame_height: Default output frame height (used if camera config doesn't specify)
                    num_slots: Ring buffer slots per camera
                    target_fps: Global FPS override (0 = use per-camera FPS from config)
                    duration_sec: Duration to run (0 = infinite until stop)
                    demuxer_type: Demuxer backend - "nvc" (PyNvVideoCodec, fastest for files) or
                                  "gstreamer" (provides ABSOLUTE RTP timestamps for RTSP streams)
                    restart_delay: Seconds to wait before restarting after a config change,
                                   allowing multiple rapid changes to be batched into one restart
        """

    def add_camera(self: Any, camera_config: Dict[str, Any]) -> bool: ...
        """
        Add a new camera at runtime via IPC command to the GPU worker.
        
                Args:
                    camera_config: Camera configuration dict
        
                Returns:
                    True if the camera was accepted
        """

    def evict_camera_mapping(self: Any, camera_id: str, reason: str = '') -> bool: ...
        """
        Remove a camera entry from GpuCameraMap.
        
                Used for graceful removal, deletion events, or startup sweep of
                stale entries. Idempotent. The placer is NOT invoked.
        
                Args:
                    camera_id: Camera identifier to evict.
                    reason: Optional reason string for the log line.
        
                Returns:
                    True if any state was actually evicted.
        """

    def get_camera_assignments(self: Any) -> Dict[str, int]: ...
        """
        Return mapping of camera_id to GPU ID.
        
                Returns:
                    Dict mapping camera_id -> gpu_id
        """

    def get_worker_statistics(self: Any) -> Dict[str, Any]: ...
        """
        Return statistics from workers.
        
                Returns:
                    Dict with worker count, camera count, FPS metrics, per-GPU stats, etc.
        """

    def is_running(self: Any) -> bool: ...
        """
        Check if the manager is currently running.
        """

    def remove_camera(self: Any, stream_key: str) -> bool: ...
        """
        Remove a camera at runtime via IPC command to the GPU worker.
        
                Args:
                    stream_key: Camera ID / stream key to remove
        
                Returns:
                    True if the removal was effected (worker ACKed, or nothing was
                    running to stop). False only if the command was sent but the worker
                    did not ACK within the timeout — DCM then keeps the camera and the
                    next refresh retries, which self-heals (the retry no-ops and ACKs).
        """

    def restart_workers(self: Any) -> None: ...
        """
        Full restart of all workers (stops everything, then starts fresh).
        
                This is the heavy-weight approach. Prefer add_camera/remove_camera/update_camera
                which use smart per-GPU restarts with debouncing.
        """

    def set_on_camera_failed(self: Any, callback: Optional[Callable[[str, str], None]]) -> None: ...
        """
        Register a callback invoked when a worker reports add_failed.
        
                The callback receives (camera_id, reason) and is expected to drop
                the phantom camera from the upstream DynamicCameraManager so the
                next periodic refresh can retry the add cleanly.
        """

    def start(self: Any) -> None: ...
        """
        Start NVDEC worker processes (one per GPU).
        
                Initializes shared multiprocessing primitives and starts a worker
                process for each GPU that has cameras assigned. If no cameras are
                configured, primitives are still created so that later add_camera
                calls can schedule per-GPU starts without a full restart.
        """

    def stop(self: Any, timeout: float = 15.0) -> None: ...
        """
        Stop all worker processes and cancel any pending restart.
        
                Args:
                    timeout: Maximum time to wait for each worker to stop gracefully
        """

    def sweep_stale_mappings(self: Any) -> int: ...
        """
        Sweep GpuCameraMap entries that don't correspond to active cameras.
        
                Active cameras are those listed in ``self.camera_configs``. Any entry
                in the persisted ``GpuCameraMap`` that isn't active AND has no
                ``/dev/shm/databus__<cam>__sg__frames`` SHM file is removed.
        
                Intended to be called on SG startup (before workers are spawned)
                and periodically thereafter as a safety net. Returns the number of
                cameras evicted.
        """

    def update_camera(self: Any, camera_config: Dict[str, Any]) -> bool: ...
        """
        Update a camera's configuration at runtime via IPC command.
        
                Args:
                    camera_config: Updated camera configuration dict
        
                Returns:
                    True if the camera was found and updated
        """

