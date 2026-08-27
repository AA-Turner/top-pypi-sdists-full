"""Auto-generated stub for module: worker_manager."""
from typing import Any, Dict, List, Optional

from __future__ import annotations
from async_camera_worker import run_async_worker
from constants import DEFAULT_IPC_COMMAND_QUEUE_MAXSIZE, DEFAULT_IPC_RESULT_QUEUE_MAXSIZE, DEFAULT_IPC_STATUS_QUEUE_MAXSIZE, DEFAULT_OPENCV_OPTIMIZATION_MODE
from shm_liveness import held_shm_paths, is_shm_path_live
import glob
import logging
import multiprocessing
import os
import queue
import signal
import sys
import threading
import time

# Functions
def resolve_opencv_optimization_mode(explicit: Optional[str] = None) -> str: ...
    """
    Resolve OpenCV optimization mode (REFACTORING_PLAN §20 — evidence-only, opt-in).
    
        Default is ``none`` (prior behavior). Override via constructor or
        ``MATRICE_SG_OPENCV_OPTIM``. ``combined`` enables frame_pool + backpressure
        only; ``executor_offload`` is separate (plan excludes added postproc threads
        from combined/default paths).
    """

# Classes
class WorkerManager:
    """
    Manages multiple async camera worker processes with dynamic scaling.
    
        Each worker handles multiple cameras concurrently using async I/O.
        Frames are published to DataBus SHM ring buffers, matching the NVDEC
        architecture — the only difference is the decoder (OpenCV vs NVDEC).
    """

    def __init__(self: Any, camera_configs: List[Dict[str, Any]], num_workers: Optional[int] = None, cpu_percentage: float = 0.9, max_cameras_per_worker: int = 100, jpeg_encode: bool = True, jpeg_quality: int = 90, num_slots: int = 32, max_msg_size: int = 300000, optimizer_config: Optional[Dict[str, Any]] = None, optimization_mode: Optional[str] = None) -> None: ...

    def add_camera(self: Any, camera_config: Dict[str, Any]) -> bool: ...
        """
        Add a camera to the least-loaded worker at runtime.
        """

    def get_camera_assignments(self: Any) -> Dict[str, int]: ...

    def get_worker_statistics(self: Any) -> Dict[str, Any]: ...
        """
        Return the last cached health snapshot without draining the queue.
        """

    def monitor(self: Any, duration: Optional[float] = None) -> Any: ...
        """
        Monitor workers and collect health reports.
        """

    def remove_camera(self: Any, stream_key: str) -> bool: ...
        """
        Remove a camera from its assigned worker.
        """

    def run(self: Any, duration: Optional[float] = None) -> Any: ...
        """
        Start workers and monitor until stopped.
        """

    def start(self: Any) -> Any: ...
        """
        Start all workers and begin streaming.
        """

    def stop(self: Any, timeout: float = 15.0) -> Any: ...
        """
        Stop all workers gracefully.
        """

    def update_camera(self: Any, camera_config: Dict[str, Any]) -> bool: ...
        """
        Update a camera's configuration.
        """

