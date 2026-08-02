"""Centralized constants for the streaming gateway."""

from __future__ import annotations

from enum import Enum


class GatewayStatus(str, Enum):
    """Status values for the streaming gateway lifecycle."""

    INITIALIZED = "initialized"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"


# Default camera dimensions: 0 = native (SG performs no resize, writes raw NV12
# from NVDEC straight to the ring buffer). The inference path (Ultralytics)
# owns letterbox + resize, so prod matches local `YOLO(...).predict(image)`
# behavior. Operators with bounded SHM budgets can override to a fixed size
# (e.g. 640 or 1280) per camera or container-wide.
DEFAULT_CAMERA_WIDTH = 0
DEFAULT_CAMERA_HEIGHT = 0
DEFAULT_CAMERA_FPS = 10
DEFAULT_CAMERA_QUALITY = 100

# Canonical default for the per-camera PUBLISH cap, in FPS, and the fallback for
# a malformed/absent ``MATRICE_OUTPUT_FPS``. This is the operator-facing default
# applied to cameras with NO declared app demand; a declared demand overrides it
# (F08), including upward.
#
# ``nvdec.py`` intentionally re-declares this value locally instead of importing
# it: nvdec.py has no module-level relative imports because importing the
# ``streaming_gateway`` package pulls in OpenCV/FFmpeg 5.x, which SIGABRTs when
# GStreamer's gst-libav (FFmpeg 4.4) later loads in the same process (see the
# comment above GSTREAMER_DEMUXER_AVAILABLE in nvdec.py). The two are pinned
# together by test_output_fps_cap_wiring.py, which fails if they drift.
DEFAULT_OUTPUT_FPS_CAP = 10.0

# F08 App-Level FPS & Resolution: fallbacks applied per-camera when NO consuming
# app declares a demand.
#   * FPS      -> min(DEFAULT_STREAM_FPS (10), cameraFPS) when no min_fps is
#     declared. The camera's own rate bounds what a cap can mean: capping a 5 fps
#     camera at 10 would be a no-op, and publishing ABOVE the source rate is
#     impossible. See resolve_publish_fps() in streaming_gateway_utils.
#   * Resolution -> NATIVE (0, 0 == the SG performs no resize) when no
#     min_resolution is declared. The app always letterboxes to its own model
#     input size (default 640x640), so an undeclared camera streams native and
#     each consumer downscales itself — no forced SG downscale without a demand.
# max(min) across the consuming apps overrides these; the SG then clamps to the
# camera capability (never upsamples).
#
# IMPORTANT: cameraFPS is the camera's SOURCE rate, never a demand. Treating it
# as one is what made the publish cap inert — every camera's per-camera target
# equalled its source rate, so _should_publish_frame's `source_fps <= target_fps`
# pass-through kept every frame and the 10 fps cap dropped nothing.
#
# Aliased to DEFAULT_OUTPUT_FPS_CAP rather than repeating the literal: the
# "no demand declared" default and the publish-cap default are the same operator
# knob, and two independent 10.0s would eventually disagree.
DEFAULT_STREAM_FPS = DEFAULT_OUTPUT_FPS_CAP
DEFAULT_STREAM_WH = (0, 0)  # (0, 0) = native (no SG resize)

# Ring-buffer depth per camera (NVDEC path). 64 retains ~40-frame clips for
# video/clip-mode inference (num_slots ~= 1.5 x clip_length) so frames referenced
# by an in-progress clip are not overwritten before the clip is emitted. A single
# global default supersedes the per-camera INF-059 sizing (py_streaming #72 /
# py_common #76); per-camera sizing may return on the refactored streaming line.
DEFAULT_NVDEC_NUM_SLOTS = 64

# Timeouts (seconds)
DEFAULT_CONNECTION_TIMEOUT = 300
DEFAULT_WORKER_STOP_TIMEOUT = 15.0

# MediaMTX defaults
DEFAULT_MEDIAMTX_PORT = 8554

# OpenCV path optimizations (REFACTORING_PLAN §20 — evidence-only, opt-in).
# Env MATRICE_SG_OPENCV_OPTIM: none | frame_pool | backpressure |
# executor_offload | combined
# combined = frame_pool + backpressure only (executor_offload is separate;
# REFACTORING_PLAN excludes added post-processing threads from default paths).
DEFAULT_OPENCV_OPTIMIZATION_MODE = "none"
