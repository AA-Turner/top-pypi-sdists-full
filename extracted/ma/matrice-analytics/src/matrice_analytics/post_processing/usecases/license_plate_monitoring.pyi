"""Auto-generated stub for module: license_plate_monitoring."""
from typing import Any, Dict, List, Set

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..ocr._deps_check import get_ort_providers
from ..ocr._ocr_ipc import normalize_run_result
from ..ocr._ocr_subprocess_client import OcrSubprocessUnavailable
from ..ocr._ocr_subprocess_client import get_shared_ocr_client
from ..ocr.preprocessing import ImagePreprocessor
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, filter_by_confidence, match_results_structure
from ..utils.alert_instance_utils import ALERT_INSTANCE
from ..utils.geometry_utils import resolve_frame_dims
from ..utils.geometry_utils import resolve_frame_dims
from ..utils.location_name_cache import LocationNameCache
from ..utils.public_ip import resolve_public_ip_once

# Constants
HAS_MATRICE_SESSION: bool
major_version: Any
minor_version: Any

# Classes
class LicensePlateMonitorConfig:
    # Configuration for License plate detection use case in License plate monitoring.
    #
    #     Available OCR models (``ocr_model_name``):
    #
    #     +-----------------------------------------+--------------+---------------------+-----------------------------------+
    #     | Model                                   | Architecture | Training Data       | Best For                          |
    #     +-----------------------------------------+--------------+---------------------+-----------------------------------+
    #     | cct-s-v1-global-model          (default)| CCT (S)      | Global plates       | General use                       |
    #     | cct-xs-v1-global-model                  | CCT (XS)     | Global plates       | Faster / smaller                  |
    #     | cct-s-relu-v1-global-model              | CCT-ReLU (S) | Global plates       | Same as S but with ReLU           |
    #     | cct-xs-relu-v1-global-model             | CCT-ReLU(XS) | Global plates       | Fastest CCT variant               |
    #     | european-plates-mobile-vit-v2-model     | MobileViT-v2 | European plates     | European plates specifically      |
    #     | global-plates-mobile-vit-v2-model       | MobileViT-v2 | Global (65+ countries)| Most comprehensive coverage      |
    #     | argentinian-plates-cnn-model            | CNN          | Argentinian plates  | Argentina only                    |
    #     | argentinian-plates-cnn-synth-model      | CNN          | Argentinian (synth) | Argentina only                    |
    #     +-----------------------------------------+--------------+---------------------+-----------------------------------+

    def validate(self: Any) -> List[str]:
        """
        Validate configuration parameters.
        """
        ...

class LicensePlateMonitorLogger:
    def __init__(self: Any) -> None: ...

    async def aclose(self: Any) -> None:
        """
        Close the shared aiohttp session (call from the loop that owns it).
        """
        ...

    async def append_view_frame(self: Any, detection_id: str, plate_text: str, timestamp: str, stream_info: Dict[str, Any], image_data: str | None = None, bbox: Any = None, ocr_confidence: float | None = None) -> bool:
        """
        Record a further sighting of a plate that already has an lpr-server detection.
        
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
        ...

    def get_server_connection_info(self: Any) -> Dict[str, Any] | None:
        """
        Fetch server connection info from RPC.
        """
        ...

    def initialize_session(self: Any, config: Any) -> None:
        """
        Initialize session and fetch server connection info if lpr_server_id is provided.
        """
        ...

    async def log_plate(self: Any, plate_text: str, timestamp: str, stream_info: Dict[str, Any], image_data: str | None = None, bbox: Any = None, ocr_confidence: float | None = None) -> str | None:
        """
        Create a new lpr-server detection for a plate not yet in the detection list.
        
                Returns:
                    The new detection document id on success, otherwise ``None``.
        
                    In ``redis`` publish mode there is no response to read an id from, so a
                    sentinel (``_PUBLISHED_MARKER``) is returned instead. Callers only use the
                    return value to decide "have I registered this plate", and the server does
                    the create-vs-append decision itself, so the real id is not needed.
        """
        ...

    def note_rate_limited(self: Any, retry_after: float = 0.0, plate_text: str = '') -> None:
        """
        Record a 429 and open a global send window in the future.
        
                Backoff doubles from ``_RATE_LIMIT_BACKOFF_MIN_S`` while rejections keep
                arriving and is capped at ``_RATE_LIMIT_BACKOFF_MAX_S``; ``note_send_ok``
                clears it. The server's ``Retry-After`` wins when it sends one.
        
                The warning is rate-limited to one line per backoff window: a single dense
                frame can reject dozens of plates, and one log line per rejection is what
                turned ordinary backpressure into a wall of tracebacks.
        """
        ...

    def note_send_failed(self: Any, reason: str = '') -> None:
        """
        Record a failed POST and open the send window once failures are consecutive.
        
                The 429 path above only opens on explicit push-back or repeated connection
                loss. A plainly broken server -- a timeout, a 500, or the 404 the missing
                ``view-frames`` route produced for weeks -- never tripped it, so every plate
                kept paying a full round trip to a service that could not answer. After
                ``_SEND_FAILURE_BREAKER_THRESHOLD`` consecutive failures this reuses the same
                backoff window, and a single success clears it.
        """
        ...

    def note_send_ok(self: Any) -> None:
        """
        A POST succeeded: forget the accumulated 429 and failure backoff.
        """
        ...

    def publish_plate_sighting(self: Any, plate_text: str, timestamp: str, stream_info: Dict[str, Any], bbox: Any = None, ocr_confidence: float | None = None) -> bool:
        """
        Publish one sighting to ``lpr-detections``. Create vs append is the server's call.
        
                ``processRedisMessage`` upserts the detection by ``(licensePlate, projectId,
                teamId)`` and calls ``AppendFrameID`` when it already exists, skipping frames
                already listed. So the client no longer has to know whether a plate is new --
                which is what the detection-id registry, the create-before-append
                serialisation and the in-flight cap all existed to arrange.
        
                No image is sent: the server extracts the frame itself from ``rtp_number``.
        """
        ...

    def rate_limit_wait_s(self: Any) -> float:
        """
        Seconds the caller should hold off before the next POST (0.0 == send now).
        """
        ...

class LicensePlateMonitorUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def close_plate_sync(self: Any) -> None:
        """
        Stop the background plate sync sender (best-effort create flush).
        """
        ...

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique license plate texts encountered so far.
        """
        ...

    async def process(self: Any, data: Any, config: Any, input_bytes: Any | None = None, context: Any | None = None, stream_info: Dict[str, Any] | None = None) -> Any: ...

    def reset_all_tracking(self: Any) -> None:
        """
        Reset both advanced tracker and plate tracking state.
        """
        ...

    def reset_plate_tracking(self: Any) -> None:
        """
        Reset plate tracking state.
        """
        ...

    def reset_tracker(self: Any) -> None:
        """
        Reset the advanced tracker instance.
        """
        ...

    def set_alert_manager(self: Any, alert_manager: Any) -> None:
        """
        Set the alert manager instance for instant alerts.
        
        Args:
            alert_manager: ALERT_INSTANCE instance configured with Redis/Kafka clients
        """
        ...

    def set_bgr_frame(self: Any, bgr_frame: Any) -> Any:
        """
        Set raw BGR frame for OCR analysis (avoids JPEG encode/decode loss).
        
                Mirrors the frame into a thread-local shared holder so the ``__RAW_BGR__``
                fast path still works when the caller sets the frame on one use-case
                instance but runs ``process()`` on another (the inference pipeline
                reuses a single holder across cached use cases). The thread-local keeps
                concurrent camera worker threads isolated.
        """
        ...

