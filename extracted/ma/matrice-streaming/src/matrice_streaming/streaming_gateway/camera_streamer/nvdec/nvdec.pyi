"""Auto-generated stub for module: nvdec."""
from typing import Any, Dict, List, Optional, Set, Tuple

from __future__ import annotations
from codec_detect import normalize_codec
from codec_detect import normalize_codec
from dataclasses import dataclass
from enum import Enum
from frame_optimizer import build_frame_optimizer
from gstreamer_subprocess_demuxer import GStreamerSubprocessDemuxer
from gstreamer_subprocess_demuxer import GStreamerSubprocessDemuxer
from matrice_common.lifecycle import finalize_cuda
from matrice_common.stream import DataBus
from matrice_common.stream.cuda_shm_ring_buffer import CudaIpcRingBuffer, GlobalFrameCounter
from matrice_common.stream.databus import DataBusProducer
from matrice_common.utils import BenchmarkMetrics
from matrice_streaming._mp_patch import install_resource_tracker_patch
from matrice_streaming.secure_cache import is_safe_cached_file, secure_cache_dir
from matrice_streaming.url_redact import redact_url
from orin_nvdec import OrinNVDECDecoderPool
from orin_nvdec import OrinNVDECDecoderPool
from pathlib import Path
from urllib.parse import urlparse, urlunparse
import PyNvVideoCodec as nvc
import argparse
import cupy as cp
import hashlib
import logging
import math
import multiprocessing as mp
import numpy as np
import os
import queue as thread_queue
import requests
import tempfile
import threading
import time
import uuid

# Constants
DEFAULT_FRAME_HEIGHT: int
DEFAULT_FRAME_WIDTH: int
DEFAULT_OUTPUT_FPS_CAP: float
DEFAULT_SOURCE_FPS: float
GPU_CAMERA_MAP_AVAILABLE: bool
GSTREAMER_DEMUXER_AVAILABLE: bool
GstRTPDemuxer: None
ORIN_NVDEC_AVAILABLE: bool
logger: Any

# Functions
def create_decoder_pool(pool_size: int, gpu_id: int = 0, demuxer_type: str = 'nvc', codec: str = 'h264') -> Any: ...
    """
    Create the appropriate decoder pool for the current platform.
    
        On Orin (MATRICE_PLATFORM=orin), returns OrinNVDECDecoderPool (gst-launch-1.0).
        On desktop/Thor, returns NVDECDecoderPool (PyNvVideoCodec CUVID).
    """
def get_video_downloader() -> Any: ...
    """
    Get or create the global VideoDownloader instance.
    """
def main() -> Any: ...
def nv12_resize(y_plane: Any, uv_plane: Any, y_stride: int, uv_stride: int, src_h: int, src_w: int, dst_h: int = 0, dst_w: int = 0) -> Any: ...
    """
    Resize NV12 without color conversion.
    
        Output: concatenated Y (H*W) + UV ((H/2)*W) as single buffer.
        Total size: H*W + (H/2)*W = H*W*1.5 bytes (50% of RGB).
    """
def nvdec_pool_process(process_id: int, camera_configs: List[StreamConfig], pool_size: int, duration_sec: float, result_queue: Any, stop_event: Any, burst_size: Optional[int] = None, num_slots: int = 64, target_fps: int = 0, shared_frame_count: Optional[mp.Value] = None, gpu_frame_counts: Optional[Dict[int, mp.Value]] = None, total_num_streams: int = 0, total_num_gpus: int = 1, demuxer_type: str = 'nvc', benchmark_mode: bool = False, command_queue: Optional[mp.Queue] = None, worker_status_queue: Optional[mp.Queue] = None, optimizer_config: Optional[Dict[str, Any]] = None, output_fps_cap: float = DEFAULT_OUTPUT_FPS_CAP) -> Any: ...
    """
    NVDEC process for one GPU.
    
        Creates NV12 ring buffers: (H*1.5, W) = 0.6 MB/frame.
    
        Args:
            gpu_frame_counts: Dict mapping gpu_id -> per-GPU frame counter (for per-GPU stats)
            shared_frame_count: Global frame counter (for overall stats)
            total_num_streams: Total streams across ALL GPUs (for global per-stream calc)
            total_num_gpus: Total number of GPUs (for context in logging)
            demuxer_type: Demuxer backend ("nvc" or "gstreamer")
            benchmark_mode: Enable granular per-stage timing
    """
def nvdec_pool_worker(worker_id: int, decoder_idx: int, pool: Any, ring_buffers: Dict[str, DataBusProducer], frame_counter: Any, duration_sec: float, result_queue: Any, stop_event: Any, burst_size: Optional[int] = None, target_h: int = 0, target_w: int = 0, target_fps: int = 0, shared_frame_count: Optional[mp.Value] = None, gpu_frame_count: Optional[mp.Value] = None, lazy_rb_cameras: Optional[set] = None, num_slots: int = 64, benchmark_mode: bool = False, worker_status_queue: Optional[Any] = None, optimizer_config: Optional[Dict[str, Any]] = None, output_fps_cap: float = DEFAULT_OUTPUT_FPS_CAP, publish_fps_by_camera: Optional[Dict[str, float]] = None) -> Any: ...
    """
    NVDEC worker thread.
    
        Decodes frames and writes NV12 tensors to ring buffers.
        Uses dedicated CUDA stream per worker for kernel overlap.
        Supports FPS limiting when target_fps > 0.
    
        F08: ``publish_fps_by_camera`` maps camera_id -> the aggregated per-camera
        publish rate (``max(app min_fps)``). When a camera has a positive entry it
        overrides the worker-global ``output_fps_cap`` for that camera's publish
        decimator; otherwise the global cap (``MATRICE_OUTPUT_FPS``) applies.
    
        Args:
            shared_frame_count: Global counter (all GPUs)
            gpu_frame_count: Per-GPU counter (this GPU only)
            benchmark_mode: Enable granular per-stage timing
    """
def setup_logging(quiet: bool = True) -> Any: ...
    """
    Configure logging level based on quiet mode.
    """
def surface_to_nv12(frame: Any, target_h: int = 0, target_w: int = 0) -> Optional[cp.ndarray]: ...
    """
    Convert NVDEC surface to NV12, optionally resized.
    
        Output: (H + H/2, W, 1) uint8 - concatenated Y + UV planes with channel dim.
        Total size: H*W*1.5 bytes (vs H*W*3 for RGB).
    
        When target_h/target_w <= 0, uses the native camera resolution (no resize).
    
        Callers that need the pre-resize source dims should use
        :func:`surface_to_nv12_with_src_dims` instead.
    """
def surface_to_nv12_with_src_dims(frame: Any, target_h: int = 0, target_w: int = 0) -> Tuple[Optional[cp.ndarray], int, int]: ...
    """
    Convert NVDEC surface to NV12 and return the pre-resize source dims.
    
        Same output format as :func:`surface_to_nv12` but also returns the
        ORIGINAL (pre-resize) source dimensions read off the NVDEC surface.
        Consumers (inference) need these to invert the letterbox geometry so
        bounding boxes in model-input space map back to source pixel space.
    
        Returns:
            (tensor, src_w, src_h) where tensor is the NV12 frame (or None on
            failure) and (src_w, src_h) are the native camera resolution.
            (None, 0, 0) on any failure path.
    """

# Classes
class DemuxerType(Enum):
    """
    Demuxer backend selection.
    
        NVC: PyNvVideoCodec demuxer - fastest for local files
        GSTREAMER: GStreamer demuxer - provides ABSOLUTE RTP timestamps for RTSP
    """

    GSTREAMER: str
    NVC: str

    pass
class GatewayConfig:
    """
    Configuration for the streaming gateway.
    """

    pass
class NVDECDecoderPool:
    """
    Pool of NVDEC decoders that time-multiplex streams.
    
        Each decoder is exclusively owned by one worker thread.
        Outputs NV12: 1.5*H*W bytes (50% smaller than RGB).
    
        Supports two demuxer backends:
        - NVC (default): PyNvVideoCodec demuxer, fastest for local files
        - GStreamer: Provides ABSOLUTE RTP timestamps for RTSP streams
    
        KNOWN ISSUE — Resolution Mismatch Crash (SIGABRT):
            NVDEC decoders are created with an implicit max resolution based on the
            first stream they decode. If a camera with a HIGHER resolution than the
            initial streams is later assigned to the same GPU (e.g., a 1280x720 camera
            mixed with 640x360 cameras), PyNvVideoCodec's C++ layer calls
            ReconfigureDecoder which fails with:
                "Error code 801: Reconfigure Not supported when width/height >
                 maxwidth/maxheight" (NvDecoder.cpp:462)
            This triggers SIGABRT, killing the entire GPU worker process and all
            cameras on that GPU.
    
            Root cause: nvc.CreateDecoder() does not accept maxWidth/maxHeight params
            in the current PyNvVideoCodec version. The decoder auto-sizes to the first
            stream's resolution.
    
        TODO: Fix resolution mismatch by either:
            1. Creating decoders with max expected resolution (e.g., 1920x1080) by
               decoding a dummy frame of that size during initialization
            2. Catching the reconfigure error and recreating the decoder with the
               new resolution (requires decoder-level try/except around Decode())
            3. Grouping cameras by resolution into separate decoder pools
            4. Validating camera resolution against decoder max before assign_stream()
               and rejecting mismatched cameras with a clear error message
    """

    def __init__(self: Any, pool_size: int, gpu_id: int = 0, demuxer_type: str = 'nvc', codec: str = 'h264') -> None: ...

    def assign_stream(self: Any, stream_id: int, camera_id: str, video_path: str, width: int = 0, height: int = 0, stream_type: str = 'file', demuxer_type: str = None, codec: str = None) -> bool: ...
        """
        Assign a stream to a decoder (round-robin).
        
                Supports two demuxer backends:
                - NVC: PyNvVideoCodec demuxer (fastest for files)
                - GStreamer: Provides ABSOLUTE RTP timestamps for RTSP
        
                Args:
                    stream_id: Stream identifier
                    camera_id: Camera identifier
                    video_path: Video file path or RTSP URL
                    width: Target width
                    height: Target height
                    stream_type: Source type ("file" or "rtsp")
                    demuxer_type: Override demuxer type ("nvc" or "gstreamer"), uses pool default if None
                    codec: Video codec ("h264" or "h265"), uses pool codec if None
        """

    def close(self: Any) -> Any: ...
        """
        Close all decoders and demuxers.
        """

    def decode_round(self: Any, decoder_idx: int, frames_per_stream: int = 4, target_h: int = 0, target_w: int = 0, benchmark_metrics: Any = None) -> Tuple[int, List[Tuple[str, cp.ndarray, int, str, str, int, Optional[int], int, int]]]: ...
        """
        Decode frames and convert to NV12.
        
                Supports two demuxer backends:
                - NVC: PyNvVideoCodec demuxer (fastest for local files)
                - GStreamer: Provides ABSOLUTE RTP timestamps for RTSP streams
        
                Returns:
                    (total_frames, [(camera_id, nv12_tensor, timestamp_ns, stream_type, session_id, session_start_ns, rtp_timestamp), ...])
                    where:
                    - timestamp_ns: For RTSP = T0 + PTS (absolute wall clock ns), for files = PTS (video-relative ns)
                    - stream_type: "rtsp" or "file"
                    - session_id: 8-char unique ID for RTSP (changes on reconnect), empty for files
                    - session_start_ns: T0 wall clock when RTSP connected (0 for files)
                    - rtp_timestamp: ABSOLUTE 32-bit RTP timestamp (GStreamer only, None for NVC)
        """

    def get_camera_ids_for_decoder(self: Any, decoder_idx: int) -> List[str]: ...
        """
        Get camera IDs for a decoder.
        """

    def get_source_fps_for_camera(self: Any, camera_id: str) -> float: ...
        """
        Detected source FPS for one camera (for the publish-rate decimator).
        
                Falls back to ``DEFAULT_SOURCE_FPS`` when the camera is unknown so the
                decimator fails open at a sane rate rather than dividing by zero.
        """

    def get_source_fps_for_decoder(self: Any, decoder_idx: int) -> float: ...
        """
        Get average source FPS for streams assigned to a decoder.
        
                Used when target_fps=0 to cap output to source video rate.
        """

    def remove_stream(self: Any, camera_id: str) -> bool: ...
        """
        Remove a specific stream by camera_id, closing its demuxer resources.
        """

class StreamConfig:
    """
    Configuration for a single video stream.
    """

    pass
class StreamState:
    """
    Track state for each logical stream in NVDEC pool.
    """

    pass
class StreamingGateway:
    """
    Multi-stream video producer outputting NV12 tensors (minimal IPC payload).
    """

    def __init__(self: Any, config: Any) -> None: ...

    def start(self: Any) -> Dict: ...
        """
        Start the gateway.
        """

    def stop(self: Any) -> Any: ...
        """
        Stop all workers.
        """

class VideoDownloader:
    """
    Downloads and caches video files from HTTPS URLs.
    
        PyNvVideoCodec uses a bundled FFmpeg that doesn't have HTTPS support.
        This class downloads HTTPS videos to local files before passing them
        to the NVDEC demuxer.
    
        Features:
        - URL deduplication: same video URL (ignoring query params) is only downloaded once
        - Disk caching: reuses existing files across runs
        - Progress tracking for large files
        - Dynamic timeout based on file size
    """

    def __init__(self: Any) -> None: ...
        """
        Initialize the video downloader.
        """

    def cleanup(self: Any) -> None: ...
        """
        Clean up downloaded temporary files.
        """

    def prepare_source(self: Any, video_path: str, camera_id: str) -> str: ...
        """
        Prepare video source, downloading HTTPS URLs if needed.
        
                Args:
                    video_path: Video file path, RTSP URL, or HTTPS URL
                    camera_id: Camera identifier for logging
        
                Returns:
                    Local file path (downloaded if HTTPS) or original path
        """

