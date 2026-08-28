# `Session` is a conditionally-None import (see below), so annotations must not be
# evaluated at runtime -- `Session | None` would compute `None | None`. PEP 563
# defers them, matching the 111 other modules in this package.
from __future__ import annotations

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # Non-fatal: exception ignored here; execution continues per surrounding logic.
    pass

import asyncio
import base64
import contextlib
import copy
import json
import logging
import os

# import torch
import re
import sys
import threading
import time
from collections import Counter, OrderedDict, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# External dependencies
try:
    import cv2
except ImportError:
    cv2 = None
import numpy as np

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..utils import (
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    apply_category_mapping,
    bbox_smoothing,
    filter_by_confidence,
    match_results_structure,
)

# Import alert system utilities
from ..utils.alert_instance_utils import ALERT_INSTANCE
from ..utils.location_name_cache import LocationNameCache

# ANA-18: the public-IP lookup used to live here in two copies. It now lives in a
# stdlib-only leaf so face_recognition_client and business_metrics_manager_utils --
# which cannot import this module -- share the same one-per-process answer.
from ..utils.public_ip import resolve_public_ip_once

_module_logger = logging.getLogger(__name__)


def _log_with_msg_meta(logger: logging.Logger, level: int, message: str) -> None:
    """Log *message* and append its character length (and rely on message for value types/lengths)."""
    logger.log(level, "%s | msg_len=%d", message, len(message))


def _format_lpr_api_bbox(bbox: Any) -> List[float] | None:
    """Normalize a plate detection bbox to LPR server format ``[xmin, ymin, xmax, ymax]``."""
    if bbox is None:
        return None
    if isinstance(bbox, dict):
        if "xmin" in bbox:
            coords = (bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"])
        elif "x" in bbox and "width" in bbox and "height" in bbox:
            coords = (bbox["x"], bbox["y"], bbox["x"] + bbox["width"], bbox["y"] + bbox["height"])
        else:
            return None
    elif isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
        coords = bbox[:4]
    else:
        return None
    try:
        return [float(coords[0]), float(coords[1]), float(coords[2]), float(coords[3])]
    except (TypeError, ValueError):
        return None


# Global plate-sync backoff bounds applied when lpr-server answers 429.
# Stand-in for the detection id in "redis" publish mode. An XADD returns a stream
# entry id, not a document id -- the detection document is created later, by
# lpr-server's consumer. Callers only test this value for truthiness (to decide
# whether a plate is already registered), so a sentinel is sufficient and is far
# safer than inventing something that looks like a real ObjectId.
_PUBLISHED_MARKER = "published"

_RATE_LIMIT_BACKOFF_MIN_S = 1.0
_RATE_LIMIT_BACKOFF_MAX_S = 15.0

# Consecutive-failure breaker for lpr-server POSTs. Distinct from the 429 backoff
# above: that one answers a server asking us to slow down, this one answers a server
# that is simply not working.
_SEND_FAILURE_BREAKER_THRESHOLD = 5
_SEND_FAILURE_BREAKER_MIN_S = 5.0
_SEND_FAILURE_BREAKER_MAX_S = 60.0

# Total timeout for a pooled lpr-server POST. ANA-2 lowered the dataclass default
# from 30.0 to 5.0, but 30.0 survived in three live assignments -- the logger's own
# __init__, and both fallbacks plus the except arm of the config read -- so a logger
# built directly, or built from a duck-typed config, still held a sender slot for
# half a minute per plate. One name, so lowering it again is one edit.
_LPR_POST_TIMEOUT_DEFAULT_S = 5.0

# Cap on retained per-(camera, plate) create anchors. Each holds a full-frame base64
# JPEG, and anchors are consumed within the frame that created them, so this is three
# orders of magnitude above what is ever live at once.
_PLATE_ANCHOR_MAX = 256

# JPEG quality for the frame attached to a plate record. Was 99, which cost 13.3 ms /
# 1.27 MB at 1080p and 51.4 ms / 5.1 MB at 4K; 90 is the conventional
# visually-lossless point and roughly halves both.
_PLATE_JPEG_QUALITY = 90


class _LprBackpressureError(Exception):
    """lpr-server is telling us to slow down. Pace against it; do not report it as a fault.

    Subclassed rather than reported per-occurrence because one dense frame can make
    dozens of plates eligible at once: a log line (let alone a stack trace) per
    rejected plate buries the log without adding information beyond the first.
    """

    def __init__(self, message: str, retry_after: float = 0.0) -> None:
        super().__init__(message)
        self.retry_after = float(retry_after or 0.0)


class _LprRateLimitedError(_LprBackpressureError):
    """lpr-server answered 429.

    Carries ``Retry-After`` when the server supplies it; callers fall back to their
    own exponential backoff when it is absent (the current server sends no such
    header, it just returns ``{"error": "rate limit exceeded"}``).
    """


class _LprConnectionLostError(_LprBackpressureError):
    """The connection dropped, and the one retry on a fresh connection dropped too.

    A single stale keep-alive is normal and the retry absorbs it silently. Two in a
    row means the server is shedding connections rather than answering, which is the
    same "slow down" signal as a 429 -- so it feeds the same global gate instead of
    raising a traceback per plate.
    """


def _format_lpr_api_log_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of the LPR request payload safe for logging (truncates imageData)."""
    logged = dict(payload)
    image_data = logged.get("imageData")
    if isinstance(image_data, str) and image_data:
        logged["imageData"] = f"{image_data[:80]}...(len={len(image_data)})"
    return logged


def _lpr_api_response_status(response: Any) -> int | None:
    """Best-effort HTTP/API status extraction from an RPC response object."""
    if isinstance(response, dict):
        for key in ("code", "status_code", "status"):
            value = response.get(key)
            if value is not None:
                try:
                    return int(value)
                except (TypeError, ValueError):
                    continue
    status = getattr(response, "status_code", None)
    if status is not None:
        try:
            return int(status)
        except (TypeError, ValueError):
            return None
    return None


def _format_lpr_api_response_for_log(response: Any) -> str:
    """Serialize an RPC response for structured logging."""
    if isinstance(response, (dict, list)):
        try:
            return json.dumps(response, default=str)
        except (TypeError, ValueError):
            pass
    return repr(response)


def _extract_lpr_exception_response_body(exc: Exception) -> str:
    """Extract response body text from an RPC/HTTP exception, when available."""
    resp = getattr(exc, "response", None)
    if resp is not None:
        text = getattr(resp, "text", None)
        if callable(text):
            try:
                text = text()
            except Exception:
                text = None
        if text:
            return str(text)
        content = getattr(resp, "content", None)
        if content is not None:
            if isinstance(content, bytes):
                return content.decode("utf-8", errors="replace")
            return str(content)
        json_body = getattr(resp, "json", None)
        if callable(json_body):
            try:
                return json.dumps(json_body(), default=str)
            except Exception:
                # Body is unreadable; fall through to the other exception attributes.
                logging.getLogger(__name__).debug("could not serialise LPR error body", exc_info=True)
    body = getattr(exc, "body", None)
    if body is not None:
        return str(body)
    return ""


def _lpr_api_response_is_success(status: int | None, response: Any = None) -> bool:
    """Return True when the LPR API response indicates success.

    _pooled_post()/rpc.post_async() only return a body when the HTTP call
    itself succeeded (2xx) — they raise otherwise, which callers handle
    separately. Some lpr-server endpoints (e.g. create-detection) reply with
    the raw created document and no "code"/"status" wrapper, so a response
    with no recognizable status is success too, unless it carries an
    explicit failure marker.
    """
    if status is not None:
        return 200 <= status < 300
    if isinstance(response, dict):
        return response.get("success") is not False
    return False


def _extract_lpr_detection_id(response: Any) -> str:
    """Best-effort extraction of lpr-server detection document id from an RPC response."""
    if isinstance(response, dict):
        for key in ("id", "_id", "detectionId", "detection_id"):
            value = response.get(key)
            if value not in (None, ""):
                return str(value)
        data = response.get("data")
        if isinstance(data, dict):
            for key in ("id", "_id", "detectionId", "detection_id"):
                value = data.get(key)
                if value not in (None, ""):
                    return str(value)
        elif data not in (None, ""):
            if not isinstance(data, (dict, list)):
                return str(data)
    return ""


# Get the major and minor version numbers
major_version = sys.version_info.major
minor_version = sys.version_info.minor
_log_with_msg_meta(
    _module_logger,
    logging.INFO,
    f"Python version: {major_version}.{minor_version} | version_info_part_types=int,int",
)
os.environ["ORT_LOG_SEVERITY_LEVEL"] = "3"

try:
    from matrice_common.session import Session
except ImportError:
    Session = None

# Pre-import the tracker seam to avoid per-frame import overhead
try:
    from ..Trackers import ConfigDrivenTracker, TrackerProfile

    _HAS_ADVANCED_TRACKER = True
except ImportError:
    ConfigDrivenTracker = None
    TrackerProfile = None
    _HAS_ADVANCED_TRACKER = False


# Lazy import mechanism for LicensePlateRecognizer
_OCR_IMPORT_SOURCE = None
_LicensePlateRecognizerClass = None


def _get_license_plate_recognizer_class():
    """Lazy-load ``LicensePlateRecognizer`` from the installed ``fast_plate_ocr``.

    We use the maintained upstream package directly -- the previously vendored
    ``fast_plate_ocr_py38`` fork was removed because it reached into upstream
    internals (e.g. ``PlateOCRConfig`` in ``fast_plate_ocr.inference.config``)
    that newer releases move/remove, coupling us to one upstream version. The
    differing ``run()`` return shapes across versions are handled by
    ``_ocr_ipc.normalize_run_result``. **Runtime pip installs are intentionally
    NOT done here**: they race with ORT init and caused the dual-installed
    onnxruntime state that broke GPU providers in prod (the OCR venv is
    provisioned ahead of time; see ``_ocr_venv_bootstrap``).
    """
    global _OCR_IMPORT_SOURCE, _LicensePlateRecognizerClass

    logging.debug("LicensePlateRecognizer OCR import source at entry: %r", _OCR_IMPORT_SOURCE)

    if _LicensePlateRecognizerClass is not None:
        return _LicensePlateRecognizerClass

    try:
        from fast_plate_ocr import LicensePlateRecognizer  # type: ignore

        _OCR_IMPORT_SOURCE = "installed_package"
        _LicensePlateRecognizerClass = LicensePlateRecognizer
        logging.info("Successfully imported LicensePlateRecognizer from installed package")
        return _LicensePlateRecognizerClass
    except ImportError as e:
        logging.error(
            "LicensePlateRecognizer unavailable: install 'fast-plate-ocr' in the image. "
            "OCR will be skipped (in-process path). %s",
            e,
        )

    _OCR_IMPORT_SOURCE = "unavailable"
    logging.debug("LicensePlateRecognizer OCR import source: %s", _OCR_IMPORT_SOURCE)
    return None


from ..core.config import AlertConfig, BaseConfig  # noqa: E402

# Internal utilities that are still required
from ..ocr.preprocessing import ImagePreprocessor  # noqa: E402

# Sentinel raised by the OCR subprocess client when the GPU worker is
# permanently unavailable. Imported here (the ``ocr`` package __init__ is empty,
# so this import stays light and triggers no heavy OCR/ORT machinery). A fallback
# class keeps the name defined even if the client module is missing.
try:
    from ..ocr._ocr_subprocess_client import (  # noqa: E402
        OcrSubprocessUnavailable as _OcrSubprocessUnavailable,
    )
except Exception:  # pragma: no cover - defensive

    class _OcrSubprocessUnavailable(Exception):  # noqa: N818 - mirrors public name
        """Fallback sentinel when the OCR subprocess client is unavailable."""


HAS_MATRICE_SESSION = True


@dataclass
class LicensePlateMonitorConfig(BaseConfig):
    """Configuration for License plate detection use case in License plate monitoring.

    Available OCR models (``ocr_model_name``):

    +-----------------------------------------+--------------+---------------------+-----------------------------------+
    | Model                                   | Architecture | Training Data       | Best For                          |
    +-----------------------------------------+--------------+---------------------+-----------------------------------+
    | cct-s-v1-global-model          (default)| CCT (S)      | Global plates       | General use                       |
    | cct-xs-v1-global-model                  | CCT (XS)     | Global plates       | Faster / smaller                  |
    | cct-s-relu-v1-global-model              | CCT-ReLU (S) | Global plates       | Same as S but with ReLU           |
    | cct-xs-relu-v1-global-model             | CCT-ReLU(XS) | Global plates       | Fastest CCT variant               |
    | european-plates-mobile-vit-v2-model     | MobileViT-v2 | European plates     | European plates specifically      |
    | global-plates-mobile-vit-v2-model       | MobileViT-v2 | Global (65+ countries)| Most comprehensive coverage      |
    | argentinian-plates-cnn-model            | CNN          | Argentinian plates  | Argentina only                    |
    | argentinian-plates-cnn-synth-model      | CNN          | Argentinian (synth) | Argentina only                    |
    +-----------------------------------------+--------------+---------------------+-----------------------------------+
    """

    enable_smoothing: bool = False
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.5
    frame_skip: int = 1
    fps: float | None = None
    bbox_format: str = "auto"
    usecase_categories: List[str] = field(default_factory=lambda: ["license_plate"])
    target_categories: List[str] = field(default_factory=lambda: ["license_plate"])
    alert_config: AlertConfig | None = None
    index_to_category: Dict[int, str] | None = field(default_factory=lambda: {0: "license_plate"})
    language: List[str] = field(default_factory=lambda: ["en"])
    country: str = field(default_factory=lambda: "us")
    ocr_mode: str = field(default_factory=lambda: "alphanumeric")  # "alphanumeric" or "numeric" or "alphabetic"
    ocr_model_name: str = "cct-s-v1-global-model"  # See table above for available models
    ocr_device: str = "auto"  # "auto", "cuda", or "cpu"
    session: Session | None = None
    lpr_server_id: str | None = None  # Optional LPR server ID for remote logging
    redis_server_id: str | None = None  # Optional Redis server ID for instant alerts
    # Plate-sync sender knobs (bounded background create/append POSTs)
    lpr_append_min_interval_s: float = (
        5.0  # Min seconds between view-frame appends per plate (also failed-create backoff)
    )
    lpr_max_in_flight: int = 2  # Max concurrent lpr-server POSTs
    lpr_max_pending_slots: int = 32  # Max pending per-plate payload slots awaiting send
    lpr_max_frame_age_s: float = 5.0  # Appends older than this (stream wall-clock) are dropped
    # Was 30.0, which meant a wedged lpr-server held a sender slot for half a minute
    # per plate. These POSTs are a single small JSON body to a service on the same
    # network; if it has not answered in 5 s it is not going to.
    lpr_post_timeout_s: float = _LPR_POST_TIMEOUT_DEFAULT_S  # Total timeout for pooled lpr-server HTTP POSTs
    # Transport for plate sightings.
    #
    # "redis" (default) publishes each sighting to the ``lpr-detections`` stream and
    # returns immediately; lpr-server's own consumer goroutine
    # (StartRedisConsumer -> processRedisMessage) does the media-server extraction,
    # the upsert and the alert evaluation off the pipeline's critical path.
    #
    # "http" is the previous behaviour, kept so this is revertible by config alone.
    # It POSTs /v1/lpr-server/detections and waits for a response -- which is the
    # problem: a structurally valid create blocks ~15s and then closes the
    # connection without a body (measured 8/8, while a 404 or a 400 answers in
    # under a millisecond). With lpr_max_in_flight=2 that caps the client near
    # 2 sends per 15s, which fills the pending-slot buffer, evicts sightings and
    # leaves lpr-server 8-13s behind the stream head.
    lpr_publish_mode: str = "redis"  # "redis" | "http"
    lpr_detections_stream: str = "lpr-detections"  # Stream lpr-server's consumer group reads
    lpr_stream_maxlen: int = 100_000  # Approximate XADD cap; bounds Redis if the consumer stalls
    # Min seconds between lpr-server POST offers for the same (camera, plate) across
    # different tracks. This is the coalescing floor that bounds how much a single
    # plate can write to the database.
    #
    # It used to default to 0.0 -- "rely on per-track episode dedup only" -- which
    # assumes one track per vehicle pass. That assumption does not survive contact
    # with dense traffic: trackers fragment across occlusion and re-detection, so one
    # physical vehicle yields many track ids, each of which looks like a fresh pass
    # and earns its own POST. Every POST costs a media-server frame extraction, a
    # Frame document and a stored JPEG, so the cost is real even though the request
    # is small.
    #
    # It went unnoticed because the append endpoint used to 404 (see append_view_frame):
    # nothing downstream of the create ever actually ran. With appends working, one
    # camera-hour produced plates holding 72, 68 and 46 view frames -- ~100
    # media-server extractions per minute and climbing -- for a stream where a vehicle
    # is in view for seconds.
    #
    # 60s bounds a plate to at most 60 writes/hour instead of 720 (the sender's 5s
    # floor), while a normal single pass still records exactly one frame. Set to 0.0
    # to restore the old per-track-only behaviour.
    plate_log_min_interval_s: float = 60.0
    # ------------------------------------------------------------------ #
    # Confirmation gates.
    #
    # These were literals in __init__ until the access-control / surveillance
    # split needed them to differ per profile. EVERY default below is the exact
    # value that was hard-coded before, so the base use case is unchanged --
    # see test_lpr_usecase_split.py::test_base_usecase_gates_are_unchanged,
    # which exists purely to keep that true.
    #
    # They express one trade-off: how much agreement to demand before treating a
    # read as real. Access control raises them (a wrong plate opens a barrier);
    # surveillance lowers them (a missed plate is gone for good).
    # ------------------------------------------------------------------ #
    # Reference space for the coordinates published on `alert_instant_triggered`.
    #
    # The consumer (fe-analytics) converts them to a fraction of the displayed
    # image by dividing BOTH axes by a constant it calls ALERT_BBOX_DETECTOR_SIZE,
    # currently 640:
    #     left = coords.x / 640 * rect.width      top = coords.y / 640 * rect.height
    # That is only correct if coordinates are expressed as a fraction of the frame
    # times 640. This use case was publishing raw source pixels (1280x720 here),
    # so every alert box was drawn at roughly twice its correct offset and twice
    # its correct size -- verified on a live alert, where the drawn box landed
    # ~480 px away on empty pavement while the plate sat exactly at the published
    # pixels.
    #
    # Setting this to 640 emits `pixel / frame_dim * 640`, which is what the
    # deployed consumer's contract actually asks for. Set it to 0 to publish raw
    # source pixels again (the previous behaviour) once fe-analytics is fixed to
    # scale by the image's natural width/height instead of a constant -- at which
    # point this whole transform should go away.
    # Coordinate space for the alert box published on `alert_instant_triggered`
    # by THIS process (`context_data.coordinates`).
    #
    #   "normalized" (default) -- fractions of the frame, 0..1, matching the VMS
    #       overlay channel (`tracking_stats.detections`) and the media-server's
    #       stored `RtpPrediction.box`. A consumer renders it as
    #       `coord * displayed_dimension`, which is resolution-independent.
    #   "pixel" -- source-frame pixels, the historical behaviour.
    #
    # Why this had to change: fe-analytics converted the box with
    # `coord / ALERT_BBOX_DETECTOR_SIZE * rect_dimension` (constant 640), which is
    # only correct for a 640x640 frame. On the 1280x720 streams here that drew
    # every alert box at ~2x its offset and size -- measured on a live alert, the
    # drawn box landed ~480 px away on empty pavement while the plate sat exactly
    # at the published pixels. Publishing fractions makes the constant unnecessary:
    # the consumer multiplies by the size it is actually rendering at.
    # "normalized" (0..1 fractions of the frame) is the agreed contract with the
    # frontend team, who are updating fe-analytics to render
    # `coord * displayed_dimension` instead of dividing by its 640 constant.
    #
    # ONE CAVEAT THAT IS NOT FIXED BY THIS SETTING: lpr-server also publishes
    # these alerts. It consumes `lpr-detections`, derives `coordinates` from that
    # message's `bbox`, and XADDs `alert_instant_triggered` itself -- always in
    # PIXELS, and it rounds to integers, so the `bbox` we send it cannot be
    # normalized without collapsing to 0x0. Wherever lpr-server is the publisher
    # (observed: lpr_cam2), the alert still carries pixels. A consumer that
    # multiplies fractions by the displayed size will therefore throw those boxes
    # far off-screen. Until lpr-server emits fractions too, the consumer needs to
    # branch, e.g. `is_normalized = max(x, y, width, height) <= 1.0`.
    #
    # Set to "pixel" to go back to a uniformly pixel wire.
    alert_bbox_coordinate_space: str = "normalized"  # "normalized" | "pixel"

    # Coordinate space for the `bbox` sent to lpr-server -- both on the
    # `lpr-detections` stream and on the legacy HTTP create payload. That single
    # field feeds TWO things: the stored detection document, and the
    # `coordinates` lpr-server puts on the alerts IT publishes.
    #
    # DEFAULT IS "pixel" and must stay that way until lpr-server ships support,
    # because lpr-server ROUNDS this to integer coordinates. Verified against the
    # live wire -- `bbox [373.75, 584.0, 438.25, 605.0]` became
    # `coordinates {x:374, y:584, width:65, height:21}`, an exact round(). Feed it
    # 0..1 fractions today and every alert box it publishes collapses to
    # `{x:0, y:1, width:0, height:0}` -- worse than the misalignment being fixed.
    #
    # Flip to "normalized" the day lpr-server treats bbox as fractions. It is the
    # last channel still in pixels; everything else this use case emits is already
    # normalized. See lpr_bbox_normalization_plan.md.
    lpr_bbox_coordinate_space: str = "pixel"  # "normalized" | "pixel"
    min_plate_len: int = 3  # Shortest accepted plate after cleaning
    max_plate_len: int = 10  # Longest accepted plate after cleaning
    stable_frames_required: int = 1  # Consecutive frames a text must repeat to be "stable"
    ocr_confidence_threshold: float = 0.75  # Mean OCR char confidence floor
    smoother_hold_frames: int = 3  # Frames a dropped detection is carried forward
    smoother_iou_threshold: float = 0.3  # IoU for associating a carried detection

    def validate(self) -> List[str]:
        """Validate configuration parameters."""
        errors = super().validate()
        if self.confidence_threshold < 0 or self.confidence_threshold > 1:
            errors.append("confidence_threshold must be between 0 and 1")
        if self.frame_skip <= 0:
            errors.append("frame_skip must be positive")
        if self.bbox_format not in ["auto", "xmin_ymin_xmax_ymax", "x_y_width_height"]:
            errors.append("bbox_format must be one of: auto, xmin_ymin_xmax_ymax, x_y_width_height")
        if self.smoothing_window_size <= 0:
            errors.append("smoothing_window_size must be positive")
        if self.smoothing_cooldown_frames < 0:
            errors.append("smoothing_cooldown_frames cannot be negative")
        if self.smoothing_confidence_range_factor <= 0:
            errors.append("smoothing_confidence_range_factor must be positive")
        if self.lpr_append_min_interval_s <= 0:
            errors.append("lpr_append_min_interval_s must be positive")
        if self.lpr_max_in_flight <= 0:
            errors.append("lpr_max_in_flight must be positive")
        if self.lpr_max_pending_slots <= 0:
            errors.append("lpr_max_pending_slots must be positive")
        if self.lpr_max_frame_age_s <= 0:
            errors.append("lpr_max_frame_age_s must be positive")
        if self.lpr_post_timeout_s <= 0:
            errors.append("lpr_post_timeout_s must be positive")
        if self.lpr_publish_mode not in ("redis", "http"):
            errors.append("lpr_publish_mode must be 'redis' or 'http'")
        if not self.lpr_detections_stream:
            errors.append("lpr_detections_stream must be a non-empty stream name")
        if self.lpr_stream_maxlen <= 0:
            errors.append("lpr_stream_maxlen must be positive")
        if self.min_plate_len < 1:
            errors.append("min_plate_len must be at least 1")
        if self.max_plate_len < self.min_plate_len:
            errors.append("max_plate_len must be >= min_plate_len")
        if self.stable_frames_required < 1:
            errors.append("stable_frames_required must be at least 1")
        if not 0.0 <= self.ocr_confidence_threshold <= 1.0:
            errors.append("ocr_confidence_threshold must be between 0.0 and 1.0")
        if self.smoother_hold_frames < 0:
            errors.append("smoother_hold_frames cannot be negative")
        if not 0.0 <= self.smoother_iou_threshold <= 1.0:
            errors.append("smoother_iou_threshold must be between 0.0 and 1.0")
        if self.alert_bbox_coordinate_space not in ("normalized", "pixel"):
            errors.append("alert_bbox_coordinate_space must be 'normalized' or 'pixel'")
        if self.lpr_bbox_coordinate_space not in ("normalized", "pixel"):
            errors.append("lpr_bbox_coordinate_space must be 'normalized' or 'pixel'")
        return errors


class _LprRedisPublisher:
    """Publish plate sightings to the ``lpr-detections`` stream.

    lpr-server has always shipped a consumer for this stream -- ``StartRedisConsumer``
    -> ``processRedisMessage`` are both in the deployed binary, and the consumer group
    ``lpr-detection-group`` is registered and blocked-reading -- but nothing ever
    published to it (``entries-added = 0``). This is that publisher.

    Deliberately synchronous: ``XADD`` is a sub-millisecond round trip, so there is
    nothing to await and no reason to hold an event loop open for it. That is the
    whole point of the change -- the previous transport made the pipeline wait on a
    remote handler that never answered.

    Connection handling mirrors ``analytics/redis_publisher.py`` (same environment
    variables, same Sentinel support, same reconnect backoff) so the stack resolves
    Redis one way.
    """

    _RECONNECT_BACKOFF_S = 5.0

    def __init__(
        self,
        stream: str = "lpr-detections",
        maxlen: int = 100_000,
        redis_client: Any = None,
    ):
        self.logger = logging.getLogger(__name__)
        self.stream = stream
        self.maxlen = int(maxlen)
        self.host = os.environ.get("REDIS_HOST") or "localhost"
        self.port = int(os.environ.get("REDIS_PORT") or 6379)
        self.password = os.environ.get("REDIS_PASSWORD")
        self.username = os.environ.get("REDIS_USERNAME")
        self.db = int(os.environ.get("REDIS_DB") or 0)
        self.master_name = os.environ.get("REDIS_MASTER_NAME")
        self._sentinel_hosts = self._parse_sentinel_hosts(os.environ.get("REDIS_SENTINEL_HOSTS"))
        self._client = redis_client  # injectable for tests
        self._injected = redis_client is not None
        self._import_failed = False
        self._last_connect_attempt = 0.0
        self._last_warn_ts = 0.0
        self.n_published = 0
        self.n_failed = 0

    @staticmethod
    def _parse_sentinel_hosts(raw: str | None) -> List[Tuple[str, int]]:
        if not raw:
            return []
        default_port = int(os.environ.get("REDIS_SENTINEL_PORT") or 26379)
        hosts: List[Tuple[str, int]] = []
        for chunk in raw.split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            if ":" in chunk:
                host, _, port = chunk.rpartition(":")
                try:
                    hosts.append((host, int(port)))
                    continue
                except ValueError:
                    pass
            hosts.append((chunk, default_port))
        return hosts

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        if self._import_failed:
            return None
        now = time.time()
        if now - self._last_connect_attempt < self._RECONNECT_BACKOFF_S:
            return None
        self._last_connect_attempt = now
        try:
            import redis  # noqa: PLC0415 - lazy: only needed when publish mode is redis
        except Exception as e:  # pragma: no cover - environment-dependent
            self._import_failed = True
            self.logger.warning("[LP_LOGGING] redis not importable (%s); plate publishing disabled", e)
            return None
        try:
            if self._sentinel_hosts and self.master_name:
                from redis.sentinel import Sentinel  # noqa: PLC0415 - lazy with the parent import

                sentinel_kwargs: Dict[str, Any] = {"socket_timeout": 5}
                if self.password:
                    sentinel_kwargs["password"] = self.password
                sentinel = Sentinel(self._sentinel_hosts, **sentinel_kwargs)
                master_kwargs: Dict[str, Any] = {
                    "db": self.db,
                    "socket_timeout": 5,
                    "decode_responses": False,
                    "retry_on_timeout": True,
                    "health_check_interval": 30,
                }
                if self.password:
                    master_kwargs["password"] = self.password
                if self.username:
                    master_kwargs["username"] = self.username
                client = sentinel.master_for(self.master_name, **master_kwargs)
            else:
                client = redis.Redis(
                    host=self.host,
                    port=self.port,
                    password=self.password,
                    username=self.username,
                    db=self.db,
                    decode_responses=False,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                )
            client.ping()
            self._client = client
            self.logger.warning(
                "[LP_LOGGING] plate publisher connected to redis %s stream=%s",
                self._target_description(),
                self.stream,
            )
        except Exception as e:
            self.logger.warning(
                "[LP_LOGGING] plate publisher redis connect failed (%s): %s",
                self._target_description(),
                e,
            )
            self._client = None
        return self._client

    def _target_description(self) -> str:
        if self._sentinel_hosts and self.master_name:
            hosts = ",".join(f"{h}:{p}" for h, p in self._sentinel_hosts)
            return f"sentinel[{hosts}] master={self.master_name}"
        return f"{self.host}:{self.port}"

    def publish(self, payload: Dict[str, Any], camera_id: str = "") -> bool:
        """XADD one sighting. Returns True on success; never raises."""
        client = self._get_client()
        if client is None:
            self.n_failed += 1
            return False
        try:
            client.xadd(
                self.stream,
                {"data": json.dumps(payload, default=str), "_message_key": camera_id or ""},
                maxlen=self.maxlen,
                approximate=True,
            )
            self.n_published += 1
            return True
        except Exception as e:
            self.n_failed += 1
            now = time.time()
            if now - self._last_warn_ts >= 10.0:
                self._last_warn_ts = now
                self.logger.warning("[LP_LOGGING] XADD to %s failed: %s", self.stream, e)
            if not self._injected:
                self._client = None  # force a reconnect on the next publish
            return False

    def stats(self) -> Dict[str, int]:
        return {"published": self.n_published, "failed": self.n_failed}


class LicensePlateMonitorLogger:
    def __init__(self):
        self.session = None
        self.logger = logging.getLogger(__name__)
        self.lpr_server_id = None
        self.server_info = None
        self.server_base_url = None
        # Shared aiohttp session for lpr-server POSTs (created lazily on the
        # sender loop; avoids a new ClientSession/TCP connection per POST).
        self._http_session = None
        self._post_timeout_s = _LPR_POST_TIMEOUT_DEFAULT_S
        # Transport selection. "redis" publishes to the lpr-detections stream and
        # returns; "http" keeps the old POST-and-wait behaviour. Set from config in
        # initialize_session(); the default matches the config default so a logger
        # built without config still takes the good path.
        self._publish_mode = "redis"
        self._lpr_bbox_space = "pixel"  # see LicensePlateMonitorConfig.lpr_bbox_coordinate_space
        self._plate_publisher: _LprRedisPublisher | None = None
        # Global (all-plates) pacing against lpr-server's 429s. The sender's own
        # limits are per-key (append_min_interval_s) and concurrency-only
        # (max_in_flight), so with N plates active the outbound rate is N/interval
        # with no ceiling -- one dense-traffic frame can make dozens eligible at
        # once and blow past the server's limiter. This is the missing global cap,
        # learned from the server's own 429s rather than a guessed constant.
        self._rate_limited_until = 0.0  # monotonic deadline; 0.0 == not limited
        self._rate_limit_backoff_s = 0.0  # current backoff, grows on repeat 429s
        self._consecutive_send_failures = 0  # reset by note_send_ok; see note_send_failed
        self._send_failure_backoff_s = 0.0  # current breaker backoff, grows while failing
        self._last_send_failure_warn_ts = 0.0  # one breaker warning per backoff window
        self._last_rate_limit_warn_ts = 0.0
        self.public_ip = self._get_public_ip()

    def initialize_session(self, config: LicensePlateMonitorConfig) -> None:
        """Initialize session and fetch server connection info if lpr_server_id is provided."""
        # Use existing session if provided, otherwise create new one
        if self.session and self.server_info and self.server_base_url:
            self.logger.info("[LP_LOGGING] Session already initialized: %s", self.server_base_url)
            return

        if config.session:
            self.session = config.session

        if not self.session:
            # Initialize Matrice session
            if not HAS_MATRICE_SESSION:
                self.logger.error("[LP_LOGGING] Matrice session module not available")
                raise ImportError("Matrice session is required for License Plate Monitoring")
            try:
                account_number = os.getenv("MATRICE_ACCOUNT_NUMBER", "")
                access_key_id = os.getenv("MATRICE_ACCESS_KEY_ID", "")
                secret_key = os.getenv("MATRICE_SECRET_ACCESS_KEY", "")
                project_id = os.getenv("MATRICE_PROJECT_ID", "")

                self.session = Session(
                    account_number=account_number,
                    access_key=access_key_id,
                    secret_key=secret_key,
                    project_id=project_id,
                )
            except Exception as e:
                self.logger.error(
                    "[LP_LOGGING] Failed to initialize Matrice session: %s",
                    e,
                    exc_info=True,
                )
                raise

        # Fetch server connection info if lpr_server_id is provided
        if config.lpr_server_id:
            self.lpr_server_id = config.lpr_server_id
            self.logger.info("[LP_LOGGING] Fetching LPR server info for id=%s", self.lpr_server_id)
            try:
                self.server_info = self.get_server_connection_info()
                if self.server_info:
                    server_host = self.server_info.get("host", "localhost")
                    server_port = self.server_info.get("port", 8200)

                    if server_host == self.public_ip:
                        self.server_base_url = f"http://localhost:{server_port}"
                    else:
                        self.server_base_url = f"http://{server_host}:{server_port}"

                    self.session.update(self.server_info.get("projectID", ""))
                    self.logger.info(
                        "[LP_LOGGING] LPR server ready: name=%s url=%s",
                        self.server_info.get("name", "Unknown"),
                        self.server_base_url,
                    )
                else:
                    self.logger.error("[LP_LOGGING] Failed to fetch LPR server connection info")
            except Exception as e:
                self.logger.error(
                    "[LP_LOGGING] Error fetching LPR server connection info: %s",
                    e,
                    exc_info=True,
                )
        else:
            self.logger.warning("[LP_LOGGING] No lpr_server_id in config; plate logging disabled")

    def _get_public_ip(self) -> str:
        """This host's public IP; see :func:`~..utils.public_ip.resolve_public_ip_once`."""
        return resolve_public_ip_once(self.logger)

    def _get_backend_base_url(self) -> str:
        """Resolve backend base URL based on ENV variable: prod/staging/dev."""
        env = os.getenv("ENV", "prod").strip().lower()
        if env in ("prod", "production"):
            host = "prod.backend.app.matrice.ai"
        elif env in ("dev", "development"):
            host = "dev.backend.app.matrice.ai"
        else:
            host = "staging.backend.app.matrice.ai"
        return f"https://{host}"

    def get_server_connection_info(self) -> Dict[str, Any] | None:
        """Fetch server connection info from RPC."""
        if not self.lpr_server_id:
            self.logger.warning("No lpr_server_id set, cannot fetch server connection info")
            return None

        try:
            endpoint = f"/v1/actions/lpr_servers/{self.lpr_server_id}"
            self.logger.info(f"Sending GET request to: {endpoint}")
            response = self.session.rpc.get(endpoint)
            self.logger.info(
                f"Received response: success={response.get('success')}, code={response.get('code')}, message={response.get('message')}"
            )

            if response.get("success", False) and response.get("code") == 200:
                # Response format:
                # {'success': True,
                # 'code': 200,
                # 'message': 'Success',
                # 'serverTime': '2025-10-19T04:58:04Z',
                # 'data': {'id': '68f07e515cd5c6134a075384',  # pragma: allowlist secret
                # 'name': 'lpr-server-1',
                # 'host': '<redacted>',
                # 'port': 8200,
                # 'status': 'created',
                # 'accountNumber': '<redacted>',
                # 'projectID': '68ca6372ab79ba13ef699ba6',  # pragma: allowlist secret
                # 'region': 'United States',
                # 'isShared': False}}
                data = response.get("data", {})
                self.logger.info(
                    f"Server connection info retrieved: name={data.get('name')}, host={data.get('host')}, port={data.get('port')}, status={data.get('status')}"
                )
                return data
            else:
                self.logger.warning(f"Failed to fetch server info: {response.get('message', 'Unknown error')}")
                return None
        except Exception as e:
            self.logger.error(f"Exception while fetching server connection info: {e}", exc_info=True)
            return None

    def _format_timestamp_rfc3339(self, timestamp: str) -> str:
        """Convert timestamp to RFC3339 format (2006-01-02T15:04:05Z).

        Handles various input formats:
        - "YYYY-MM-DD-HH:MM:SS.ffffff UTC"
        - "YYYY:MM:DD HH:MM:SS"
        - Unix timestamp (float/int)
        """
        try:
            # If already in RFC3339 format, return as is
            if "T" in timestamp and timestamp.endswith("Z"):
                return timestamp

            # Try to parse common formats
            dt = None

            # Format: "2025-08-19-04:22:47.187574 UTC"
            if "-" in timestamp and "UTC" in timestamp:
                timestamp_clean = timestamp.replace(" UTC", "")
                dt = datetime.strptime(timestamp_clean, "%Y-%m-%d-%H:%M:%S.%f")
            # Format: "2025:10:23 14:30:45"
            elif ":" in timestamp and " " in timestamp:
                dt = datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S")
            # Format: numeric timestamp
            elif timestamp.replace(".", "").isdigit():
                dt = datetime.fromtimestamp(float(timestamp), tz=timezone.utc)

            if dt is None:
                # Fallback to current time
                dt = datetime.now(timezone.utc)
            else:
                # Ensure timezone is UTC
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)

            # Format to RFC3339: 2006-01-02T15:04:05Z
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        except Exception as e:
            self.logger.warning(f"Failed to parse timestamp '{timestamp}': {e}. Using current time.")
            return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _extract_camera_info_from_stream(self, stream_info: Dict[str, Any] | None) -> Dict[str, str]:
        """
        Extract camera_name, camera_id, and location_id from stream_info.

        Handles multiple sources and shapes for camera_id/camera_name/location_id to ensure
        correct extraction even when a single container is connected to multiple camera streams.

        Supported stream_info shapes (seen across pipeline/components):
        - stream_info["camera_info"]
        - stream_info["input_settings"]["camera_info"]
        - stream_info["input_settings"]["input_stream"]["camera_info"]
        - stream_info["input_streams"][i]["input_stream"]["camera_info"]
        - camera_id derived from stream_info["topic"] suffix markers ("_input_topic" or "_input-topic")

        Args:
            stream_info: Stream information dictionary

        Returns:
            Dict with camera_name, camera_id, location_id
        """
        camera_name = ""
        camera_id = ""
        location_id = ""

        if not stream_info or not isinstance(stream_info, dict):
            self.logger.debug("stream_info is None/invalid, returning empty camera info")
            return {
                "camera_name": camera_name,
                "camera_id": camera_id,
                "location_id": location_id,
            }

        def _to_str(value: Any) -> str:
            """Convert common stream-info values to a safe string."""
            if value is None:
                return ""
            if isinstance(value, str):
                return value.strip()
            if isinstance(value, (int, float)):
                return str(value)
            if isinstance(value, dict):
                return ""
            if isinstance(value, (list, tuple, set)):
                for item in value:
                    s = _to_str(item)
                    if s:
                        return s
                return ""
            try:
                return str(value).strip()
            except Exception:
                return ""

        def _dict_get_str(d: Any, *keys: str) -> str:
            """Get first non-empty key from dict as string."""
            if not isinstance(d, dict):
                return ""
            for k in keys:
                val = _to_str(d.get(k))
                if val:
                    return val
            return ""

        def _extract_camera_id_from_topic(topic_val: Any) -> str:
            """Extract camera_id from topic formats like '{camera_id}_input_topic' or '{camera_id}_input-topic'."""
            topic = _to_str(topic_val)
            if not topic:
                return ""
            for suffix in ("_input_topic", "_input-topic"):
                if topic.endswith(suffix):
                    return topic[: -len(suffix)].strip()
            for marker in ("_input_topic", "_input-topic"):
                if marker in topic:
                    return topic.split(marker)[0].strip()
            return ""

        def _extract_camera_id_from_frame_id(frame_id_val: Any) -> str:
            """
            Best-effort fallback: extract a stable camera/stream identifier from frame_id.

            Observed upstream format (py_inference legacy mode):
              - 'legacy_{hexId}_{suffix}'
            Example:
              - 'legacy_694e7603a086e13d9c95dd3d_51b30e93'

            We ONLY accept the middle segment if it looks like a hex identifier (>= 8 chars)
            to avoid mis-parsing arbitrary frame_id formats.
            """
            fid = _to_str(frame_id_val)
            if not fid:
                return ""
            if fid.startswith("legacy_"):
                parts = fid.split("_")
                if len(parts) >= 3:
                    candidate = parts[1].strip()
                    if candidate and re.fullmatch(r"[0-9a-f]{8,}", candidate, re.IGNORECASE):
                        return candidate
            return ""

        input_settings = stream_info.get("input_settings") or {}
        if not isinstance(input_settings, dict):
            input_settings = {}

        camera_info_root = stream_info.get("camera_info") or {}
        if not isinstance(camera_info_root, dict):
            camera_info_root = {}

        camera_info_input_settings = input_settings.get("camera_info") or {}
        if not isinstance(camera_info_input_settings, dict):
            camera_info_input_settings = {}

        input_stream = input_settings.get("input_stream") or {}
        if not isinstance(input_stream, dict):
            input_stream = {}

        camera_info_input_stream = input_stream.get("camera_info") or {}
        if not isinstance(camera_info_input_stream, dict):
            camera_info_input_stream = {}

        input_streams = stream_info.get("input_streams") or []
        input_stream_candidates: List[Dict[str, Any]] = []
        camera_info_input_streams: List[Dict[str, Any]] = []
        if isinstance(input_streams, list):
            for item in input_streams:
                if not isinstance(item, dict):
                    continue
                inner = item.get("input_stream", item)
                if not isinstance(inner, dict):
                    continue
                input_stream_candidates.append(inner)
                ci = inner.get("camera_info") or {}
                if isinstance(ci, dict) and ci:
                    camera_info_input_streams.append(ci)

        topic_camera_id = _extract_camera_id_from_topic(stream_info.get("topic")) or _extract_camera_id_from_topic(
            input_settings.get("topic")
        )
        if not topic_camera_id:
            topics_val = stream_info.get("topics")
            if isinstance(topics_val, (list, tuple, set)):
                for t in topics_val:
                    topic_camera_id = _extract_camera_id_from_topic(t)
                    if topic_camera_id:
                        break

        camera_info_sources: List[Dict[str, Any]] = [
            camera_info_root,
            camera_info_input_settings,
            camera_info_input_stream,
        ] + camera_info_input_streams

        def _camera_id_from_camera_info(ci: Dict[str, Any]) -> str:
            return _dict_get_str(ci, "camera_id", "cameraId", "_id", "id")

        matched_ci: Dict[str, Any] = {}
        if topic_camera_id:
            camera_id = topic_camera_id
            for ci in camera_info_sources:
                if _camera_id_from_camera_info(ci) == camera_id:
                    matched_ci = ci
                    break

        if not camera_id:
            camera_id = (
                _dict_get_str(stream_info, "camera_id", "cameraId")
                or _dict_get_str(input_settings, "camera_id", "cameraId")
                or _camera_id_from_camera_info(camera_info_root)
                or _camera_id_from_camera_info(camera_info_input_settings)
                or _camera_id_from_camera_info(camera_info_input_stream)
            )
            if not camera_id:
                for candidate in input_stream_candidates:
                    camera_id = _dict_get_str(candidate, "camera_id", "cameraId", "_id", "id")
                    if camera_id:
                        break
            if not camera_id:
                camera_id = topic_camera_id

        # Final fallback: derive camera_id from frame_id if stream_info doesn't include camera_info/topic
        if not camera_id:
            camera_id = _extract_camera_id_from_frame_id(stream_info.get("frame_id"))

        # Use matched camera_info (if found) to set camera_name/location_id
        if matched_ci:
            camera_name = _dict_get_str(matched_ci, "camera_name", "cameraName", "name")
            location_id = _dict_get_str(matched_ci, "location", "location_id", "locationId")

        if not camera_name:
            camera_name = (
                _dict_get_str(camera_info_root, "camera_name", "cameraName", "name")
                or _dict_get_str(camera_info_input_settings, "camera_name", "cameraName", "name")
                or _dict_get_str(camera_info_input_stream, "camera_name", "cameraName", "name")
                or _dict_get_str(stream_info, "camera_name", "cameraName")
                or _dict_get_str(input_settings, "camera_name", "cameraName")
            )
            if not camera_name:
                for ci in camera_info_input_streams:
                    camera_name = _dict_get_str(ci, "camera_name", "cameraName", "name")
                    if camera_name:
                        break

        if not location_id:
            location_id = (
                _dict_get_str(camera_info_root, "location", "location_id", "locationId")
                or _dict_get_str(camera_info_input_settings, "location", "location_id", "locationId")
                or _dict_get_str(camera_info_input_stream, "location", "location_id", "locationId")
                or _dict_get_str(stream_info, "location_id", "location", "locationId")
                or _dict_get_str(input_settings, "location_id", "location", "locationId")
            )
            if not location_id:
                for ci in camera_info_input_streams:
                    location_id = _dict_get_str(ci, "location", "location_id", "locationId")
                    if location_id:
                        break

        self.logger.debug(
            "Extracted camera info - camera_name: '%s', camera_id: '%s', location_id: '%s'",
            camera_name,
            camera_id,
            location_id,
        )

        return {
            "camera_name": camera_name,
            "camera_id": camera_id,
            "location_id": location_id,
        }

    def _extract_application_id_from_stream(self, stream_info: Dict[str, Any] | None) -> str:
        """
        Extract application_id from stream_info.

        LicensePlateMonitorLogger does not inherit BaseProcessor (unlike
        LicensePlateMonitorUseCase), so it has no access to
        BaseProcessor.extract_deployment_ids(); this mirrors that same
        priority-based fallback chain (stream_info root -> input_settings ->
        camera_info, checking snake_case and camelCase key variants).
        """
        if not stream_info or not isinstance(stream_info, dict):
            return ""

        input_settings = stream_info.get("input_settings", {}) or {}
        if not isinstance(input_settings, dict):
            input_settings = {}
        cam_info = stream_info.get("camera_info", {}) or {}
        if not isinstance(cam_info, dict):
            cam_info = {}

        return (
            stream_info.get("application_id", "")
            or stream_info.get("applicationId", "")
            or stream_info.get("app_id", "")
            or input_settings.get("application_id", "")
            or input_settings.get("applicationId", "")
            or cam_info.get("application_id", "")
            or cam_info.get("applicationId", "")
            or ""
        )

    def _build_lpr_request_context(
        self,
        plate_text: str,
        timestamp: str,
        stream_info: Dict[str, Any],
        image_data: str | None = None,
        bbox: Any = None,
        ocr_confidence: float | None = None,
    ) -> Dict[str, Any]:
        """Build shared lpr-server request fields for create and view-frame append."""
        if not stream_info:
            stream_info = {}

        camera_info = self._extract_camera_info_from_stream(stream_info)
        camera_id = camera_info.get("camera_id", "")
        camera_name = camera_info.get("camera_name", "default_camera")
        location = camera_info.get("location_id", "") or camera_info.get("location", "default_location")
        application_id = self._extract_application_id_from_stream(stream_info)
        input_settings = (
            stream_info.get("input_settings", {}) if isinstance(stream_info.get("input_settings", {}), dict) else {}
        )
        frame_id = (
            stream_info.get("frame_id", "")
            or stream_info.get("frameId", "")
            or input_settings.get("frame_id", "")
            or input_settings.get("frameId", "")
            or ""
        )
        rtp_number = (
            stream_info.get("rtp_number", "")
            or stream_info.get("rtpNumber", "")
            or input_settings.get("rtp_number", "")
            or input_settings.get("rtpNumber", "")
            or ""
        )
        # lpr-server's CreateDetectionRequest types frameId as a Go string, and Go
        # will not coerce a JSON number into one -- a numeric frame_id is rejected
        # outright with
        #   400 json: cannot unmarshal number into Go struct field
        #       CreateDetectionRequest.frameId of type string
        # and the sighting is lost. Nothing upstream guarantees the type:
        # build_stream_info() stores frame_id as passed, and the extractors above
        # only pick the first truthy candidate. rtp_number is already normalised
        # (to int, below) -- frame_id was simply missed. Pre-existing, but only
        # observable once appends stopped 404-ing before the body was parsed.
        frame_id = "" if frame_id is None else str(frame_id)
        try:
            rtp_number_int = 0 if rtp_number in (None, "") else int(rtp_number)
        except (TypeError, ValueError):
            rtp_number_int = 0

        project_id = self.server_info.get("projectID", "") if self.server_info else ""
        rfc3339_timestamp = self._format_timestamp_rfc3339(timestamp)

        payload: Dict[str, Any] = {
            "licensePlate": plate_text,
            "frameId": frame_id,
            "rtpNumber": rtp_number_int,
            "location": location,
            "camera": camera_name,
            "cameraId": camera_id,
            "applicationId": application_id,
            "captureTimestamp": rfc3339_timestamp,
            "projectId": project_id,
            "imageData": image_data if image_data else "",
        }
        api_bbox = _format_lpr_api_bbox(bbox)
        api_bbox = self._to_lpr_bbox_space(api_bbox, stream_info)
        if api_bbox is not None:
            payload["bbox"] = api_bbox
        if ocr_confidence is not None:
            payload["ocr_confidence"] = float(ocr_confidence)

        return {
            "payload": payload,
            "project_id": project_id,
            "camera_id": camera_id,
            "camera_name": camera_name,
            "application_id": application_id,
            "location": location,
            "frame_id": frame_id,
            "rtp_number": rtp_number,
            "rtp_number_int": rtp_number_int,
            "rfc3339_timestamp": rfc3339_timestamp,
        }

    def _to_lpr_bbox_space(
        self, api_bbox: List[float] | None, stream_info: Dict[str, Any] | None
    ) -> List[float] | None:
        """Convert the lpr-server `bbox` to the configured space.

        Pixels by default -- see `lpr_bbox_coordinate_space`. lpr-server rounds
        this field to integer coordinates, so normalizing it before that server
        supports fractions collapses every alert box it publishes to 0x0.

        Fails open: with no frame dimensions the box is left in pixels. A wrong
        scale is recoverable, a dropped sighting is not.
        """
        if api_bbox is None or len(api_bbox) < 4:
            return api_bbox
        if getattr(self, "_lpr_bbox_space", "pixel") != "normalized":
            return api_bbox

        from ..utils.geometry_utils import resolve_frame_dims

        width, height = resolve_frame_dims(stream_info)
        if width <= 0 or height <= 0:
            return api_bbox
        try:
            return [
                round(float(api_bbox[0]) / width, 6),
                round(float(api_bbox[1]) / height, 6),
                round(float(api_bbox[2]) / width, 6),
                round(float(api_bbox[3]) / height, 6),
            ]
        except (TypeError, ValueError):
            return api_bbox

    @staticmethod
    def _build_lpr_stream_payload(ctx: Dict[str, Any], plate_text: str) -> Dict[str, Any]:
        """Project a request context onto the ``lpr-detections`` stream schema.

        Built from the same ``_build_lpr_request_context`` output the HTTP path uses,
        so the two transports cannot drift -- including the ``str(frame_id)`` coercion.

        The field names are snake_case and the plate key is ``license_plate``. That is
        not a guess: the binary carries both conventions (the camelCase set --
        ``licensePlate``/``frameId``/``rtpNumber`` -- belongs to the HTTP and Mongo
        DTOs), so it was settled by probe. A message keyed ``license_plate`` was
        consumed and reached alert evaluation; the same message keyed ``licensePlate``
        was read as an empty plate and skipped.
        """
        api_payload = ctx.get("payload") or {}
        payload: Dict[str, Any] = {
            "frame_id": ctx.get("frame_id", ""),
            "project_id": ctx.get("project_id", ""),
            "application_id": ctx.get("application_id", ""),
            "camera_id": ctx.get("camera_id", ""),
            "camera_name": ctx.get("camera_name", ""),
            "location": ctx.get("location", ""),
            "license_plate": plate_text,
            "rtp_number": ctx.get("rtp_number_int", 0),
            "timestamp": ctx.get("rfc3339_timestamp", ""),
            "stream_time": ctx.get("rfc3339_timestamp", ""),
        }
        bbox = api_payload.get("bbox")
        if bbox is not None:
            payload["bbox"] = bbox
        confidence = api_payload.get("ocr_confidence")
        if confidence is not None:
            payload["confidence"] = confidence
        return payload

    def publish_plate_sighting(
        self,
        plate_text: str,
        timestamp: str,
        stream_info: Dict[str, Any],
        bbox: Any = None,
        ocr_confidence: float | None = None,
    ) -> bool:
        """Publish one sighting to ``lpr-detections``. Create vs append is the server's call.

        ``processRedisMessage`` upserts the detection by ``(licensePlate, projectId,
        teamId)`` and calls ``AppendFrameID`` when it already exists, skipping frames
        already listed. So the client no longer has to know whether a plate is new --
        which is what the detection-id registry, the create-before-append
        serialisation and the in-flight cap all existed to arrange.

        No image is sent: the server extracts the frame itself from ``rtp_number``.
        """
        if self._plate_publisher is None:
            return False
        try:
            ctx = self._build_lpr_request_context(
                plate_text,
                timestamp,
                stream_info,
                image_data=None,
                bbox=bbox,
                ocr_confidence=ocr_confidence,
            )
            payload = self._build_lpr_stream_payload(ctx, plate_text)
            return self._plate_publisher.publish(payload, camera_id=ctx.get("camera_id", ""))
        except Exception as e:
            self.logger.error(
                "[LP_LOGGING] Publish plate sighting failed: plate=%s error=%s",
                plate_text,
                e,
                exc_info=True,
            )
            return False

    def _get_http_session(self, aiohttp_mod):
        """Return the shared aiohttp session, creating it lazily.

        The session must be created (and used) on the plate-sync sender loop;
        it is bound to whichever running loop first uses its connector.

        ``_post_timeout_s`` is read once, here, and baked into the session's
        ``ClientTimeout``: a later re-assignment does not reach an already-created
        session. See the ordering note in ``_initialize_plate_logger``.
        """
        session = self._http_session
        if session is None or session.closed:
            session = aiohttp_mod.ClientSession(timeout=aiohttp_mod.ClientTimeout(total=float(self._post_timeout_s)))
            self._http_session = session
        return session

    async def _pooled_post(self, session, url: str, headers: Dict[str, str], payload: Dict[str, Any]) -> Any:
        """POST once via the pooled session; mimic ``rpc.post_async`` semantics.

        Returns the parsed JSON body on 2xx; raises on non-2xx (same as the
        rpc path, whose exception is handled by the existing call sites).
        """
        async with session.post(url, json=payload, headers=headers, allow_redirects=True) as response:
            status = response.status
            try:
                body = await response.json(content_type=None)
            except Exception:
                body = await response.text()
            if status == 429:
                # Backpressure, not a fault: lpr-server is telling us to slow down.
                # Raised as a distinct type so callers can throttle instead of
                # logging a stack trace per rejected plate -- a dense-traffic frame
                # can make dozens of plates eligible at once, and treating each
                # rejection as an error buried the log in tracebacks.
                retry_after = 0.0
                header_value = response.headers.get("Retry-After")
                if header_value:
                    try:
                        retry_after = float(header_value)
                    except (TypeError, ValueError):
                        retry_after = 0.0
                raise _LprRateLimitedError(
                    f"LPR rate limited: url={url} response_body={body!r}",
                    retry_after=retry_after,
                )
            if not (200 <= status < 300):
                raise Exception(  # noqa: TRY002 - parity with rpc.post_async failure behavior
                    f"LPR pooled POST failed: status={status} url={url} response_body={body!r}"
                )
            return body

    async def _post_async_pooled(self, endpoint: str, payload: Dict[str, Any]) -> Any:
        """POST to the lpr-server reusing ONE shared aiohttp session.

        Replicates the auth preamble of ``matrice_common.rpc.async_send_request``
        (token refresh, bearer header, sdk_version header, projectId query
        param) but keeps the TCP connection pool alive across calls. On any
        structural failure (missing aiohttp, mocked/unusable rpc internals,
        non-string token, ...) it degrades to the legacy per-call
        ``session.rpc.post_async`` path instead of breaking plate logging.
        """
        try:
            import aiohttp

            rpc = self.session.rpc
            rpc.refresh_token()
            auth_token = rpc.AUTH_TOKEN
            auth_token.set_bearer_token()
            bearer = auth_token.bearer_token
            if not isinstance(bearer, str) or not bearer:
                raise TypeError("bearer token unavailable or not a string")
            url = rpc.add_project_id(f"{self.server_base_url}{endpoint}")
            if not isinstance(url, str):
                raise TypeError("request url is not a string")
            headers = {
                "Authorization": bearer,
                "sdk_version": str(getattr(rpc, "sdk_version", "0.0.0")),
            }
            http_session = self._get_http_session(aiohttp)
        except Exception as e:
            self.logger.warning(
                "[LP_LOGGING] Pooled HTTP path unavailable (%s: %s); falling back to session.rpc.post_async",
                type(e).__name__,
                e,
            )
            return await self.session.rpc.post_async(endpoint, payload=payload, base_url=self.server_base_url)

        try:
            return await self._pooled_post(http_session, url, headers, payload)
        except RuntimeError as e:
            # e.g. "Session is closed" / "Event loop is closed": recreate once.
            if "closed" not in str(e).lower():
                raise
            try:
                await http_session.close()
            except Exception:
                # Expected: the session/loop is already closed, which is why we are here.
                self.logger.debug("[LP_LOGGING] closing stale http session failed", exc_info=True)
            self._http_session = None
            http_session = self._get_http_session(aiohttp)
            return await self._pooled_post(http_session, url, headers, payload)
        except aiohttp.ClientConnectionError as e:  # noqa: F841 - reused in the nested handler
            # A pooled keep-alive connection the server had already closed: the
            # failure surfaces only when we try to reuse it, so the request never
            # reached lpr-server and retrying it once on a fresh connection is
            # safe. Retrying is also safe *semantically*: the create endpoint is
            # idempotent on (licensePlate, projectId, teamId), so a retry can
            # never duplicate a detection.
            #
            # Only RuntimeError("...closed") was handled before, which covers a
            # closed session/loop but not ServerDisconnectedError -- so every
            # server-side keep-alive expiry lost a detection outright.
            self.logger.debug(
                "[LP_LOGGING] Pooled connection dropped (%s: %s); retrying once on a fresh connection",
                type(e).__name__,
                e,
            )
            try:
                await http_session.close()
            except Exception:
                # Non-fatal: the session is dropped and rebuilt regardless.
                self.logger.debug("[LP_LOGGING] closing dropped http session failed", exc_info=True)
            self._http_session = None
            http_session = self._get_http_session(aiohttp)
            try:
                return await self._pooled_post(http_session, url, headers, payload)
            except aiohttp.ClientConnectionError as retry_exc:
                # Two dropped connections back to back is not a stale keep-alive,
                # it is the server refusing to serve. Convert to backpressure so it
                # feeds the same global pause as a 429 and is logged once per
                # window, instead of raising a per-plate traceback.
                raise _LprConnectionLostError(f"connection lost twice: {retry_exc}") from retry_exc

    async def aclose(self) -> None:
        """Close the shared aiohttp session (call from the loop that owns it)."""
        session = self._http_session
        self._http_session = None
        if session is not None and not session.closed:
            try:
                await session.close()
            except Exception:
                # Non-fatal: the reference is already dropped, so the session cannot leak.
                self.logger.debug("[LP_LOGGING] aclose of http session failed", exc_info=True)

    def note_rate_limited(self, retry_after: float = 0.0, plate_text: str = "") -> None:
        """Record a 429 and open a global send window in the future.

        Backoff doubles from ``_RATE_LIMIT_BACKOFF_MIN_S`` while rejections keep
        arriving and is capped at ``_RATE_LIMIT_BACKOFF_MAX_S``; ``note_send_ok``
        clears it. The server's ``Retry-After`` wins when it sends one.

        The warning is rate-limited to one line per backoff window: a single dense
        frame can reject dozens of plates, and one log line per rejection is what
        turned ordinary backpressure into a wall of tracebacks.
        """
        now = time.monotonic()
        if retry_after > 0:
            wait = retry_after
            self._rate_limit_backoff_s = min(retry_after, _RATE_LIMIT_BACKOFF_MAX_S)
        else:
            self._rate_limit_backoff_s = (
                _RATE_LIMIT_BACKOFF_MIN_S
                if self._rate_limit_backoff_s <= 0
                else min(self._rate_limit_backoff_s * 2.0, _RATE_LIMIT_BACKOFF_MAX_S)
            )
            wait = self._rate_limit_backoff_s
        self._rate_limited_until = max(self._rate_limited_until, now + wait)

        if now - self._last_rate_limit_warn_ts >= wait:
            self._last_rate_limit_warn_ts = now
            self.logger.warning(
                "[LP_LOGGING] lpr-server pushing back (429 / connection loss); pausing plate sync for %.1fs%s",
                wait,
                f" (latest plate={plate_text})" if plate_text else "",
            )

    def note_send_failed(self, reason: str = "") -> None:
        """Record a failed POST and open the send window once failures are consecutive.

        The 429 path above only opens on explicit push-back or repeated connection
        loss. A plainly broken server -- a timeout, a 500, or the 404 the missing
        ``view-frames`` route produced for weeks -- never tripped it, so every plate
        kept paying a full round trip to a service that could not answer. After
        ``_SEND_FAILURE_BREAKER_THRESHOLD`` consecutive failures this reuses the same
        backoff window, and a single success clears it.
        """
        self._consecutive_send_failures += 1
        if self._consecutive_send_failures < _SEND_FAILURE_BREAKER_THRESHOLD:
            return
        now = time.monotonic()
        self._send_failure_backoff_s = (
            _SEND_FAILURE_BREAKER_MIN_S
            if self._send_failure_backoff_s <= 0
            else min(self._send_failure_backoff_s * 2.0, _SEND_FAILURE_BREAKER_MAX_S)
        )
        self._rate_limited_until = max(self._rate_limited_until, now + self._send_failure_backoff_s)
        # One line per backoff window, same as note_rate_limited: a broken server fails
        # every plate, and one line per plate is what buried the useful signal before.
        if now - self._last_send_failure_warn_ts >= self._send_failure_backoff_s:
            self._last_send_failure_warn_ts = now
            self.logger.warning(
                "[LP_LOGGING] %d consecutive lpr-server POST failures; pausing plate sync for %.1fs%s",
                self._consecutive_send_failures,
                self._send_failure_backoff_s,
                f" (last error: {reason})" if reason else "",
            )

    def note_send_ok(self) -> None:
        """A POST succeeded: forget the accumulated 429 and failure backoff."""
        self._rate_limit_backoff_s = 0.0
        self._consecutive_send_failures = 0
        self._send_failure_backoff_s = 0.0

    def rate_limit_wait_s(self) -> float:
        """Seconds the caller should hold off before the next POST (0.0 == send now)."""
        if self._rate_limited_until <= 0.0:
            return 0.0
        remaining = self._rate_limited_until - time.monotonic()
        if remaining <= 0.0:
            self._rate_limited_until = 0.0
            return 0.0
        return remaining

    async def _execute_lpr_api_call(
        self,
        method: str,
        endpoint: str,
        payload: Dict[str, Any],
        plate_text: str,
        action_label: str,
    ) -> Any:
        """Execute an lpr-server RPC call with concise request/response logging."""
        full_url = f"{self.server_base_url}{endpoint}"

        response = await self._post_async_pooled(endpoint, payload)

        response_status = _lpr_api_response_status(response)
        if not _lpr_api_response_is_success(response_status, response):
            self.logger.warning(
                "[LP_LOGGING] API %s failed (%s): url=%s status=%s plate=%s response=%s",
                method,
                action_label,
                full_url,
                response_status if response_status is not None else "unknown",
                plate_text,
                _format_lpr_api_response_for_log(response),
            )
            return None

        self.logger.info(
            "[LP_LOGGING] API %s ok (%s): plate=%s status=%s response=%s",
            method,
            action_label,
            plate_text,
            response_status,
            _format_lpr_api_response_for_log(response),
        )
        return response

    async def log_plate(
        self,
        plate_text: str,
        timestamp: str,
        stream_info: Dict[str, Any],
        image_data: str | None = None,
        bbox: Any = None,
        ocr_confidence: float | None = None,
    ) -> str | None:
        """Create a new lpr-server detection for a plate not yet in the detection list.

        Returns:
            The new detection document id on success, otherwise ``None``.

            In ``redis`` publish mode there is no response to read an id from, so a
            sentinel (``_PUBLISHED_MARKER``) is returned instead. Callers only use the
            return value to decide "have I registered this plate", and the server does
            the create-vs-append decision itself, so the real id is not needed.
        """
        if self._publish_mode == "redis":
            ok = self.publish_plate_sighting(
                plate_text,
                timestamp,
                stream_info,
                bbox=bbox,
                ocr_confidence=ocr_confidence,
            )
            return _PUBLISHED_MARKER if ok else None
        try:
            ctx = self._build_lpr_request_context(
                plate_text,
                timestamp,
                stream_info,
                image_data=image_data,
                bbox=bbox,
                ocr_confidence=ocr_confidence,
            )
            payload = ctx["payload"]
            project_id = ctx["project_id"]

            endpoint = f"/v1/lpr-server/detections?projectId={project_id}"
            response = await self._execute_lpr_api_call(
                "POST",
                endpoint,
                payload,
                plate_text,
                action_label="create_detection",
            )
            if response is None:
                return None

            detection_id = _extract_lpr_detection_id(response)
            self.note_send_ok()
            self.logger.info(
                "[LP_LOGGING] Created detection plate=%s detection_id=%s camera=%s",
                plate_text,
                detection_id,
                ctx.get("camera_name", ""),
            )
            return detection_id or None

        except _LprBackpressureError as e:
            # Expected backpressure (429 or repeated connection loss) -- pace and
            # move on; no stack trace, one warning per backoff window.
            self.note_rate_limited(e.retry_after, plate_text)
            return None
        except Exception as e:
            err_status = _lpr_api_response_status(getattr(e, "response", None))
            if err_status is None:
                raw_status = getattr(e, "status_code", None)
                if raw_status is not None:
                    try:
                        err_status = int(raw_status)
                    except (TypeError, ValueError):
                        err_status = None
            self.note_send_failed(f"create status={err_status if err_status is not None else 'unknown'}")
            self.logger.error(
                "[LP_LOGGING] Create detection failed: plate=%s status=%s error=%s",
                plate_text,
                err_status if err_status is not None else "unknown",
                e,
                exc_info=True,
            )
            return None

    async def append_view_frame(
        self,
        detection_id: str,
        plate_text: str,
        timestamp: str,
        stream_info: Dict[str, Any],
        image_data: str | None = None,
        bbox: Any = None,
        ocr_confidence: float | None = None,
    ) -> bool:
        """Record a further sighting of a plate that already has an lpr-server detection.

        This posts to the **create** endpoint, not to a dedicated append route.
        ``POST /v1/lpr-server/detections`` is idempotent on
        ``(licensePlate, projectId, teamId)``: when the plate already has a detection
        the server resolves it via ``FindOneByLicensePlateProjectAndTeam``, pulls the
        frame for ``rtpNumber`` from the media server, stores a Frame document and
        appends its id to the existing detection's ``frameIds``. It does not insert a
        second detection -- verified against a live server: 231 detection documents,
        231 distinct plates, zero duplicates, 149 of them holding more than one frame.

        The previous implementation posted to
        ``POST /v1/lpr-server/detections/{id}/view-frames``, which **no lpr-server build
        has ever implemented** -- there is no such route, handler or DTO in the service,
        and the strings ``view-frames``/``viewFrame`` do not occur anywhere in its
        binary. Every call returned ``404 page not found``, raised, and logged a full
        traceback, so a view frame was only ever recorded on the one sighting per
        process where ``_registered_plate_detections`` was still empty and the CREATE
        branch ran -- i.e. once per container restart, instead of once per
        ``append_min_interval_s``. The dedicated call was therefore both broken and
        redundant.

        ``detection_id`` is retained for logging and for the sender's create/append
        routing; the server resolves the target detection from the plate itself.

        In ``redis`` publish mode create and append collapse into a single message
        type -- which is what the stream consumer already expects, since it upserts
        and calls ``AppendFrameID`` on its own.
        """
        if not detection_id:
            return False

        if self._publish_mode == "redis":
            return self.publish_plate_sighting(
                plate_text,
                timestamp,
                stream_info,
                bbox=bbox,
                ocr_confidence=ocr_confidence,
            )

        try:
            # ``image_data`` is deliberately NOT forwarded on a repeat sighting.
            # lpr-server does not persist the posted bytes for a view frame: it
            # extracts the frame itself from the media server by ``rtpNumber`` and
            # stores the resulting URL, which is why every stored Frame carries an
            # ``imageUrl`` of the form
            # ``.../v1/storage/images/<acct>/<camera>/lpr/<date>/<rtp>.jpg`` and no
            # inline image. Sending the ~200 KB base64 JPEG anyway made each append
            # a large-body POST for no gain and was the practical cause of the
            # ``ServerDisconnectedError`` bursts on the shared keep-alive session.
            # The first sighting still sends it (see ``log_plate``).
            ctx = self._build_lpr_request_context(
                plate_text,
                timestamp,
                stream_info,
                image_data=None,
                bbox=bbox,
                ocr_confidence=ocr_confidence,
            )
            project_id = ctx["project_id"]

            # Same endpoint and payload shape as log_plate(): the server decides
            # create-vs-append itself, so the two calls are deliberately identical
            # on the wire apart from the omitted image.
            endpoint = f"/v1/lpr-server/detections?projectId={project_id}"
            response = await self._execute_lpr_api_call(
                "POST",
                endpoint,
                ctx["payload"],
                plate_text,
                action_label="append_view_frame",
            )
            if response is None:
                return False

            self.note_send_ok()
            self.logger.info(
                "[LP_LOGGING] Appended view frame plate=%s detection_id=%s rtp=%s",
                plate_text,
                detection_id,
                ctx["rtp_number_int"],
            )
            return True

        except _LprBackpressureError as e:
            # Expected backpressure (429 or repeated connection loss) -- pace and
            # move on; no stack trace, one warning per backoff window.
            self.note_rate_limited(e.retry_after, plate_text)
            return False
        except Exception as e:
            # Before the log, so the breaker trips on the same failure that produced
            # the line rather than one plate later.
            self.note_send_failed("append")
            self.logger.error(
                "[LP_LOGGING] Append view frame failed: plate=%s detection_id=%s error=%s",
                plate_text,
                detection_id,
                e,
                exc_info=True,
            )
            return False


def _extract_stream_frame_fields(stream_info: Dict[str, Any] | None) -> Tuple[str, str]:
    """Return ``(frame_id, rtp_number)`` from stream_info with input_settings fallback."""
    if not stream_info:
        return "", ""
    input_settings = (
        stream_info.get("input_settings", {}) if isinstance(stream_info.get("input_settings", {}), dict) else {}
    )
    frame_id = (
        stream_info.get("frame_id", "")
        or stream_info.get("frameId", "")
        or input_settings.get("frame_id", "")
        or input_settings.get("frameId", "")
        or ""
    )
    rtp_number = (
        stream_info.get("rtp_number", "")
        or stream_info.get("rtpNumber", "")
        or input_settings.get("rtp_number", "")
        or input_settings.get("rtpNumber", "")
        or ""
    )
    return str(frame_id), str(rtp_number)


def _snapshot_stream_info_for_plate(
    stream_info: Dict[str, Any] | None,
    frame_id_override: str = "",
    rtp_number_override: str = "",
) -> Dict[str, Any]:
    """Shallow-copy stream_info with frame_id/rtp_number frozen for plate CREATE/alert.

    ``*_override`` -- when the winning detection is a ``_smoothed`` carry-forward, its bbox is
    from an earlier frame than ``stream_info`` (the current call). Callers that already know the
    bbox's true frame (``_build_plate_create_anchor``, from ``plate_meta``) must pass it here, or
    this snapshot -- which the lpr-server CREATE/append payload reads via
    ``anchor["stream_info"]`` -- would freeze the CURRENT frame's identity regardless, silently
    undoing that correction for the lpr-server channel even though ``_send_instant_alerts``' own
    ``anchor["frame_id"]``/``anchor["rtp_number"]`` read got it right.
    """
    if not stream_info:
        return {}
    frame_id, rtp_number = _extract_stream_frame_fields(stream_info)
    frame_id = frame_id_override or frame_id
    rtp_number = rtp_number_override or rtp_number
    snap: Dict[str, Any] = dict(stream_info)
    snap["frame_id"] = frame_id
    snap["rtp_number"] = rtp_number
    raw_settings = stream_info.get("input_settings", {})
    if isinstance(raw_settings, dict):
        settings = dict(raw_settings)
        settings["frame_id"] = frame_id
        settings["rtp_number"] = rtp_number
        snap["input_settings"] = settings
    return snap


def _parse_lpr_stream_wallclock(value: Any) -> datetime | None:
    """Parse a stream wall-clock timestamp string into an aware UTC datetime.

    Accepts the pipeline's ``YYYY-MM-DD-HH:MM:SS.ffffff UTC`` form (with or
    without fractional seconds / ``UTC`` suffix) plus ISO-8601 as a fallback.
    Returns ``None`` when unparsable.
    """
    if not value or not isinstance(value, str):
        return None
    cleaned = value.replace(" UTC", "").strip()
    for fmt in ("%Y-%m-%d-%H:%M:%S.%f", "%Y-%m-%d-%H:%M:%S"):
        try:
            return datetime.strptime(cleaned, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    try:
        parsed = datetime.fromisoformat(cleaned)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


class _PlateSyncSender:
    """Bounded background sender for lpr-server plate create/append POSTs.

    The producer (``process()``) offers per-plate payload "slots" via
    :meth:`offer_batch`, which is non-blocking and thread-safe. Coalescing
    policy is asymmetric:

    * **CREATE** (key absent from registry): **first-frame-wins** — the first
      offered payload for a pending create is kept so the lpr-server/BOLO
      thumbnail matches the first confirmed sighting, not a later frame where
      the vehicle may have moved on.
    * **APPEND** (key present in registry): **latest-frame-wins** — view-frame
      updates may use the freshest frame (subject to staleness cap).

    A dedicated daemon thread runs its own asyncio loop that drains the slots
    subject to:

    * at most one outstanding operation per registry key (serializes
      create-before-append; kills duplicate creates during create latency);
    * a global ``max_in_flight`` semaphore;
    * a per-key ``append_min_interval_s`` rate limit (also used as the
      failed-create backoff);
    * a staleness rule: appends whose frame is older than ``max_frame_age_s``
      are dropped silently; creates are NEVER dropped for staleness.

    ``registry`` is the use case's ``_registered_plate_detections`` dict held
    BY REFERENCE (never rebound): key present -> append, absent -> create.
    """

    _WARN_INTERVAL_S = 10.0

    def __init__(
        self,
        plate_logger,
        registry: Dict[str, str],
        *,
        max_in_flight: int = 2,
        append_min_interval_s: float = 5.0,
        max_frame_age_s: float = 5.0,
        max_pending_slots: int = 32,
    ):
        self.logger = logging.getLogger(__name__)
        self._plate_logger = plate_logger
        self._registry = registry  # shared with the use case, by reference
        self._max_in_flight = max(1, int(max_in_flight))
        self._append_min_interval_s = float(append_min_interval_s)
        self._max_frame_age_s = float(max_frame_age_s)
        self._max_pending_slots = max(1, int(max_pending_slots))

        # ALL mutable coordination state below is guarded by this one lock.
        self._lock = threading.Lock()
        self._slots: Dict[str, dict] = {}  # key -> latest pending payload
        self._slot_order: "OrderedDict[str, None]" = OrderedDict()  # key -> None, oldest-updated first
        self._inflight: set = set()  # keys with an outstanding create/append
        self._next_ok_ts: Dict[str, float] = {}  # key -> monotonic earliest-next-send
        self._last_warn_ts: Dict[str, float] = {}

        self._thread: threading.Thread | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._loop_ready = threading.Event()
        self._stopped = False
        self._wake: asyncio.Event | None = None
        self._semaphore: asyncio.Semaphore | None = None
        # Strong refs to in-flight send tasks (loop only holds weak refs).
        self._send_tasks: set = set()

        # Best-effort counters (diagnostics only)
        self._n_created = 0
        self._n_appended = 0
        self._n_failed = 0
        self._n_dropped_stale = 0
        self._n_evicted = 0

    # ------------------------------------------------------------------ #
    # Producer-side API (any thread)
    # ------------------------------------------------------------------ #

    def start(self) -> None:
        """Start the sender thread (idempotent). Pre-start offers are drained."""
        if self._thread is not None and self._thread.is_alive():
            return
        self._stopped = False
        self._loop_ready.clear()
        self._thread = threading.Thread(target=self._thread_main, name="lpr-plate-sync", daemon=True)
        self._thread.start()

    def offer_batch(self, items: List[Tuple[str, dict]]) -> Dict[str, str]:
        """Offer per-key payloads; non-blocking (lock + dict ops only).

        CREATE (registry miss): first-frame-wins — a pending create slot is not
        replaced by later offers. APPEND (registry hit): latest-frame-wins.

        Returns per-key dispositions: "queued" / "coalesced" / "held_create"
        (evicted keys, if any, are reported as "evicted_oldest").
        """
        dispositions: Dict[str, str] = {}
        with self._lock:
            if self._stopped:
                return {key: "stopped" for key, _ in items}
            for key, payload in items:
                is_create = key not in self._registry
                if key in self._slots:
                    if is_create:
                        # Keep the first confirmed-sighting frame for BOLO/create.
                        dispositions[key] = "held_create"
                        continue
                    dispositions[key] = "coalesced"
                else:
                    dispositions[key] = "queued"
                    while len(self._slots) >= self._max_pending_slots:
                        evicted_key, _ = self._slot_order.popitem(last=False)
                        self._slots.pop(evicted_key, None)
                        dispositions[evicted_key] = "evicted_oldest"
                        self._n_evicted += 1
                        self._warn_rate_limited(
                            "slot_evict",
                            f"[LP_LOGGING] Plate sync slot cap ({self._max_pending_slots}) reached; "
                            f"evicted oldest pending plate sync (total evicted={self._n_evicted})",
                        )
                self._slots[key] = payload
                self._slot_order.pop(key, None)
                self._slot_order[key] = None
        self._wake_loop()
        return dispositions

    def reset_state(self) -> None:
        """Clear pending slots and rate-limit state (NOT the shared registry)."""
        with self._lock:
            self._slots.clear()
            self._slot_order.clear()
            self._next_ok_ts.clear()

    def stop(self, timeout: float = 5.0) -> None:
        """Stop the sender: best-effort flush of pending CREATES, then join."""
        with self._lock:
            self._stopped = True
            pending_creates = [(key, self._slots[key]) for key in list(self._slots) if key not in self._registry]
            self._slots.clear()
            self._slot_order.clear()
        thread = self._thread
        deadline = time.monotonic() + max(0.1, float(timeout))
        if thread is not None and thread.is_alive():
            # The loop may still be starting up; wait for the ready handshake so
            # we can drain and stop it instead of timing out on join below.
            self._loop_ready.wait(timeout=min(1.0, max(0.1, float(timeout) / 2)))
        loop = self._loop
        if loop is not None and not loop.is_closed() and thread is not None and thread.is_alive():
            drain_budget = max(0.1, deadline - time.monotonic() - 0.5)
            try:
                future = asyncio.run_coroutine_threadsafe(self._drain_on_stop(pending_creates, drain_budget), loop)
                future.result(timeout=drain_budget + 0.5)
            except Exception:
                # Shutdown continues, but queued plates may not have been flushed.
                self.logger.warning("[LP_LOGGING] drain-on-stop incomplete; plates may be lost", exc_info=True)
            try:
                loop.call_soon_threadsafe(loop.stop)
            except Exception:
                # Non-fatal: the loop is already stopping/closed; the join below still bounds us.
                self.logger.debug("[LP_LOGGING] could not signal sender loop to stop", exc_info=True)
        if thread is not None:
            thread.join(max(0.1, deadline - time.monotonic()))

    # ------------------------------------------------------------------ #
    # Sender-loop internals
    # ------------------------------------------------------------------ #

    def _thread_main(self) -> None:
        loop = None
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self._loop = loop
            self._wake = asyncio.Event()
            self._semaphore = asyncio.Semaphore(self._max_in_flight)
            runner = loop.create_task(self._run())
            self._loop_ready.set()
            loop.run_forever()
            runner.cancel()
            pending = [task for task in asyncio.all_tasks(loop) if not task.done()]
            if pending:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        except Exception as e:
            self.logger.error(f"[LP_LOGGING] Plate sync sender thread died: {e}", exc_info=True)
        finally:
            self._loop_ready.set()
            if loop is not None:
                try:
                    loop.close()
                except Exception:
                    # Non-fatal: thread is exiting; the loop is unreachable either way.
                    self.logger.debug("[LP_LOGGING] closing sender loop failed", exc_info=True)

    def _wake_loop(self) -> None:
        loop = self._loop
        if loop is None or not self._loop_ready.is_set():
            # Not started yet: slots are drained once the loop comes up.
            return
        if loop.is_closed() or self._stopped:
            self._warn_rate_limited(
                "loop_dead",
                "[LP_LOGGING] Plate sync loop is stopped/closed; offered plates will not be sent",
            )
            return
        try:
            loop.call_soon_threadsafe(self._wake.set)
        except RuntimeError:
            self._warn_rate_limited(
                "loop_dead",
                "[LP_LOGGING] Plate sync loop rejected wake-up; offered plates will not be sent",
            )

    def _warn_rate_limited(self, tag: str, message: str) -> None:
        now = time.monotonic()
        if now - self._last_warn_ts.get(tag, 0.0) >= self._WARN_INTERVAL_S:
            self._last_warn_ts[tag] = now
            self.logger.warning(message)

    def _payload_age_s(self, payload: dict, now_monotonic: float) -> float:
        """Frame age in seconds: stream wall-clock ref, else time-in-queue."""
        parsed = _parse_lpr_stream_wallclock(payload.get("frame_age_ref"))
        if parsed is not None:
            return max(0.0, (datetime.now(timezone.utc) - parsed).total_seconds())
        enq = payload.get("enq_monotonic")
        if isinstance(enq, (int, float)):
            return max(0.0, now_monotonic - float(enq))
        return 0.0

    def _pop_ready_jobs(self) -> Tuple[List[Tuple[str, dict]], float | None]:
        """Pop sendable jobs; return them plus the earliest retry delta (s)."""
        now = time.monotonic()
        ready: List[Tuple[str, dict]] = []
        earliest_delta: float | None = None

        # Global gate: while lpr-server is rate limiting us, dispatch nothing at
        # all. The per-key next_ok below is unaware of the other keys, so without
        # this a burst of newly-eligible plates walks straight back into the 429.
        # Slots are left in place and retried once the window opens.
        wait_s = getattr(self._plate_logger, "rate_limit_wait_s", None)
        if callable(wait_s):
            remaining = wait_s()
            if remaining > 0:
                return [], remaining

        with self._lock:
            for key in list(self._slots.keys()):
                if key in self._inflight:
                    continue
                next_ok = self._next_ok_ts.get(key, 0.0)
                if now < next_ok:
                    delta = next_ok - now
                    earliest_delta = delta if earliest_delta is None else min(earliest_delta, delta)
                    continue
                payload = self._slots[key]
                if key in self._registry and self._payload_age_s(payload, now) > self._max_frame_age_s:
                    # Stale APPEND: drop silently. Creates are never dropped.
                    del self._slots[key]
                    self._slot_order.pop(key, None)
                    self._n_dropped_stale += 1
                    continue
                del self._slots[key]
                self._slot_order.pop(key, None)
                self._inflight.add(key)
                ready.append((key, payload))
        return ready, earliest_delta

    async def _run(self) -> None:
        loop = asyncio.get_event_loop()
        while not self._stopped:
            try:
                try:
                    await asyncio.wait_for(self._wake.wait(), timeout=0.5)
                except (TimeoutError, asyncio.TimeoutError):  # noqa: UP041 - asyncio alias needed on py<3.11
                    pass
                self._wake.clear()
                if self._stopped:
                    break
                ready, earliest_delta = self._pop_ready_jobs()
                if earliest_delta is not None:
                    loop.call_later(earliest_delta, self._wake.set)
                for key, payload in ready:
                    await self._semaphore.acquire()
                    task = loop.create_task(self._send(key, payload))
                    self._send_tasks.add(task)
                    task.add_done_callback(self._send_tasks.discard)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"[LP_LOGGING] Plate sync run loop error: {e}", exc_info=True)
                await asyncio.sleep(0.5)

    async def _send(self, key: str, payload: dict) -> None:
        """Send one create/append for ``key``. Must never raise."""
        try:
            if key not in self._registry:
                detection_id = None
                try:
                    detection_id = await self._plate_logger.log_plate(**payload["create_kwargs"])
                except Exception as e:
                    self.logger.error(
                        f"[LP_LOGGING] Plate sync create raised for key={key!r}: {e}",
                        exc_info=True,
                    )
                if detection_id:
                    self._registry[key] = detection_id
                    self._n_created += 1
                    with self._lock:
                        self._next_ok_ts[key] = time.monotonic() + self._append_min_interval_s
                else:
                    # Failed create: back off and keep the slot so the create
                    # naturally retries (with a fresher frame when one arrives).
                    # NEVER convert to an append.
                    self._n_failed += 1
                    with self._lock:
                        self._next_ok_ts[key] = time.monotonic() + self._append_min_interval_s
                        if key not in self._slots:
                            self._slots[key] = payload
                            self._slot_order.pop(key, None)
                            self._slot_order[key] = None
            else:
                ok = False
                try:
                    ok = await self._plate_logger.append_view_frame(
                        detection_id=self._registry[key],
                        **payload["append_kwargs"],
                    )
                except Exception as e:
                    self.logger.error(
                        f"[LP_LOGGING] Plate sync append raised for key={key!r}: {e}",
                        exc_info=True,
                    )
                if ok:
                    self._n_appended += 1
                else:
                    self._n_failed += 1
                with self._lock:
                    self._next_ok_ts[key] = time.monotonic() + self._append_min_interval_s
        except Exception as e:
            self.logger.error(f"[LP_LOGGING] Plate sync send error for key={key!r}: {e}", exc_info=True)
        finally:
            with self._lock:
                self._inflight.discard(key)
                slot_pending = key in self._slots
            try:
                self._semaphore.release()
            except Exception:
                # A failed release would permanently shrink send concurrency - worth seeing.
                self.logger.warning("[LP_LOGGING] semaphore release failed key=%r", key, exc_info=True)
            if slot_pending and self._wake is not None:
                self._wake.set()

    async def _drain_on_stop(self, pending_creates: List[Tuple[str, dict]], budget_s: float) -> None:
        """Best-effort flush of pending creates + logger session close on stop."""
        deadline = time.monotonic() + max(0.05, budget_s)
        # Let in-flight sends settle first so we don't duplicate creates.
        while time.monotonic() < deadline:
            with self._lock:
                if not self._inflight:
                    break
            await asyncio.sleep(0.02)
        for key, payload in pending_creates:
            if time.monotonic() >= deadline:
                break
            if key in self._registry:
                continue
            try:
                detection_id = await self._plate_logger.log_plate(**payload["create_kwargs"])
                if detection_id:
                    self._registry[key] = detection_id
            except Exception:
                # This plate is dropped; the drain continues with the rest.
                self.logger.warning("[LP_LOGGING] drain-on-stop plate failed key=%r", key, exc_info=True)
        try:
            aclose = getattr(self._plate_logger, "aclose", None)
            if aclose is not None:
                await aclose()
        except Exception:
            # Non-fatal: teardown is best-effort at this point.
            self.logger.debug("[LP_LOGGING] plate logger aclose failed", exc_info=True)


class _DetectionSmoother:
    """Temporal smoothing: carry forward tracked detections for a few frames to reduce flickering.

    When the model intermittently drops a detection for 1-2 frames, the overlay
    blinks on the frontend.  This buffer carries the last-known position forward
    with decaying confidence until the model picks it up again (or the hold
    window expires).
    """

    def __init__(self, hold_frames: int = 3, iou_threshold: float = 0.3):
        self._buffers: Dict[str, Dict] = {}  # camera_id -> {track_key: {det, last_seen, miss_count}}
        self._hold_frames = hold_frames
        self._iou_threshold = iou_threshold

    @staticmethod
    def _iou(a: dict, b: dict) -> float:
        x1 = max(a["xmin"], b["xmin"])
        y1 = max(a["ymin"], b["ymin"])
        x2 = min(a["xmax"], b["xmax"])
        y2 = min(a["ymax"], b["ymax"])
        inter = max(0, x2 - x1) * max(0, y2 - y1)
        if inter == 0:
            return 0.0
        a1 = (a["xmax"] - a["xmin"]) * (a["ymax"] - a["ymin"])
        a2 = (b["xmax"] - b["xmin"]) * (b["ymax"] - b["ymin"])
        return inter / (a1 + a2 - inter) if (a1 + a2 - inter) > 0 else 0.0

    def smooth(
        self,
        camera_id: str,
        detections: list,
        frame_idx: int,
        frame_id: str = "",
        rtp_number: str = "",
    ) -> list:
        """Merge current detections with buffered ones.  Returns smoothed list.

        ``frame_id``/``rtp_number`` identify *this* call's frame (the caller's
        ``stream_info``, extracted once up front -- this class has no other way to
        know which frame a buffered bbox actually came from). They are stored
        alongside each buffer entry so a later carry-forward can stamp the held
        bbox with the frame it was TRUE for, instead of the frame it's being
        replayed on -- see the carry-forward loop below and
        ``_stamp_detections_frame_ids``, which relies on a ``_smoothed`` detection
        already carrying correct identity and skips it rather than overwriting.
        """
        buf = self._buffers.setdefault(camera_id, {})

        matched_keys: set = set()
        for det in detections:
            bb = det.get("bounding_box", {})
            if not bb or "xmin" not in bb:
                continue
            tid = det.get("track_id", "")
            # Exact track_id match (persistent IDs only)
            if tid and not str(tid).startswith("simple_") and tid in buf:
                buf[tid] = {
                    "det": dict(det),
                    "last_seen": frame_idx,
                    "miss_count": 0,
                    "frame_id": frame_id,
                    "rtp_number": rtp_number,
                }
                matched_keys.add(tid)
                continue
            # IoU fallback
            best_key, best_iou = None, 0.0
            for key, entry in buf.items():
                if key in matched_keys:
                    continue
                ebb = entry["det"].get("bounding_box", {})
                if ebb and "xmin" in ebb:
                    iou = self._iou(bb, ebb)
                    if iou > best_iou:
                        best_iou = iou
                        best_key = key
            if best_key and best_iou > self._iou_threshold:
                buf[best_key]["det"] = dict(det)
                buf[best_key]["det"]["track_id"] = best_key
                buf[best_key]["last_seen"] = frame_idx
                buf[best_key]["miss_count"] = 0
                buf[best_key]["frame_id"] = frame_id
                buf[best_key]["rtp_number"] = rtp_number
                matched_keys.add(best_key)
            else:
                key = tid if tid and not str(tid).startswith("simple_") else f"s_{frame_idx}_{id(det)}"
                buf[key] = {
                    "det": dict(det),
                    "last_seen": frame_idx,
                    "miss_count": 0,
                    "frame_id": frame_id,
                    "rtp_number": rtp_number,
                }
                matched_keys.add(key)

        # Carry forward missing detections
        carried: list = []
        expired: list = []
        for key, entry in buf.items():
            if key in matched_keys:
                continue
            entry["miss_count"] += 1
            if entry["miss_count"] <= self._hold_frames:
                carry_det = dict(entry["det"])
                orig_conf = carry_det.get("confidence", 0.5)
                carry_det["confidence"] = round(max(0.1, orig_conf - 0.05 * entry["miss_count"]), 2)
                # Private marker: this bbox is a carried-forward copy, not a
                # detection from the current frame. Downstream consumers that
                # must re-localize per frame (e.g. _count_categories) use it
                # to prefer real detections over held ones.
                carry_det["_smoothed"] = True
                # Stamp with the frame this bbox was actually TRUE for (the last
                # real sighting), not the frame it's being replayed on now --
                # otherwise a downstream alert/lpr-server payload built from this
                # bbox would claim a frame identity the bbox doesn't match (the
                # "matches the previous ~2 RTP" defect).
                if entry.get("frame_id"):
                    carry_det["frame_id"] = entry["frame_id"]
                if entry.get("rtp_number"):
                    carry_det["rtp_number"] = entry["rtp_number"]
                carried.append(carry_det)
            else:
                expired.append(key)
        for key in expired:
            del buf[key]

        return detections + carried


def _map_tracker_ids_to_source(source_data: list, tracked_data: list) -> None:
    """Write persistent track IDs from *tracked_data* back into the original *source_data* dicts (in-place).

    After ``tracker.update()`` returns **new** detection dicts with ``track_id``
    assigned, the original model-output dicts (``source_data``) still lack IDs.
    This function matches each source detection to its tracked counterpart via
    bounding-box IoU and copies the ``track_id`` over so that callers who hold a
    reference to the original list (e.g. workers.py → ``format_output_rtp``)
    automatically see the correct IDs.
    """
    if not tracked_data:
        return
    for src in source_data:
        sbb = src.get("bounding_box", src.get("bbox", {}))
        if not sbb or "xmin" not in sbb:
            continue
        best_iou, best_tid = 0.0, None
        for trk in tracked_data:
            tid = trk.get("track_id")
            tbb = trk.get("bounding_box", trk.get("bbox", {}))
            if tid is None or not tbb or "xmin" not in tbb:
                continue
            x1 = max(float(sbb["xmin"]), float(tbb["xmin"]))
            y1 = max(float(sbb["ymin"]), float(tbb["ymin"]))
            x2 = min(float(sbb["xmax"]), float(tbb["xmax"]))
            y2 = min(float(sbb["ymax"]), float(tbb["ymax"]))
            inter = max(0, x2 - x1) * max(0, y2 - y1)
            if inter == 0:
                continue
            a1 = (float(sbb["xmax"]) - float(sbb["xmin"])) * (float(sbb["ymax"]) - float(sbb["ymin"]))
            a2 = (float(tbb["xmax"]) - float(tbb["xmin"])) * (float(tbb["ymax"]) - float(tbb["ymin"]))
            iou = inter / (a1 + a2 - inter) if (a1 + a2 - inter) > 0 else 0
            if iou > best_iou:
                best_iou = iou
                best_tid = tid
        if best_tid is not None and best_iou > 0.3:
            src["track_id"] = best_tid


# Thread-local shared holder for the most recent raw BGR frame. The inference
# pipeline sets the frame on one use-case instance via set_bgr_frame() but may
# run process() on a *different* cached instance (a single holder reused across
# the use-case cache), so a per-instance attribute alone loses the frame. The
# thread-local bridges set->read within one worker thread while keeping
# concurrent camera worker threads isolated from each other's frames.
_BGR_FRAME_TLS = threading.local()

# Platforms where OCR is expected to run on the GPU. On these, OCR binding to
# CPU-only is a degradation (or, with MATRICE_OCR_REQUIRE_GPU=1, a hard error).
_GPU_REQUIRED_PLATFORMS = frozenset({"gpu", "thor", "orin", "blackwell"})
# ONNXRuntime execution providers that count as "on GPU".
_GPU_EXECUTION_PROVIDERS = frozenset({"TensorrtExecutionProvider", "CUDAExecutionProvider"})


def _preferred_ocr_providers() -> tuple:
    """ORT execution-provider precedence for the plate OCR model.

    CUDA is first by default. The TensorRT EP rebuilds its engine from the ONNX
    on every process start (no TRT engine cache is persisted for this model),
    which measured >120s on the H100 LPR deployment and blew the OCR subprocess
    ``ready_timeout`` (60s at the time, 15s since ANA-21) on every attempt -- so
    the GPU OCR worker never came up ("OCR worker read timed out"), every plate
    went un-OCR'd, and the monitoring use case emitted empty
    ``tracking_stats.detections`` (no VMS overlays). The CUDA EP builds the same
    model in ~3s, which is what that budget is sized for. Set
    ``MATRICE_OCR_ENABLE_TRT=1`` to restore TRT-first once an engine cache is
    wired up -- and raise ``MATRICE_OCR_READY_TIMEOUT_S`` /
    ``MATRICE_OCR_STARTUP_BUDGET_S`` with it, or the worker will time out exactly
    as it did before.
    """
    if os.environ.get("MATRICE_OCR_ENABLE_TRT", "").strip() == "1":
        return ("TensorrtExecutionProvider", "CUDAExecutionProvider", "CPUExecutionProvider")
    return ("CUDAExecutionProvider", "CPUExecutionProvider")


# Min seconds between repeated "OCR degraded to CPU" error logs (periodic, not one-shot).
_CPU_DEGRADE_WARN_INTERVAL_S = 60.0


class LicensePlateMonitorUseCase(BaseProcessor):
    CATEGORY_DISPLAY = {"license_plate": "license_plate"}

    # Class-level defaults for the confirmation gates, mirroring the values
    # __init__ sets. They exist because instances are legitimately built with
    # __new__ (bypassing __init__) to avoid the heavy constructor -- the test
    # suite does exactly that. Before these were declared here, promoting the
    # bare literal 10 to self._max_plate_len turned every such instance into an
    # AttributeError at the first plate-length check. Defining them on the class
    # means a gate is always resolvable; __init__ and _apply_profile_gates
    # override them per instance.
    _min_plate_len = 3
    _max_plate_len = 10
    _stable_frames_required = 1
    _ocr_confidence_threshold = 0.75

    def __init__(self):
        super().__init__("license_plate_monitor")
        self.category = "license_plate_monitor"
        self.target_categories = ["license_plate"]
        self.CASE_TYPE: str | None = "license_plate_monitor"
        self.CASE_VERSION: str | None = "1.3"
        self.smoothing_tracker = None
        self.tracker = None
        self._tracker_seam = ConfigDrivenTracker() if _HAS_ADVANCED_TRACKER else None
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        self._track_merge_iou_threshold: float = 0.05
        self._track_merge_time_window: float = 7.0
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"
        self._seen_plate_texts = set()
        # CHANGE: Added _tracked_plate_texts to store the longest plate_text per track_id
        self._tracked_plate_texts: Dict[Any, str] = {}
        # Containers for text stability & uniqueness
        self._unique_plate_texts: Dict[str, str] = {}  # cleaned_text -> original (longest)
        # NEW: track-wise frequency of cleaned texts to pick the dominant variant per track
        self._track_text_counts: Dict[Any, Counter] = defaultdict(Counter)  # track_id -> Counter(cleaned_text -> count)
        # Helper dictionary to keep history of plate texts per track
        self.helper: Dict[Any, List[str]] = {}
        # Map of track_id -> current dominant plate text
        self.unique_plate_track: Dict[Any, str] = {}
        self.image_preprocessor = ImagePreprocessor()
        # OCR model will be lazily initialized when first used
        self.ocr_model = None
        self._ocr_model_name = "cct-s-v1-global-model"
        self._ocr_device = "auto"
        self._ocr_initialization_attempts = 0
        self._ocr_max_init_attempts = 3
        # OCR runs in an isolated subprocess (numpy<2 + onnxruntime-gpu) so it
        # doesn't conflict with the parent's numpy>=2 + CuPy. The subprocess is
        # the primary path; on permanent failure we fall back to in-process CPU
        # OCR (see _try_load_subprocess_ocr / _run_ocr).
        self._ocr_use_subprocess = True
        self._ocr_subprocess_failed = False
        # Set True when OCR is running on CPU on a GPU-required platform (the
        # _assert_or_warn_gpu_ocr guard); surfaced for monitoring.
        self._ocr_degraded_cpu = False
        # Throttle for the periodic "degraded to CPU" error log (0.0 == never logged).
        self._last_cpu_warn_ts = 0.0
        # OCR text history for stability checks (text  consecutive frame count)
        self._text_history: Dict[str, int] = {}

        self.start_timer = None
        # self.reset_timer = "2025-08-19-04:22:47.187574 UTC"

        # Minimum length for a valid plate (after cleaning)
        self._min_plate_len = 3
        # Maximum length for a valid plate (was a bare literal 10 at each use site)
        self._max_plate_len = 10
        # number of consecutive frames a plate must appear to be considered "stable"
        self._stable_frames_required = 1
        self._non_alnum_regex = re.compile(r"[^A-Za-z0-9]+")
        self._ocr_mode = "alphanumeric"
        self._ocr_confidence_threshold = 0.75
        self._bgr_frame = None
        self._detection_smoother = _DetectionSmoother(hold_frames=3, iou_threshold=0.3)
        # self.jpeg = TurboJPEG()

        # Initialize plate logger (optional, only used if lpr_server_id is provided)
        self.plate_logger: LicensePlateMonitorLogger | None = None
        self._logging_enabled = True  # False  //ToDo: DISABLED FOR NOW, ENABLED FOR PRODUCTION. ##
        self._plate_logger_initialized = False  # Track if plate logger has been initialized

        # Maps camera+plate -> lpr-server detection id for create-vs-update routing
        self._registered_plate_detections: Dict[str, str] = {}

        # Frozen first-sighting frame per camera+plate for CREATE + instant BOLO alerts.
        # Key: registry_key (camera_id:normalized_plate) -> anchor dict with stream_info,
        # image_data, bbox, ocr_confidence, timestamp, frame_id, rtp_number.
        # LRU-bounded: each anchor retains a full-frame base64 JPEG (measured 1.27 MB
        # at 1080p, 5.1 MB at 4K), and this map was never pruned, so a thousand
        # distinct plates retained well over a gigabyte. The only cross-call reader
        # (`_send_instant_alerts`) runs inside the same `process()` call and is gated
        # on `_pending_plate_sighting_commits`, which is cleared every frame, so a cap
        # three orders of magnitude above plates-per-frame cannot evict a live entry.
        self._plate_create_anchors: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
        # Frame decoded by the current process() call's OCR pass; see
        # `_encode_frame_for_plate`. Not state that outlives a frame.
        self._last_resolved_frame: Optional[np.ndarray] = None
        # None = not yet probed, True/False = latched. See `_run_ocr_batch`.
        self._ocr_batch_supported: Optional[bool] = None
        # Per-(camera, plate) track id we last POSTed for — new track = new vehicle pass.
        self._plate_offered_track_ids: Dict[str, Any] = {}
        # Monotonic timestamp of last POST offer (optional plate_log_min_interval_s floor).
        self._plate_last_offered_monotonic: Dict[str, float] = {}
        # Sighting commits deferred until after instant alerts on the same frame.
        self._pending_plate_sighting_commits: Dict[str, Any] = {}

        # Bounded background sender for plate create/append POSTs (holds
        # _registered_plate_detections by reference; built on logger init).
        self._plate_sync: _PlateSyncSender | None = None

        # Initialize instant alert manager (will be lazily initialized on first process() call)
        self.alert_manager: ALERT_INSTANCE | None = None
        self._alert_manager_initialized = False  # Track initialization to do it only once

    def set_alert_manager(self, alert_manager: ALERT_INSTANCE) -> None:
        """
        Set the alert manager instance for instant alerts.

        Args:
            alert_manager: ALERT_INSTANCE instance configured with Redis/Kafka clients
        """
        self.alert_manager = alert_manager
        self.logger.info("Alert manager set for license plate monitoring")

    def _discover_action_id(self) -> str | None:
        """Discover action_id from current working directory name (and parents), similar to face_recognition flow."""
        try:
            import re as _re

            pattern = _re.compile(r"^[0-9a-f]{8,}$", _re.IGNORECASE)
            candidates: List[str] = []
            try:
                cwd = Path.cwd()
                candidates.append(cwd.name)
                for parent in cwd.parents:
                    candidates.append(parent.name)
            except Exception:
                # Non-fatal: cwd is only one of several action_id candidate sources.
                self.logger.debug("[LP_LOGGING] cwd scan for action_id failed", exc_info=True)

            try:
                usr_src = Path("/usr/src")
                if usr_src.exists():
                    for child in usr_src.iterdir():
                        if child.is_dir():
                            candidates.append(child.name)
            except Exception:
                # Non-fatal: /usr/src is absent outside the container image.
                self.logger.debug("[LP_LOGGING] /usr/src scan for action_id failed", exc_info=True)

            for candidate in candidates:
                if candidate and len(candidate) >= 8 and pattern.match(candidate):
                    return candidate
        except Exception:
            # Non-fatal: callers treat an unresolved action_id as "not discoverable".
            self.logger.debug("[LP_LOGGING] action_id discovery failed", exc_info=True)
        return None

    def _get_backend_base_url(self) -> str:
        """Resolve backend base URL based on ENV variable: prod/staging/dev."""
        env = os.getenv("ENV", "prod").strip().lower()
        if env in ("prod", "production"):
            host = "prod.backend.app.matrice.ai"
        elif env in ("dev", "development"):
            host = "dev.backend.app.matrice.ai"
        else:
            host = "staging.backend.app.matrice.ai"
        return f"https://{host}"

    def _mask_value(self, value: str | None) -> str:
        """Mask sensitive values for logging/printing."""
        if not value:
            return ""
        if len(value) <= 4:
            return "*" * len(value)
        return value[:2] + "*" * (len(value) - 4) + value[-2:]

    def _get_public_ip(self) -> str:
        """This host's public IP; see :func:`~..utils.public_ip.resolve_public_ip_once`."""
        return resolve_public_ip_once(self.logger)

    def _fetch_location_name(self, location_id: str, session: Session | None = None) -> str:
        """
        Fetch location name from API using location_id.

        Args:
            location_id: The location ID to look up
            session: Matrice session for API calls

        Returns:
            Location name string, or 'Entry Reception' as default if API fails
        """
        default_location = "Entry Reception"

        # Empty OR placeholder all-zeros ObjectId ("000...0") -> no backend call (hot path).
        if not location_id or not str(location_id).strip("0"):
            self.logger.debug(f"[LOCATION] No/placeholder location_id, using default: '{default_location}'")
            return default_location

        # Check cache first
        if not hasattr(self, "_location_name_cache"):
            self._location_name_cache = LocationNameCache()

        cached_name = self._location_name_cache.resolved(location_id)
        if cached_name is not None:
            self.logger.debug(f"[LOCATION] Using cached location name for '{location_id}': '{cached_name}'")
            return cached_name

        if not session:
            self.logger.warning(f"[LOCATION] No session provided, using default: '{default_location}'")
            return default_location

        # A recent failure suppresses the request for a cool-off, but no longer forever:
        # caching the failure pinned the placeholder onto every plate record for this
        # location for the life of the process, and the API recovering changed nothing
        # (INC-2606).
        if not self._location_name_cache.should_fetch(location_id):
            return default_location

        try:
            endpoint = f"/v1/inference/get_location/{location_id}"
            self.logger.info(f"[LOCATION] Fetching location name from API: {endpoint}")

            response = session.rpc.get(endpoint, timeout=3, raise_exception=False)

            if response and isinstance(response, dict):
                success = response.get("success", False)
                if success:
                    data = response.get("data", {})
                    location_name = data.get("locationName", default_location)
                    self.logger.info(
                        f"[LOCATION] ✓ Fetched location name: '{location_name}' for location_id: '{location_id}'"
                    )

                    # Cache the result
                    self._location_name_cache.store(location_id, location_name)
                    return location_name
                else:
                    self.logger.warning(
                        f"[LOCATION] API returned success=false for location_id '{location_id}': "
                        f"{response.get('message', 'Unknown error')}"
                    )
            else:
                self.logger.warning(f"[LOCATION] Invalid response format from API: {response}")

        except Exception as e:
            self.logger.error(
                f"[LOCATION] Error fetching location name for '{location_id}': {e}",
                exc_info=True,
            )

        # Use default on any failure
        self.logger.info(f"[LOCATION] Using default location name: '{default_location}'")
        self._location_name_cache.note_failure(location_id)
        return default_location

    def _cached_lpr_server_info(self) -> Dict[str, Any] | None:
        """The lpr-server record the plate logger already fetched, or None.

        Returns None rather than an empty dict so "the logger has no copy" stays
        distinguishable from "the server returned nothing".
        """
        info = getattr(getattr(self, "plate_logger", None), "server_info", None)
        return info if isinstance(info, dict) and info else None

    def _resolve_lpr_server_record(self, rpc: Any, lpr_server_id: str) -> Dict[str, Any] | None:
        """The lpr-server record, fetching it only if nobody has it yet.

        ANA-16: ``get_server_connection_info`` and the alert-manager initialiser
        both issued a blocking GET ``/v1/actions/lpr_servers/{id}`` on frame 1.
        Same id, same payload -- and the alert path reads exactly one field
        (``host``) out of it -- so the second round trip was pure frame latency.
        The plate logger is initialised earlier in the same ``process()`` call,
        under the same ``if config.lpr_server_id`` condition, so on the normal
        path its copy is already there and this costs nothing.

        The fetch is kept rather than deleted because it is the only path to
        ``host`` when the logger has no copy: its own init failed, or the response
        was not a 200 and it kept None.
        """
        cached = self._cached_lpr_server_info()
        if cached is not None:
            return cached
        response = rpc.get(f"/v1/actions/lpr_servers/{lpr_server_id}")
        if response.get("success", False) and response.get("data"):
            return response.get("data", {})
        return None

    def _initialize_alert_manager_once(self, config: LicensePlateMonitorConfig) -> None:
        """
        Initialize alert manager ONCE with Redis OR Kafka clients (Environment based).
        Called from process() on first invocation.
        Uses config.session (existing session from pipeline).
        """
        if self._alert_manager_initialized:
            return

        try:
            # Import required modules
            from matrice_common.stream.matrice_stream import MatriceStream, StreamType

            # Use existing session from config (same pattern as plate_logger)
            if not config.session:
                account_number = os.getenv("MATRICE_ACCOUNT_NUMBER", "")
                access_key_id = os.getenv("MATRICE_ACCESS_KEY_ID", "")
                secret_key = os.getenv("MATRICE_SECRET_ACCESS_KEY", "")
                project_id = os.getenv("MATRICE_PROJECT_ID", "")

                self.session = Session(
                    account_number=account_number,
                    access_key=access_key_id,
                    secret_key=secret_key,
                    project_id=project_id,
                )
                config.session = self.session
                if not self.session:
                    self.logger.warning("[ALERT] No session in config OR manual, skipping alert manager initialization")
                    self._alert_manager_initialized = True
                    return

            rpc = config.session.rpc

            # Determine environment: Localhost vs Cloud
            # We use LPR server info to determine if we are local or cloud, similar to face_recognition_client
            is_localhost = False
            lpr_server_id = config.lpr_server_id
            _cfg_repr = repr(config)
            self.logger.info(
                "[ALERT] CONFIG-PRINT | config_type=%s repr_len=%d",
                type(config).__name__,
                len(_cfg_repr),
            )
            self.logger.debug("[ALERT] CONFIG-PRINT repr=%s", _cfg_repr)
            if lpr_server_id:
                try:
                    # One fetch per frame, shared with the plate logger -- ANA-16.
                    server_data = self._resolve_lpr_server_record(rpc, lpr_server_id)
                    if server_data:
                        server_host = server_data.get("host", "")
                        public_ip = self._get_public_ip()

                        # Check if server_host indicates localhost
                        localhost_indicators = ["localhost", "127.0.0.1", "0.0.0.0"]  # nosec B104
                        if server_host in localhost_indicators or server_host == public_ip:
                            is_localhost = True
                            self.logger.info(
                                f"[ALERT] Detected Localhost environment (Public IP={public_ip}, Server IP={server_host})"
                            )
                        else:
                            is_localhost = False
                            self.logger.info(
                                f"[ALERT] Detected Cloud environment (Public IP={public_ip}, Server IP={server_host})"
                            )
                    else:
                        self.logger.warning(
                            "[ALERT] Failed to fetch LPR server info for environment detection, defaulting to Cloud mode"
                        )
                except Exception as e:
                    self.logger.warning(f"[ALERT] Error detecting environment: {e}, defaulting to Cloud mode")
            else:
                self.logger.info("[ALERT] No LPR server ID, defaulting to Cloud mode")

            # ------------------------------------------------------------------
            # Discover action_id and fetch action details (STRICT API-DRIVEN)
            # ------------------------------------------------------------------
            action_id = self._discover_action_id()
            if not action_id:
                self.logger.error("[ALERT] Could not discover action_id from working directory or parents")
                _log_with_msg_meta(
                    self.logger,
                    logging.WARNING,
                    "[ALERT] ALERT ACTION DISCOVERY | action_id=NOT FOUND | note=discover_returned_falsy",
                )
                self._alert_manager_initialized = True
                return

            try:
                action_url = f"/v1/actions/action/{action_id}/details"
                action_resp = rpc.get(action_url)
                if not (action_resp and action_resp.get("success", False)):
                    raise RuntimeError(
                        action_resp.get("message", "Unknown error")
                        if isinstance(action_resp, dict)
                        else "Unknown error"
                    )
                action_doc = action_resp.get("data", {}) if isinstance(action_resp, dict) else {}
                action_details = action_doc.get("actionDetails", {}) if isinstance(action_doc, dict) else {}

                # server id and type extraction (robust to variants)
                server_id = (
                    action_details.get("serverId")
                    or action_details.get("server_id")
                    or action_details.get("serverID")
                    or action_details.get("redis_server_id")
                    or action_details.get("kafka_server_id")
                )
                server_type = (
                    action_details.get("serverType") or action_details.get("server_type") or action_details.get("type")
                )

                # Persist identifiers for future
                self._action_id = action_id
                self._deployment_id = action_details.get("_idDeployment") or action_details.get("deployment_id")
                self._app_deployment_id = action_details.get("app_deployment_id")
                self._instance_id = action_details.get("instanceID") or action_details.get("instanceId")
                self._external_ip = action_details.get("externalIP") or action_details.get("externalIp")

                _ad_msg = (
                    f"[ALERT] Action details: action_id={action_id} server_type={server_type} server_id={server_id}"
                )
                self.logger.info(_ad_msg)
                self.logger.debug(f"[ALERT] Full action_details: {action_details}")
            except Exception as e:
                self.logger.error(
                    f"[ALERT] Failed to fetch action details for action_id={action_id}: {e}",
                    exc_info=True,
                )
                _ade_msg = (
                    f"[ALERT] ALERT ACTION DETAILS ERROR | action_id={action_id!r} id_type={type(action_id).__name__} "
                    f"error={e!r} err_type={type(e).__name__}"
                )
                _log_with_msg_meta(self.logger, logging.ERROR, _ade_msg)
                self._alert_manager_initialized = True
                return

            # Historical deployment behavior: always initialize via Redis (instance API), not Kafka.
            is_localhost = True

            redis_client = None
            kafka_client = None

            # STRICT SWITCH: Only Redis if localhost, Only Kafka if cloud
            if is_localhost:
                # Initialize Redis client (ONLY) using STRICT API by instanceID
                instance_id = getattr(self, "_instance_id", None)
                if not instance_id:
                    self.logger.error(
                        "[ALERT] Localhost mode but instance_id missing in action details for Redis initialization"
                    )
                else:
                    try:
                        url = f"/v1/actions/get_redis_server_by_instance_id/{instance_id}"
                        self.logger.info(
                            f"[ALERT] Initializing Redis client via API for Localhost mode (instance_id={instance_id})"
                        )
                        response = rpc.get(url)
                        if isinstance(response, dict) and response.get("success", False):
                            data = response.get("data", {})
                            host = data.get("host")
                            port = data.get("port")
                            username = data.get("username")
                            password = data.get("password", "")
                            db_index = data.get("db", 0)
                            conn_timeout = data.get("connection_timeout", 120)

                            # Sentinel HA support
                            sentinel_hosts = None
                            master_name = None
                            sentinel_cfg = data.get("sentinelConfig") or {}
                            if sentinel_cfg.get("sentinelHosts"):
                                sentinel_hosts = [(h, 26379) for h in sentinel_cfg["sentinelHosts"]]
                                master_name = sentinel_cfg.get("masterName")

                            sentinel_str = (
                                f"yes, master={master_name}, nodes={len(sentinel_hosts)}" if sentinel_hosts else "no"
                            )

                            self.logger.debug(  # nosemgrep: python.lang.security.audit.logging.logger-credential-leak.python-logger-credential-disclosure
                                "[ALERT] Redis server params (credentials redacted) | instance_id=%s host=%s port=%s db=%s timeout=%s sentinel=%s has_user=%s",
                                instance_id,
                                host,
                                port,
                                db_index,
                                conn_timeout,
                                sentinel_str,
                                bool(username),
                            )

                            self.logger.info(
                                "[ALERT] Redis server params | instance_id=%s, host=%s, port=%s, db=%s, sentinel=%s",
                                instance_id,
                                host,
                                port,
                                db_index,
                                sentinel_str,
                            )

                            # Initialize with Sentinel support
                            stream_kwargs = dict(
                                host=host,
                                port=int(port),
                                password=password,
                                username=username,
                                db=db_index,
                                connection_timeout=conn_timeout,
                            )
                            if sentinel_hosts and master_name:
                                stream_kwargs["sentinel_hosts"] = sentinel_hosts
                                stream_kwargs["master_name"] = master_name
                            redis_client = MatriceStream(StreamType.REDIS, **stream_kwargs)
                            redis_client.setup("alert_instant_config_request")
                            self.logger.info("[ALERT] Redis client initialized successfully")
                        else:
                            self.logger.warning(
                                f"[ALERT] Failed to fetch Redis server info: {response.get('message', 'Unknown error') if isinstance(response, dict) else 'Unknown error'}"
                            )
                    except Exception as e:
                        self.logger.warning(f"[ALERT] Redis initialization failed: {e}")

            # Create alert manager if client is available
            if redis_client or kafka_client:
                # Get app_deployment_id from action_details for filtering alerts
                app_deployment_id_for_alert = getattr(self, "_app_deployment_id", None)
                self.logger.info(f"[ALERT] Using app_deployment_id for alert filtering: {app_deployment_id_for_alert}")

                self.alert_manager = ALERT_INSTANCE(
                    redis_client=redis_client,
                    kafka_client=kafka_client,
                    config_topic="alert_instant_config_request",
                    trigger_topic="alert_instant_triggered",
                    polling_interval=10,  # Poll every 10 seconds
                    logger=self.logger,
                    app_deployment_id=app_deployment_id_for_alert,
                )
                self.alert_manager.start()
                transport = "Redis" if redis_client else "Kafka"
                self.logger.info(f"[ALERT] Alert manager initialized and started with {transport} (polling every 10s)")
            else:
                self.logger.warning(
                    f"[ALERT] No {'Redis' if is_localhost else 'Kafka'} client available for {'Localhost' if is_localhost else 'Cloud'} mode, alerts disabled"
                )

        except Exception as e:
            self.logger.error(f"[ALERT] Alert manager initialization failed: {e}", exc_info=True)
        finally:
            self._alert_manager_initialized = True  # Mark as initialized (don't retry every frame)

    def reset_tracker(self) -> None:
        """Reset the advanced tracker instance."""
        if self.tracker is not None:
            self.tracker.reset()
            self.logger.info("AdvancedTracker reset for new tracking session")

    def reset_plate_tracking(self) -> None:
        """Reset plate tracking state."""
        self._seen_plate_texts = set()
        # CHANGE: Reset _tracked_plate_texts
        self._tracked_plate_texts = {}
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._text_history = {}
        self._unique_plate_texts = {}
        self.helper = {}
        self.unique_plate_track = {}
        # Reset registered plate detections to allow fresh create/update routing.
        # NOTE: .clear() (not rebind) — _PlateSyncSender holds this dict by reference.
        self._registered_plate_detections.clear()
        self._plate_create_anchors.clear()
        self._plate_offered_track_ids.clear()
        self._plate_last_offered_monotonic.clear()
        self._pending_plate_sighting_commits.clear()
        # These two were the only tracking maps this reset missed, which is why they
        # grew for the life of the process regardless of how often it was called.
        self._track_aliases.clear()
        self._canonical_tracks.clear()
        if self._plate_sync:
            self._plate_sync.reset_state()
        self.logger.info("Plate tracking state reset")

    def reset_all_tracking(self) -> None:
        """Reset both advanced tracker and plate tracking state."""
        self.reset_tracker()
        self.reset_plate_tracking()
        self.logger.info("All plate tracking state reset")

    def _scale_alert_coordinates(
        self,
        coordinates: Dict[str, Any],
        stream_info: Dict[str, Any] | None,
        config: Any,
    ) -> Dict[str, Any]:
        """Express alert coordinates in the reference space the consumer implements.

        Publishes the box as a fraction of the frame, so a consumer renders it as
        ``coord * displayed_dimension`` and no resolution constant is involved.
        The previous wire carried source pixels, which fe-analytics divided by a
        hard-coded 640 -- correct only for a 640x640 frame, and the cause of the
        ~2x offset and size error measured on live alerts.

        IMPORTANT -- this only affects alerts published by THIS process. Where an
        ``lpr_server_id`` is configured, the alert is published by lpr-server
        instead: it consumes the ``lpr-detections`` stream, derives
        ``coordinates`` from the ``bbox`` field of that message, and XADDs
        ``alert_instant_triggered`` itself (verified on Thor -- its "published
        alert to Redis stream" log matches each stream entry to the millisecond,
        while this path's rescaled values never appear on the wire). That channel
        carries raw source pixels by design, because the same ``bbox`` is what the
        detection document stores, and it cannot be rescaled here without changing
        what a stored detection means. For those deployments the divisor has to be
        fixed in fe-analytics (use the image's natural width/height, which the
        component already captures) or in lpr-server.

        Fails open: with no frame dimensions, or ``alert_bbox_coordinate_space =
        "pixel"``, the coordinates are returned untouched. Getting this wrong
        should misplace a box, never drop an alert.

        Values are kept as floats, not rounded. A normalized box rounded to an int
        collapses to 0 or 1 -- which is exactly how the deployed lpr-server would
        destroy a normalized ``bbox`` (it rounds to integer coordinates; verified
        against the wire), and the reason the ``lpr-detections`` payload must stay
        in pixels until that server is changed.
        """
        space = str(getattr(config, "alert_bbox_coordinate_space", "normalized") or "normalized").lower()
        if space != "normalized" or not coordinates:
            return coordinates

        from ..utils.geometry_utils import resolve_frame_dims

        width, height = resolve_frame_dims(stream_info)
        if width <= 0 or height <= 0:
            # _backfill_stream_resolution normally fills this from the payload's
            # coordinate_frame. If it could not, publishing pixels is still the
            # better failure: wrong scale beats no alert.
            self._warn_once_no_frame_dims()
            return coordinates

        try:
            return {
                "x": round(float(coordinates.get("x", 0)) / width, 6),
                "y": round(float(coordinates.get("y", 0)) / height, 6),
                "width": round(float(coordinates.get("width", 0)) / width, 6),
                "height": round(float(coordinates.get("height", 0)) / height, 6),
            }
        except (TypeError, ValueError):
            return coordinates

    def _warn_once_no_frame_dims(self) -> None:
        now = time.time()
        if now - getattr(self, "_last_no_dims_warn_ts", 0.0) < 60.0:
            return
        self._last_no_dims_warn_ts = now
        self.logger.warning(
            "[ALERT] No frame dimensions in stream_info; publishing alert coordinates as raw "
            "source pixels. The alert overlay will be misplaced until stream_resolution or the "
            "payload's coordinate_frame is available."
        )

    def _send_instant_alerts(
        self,
        detections: List[Dict[str, Any]],
        stream_info: Dict[str, Any] | None,
        config: LicensePlateMonitorConfig,
    ) -> None:
        """
        Send detection events to the instant alert system.

        Only fires for confirmed/stable plates (same gate as lpr-server logging).
        Uses the frozen first-sighting frame anchor so BOLO thumbnails match the
        vehicle when the plate was first confirmed, not a later frame.
        """
        if not self.alert_manager:
            return

        if not detections:
            return

        plates_to_alert = self._collect_confirmed_plates(detections)
        if not plates_to_alert:
            return

        self.logger.debug("[ALERT] Processing %d confirmed plate(s) for alerts", len(plates_to_alert))

        # Extract metadata directly from stream_info with empty string defaults
        # No complex nested checks - if not found, pass empty string (no errors)
        camera_id = ""
        app_deployment_id = ""
        application_id = ""
        camera_name = ""
        frame_id = ""
        rtp_number = ""
        location_name = ""

        if stream_info:
            # Direct extraction with safe defaults
            camera_id = stream_info.get("camera_id", "")
            if not camera_id and "camera_info" in stream_info:
                camera_id = stream_info.get("camera_info", {}).get("camera_id", "")

            camera_name = stream_info.get("camera_name", "")
            if not camera_name and "camera_info" in stream_info:
                camera_name = stream_info.get("camera_info", {}).get("camera_name", "")

            app_deployment_id = stream_info.get("app_deployment_id", "")
            application_id = stream_info.get("application_id", stream_info.get("app_id", ""))

            # Extract frame_id and rtp_number - at root level of stream_info
            input_settings = (
                stream_info.get("input_settings", {}) if isinstance(stream_info.get("input_settings", {}), dict) else {}
            )
            frame_id = (
                stream_info.get("frame_id", "")
                or stream_info.get("frameId", "")
                or input_settings.get("frame_id", "")
                or input_settings.get("frameId", "")
                or ""
            )
            rtp_number = (
                stream_info.get("rtp_number", "")
                or stream_info.get("rtpNumber", "")
                or input_settings.get("rtp_number", "")
                or input_settings.get("rtpNumber", "")
                or ""
            )

            # Extract location_id and fetch location_name from API
            location_id = ""
            if "camera_info" in stream_info:
                location_id = stream_info.get("camera_info", {}).get("location", "")

            if location_id:
                # Fetch location name from API
                location_name = self._fetch_location_name(location_id, config.session)
            else:
                location_name = "Entry Reception"  # Default if no location_id
        else:
            location_name = "Entry Reception"  # Default

        # Process each confirmed plate
        sent_count = 0
        for plate_text, plate_meta in plates_to_alert.items():
            registry_key = self._plate_registry_key(camera_id, plate_text) if camera_id else ""
            if registry_key and registry_key not in self._pending_plate_sighting_commits:
                continue
            anchor = self._plate_create_anchors.get(registry_key) if registry_key else None

            anchor_stream = anchor["stream_info"] if anchor else (stream_info or {})
            frame_id = (anchor or {}).get("frame_id", "")
            rtp_number = (anchor or {}).get("rtp_number", "")
            if not frame_id or not rtp_number:
                frame_id, rtp_number = _extract_stream_frame_fields(anchor_stream)

            confidence = plate_meta.get("ocr_confidence")
            if confidence is None:
                confidence = plate_meta.get("confidence", 0.0)
            confidence = float(confidence or 0.0)
            # Bbox must come from the SAME frame as frame_id/rtp_number above, or the
            # alert draws a current-frame box over the anchor's (older) rtp_number image
            # -- the box then sits on wherever the vehicle was ~stable_frames+hold_frames
            # ago, not where the image actually shows it. _build_plate_create_anchor()
            # already freezes bbox alongside frame_id/rtp_number for exactly this reason
            # (:2481); prefer it here and only fall back to the live bbox when there is
            # no anchor at all (no camera_id -> no registry_key -> no anchor lookup).
            bbox = (anchor or {}).get("bbox") or plate_meta.get("bbox", [])

            # Build coordinates dict
            coordinates = {}
            if isinstance(bbox, dict):
                # Handle dict format bbox
                if "xmin" in bbox:
                    coordinates = {
                        "x": int(bbox.get("xmin", 0)),
                        "y": int(bbox.get("ymin", 0)),
                        "width": int(bbox.get("xmax", 0) - bbox.get("xmin", 0)),
                        "height": int(bbox.get("ymax", 0) - bbox.get("ymin", 0)),
                    }
                elif "x" in bbox:
                    coordinates = {
                        "x": int(bbox.get("x", 0)),
                        "y": int(bbox.get("y", 0)),
                        "width": int(bbox.get("width", 0)),
                        "height": int(bbox.get("height", 0)),
                    }
            elif isinstance(bbox, list) and len(bbox) >= 4:
                x1, y1, x2, y2 = bbox[:4]
                coordinates = {
                    "x": int(x1),
                    "y": int(y1),
                    "width": int(x2 - x1),
                    "height": int(y2 - y1),
                }

            coordinates = self._scale_alert_coordinates(coordinates, stream_info, config)

            # Build detection event for alert system
            detection_event = {
                "camera_id": camera_id,
                "app_deployment_id": app_deployment_id,
                "application_id": application_id,
                "detectionType": "license_plate",
                "plateNumber": plate_text,
                "confidence": float(confidence),
                "frameUrl": "",  # Will be filled by analytics publisher if needed
                "coordinates": coordinates,
                "cameraName": camera_name,
                "locationName": location_name,
                "frame_id": frame_id,
                "rtp_number": rtp_number,
                "vehicleType": "",
                "vehicleColor": "",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

            # Send to alert manager for evaluation
            try:
                self.alert_manager.process_detection_event(detection_event, anchor_stream or stream_info)
                sent_count += 1
            except Exception as e:
                self.logger.error(
                    "[ALERT] Failed to send detection event: plate=%s error=%s",
                    plate_text,
                    e,
                    exc_info=True,
                )

        if sent_count:
            self.logger.info("[ALERT] Sent %d instant alert event(s)", sent_count)

    def _initialize_plate_logger(self, config: LicensePlateMonitorConfig) -> bool:
        """Initialize the plate logger if lpr_server_id is provided. Returns True if successful."""
        if not config.lpr_server_id:
            self._logging_enabled = False
            self._plate_logger_initialized = False
            self.logger.warning("[LP_LOGGING] Plate logging disabled: no lpr_server_id provided")
            return False

        try:
            if self.plate_logger is None:
                self.plate_logger = LicensePlateMonitorLogger()

            self.plate_logger.initialize_session(config)
            self._logging_enabled = True
            self._plate_logger_initialized = True
            # The getattr default covers a duck-typed config with no such field; the
            # `or` covers a config that has it set to 0/None. Both used to read 30.0
            # independently of the dataclass default, so the documented 5 s was only
            # ever in force for a real LicensePlateMonitorConfig.
            #
            # Ordering note (do not restructure): _get_http_session bakes this value
            # into the ClientSession's ClientTimeout at creation, so re-assigning
            # _post_timeout_s after that session exists is silently ignored. It is
            # correct today only because the assignment happens here on frame 1 and
            # the session is created lazily on the sender thread afterwards.
            try:
                self.plate_logger._post_timeout_s = float(
                    getattr(config, "lpr_post_timeout_s", _LPR_POST_TIMEOUT_DEFAULT_S) or _LPR_POST_TIMEOUT_DEFAULT_S
                )
            except (TypeError, ValueError):
                self.plate_logger._post_timeout_s = _LPR_POST_TIMEOUT_DEFAULT_S
            mode = str(getattr(config, "lpr_publish_mode", "redis") or "redis").lower()
            if mode not in ("redis", "http"):
                self.logger.warning("[LP_LOGGING] Unknown lpr_publish_mode=%r; using 'redis'", mode)
                mode = "redis"
            self.plate_logger._publish_mode = mode
            self.plate_logger._lpr_bbox_space = str(
                getattr(config, "lpr_bbox_coordinate_space", "pixel") or "pixel"
            ).lower()
            if mode == "redis" and self.plate_logger._plate_publisher is None:
                self.plate_logger._plate_publisher = _LprRedisPublisher(
                    stream=str(getattr(config, "lpr_detections_stream", "lpr-detections") or "lpr-detections"),
                    maxlen=int(getattr(config, "lpr_stream_maxlen", 100_000) or 100_000),
                )
            if self._plate_sync is None:
                max_in_flight = int(getattr(config, "lpr_max_in_flight", 2) or 2)
                max_pending_slots = int(getattr(config, "lpr_max_pending_slots", 32) or 32)
                if mode == "redis":
                    # Both caps exist to bound a queue that only forms when a send
                    # blocks on a remote handler. An XADD does not: it returns in
                    # well under a millisecond. Keeping max_in_flight=2 would hold
                    # the old ~2-sends-per-15s ceiling for no reason, and the
                    # 32-slot cap evicts the OLDEST pending sighting when it fills
                    # -- silent data loss (25 evicted within 22s of one startup) in
                    # service of a backlog that no longer happens.
                    #
                    # Volume is still bounded, deliberately, by
                    # plate_log_min_interval_s and max_frame_age_s. These two were
                    # never the volume control; they were the damage control.
                    max_in_flight = max(max_in_flight, 32)
                    max_pending_slots = max(max_pending_slots, 4096)
                self._plate_sync = _PlateSyncSender(
                    self.plate_logger,
                    self._registered_plate_detections,
                    max_in_flight=max_in_flight,
                    append_min_interval_s=float(getattr(config, "lpr_append_min_interval_s", 5.0) or 5.0),
                    max_frame_age_s=float(getattr(config, "lpr_max_frame_age_s", 5.0) or 5.0),
                    max_pending_slots=max_pending_slots,
                )
                self.logger.warning(
                    "[LP_LOGGING] Plate sync starting: mode=%s max_in_flight=%d max_pending_slots=%d",
                    mode,
                    max_in_flight,
                    max_pending_slots,
                )
                self._plate_sync.start()
                self.logger.info("[LP_LOGGING] Plate sync sender started")
            self.logger.info("[LP_LOGGING] Plate logging enabled (server_id=%s)", config.lpr_server_id)
            return True
        except Exception as e:
            self.logger.error(
                f"[LP_LOGGING] ERROR - Failed to initialize plate logger: {e}",
                exc_info=True,
            )
            self._logging_enabled = False
            self._plate_logger_initialized = False
            self.logger.error("[LP_LOGGING] Plate logging has been DISABLED due to initialization failure")
            return False

    def _plate_registry_key(self, camera_id: str, plate_text: str) -> str:
        """Stable registry key for a plate on a specific camera."""
        return f"{camera_id}:{self._normalize_plate(plate_text)}"

    def _build_plate_create_anchor(
        self,
        stream_info: Dict[str, Any],
        image_data: str,
        plate_meta: Dict[str, Any],
        timestamp: str,
    ) -> Dict[str, Any]:
        """Capture immutable first-sighting frame metadata for CREATE and BOLO alerts.

        ``plate_meta``'s own ``frame_id``/``rtp_number`` (set by ``_collect_confirmed_plates``
        from the winning detection) take priority over ``stream_info`` -- the current call's
        frame. When the winning detection is a ``_smoothed`` carry-forward, its bbox is from an
        earlier frame, and ``plate_meta`` carries THAT frame's identity (via
        ``_DetectionSmoother.smooth()``'s carry-forward stamping); using ``stream_info`` instead
        would pair a stale bbox with the current frame's identity -- the "alert bbox matches the
        previous ~2 RTP" defect. Falls back to ``stream_info`` only when the detection carries no
        identity of its own (e.g. a non-LPR caller that never populated it).
        """
        meta_frame_id = plate_meta.get("frame_id")
        meta_rtp_number = plate_meta.get("rtp_number")
        if meta_frame_id or meta_rtp_number:
            frame_id, rtp_number = meta_frame_id or "", meta_rtp_number or ""
        else:
            frame_id, rtp_number = _extract_stream_frame_fields(stream_info)
        return {
            # Pass the same corrected identity into the stream_info snapshot --
            # the lpr-server CREATE/append payload reads THIS, not the top-level
            # frame_id/rtp_number keys below, so both channels must agree.
            "stream_info": _snapshot_stream_info_for_plate(
                stream_info, frame_id_override=frame_id, rtp_number_override=rtp_number
            ),
            "image_data": image_data,
            "bbox": plate_meta.get("bbox"),
            "ocr_confidence": plate_meta.get("ocr_confidence"),
            "track_id": plate_meta.get("track_id"),
            "timestamp": timestamp,
            "frame_id": frame_id,
            "rtp_number": rtp_number,
        }

    def _should_offer_plate_sighting(
        self,
        registry_key: str,
        track_id: Any,
        config: LicensePlateMonitorConfig,
    ) -> bool:
        """True when this (camera, plate) sighting should be POSTed to lpr-server.

        Dedup is per vehicle pass (track_id), not permanent log-once. Watchlist
        cooldown is enforced downstream by lpr-server and inference-tracker.
        """
        if track_id is None:
            return True
        if self._plate_offered_track_ids.get(registry_key) == track_id:
            return False
        min_interval = float(getattr(config, "plate_log_min_interval_s", 0.0) or 0.0)
        if min_interval > 0:
            last_offered = self._plate_last_offered_monotonic.get(registry_key, 0.0)
            if (time.monotonic() - last_offered) < min_interval:
                return False
        return True

    def _mark_plate_sighting_offered(self, registry_key: str, track_id: Any) -> None:
        """Record that this track's first-sighting frame was offered for POST."""
        if track_id is not None:
            self._plate_offered_track_ids[registry_key] = track_id
        self._plate_last_offered_monotonic[registry_key] = time.monotonic()

    def _commit_pending_plate_sightings(self) -> None:
        """Apply deferred per-track dedup after lpr-server offer + instant alerts."""
        for registry_key, track_id in self._pending_plate_sighting_commits.items():
            self._mark_plate_sighting_offered(registry_key, track_id)
        self._pending_plate_sighting_commits.clear()

    def _stamp_detections_frame_ids(
        self,
        detections: List[Dict[str, Any]],
        stream_info: Dict[str, Any] | None,
    ) -> None:
        """Bind each detection to the frame's rtp/frame_id at OCR-read time (in-place).

        Skips ``_smoothed`` (carried-forward) detections: their bbox is from an
        earlier frame -- up to ``_DetectionSmoother``'s ``hold_frames`` back -- and
        ``_DetectionSmoother.smooth()`` already stamped them with the frame that
        bbox was actually true for. Overwriting that here with THIS frame's identity
        would make a stale bbox claim to be current -- the "alert bbox matches the
        previous ~2 RTP frames" defect.
        """
        frame_id, rtp_number = _extract_stream_frame_fields(stream_info)
        if not frame_id and not rtp_number:
            return
        for det in detections:
            if det.get("_smoothed"):
                continue
            if det.get("plate_text"):
                if frame_id:
                    det["frame_id"] = frame_id
                if rtp_number:
                    det["rtp_number"] = rtp_number

    def _offer_detected_plates(
        self,
        detections: List[Dict[str, Any]],
        config: LicensePlateMonitorConfig,
        stream_info: Dict[str, Any] | None,
        image_bytes: bytes | None = None,
    ) -> None:
        """
        Offer confirmed/dominant plates to the background plate-sync sender.

        - New plate (per camera): the sender POSTs a create detection
        - Known plate: the sender POSTs an append view frame on the existing record

        Runs SYNCHRONOUSLY on the producer thread: everything thread-affine
        (frame image resolution via ``_resolve_ocr_image`` / the thread-local
        BGR holder, registry keys, timestamps) is precomputed here; the actual
        HTTP POSTs happen on the sender's own loop, bounded and coalesced.

        IMPORTANT: This method expects detections from counting_summary["detections"] which
        already contain the CORRECT dominant plate_text (computed from last 50% of tracking history
        in _count_categories). This ensures we log validated/confirmed plates only, not raw OCR output.
        """
        # Enhanced logging for diagnostics
        self.logger.debug(
            f"[LP_LOGGING] Starting plate logging check - detections count: {len(detections)} "
            f"| logging_enabled={self._logging_enabled} plate_logger={self.plate_logger is not None} "
            f"registered={len(self._registered_plate_detections)}"
        )

        if not self._logging_enabled:
            self.logger.warning("[LP_LOGGING] Plate logging disabled")
            return

        if not self.plate_logger:
            self.logger.warning("[LP_LOGGING] Plate logger not initialized")
            return

        if not self._plate_sync:
            self.logger.warning("[LP_LOGGING] Plate sync sender not initialized")
            return

        if stream_info is None:
            stream_info = {}

        camera_info = self.plate_logger._extract_camera_info_from_stream(stream_info)
        camera_id = camera_info.get("camera_id", "")

        # Get current timestamp
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=True)

        # The frame encode used to happen HERE, unconditionally, before we knew whether
        # any plate would survive `_should_offer_plate_sighting` -- i.e. on every frame a
        # vehicle was visible, while the offer floor is 60 s (surveillance) or 300 s
        # (access control) plus per-track dedup, so measurements put >99.8% of the work
        # in the bin (13.3 ms / 1.27 MB at 1080p, 51.4 ms / 5.1 MB at 4K). It is now
        # deferred to the first plate that actually needs it, and memoised so several
        # surviving plates in one frame still share a single encode.
        _encoded: List[str] = []

        def _frame_image_data() -> str:
            if not _encoded:
                _encoded.append(self._encode_frame_for_plate(image_bytes))
            return _encoded[0]

        # Collect CONFIRMED/DOMINANT plates from detections.
        plates_to_log = self._collect_confirmed_plates(detections)

        if plates_to_log:
            raw_input_settings = stream_info.get("input_settings", {})
            input_settings = raw_input_settings if isinstance(raw_input_settings, dict) else {}
            frame_age_ref = str(input_settings.get("stream_time", "") or stream_info.get("stream_time", "") or "")
            enq_monotonic = time.monotonic()
            items: List[Tuple[str, dict]] = []
            for plate_text, plate_meta in plates_to_log.items():
                registry_key = self._plate_registry_key(camera_id, plate_text)
                track_id = plate_meta.get("track_id")

                # One POST per vehicle pass (track). Do not permanently skip once
                # registered — lpr-server + inference-tracker apply watchlist cooldown.
                if not self._should_offer_plate_sighting(registry_key, track_id, config):
                    continue

                # Fresh anchor for this sighting episode (first stable frame on track).
                self._plate_create_anchors[registry_key] = self._build_plate_create_anchor(
                    stream_info,
                    _frame_image_data(),
                    plate_meta,
                    current_timestamp,
                )
                self._plate_create_anchors.move_to_end(registry_key)
                while len(self._plate_create_anchors) > _PLATE_ANCHOR_MAX:
                    self._plate_create_anchors.popitem(last=False)
                self._pending_plate_sighting_commits[registry_key] = track_id
                anchor = self._plate_create_anchors[registry_key]

                call_kwargs = {
                    "plate_text": plate_text,
                    "timestamp": anchor["timestamp"],
                    "stream_info": anchor["stream_info"],
                    "image_data": anchor["image_data"],
                    "bbox": anchor.get("bbox"),
                    "ocr_confidence": anchor.get("ocr_confidence"),
                }
                items.append(
                    (
                        registry_key,
                        {
                            "create_kwargs": dict(call_kwargs),
                            "append_kwargs": dict(call_kwargs),
                            "frame_age_ref": frame_age_ref,
                            "enq_monotonic": enq_monotonic,
                        },
                    )
                )
            if items:
                self._plate_sync.offer_batch(items)
                self.logger.debug(
                    "[LP_LOGGING] Offered %d plate CREATE(s) to sync sender (registered=%d anchors=%d)",
                    len(items),
                    len(self._registered_plate_detections),
                    len(self._plate_create_anchors),
                )
        else:
            self.logger.debug("[LP_LOGGING] No confirmed plates to sync this frame")

    def _collect_confirmed_plates(self, detections: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Collect CONFIRMED/DOMINANT plates from detections.

        Returns ``plate_text -> logging metadata (track_id, bbox, ocr_confidence)``.
        """
        plates_to_log = {}  # plate_text -> logging metadata (track_id, bbox, ocr_confidence)

        for det in detections:
            track_id = det.get("track_id")
            if track_id is None:
                continue

            dominant_plate = self._clean_text(str(det.get("plate_text") or ""))
            if not dominant_plate:
                continue

            history = self.helper.get(track_id, [])
            if len(history) < self._stable_frames_required:
                self.logger.debug(
                    f"[LP_LOGGING] Skipping track_id={track_id} - insufficient history "
                    f"({len(history)}/{self._stable_frames_required})"
                )
                continue

            recent = history[-self._stable_frames_required :]
            if len(set(recent)) != 1:
                self.logger.debug(f"[LP_LOGGING] Skipping track_id={track_id} - plate not stable yet (recent={recent})")
                continue

            stable_plate = recent[0]
            if not self._plates_match(stable_plate, dominant_plate):
                self.logger.debug(
                    f"[LP_LOGGING] Skipping track_id={track_id} - dominant '{dominant_plate}' != stable '{stable_plate}'"
                )
                continue

            if not (self._min_plate_len <= len(stable_plate) <= self._max_plate_len):
                self.logger.debug(
                    f"[LP_LOGGING] Skipping plate '{stable_plate}' - invalid length ({len(stable_plate)})"
                )
                continue

            if stable_plate not in plates_to_log and not any(
                self._plates_match(stable_plate, existing) for existing in plates_to_log
            ):
                plates_to_log[stable_plate] = {
                    "track_id": track_id,
                    "bbox": det.get("bounding_box") or det.get("bbox"),
                    "ocr_confidence": det.get("ocr_confidence"),
                    # The frame this bbox is actually true for -- set by
                    # _stamp_detections_frame_ids for a live detection, or carried
                    # from the last real sighting by _DetectionSmoother for a
                    # `_smoothed` one. _build_plate_create_anchor prefers these over
                    # the current call's stream_info so an anchor built from a
                    # held/stale bbox doesn't claim to be from "now".
                    "frame_id": det.get("frame_id"),
                    "rtp_number": det.get("rtp_number"),
                }
                self.logger.debug(
                    f"[LP_LOGGING] Found confirmed dominant plate: '{stable_plate}' (track_id={track_id})"
                )

        return plates_to_log

    def close_plate_sync(self) -> None:
        """Stop the background plate sync sender (best-effort create flush)."""
        plate_sync = self._plate_sync
        if plate_sync is not None:
            try:
                plate_sync.stop()
            except Exception as e:
                self.logger.warning(f"[LP_LOGGING] Error stopping plate sync sender: {e}")

    def __del__(self):
        # No logging here: GC may run after the logging module is torn down.
        with contextlib.suppress(Exception):
            self.close_plate_sync()

    def _apply_profile_gates(self, config: Any) -> None:
        """Bind the per-profile confirmation gates from config onto this instance.

        These used to be literals in ``__init__``. The access-control /
        surveillance split needs them to differ per profile, and this use case --
        unlike the FR one -- takes no config in its constructor, so the binding
        has to happen here, alongside the existing ``ocr_mode``/``ocr_device``
        binding.

        Every ``getattr`` default below is the value that was hard-coded before,
        so a config that predates these fields (or any non-LPR config that
        reaches here) reproduces the old behaviour exactly.

        Note ``confidence_threshold`` is deliberately NOT bound here: ``process``
        overwrites it with a literal 0.37 a few lines above, so a per-profile
        value would be silently discarded. Differentiating on it needs that
        override removed first, which changes live detector behaviour and is out
        of scope for the split.
        """
        self._min_plate_len = int(getattr(config, "min_plate_len", 3) or 3)
        self._max_plate_len = int(getattr(config, "max_plate_len", 10) or 10)
        self._stable_frames_required = int(getattr(config, "stable_frames_required", 1) or 1)
        ocr_floor = getattr(config, "ocr_confidence_threshold", None)
        if ocr_floor is not None:
            self._ocr_confidence_threshold = float(ocr_floor)
        # Mutate the existing smoother rather than rebuilding it: it carries
        # per-camera state that a fresh instance would drop every frame.
        smoother = getattr(self, "_detection_smoother", None)
        if smoother is not None:
            smoother._hold_frames = int(getattr(config, "smoother_hold_frames", 3) or 3)
            smoother._iou_threshold = float(getattr(config, "smoother_iou_threshold", 0.3))

    async def process(
        self,
        data: Any,
        config: ConfigProtocol,
        input_bytes: bytes | None = None,
        context: ProcessingContext | None = None,
        stream_info: Dict[str, Any] | None = None,
    ) -> ProcessingResult:
        processing_start = time.monotonic()
        try:
            if not isinstance(config, LicensePlateMonitorConfig):
                return self.create_error_result(
                    "Invalid configuration type for license plate monitoring",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            if context is None:
                context = ProcessingContext()

            if input_bytes is None or (hasattr(input_bytes, "__len__") and len(input_bytes) == 0):
                return self.create_error_result(
                    "input_bytes (video/image) is required for license plate monitoring",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            # Initialize plate logger once if lpr_server_id is provided (optional flow)
            if not self._plate_logger_initialized and config.lpr_server_id:
                self.logger.info("[LP_LOGGING] First-time initialization - lpr_server_id: %s", config.lpr_server_id)
                success = self._initialize_plate_logger(config)
                if success:
                    self.logger.info("[LP_LOGGING] Plate logger initialized successfully and ready to send plates")
                else:
                    self.logger.error("[LP_LOGGING] Plate logger initialization FAILED - plates will NOT be sent")
            elif self._plate_logger_initialized:
                self.logger.debug("[LP_LOGGING] Plate logger already initialized, skipping re-initialization")
            elif not config.lpr_server_id:
                if self._total_frame_counter == 0:  # Only log once at start
                    self.logger.warning(
                        "[LP_LOGGING] Plate logging will be DISABLED - no lpr_server_id provided in config"
                    )

            # Initialize alert manager once (lazy initialization on first call)
            if not self._alert_manager_initialized:
                self._initialize_alert_manager_once(config)

            # Normalize alert_config if provided as a plain dict (JS JSON)
            if isinstance(getattr(config, "alert_config", None), dict):
                try:
                    config.alert_config = AlertConfig(**config.alert_config)  # type: ignore[arg-type]
                except Exception:
                    # Non-fatal: the raw dict is left in place and alerting degrades.
                    self.logger.warning("[LP] alert_config dict -> AlertConfig coercion failed", exc_info=True)

            # OCR model will be lazily initialized when _run_ocr is first called
            # No need to initialize here

            _t = time.monotonic
            _t0 = _t()

            input_format = match_results_structure(data)
            context.input_format = input_format
            config.confidence_threshold = 0.37
            context.confidence_threshold = config.confidence_threshold
            self._ocr_mode = config.ocr_mode
            if hasattr(config, "ocr_model_name") and config.ocr_model_name:
                self._ocr_model_name = config.ocr_model_name
            if hasattr(config, "ocr_device") and config.ocr_device:
                self._ocr_device = config.ocr_device
            self._apply_profile_gates(config)
            self.logger.debug(
                "Processing license plate monitoring with format: %s and CONFIDENCE THRESHOLD: %s",
                input_format.value,
                config.confidence_threshold,
            )

            # Step 1: Apply confidence filtering
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            self.logger.debug("Applied confidence filtering with threshold %s", config.confidence_threshold)

            # Step 2: Apply category mapping if provided
            if config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
            # Step 3: Filter to target categories (handle dict or list)
            if isinstance(processed_data, dict):
                processed_data = processed_data.get("detections", [])
            effective_targets = getattr(config, "target_categories", self.target_categories) or self.target_categories
            targets_lower = {str(cat).lower() for cat in effective_targets}
            processed_data = [d for d in processed_data if str(d.get("category", "")).lower() in targets_lower]

            # The mask probe has to happen HERE, not at the consumer below: this is the
            # pre-tracker list, and the tracker may drop `mask`/`segmentation` keys, so
            # moving the copy down to the guard would probe the wrong list and silently
            # stop attaching masks. Probing here and copying conditionally keeps both
            # the guard's meaning and the saved work.
            _has_masks = any(d.get("mask") or d.get("segmentation") for d in processed_data[:5])
            raw_processed_data = [copy.deepcopy(det) for det in processed_data] if _has_masks else []

            _t1 = _t()  # after filtering

            # Step 4: Apply bounding box smoothing if enabled
            if config.enable_smoothing:
                if self.smoothing_tracker is None:
                    smoothing_config = BBoxSmoothingConfig(
                        smoothing_algorithm=config.smoothing_algorithm,
                        window_size=config.smoothing_window_size,
                        cooldown_frames=config.smoothing_cooldown_frames,
                        confidence_threshold=config.confidence_threshold,
                        confidence_range_factor=config.smoothing_confidence_range_factor,
                        enable_smoothing=True,
                    )
                    self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
                processed_data = bbox_smoothing(
                    processed_data,
                    self.smoothing_tracker.config,
                    self.smoothing_tracker,
                )

            _t2 = _t()  # after smoothing

            # Step 5: Apply advanced tracking
            if _HAS_ADVANCED_TRACKER:
                try:
                    if self.tracker is None:
                        self.tracker = self._tracker_seam.get_shared_tracker(
                            config,
                            profile=TrackerProfile.DEFAULT,
                        )
                    processed_data = self.tracker.update(processed_data)
                except Exception as e:
                    self.logger.warning(f"AdvancedTracker failed: {e}")

            # Map persistent track IDs back to original data dicts (in-place) so that
            # callers holding a reference (e.g. workers.py → format_output_rtp) see them.
            _map_tracker_ids_to_source(
                data if isinstance(data, list) else data.get("detections", []),
                processed_data,
            )

            # Temporal smoothing — carry forward tracked detections that the model
            # intermittently drops, reducing bbox flickering on the frontend.
            _camera_id = (stream_info or {}).get("camera_id", "")
            _cur_frame_id, _cur_rtp_number = _extract_stream_frame_fields(stream_info)
            processed_data = self._detection_smoother.smooth(
                _camera_id,
                processed_data,
                self._total_frame_counter,
                frame_id=_cur_frame_id,
                rtp_number=_cur_rtp_number,
            )

            _t3 = _t()  # after tracker + smoothing

            # Step 6: Update tracking state
            self._update_tracking_state(processed_data)
            # Step 7: Attach masks to detections (skip if no masks — O(n²) IOU matching)
            if raw_processed_data:  # non-empty only when the pre-tracker probe saw masks
                processed_data = self._attach_masks_to_detections(processed_data, raw_processed_data)

            _t4 = _t()  # after tracking state + masks

            # Step 8: Perform OCR on media
            ocr_analysis = self._analyze_ocr_in_media(processed_data, input_bytes, config)

            _n_ocr_ok = sum(1 for r in ocr_analysis if r.get("plate_text"))
            _n_rejected = sum(1 for r in ocr_analysis if r.get("reject_reason"))
            _n_ocr_run = sum(1 for r in ocr_analysis if not r.get("ocr_cached"))

            _t5 = _t()  # after OCR

            # Step 9: Update plate texts
            processed_data = self._update_detections_with_ocr(processed_data, ocr_analysis)
            self._stamp_detections_frame_ids(processed_data, stream_info)
            self._update_plate_texts(processed_data)

            _t6 = _t()  # after plate text update

            # Step 10: Update frame counter
            self._total_frame_counter += 1

            # Step 11: Extract frame information
            frame_number = None
            if stream_info:
                input_settings = stream_info.get("input_settings", {})
                start_frame = input_settings.get("start_frame")
                end_frame = input_settings.get("end_frame")
                if start_frame is not None and end_frame is not None and start_frame == end_frame:
                    frame_number = start_frame

            # Step 12: Calculate summaries (computes dominant plates from history)
            counting_summary = self._count_categories(processed_data, config)
            counting_summary["total_counts"] = self.get_total_counts()

            _t8 = _t()  # after counting

            # Step 12.5: Log CONFIRMED/DOMINANT plates to RPC server
            confirmed_detections = counting_summary.get("detections", [])
            # Hand confirmed plates to the bounded background sender (non-blocking,
            # coalescing): the frame is never blocked on lpr-server HTTP POSTs and
            # no asyncio task is scheduled on this (processing) loop.

            if confirmed_detections:
                self._offer_detected_plates(confirmed_detections, config, stream_info, input_bytes)

            _t8a = _t()  # after the plate offer (the frame JPEG encode lives in here)

            # Step 12.6: Instant BOLO alerts — after confirmation + anchor freeze so
            # rtp_number/frame_id match the first sighting, not a later frame.
            if confirmed_detections:
                try:
                    self._send_instant_alerts(confirmed_detections, stream_info, config)
                except Exception as e:
                    self.logger.error(
                        "[ALERT] Instant alert dispatch failed (frame continues): %s",
                        e,
                        exc_info=True,
                    )
                self._commit_pending_plate_sightings()

            _t8b = _t()  # after instant alerts + sighting commit (synchronous alert publish)

            # Step 13: Generate alerts and summaries
            alerts = self._check_alerts(counting_summary, frame_number, config)
            incidents_list = self._generate_incidents(counting_summary, alerts, config, frame_number, stream_info)
            tracking_stats_list = self._generate_tracking_stats(
                counting_summary, alerts, config, frame_number, stream_info
            )
            business_analytics_list = []
            summary_list = self._generate_summary(
                counting_summary,
                incidents_list,
                tracking_stats_list,
                business_analytics_list,
                alerts,
            )

            _t9 = _t()  # after summaries

            # Step 14: Build result
            incidents = incidents_list[0] if incidents_list else {}
            tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
            business_analytics = business_analytics_list[0] if business_analytics_list else {}
            summary = summary_list[0] if summary_list else {}
            # NOTE: a `LPR_dict` / `counter` pair used to be built here -- a list copy
            # plus a Counter over EVERY track id ever seen, on every frame, and read by
            # nothing (`self.helper` is only cleared by an external
            # `reset_plate_tracking()`, so the cost grew with uptime without bound:
            # measured 1.4 ms at 500 accumulated tracks, 235 ms at 10,000). Deleted.
            # `_count_categories` already derives the dominant plate per track for the
            # summary; if a per-track history dump is ever needed on the wire, build it
            # from `self.helper` at the point of use, not unconditionally per frame.
            agg_summary = {
                str(frame_number): {
                    "incidents": incidents,
                    "tracking_stats": tracking_stats,
                    "business_analytics": business_analytics,
                    "alerts": alerts,
                    "human_text": summary,
                }
            }

            context.mark_completed()
            result = self.create_result(
                data={"agg_summary": agg_summary},
                usecase=self.name,
                category=self.category,
                context=context,
            )
            _t10 = _t()  # after result build
            proc_time = time.monotonic() - processing_start
            processing_latency_ms = proc_time * 1000.0
            processing_fps = (1.0 / proc_time) if proc_time > 0 else 0.0
            self.logger.debug(
                "[LPR_FRAME] F%s | %d dets | %d OCR ok | %d rejected | latency=%.1fms fps=%.1f",
                frame_number,
                len(processed_data),
                _n_ocr_ok,
                _n_rejected,
                processing_latency_ms,
                processing_fps,
            )
            _t11 = _t()  # after the [LPR_FRAME] line -- the `log=` column below
            if self.logger.isEnabledFor(logging.DEBUG):
                # Every span between _t0 and _t11 is attributed, and `cols` is printed
                # next to `latency` so the un-instrumented prologue (logger + alert
                # manager init, config normalisation) shows up as a residual instead of
                # being assumed free. Previously `alerts=` was always ~0.0 because its
                # end marker was set one statement after its start, `state=` was missing
                # entirely, and count/offer/sync_alerts/summary/build/log were computed
                # but never printed -- so the most expensive part of the frame was the
                # part the log did not mention.
                _spans = (
                    (_t1 - _t0),
                    (_t2 - _t1),
                    (_t3 - _t2),
                    (_t4 - _t3),
                    (_t5 - _t4),
                    (_t6 - _t5),
                    (_t8 - _t6),
                    (_t8a - _t8),
                    (_t8b - _t8a),
                    (_t9 - _t8b),
                    (_t10 - _t9),
                    (_t11 - _t10),
                )
                self.logger.debug(
                    "[LPR_TIMING] %s F%s filter=%.1f smooth=%.1f track=%.1f state=%.1f ocr=%.1f(n=%d) "
                    "plates=%.1f count=%.1f offer=%.1f sync_alerts=%.1f summary=%.1f build=%.1f log=%.1f "
                    "| cols=%.1f latency=%.1f tracks=%d anchors=%d",
                    self.name,
                    frame_number,
                    _spans[0] * 1e3,
                    _spans[1] * 1e3,
                    _spans[2] * 1e3,
                    _spans[3] * 1e3,
                    _spans[4] * 1e3,
                    _n_ocr_run,
                    _spans[5] * 1e3,
                    _spans[6] * 1e3,
                    _spans[7] * 1e3,
                    _spans[8] * 1e3,
                    _spans[9] * 1e3,
                    _spans[10] * 1e3,
                    _spans[11] * 1e3,
                    sum(_spans) * 1e3,
                    processing_latency_ms,
                    len(self.helper),
                    len(self._plate_create_anchors),
                )
                # Both joins are only ever fed to a DEBUG log, so they belong inside
                # this guard -- they used to be built unconditionally.
                plates_str = " ".join(
                    f"{r['plate_text']}({r.get('ocr_confidence', 0):.2f})" for r in ocr_analysis if r.get("plate_text")
                )
                if plates_str:
                    self.logger.debug("[LPR_PLATES] F%s | %s", frame_number, plates_str)
                rejected_str = " ".join(
                    f"{r.get('raw_text', '')}({r.get('ocr_confidence', 0):.2f},{r.get('reject_reason', '')})"
                    for r in ocr_analysis
                    if r.get("reject_reason")
                )
                if rejected_str:
                    self.logger.debug("[LPR_REJECTED] F%s | %s", frame_number, rejected_str)
            return result

        except Exception as e:
            self.logger.error(f"License plate monitoring failed: {str(e)}", exc_info=True)
            if context:
                context.mark_completed()
            return self.create_error_result(
                str(e),
                type(e).__name__,
                usecase=self.name,
                category=self.category,
                context=context,
            )

    def _is_video_bytes(self, media_bytes: bytes) -> bool:
        """Determine if bytes represent a video file."""
        video_signatures = [
            b"\x00\x00\x00\x20ftypmp4",  # MP4
            b"\x00\x00\x00\x18ftypmp4",  # MP4 variant
            b"RIFF",  # AVI
            b"\x1aE\xdf\xa3",  # MKV/WebM
            b"ftyp",  # General MP4 family
        ]
        for signature in video_signatures:
            if media_bytes.startswith(signature) or signature in media_bytes[:50]:
                return True
        return False

    def _analyze_ocr_in_media(
        self, data: Any, media_bytes: bytes, config: LicensePlateMonitorConfig
    ) -> List[Dict[str, Any]]:
        """Analyze OCR of license plates in video frames or images."""
        result = self._analyze_ocr_in_image(data, media_bytes, config)
        # Store timing metadata for process() to log
        self._last_img_src = getattr(self, "_last_img_src", "unknown")
        self._last_decode_ms = getattr(self, "_last_decode_ms", 0.0)
        self._last_cvt_ms = getattr(self, "_last_cvt_ms", 0.0)
        return result

    def _analyze_ocr_in_image(self, data: Any, image_bytes, config: LicensePlateMonitorConfig) -> List[Dict[str, Any]]:
        """Analyze OCR in a single image. Accepts JPEG bytes, raw BGR numpy, or __RAW_BGR__ sentinel."""
        _mt = time.monotonic
        _img_t0 = _mt()
        image, _img_src = self._resolve_ocr_image(image_bytes)
        _img_t1 = _mt()
        # Handed to `_encode_frame_for_plate` later in this same process() call so the
        # plate image does not pay a second decode of the same bytes. Reset (not left
        # stale) on failure, so a later call can never encode a previous frame.
        self._last_resolved_frame = image

        if image is None:
            self.logger.warning(
                f"Failed to decode image from bytes (src={_img_src}, "
                f"type={type(image_bytes).__name__}, "
                f"len={len(image_bytes) if hasattr(image_bytes, '__len__') else '?'})"
            )
            return []

        # The full-frame BGR->RGB conversion used to happen here, unconditionally --
        # so it was paid with zero detections and when every read was cache-served.
        # Crops are ~200x60, so converting per crop instead is ~100x cheaper
        # (measured 0.48 ms -> 0.005 ms at 1080p, 2.83 ms -> 0.004 ms at 4K).
        # `_crop_bbox` clamps against `image.shape[:2]`, which is identical either
        # way, so crop geometry is unchanged -- but the array handed to OCR must
        # stay RGB, hence the conversion below at the point of use.
        _cvt_ms_total = 0.0
        _img_t2 = _mt()
        ocr_analysis = []
        detections = self._get_frame_detections(data, "0")

        # Two passes, so every crop this frame still needs OCR for goes to the model in
        # ONE call instead of one blocking IPC round trip each (~80-180 ms apiece --
        # three unstable plates used to cost a quarter to half a second here). Pass 1
        # crops, applies the stability cache, and appends a record per detection in
        # detection order (`detection_id` and the [LPR_PLATES]/[LPR_REJECTED] strings
        # depend on that order); pass 2 fills in the records the cache could not.
        _pending: "List[Tuple[int, np.ndarray, int, int]]" = []  # (record idx, RGB crop, w, h)

        for detection in detections:
            if detection.get("confidence", 1.0) < config.confidence_threshold:
                continue

            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                self.logger.debug("Detection has no bounding_box or bbox key")
                continue

            crop = self._crop_bbox(image, bbox, config.bbox_format)  # BGR
            if crop.size == 0:
                continue

            track_id = detection.get("track_id")
            # Skip OCR if track already has stable plate text (saves ~80-180ms per detection)
            ocr_result = None
            if track_id is not None and hasattr(self, "helper") and track_id in self.helper:
                hist = self.helper[track_id]
                if len(hist) >= 3:
                    half = max(1, len(hist) // 2)
                    dom, cnt = Counter(hist[-half:]).most_common(1)[0]
                    if dom and cnt >= 2:
                        # Stable text exists — reuse it, skip expensive OCR
                        ocr_result = {
                            "text": dom,
                            "avg_conf": 0.95,
                            "raw_text": dom,
                            "char_confs": [],
                            "rejected": False,
                            "reject_reason": None,
                        }
            _ocr_skipped = ocr_result is not None

            crop_h, crop_w = crop.shape[:2]
            ocr_record = {
                "frame_id": "0",
                "timestamp": 0.0,
                "category": detection.get("category", ""),
                "confidence": round(detection.get("confidence", 0.0), 3),
                "plate_text": None,
                "bbox": bbox,
                "detection_id": detection.get("id", f"det_{len(ocr_analysis)}"),
                "track_id": track_id,
                "ocr_confidence": 0.0,
                "reject_reason": None,
                "raw_text": "",
                "ocr_ms": 0.0,
                # True when the stability cache served this read, so `[LPR_TIMING]`'s
                # `n=` counts only crops that actually reached the model. That count is
                # what decides whether batching OCR is worth building at all.
                "ocr_cached": _ocr_skipped,
            }
            ocr_analysis.append(ocr_record)

            if _ocr_skipped:
                self._apply_ocr_to_record(ocr_record, ocr_result, 0.0, crop_w, crop_h, cached=True)
            else:
                _cvt_t0 = _mt()
                rgb_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
                _cvt_ms_total += (_mt() - _cvt_t0) * 1000.0
                _pending.append((len(ocr_analysis) - 1, rgb_crop, crop_w, crop_h))

        if _pending:
            _t0 = _mt()
            _results = self._run_ocr_batch([crop for _, crop, _, _ in _pending])
            # Amortised: the model was called once for the whole batch, so there is no
            # honest per-crop figure to report. `[LPR_TIMING]`'s `ocr=`/`n=` pair is the
            # number to reason about.
            _per_crop_ms = (_mt() - _t0) * 1000.0 / len(_pending)
            for (idx, _crop, _w, _h), _result in zip(_pending, _results, strict=False):
                self._apply_ocr_to_record(ocr_analysis[idx], _result, _per_crop_ms, _w, _h, cached=False)

        # Store timing on self so process() can log it (in case logger doesn't work here)
        self._last_img_src = _img_src
        self._last_decode_ms = (_img_t1 - _img_t0) * 1e3
        # Now the summed per-crop conversions rather than one full-frame convert.
        self._last_cvt_ms = _cvt_ms_total
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(
                "[LPR_IMG] src=%s shape=%s decode=%.1fms cvt=%.1fms n_dets=%d total_ocr_ms=%.1f",
                _img_src,
                image.shape,
                self._last_decode_ms,
                self._last_cvt_ms,
                len(detections),
                sum(r.get("ocr_ms", 0) for r in ocr_analysis),
            )
        return ocr_analysis

    def _crop_bbox(self, image: np.ndarray, bbox: Dict[str, Any], bbox_format: str) -> np.ndarray:
        """Crop bounding box region from image."""
        h, w = image.shape[:2]

        if bbox_format == "auto":
            if "xmin" in bbox:
                bbox_format = "xmin_ymin_xmax_ymax"
            elif "x" in bbox:
                bbox_format = "x_y_width_height"
            else:
                return np.zeros((0, 0, 3), dtype=np.uint8)

        if bbox_format == "xmin_ymin_xmax_ymax":
            xmin = max(0, int(bbox["xmin"]))
            ymin = max(0, int(bbox["ymin"]))
            xmax = min(w, int(bbox["xmax"]))
            ymax = min(h, int(bbox["ymax"]))
        elif bbox_format == "x_y_width_height":
            xmin = max(0, int(bbox["x"]))
            ymin = max(0, int(bbox["y"]))
            xmax = min(w, int(bbox["x"] + bbox["width"]))
            ymax = min(h, int(bbox["y"] + bbox["height"]))
        else:
            return np.zeros((0, 0, 3), dtype=np.uint8)

        return image[ymin:ymax, xmin:xmax]

    # ------------------------------------------------------------------
    # Fast OCR helpers
    # ------------------------------------------------------------------
    def set_bgr_frame(self, bgr_frame):
        """Set raw BGR frame for OCR analysis (avoids JPEG encode/decode loss).

        Mirrors the frame into a thread-local shared holder so the ``__RAW_BGR__``
        fast path still works when the caller sets the frame on one use-case
        instance but runs ``process()`` on another (the inference pipeline
        reuses a single holder across cached use cases). The thread-local keeps
        concurrent camera worker threads isolated.
        """
        self._bgr_frame = bgr_frame
        _BGR_FRAME_TLS.frame = bgr_frame

    def _encode_frame_for_plate(self, image_bytes) -> str:
        """The frame as a base64 JPEG for a plate record, or ``""`` if unavailable.

        Called at most once per ``_offer_detected_plates`` call, and only once a plate
        has actually cleared the offer gates -- see the memoising closure there.

        Prefers the frame ``_analyze_ocr_in_image`` already decoded this same
        ``process()`` call: on the encoded-bytes path this method would otherwise run a
        second full ``cv2.imdecode`` of bytes that were just decoded. It is never stale,
        because OCR always runs earlier in the same call.
        """
        if image_bytes is None:
            self.logger.debug("[LP_LOGGING] No image_bytes provided, sending without image")
            return ""
        try:
            image = self._last_resolved_frame
            if image is None:
                image, _ = self._resolve_ocr_image(image_bytes)
            if image is None:
                self.logger.warning("[LP_LOGGING] Failed to decode image bytes")
                return ""
            success, jpeg_buffer = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, _PLATE_JPEG_QUALITY])
            if not success:
                self.logger.warning("[LP_LOGGING] Failed to encode JPEG image")
                return ""
            return base64.b64encode(jpeg_buffer.tobytes()).decode("utf-8")
        except Exception as e:
            self.logger.error("[LP_LOGGING] Exception while encoding frame image: %s", e, exc_info=True)
            return ""

    def _resolve_ocr_image(self, image_bytes):
        """Resolve OCR input to a BGR ndarray. Returns ``(image | None, src_label)``.

        Handles three forms the pipeline may pass:
        * an ndarray -> used directly;
        * the ``b"__RAW_BGR__"`` sentinel -> the raw frame from this instance,
          else the thread-local shared frame (bridges a cross-instance hand-off);
        * encoded bytes (JPEG/PNG) -> ``cv2.imdecode``.

        When the sentinel arrives but no raw frame is available anywhere, log a
        loud, greppable contract-violation error instead of silently feeding the
        11-byte sentinel into ``imdecode`` (which yields a misleading
        "Failed to decode jpeg(11B)").
        """
        if image_bytes is None:
            return None, "none"
        if isinstance(image_bytes, np.ndarray):
            return image_bytes, "numpy"
        if image_bytes == b"__RAW_BGR__":
            frame = self._bgr_frame
            if frame is None:
                frame = getattr(_BGR_FRAME_TLS, "frame", None)
                if frame is not None:
                    return frame, "bgr_tls"
                self.logger.error(
                    "[LPR] __RAW_BGR__ sentinel received but no raw BGR frame is "
                    "available on this instance (id=%s) or the thread-local holder; "
                    "set_bgr_frame() was not called on this worker thread. OCR skipped.",
                    id(self),
                )
                return None, "raw_bgr_missing"
            return frame, "bgr_holder"
        image_array = np.frombuffer(image_bytes, np.uint8)
        return cv2.imdecode(image_array, cv2.IMREAD_COLOR), f"jpeg({len(image_bytes)}B)"

    def _assert_or_warn_gpu_ocr(self, bound_providers, source: str) -> None:
        """Guard against OCR silently running on CPU on a GPU-required platform.

        ``bound_providers`` is the list of ORT execution providers the OCR model
        is *actually* bound to (the subprocess worker's reported ``bound_providers``
        or the in-process session's ``get_providers()``). ``source`` is "subprocess"
        or "in-process" for the log.

        On a GPU-required platform (``MATRICE_PLATFORM`` in gpu/thor/orin/blackwell)
        with no GPU execution provider bound:
          - ``MATRICE_OCR_REQUIRE_GPU=1`` -> raise (hard-fail, refuse CPU OCR).
          - otherwise -> set ``_ocr_degraded_cpu`` and emit a periodic, throttled,
            multi-line ERROR (keeps producing plates on CPU, but loudly visible).
        On non-GPU platforms, or when a GPU provider is bound, this is a no-op.
        """
        platform = os.environ.get("MATRICE_PLATFORM", "").strip().lower()
        if platform not in _GPU_REQUIRED_PLATFORMS:
            return
        providers = list(bound_providers or [])
        if any(p in _GPU_EXECUTION_PROVIDERS for p in providers):
            # Healthy: a GPU provider is bound.
            self._ocr_degraded_cpu = False
            return

        msg = (
            "\n" + "=" * 72 + "\n"
            "LPR OCR DEGRADED TO CPU on a GPU-required host\n"
            f"  platform        : {platform}\n"
            f"  ocr path        : {source}\n"
            f"  bound providers : {providers or '[]'}\n"
            "  impact          : plate-read quality/throughput reduced "
            "(detection via TRT is unaffected)\n"
            "  fix             : ensure the isolated OCR venv has onnxruntime-gpu "
            "(MATRICE_OCR_AUTO_VENV=1 / pre-baked /opt/ocr-venv)\n"
            "  strict mode     : set MATRICE_OCR_REQUIRE_GPU=1 to hard-fail instead "
            "of degrading\n" + "=" * 72
        )
        if os.environ.get("MATRICE_OCR_REQUIRE_GPU") == "1":
            raise RuntimeError(msg)

        # warn-and-degrade: keep the CPU model, but re-log periodically so the
        # degraded state stays visible (not a one-shot warning).
        self._ocr_degraded_cpu = True
        now = time.monotonic()
        last = getattr(self, "_last_cpu_warn_ts", 0.0)
        if last == 0.0 or (now - last) >= _CPU_DEGRADE_WARN_INTERVAL_S:
            self._last_cpu_warn_ts = now
            self.logger.error(msg)

    def _try_load_subprocess_ocr(self) -> bool:
        """Try to bring up the isolated GPU OCR subprocess as ``self.ocr_model``.

        Opt-in: the subprocess is used when ``MATRICE_OCR_PYTHON`` points at an
        isolated venv interpreter, or when ``MATRICE_OCR_AUTO_VENV=1`` lets the
        client create/repair that venv at runtime. It exists for platforms where
        onnxruntime-gpu cannot share a process with cupy (numpy>=2) or where a
        dual onnxruntime/onnxruntime-gpu install hides the GPU provider. On
        images where OCR coexists in-process under one numpy ABI, both vars are
        unset and OCR runs in-process on the GPU.

        Returns True if the subprocess is GPU-ready. On failure it sets
        ``_ocr_subprocess_failed`` so we don't re-spawn on every frame, and the
        caller falls through to the in-process path.
        """
        if self._ocr_subprocess_failed:
            return False
        if not os.environ.get("MATRICE_OCR_PYTHON") and os.environ.get("MATRICE_OCR_AUTO_VENV") != "1":
            # No isolated OCR venv configured and auto-creation disabled ->
            # run OCR in-process. With MATRICE_OCR_AUTO_VENV=1 the client
            # bootstraps the venv on demand, so let the subprocess path proceed.
            return False

        # Hand the worker the FULL preferred order and let it bind what it can.
        #
        # Deliberately NOT intersected with this process's onnxruntime
        # capabilities. The worker runs a different interpreter with a different
        # onnxruntime build, and that difference is the entire reason the venv
        # exists: the parent needs numpy>=2 for cupy and therefore carries the
        # CPU-only `onnxruntime` wheel, while the venv carries `onnxruntime-gpu`
        # on numpy<2. Intersecting the wanted providers against the parent's
        # therefore collapsed
        #     ('CUDAExecutionProvider', 'CPUExecutionProvider')
        #        n ['AzureExecutionProvider', 'CPUExecutionProvider']
        #     = ['CPUExecutionProvider']
        # and pinned a fully GPU-capable worker to CPU on every Thor/Orin
        # deployment -- the isolation was defeated by the check meant to protect
        # it. The venv here reports ['TensorrtExecutionProvider',
        # 'CUDAExecutionProvider', 'CPUExecutionProvider'] and binds CUDA fine.
        #
        # Dropping the probe also removes a side effect: get_ort_providers()
        # attempts a `pip install onnxruntime-gpu` "repair" of the PARENT
        # interpreter, which fails on Thor (and would break cupy's numpy>=2 if it
        # succeeded) -- that is the CalledProcessError traceback in the log.
        #
        # The worker reports its real EPs back via health['bound_providers'],
        # which _assert_or_warn_gpu_ocr checks below, so a genuinely CPU-only
        # worker is still caught -- just diagnosed instead of caused.
        preferred = _preferred_ocr_providers()
        chosen_providers = list(preferred)

        try:
            from ..ocr._ocr_subprocess_client import get_shared_ocr_client

            model_name = getattr(self, "_ocr_model_name", "cct-s-v1-global-model")
            client = get_shared_ocr_client(model_name, chosen_providers)
            started = client.start()
        except Exception as e:
            # An exception here is an unexpected wiring error, not a known
            # transient -> latch off to avoid per-frame exceptions.
            self._ocr_subprocess_failed = True
            self.logger.warning(
                "OCR subprocess init raised (%s); falling back to in-process CPU OCR.",
                e,
            )
            return False

        if not started:
            # Only give up permanently if the client classified the failure as
            # non-recoverable (missing onnxruntime / interpreter). A transient
            # failure (e.g. a model-download 504) is left unlatched so a later
            # frame retries -- the client rate-limits the actual re-start via its
            # cooldown, so this is cheap per frame.
            if getattr(client, "is_permanently_unavailable", lambda: False)():
                self._ocr_subprocess_failed = True
                self.logger.warning("OCR subprocess permanently unavailable; using in-process CPU OCR.")
            else:
                self.logger.info("OCR subprocess not ready yet (transient); will retry on a later frame.")
            return False

        # Started OK. Guard BEFORE adopting the model and OUTSIDE the try above so
        # a hard-fail (MATRICE_OCR_REQUIRE_GPU=1) propagates instead of being
        # swallowed. Use the worker's reported bound providers (its actual EPs).
        health = getattr(client, "health", None) or {}
        self._assert_or_warn_gpu_ocr(health.get("bound_providers", []), "subprocess")
        self.ocr_model = client
        self.logger.info(
            "OCR subprocess loaded (model=%s, providers=%s, bound=%s)",
            model_name,
            chosen_providers,
            health.get("bound_providers", []),
        )
        return True

    def _ensure_ocr_model_loaded(self) -> bool:
        """Lazy initialization of OCR model with retry. Returns True if model is available."""
        if self.ocr_model is not None:
            return True

        # Primary path: isolated GPU OCR subprocess. Falls through to the
        # in-process CPU recognizer below if it can't be brought up.
        if self._ocr_use_subprocess and self._try_load_subprocess_ocr():
            return True

        if self._ocr_initialization_attempts >= self._ocr_max_init_attempts:
            return False

        self._ocr_initialization_attempts += 1
        attempt = self._ocr_initialization_attempts

        # Try to get the LicensePlateRecognizer class via the module-level helper.
        # Importing the local fork runs the ORT-GPU pre-flight in its __init__.py.
        LicensePlateRecognizerClass = _get_license_plate_recognizer_class()

        # Direct import fallback if the helper returns None
        if LicensePlateRecognizerClass is None:
            self.logger.warning(
                f"OCR init attempt {attempt}/{self._ocr_max_init_attempts}: "
                "module-level import returned None, trying direct import..."
            )
            try:
                from fast_plate_ocr import LicensePlateRecognizer as _DirectLPR

                LicensePlateRecognizerClass = _DirectLPR
                self.logger.info("Direct import of LicensePlateRecognizer succeeded")
            except ImportError as e:
                self.logger.error(f"Direct import also failed: {e}")

        if LicensePlateRecognizerClass is None:
            self.logger.error(
                f"OCR init attempt {attempt}/{self._ocr_max_init_attempts}: LicensePlateRecognizer class unavailable"
            )
            return False

        # Build the OCR model. If the local fork's pre-flight surfaced GPU
        # providers, pass an explicit ordered providers list (CUDA-first; see
        # _preferred_ocr_providers for why TRT is opt-in). Otherwise honor the
        # configured device.
        model_name = getattr(self, "_ocr_model_name", "cct-s-v1-global-model")
        configured_device = getattr(self, "_ocr_device", "auto")
        preferred = _preferred_ocr_providers()
        try:
            from ..ocr._deps_check import get_ort_providers

            _ort_providers = get_ort_providers()
        except Exception:
            _ort_providers = []
        _platform = os.environ.get("MATRICE_PLATFORM", "").strip().lower()
        try:
            if configured_device == "auto":
                if _ort_providers:
                    chosen_providers = [p for p in preferred if p in _ort_providers]
                elif _platform in _GPU_REQUIRED_PLATFORMS:
                    # On a GPU box, request the GPU EPs rather than silently
                    # pinning CPU; the guard below verifies what actually bound.
                    chosen_providers = list(preferred)
                else:
                    chosen_providers = ["CPUExecutionProvider"]
                self.ocr_model = LicensePlateRecognizerClass(model_name, providers=chosen_providers)
                self.logger.info(
                    "LicensePlateRecognizer loaded on attempt %d (model=%s, providers=%s, ort_providers=%s)",
                    attempt,
                    model_name,
                    chosen_providers,
                    _ort_providers,
                )
            else:
                self.ocr_model = LicensePlateRecognizerClass(model_name, device=configured_device)
                self.logger.info(
                    "LicensePlateRecognizer loaded on attempt %d (model=%s, device=%s, ort_providers=%s)",
                    attempt,
                    model_name,
                    configured_device,
                    _ort_providers,
                )
        except Exception as e:
            self.logger.error(
                f"OCR init attempt {attempt}/{self._ocr_max_init_attempts} failed: {e}",
                exc_info=True,
            )
            self.ocr_model = None
            return False

        # Guard AFTER successful construction (outside the try so hard-fail
        # raises propagate instead of being swallowed as an init failure). Read
        # the actually-bound providers from the live ORT session.
        try:
            bound = list(self.ocr_model.model.get_providers())
        except Exception:
            bound = chosen_providers if configured_device == "auto" else [configured_device]
        self._assert_or_warn_gpu_ocr(bound, "in-process")
        return True

    def _clean_text(self, text: str) -> str:
        """Sanitise OCR output to keep only alphanumerics and uppercase."""
        if not text:
            return ""
        return self._non_alnum_regex.sub("", text).upper()

    # OCR-confusable character classes observed in production fragments
    # (EY09VWS/EY09VW5/EV09VWS, NL640CX/NL64OGX, ...): each maps to one
    # canonical representative so variants of the same physical plate
    # normalize to the same key. Used ONLY for grouping/uniqueness — the
    # displayed text stays the raw OCR majority variant.
    _PLATE_CANON_TRANS = str.maketrans(
        {
            "O": "0",
            "Q": "0",
            "I": "1",
            "S": "5",
            "Z": "2",
            "B": "8",
            "Y": "V",
        }
    )

    def _normalize_plate(self, text: str) -> str:
        """Canonical form of a plate text for variant merging (0/O, 5/S, ...)."""
        return self._clean_text(text).translate(self._PLATE_CANON_TRANS)

    def _dominant_from_window(self, window: List[str]) -> str | None:
        """Majority text over *window* with OCR-confusable variants merged.

        Groups readings by their normalized form, picks the dominant group,
        then returns that group's most frequent ORIGINAL spelling — so one
        physical plate fragmented into EY09VWS/EY09VW5/EV09VWS still
        resolves to a single dominant text instead of splitting the vote.
        """
        if not window:
            return None
        groups: Dict[str, Counter] = defaultdict(Counter)
        for text in window:
            groups[self._normalize_plate(text)][text] += 1
        best_group = max(groups.values(), key=lambda c: sum(c.values()))
        dominant, _ = best_group.most_common(1)[0]
        return dominant

    def _plates_match(self, a: str, b: str) -> bool:
        """True when two plate readings are the same plate modulo OCR confusions."""
        return self._normalize_plate(a) == self._normalize_plate(b)

    @staticmethod
    def _empty_ocr_result(reason: Optional[str]) -> dict:
        return {
            "text": "",
            "avg_conf": 0.0,
            "raw_text": "",
            "char_confs": [],
            "rejected": True,
            "reject_reason": reason,
        }

    def _ocr_run_raw(self, crops: "List[np.ndarray]"):
        """``(texts, confs)`` for ``crops``, recovering once from a dead GPU worker.

        A single crop is passed as ``crops[0]``, **not** as a one-element list, so the
        N==1 case -- the common one, because the stability cache skips settled tracks --
        takes byte-for-byte the call path it took before batching existed.
        """
        source = crops[0] if len(crops) == 1 else crops
        try:
            result = self.ocr_model.run(source, return_confidence=True)
        except _OcrSubprocessUnavailable as exc:
            # The GPU subprocess died mid-session. Drop it, disable the
            # subprocess path, and retry once via the in-process CPU OCR.
            self.logger.warning(
                "OCR subprocess became unavailable (%s); switching to in-process CPU OCR.",
                exc,
            )
            self.ocr_model = None
            self._ocr_use_subprocess = False
            self._ocr_subprocess_failed = True
            if not self._ensure_ocr_model_loaded() or self.ocr_model is None:
                raise
            result = self.ocr_model.run(source, return_confidence=True)

        # Normalize across upstream versions: <=1.0.x returns a
        # (texts, confs) tuple; >=1.1.0 returns list[PlatePrediction]. The
        # subprocess path already hands back a tuple (the worker normalizes),
        # but the in-process recognizer returns the raw upstream shape.
        from ..ocr._ocr_ipc import normalize_run_result

        return normalize_run_result(result)

    # Class-level default so an instance built without running __init__ (the OCR test
    # harness does exactly this) still has a defined latch state.
    _ocr_batch_supported: Optional[bool] = None

    def _run_ocr_batch(self, crops: "List[np.ndarray]") -> "List[dict]":
        """OCR several crops, in one model call where the model supports it.

        Result ``i`` belongs to ``crops[i]``. Batching collapses N IPC round trips to
        the OCR subprocess into one; each round trip costs ~80-180 ms, so a frame with
        three unstable plates was spending a quarter to half a second here.

        Falls back to per-crop OCR, permanently for this process, if the model turns
        out not to honour a list. The length check is the load-bearing half of that:
        a recognizer that silently ignored batching would return one text for N crops,
        and associating it with all of them would put the wrong plate on a record --
        a wrong-gate-opens defect, not a slow one.
        """
        if not crops:
            return []
        if not self._ensure_ocr_model_loaded() or self.ocr_model is None or not hasattr(self.ocr_model, "run"):
            return [self._empty_ocr_result("ocr_model_unavailable") for _ in crops]

        if len(crops) >= 2 and self._ocr_batch_supported is not False:
            try:
                texts, confs = self._ocr_run_raw(crops)
                if len(texts) != len(crops) or (confs is not None and len(confs) != len(crops)):
                    raise ValueError(f"batched OCR returned {len(texts)} texts for {len(crops)} crops")
                self._ocr_batch_supported = True
                return [
                    self._interpret_ocr_result(
                        texts[i] if i < len(texts) else "",
                        confs[i] if confs is not None and i < len(confs) else [],
                    )
                    for i in range(len(crops))
                ]
            except _OcrSubprocessUnavailable:
                # A dead worker says nothing about batch support -- do NOT latch it
                # off here, or one GPU hiccup would disable batching for good.
                return [self._empty_ocr_result("ocr_model_unavailable") for _ in crops]
            except Exception as exc:
                self._ocr_batch_supported = False
                self.logger.warning(
                    "OCR model does not support batched run (%s); falling back to "
                    "per-crop OCR for the rest of this process's life.",
                    exc,
                )

        return [self._run_ocr(crop) for crop in crops]

    def _run_ocr(self, crop: np.ndarray) -> dict:
        """Run OCR on a cropped plate image. Returns dict with text, confidence, and diagnostics."""
        _empty = self._empty_ocr_result

        if crop is None or crop.size == 0:
            return _empty("empty_crop")

        if not self._ensure_ocr_model_loaded() or self.ocr_model is None or not hasattr(self.ocr_model, "run"):
            return _empty("ocr_model_unavailable")

        try:
            try:
                texts, confs = self._ocr_run_raw([crop])
            except _OcrSubprocessUnavailable:
                return _empty("ocr_model_unavailable")
            return self._interpret_ocr_result(
                texts[0] if texts else "",
                confs[0] if confs is not None and len(confs) > 0 else [],
            )
        except Exception as exc:
            self.logger.warning("OCR exception: %s", exc)
            return _empty("ocr_exception")

    def _apply_ocr_to_record(
        self,
        record: dict,
        ocr_result: dict,
        ocr_ms: float,
        crop_w: int,
        crop_h: int,
        cached: bool,
    ) -> None:
        """Write one OCR read onto its record, and log it.

        Split out so the cache-served and model-served paths cannot disagree about
        which fields a record carries.
        """
        record["plate_text"] = ocr_result["text"] or None
        record["ocr_confidence"] = round(ocr_result["avg_conf"], 3)
        record["reject_reason"] = ocr_result["reject_reason"]
        record["raw_text"] = ocr_result["raw_text"]
        record["ocr_ms"] = round(ocr_ms, 1)
        # Per detection, per frame. Was an eager f-string at INFO, so the string was
        # built and emitted in production on every read; DEBUG matches the other
        # [LPR_*] lines ([LPR_TIMING], [LPR_FRAME], [LPR_PLATES], [LPR_REJECTED]),
        # which are all already DEBUG.
        self.logger.debug(
            "[LPR_OCR] track=%s crop=%dx%d text=%r conf=%.2f reason=%s ocr_ms=%.1f%s",
            record.get("track_id"),
            crop_w,
            crop_h,
            ocr_result["text"],
            ocr_result["avg_conf"],
            ocr_result.get("reject_reason"),
            ocr_ms,
            " CACHED" if cached else "",
        )

    def _interpret_ocr_result(self, raw_text: str, char_confs_raw) -> dict:
        """Turn one model read into the result dict: confidence, cleaning, rejections.

        Lifted verbatim out of ``_run_ocr`` so the single-crop and batched paths cannot
        drift apart on thresholds or ``reject_reason`` values.
        """
        try:
            raw_text = raw_text or ""
            have_confs = char_confs_raw is not None and len(char_confs_raw) > 0
            if have_confs:
                valid_confs = [
                    float(c) for j, c in enumerate(char_confs_raw) if j < len(raw_text) and raw_text[j] != "_"
                ]
                avg_conf = sum(valid_confs) / len(valid_confs) if valid_confs else 0.0
                char_confs_list = [round(float(c), 3) for c in char_confs_raw]

                if avg_conf < self._ocr_confidence_threshold:
                    return {
                        "text": "",
                        "avg_conf": avg_conf,
                        "raw_text": raw_text,
                        "char_confs": char_confs_list,
                        "rejected": True,
                        "reject_reason": "low_confidence",
                    }
            else:
                avg_conf = 0.0
                char_confs_list = []

            display_text = raw_text.replace("_", "")
            cleaned_text = self._clean_text(display_text)

            if not cleaned_text or len(cleaned_text) < self._min_plate_len:
                return {
                    "text": "",
                    "avg_conf": avg_conf,
                    "raw_text": raw_text,
                    "char_confs": char_confs_list,
                    "rejected": True,
                    "reject_reason": "too_short",
                }

            if self._ocr_mode == "numeric" and not all(ch.isdigit() for ch in cleaned_text):
                return {
                    "text": "",
                    "avg_conf": avg_conf,
                    "raw_text": raw_text,
                    "char_confs": char_confs_list,
                    "rejected": True,
                    "reject_reason": "mode_mismatch",
                }
            elif self._ocr_mode == "alphabetic" and not all(ch.isalpha() for ch in cleaned_text):
                return {
                    "text": "",
                    "avg_conf": avg_conf,
                    "raw_text": raw_text,
                    "char_confs": char_confs_list,
                    "rejected": True,
                    "reject_reason": "mode_mismatch",
                }

            return {
                "text": cleaned_text,
                "avg_conf": avg_conf,
                "raw_text": raw_text,
                "char_confs": char_confs_list,
                "rejected": False,
                "reject_reason": None,
            }
        except Exception as exc:
            self.logger.warning("OCR interpretation failed: %s", exc)
            return self._empty_ocr_result("ocr_exception")

    def _get_frame_detections(self, data: Any, frame_key: str) -> List[Dict[str, Any]]:
        """Extract detections for a specific frame from data."""
        if isinstance(data, dict):
            return data.get(frame_key, [])
        elif isinstance(data, list):
            return data
        else:
            return []

    def _update_detections_with_ocr(
        self, detections: List[Dict[str, Any]], ocr_analysis: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Update detections with OCR results using track_id or bounding box for matching."""
        # print("---------UPDATE DETECTIONS WITH OCR",ocr_analysis)
        ocr_dict = {}
        ocr_confidence_by_track: Dict[Any, float] = {}
        ocr_confidence_by_bbox: Dict[Any, float] = {}
        for rec in ocr_analysis:
            if rec.get("plate_text"):
                # Primary key: track_id
                track_id = rec.get("track_id")
                ocr_conf = rec.get("ocr_confidence")
                if track_id is not None:
                    ocr_dict[track_id] = rec["plate_text"]
                    if ocr_conf is not None:
                        ocr_confidence_by_track[track_id] = ocr_conf
                # Fallback key: bounding box as tuple
                else:
                    bbox_key = tuple(sorted(rec["bbox"].items())) if rec.get("bbox") else None
                    if bbox_key:
                        ocr_dict[bbox_key] = rec["plate_text"]
                        if ocr_conf is not None:
                            ocr_confidence_by_bbox[bbox_key] = ocr_conf
                # self.logger.info(f"OCR record: track_id={track_id}, plate_text={rec.get('plate_text')}, bbox={rec.get('bbox')}")

        # print("---------UPDATE DETECTIONS WITH OCR -II",ocr_dict)
        for det in detections:
            track_id = det.get("track_id")
            bbox_key = (
                tuple(sorted(det.get("bounding_box", det.get("bbox", {})).items()))
                if det.get("bounding_box") or det.get("bbox")
                else None
            )
            plate_text = None
            ocr_confidence = None
            if track_id is not None and track_id in ocr_dict:
                plate_text = ocr_dict[track_id]
                ocr_confidence = ocr_confidence_by_track.get(track_id)
            elif bbox_key and bbox_key in ocr_dict:
                plate_text = ocr_dict[bbox_key]
                ocr_confidence = ocr_confidence_by_bbox.get(bbox_key)
            det["plate_text"] = plate_text
            if ocr_confidence is not None:
                det["ocr_confidence"] = ocr_confidence
            # self.logger.info(f"Detection track_id={track_id}, bbox={det.get('bounding_box')}: Assigned plate_text={plate_text}")
        return detections

    def _count_categories(self, detections: List[Dict], _config: LicensePlateMonitorConfig) -> Dict[str, Any]:
        """Count unique licence-plate texts per frame and attach detections."""
        _ = (_config,)
        unique_texts: set = set()
        valid_detections: List[Dict[str, Any]] = []

        # Group detections by track_id for per-track dominance
        tracks: Dict[Any, List[Dict[str, Any]]] = {}
        for det in detections:
            if not all(k in det for k in ["category", "confidence", "bounding_box"]):
                continue
            tid = det.get("track_id")
            if tid is None:
                # If no track id, treat as its own pseudo-track keyed by bbox
                tid = det.get("bounding_box") or det.get("bbox")
            tracks.setdefault(tid, []).append(det)

        for tid, dets in tracks.items():
            # Re-localize the labeled box every frame: prefer the freshest REAL
            # detection for this track (current model output), falling back to a
            # smoother-carried copy only when nothing real arrived this frame
            # (the smoother holds for at most hold_frames). The previous
            # `rep = dets[0]` could pin the box to a stale carried copy while
            # the plate moved — the held label then drew at the old position
            # for the whole hold window and every cache-replay thereafter.
            real_dets = [d for d in dets if not d.get("_smoothed")]
            rep = real_dets[-1] if real_dets else dets[-1]
            cat = rep.get("category", "")
            bbox = rep.get("bounding_box")
            conf = rep.get("confidence")
            frame_id = rep.get("frame_id")
            rtp_number = rep.get("rtp_number")

            # Compute dominant text for this track from last 50% of history,
            # merging OCR-confusable character variants (0/O, 5/S, ...) so one
            # physical plate yields one dominant text.
            dominant_text = None
            history = self.helper.get(tid, [])
            if history:
                half = max(1, len(history) // 2)
                window = history[-half:]
                dominant_text = self._dominant_from_window(window)
            elif rep.get("plate_text"):
                candidate = self._clean_text(rep.get("plate_text", ""))
                if self._min_plate_len <= len(candidate) <= self._max_plate_len:
                    dominant_text = candidate

            # Fallback to already computed per-track mapping
            if not dominant_text:
                dominant_text = self.unique_plate_track.get(tid)

            # Enforce length range and uniqueness per frame. Uniqueness is by
            # normalized text so OCR variants of one plate count once.
            if dominant_text and self._min_plate_len <= len(dominant_text) <= self._max_plate_len:
                unique_texts.add(self._normalize_plate(dominant_text))
                valid_detections.append(
                    {
                        "bounding_box": bbox,
                        "category": cat,
                        "confidence": conf,
                        "track_id": rep.get("track_id"),
                        "frame_id": frame_id,
                        # rtp_number was missing here entirely (only frame_id was
                        # propagated) -- _collect_confirmed_plates/_build_plate_create_anchor
                        # read plate_meta["rtp_number"], so without this an anchor built
                        # from a `_smoothed` (stale) rep always fell back to re-deriving
                        # BOTH frame_id and rtp_number from the CURRENT stream_info,
                        # silently discarding the correct frame_id captured above too.
                        "rtp_number": rtp_number,
                        "masks": rep.get("masks", []),
                        "plate_text": dominant_text,
                        "ocr_confidence": rep.get("ocr_confidence"),
                    }
                )

        counts = {"License_Plate": len(unique_texts)} if unique_texts else {}

        return {
            "total_count": len(unique_texts),
            "per_category_count": counts,
            "detections": valid_detections,
        }

    def _generate_tracking_stats(
        self,
        counting_summary: Dict,
        alerts: Any,
        config: LicensePlateMonitorConfig,
        _frame_number: int | None = None,
        stream_info: Dict[str, Any] | None = None,
    ) -> List[Dict]:
        """Generate structured tracking stats with frame-based keys."""
        _ = (_frame_number,)
        tracking_stats = []
        total_detections = counting_summary.get("total_count", 0)
        per_category_count = counting_summary.get("per_category_count", {})
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        self._debug_stream_timing("start_timestamp", start_timestamp)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)
        camera_info = self.get_camera_info_from_stream(stream_info)

        total_counts_dict = counting_summary.get("total_counts") or self.get_total_counts()
        if not isinstance(total_counts_dict, dict):
            total_counts_dict = self.get_total_counts()
        total_counts_list = [
            {"category": str(cat), "count": int(count)} for cat, count in total_counts_dict.items() if int(count) > 0
        ]
        current_counts: List[Dict[str, Any]] = []
        for cat, count in per_category_count.items():
            if count > 0 or total_detections > 0:
                current_counts.append({"category": str(cat), "count": int(count)})
        new_counts_dict = self.get_new_counts_this_frame()
        current_new_counts = [{"category": str(cat), "count": int(count)} for cat, count in new_counts_dict.items()]

        human_text_lines = []
        # print("counting_summary", counting_summary)
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        sum_of_current_frame_detections = sum(per_category_count.values())

        if total_detections > 0:
            # for cat, count in per_category_count.items():
            human_text_lines.append(f"\t- License Plates Detected: {sum_of_current_frame_detections}")
            # human_text_lines.append(f"\t- {detection_text}")
            # Show dominant per-track license plates for current frame
            seen = set()
            display_texts = []
            for det in counting_summary.get("detections", []):
                t = det.get("track_id")
                dom = det.get("plate_text")
                if not dom or not (self._min_plate_len <= len(dom) <= self._max_plate_len):
                    continue
                if t in seen:
                    continue
                seen.add(t)
                display_texts.append(dom)
        else:
            human_text_lines.append("\t- License Plates Detected: 0")

        human_text_lines.append("")
        detections = []
        for detection in counting_summary.get("detections", []):
            dom = detection.get("plate_text", "")
            if not dom:
                dom = ""
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "")
            detection_obj = self.create_detection_object(
                category,
                bbox,
                segmentation=None,
                plate_text=dom,
                track_id=detection.get("track_id"),
            )
            detections.append(detection_obj)

        alert_settings = []
        # Build alert settings tolerating dict or dataclass for alert_config
        if config.alert_config:
            alert_cfg = config.alert_config
            alert_type = (
                getattr(alert_cfg, "alert_type", None)
                if not isinstance(alert_cfg, dict)
                else alert_cfg.get("alert_type")
            )
            alert_value = (
                getattr(alert_cfg, "alert_value", None)
                if not isinstance(alert_cfg, dict)
                else alert_cfg.get("alert_value")
            )
            count_thresholds = (
                getattr(alert_cfg, "count_thresholds", None)
                if not isinstance(alert_cfg, dict)
                else alert_cfg.get("count_thresholds")
            )
            if not isinstance(alert_type, list):
                alert_type = list(alert_type) if alert_type is not None else ["Default"]
            if not isinstance(alert_value, list):
                alert_value = list(alert_value) if alert_value is not None else ["JSON"]
            alert_settings.append(
                {
                    "alert_type": alert_type,
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": count_thresholds or {},
                    "ascending": True,
                    "settings": dict(zip(alert_type, alert_value, strict=False)),
                }
            )

        if alerts:
            human_text_lines.append(f"Alerts: {alerts[0].get('settings', {})}")
        else:
            human_text_lines.append("Alerts: None")

        human_text = "\n".join(human_text_lines)
        reset_settings = [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]

        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts_list,
            current_counts=current_counts,
            detections=detections,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=reset_settings,
            start_time=high_precision_start_timestamp,
            reset_time=high_precision_reset_timestamp,
        )
        tracking_stat["target_categories"] = self.target_categories
        # current_new_counts: NEW track IDs that appeared for first time in this frame/aggregation
        tracking_stat["current_new_counts"] = current_new_counts
        tracking_stats.append(tracking_stat)
        return tracking_stats

    def _check_alerts(self, summary: Dict, frame_number: Any, config: LicensePlateMonitorConfig) -> List[Dict]:
        """Check if any alert thresholds are exceeded."""

        def get_trend(data, lookback=900, threshold=0.6):
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True
            increasing = sum(1 for i in range(1, len(window)) if window[i] >= window[i - 1])
            return increasing / (len(window) - 1) >= threshold

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts = []
        total_detections = summary.get("total_count", 0)
        per_category_count = summary.get("per_category_count", {})

        if not config.alert_config:
            return alerts

        # Extract thresholds regardless of dict/dataclass
        _alert_cfg = config.alert_config
        _thresholds = (
            getattr(_alert_cfg, "count_thresholds", None)
            if not isinstance(_alert_cfg, dict)
            else _alert_cfg.get("count_thresholds")
        )
        _types = (
            getattr(_alert_cfg, "alert_type", None)
            if not isinstance(_alert_cfg, dict)
            else _alert_cfg.get("alert_type")
        )
        _values = (
            getattr(_alert_cfg, "alert_value", None)
            if not isinstance(_alert_cfg, dict)
            else _alert_cfg.get("alert_value")
        )
        _types = _types if isinstance(_types, list) else (list(_types) if _types is not None else ["Default"])
        _values = _values if isinstance(_values, list) else (list(_values) if _values is not None else ["JSON"])
        if _thresholds:
            for category, threshold in _thresholds.items():
                if category == "all" and total_detections > threshold:
                    alerts.append(
                        {
                            "alert_type": _types,
                            "alert_id": f"alert_{category}_{frame_key}",
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(self._ascending_alert_list),
                            "settings": {t: v for t, v in zip(_types, _values, strict=False)},
                        }
                    )
                elif category in per_category_count and per_category_count[category] > threshold:
                    alerts.append(
                        {
                            "alert_type": _types,
                            "alert_id": f"alert_{category}_{frame_key}",
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(self._ascending_alert_list),
                            "settings": {t: v for t, v in zip(_types, _values, strict=False)},
                        }
                    )
        return alerts

    def _generate_incidents(
        self,
        counting_summary: Dict,
        alerts: List,
        config: LicensePlateMonitorConfig,
        frame_number: int | None = None,
        stream_info: Dict[str, Any] | None = None,
    ) -> List[Dict]:
        """Generate structured incidents."""
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        incidents = []
        total_detections = counting_summary.get("total_count", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        camera_info = self.get_camera_info_from_stream(stream_info)

        self._ascending_alert_list = (
            self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list
        )

        if total_detections > 0:
            start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
            self._debug_stream_timing("start_timestamp", start_timestamp)
            if start_timestamp and self.current_incident_end_timestamp == "N/A":
                self.current_incident_end_timestamp = "Incident still active"
            elif start_timestamp and self.current_incident_end_timestamp == "Incident still active":
                if len(self._ascending_alert_list) >= 15 and sum(self._ascending_alert_list[-15:]) / 15 < 1.5:
                    self.current_incident_end_timestamp = current_timestamp
            elif (
                self.current_incident_end_timestamp != "Incident still active"
                and self.current_incident_end_timestamp != "N/A"
            ):
                self.current_incident_end_timestamp = "N/A"

            if config.alert_config and config.alert_config.count_thresholds:
                threshold = config.alert_config.count_thresholds.get("all", 15)
                intensity = min(10.0, (total_detections / threshold) * 10)
                if intensity >= 9:
                    level = "critical"
                    self._ascending_alert_list.append(3)
                elif intensity >= 7:
                    level = "significant"
                    self._ascending_alert_list.append(2)
                elif intensity >= 5:
                    level = "medium"
                    self._ascending_alert_list.append(1)
                else:
                    level = "low"
                    self._ascending_alert_list.append(0)
            else:
                if total_detections > 30:
                    level = "critical"
                    self._ascending_alert_list.append(3)
                elif total_detections > 25:
                    level = "significant"
                    self._ascending_alert_list.append(2)
                elif total_detections > 15:
                    level = "medium"
                    self._ascending_alert_list.append(1)
                else:
                    level = "low"
                    self._ascending_alert_list.append(0)

            human_text_lines = [f"INCIDENTS DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            human_text = "\n".join(human_text_lines)

            alert_settings = []
            if config.alert_config:
                _alert_cfg = config.alert_config
                _types = (
                    getattr(_alert_cfg, "alert_type", None)
                    if not isinstance(_alert_cfg, dict)
                    else _alert_cfg.get("alert_type")
                )
                _values = (
                    getattr(_alert_cfg, "alert_value", None)
                    if not isinstance(_alert_cfg, dict)
                    else _alert_cfg.get("alert_value")
                )
                _thresholds = (
                    getattr(_alert_cfg, "count_thresholds", None)
                    if not isinstance(_alert_cfg, dict)
                    else _alert_cfg.get("count_thresholds")
                )
                _types = _types if isinstance(_types, list) else (list(_types) if _types is not None else ["Default"])
                _values = _values if isinstance(_values, list) else (list(_values) if _values is not None else ["JSON"])
                alert_settings.append(
                    {
                        "alert_type": _types,
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": _thresholds or {},
                        "ascending": True,
                        "settings": {t: v for t, v in zip(_types, _values, strict=False)},
                    }
                )

            event = self.create_incident(
                incident_id=f"{self.CASE_TYPE}_{frame_key}",
                incident_type=self.CASE_TYPE,
                severity_level=level,
                human_text=human_text,
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=alert_settings,
                start_time=start_timestamp,
                end_time=self.current_incident_end_timestamp,
                level_settings={"low": 1, "medium": 3, "significant": 4, "critical": 7},
            )
            incidents.append(event)
        else:
            self._ascending_alert_list.append(0)
            # An empty scene must also be able to CLOSE an open incident. The
            # close check previously lived only inside the total>0 branch, so
            # once the road emptied the incident stayed "Incident still
            # active" forever (observed: 3 days on Thor). Apply the same
            # low-activity close rule here and emit one closing event so the
            # end_time actually reaches downstream consumers.
            if (
                self.current_incident_end_timestamp == "Incident still active"
                and len(self._ascending_alert_list) >= 15
                and sum(self._ascending_alert_list[-15:]) / 15 < 1.5
            ):
                self.current_incident_end_timestamp = current_timestamp
                start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
                closing_event = self.create_incident(
                    incident_id=f"{self.CASE_TYPE}_{frame_key}",
                    incident_type=self.CASE_TYPE,
                    severity_level="low",
                    human_text=f"INCIDENT ENDED @ {current_timestamp}",
                    camera_info=camera_info,
                    alerts=alerts,
                    alert_settings=[],
                    start_time=start_timestamp,
                    end_time=self.current_incident_end_timestamp,
                    level_settings={"low": 1, "medium": 3, "significant": 4, "critical": 7},
                )
                incidents.append(closing_event)
            else:
                incidents.append({})

        return incidents

    def _generate_summary(
        self,
        _summary: Dict,
        incidents: List,
        tracking_stats: List,
        business_analytics: List,
        _alerts: List,
    ) -> List[str]:
        """Generate a human-readable summary."""
        _ = (_alerts, _summary)
        """
        Generate a human_text string for the tracking_stat, incident, business analytics and alerts.
        """
        lines = []
        lines.append("Application Name: " + self.CASE_TYPE)
        lines.append("Application Version: " + self.CASE_VERSION)
        if len(incidents) > 0:
            lines.append("Incidents: " + f"\n\t{incidents[0].get('human_text', 'No incidents detected')}")
        if len(tracking_stats) > 0:
            lines.append(
                "Tracking Statistics: " + f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}"
            )
        if len(business_analytics) > 0:
            lines.append(
                "Business Analytics: "
                + f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}"
            )

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines.append("Summary: " + "No Summary Data")

        return ["\n".join(lines)]

    def _update_tracking_state(self, detections: List[Dict]):
        """Track unique track_ids per category.
        Computes which track IDs are NEW (appeared for first time this frame).
        """
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        if not hasattr(self, "_previous_frame_track_ids"):
            self._previous_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.target_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id
            self._per_category_total_track_ids.setdefault(cat, set()).add(canonical_id)
            self._current_frame_track_ids[cat].add(canonical_id)

        # NEW track IDs = present in current frame but NOT in previous frame
        self._new_track_ids_this_frame = {
            cat: (self._current_frame_track_ids.get(cat, set()) - self._previous_frame_track_ids.get(cat, set()))
            for cat in self.target_categories
        }

        # Snapshot current -> previous for next call
        self._previous_frame_track_ids = {cat: set(ids) for cat, ids in self._current_frame_track_ids.items()}

    def _update_plate_texts(self, detections: List[Dict]):
        """Update set of seen plate texts and track the longest plate_text per track_id."""
        for det in detections:
            raw_text = det.get("plate_text")
            track_id = det.get("track_id")
            if not raw_text or track_id is None:
                continue

            cleaned = self._clean_text(raw_text)

            # Enforce plate length range
            if not (self._min_plate_len <= len(cleaned) <= self._max_plate_len):
                continue

            # Append to per-track rolling history (keep reasonable size)
            history = self.helper.get(track_id)
            if history is None:
                history = []
                self.helper[track_id] = history
            history.append(cleaned)
            if len(history) > 200:
                del history[: len(history) - 200]

            # Update per-track frequency counter (all-time)
            self._track_text_counts[track_id][cleaned] += 1

            # Update consecutive frame counter for stability across whole video
            self._text_history[cleaned] = self._text_history.get(cleaned, 0) + 1

            # Once stable, decide dominant text from LAST 50% of history
            # (OCR-confusable variants vote together via _dominant_from_window)
            if self._text_history[cleaned] >= self._stable_frames_required:
                half = max(1, len(history) // 2)
                window = history[-half:]
                dominant = self._dominant_from_window(window)

                # Update per-track mapping to dominant
                self._tracked_plate_texts[track_id] = dominant
                self.unique_plate_track[track_id] = dominant

                # Maintain global unique mapping with dominant only. Keyed by
                # the NORMALIZED form so OCR variants of one physical plate
                # (EY09VWS / EY09VW5 / EV09VWS) count as a single unique plate
                # in total_counts instead of inflating it per variant.
                norm = self._normalize_plate(dominant)
                if norm not in self._unique_plate_texts:
                    self._unique_plate_texts[norm] = dominant

        # Let text_history counts accumulate so dominant text can emerge
        # even with inconsistent per-frame OCR. The majority voting in
        # _count_categories (last 50% of history) already provides robustness.

    def get_total_counts(self):
        """Return total unique license plate texts encountered so far."""
        return {"License_Plate": len(self._unique_plate_texts)}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Get count of NEW track IDs that appeared in this frame vs the previous one."""
        return {cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()}

    def get_current_frame_counts(self) -> Dict[str, int]:
        """Get count of ALL track IDs currently in this frame (existing + new)."""
        return {cat: len(ids) for cat, ids in getattr(self, "_current_frame_track_ids", {}).items()}

    def _get_track_ids_info(self, detections: List[Dict]) -> Dict[str, Any]:
        """Get detailed information about track IDs."""
        frame_track_ids = {det.get("track_id") for det in detections if det.get("track_id") is not None}
        total_track_ids = set()
        for s in getattr(self, "_per_category_total_track_ids", {}).values():
            total_track_ids.update(s)
        return {
            "total_count": len(total_track_ids),
            "current_frame_count": len(frame_track_ids),
            "total_unique_track_ids": len(total_track_ids),
            "current_frame_track_ids": list(frame_track_ids),
            "last_update_time": time.time(),
            "total_frames_processed": getattr(self, "_total_frame_counter", 0),
        }

    def _compute_iou(self, box1: Any, box2: Any) -> float:
        """Compute IoU between two bounding boxes."""

        def _bbox_to_list(bbox):
            if bbox is None:
                return []
            if isinstance(bbox, list):
                return bbox[:4] if len(bbox) >= 4 else []
            if isinstance(bbox, dict):
                if "xmin" in bbox:
                    return [bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]]
                if "x1" in bbox:
                    return [bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]]
                values = [v for v in bbox.values() if isinstance(v, (int, float))]
                return values[:4] if len(values) >= 4 else []
            return []

        l1 = _bbox_to_list(box1)
        l2 = _bbox_to_list(box2)
        if len(l1) < 4 or len(l2) < 4:
            return 0.0
        x1_min, y1_min, x1_max, y1_max = l1
        x2_min, y2_min, x2_max, y2_max = l2
        x1_min, x1_max = min(x1_min, x1_max), max(x1_min, x1_max)
        y1_min, y1_max = min(y1_min, y1_max), max(y1_min, y1_max)
        x2_min, x2_max = min(x2_min, x2_max), max(x2_min, x2_max)
        y2_min, y2_max = min(y2_min, y2_max), max(y2_min, y2_max)
        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)
        inter_w = max(0.0, inter_x_max - inter_x_min)
        inter_h = max(0.0, inter_y_max - inter_y_min)
        inter_area = inter_w * inter_h
        area1 = (x1_max - x1_min) * (y1_max - y1_min)
        area2 = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = area1 + area2 - inter_area
        return (inter_area / union_area) if union_area > 0 else 0.0

    def _merge_or_register_track(self, raw_id: Any, bbox: Any) -> Any:
        """Return a stable canonical ID for a raw tracker ID."""
        if raw_id is None or bbox is None:
            return raw_id
        now = time.time()
        if raw_id in self._track_aliases:
            canonical_id = self._track_aliases[raw_id]
            track_info = self._canonical_tracks.get(canonical_id)
            if track_info is not None:
                track_info["last_bbox"] = bbox
                track_info["last_update"] = now
                track_info["raw_ids"].add(raw_id)
            return canonical_id
        # Entries older than the merge window are skipped by the scan below, so they
        # are pure per-frame cost and unbounded memory -- neither map was ever pruned
        # (measured 0.12 ms at 500 accumulated tracks, 4.4 ms at 20,000). Evict them
        # before scanning. Note the behaviour this makes explicit: a raw id whose
        # canonical entry has gone stale no longer resolves through `_track_aliases`
        # into the `track_info is None` branch above -- it registers as its own
        # canonical id, which is what a track dormant for longer than the window
        # should do rather than re-adopting an ancient identity.
        if self._canonical_tracks:
            stale = [
                cid
                for cid, info in self._canonical_tracks.items()
                if now - info["last_update"] > self._track_merge_time_window
            ]
            for cid in stale:
                for rid in self._canonical_tracks.pop(cid)["raw_ids"]:
                    self._track_aliases.pop(rid, None)
        for canonical_id, info in self._canonical_tracks.items():
            if now - info["last_update"] > self._track_merge_time_window:
                continue
            iou = self._compute_iou(bbox, info["last_bbox"])
            if iou >= self._track_merge_iou_threshold:
                self._track_aliases[raw_id] = canonical_id
                info["last_bbox"] = bbox
                info["last_update"] = now
                info["raw_ids"].add(raw_id)
                return canonical_id
        canonical_id = raw_id
        self._track_aliases[raw_id] = canonical_id
        self._canonical_tracks[canonical_id] = {
            "last_bbox": bbox,
            "last_update": now,
            "raw_ids": {raw_id},
        }
        return canonical_id

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        """Format timestamp for streams (YYYY:MM:DD HH:MM:SS format)."""
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        """Format timestamp for video chunks (HH:MM:SS.ms format)."""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp to match the current timestamp format: YYYY:MM:DD HH:MM:SS.

        The input can be either:
        1. A numeric Unix timestamp (``float`` / ``int``) – it will be converted to datetime.
        2. A string in the format ``YYYY-MM-DD-HH:MM:SS.ffffff UTC``.

        The returned value will be in the format: YYYY:MM:DD HH:MM:SS (no milliseconds, no UTC suffix).

        Example
        -------
        >>> self._format_timestamp("2025-10-27-19:31:20.187574 UTC")
        '2025:10:27 19:31:20'
        """

        # Convert numeric timestamps to datetime first
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp, timezone.utc)
            return dt.strftime("%Y:%m:%d %H:%M:%S")

        # Ensure we are working with a string from here on
        if not isinstance(timestamp, str):
            return str(timestamp)

        # Remove ' UTC' suffix if present
        timestamp_clean = timestamp.replace(" UTC", "").strip()

        # Remove milliseconds if present (everything after the last dot)
        if "." in timestamp_clean:
            timestamp_clean = timestamp_clean.split(".")[0]

        # Parse the timestamp string and convert to desired format
        try:
            # Handle format: YYYY-MM-DD-HH:MM:SS
            if timestamp_clean.count("-") >= 2:
                # Replace first two dashes with colons for date part, third with space
                parts = timestamp_clean.split("-")
                if len(parts) >= 4:
                    # parts = ['2025', '10', '27', '19:31:20']
                    formatted = f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
                    return formatted
        except Exception:
            # Non-fatal: falls through to returning the cleaned string as-is.
            self.logger.debug("[LP] could not reformat timestamp %r", timestamp_clean, exc_info=True)

        # If parsing fails, return the cleaned string as-is
        return timestamp_clean

    def _get_current_timestamp_str(
        self,
        stream_info: Dict[str, Any] | None,
        precision=False,
        frame_id: str | None = None,
    ) -> str:
        """Get formatted current timestamp based on stream type."""

        if not stream_info:
            return "00:00:00.00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id) / stream_info.get("input_settings", {}).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get("start_frame", 30) / stream_info.get(
                        "input_settings", {}
                    ).get("original_fps", 30)
                stream_time_str = self._format_timestamp_for_video(start_time)
                self._debug_stream_timing("stream_time_str", stream_time_str)
                return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            if frame_id:
                start_time = int(frame_id) / stream_info.get("input_settings", {}).get("original_fps", 30)
            else:
                start_time = stream_info.get("input_settings", {}).get("start_frame", 30) / stream_info.get(
                    "input_settings", {}
                ).get("original_fps", 30)

            stream_time_str = self._format_timestamp_for_video(start_time)

            self._debug_stream_timing("stream_time_str", stream_time_str)
            return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
        else:
            stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
            if stream_time_str:
                try:
                    timestamp_str = stream_time_str.replace(" UTC", "")
                    dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                    return self._format_timestamp_for_stream(timestamp)
                except Exception:
                    return self._format_timestamp_for_stream(time.time())
            else:
                return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(self, stream_info: Dict[str, Any] | None, precision=False) -> str:
        """Get formatted start timestamp for 'TOTAL SINCE' based on stream type."""
        if not stream_info:
            return "00:00:00"

        if precision:
            if self.start_timer is None:
                candidate = stream_info.get("input_settings", {}).get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
                candidate = stream_info.get("input_settings", {}).get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            else:
                return self._format_timestamp(self.start_timer)

        if self.start_timer is None:
            # Prefer direct input_settings.stream_time if available and not NA
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                # Fallback to nested stream_info.stream_time used by current timestamp path
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(self._tracking_start_time, timezone.utc).strftime(
                            "%Y-%m-%d-%H:%M:%S.%f UTC"
                        )
                    except Exception:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)
        elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        ts = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                    except Exception:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)

        else:
            if self.start_timer is not None and self.start_timer != "NA":
                return self._format_timestamp(self.start_timer)

            if self._tracking_start_time is None:
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                    except Exception:
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()

            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _get_tracking_start_time(self) -> str:
        """Get the tracking start time, formatted as a string."""
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        """Set the tracking start time to the current time."""
        self._tracking_start_time = time.time()

    def _attach_masks_to_detections(
        self,
        processed_detections: List[Dict[str, Any]],
        raw_detections: List[Dict[str, Any]],
        iou_threshold: float = 0.5,
    ) -> List[Dict[str, Any]]:
        """Attach segmentation masks from raw detections to processed detections."""
        if not processed_detections or not raw_detections:
            for det in processed_detections:
                det.setdefault("masks", [])
            return processed_detections

        used_raw_indices = set()
        for det in processed_detections:
            best_iou = 0.0
            best_idx = None
            for idx, raw_det in enumerate(raw_detections):
                if idx in used_raw_indices:
                    continue
                iou = self._compute_iou(det.get("bounding_box"), raw_det.get("bounding_box"))
                if iou > best_iou:
                    best_iou = iou
                    best_idx = idx
            if best_idx is not None and best_iou >= iou_threshold:
                raw_det = raw_detections[best_idx]
                masks = raw_det.get("masks", raw_det.get("mask"))
                if masks is not None:
                    det["masks"] = masks
                used_raw_indices.add(best_idx)
            else:
                det.setdefault("masks", ["EMPTY"])
        return processed_detections
