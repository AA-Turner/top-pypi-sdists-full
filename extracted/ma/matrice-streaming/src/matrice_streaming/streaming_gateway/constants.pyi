"""Auto-generated stub for module: constants."""
from typing import Any, Tuple

from __future__ import annotations
from enum import Enum

# Constants
DEFAULT_CAMERA_FPS: int
DEFAULT_CAMERA_HEIGHT: int
DEFAULT_CAMERA_QUALITY: int
DEFAULT_CAMERA_WIDTH: int
DEFAULT_CONNECTION_TIMEOUT: int
DEFAULT_IPC_COMMAND_QUEUE_MAXSIZE: int
DEFAULT_IPC_RESULT_QUEUE_MAXSIZE: int
DEFAULT_IPC_STATUS_QUEUE_MAXSIZE: int
DEFAULT_MEDIAMTX_PORT: int
DEFAULT_NVDEC_NUM_SLOTS: int
DEFAULT_OPENCV_OPTIMIZATION_MODE: str
DEFAULT_OUTPUT_FPS_CAP: float
DEFAULT_STREAM_FPS: Any
DEFAULT_STREAM_WH: Tuple[Any, ...]
DEFAULT_WORKER_STOP_TIMEOUT: float

# Classes
class GatewayStatus(str, Enum):
    """
    Status values for the streaming gateway lifecycle.
    """

    INITIALIZED: str
    RUNNING: str
    STOPPED: str
    STOPPING: str

    pass
