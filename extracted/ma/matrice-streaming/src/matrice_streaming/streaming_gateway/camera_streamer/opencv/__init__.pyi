"""Stub file for streaming_gateway.camera_streamer.opencv directory."""
from typing import Any, Dict, List, Optional, Tuple, Union

from  import frame_processor
from __future__ import annotations
from async_camera_worker import run_async_worker
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from constants import DEFAULT_OPENCV_OPTIMIZATION_MODE
from databus_backpressure import BackpressurePublisher
from frame_optimizer import build_frame_optimizer
from frame_pool import GatewayFramePool
from matrice_common.lifecycle import finalize_cuda
from matrice_common.stream import DataBus
from matrice_common.stream.databus import DataBusProducer
from matrice_streaming.secure_cache import is_safe_cached_file, secure_cache_dir
from matrice_streaming.url_redact import redact_url
from pathlib import Path
from shm_liveness import held_shm_paths, is_shm_path_live
from urllib.parse import urlparse, urlunparse
from video_capture_manager import VideoCaptureManager
import asyncio
import atexit
import cv2
import glob
import hashlib
import logging
import multiprocessing
import numpy as np
import os
import psutil
import queue
import requests
import signal
import sys
import tempfile
import threading
import time

# Functions
# From async_camera_worker
def run_async_worker(worker_id: int, camera_configs: List[Dict[str, Any]], stop_event: Any, health_queue: Any, command_queue: Optional[Any] = None, response_queue: Optional[Any] = None, jpeg_encode: bool = True, jpeg_quality: int = 90, num_slots: int = 32, max_msg_size: int = 300000, optimizer_config: Optional[Dict[str, Any]] = None, use_frame_pool: bool = False, use_backpressure: bool = False, use_executor_publish: bool = False) -> Any: ...
    """
    Entry point for async worker process (called by multiprocessing.Process).
    """

# From frame_processor
def actual_dimensions(video_width: int, video_height: int, target_width: Optional[int], target_height: Optional[int]) -> Tuple[int, int]: ...
    """
    Return the output (width, height): the target if set, else the source size.
    """

# From frame_processor
def pool_exhausted_total() -> int: ...

# From frame_processor
def resize_frame(frame: Any, target_width: Optional[int], target_height: Optional[int]) -> Any: ...
    """
    Resize a frame with letterbox padding, preserving aspect ratio.
    
        Matches ultralytics LetterBox preprocessing: scale to fit within the target
        dimensions, then pad with gray (114) to reach the exact target size. Returns
        the original frame unchanged if no resize is needed.
    """

# From frame_processor
def set_use_frame_pool(enabled: bool) -> None: ...
    """
    Toggle pooled letterbox canvases (used by WorkerManager optimization modes).
    """

# From worker_manager
def resolve_opencv_optimization_mode(explicit: Optional[str] = None) -> str: ...
    """
    Resolve OpenCV optimization mode (REFACTORING_PLAN §20 — evidence-only, opt-in).
    
        Default is ``none`` (prior behavior). Override via constructor or
        ``MATRICE_SG_OPENCV_OPTIM``. ``combined`` enables frame_pool + backpressure
        only; ``executor_offload`` is separate (plan excludes added postproc threads
        from combined/default paths).
    """

# Classes
# From async_camera_worker
class AsyncCameraWorker:
    """
    Async worker that captures frames via OpenCV and publishes to DataBus.
    
        Runs an async event loop to handle multiple cameras concurrently. Frames are
        JPEG-encoded (default) and published to POSIX SHM via DataBus, using the same
        address scheme as the NVDEC path: ``/dev/shm/databus__{camera_id}__sg__frames``.
    """

    def __init__(self: Any, worker_id: int, camera_configs: List[Dict[str, Any]], stop_event: Any, health_queue: Any, command_queue: Optional[Any] = None, response_queue: Optional[Any] = None, jpeg_encode: bool = True, jpeg_quality: int = 90, num_slots: int = 32, max_msg_size: int = 300000, optimizer_config: Optional[Dict[str, Any]] = None, use_frame_pool: bool = False, use_backpressure: bool = False, use_executor_publish: bool = False) -> None: ...

    async def initialize(self: Any) -> Any: ...
        """
        Initialize async resources.
        """

    async def run(self: Any) -> Any: ...
        """
        Main worker loop.
        """


# From video_capture_manager
class VideoCaptureManager:
    """
    Manages video capture from various sources with retry logic and caching.
    
        Features URL deduplication: if multiple cameras use the same video URL
        (ignoring query parameters like AWS signed URL tokens), the video is only
        downloaded once and the local path is shared between cameras.
    """

    def __init__(self: Any) -> None: ...
        """
        Initialize video capture manager.
        """

    def cleanup(self: Any) -> None: ...
        """
        Clean up downloaded temporary files.
        """

    def get_video_properties(self: Any, cap: Any) -> Dict[str, Any]: ...
        """
        Extract video properties from capture.
        
                Args:
                    cap: VideoCapture object
        
                Returns:
                    Dictionary with video properties
        """

    def open_capture(self: Any, source: Union[str, int], width: Optional[int] = None, height: Optional[int] = None) -> Tuple[cv2.VideoCapture, str]: ...
        """
        Open video capture with retry logic.
        
                Args:
                    source: Video source
                    width: Target width for camera
                    height: Target height for camera
        
                Returns:
                    Tuple of (VideoCapture object, source_type)
        
                Raises:
                    RuntimeError: If unable to open capture after retries
        """

    def prepare_source(self: Any, source: Union[str, int], stream_key: str) -> Union[str, int]: ...
        """
        Prepare video source, downloading if it's a URL.
        
                Args:
                    source: Video source (camera index, file path, or URL)
                    stream_key: Stream identifier for caching
        
                Returns:
                    Prepared source (downloaded file path or original source)
        """


# From video_capture_manager
class VideoSourceConfig:
    """
    Configuration for video source handling.
    """

    pass

# From worker_manager
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


from . import async_camera_worker, frame_processor, video_capture_manager, worker_manager