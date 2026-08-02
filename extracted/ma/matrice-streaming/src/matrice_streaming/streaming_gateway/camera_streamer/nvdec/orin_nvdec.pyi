"""Auto-generated stub for module: orin_nvdec."""
from typing import Any, Dict, List, Optional, Tuple

from __future__ import annotations
from codec_detect import normalize_codec
from dataclasses import dataclass, field
import cupy as cp
import json
import logging
import math
import numpy as np
import os
import select
import signal
import struct
import subprocess
import sys
import tempfile
import threading
import time
import uuid

# Constants
DEFAULT_SOURCE_FPS: float
FRAME_SIZE: Any
NV12_HEIGHT: int
RTP_CLOCK_RATE: int
TARGET_HEIGHT: int
TARGET_WIDTH: int
logger: Any

# Classes
class OrinNVDECDecoderPool:
    """
    Orin-compatible NVDEC decoder pool using Python GStreamer subprocesses.
    
        Drop-in replacement for NVDECDecoderPool on Jetson Orin where CUVID API
        is not available. Uses a Python subprocess per camera with GStreamer
        pipeline + pad probes for RTP timestamp extraction.
    
        API matches NVDECDecoderPool exactly:
            - assign_stream(stream_id, camera_id, video_path, ...)
            - decode_round(decoder_idx, frames_per_stream) -> (total, [(cam, tensor, ts, ...)])
            - get_camera_ids_for_decoder(decoder_idx)
            - get_source_fps_for_decoder(decoder_idx)
            - release()
    """

    def __init__(self: Any, pool_size: int, gpu_id: int = 0, demuxer_type: str = 'gstreamer', codec: str = 'h264') -> None: ...

    def assign_stream(self: Any, stream_id: int, camera_id: str, video_path: str, width: int = TARGET_WIDTH, height: int = TARGET_HEIGHT, stream_type: str = 'file', demuxer_type: str = None, codec: str = None) -> bool: ...
        """
        Assign a camera stream and start its subprocess.
        """

    def close(self: Any) -> Any: ...
        """
        Close all decoders (API compat with NVDECDecoderPool).
        """

    def decode_round(self: Any, decoder_idx: int, frames_per_stream: int = 4, target_h: int = TARGET_HEIGHT, target_w: int = TARGET_WIDTH, benchmark_metrics: Any = None) -> Tuple[int, List[Tuple[str, Any, int, str, str, int, Optional[int]]]]: ...
        """
        Decode frames from all streams assigned to this decoder slot.
        
                Returns same format as NVDECDecoderPool.decode_round:
                    (total_frames, [(camera_id, nv12_tensor, timestamp_ns,
                                     stream_type, session_id, session_start_ns, rtp_timestamp), ...])
        """

    def get_camera_ids_for_decoder(self: Any, decoder_idx: int) -> List[str]: ...
        """
        Get camera IDs assigned to a decoder slot.
        """

    def get_source_fps_for_decoder(self: Any, decoder_idx: int) -> float: ...
        """
        Get average source FPS for streams on this decoder.
        """

    def release(self: Any) -> Any: ...
        """
        Stop all subprocess pipelines.
        """

class OrinStreamState:
    """
    State for a Python GStreamer subprocess camera stream.
    """

    pass
