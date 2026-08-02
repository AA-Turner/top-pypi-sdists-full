# CRITICAL: Initialize GStreamer and remove gst-libav BEFORE any other imports.
# PyNvVideoCodec bundles FFmpeg 6.x (libavcodec.so.61), while GStreamer's gst-libav
# plugin uses system FFmpeg 4.4 (libavcodec.so.58). When both are loaded in the same
# process, rtspsrc triggers a SIGABRT/SIGSEGV due to symbol collision.
#
# Fix: Remove gst-libav from GStreamer's plugin registry so it never loads system FFmpeg.
# This is safe because our pipeline (rtspsrc -> rtph264depay -> h264parse -> appsink)
# doesn't need gst-libav — it only needs RTP/RTSP and H264 parsing plugins.
try:
    import gi

    gi.require_version("Gst", "1.0")
    gi.require_version("GstRtp", "1.0")
    gi.require_version("GstApp", "1.0")
    from gi.repository import Gst

    Gst.init(None)

    # Remove gst-libav to prevent FFmpeg 4.4 vs 6.x symbol conflict with PyNvVideoCodec
    _registry = Gst.Registry.get()
    _libav = _registry.find_plugin("libav")
    if _libav:
        _registry.remove_plugin(_libav)
    del _registry, _libav
except (ImportError, ValueError):
    pass

from .databus_backpressure import BackpressurePublisher
from .frame_optimizer import (
    FrameOptimizer,
    MotionFrameOptimizer,
    NoOpFrameOptimizer,
    build_frame_optimizer,
)
from .frame_pool import GatewayFramePool
from .opencv.async_camera_worker import AsyncCameraWorker
from .opencv.worker_manager import WorkerManager

# NVDEC components (optional - graceful import)
try:
    from .nvdec.nvdec import ORIN_NVDEC_AVAILABLE, DemuxerType
    from .nvdec.nvdec_worker_manager import (
        NVDECWorkerManager,
        get_available_gpu_count,
        is_nvdec_available,
    )

    NVDEC_AVAILABLE = is_nvdec_available()
except (ImportError, AttributeError, RuntimeError, TypeError, ValueError):
    # NVDEC not available (requires CuPy, PyNvVideoCodec, cuda_shm_ring_buffer)
    # Suppress warnings - these are optional dependencies
    NVDEC_AVAILABLE = False
    ORIN_NVDEC_AVAILABLE = False  # type: ignore[assignment]
    NVDECWorkerManager = None  # type: ignore[assignment, misc]
    DemuxerType = None  # type: ignore[assignment, misc]

    def is_nvdec_available():  # type: ignore[misc]
        return False

    def get_available_gpu_count():  # type: ignore[misc]
        return 1


# GStreamer RTP Demuxer (optional - for ABSOLUTE RTP timestamps, used by NVDEC)
try:
    from .nvdec.gstreamer_rtp_demuxer import (
        GstRTPDemuxer,
        RTCPSenderReport,
        RTCPTracker,
    )

    GST_RTP_DEMUXER_AVAILABLE = True
except (ImportError, ValueError, AttributeError, RuntimeError, TypeError):
    # GStreamer RTP demuxer not available
    GST_RTP_DEMUXER_AVAILABLE = False
    GstRTPDemuxer = None  # type: ignore[assignment, misc]
    RTCPSenderReport = None  # type: ignore[assignment, misc]
    RTCPTracker = None  # type: ignore[assignment, misc]

__all__ = [
    # Core components
    "WorkerManager",
    "AsyncCameraWorker",
    # Frame-skip optimization
    "FrameOptimizer",
    "MotionFrameOptimizer",
    "NoOpFrameOptimizer",
    "build_frame_optimizer",
    "GatewayFramePool",
    "BackpressurePublisher",
    # NVDEC components
    "NVDECWorkerManager",
    "is_nvdec_available",
    "get_available_gpu_count",
    "NVDEC_AVAILABLE",
    "ORIN_NVDEC_AVAILABLE",
    "DemuxerType",
    # GStreamer RTP Demuxer (used by NVDEC for ABSOLUTE RTP timestamps)
    "GstRTPDemuxer",
    "RTCPSenderReport",
    "RTCPTracker",
    "GST_RTP_DEMUXER_AVAILABLE",
]
