"""Stub file for streaming_gateway.camera_streamer.nvdec directory."""
from typing import Any, Dict, List, Optional, Set, Tuple

from __future__ import annotations
from codec_detect import normalize_codec
from dataclasses import dataclass
from dataclasses import dataclass, field
from enum import Enum
from frame_optimizer import build_frame_optimizer
from gi.repository import GLib, Gst, GstRtp
from gstreamer_subprocess_demuxer import GStreamerSubprocessDemuxer
from matrice_common.diagnostics import format_table, snapshot
from matrice_common.lifecycle import finalize_cuda
from matrice_common.stream import DataBus
from matrice_common.stream.cuda_shm_ring_buffer import CudaIpcRingBuffer, GlobalFrameCounter
from matrice_common.stream.cuda_shm_ring_buffer import GlobalFrameCounter
from matrice_common.stream.databus import DataBusProducer
from matrice_common.stream.device_topology import topology
from matrice_common.stream.gpu_camera_map import GpuCameraMap
from matrice_common.utils import BenchmarkMetrics
from matrice_streaming._mp_patch import install_resource_tracker_patch
from matrice_streaming.secure_cache import is_safe_cached_file, secure_cache_dir
from matrice_streaming.url_redact import redact_url
from nvdec import CUPY_AVAILABLE, DEFAULT_OUTPUT_FPS_CAP, ORIN_NVDEC_AVAILABLE, PYNVCODEC_AVAILABLE, RING_BUFFER_AVAILABLE, StreamConfig, nvdec_pool_process
from nvdec import _get_nv12_resize_kernel
from orin_nvdec import OrinNVDECDecoderPool
from pathlib import Path
from rtp_correlation import DEFAULT_MAX_ENTRIES
from rtp_correlation import RtpPtsCorrelator
from shm_liveness import camera_has_live_shm
from shm_liveness import held_shm_paths, is_shm_path_live
from urllib.parse import urlparse, urlunparse
import PyNvVideoCodec as nvc
import argparse
import cupy as _cp
import cupy as cp
import gi
import glob
import hashlib
import importlib.util as _ilu
import json
import json as _json
import logging
import math
import multiprocessing as mp
import numpy as np
import os
import os as _os
import queue as thread_queue
import re
import requests
import select
import signal
import signal as _sig
import site
import struct
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
import uuid

# Constants
RTP_CLOCK_RATE: int = ...  # From gstreamer_rtp_demuxer
logger: Any = ...  # From gstreamer_rtp_demuxer
logger: Any = ...  # From gstreamer_subprocess_demuxer
DEFAULT_FRAME_HEIGHT: int = ...  # From nvdec
DEFAULT_FRAME_WIDTH: int = ...  # From nvdec
DEFAULT_OUTPUT_FPS_CAP: float = ...  # From nvdec
DEFAULT_SOURCE_FPS: float = ...  # From nvdec
GPU_CAMERA_MAP_AVAILABLE: bool = ...  # From nvdec
GSTREAMER_DEMUXER_AVAILABLE: bool = ...  # From nvdec
GstRTPDemuxer: None = ...  # From nvdec
ORIN_NVDEC_AVAILABLE: bool = ...  # From nvdec
logger: Any = ...  # From nvdec
CIRCUIT_BREAKER_MAX_RESTARTS: Any = ...  # From nvdec_worker_manager
CIRCUIT_BREAKER_WINDOW_SEC: Any = ...  # From nvdec_worker_manager
FRAME_STALL_THRESHOLD_SEC: Any = ...  # From nvdec_worker_manager
HOTADD_MAX_ATTEMPTS: Any = ...  # From nvdec_worker_manager
HOTADD_RETRY_BACKOFF_SEC: Any = ...  # From nvdec_worker_manager
PRODUCER_READY_TIMEOUT_SEC: Any = ...  # From nvdec_worker_manager
logger: Any = ...  # From nvdec_worker_manager
DEFAULT_SOURCE_FPS: float = ...  # From orin_nvdec
FRAME_SIZE: Any = ...  # From orin_nvdec
NV12_HEIGHT: int = ...  # From orin_nvdec
RTP_CLOCK_RATE: int = ...  # From orin_nvdec
TARGET_HEIGHT: int = ...  # From orin_nvdec
TARGET_WIDTH: int = ...  # From orin_nvdec
logger: Any = ...  # From orin_nvdec

# Functions
# From nvdec
def create_decoder_pool(pool_size: int, gpu_id: int = 0, demuxer_type: str = 'nvc', codec: str = 'h264') -> Any: ...
    """
    Create the appropriate decoder pool for the current platform.
    
        On Orin (MATRICE_PLATFORM=orin), returns OrinNVDECDecoderPool (gst-launch-1.0).
        On desktop/Thor, returns NVDECDecoderPool (PyNvVideoCodec CUVID).
    """

# From nvdec
def get_video_downloader() -> Any: ...
    """
    Get or create the global VideoDownloader instance.
    """

# From nvdec
def main() -> Any: ...

# From nvdec
def nv12_resize(y_plane: Any, uv_plane: Any, y_stride: int, uv_stride: int, src_h: int, src_w: int, dst_h: int = 0, dst_w: int = 0) -> Any: ...
    """
    Resize NV12 without color conversion.
    
        Output: concatenated Y (H*W) + UV ((H/2)*W) as single buffer.
        Total size: H*W + (H/2)*W = H*W*1.5 bytes (50% of RGB).
    """

# From nvdec
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

# From nvdec
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

# From nvdec
def setup_logging(quiet: bool = True) -> Any: ...
    """
    Configure logging level based on quiet mode.
    """

# From nvdec
def surface_to_nv12(frame: Any, target_h: int = 0, target_w: int = 0) -> Optional[cp.ndarray]: ...
    """
    Convert NVDEC surface to NV12, optionally resized.
    
        Output: (H + H/2, W, 1) uint8 - concatenated Y + UV planes with channel dim.
        Total size: H*W*1.5 bytes (vs H*W*3 for RGB).
    
        When target_h/target_w <= 0, uses the native camera resolution (no resize).
    
        Callers that need the pre-resize source dims should use
        :func:`surface_to_nv12_with_src_dims` instead.
    """

# From nvdec
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

# From nvdec_worker_manager
def get_available_gpu_count() -> int: ...
    """
    Detect the number of available CUDA GPUs.
    
        Returns:
            Number of available GPUs, or 1 if detection fails.
    """

# From nvdec_worker_manager
def is_nvdec_available() -> bool: ...
    """
    Check if NVDEC backend is available.
    
        On desktop/Thor: Requires CuPy, PyNvVideoCodec, ring buffer.
        On Orin (MATRICE_PLATFORM=orin): Requires CuPy, gst-launch-1.0, ring buffer.
        PyNvVideoCodec is NOT needed on Orin (CUVID API unavailable).
    """

# Classes
# From gstreamer_rtp_demuxer
class DemuxerType(Enum):
    """
    Demuxer backend selection.
    """

    GSTREAMER: str
    NVC: str

    pass

# From gstreamer_rtp_demuxer
class GstRTPDemuxer:
    """
    GStreamer H264 demuxer with ABSOLUTE RTP timestamp capture.
    
        For RTSP streams:
        - Captures RAW 32-bit RTP timestamps via pad probe BEFORE depayloading
        - These are the ACTUAL timestamps from the RTP packet header
        - NOT normalized like PyAV (which starts near 0 each session)
        - Timestamps persist across reconnections (monotonically increasing from source)
        - Automatically converts localhost to 127.0.0.1 to avoid IPv6 issues
        - Uses TCP by default to avoid UDP IPv6 socket issues
    
        For files:
        - Uses container PTS (presentation timestamp)
        - No RTP timestamps available
    
        Outputs H264 NAL units for external decoder (e.g., PyNvVideoCodec).
    
        Args:
            source: RTSP URL or file path
            use_tcp: Use TCP for RTSP transport (default: True, more reliable)
            loop: Loop file playback (default: False)
    """

    def __init__(self: Any, source: str, use_tcp: bool = True, loop: bool = False, codec: str = 'h264') -> None: ...

    MAX_RETRIES: int
    RETRY_DELAYS: List[Any]

    def close(self: Any) -> Any: ...
        """
        Close demuxer and release resources.
        """

    def demux(self: Any) -> Any: ...
        """
        Demux H264/H265 NAL units with timestamps.
        
                Yields:
                    (nal_bytes, timestamp, timestamp_ns, absolute_time_ns)
        
                    For RTSP:
                    - nal_bytes: H264/H265 NAL unit as bytes
                    - timestamp: RAW 32-bit RTP timestamp (ABSOLUTE, NOT normalized)
                    - timestamp_ns: RTP timestamp converted to nanoseconds (at 90kHz)
                    - absolute_time_ns: Unix time if RTCP SR available, None otherwise
        
                    For files:
                    - nal_bytes: H264/H265 NAL unit as bytes
                    - timestamp: Container PTS
                    - timestamp_ns: PTS in nanoseconds
                    - absolute_time_ns: None
        """

    def first_rtp_timestamp(self: Any) -> Optional[int]: ...
        """
        First ABSOLUTE RTP timestamp captured (RTSP only).
        """

    def fps(self: Any) -> float: ...
        """
        Video frame rate.
        """

    def frames_demuxed(self: Any) -> int: ...
        """
        Number of frames demuxed in this session.
        """

    def has_rtcp_sr(self: Any) -> bool: ...
        """
        Whether RTCP Sender Report is available for absolute time mapping.
        """

    def height(self: Any) -> int: ...
        """
        Video frame height.
        """

    def is_eof(self: Any) -> bool: ...
        """
        Whether end-of-stream has been reached.
        """

    def is_rtsp(self: Any) -> bool: ...
        """
        Whether source is RTSP stream.
        """

    def latest_rtcp_sr(self: Any) -> Optional[RTCPSenderReport]: ...
        """
        Most recent RTCP Sender Report.
        """

    def open(self: Any, quiet: bool = False) -> Any: ...
        """
        Open source and initialize demuxer pipeline with retry logic.
        
                For RTSP streams, automatically retries with TCP if UDP fails,
                and converts localhost to 127.0.0.1 to avoid IPv6 issues.
        
                Args:
                    quiet: Suppress info logging
        
                Returns:
                    self (for chaining)
        
                Raises:
                    RuntimeError: If pipeline creation fails after all retries
        """

    def rtp_correlation_stats(self: Any) -> Tuple[int, int]: ...
        """
        ``(hits, misses)`` for PTS -> RTP correlation. Diagnostics only.
        """

    def session_id(self: Any) -> str: ...
        """
        Unique session identifier.
        """

    def session_start_ns(self: Any) -> int: ...
        """
        Session start time in nanoseconds.
        """

    def width(self: Any) -> int: ...
        """
        Video frame width.
        """


# From gstreamer_rtp_demuxer
class RTCPSenderReport:
    """
    Parsed RTCP Sender Report for RTP-to-NTP time mapping.
    
        Attributes:
            ssrc: Synchronization source identifier
            ntp_timestamp: 64-bit NTP timestamp from RTCP SR
            rtp_timestamp: 32-bit RTP timestamp at SR time
            unix_time: NTP timestamp converted to Unix time
            received_at_ns: Local time when SR was received (nanoseconds)
    """

    pass

# From gstreamer_rtp_demuxer
class RTCPTracker:
    """
    Tracks RTCP Sender Reports for RTP-to-absolute-time mapping.
    
        RTCP Sender Reports provide the mapping between RTP timestamps (at 90kHz)
        and absolute wall-clock time (NTP). This allows converting any RTP timestamp
        to Unix time for cross-camera synchronization.
    """

    def __init__(self: Any, clock_rate: int = RTP_CLOCK_RATE) -> None: ...

    NTP_UNIX_EPOCH_DIFF: int

    def has_sender_report(self: Any) -> bool: ...
        """
        Check if at least one RTCP Sender Report has been received.
        """

    def latest_sr(self: Any) -> Optional[RTCPSenderReport]: ...
        """
        Get the most recent RTCP Sender Report.
        """

    def rtp_to_unix_ns(self: Any, rtp_timestamp: int) -> Optional[int]: ...
        """
        Convert RTP timestamp to absolute Unix time in nanoseconds.
        
                Uses the most recent RTCP Sender Report to map RTP timestamps to
                absolute wall-clock time. Handles 32-bit RTP timestamp rollover.
        
                Args:
                    rtp_timestamp: 32-bit RTP timestamp to convert
        
                Returns:
                    Unix time in nanoseconds, or None if no SR available
        """

    def update_from_session_stats(self: Any, stats_str: str, ssrc: int) -> Optional[RTCPSenderReport]: ...
        """
        Parse RTCP SR from GStreamer session stats.
        
                Args:
                    stats_str: GStreamer stats structure as string
                    ssrc: Source SSRC identifier
        
                Returns:
                    RTCPSenderReport if valid SR found, None otherwise
        """


# From gstreamer_subprocess_demuxer
class GStreamerSubprocessDemuxer:
    """
    GStreamer demuxer that runs in a subprocess to avoid FFmpeg conflicts.
    
        Drop-in replacement for GstRTPDemuxer with the same interface:
        - open() / close()
        - demux() generator yielding (nal_bytes, rtp_ts, rtp_ts_ns, absolute_ns)
        - Properties: width, height, fps, session_id, first_rtp_timestamp
    """

    def __init__(self: Any, video_path: str, use_tcp: bool = True, codec: str = 'h264') -> None: ...

    def close(self: Any) -> None: ...
        """
        Stop the subprocess and clean up all resources.
        """

    def demux(self: Any) -> Any: ...
        """
        Yield (nal_bytes, rtp_ts, rtp_ts_ns, absolute_ns) from subprocess.
        """

    def open(self: Any, quiet: bool = True) -> None: ...
        """
        Start the GStreamer subprocess and wait for metadata.
        
                Retries up to 5 times with exponential backoff to handle transient
                RTSP source unavailability (e.g., video storage restart).
        """

    def restart(self: Any) -> None: ...
        """
        Restart the demuxer (reconnect to RTSP).
        """


# From nvdec
class DemuxerType(Enum):
    """
    Demuxer backend selection.
    
        NVC: PyNvVideoCodec demuxer - fastest for local files
        GSTREAMER: GStreamer demuxer - provides ABSOLUTE RTP timestamps for RTSP
    """

    GSTREAMER: str
    NVC: str

    pass

# From nvdec
class GatewayConfig:
    """
    Configuration for the streaming gateway.
    """

    pass

# From nvdec
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


# From nvdec
class StreamConfig:
    """
    Configuration for a single video stream.
    """

    pass

# From nvdec
class StreamState:
    """
    Track state for each logical stream in NVDEC pool.
    """

    pass

# From nvdec
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


# From nvdec
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


# From nvdec_worker_manager
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
                    True if the camera was found and removed
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


# From orin_nvdec
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


# From orin_nvdec
class OrinStreamState:
    """
    State for a Python GStreamer subprocess camera stream.
    """

    pass

from . import gstreamer_rtp_demuxer, gstreamer_subprocess_demuxer, nvdec, nvdec_worker_manager, orin_nvdec