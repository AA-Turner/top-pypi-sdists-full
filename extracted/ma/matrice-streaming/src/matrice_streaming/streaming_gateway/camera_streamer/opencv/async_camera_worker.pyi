"""Auto-generated stub for module: async_camera_worker."""
from typing import Any, Dict, List, Optional, Tuple

from  import frame_processor
from __future__ import annotations
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from databus_backpressure import BackpressurePublisher
from frame_optimizer import build_frame_optimizer
from matrice_common.lifecycle import finalize_cuda
from matrice_common.stream import DataBus
from matrice_common.stream.databus import DataBusProducer
from video_capture_manager import VideoCaptureManager
import asyncio
import atexit
import cv2
import logging
import os
import psutil
import queue
import time

# Functions
def run_async_worker(worker_id: int, camera_configs: List[Dict[str, Any]], stop_event: Any, health_queue: Any, command_queue: Optional[Any] = None, response_queue: Optional[Any] = None, jpeg_encode: bool = True, jpeg_quality: int = 90, num_slots: int = 32, max_msg_size: int = 300000, optimizer_config: Optional[Dict[str, Any]] = None, use_frame_pool: bool = False, use_backpressure: bool = False, use_executor_publish: bool = False) -> Any: ...
    """
    Entry point for async worker process (called by multiprocessing.Process).
    """

# Classes
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

