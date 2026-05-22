from __future__ import annotations

import numbers
import copy
import logging
import threading
import time
from datetime import datetime, timezone
from collections import Counter
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

if TYPE_CHECKING:
    from .hazard_zone_entry import PostProcessingConfigClient

logger = logging.getLogger(__name__)

_GEOMETRY_RETRY_INTERVAL = (
    30  # Seconds between background retry attempts when API fails
)

from ..core.base import (  # noqa: E402
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig, ZoneConfig  # noqa: E402
from ..utils import (  # noqa: E402
    filter_by_confidence,
    get_bbox_bottom25_center,
    match_results_structure,
)
from ..utils.tailgating_utils import (  # noqa: E402
    AccessEventManager,
    CrossingRecord,
    DoorRuntime,
    analyze_passage,
    compute_entry_normal,
    detect_crossing,
    signed_distance,
)

def _post_processing_config_client_cls() -> Any:
    """Late import: ``hazard_zone_entry`` is heavy; only load when API zones are used."""
    from .hazard_zone_entry import PostProcessingConfigClient

    return PostProcessingConfigClient


def lift_ai_camera_zones_into_post_processing(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Fold AI-style payloads into ``postProcessing`` (same contract as overcrowding).

    Matrice UI / exports may place ``zone_config`` under a top-level camera id key;
    this merges those into ``postProcessing`` without overwriting existing keys.
    """
    if not isinstance(doc, dict):
        return doc

    reserved = {
        "_id",
        "_idCamera",
        "_idApplication",
        "_idAppDeployment",
        "postProcessing",
        "postprocessing",
        "createdAt",
        "updatedAt",
        "created_at",
        "updated_at",
    }
    lifted: Dict[str, Any] = {}
    for k, v in doc.items():
        if k in reserved or not isinstance(v, dict):
            continue
        zc = v.get("zone_config")
        if not isinstance(zc, dict):
            continue
        if zc.get("zones") or zc.get("lines") is not None:
            lifted[k] = v
    if not lifted:
        return doc

    out = copy.deepcopy(doc)
    post = dict(out.get("postProcessing") or {})
    for k, v in lifted.items():
        if k not in post:
            post[k] = v
    out["postProcessing"] = post
    return out


def _normalize_pixel_points_to_fraction(
    width: int,
    height: int,
    points: Any,
) -> List[List[float]]:
    """Convert integer pixel [[x,y],...] to normalized [0,1] fractions (tailgating geometry)."""
    if width <= 0 or height <= 0 or not isinstance(points, list):
        return []
    out: List[List[float]] = []
    for pt in points:
        if not isinstance(pt, (list, tuple)) or len(pt) < 2:
            continue
        try:
            out.append([float(pt[0]) / width, float(pt[1]) / height])
        except (TypeError, ValueError, ZeroDivisionError):
            continue
    return out


def _tailgating_zone_config_from_ui_pixels(
    zone_config_raw: Dict[str, Any],
    width: int,
    height: int,
) -> Optional[ZoneConfig]:
    """Build ``ZoneConfig`` for one door from denormalized (pixel) ``zone_config``."""
    if not isinstance(zone_config_raw, dict) or width <= 0 or height <= 0:
        return None

    lines = zone_config_raw.get("lines") or {}
    zones = zone_config_raw.get("zones") or {}
    if not isinstance(lines, dict):
        lines = {}
    if not isinstance(zones, dict):
        zones = {}

    access_src: Any = None
    if isinstance(lines.get("access_line"), list):
        access_src = lines.get("access_line")
    elif isinstance(zones.get("access_line"), list):
        access_src = zones.get("access_line")

    if not isinstance(access_src, list) or len(access_src) < 2:
        return None

    if len(access_src) == 2:
        access_pair = [access_src[0], access_src[1]]
    else:
        access_pair = [access_src[0], access_src[-1]]

    secured_src = zones.get("secured_zone")
    if not isinstance(secured_src, list) or len(secured_src) < 3:
        return None

    access_line = _normalize_pixel_points_to_fraction(width, height, access_pair)
    secured_zone = _normalize_pixel_points_to_fraction(width, height, secured_src)

    if len(access_line) != 2 or len(secured_zone) < 3:
        return None

    merged: Dict[str, List[List[float]]] = {
        "access_line": access_line,
        "secured_zone": secured_zone,
    }

    buf = zones.get("access_buffer_zone")
    if isinstance(buf, list) and len(buf) >= 3:
        buf_n = _normalize_pixel_points_to_fraction(width, height, buf)
        if len(buf_n) >= 3:
            merged["access_buffer_zone"] = buf_n

    try:
        zc = ZoneConfig(zones=merged)
        # Reuse tailgating geometry rules (access_line length 2, secured polygon).
        TailgatingConfig.validate_door_geometry("api", zc)
    except ValueError:
        return None

    return zc


def _door_id_for_api_zone_merge(
    config: "TailgatingConfig",
    stream_info: Optional[Dict[str, Any]],
) -> str:
    """Pick which door id UI/API geometry should update."""
    explicit = None
    if stream_info and isinstance(stream_info, dict):
        raw = stream_info.get("tailgating_door_id")
        if raw is not None and str(raw).strip():
            explicit = str(raw).strip()
    if explicit:
        return explicit
    if isinstance(config.zones, dict) and len(config.zones) == 1:
        return next(iter(config.zones.keys()))
    return "main_door"


def _normalize_track_id_for_label(track_id: Any) -> Any:
    """Normalize tracker id for set membership (``int`` for numpy/Python integers)."""
    if track_id is None:
        return None
    if isinstance(track_id, bool):
        return track_id
    if isinstance(track_id, numbers.Integral):
        return int(track_id)
    return track_id


def _suspect_track_ids_from_analyses(analyses: List[Tuple[str, Any]]) -> set[Any]:
    """Union of ``suspected_tailgaters`` track ids across all doors for this frame."""
    ids: set[Any] = set()
    for _door_id, analysis in analyses:
        suspects = getattr(analysis, "suspected_tailgaters", None) or []
        for tid in suspects:
            n = _normalize_track_id_for_label(tid)
            if n is not None:
                ids.add(n)
    return ids


# ============================================================
# CONFIG
# ============================================================


class TailgatingConfig(BaseConfig):
    """Tailgating post-processing configuration.

    **Zones** are **required**: supply ``zones`` at the top level and/or under
    ``extra_params["zones"]`` (same shape). Top-level ``zones`` overrides
    ``extra_params`` on duplicate door ids.

    **Matrice UI / API geometry**: When ``stream_info`` is present and
    ``PostProcessingConfigClient`` can reach the deployment post-processing
    config (env credentials or ``stream_info["config_client"]`` or
    ``TailgatingDetectionUseCase.set_config_client``), door geometry for one
    door is merged on the first frame. Expected keys in the camera
    ``zone_config`` (after denormalization) are ``lines["access_line"]`` or
    ``zones["access_line"]`` (two points), ``zones["secured_zone"]`` (polygon),
    and optionally ``zones["access_buffer_zone"]``. Use
    ``stream_info["tailgating_door_id"]`` to choose which door id to update when
    several doors exist; if exactly one door is configured, that id is used.
    For local file / bench runs without deployment context, set
    ``stream_info["skip_tailgating_api_zones"]`` to true to skip Matrice API
    resolution entirely (avoids opening a session when credentials exist).

    **Output labeling**: In each frame, ``tracking_stats.detections`` may use
    ``category: "tailgating_person"`` for any detection whose ``track_id`` is
    listed in that frame’s tailgating analysis ``suspected_tailgaters``; others
    remain ``"person"``. Counts in ``total_counts`` / ``current_counts`` match
    those categories.

    **Timing and geometry tuning** in ``extra_params`` (``access_window_sec``,
    ``silence_timeout_sec``, ``cooldown_sec``, ``allowed_persons_per_event``,
    ``max_follow_time_delta_sec``, ``min_motion_magnitude``,
    ``line_intersection_tolerance``, ``enable_direction_validation``,
    ``cross_memory_frames``) are merged onto this config and removed from
    ``extra_params`` so they take effect in production payloads that nest them.
    """

    EXTRA_PARAM_KEYS = frozenset(
        {
            "access_window_sec",
            "silence_timeout_sec",
            "cooldown_sec",
            "allowed_persons_per_event",
            "max_follow_time_delta_sec",
            "zones",
            "min_motion_magnitude",
            "line_intersection_tolerance",
            "enable_direction_validation",
            "cross_memory_frames",
        }
    )

    @staticmethod
    def normalize_zones_mapping(raw: Any) -> Dict[str, ZoneConfig]:
        """Coerce door_id -> ZoneConfig from ZoneConfig instances or nested dicts."""
        if not raw or not isinstance(raw, dict):
            return {}
        out: Dict[str, ZoneConfig] = {}
        for door_id, value in raw.items():
            did = str(door_id)
            if isinstance(value, ZoneConfig):
                out[did] = value
            elif isinstance(value, dict):
                if "zones" in value and isinstance(value["zones"], dict):
                    out[did] = ZoneConfig(
                        zones=value["zones"],
                        zone_confidence_thresholds=value.get("zone_confidence_thresholds") or {},
                        zone_categories=value.get("zone_categories") or {},
                    )
                else:
                    out[did] = ZoneConfig(zones=value)
            else:
                raise ValueError(
                    f"zones['{did}'] must be a ZoneConfig or a dict (flat zone map or {{'zones': {{...}}}})"
                )
        return out

    @staticmethod
    def merge_zones_sources(
        top_level: Optional[Dict[str, Any]],
        from_extra: Any,
    ) -> Dict[str, ZoneConfig]:
        """Merge zone maps; top-level ``zones`` wins on duplicate door ids."""
        from_ep = TailgatingConfig.normalize_zones_mapping(from_extra)
        from_top = TailgatingConfig.normalize_zones_mapping(top_level)
        return {**from_ep, **from_top}

    @staticmethod
    def validate_zone_point(label: str, pt: Any, door_id: str) -> None:
        if not isinstance(pt, (list, tuple)) or len(pt) != 2:
            raise ValueError(f"{door_id} {label} point must be a sequence of two numbers")
        if not all(isinstance(c, numbers.Real) for c in pt):
            raise ValueError(f"{door_id} {label} coordinates must be numbers")

    @staticmethod
    def validate_door_geometry(door_id: str, zone_cfg: ZoneConfig) -> None:
        z = zone_cfg.zones
        line = z.get("access_line")
        if not isinstance(line, (list, tuple)) or len(line) != 2:
            raise ValueError(f"{door_id} access_line must be exactly two points [p1, p2]")
        TailgatingConfig.validate_zone_point("access_line", line[0], door_id)
        TailgatingConfig.validate_zone_point("access_line", line[1], door_id)

        poly = z.get("secured_zone")
        if not isinstance(poly, (list, tuple)) or len(poly) < 3:
            raise ValueError(f"{door_id} secured_zone must be a polygon with at least 3 points")
        for i, pt in enumerate(poly):
            if not isinstance(pt, (list, tuple)) or len(pt) != 2:
                raise ValueError(f"{door_id} secured_zone point {i} must be [x, y]")
            if not all(isinstance(c, numbers.Real) for c in pt):
                raise ValueError(f"{door_id} secured_zone point {i} must be numeric")

    def __init__(
        self,
        usecase: str = "tailgating_detection",  # Registry / pipeline id; must be "tailgating_detection".
        category: str = "security",  # Post-processor category (e.g. security) for registration and routing.
        confidence_threshold: float = 0.5,  # Min detection confidence; frames are filtered before crossing logic (see test: 0.25).
        target_categories: Optional[
            List[str]
        ] = None,  # Intended object classes (e.g. ["person"]); not filtered in _process_frame today.
        zones: Optional[
            Dict[str, ZoneConfig]
        ] = None,  # door_id -> ZoneConfig; may also be set via extra_params["zones"] (merged).
        access_window_sec: float = 5.0,  # Seconds after the first crossing in an access event; closes analysis window when elapsed (hard cap).
        silence_timeout_sec: float = 2.0,  # Seconds with no new crossings after the last one; closes the event when elapsed.
        cooldown_sec: float = 4.0,  # Seconds after closing an event before cooldown state updates (see AccessEventManager / door state).
        allowed_persons_per_event: int = 1,  # Authorized headcount per passage window; extra distinct crossings in the window → suspected tailgaters.
        max_follow_time_delta_sec: float = 3.0,  # Max seconds between consecutive crossings to treat a follower as tailgating vs. a new authorized entry (analyze_passage).
        min_motion_magnitude: float = 0.002,  # Min foot displacement (normalized coords) to consider motion for crossing detection.
        line_intersection_tolerance: float = 0.02,  # Max abs signed distance to line to count as "on line" when not using strict zone transition.
        enable_direction_validation: bool = False,  # If True, require enter/exit of secured_zone (no near_line-only) and motion vs entry_normal alignment.
        cross_memory_frames: int = 0,  # Drop stale per-track foot/latch state after this many frames without the track (0 = disable).
        alert_config: Optional[
            AlertConfig
        ] = None,  # Alert channels (e.g. email list, incident categories like TAILGATING-ALERT); validated when present.
        **kwargs,  # Forwarded to BaseConfig: e.g. enable_tracking, enable_analytics, batch_size, max_objects, extra_params (prod tuning blob).
    ):
        super().__init__(usecase=usecase, category=category, **kwargs)

        self.confidence_threshold = confidence_threshold
        self.target_categories = target_categories or ["person"]

        self.access_window_sec = access_window_sec
        self.silence_timeout_sec = silence_timeout_sec
        self.cooldown_sec = cooldown_sec

        self.allowed_persons_per_event = allowed_persons_per_event
        self.max_follow_time_delta_sec = max_follow_time_delta_sec

        self.min_motion_magnitude = min_motion_magnitude
        self.line_intersection_tolerance = line_intersection_tolerance
        self.enable_direction_validation = enable_direction_validation
        self.cross_memory_frames = cross_memory_frames

        self.alert_config = alert_config

        ep = dict(self.extra_params or {})
        zones_extra = ep.pop("zones", None)
        self.zones = TailgatingConfig.merge_zones_sources(zones, zones_extra)

        def _pop_float(key: str, attr: str) -> None:
            if key not in ep:
                return
            setattr(self, attr, float(ep.pop(key)))

        _pop_float("access_window_sec", "access_window_sec")
        _pop_float("silence_timeout_sec", "silence_timeout_sec")
        _pop_float("cooldown_sec", "cooldown_sec")
        _pop_float("max_follow_time_delta_sec", "max_follow_time_delta_sec")

        if "allowed_persons_per_event" in ep:
            self.allowed_persons_per_event = int(ep.pop("allowed_persons_per_event"))

        if "min_motion_magnitude" in ep:
            self.min_motion_magnitude = float(ep.pop("min_motion_magnitude"))

        if "line_intersection_tolerance" in ep:
            self.line_intersection_tolerance = float(ep.pop("line_intersection_tolerance"))

        if "enable_direction_validation" in ep:
            raw_edv = ep.pop("enable_direction_validation")
            self.enable_direction_validation = bool(raw_edv)

        if "cross_memory_frames" in ep:
            self.cross_memory_frames = int(ep.pop("cross_memory_frames"))

        for k in list(ep.keys()):
            if k in TailgatingConfig.EXTRA_PARAM_KEYS:
                ep.pop(k, None)

        self.extra_params = ep

    # --------------------------------------------------------

    def validate(self):
        if not (0.0 <= self.confidence_threshold <= 1.0):
            raise ValueError("confidence_threshold must be between 0 and 1")

        if not isinstance(self.zones, dict) or not self.zones:
            raise ValueError(
                "At least one door zone is required: set top-level 'zones' and/or "
                "extra_params['zones'] (door_id -> ZoneConfig or zone dict with "
                "access_line + secured_zone)"
            )

        for door_id, zone_cfg in self.zones.items():
            if not isinstance(zone_cfg, ZoneConfig):
                raise ValueError(f"{door_id} must be a ZoneConfig")

            if "access_line" not in zone_cfg.zones:
                raise ValueError(f"{door_id} missing access_line")

            if "secured_zone" not in zone_cfg.zones:
                raise ValueError(f"{door_id} missing secured_zone")

            TailgatingConfig.validate_door_geometry(door_id, zone_cfg)

        if self.access_window_sec <= 0:
            raise ValueError("access_window_sec must be positive")

        if self.silence_timeout_sec <= 0:
            raise ValueError("silence_timeout_sec must be positive")

        if self.cooldown_sec <= 0:
            raise ValueError("cooldown_sec must be positive")

        if self.max_follow_time_delta_sec <= 0:
            raise ValueError("max_follow_time_delta_sec must be positive")

        if self.allowed_persons_per_event < 1:
            raise ValueError("allowed_persons_per_event must be at least 1")

        if self.min_motion_magnitude < 0:
            raise ValueError("min_motion_magnitude must be non-negative")

        if self.line_intersection_tolerance < 0:
            raise ValueError("line_intersection_tolerance must be non-negative")

        if self.cross_memory_frames < 0:
            raise ValueError("cross_memory_frames must be non-negative")

        if self.alert_config:
            alert_errors = self.alert_config.validate()
            if alert_errors:
                raise ValueError("; ".join(alert_errors))


# ============================================================
# USE CASE
# ============================================================


class TailgatingDetectionUseCase(BaseProcessor):
    def __init__(self):
        super().__init__("tailgating_detection")

        self.event_manager = AccessEventManager()
        self.category = "security"

        # Runtime state isolated per stream
        self._runtime: Dict[str, Dict[str, Any]] = {}
        self._streams_warned_no_track: set = set()

        self._config_client: Optional[PostProcessingConfigClient] = None
        self._resolved_geometry_cache: Optional[TailgatingConfig] = None
        self._geometry_thread: Optional[threading.Thread] = None
        self._zone_resolution_attempted: bool = False

    # ------------------------------------------------------------------
    # Matrice UI / post-processing API zone geometry (same flow as overcrowding)
    # ------------------------------------------------------------------

    def set_config_client(self, client: Optional[PostProcessingConfigClient]) -> None:
        """Set client used to resolve door geometry from deployment post-processing config."""
        self._config_client = client

    def _api_zone_retry_is_worthwhile(self, stream_info: Dict[str, Any]) -> bool:
        """True when credentials exist and stream_info yields deployment + camera ids."""
        try:
            client = self._config_client or stream_info.get("config_client")
            if not client:
                PPC = _post_processing_config_client_cls()
                client = PPC(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    return False
                self._config_client = client
            ids = client.get_stream_identifiers(stream_info)
            return bool(ids.get("app_deployment_id") and ids.get("camera_id"))
        except Exception:
            return False

    def _start_geometry_resolver(
        self,
        config: TailgatingConfig,
        stream_info: Dict[str, Any],
    ) -> None:
        if self._geometry_thread is not None:
            return

        def _resolver() -> None:
            while True:
                try:
                    result = self._resolve_geometry_from_api(config, stream_info)
                    if result is not None:
                        self._resolved_geometry_cache = result
                        self.logger.info(
                            "TailgatingDetection: door geometry resolved from API "
                            "(background thread)"
                        )
                        return
                    self.logger.info(
                        "TailgatingDetection: API geometry returned None, retrying in %ds",
                        _GEOMETRY_RETRY_INTERVAL,
                    )
                except Exception as exc:
                    self.logger.warning(
                        "TailgatingDetection: background geometry resolve error: %s",
                        exc,
                    )
                time.sleep(_GEOMETRY_RETRY_INTERVAL)

        t = threading.Thread(
            target=_resolver,
            daemon=True,
            name="tailgating-zone-geometry-resolver",
        )
        self._geometry_thread = t
        t.start()
        self.logger.info(
            "TailgatingDetection: started background door geometry resolver thread"
        )

    def _resolve_geometry_from_api(
        self,
        config: TailgatingConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[TailgatingConfig]:
        """Merge ``access_line`` / ``secured_zone`` (and optional buffer) from Matrice API.

        ``PostProcessingConfigClient`` returns pixel coordinates; tailgating expects
        normalized fractions to match ``bounding_box`` / foot points, so this path
        converts pixels back using stream width/height.

        Client resolution order:
        ``set_config_client()`` → ``stream_info["config_client"]`` → env credentials.
        """
        client = self._config_client or (
            stream_info.get("config_client") if stream_info else None
        )
        if not client and stream_info:
            try:
                PPC = _post_processing_config_client_cls()
                client = PPC(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    self.logger.info(
                        "TailgatingDetection: _resolve_geometry_from_api skipped "
                        "(no config_client; set MATRICE_ACCESS_KEY_ID, "
                        "MATRICE_SECRET_ACCESS_KEY, MATRICE_ACCOUNT_NUMBER "
                        "or call set_config_client() for API zone resolution)"
                    )
                    return None
                self._config_client = client
            except Exception as e:
                self.logger.warning(
                    "TailgatingDetection: could not create config client from env: %s",
                    e,
                )
                return None

        if not stream_info:
            self.logger.info(
                "TailgatingDetection: _resolve_geometry_from_api skipped (no stream_info)"
            )
            return None
        if not client:
            self.logger.info(
                "TailgatingDetection: _resolve_geometry_from_api skipped (no config_client)"
            )
            return None

        ids = client.get_stream_identifiers(stream_info)
        app_deployment_id = ids.get("app_deployment_id") or ""
        camera_id = ids.get("camera_id") or ""
        self.logger.info(
            "TailgatingDetection: _resolve_geometry_from_api app_deployment_id=%s camera_id=%s",
            app_deployment_id or "(empty)",
            camera_id or "(empty)",
        )

        if not app_deployment_id or not camera_id:
            self.logger.info(
                "TailgatingDetection: _resolve_geometry_from_api returning None "
                "(missing app_deployment_id or camera_id)"
            )
            return None

        configs, err, _ = client.get_post_processing_configs_by_app_deployment(
            app_deployment_id
        )
        if err or not configs:
            self.logger.info(
                "TailgatingDetection: _resolve_geometry_from_api returning None "
                "(by_app_deployment err=%r, configs=%s)",
                err,
                len(configs) if configs else 0,
            )
            return None

        filtered = client.filter_configs_by_camera_id(configs, camera_id)
        if not filtered:
            self.logger.info(
                "TailgatingDetection: _resolve_geometry_from_api returning None "
                "(no postProcessing entry for camera_id=%s)",
                camera_id,
            )
            return None

        doc = lift_ai_camera_zones_into_post_processing(filtered[0])
        width, height = client.get_resolution(camera_id)
        if width is None or height is None:
            self.logger.info(
                "TailgatingDetection: _resolve_geometry_from_api returning None "
                "(get_resolution width=%r height=%r for camera_id=%s)",
                width,
                height,
                camera_id,
            )
            return None

        doc_px = client.denormalize_config(doc, width, height)
        post = doc_px.get("postProcessing") or {}
        cam_cfg = post.get(camera_id) if isinstance(post, dict) else None
        if not isinstance(cam_cfg, dict):
            return None

        zone_config_raw = cam_cfg.get("zone_config") or {}
        if not isinstance(zone_config_raw, dict):
            return None

        door_zc = _tailgating_zone_config_from_ui_pixels(
            zone_config_raw, int(width), int(height)
        )
        if door_zc is None:
            self.logger.info(
                "TailgatingDetection: _resolve_geometry_from_api returning None "
                "(zone_config missing access_line + secured_zone for camera_id=%s)",
                camera_id,
            )
            return None

        door_id = _door_id_for_api_zone_merge(config, stream_info)
        merged = copy.copy(config)
        merged.zones = dict(config.zones)
        merged.zones[door_id] = door_zc

        self.logger.info(
            "TailgatingDetection: merged API door geometry for door_id=%r", door_id
        )
        return merged

    def draw_zones_on_frame(
        self,
        frame: Any,
        zone_cfg: ZoneConfig,
        *,
        secured_color: Tuple[int, int, int] = (0, 255, 0),
        access_buffer_color: Tuple[int, int, int] = (0, 255, 255),
        access_line_color: Tuple[int, int, int] = (0, 0, 255),
        line_thickness: int = 2,
        poly_thickness: int = 2,
    ) -> None:
        """
        Draw secured zone, optional access buffer zone, and access (intersection) line on
        *frame* in place. *frame* is BGR; zone points are normalized [0, 1].

        Requires ``opencv-python`` and ``numpy``.
        """
        import cv2
        import numpy as np

        h, w = int(frame.shape[0]), int(frame.shape[1])

        def _to_pix(pt: Any) -> Tuple[int, int]:
            return int(pt[0] * w), int(pt[1] * h)

        z = zone_cfg.zones

        secured = z.get("secured_zone")
        if secured:
            pts = np.array(
                [[_to_pix(p)[0], _to_pix(p)[1]] for p in secured],
                dtype=np.int32,
            )
            cv2.polylines(frame, [pts], True, secured_color, poly_thickness)

        access_buf = z.get("access_buffer_zone")
        if access_buf:
            pts = np.array(
                [[_to_pix(p)[0], _to_pix(p)[1]] for p in access_buf],
                dtype=np.int32,
            )
            cv2.polylines(frame, [pts], True, access_buffer_color, poly_thickness)

        line = z.get("access_line")
        if line and len(line) >= 2:
            p1 = _to_pix(line[0])
            p2 = _to_pix(line[1])
            cv2.line(frame, p1, p2, access_line_color, max(1, line_thickness))

    def draw_config_zones_on_frame(self, frame: Any, config: TailgatingConfig) -> None:
        """Draw all doors in *config* onto *frame*."""
        for _door_id, zc in config.zones.items():
            self.draw_zones_on_frame(frame, zc)

    # ========================================================
    # TEMPLATE
    # ========================================================

    def create_default_config(self, **overrides):
        defaults = {
            "usecase": self.name,
            "category": "security",
            "confidence_threshold": 0.5,
        }
        defaults.update(overrides)
        return TailgatingConfig(**defaults)

    # ========================================================

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Any] = None,
    ) -> ProcessingResult:
        if not isinstance(config, TailgatingConfig):
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category="security",
                context=context,
            )

        si_dict: Optional[Dict[str, Any]] = (
            stream_info if isinstance(stream_info, dict) else None
        )

        if not self._zone_resolution_attempted:
            self._zone_resolution_attempted = True
            if si_dict and si_dict.get("skip_tailgating_api_zones"):
                self.logger.info(
                    "TailgatingDetection: skipping API door geometry "
                    "(skip_tailgating_api_zones in stream_info)"
                )
            elif si_dict:
                self.logger.info(
                    "TailgatingDetection: attempting door geometry resolution from API "
                    "(first frame, blocking)"
                )
                try:
                    resolved = self._resolve_geometry_from_api(config, si_dict)
                    if resolved is not None:
                        self._resolved_geometry_cache = resolved
                        self.logger.info(
                            "TailgatingDetection: door geometry resolved from API and cached"
                        )
                    elif self._api_zone_retry_is_worthwhile(si_dict):
                        self.logger.warning(
                            "TailgatingDetection: API returned no door geometry on first "
                            "attempt; starting background retry thread (every %ds). "
                            "Using zones from user config until resolved.",
                            _GEOMETRY_RETRY_INTERVAL,
                        )
                        self._start_geometry_resolver(config, si_dict)
                    else:
                        self.logger.info(
                            "TailgatingDetection: not starting API geometry background retry "
                            "(stream_info did not yield both app_deployment_id and camera_id; "
                            "using zones from user config)"
                        )
                except Exception as exc:
                    if self._api_zone_retry_is_worthwhile(si_dict):
                        self.logger.warning(
                            "TailgatingDetection: door geometry resolution raised on first "
                            "attempt (%s); starting background retry thread (every %ds). "
                            "Using zones from user config until resolved.",
                            exc,
                            _GEOMETRY_RETRY_INTERVAL,
                        )
                        self._start_geometry_resolver(config, si_dict)
                    else:
                        self.logger.warning(
                            "TailgatingDetection: door geometry resolution failed (%s); "
                            "not starting background retry (stream_info lacks "
                            "app_deployment_id or camera_id, or Matrice session unavailable)",
                            exc,
                        )
            else:
                self.logger.info(
                    "TailgatingDetection: no stream_info on first frame; "
                    "using zones from user config"
                )

        effective_config = (
            self._resolved_geometry_cache
            if self._resolved_geometry_cache is not None
            else config
        )

        try:
            effective_config.validate()
        except ValueError as exc:
            ctx = context or ProcessingContext()
            ctx.mark_completed()
            return self.create_error_result(
                str(exc),
                usecase=self.name,
                category="security",
                context=ctx,
            )

        if si_dict and si_dict.get("visualization_frame") is not None:
            try:
                self.draw_config_zones_on_frame(
                    si_dict["visualization_frame"],
                    effective_config,
                )
            except ImportError:
                logger.debug(
                    "tailgating visualization skipped: opencv and/or numpy not installed",
                )
            except Exception as e:
                logger.warning("tailgating zone visualization failed: %s", e)

        context = context or ProcessingContext()
        context.input_format = match_results_structure(data)

        stream_id = self._get_stream_id(si_dict)

        runtime = self._runtime.setdefault(
            stream_id,
            {
                "door_states": {},
                "last_positions": {},
                "crossing_latch": {},
                "recent_crossings": {},
                "alert_state": {},
                "entity_last_frame": {},
            },
        )

        # Single-frame processing (canonical style)

        frame_id = int(si_dict.get("frame_number", 0)) if si_dict else 0

        frame_output = self._process_frame(
            frame_id=frame_id,
            detections=data,
            config=effective_config,
            stream_info=si_dict,
            runtime=runtime,
        )

        # String frame keys only (matches BaseProcessor.create_agg_summary / protobuf).
        agg_summary = {str(frame_id): frame_output}

        context.mark_completed()

        return self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category="security",
            context=context,
        )

    # ========================================================
    # FRAME PROCESSING
    # ========================================================

    def _process_frame(
        self,
        frame_id,
        detections,
        config,
        stream_info,
        runtime,
    ):
        detections = filter_by_confidence(
            detections,
            config.confidence_threshold,
        )

        if (
            config.enable_tracking
            and isinstance(detections, list)
            and detections
            and all(d.get("track_id") is None for d in detections)
        ):
            sid = self._get_stream_id(stream_info)
            if sid not in self._streams_warned_no_track:
                self._streams_warned_no_track.add(sid)
                logger.warning(
                    "tailgating_detection: enable_tracking is True but detections lack "
                    "track_id (stream=%s); tailgating logic requires tracked objects",
                    sid,
                )

        now_ts = stream_info.get("video_ts") if stream_info and "video_ts" in stream_info else time.time()

        analyses = []

        for door_id, zone_cfg in config.zones.items():
            door = self._get_or_create_door_state(
                door_id,
                zone_cfg,
                runtime,
            )

            line_p1, line_p2 = zone_cfg.zones["access_line"]
            secured_zone = zone_cfg.zones["secured_zone"]

            frame_had_crossing = False

            for det in detections:
                track_id = det.get("track_id")
                if track_id is None:
                    continue

                key = (door_id, track_id)

                foot = get_bbox_bottom25_center(det["bounding_box"])

                prev = runtime["last_positions"].get(key)
                runtime["last_positions"][key] = foot
                runtime["entity_last_frame"][key] = frame_id

                if prev is None:
                    continue

                crossed = detect_crossing(
                    prev,
                    foot,
                    line_p1,
                    line_p2,
                    secured_zone,
                    min_motion_magnitude=config.min_motion_magnitude,
                    line_intersection_tolerance=config.line_intersection_tolerance,
                    enable_direction_validation=config.enable_direction_validation,
                    entry_normal=door.entry_normal,
                )

                if not crossed:
                    continue

                last_cross_frame = runtime["crossing_latch"].get(key)
                if last_cross_frame == frame_id:
                    continue

                runtime["crossing_latch"][key] = frame_id
                frame_had_crossing = True

                crossing = CrossingRecord(
                    track_id=track_id,
                    timestamp=now_ts,
                )

                self._handle_crossing(
                    door,
                    crossing,
                    config,
                    now_ts,
                )

            if frame_had_crossing:
                door.last_activity_ts = now_ts

            analysis = self._finalize_event_if_needed(
                door,
                config,
                now_ts,
            )

            if analysis:
                analyses.append((door_id, analysis))

        cm = config.cross_memory_frames
        if cm > 0:
            elp = runtime["entity_last_frame"]
            for key in list(runtime["last_positions"].keys()):
                last_f = elp.get(key, -1)
                if frame_id - last_f > cm:
                    runtime["last_positions"].pop(key, None)
                    runtime["crossing_latch"].pop(key, None)
                    elp.pop(key, None)

        incident_list = self._generate_incidents(
            analyses,
            frame_id,
            stream_info,
        )

        incident = incident_list[0] if incident_list else {}

        alerts = self._generate_alerts(
            analyses,
            frame_id,
            stream_info,
            config,
            runtime,
        )

        suspect_track_ids = _suspect_track_ids_from_analyses(analyses)

        # -----------------------------
        # CLEAN DETECTIONS (remove np)
        # -----------------------------
        clean_detections: List[Dict[str, Any]] = []

        for det in detections:
            bbox = det.get("bounding_box", {})
            clean_bbox = {k: float(v) for k, v in bbox.items()}
            tid_raw = det.get("track_id")
            tid_norm = _normalize_track_id_for_label(tid_raw)
            category = (
                "tailgating_person"
                if tid_norm is not None and tid_norm in suspect_track_ids
                else "person"
            )
            clean_detections.append(
                self.create_detection_object(
                    category,
                    clean_bbox,
                    track_id=tid_raw,
                )
            )

        # -----------------------------
        # COUNTS (aligned with clean_detections categories)
        # -----------------------------
        cat_counts = Counter(d.get("category", "person") for d in clean_detections)
        total_counts = [
            self.create_count_object(cat, cat_counts[cat])
            for cat in ("person", "tailgating_person")
            if cat_counts[cat] > 0
        ]
        if not total_counts:
            total_counts = [self.create_count_object("person", 0)]
        current_counts = list(total_counts)

        n_tailgaters = cat_counts.get("tailgating_person", 0)
        person_count = len(clean_detections)

        # -----------------------------
        # HUMAN TEXT
        # -----------------------------
        if n_tailgaters:
            tracking_text = (
                f"CURRENT FRAME:\n\t- People Detected: {person_count}\n"
                f"\t- tailgating_person: {n_tailgaters}"
            )
        else:
            tracking_text = f"CURRENT FRAME:\n\t- People Detected: {person_count}"

        # -----------------------------
        # CREATE TRACKING STATS
        # -----------------------------
        tracking_stats = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=clean_detections,
            human_text=tracking_text,
            camera_info=self.get_camera_info_from_stream(stream_info),
        )

        business_analytics = self.create_business_analytics(
            analysis_name="tailgating",
            statistics={
                "doors_monitored": len(config.zones),
                "tailgating_events": len(analyses),
                "tailgating_person_count": n_tailgaters,
            },
            human_text=f"Tailgating events detected: {len(analyses)}",
            camera_info=self.get_camera_info_from_stream(stream_info),
        )

        if analyses:
            total = sum(len(a.suspected_tailgaters) for _, a in analyses)
            human_text = f"Application: tailgating_detection\nTailgating detected: {total} unauthorized follower(s)"
        else:
            human_text = "Application: tailgating_detection\nNo tailgating events detected"

        return {
            "incidents": incident,
            "tracking_stats": tracking_stats,
            "business_analytics": business_analytics,
            "alerts": alerts,
            "zone_analysis": {},
            "human_text": human_text,
        }

    # ========================================================
    # INCIDENTS & ALERTS
    # ========================================================

    def _generate_incidents(self, analyses, frame_id, stream_info):
        incidents = []

        for door_id, analysis in analyses:
            if not analysis.suspected_tailgaters:
                continue

            incident_id = f"tailgating_{door_id}_{frame_id}"

            incident = self.create_incident(
                incident_id=incident_id,
                incident_type="tailgating",
                severity_level=analysis.debug.get("severity", "warning"),
                human_text=f"Tailgating detected: {analysis.suspected_tailgaters}",
                camera_info=self.get_camera_info_from_stream(stream_info),
            )

            incident["door_id"] = door_id
            incident["suspected_tailgaters"] = analysis.suspected_tailgaters
            incident["confidence"] = analysis.confidence

            incidents.append(incident)

        return incidents

    # --------------------------------------------------------

    def _generate_alerts(self, analyses, frame_id, stream_info, config, runtime):
        alerts = []

        now_ts = stream_info.get("video_ts") if stream_info and "video_ts" in stream_info else time.time()

        alert_state = runtime["alert_state"]

        for door_id, analysis in analyses:
            if not analysis.suspected_tailgaters:
                continue

            # Initialize per-door state
            state = alert_state.setdefault(door_id, {"last_alert_ts": 0.0, "alerted_track_ids": set()})

            tailgaters = analysis.suspected_tailgaters

            # --- NEW TRACKS CHECK ---
            new_tailgaters = [tid for tid in tailgaters if tid not in state["alerted_track_ids"]]

            # --- COOLDOWN CHECK ---
            cooldown_ok = (now_ts - state["last_alert_ts"]) >= config.cooldown_sec

            # --- TRIGGER CONDITION ---
            if not new_tailgaters:
                continue

            if not cooldown_ok:
                continue

            # --- CREATE ALERT ---
            alert_id = f"tailgating_{door_id}_{frame_id}"
            alert = self.create_alert_object(
                alert_type="tailgating",
                alert_id=alert_id,
                incident_category="security",
                threshold_value=float(len(tailgaters)),
                ascending=True,
                settings={
                    "door_id": door_id,
                    "tailgaters": tailgaters,
                    "new_tailgaters": new_tailgaters,
                    "confidence": analysis.confidence,
                },
            )

            alerts.append(alert)

            # --- UPDATE STATE ---
            state["last_alert_ts"] = now_ts
            state["alerted_track_ids"].update(tailgaters)

        return alerts

    # --------------------------------------------------------

    def _generate_summary(self, analyses):
        if not analyses:
            return "No tailgating events detected"

        total = sum(len(a.suspected_tailgaters) for _, a in analyses)
        return f"Tailgating detected: {total} unauthorized follower(s)"

    # ========================================================
    # EVENT MANAGEMENT
    # ========================================================

    def _handle_crossing(self, door, crossing, config, now_ts):
        if door.active_event is None:
            self.event_manager.open_event(
                door,
                config.access_window_sec,
                now_ts,
            )

        if not door.active_event:
            return

        self.event_manager.add_crossing(
            door.active_event,
            crossing,
        )

    # --------------------------------------------------------

    def _finalize_event_if_needed(self, door, config, now_ts):
        event = door.active_event
        if not event:
            return None

        if not self.event_manager.should_close(
            event,
            door,
            now_ts,
            config.silence_timeout_sec,
        ):
            return None

        closed = self.event_manager.close_event(
            door,
            config.cooldown_sec,
            now_ts,
        )

        if not closed:
            return None

        analysis = analyze_passage(
            closed.crossings,
            config.allowed_persons_per_event,
            config.max_follow_time_delta_sec,
        )

        return analysis

    # ========================================================
    # DOOR STATE
    # ========================================================

    def _get_or_create_door_state(self, door_id, zone_cfg, runtime):
        door_states = runtime["door_states"]

        if door_id in door_states:
            return door_states[door_id]

        secured = zone_cfg.zones["secured_zone"]

        center = (
            sum(p[0] for p in secured) / len(secured),
            sum(p[1] for p in secured) / len(secured),
        )

        door = DoorRuntime(door_id=door_id)

        p1, p2 = zone_cfg.zones["access_line"]

        normal = compute_entry_normal(p1, p2, center)

        dist = signed_distance(center, p1, p2)
        if dist < 0:
            normal = (-normal[0], -normal[1])

        door.entry_normal = normal

        door_states[door_id] = door
        return door

    # ========================================================
    # STREAM ISOLATION
    # ========================================================

    def _get_stream_id(self, stream_info):
        if not stream_info:
            return "default_stream"

        camera = self.get_camera_info_from_stream(stream_info)
        return camera.get("camera_id", "default_stream")

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp, timezone.utc)
            return dt.strftime("%Y:%m:%d %H:%M:%S")

        if not isinstance(timestamp, str):
            return str(timestamp)

        timestamp_clean = timestamp.replace(" UTC", "").strip()
        if "." in timestamp_clean:
            timestamp_clean = timestamp_clean.split(".")[0]

        try:
            if timestamp_clean.count("-") >= 2:
                parts = timestamp_clean.split("-")
                if len(parts) >= 4:
                    formatted = f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
                    return formatted
        except Exception as e:
            import logging

            logging.getLogger(__name__).warning(
                "Failed to normalize timestamp '%s': %s",
                timestamp_clean,
                e,
            )

        return timestamp_clean

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision=False,
        frame_id: Optional[str] = None,
    ) -> str:
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
                _ = self._format_timestamp_for_video(start_time)
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
            _ = self._format_timestamp_for_video(start_time)
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

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False) -> str:
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
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
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
