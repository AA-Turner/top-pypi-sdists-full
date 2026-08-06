"""Auto-generated stub for module: gateway_builder."""
from typing import Any, Dict, Optional

from __future__ import annotations
from matrice_streaming.streaming_gateway.camera_streamer.nvdec.nvdec_worker_manager import NVDECWorkerManager, is_nvdec_available
from matrice_streaming.streaming_gateway.camera_streamer.opencv.worker_manager import WorkerManager
from matrice_streaming.streaming_gateway.streaming_gateway import KafkaConsumerWatchdog
import logging

# Constants
log: Any

# Functions
def build_kafka_watchdog(event_listener: Any, is_active_fn: Any, **kwargs: Any) -> Any: ...
    """
    Build a KafkaConsumerWatchdog for the given event listener.
    """
def build_nvdec_backend(camera_configs: Any, stream_config: Any, gpu_id: int = 0, num_gpus: int = 0, nvdec_pool_size: int = 8, nvdec_burst_size: Optional[int] = None, frame_width: int = 0, frame_height: int = 0, num_slots: int = 64, target_fps: int = 0, output_fps_cap: Optional[float] = None, optimizer_config: Optional[Dict[str, Any]] = None, demuxer_type: str = 'gstreamer', tampering_config: Optional[Dict[str, Any]] = None, manager_cls: Optional[Any] = None) -> Any: ...
    """
    Build and return an NVDECWorkerManager if NVDEC is available.
    
        Returns None only when NVDEC hardware/drivers are not installed (ImportError
        or is_nvdec_available() → False). If NVDEC is available but initialisation
        fails, the exception propagates — matching prod's fail-loud behaviour so a
        broken GPU configuration is never silently swallowed.
    """
def build_opencv_backend(camera_configs: Any, num_workers: Any, max_cameras_per_worker: int, num_slots: int = 32, tampering_config: Optional[Dict[str, Any]] = None, manager_cls: Optional[Any] = None) -> Any: ...
    """
    Build and return an OpenCV WorkerManager.
    
        Args:
            manager_cls: WorkerManager class to instantiate. Callers pass their own
                module-level reference so that patching it (e.g.
                ``patch("...streaming_gateway.WorkerManager")``) still intercepts
                construction — a function-local import here would bypass such
                patches and let unit tests spawn real worker subprocesses.
                Defaults to the real class.
    """
