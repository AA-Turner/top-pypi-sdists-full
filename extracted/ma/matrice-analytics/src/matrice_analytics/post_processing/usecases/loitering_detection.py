from __future__ import annotations

import os
import threading
import time
from collections import deque
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..Trackers import ConfigDrivenTracker, TrackerProfile, legacy_sort_tracker_overrides
from ..utils import (
    BBoxSmoothingTracker,
    ByteTrackWrapper,
    SORTTracker,
    apply_category_mapping,
    bbox_centroid,
    bbox_feet_point,
    bbox_iou,
    dist,
    filter_by_confidence,
    match_results_structure,
    point_in_polygon,
    smooth_point,
)
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.post_processing_config_client import (
    GEOMETRY_RETRY_INTERVAL,
    PostProcessingConfigClient,
)

_DEFAULT_CAMERA_ID = "camera"
_INCIDENT_LOG = "[INCIDENT_MANAGER]"


def _resolve_manager_camera_id(stream_info: Optional[Dict[str, Any]]) -> str:
    """Resolve the camera key used by IncidentManager state tracking."""
    if not stream_info:
        return _DEFAULT_CAMERA_ID
    inp = stream_info.get("input_settings")
    if not isinstance(inp, dict):
        inp = {}
    camera_info = stream_info.get("camera_info")
    if not isinstance(camera_info, dict):
        camera_info = {}
    camera_id = (
        stream_info.get("camera_id")
        or inp.get("camera_id")
        or camera_info.get("camera_id")
        or stream_info.get("stream_key")
    )
    return str(camera_id) if camera_id else _DEFAULT_CAMERA_ID


# =============================================================================
# Config
# =============================================================================
@dataclass
class LoiteringConfig(BaseConfig):
    confidence_threshold: float = 0.6
    target_categories: List[str] = field(default_factory=lambda: ["person"])

    # ----------------------------------------------------------------- #
    # Zones (req 1-5)
    # ----------------------------------------------------------------- #
    # Loitering is evaluated per zone. If ``zone_config`` is omitted (or empty),
    # the entire frame is treated as a single implicit ``global`` zone using the
    # global defaults below — zones are never strictly required.
    zone_config: Optional[ZoneConfig] = None

    # Per-zone parameter overrides (name -> {param: value}), e.g.
    # {"lobby": {"loiter_threshold_seconds": 15, "count": 4}}. In the UI/API/JSON
    # payload these live *inside* ``zone_config`` (sibling of ``zones``);
    # ``__post_init__`` lifts them onto this field so the shared ``ZoneConfig`` in
    # core/config.py is not modified. Any param absent for a zone falls back to the
    # global default of the same name (see ``_zone_param`` on the use case).
    zone_params: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # ----------------------------------------------------------------- #
    # Incident threshold + severity (req 6) — overcrowding-style model on the
    # number of *loitering* persons per zone.
    # ----------------------------------------------------------------- #
    # Loiterer-count threshold that raises an incident for a zone (the "capacity").
    # Global default applies to the implicit ``global`` zone; per-zone override via
    # zone_params[<zone>]["count"] (or ["loiter_person_threshold"]).
    loiter_person_threshold: int = 3

    # Severity bands expressed as occupancy percentage (loiterers / threshold * 100).
    # Incident is raised at >= high_severity_percent (100% = loiterers >= threshold).
    # [high, critical] -> "high"; > critical -> "critical".
    high_severity_percent: float = 100.0
    critical_severity_percent: float = 120.0

    # Stability / anti-flicker controls.
    persistence_frames: int = 3
    recovery_frames: int = 5
    # Hysteresis exit ratio: incident clears only once loiterers fall to
    # <= recovery_ratio * threshold for recovery_frames consecutive frames.
    recovery_ratio: float = 0.8

    loiter_threshold_seconds: float = 10.0
    velocity_threshold_px_per_sec: float = 18.0
    stationary_ratio_threshold: float = 0.70
    min_presence_seconds: float = 2.0

    behavior_window_seconds: float = 8.0
    min_behavior_window_seconds: float = 4.0

    track_timeout_seconds: float = 12.0

    max_centroid_jump_px: float = 80.0
    centroid_ema_alpha: float = 0.25

    speed_window_size: int = 15
    slow_flags_window_size: int = 15

    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: {0: "person"})

    alert_cooldown_seconds: float = 4.0
    alert_config: Optional[AlertConfig] = None

    enable_tracking: bool = True
    tracking_method: str = "sort"

    # Frames with loiter signal before building agg_summary incident (weapon uses 5;
    # default 1 here so short dwell episodes still open on incident_res).
    min_confirmation_frames: int = 1

    tracking_max_age: int = 30
    tracking_min_hits: int = 2
    tracking_iou_threshold: float = 0.25

    # Incident manager wiring (same as weapon_detection / fire_detection).
    session: Optional[Any] = None
    server_id: Optional[str] = None

    def __post_init__(self) -> None:
        """Accept ``zone_config`` as a plain dict (UI/API/JSON payload shape).

        The Matrice UI / post-processing JSON emit ``zone_config`` as a dict with
        ``zones`` (pixel polygons) and ``zone_params`` (per-zone overrides) nested
        inside it, plus an unused ``lines`` key. Lift ``zones`` into a plain
        :class:`ZoneConfig` (untouched in core/config.py) and hoist ``zone_params``
        onto this config's own field, so behavior is identical whether built in
        Python or loaded from JSON.
        """
        zc = self.zone_config
        if isinstance(zc, dict):
            if not self.zone_params:
                nested = zc.get("zone_params", {})
                if isinstance(nested, dict):
                    self.zone_params = {str(zn): dict(zp) for zn, zp in nested.items() if isinstance(zp, dict)}
            self.zone_config = ZoneConfig(
                zones=zc.get("zones", {}) or {},
                zone_confidence_thresholds=zc.get("zone_confidence_thresholds", {}) or {},
                zone_categories=zc.get("zone_categories", {}) or {},
            )

    def resolve_loiter_person_threshold(self, zone_name: str) -> int:
        """Resolve a zone's loiterer-count incident threshold.

        Lookup order: ``zone_params[<zone>]["count"]`` -> ``["loiter_person_threshold"]``
        -> global ``loiter_person_threshold``.
        """
        params = (self.zone_params or {}).get(zone_name)
        if isinstance(params, dict):
            for key in ("count", "loiter_person_threshold"):
                if key in params:
                    try:
                        val = int(params[key])
                        if val > 0:
                            return val
                    except (TypeError, ValueError):
                        pass
        return int(self.loiter_person_threshold)

    def validate(self) -> List[str]:
        errors: List[str] = super().validate()

        if self.loiter_threshold_seconds < 0:
            errors.append("loiter_threshold_seconds must be non-negative")
        if self.velocity_threshold_px_per_sec < 0:
            errors.append("velocity_threshold_px_per_sec must be non-negative")
        if not 0.0 <= self.stationary_ratio_threshold <= 1.0:
            errors.append("stationary_ratio_threshold must be between 0 and 1")
        if self.speed_window_size < 3:
            errors.append("speed_window_size must be >= 3")
        if self.slow_flags_window_size < 3:
            errors.append("slow_flags_window_size must be >= 3")

        if self.loiter_person_threshold <= 0:
            errors.append("loiter_person_threshold must be positive")
        if self.persistence_frames <= 0:
            errors.append("persistence_frames must be positive")
        if self.recovery_frames <= 0:
            errors.append("recovery_frames must be positive")
        if not (0.0 < self.recovery_ratio <= 1.0):
            errors.append("recovery_ratio must be between 0 and 1")

        # Zones are optional — an absent/empty zone_config falls back to a single
        # full-frame "global" zone at runtime. Only validate per-zone params here.
        zones = self.zone_config.zones if (self.zone_config and self.zone_config.zones) else {}
        if zones:
            for zone_name in zones:
                params = (self.zone_params or {}).get(zone_name, {})
                if isinstance(params, dict) and "count" in params:
                    try:
                        if int(params["count"]) <= 0:
                            errors.append(f"count for zone '{zone_name}' must be positive.")
                    except (TypeError, ValueError):
                        errors.append(f"count for zone '{zone_name}' must be an integer.")

        if self.zone_config:
            errors.extend(self.zone_config.validate())
        if self.alert_config:
            errors.extend(self.alert_config.validate())

        return errors


# =============================================================================
# Use Case
# =============================================================================
class LoiteringUseCase(BaseProcessor):
    GLOBAL_ZONE_NAME = "global"
    _INCIDENT_LOG = "[INCIDENT_MANAGER]"

    def __init__(self):
        super().__init__("loitering_detection")
        self.category = "general"
        self.CASE_TYPE = "loitering_detection"
        self.CASE_VERSION = "5.0"

        self.target_categories = ["person"]

        self.smoothing_tracker: Optional[BBoxSmoothingTracker] = None
        self.tracker: Optional[Any] = None

        self._total_frame_counter = 0
        self._loiter_tracks: Dict[int, Dict[str, Any]] = {}

        self._per_category_total_track_ids: Dict[str, set] = {}
        self._current_frame_track_ids: Dict[str, set] = {}
        # Track ids appearing for the first time this frame (drives current_new_counts).
        self._new_track_ids_this_frame: Dict[str, set] = {}
        self.start_timer = None
        self._tracking_start_time = None

        # Persistent single-incident lifecycle (same pattern as the other usecases):
        # one stable incident while loitering is active; a closing snapshot (with a
        # real end_time) is emitted on the frame the episode ends.
        self._loitering_incident_active: bool = False
        self._loitering_incident_id: str = "loitering_detection"
        self._loitering_last_incident: Optional[Dict[str, Any]] = None
        self.current_incident_end_timestamp: str = "N/A"
        self._consecutive_loiter_frames: int = 0
        # Per-track alerted set so each loitering track alerts exactly once (one-time alerts).
        self._alerted_loiter_tracks: set = set()
        # Per-track longest continuous ``presence_seconds`` while ``is_loitering``,
        # retained after the track leaves — backs avg/max_loiter_time_seconds
        # (same reasoning as intrusion_detection's own avg/max_intrusion_time_seconds:
        # the reading stays stable rather than collapsing to 0 the moment the last
        # loiterer leaves the frame).
        self._loiter_ever_seconds: Dict[int, float] = {}

        # ----------------------------------------------------------------- #
        # Zones — API geometry resolution (same flow as intrusion_detection)
        # ----------------------------------------------------------------- #
        self._config_client: Optional[PostProcessingConfigClient] = None
        self._resolved_geometry_cache: Optional[LoiteringConfig] = None
        self._geometry_thread: Optional[threading.Thread] = None
        self._zone_resolution_attempted: bool = False

        # Pixel polygons of the zones used on the current frame, keyed by zone name.
        # Surfaced as "zone_coords" in zone_analysis.
        self._current_zone_polys: Dict[str, Any] = {}

        # Per-zone track-id tracking (parity with overcrowding_detection).
        self._zone_current_track_ids: Dict[str, set] = {}
        self._zone_total_track_ids: Dict[str, set] = {}

        # Per-zone hysteresis/severity state for the loiterer-count incident model.
        self._zone_states: Dict[str, Dict[str, Any]] = {}

        # Per-zone param source for the current call (set each process() after zone
        # resolution + global fallback). Read via _zone_param.
        self._active_zone_params: Dict[str, Dict[str, Any]] = {}

        # Incident manager (same wiring as intrusion_detection / overcrowding_detection).
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._incident_manager_initialized: bool = False
        self._legacy_redis_publisher: Any = None

        # Matrice alert emission state. The cooldown is keyed per logical alert stream
        # (zone / track) so one stream's emission never suppresses another's, and stamped
        # with time.monotonic() so a wall-clock step backwards (NTP correction, VM restore)
        # cannot suppress alerts past the cooldown.
        self._ascending_alert_list: List[int] = []
        self._last_matrice_alert_emit_monotonic: Dict[str, float] = {}

    @staticmethod
    def _parse_track_id(tid: Any) -> Optional[int]:
        """Return int track_id, or None if missing or not coercible (same skip behavior as before, no crash)."""
        if tid is None:
            return None
        try:
            return int(tid)
        except (TypeError, ValueError):
            return None

    # =========================================================================
    # Zones — per-zone params + API geometry resolution + global fallback
    # =========================================================================
    def set_config_client(self, client: Optional[PostProcessingConfigClient]) -> None:
        """Set the client used to resolve zones from deployment/camera post-processing config."""
        self._config_client = client

    def _zone_param(self, zone_name: str, key: str, default: Any) -> Any:
        """Return a per-zone override from ``config.zone_params`` or the global default."""
        params = (self._active_zone_params or {}).get(zone_name)
        if isinstance(params, dict) and key in params:
            return params[key]
        return default

    @staticmethod
    def _resolve_stream_wh(stream_info: Optional[Dict[str, Any]]) -> Tuple[Optional[int], Optional[int]]:
        """Frame (width, height) from stream_info, or (None, None) if unavailable.

        Accepts ``stream_resolution`` as a dict ({"width","height"}) or a 2-list
        [w, h], at the top level or under ``input_settings``.
        """
        if not isinstance(stream_info, dict):
            return (None, None)
        candidates = [
            stream_info.get("stream_resolution"),
            (stream_info.get("input_settings") or {}).get("stream_resolution"),
        ]
        for src in candidates:
            if isinstance(src, dict):
                w = src.get("width")
                h = src.get("height")
                if w and h:
                    try:
                        return int(w), int(h)
                    except (TypeError, ValueError):
                        pass
            elif isinstance(src, (list, tuple)) and len(src) >= 2:
                try:
                    w, h = int(src[0]), int(src[1])
                    if w > 0 and h > 0:
                        return w, h
                except (TypeError, ValueError):
                    pass
        return (None, None)

    def _frame_dims(self, stream_info: Optional[Dict[str, Any]]) -> Tuple[int, int]:
        """Best-effort frame (width, height) from stream_info; large fallback box."""
        w, h = self._resolve_stream_wh(stream_info)
        if w and h:
            return w, h
        return 10000, 10000

    def _denormalize_detections_if_needed(
        self, detections: List[Dict[str, Any]], stream_info: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Scale normalized (0-1) detection bboxes to pixel space (in place).

        The loitering geometry (zone polygons in pixels, velocity_threshold_px_per_sec,
        max_centroid_jump_px) all assume pixel coordinates. Some pipelines emit
        normalized bboxes; detect that (every coord <= 1.0) and scale by the stream
        resolution so all downstream math operates in pixels. No-op when the boxes are
        already pixels or the resolution is unknown.
        """
        if not detections:
            return detections

        def _coords(bb: Any) -> List[float]:
            if not isinstance(bb, dict):
                return []
            keys = (
                ("xmin", "ymin", "xmax", "ymax") if "xmin" in bb else (("x1", "y1", "x2", "y2") if "x1" in bb else ())
            )
            return [bb[k] for k in keys if isinstance(bb.get(k), (int, float))]

        max_coord = 0.0
        saw_any = False
        for d in detections:
            cs = _coords(d.get("bounding_box") or d.get("bbox"))
            if cs:
                saw_any = True
                max_coord = max(max_coord, max(abs(c) for c in cs))

        # Pixels already (or nothing to scale): leave untouched.
        if not saw_any or max_coord > 1.0:
            return detections

        w, h = self._resolve_stream_wh(stream_info)
        if not w or not h:
            self.logger.warning(
                "LoiteringDetection: detections look normalized (max coord %.3f) but no "
                "stream_resolution is available; cannot denormalize -> zone/velocity logic "
                "will be wrong. Provide stream_info['stream_resolution'].",
                max_coord,
            )
            return detections

        for d in detections:
            bb = d.get("bounding_box") or d.get("bbox")
            if not isinstance(bb, dict):
                continue
            if "xmin" in bb:
                bb["xmin"] = float(bb["xmin"]) * w
                bb["xmax"] = float(bb["xmax"]) * w
                bb["ymin"] = float(bb["ymin"]) * h
                bb["ymax"] = float(bb["ymax"]) * h
            elif "x1" in bb:
                bb["x1"] = float(bb["x1"]) * w
                bb["x2"] = float(bb["x2"]) * w
                bb["y1"] = float(bb["y1"]) * h
                bb["y2"] = float(bb["y2"]) * h
        self.logger.info("LoiteringDetection: denormalized %d detection bbox(es) to %dx%d px", len(detections), w, h)
        return detections

    def _apply_global_zone_fallback(
        self, config: LoiteringConfig, stream_info: Optional[Dict[str, Any]]
    ) -> LoiteringConfig:
        """When no zones are configured, treat the whole frame as one ``global`` zone.

        Returns a config whose ``zone_config`` holds a single full-frame ``global``
        polygon so the zone pipeline (counting, per-zone params, incidents) runs
        unchanged with global defaults. No-op when zones are already configured.
        """
        if config.zone_config and getattr(config.zone_config, "zones", None):
            return config
        w, h = self._frame_dims(stream_info)
        self.logger.info(
            "LoiteringDetection: no zones configured; using full-frame '%s' zone (%dx%d)",
            self.GLOBAL_ZONE_NAME,
            w,
            h,
        )
        global_poly = [[0, 0], [w, 0], [w, h], [0, h]]
        return replace(config, zone_config=ZoneConfig(zones={self.GLOBAL_ZONE_NAME: global_poly}))

    def _start_geometry_resolver(self, config: LoiteringConfig, stream_info: Dict[str, Any]) -> None:
        """Spawn a daemon thread that resolves zone geometry from the API."""
        if self._geometry_thread is not None:
            return

        def _resolver() -> None:
            while True:
                try:
                    result = self._resolve_geometry_from_api(config, stream_info)
                    if result is not None:
                        self._resolved_geometry_cache = result
                        self.logger.info("LoiteringDetection: zone geometry resolved from API (background thread)")
                        return
                    self.logger.info(
                        "LoiteringDetection: API geometry returned None, retrying in %ds",
                        GEOMETRY_RETRY_INTERVAL,
                    )
                except Exception as exc:
                    self.logger.warning("LoiteringDetection: background geometry resolve error: %s", exc)
                time.sleep(GEOMETRY_RETRY_INTERVAL)

        t = threading.Thread(target=_resolver, daemon=True, name="loitering-zone-geometry-resolver")
        self._geometry_thread = t
        t.start()
        self.logger.info("LoiteringDetection: started background zone geometry resolver thread")

    def _resolve_geometry_from_api(
        self,
        config: LoiteringConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[LoiteringConfig]:
        """Resolve ``zone_config`` from PostProcessingConfigClient (UI zones -> pixel coords)."""
        client = self._config_client or (stream_info.get("config_client") if stream_info else None)
        if not client and stream_info:
            try:
                client = PostProcessingConfigClient(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    self.logger.info(
                        "LoiteringDetection: _resolve_geometry_from_api skipped (no config_client; set "
                        "MATRICE_ACCESS_KEY_ID, MATRICE_SECRET_ACCESS_KEY, MATRICE_ACCOUNT_NUMBER "
                        "or call set_config_client() for API zone geometry resolution)"
                    )
                    return None
                self._config_client = client
            except Exception as e:
                self.logger.warning(
                    "LoiteringDetection: _resolve_geometry_from_api could not create config client from env: %s",
                    e,
                )
                return None

        if not stream_info:
            self.logger.info("LoiteringDetection: _resolve_geometry_from_api skipped (no stream_info)")
            return None
        if not client:
            self.logger.info("LoiteringDetection: _resolve_geometry_from_api skipped (no config_client)")
            return None

        ids = client.get_stream_identifiers(stream_info)
        app_deployment_id = ids.get("app_deployment_id") or ""
        camera_id = ids.get("camera_id") or ""
        self.logger.info(
            "LoiteringDetection: _resolve_geometry_from_api app_deployment_id=%s camera_id=%s",
            app_deployment_id or "(empty)",
            camera_id or "(empty)",
        )

        if not app_deployment_id or not camera_id:
            self.logger.info("_resolve_geometry_from_api: returning None (missing app_deployment_id or camera_id)")
            return None

        configs, err, _ = client.get_post_processing_configs_by_app_deployment(app_deployment_id)
        if err or not configs:
            self.logger.info(
                "_resolve_geometry_from_api: returning None "
                "(get_post_processing_configs_by_app_deployment: err=%r, configs count=%s)",
                err,
                len(configs) if configs else 0,
            )
            return None

        filtered = client.filter_configs_by_camera_id(configs, camera_id)
        if not filtered:
            self.logger.info(
                "_resolve_geometry_from_api: returning None (filter_configs_by_camera_id: no config for camera_id=%s)",
                camera_id,
            )
            return None

        doc = filtered[0]
        width, height = client.get_resolution(camera_id)
        if width is None or height is None:
            self.logger.info(
                "_resolve_geometry_from_api: returning None (get_resolution: width=%r, height=%r for camera_id=%s)",
                width,
                height,
                camera_id,
            )
            return None

        doc_px = client.denormalize_config(doc, width, height)
        post = doc_px.get("postProcessing") or {}
        cam_cfg = post.get(camera_id) or {}
        zone_config_raw = cam_cfg.get("zone_config") or {}
        zones_px = zone_config_raw.get("zones") or {}

        if not isinstance(zones_px, dict) or not zones_px:
            self.logger.info(
                "_resolve_geometry_from_api: returning None (no zones found in zone_config for camera_id=%s)",
                camera_id,
            )
            return None

        zones_dict = {name: [list(pt) for pt in points] for name, points in zones_px.items()}
        new_zone_config = ZoneConfig(zones=zones_dict)

        # Per-zone params (loiter_threshold_seconds, count, ...) live as a sibling of
        # "zones" inside "zone_config".
        zone_params_raw = zone_config_raw.get("zone_params") or {}
        zone_params_dict: Dict[str, Dict[str, Any]] = {
            str(zn): dict(zp) for zn, zp in zone_params_raw.items() if isinstance(zp, dict)
        }

        self.logger.info(
            "LoiteringDetection: resolved %d zone(s) from API: %s (zone_params: %s)",
            len(zones_dict),
            list(zones_dict.keys()),
            list(zone_params_dict.keys()),
        )
        return replace(
            config,
            zone_config=new_zone_config,
            zone_params=zone_params_dict or config.zone_params,
        )

    def _get_legacy_redis_publisher(self) -> Any:
        if self._legacy_redis_publisher is None:
            from ...analytics.redis_publisher import AnalyticsRedisPublisher

            self._legacy_redis_publisher = AnalyticsRedisPublisher()
        return self._legacy_redis_publisher

    # =========================================================================
    # Incident Manager (weapon_detection parity)
    # =========================================================================
    def _initialize_incident_manager_once(self, config: LoiteringConfig) -> None:
        if self._incident_manager_initialized:
            return
        try:
            self.logger.info(f"{self._INCIDENT_LOG} Initializing incident manager for loitering detection...")
            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=self.logger)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            if self._incident_manager:
                self.logger.info(f"{self._INCIDENT_LOG} Incident manager ready")
            else:
                self.logger.warning(
                    f"{self._INCIDENT_LOG} Incident manager unavailable; incidents will not be published"
                )
        except Exception as e:
            self.logger.error(
                f"{self._INCIDENT_LOG} Incident manager init failed: {e}",
                exc_info=True,
            )
        finally:
            self._incident_manager_initialized = True

    def _send_incident_to_manager(
        self,
        incident: Dict,
        stream_info: Optional[Dict[str, Any]] = None,
        context: Optional[ProcessingContext] = None,
    ) -> bool:
        """Route incidents like weapon_detection, but feed ``{}`` every idle frame (fire-style).

        Weapon skips empty incidents; loitering also calls the manager with ``{}`` on
        idle frames so the 5-frame open confirm and idle close lifecycle complete
        instead of publishing only ``info`` / ``Incident ended`` closes.
        """
        published = False
        camera_id = _resolve_manager_camera_id(stream_info)

        if self._incident_manager:
            try:
                published = bool(
                    self._incident_manager.process_incident(
                        camera_id=camera_id,
                        incident_data=incident or {},
                        stream_info=stream_info,
                    )
                )
                if published:
                    self.logger.info(f"{self._INCIDENT_LOG} Incident published for camera: {camera_id}")
            except Exception as e:
                self.logger.error(
                    f"{self._INCIDENT_LOG} Error publishing incident: {e}",
                    exc_info=True,
                )
        elif incident:
            try:
                from ..utils.legacy_analytics_bridge import get_legacy_session

                stream_key = str((stream_info or {}).get("stream_key") or "default_stream")
                session = get_legacy_session(stream_key)
                published = session.maybe_publish_incident(
                    incident,
                    stream_info,
                    usecase=self.name,
                    app_name=None,
                    publisher=self._get_legacy_redis_publisher(),
                    camera_id=camera_id,
                )
                if published:
                    self.logger.info(
                        f"{self._INCIDENT_LOG} Incident published via legacy Redis bridge for camera: {camera_id}"
                    )
            except Exception as e:
                self.logger.error(
                    f"{self._INCIDENT_LOG} Legacy Redis incident publish failed: {e}",
                    exc_info=True,
                )

        if context is not None:
            context.metadata["incident_published_via_manager"] = bool(self._incident_manager)
        return published

    # =========================================================================
    # Canonical Process
    # =========================================================================
    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        processing_start = time.time()

        if not isinstance(config, LoiteringConfig):
            return self.create_error_result(
                "Invalid configuration type",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        context.input_format = match_results_structure(data)
        context.confidence_threshold = config.confidence_threshold

        errors = config.validate()
        if errors:
            context.mark_completed()
            return self.create_error_result(
                f"Configuration validation failed: {errors}",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if not self._incident_manager_initialized:
            self._initialize_incident_manager_once(config)

        # --------------------------------------------------------------- #
        # Zone geometry from API (first frame blocking; background retry on
        # failure — same flow as intrusion_detection / overcrowding_detection).
        # --------------------------------------------------------------- #
        if not self._zone_resolution_attempted:
            self._zone_resolution_attempted = True
            if stream_info:
                self.logger.info(
                    "LoiteringDetection: attempting zone geometry resolution from API (first frame, blocking)"
                )
                try:
                    resolved = self._resolve_geometry_from_api(config, stream_info)
                    if resolved is not None:
                        self._resolved_geometry_cache = resolved
                        self.logger.info("LoiteringDetection: zone geometry resolved from API and cached")
                    else:
                        self.logger.warning(
                            "LoiteringDetection: API returned no zone config on first frame; "
                            "starting background retry thread (every %ds). Using zone_config from "
                            "user config until resolved.",
                            GEOMETRY_RETRY_INTERVAL,
                        )
                        self._start_geometry_resolver(config, stream_info)
                except Exception as exc:
                    self.logger.warning(
                        "LoiteringDetection: zone geometry resolution raised on first frame (%s); "
                        "starting background retry thread (every %ds). Using zone_config from "
                        "user config until resolved.",
                        exc,
                        GEOMETRY_RETRY_INTERVAL,
                    )
                    self._start_geometry_resolver(config, stream_info)
            else:
                self.logger.info(
                    "LoiteringDetection: no stream_info on first frame; using zone_config from user config"
                )

        if self._resolved_geometry_cache is not None:
            config = self._resolved_geometry_cache
            self.logger.debug("LoiteringDetection: using API-resolved zone geometry")

        # If no zones are configured, treat the whole frame as a single "global"
        # zone so the zone pipeline runs unchanged with global defaults (req 5).
        config = self._apply_global_zone_fallback(config, stream_info)

        # Per-zone param source for _zone_param (req 4 / req 5 fallback).
        self._active_zone_params = config.zone_params or {}

        is_multi_frame = self.detect_frame_structure(data)
        if stream_info and "input_settings" in stream_info:
            frame_id = stream_info["input_settings"].get("start_frame")
        else:
            frame_id = None

        # HARD FALLBACK
        if frame_id is None or not isinstance(frame_id, (int, float)):
            frame_id = self._total_frame_counter + 1
        frame_id = int(frame_id)

        frames = data if is_multi_frame else {str(frame_id): data}

        frame_incidents = {}
        frame_tracking_stats = {}
        frame_business_analytics = {}
        frame_alerts = {}
        frame_human_text = {}
        frame_zone_analysis: Dict[str, Dict[str, Any]] = {}

        enriched_detections: List[Dict[str, Any]] = []

        for frame_key, frame_data in frames.items():
            (
                incidents,
                tracking_stats,
                business_analytics,
                new_alerts,
                active_alerts,
                summary_text,
                detections_out,
                zone_analysis,
            ) = self._process_frame(frame_data, config, str(frame_key), stream_info)

            frame_incidents[str(frame_key)] = incidents
            frame_tracking_stats[str(frame_key)] = tracking_stats
            frame_business_analytics[str(frame_key)] = business_analytics
            frame_alerts[str(frame_key)] = active_alerts
            frame_human_text[str(frame_key)] = summary_text
            frame_zone_analysis[str(frame_key)] = zone_analysis

            enriched_detections = detections_out

            # Publish this frame's incident to the incident manager for level tracking.
            # Pass context so the bridge skips duplicate incident_res publishing.
            self._send_incident_to_manager(incidents, stream_info, context=context)

        agg_summary = self.create_frame_wise_agg_summary(
            frame_incidents,
            frame_tracking_stats,
            frame_business_analytics,
            frame_alerts,
            frame_human_text,
        )

        # zone_analysis is a top-level per-frame key (parity with overcrowding /
        # intrusion), not part of create_frame_wise_agg_summary — inject it here.
        for fk, za in frame_zone_analysis.items():
            if za and fk in agg_summary:
                agg_summary[fk]["zone_analysis"] = za

        context.mark_completed()

        result = self.create_result(
            data={
                "agg_summary": agg_summary,
                "detections": enriched_detections,
            },
            usecase=self.name,
            category=self.category,
            context=context,
        )

        proc_time = time.time() - processing_start
        latency_ms = proc_time * 1000.0
        fps = (1.0 / proc_time) if proc_time > 0 else None

        perf_suffix = f"fps={fps:.1f}" if fps else ""
        self.logger.debug(
            "[PERF] F%s | latency=%.1fms %s",
            self._total_frame_counter,
            latency_ms,
            perf_suffix,
        )

        return result

    # =========================================================================

    def _init_track_state(
        self,
        bbox: Dict[str, Any],
        centroid: Tuple[float, float],
        feet: Tuple[float, float],
        config: LoiteringConfig,
    ) -> Dict[str, Any]:
        """
        Create a new per-track state dict.

        The two sliding windows:
          - speed_window: instantaneous feet speed per frame (px/sec)
          - slow_flags_window: 1.0 if stationary else 0.0 (same length as speed_window)
        """
        win = max(3, int(config.speed_window_size))
        return {
            "presence_seconds": 0.0,
            "missing_for_seconds": 0.0,
            "last_bbox": bbox,
            "last_centroid": centroid,
            "smoothed_centroid": centroid,
            "last_feet": feet,
            "smoothed_feet": feet,
            "speed_window": deque(maxlen=win),
            "slow_flags_window": deque(maxlen=max(3, int(config.slow_flags_window_size))),
            "last_inst_speed_feet": 0.0,
            "last_inst_speed_centroid": 0.0,
            "is_loitering": False,
            "last_alert_video_time": None,
            "resurrection_hits": 0,
            # Zone the track's feet point fell in this frame (None if outside all
            # zones). Set every frame in _update_loiter_states.
            "zone_name": None,
        }

    def _is_stationary(
        self,
        inst_speed_feet: float,
        inst_speed_centroid: float,
        vth: float,
    ) -> bool:
        """
        Determine if a track is stationary for this frame.
        Feet speed is treated more strictly, centroid speed is allowed more tolerance.

        ``vth`` is the (per-zone resolved) velocity threshold in px/sec.
        """
        vth = float(vth)
        return (inst_speed_feet <= vth * 0.80) and (inst_speed_centroid <= vth * 1.20)

    def _zone_for_point(self, point: Tuple[float, float], zones: Dict[str, Any]) -> Optional[str]:
        """Return the name of the first zone whose polygon contains ``point`` (else None)."""
        for zone_name, polygon in (zones or {}).items():
            if not polygon:
                continue
            poly_points = [(p[0], p[1]) for p in polygon]
            if point_in_polygon(point, poly_points):
                return zone_name
        return None

    def _process_frame(
        self,
        frame_data: Any,
        config: LoiteringConfig,
        frame_key: str,
        stream_info: Optional[Dict[str, Any]],
    ):
        """
        Canonical per-frame processing aligned with Matrice template.

        Returns:
            incidents: List[Dict]
            tracking_stats: List[Dict]
            business_analytics: List[Dict]
            alerts: List[Dict]
            summary_text: str
            enriched_detections: List[Dict]
        """

        # -------------------------------------------------
        # Frame counter (canonical)
        # -------------------------------------------------
        self._total_frame_counter = int(frame_key)

        # -------------------------------------------------
        # Normalize detections
        # -------------------------------------------------
        if isinstance(frame_data, list):
            detections = frame_data
        elif isinstance(frame_data, dict) and "predictions" in frame_data:
            detections = frame_data["predictions"]
        else:
            detections = []

        # -------------------------------------------------
        # Confidence filtering
        # -------------------------------------------------
        detections = filter_by_confidence(detections, config.confidence_threshold)

        # -------------------------------------------------
        # Category mapping (if needed)
        # -------------------------------------------------
        if config.index_to_category:
            detections = apply_category_mapping(detections, config.index_to_category)

        # -------------------------------------------------
        # Keep only target categories
        # -------------------------------------------------
        detections = [d for d in detections if d.get("category") in config.target_categories]
        self.logger.debug(
            "[FRAME %s] Person detections after filtering: %s",
            frame_key,
            len(detections),
        )

        # -------------------------------------------------
        # Coordinate space: scale normalized (0-1) bboxes to pixels so all
        # downstream geometry (zones, px/sec velocity, px jump clamps) is correct.
        # -------------------------------------------------
        detections = self._denormalize_detections_if_needed(detections, stream_info)

        # -------------------------------------------------
        # Compute dt_video + video_time_seconds
        # -------------------------------------------------
        fps = 30.0
        if stream_info:
            try:
                fps_val = stream_info.get("input_settings", {}).get("original_fps")
                if fps_val and float(fps_val) > 1e-6:
                    fps = float(fps_val)
            except Exception:
                fps = 30.0

        dt_video = 1.0 / max(1e-6, fps)
        video_time_seconds = self._total_frame_counter * dt_video

        # -------------------------------------------------
        # Tracking (if enabled)
        # -------------------------------------------------
        if config.enable_tracking:
            self._init_tracker(config, stream_info)

            if self.tracker:
                try:
                    if isinstance(self.tracker, ByteTrackWrapper):
                        detections = self.tracker.update(detections, stream_info=stream_info)
                    else:
                        detections = self.tracker.update(detections)
                except Exception:
                    self.logger.exception("[TRACKER-ERROR] tracker update failed")

            self.logger.debug(
                "[FRAME %s] Active tracked detections: %s",
                frame_key,
                len(detections),
            )

        # -------------------------------------------------
        # Zones for this frame (global fallback guarantees at least one zone)
        # -------------------------------------------------
        zones: Dict[str, Any] = {}
        if config.zone_config and getattr(config.zone_config, "zones", None):
            zones = config.zone_config.zones
        self._current_zone_polys = dict(zones)

        # -------------------------------------------------
        # Update loiter state machine (zone-aware: assigns each track a zone and
        # resolves loitering thresholds per that zone — req 1 & 4)
        # -------------------------------------------------
        # Positional 4th arg: avoids keyword drift (_video_time_seconds vs video_time_seconds) in prod.
        self._update_loiter_states(
            detections,
            config,
            dt_video,
            video_time_seconds,
            zones,
        )
        self.logger.debug(
            "[FRAME %s] Loiter state-machine active tracks: %s",
            frame_key,
            len(self._loiter_tracks),
        )

        # -------------------------------------------------
        # Enrich detections with loiter flag
        # -------------------------------------------------
        enriched_detections: List[Dict[str, Any]] = []

        for det in detections:
            tid = det.get("track_id")
            is_loitering = False

            tid_int = self._parse_track_id(tid)
            if tid_int is not None and tid_int >= 0:
                st = self._loiter_tracks.get(tid_int)
                if st:
                    is_loitering = bool(st.get("is_loitering", False))

            det_out = dict(det)
            det_out["frame_id"] = frame_key
            det_out["is_loitering"] = is_loitering

            # Optional category transformation
            if is_loitering:
                det_out["category"] = "loitering_person"

            enriched_detections.append(det_out)

        loiter_frame_count = sum(1 for d in enriched_detections if d.get("is_loitering"))
        self.logger.debug(
            "[FRAME %s] Loiter detections in frame: %s",
            frame_key,
            loiter_frame_count,
        )

        # -------------------------------------------------
        # Update unique tracking counts
        # -------------------------------------------------
        self._update_tracking_state(enriched_detections)

        # -------------------------------------------------
        # Per-zone counting (current persons + loiterers per zone)
        # -------------------------------------------------
        zone_current_ids, zone_loiter_ids = self._count_per_zone(enriched_detections, zones)
        self._update_zone_track_ids(zone_current_ids)
        self._cleanup_stale_zones(set(zones.keys()))

        # Per-zone loiterer counts drive the incident severity model (req 6).
        zone_loiter_counts = {zn: len(ids) for zn, ids in zone_loiter_ids.items()}
        zone_results = self._evaluate_loiter_incidents(zone_loiter_counts, config)

        # -------------------------------------------------
        # Counting summary (canonical)
        # -------------------------------------------------
        counting_summary = self._count_categories(enriched_detections)

        # -------------------------------------------------
        # Alerts (one-time per track — req 7)
        # -------------------------------------------------
        new_alerts = self._check_alerts(
            detections=enriched_detections,
            frame_key=frame_key,
            config=config,
            video_time_seconds=video_time_seconds,
            frame_number=int(frame_key) if frame_key.isdigit() else None,
        )
        self.logger.debug(
            "[FRAME %s] Alerts emitted this frame: %s",
            frame_key,
            len(new_alerts),
        )

        # Alerts are one-time per track (see _check_alerts). The incident persists
        # every frame, but the alert payload is only present on the onset frame.
        active_alerts = new_alerts

        # -------------------------------------------------
        # Zone analysis (req 3) — built before incidents so they can share it
        # -------------------------------------------------
        zone_analysis = self._build_zone_analysis(zone_results, zone_loiter_ids, config)

        # -------------------------------------------------
        # Incidents (persistent, loiterer-count threshold per zone — req 6 & 7)
        # -------------------------------------------------
        incidents = self._generate_incidents(
            zone_results=zone_results,
            counting_summary=counting_summary,
            alerts=active_alerts,
            config=config,
            frame_number=int(frame_key) if frame_key.isdigit() else None,
            stream_info=stream_info,
        )

        # -------------------------------------------------
        # Tracking stats
        # -------------------------------------------------
        tracking_stats = self._generate_tracking_stats(
            counting_summary,
            active_alerts,
            config,
            int(frame_key) if frame_key.isdigit() else None,
            stream_info,
            zone_analysis,
        )

        # -------------------------------------------------
        # Business analytics (minimal canonical)
        # -------------------------------------------------
        business_analytics = {}

        # -------------------------------------------------
        # Human summary
        # -------------------------------------------------
        summary_text = self._generate_summary(
            incidents=incidents,
            tracking_stats=tracking_stats,
            business_analytics=business_analytics,
        )

        return (
            incidents,
            tracking_stats,
            business_analytics,
            new_alerts,
            active_alerts,
            summary_text,
            enriched_detections,
            zone_analysis,
        )

    def _init_tracker(self, config: LoiteringConfig, stream_info: Optional[Dict[str, Any]]) -> None:
        """
        Initialize an internal tracker if enabled by config.

        Supported:
          - SORTTracker (Kalman + Hungarian)
          - ByteTrackWrapper (YOLOX BYTETracker wrapper)

        NOTE:
        - If you are already running YOLO.track(persist=True), you typically set
          enable_tracking=False so this is skipped.
        """
        if self.tracker is not None:
            return

        method = str(getattr(config, "tracking_method", "sort")).lower().strip()

        # F10b S9 (consolidation-plan.md Step 9): route the legacy SORT/ByteTrack
        # default onto the AdvancedTracker seam. MATRICE_LEGACY_SORT=1 keeps the
        # pre-migration path alive for one release (kill-switch, plan §7).
        if method in ("sort", "bytetrack") and os.environ.get("MATRICE_LEGACY_SORT") != "1":
            self.tracker = ConfigDrivenTracker().get_shared_tracker(
                profile=TrackerProfile.DEFAULT,
                **legacy_sort_tracker_overrides(config, method),
            )
            return

        if method == "sort":
            self.tracker = SORTTracker(
                iou_threshold=float(getattr(config, "tracking_iou_threshold", 0.25)),
                max_age=int(getattr(config, "tracking_max_age", 30)),
                min_hits=int(getattr(config, "tracking_min_hits", 2)),
            )
            return

        if method == "bytetrack":
            # ByteTrackWrapper needs fps mostly for track management / time scaling
            fps = 30.0
            try:
                if stream_info:
                    fps_val = stream_info.get("input_settings", {}).get("original_fps")
                    if fps_val and float(fps_val) > 1e-6:
                        fps = float(fps_val)
            except Exception:
                fps = 30.0

            self.tracker = ByteTrackWrapper(
                fps=float(fps),
                track_thresh=float(getattr(config, "bytetrack_track_thresh", 0.25)),
                match_thresh=float(getattr(config, "bytetrack_match_thresh", 0.80)),
                track_buffer=int(getattr(config, "tracking_max_age", 30)),
            )
            return

        # Unknown method => no tracking
        self.tracker = None

    def _update_loiter_states(
        self,
        detections: List[Dict[str, Any]],
        config: LoiteringConfig,
        dt_video: float,
        video_time_seconds: float,
        zones: Dict[str, Any],
    ) -> None:
        """
        Update the canonical per-track loiter state in `self._loiter_tracks`.

        This method is the "state machine heart" of the usecase.

        What it does:
        - Iterates detections for the configured target_categories ("person" by default)
        - For each detection with a valid track_id:
            * Initialize per-track state if this is a new track
            * Assign the track to a zone via its feet point (req 1)
            * Accumulate presence time using dt_video (fps-based)
            * Smooth centroid + feet point to reduce jitter (EMA)
            * Clamp large centroid jumps (prevents spikes in speed)
            * Compute instantaneous speed (px/sec) for centroid and feet
            * Push speed + stationary flags into sliding windows
            * Decide loitering using the track's ZONE-resolved thresholds (req 4):
                - presence >= loiter_threshold_seconds
                - slow_ratio >= stationary_ratio_threshold
                - avg_speed <= velocity_threshold_px_per_sec
        - Tracks missing detections and expires old tracks after track_timeout_seconds

        Notes:
        - `video_time_seconds` is currently used for alert cooldown outside this method,
          but it is kept in signature to support future time-based extensions.
        - This method does NOT modify detection objects directly. It only updates track state.
        """
        present_ids: set[int] = set()

        # Per-zone resolved loitering thresholds (req 4). Falls back to the global
        # config defaults for any zone/param not overridden in zone_params (req 5).
        def _loiter_secs(zone: Optional[str]) -> float:
            return float(self._zone_param(zone, "loiter_threshold_seconds", config.loiter_threshold_seconds))

        def _vth(zone: Optional[str]) -> float:
            return float(self._zone_param(zone, "velocity_threshold_px_per_sec", config.velocity_threshold_px_per_sec))

        def _ratio(zone: Optional[str]) -> float:
            return float(self._zone_param(zone, "stationary_ratio_threshold", config.stationary_ratio_threshold))

        def _min_presence(zone: Optional[str]) -> float:
            return float(self._zone_param(zone, "min_presence_seconds", config.min_presence_seconds))

        def _behavior_window(zone: Optional[str]) -> float:
            return float(self._zone_param(zone, "behavior_window_seconds", config.behavior_window_seconds))

        def _min_behavior_window(zone: Optional[str]) -> float:
            return float(self._zone_param(zone, "min_behavior_window_seconds", config.min_behavior_window_seconds))

        # Helper: safely extract bbox dict from a detection
        def _get_bbox(det: Dict[str, Any]) -> Optional[Dict[str, float]]:
            bbox = det.get("bounding_box") or det.get("bbox")
            return bbox if isinstance(bbox, dict) else None

        # Helper: attempt to "heal" / merge an old track into a newly seen track_id
        # if the tracker re-assigns IDs briefly (common in occlusion / ID switches).
        def _try_heal_track_id(
            new_tid: int,
            new_bbox: Dict[str, float],
            new_feet: Tuple[float, float],
        ) -> Optional[int]:
            best_old_tid: Optional[int] = None
            best_score: float = -1.0

            # Only consider tracks missing for <= track_timeout_seconds
            max_missing = float(config.track_timeout_seconds)

            # Healing thresholds (soft-configurable via getattr)
            iou_thr = float(getattr(config, "id_heal_iou_threshold", 0.30))
            feet_dist_thr = float(getattr(config, "id_heal_feet_distance_px", 60.0))

            for old_tid, st in self._loiter_tracks.items():
                if old_tid == new_tid:
                    continue

                # Only consider "recently missing" tracks
                missing_for = float(st.get("missing_for_seconds", 0.0))
                if missing_for <= 0.0 or missing_for > max_missing:
                    continue

                old_bbox = st.get("last_bbox")
                if not isinstance(old_bbox, dict):
                    continue

                # Primary match signal = bbox IoU
                iou = float(bbox_iou(old_bbox, new_bbox))
                if iou >= iou_thr:
                    score = iou
                else:
                    # Fallback match signal = feet-point proximity
                    old_feet = st.get("smoothed_feet") or st.get("last_feet")
                    if not old_feet:
                        continue

                    feet_dist = float(dist(old_feet, new_feet))
                    if feet_dist <= feet_dist_thr:
                        score = 1.0 - min(1.0, feet_dist / max(1.0, feet_dist_thr))
                    else:
                        continue

                if score > best_score:
                    best_score = score
                    best_old_tid = old_tid

            if best_old_tid is None:
                return None

            # Merge old state into new track ID
            old_state = self._loiter_tracks.get(best_old_tid)
            if not old_state:
                return None

            self._loiter_tracks[new_tid] = old_state
            self._loiter_tracks.pop(best_old_tid, None)

            if getattr(config, "enable_id_healing_debug", True):
                self.logger.info(
                    f"[LOITER-ID-HEAL] merged old_tid={best_old_tid} -> new_tid={new_tid} score={best_score:.2f}"
                )

            return best_old_tid

        # ---------------------------------------------------------------------
        # Per-detection update (present tracks)
        # ---------------------------------------------------------------------
        for det in detections:
            # Ignore unrelated categories
            if det.get("category") not in self.target_categories:
                continue

            # Must have track_id for temporal analysis
            tid = det.get("track_id")
            tid_int = self._parse_track_id(tid)
            if tid_int is None or tid_int < 0:
                continue

            bbox = _get_bbox(det)
            if not bbox:
                continue

            # Feature points derived from bbox
            centroid = bbox_centroid(bbox)
            feet = bbox_feet_point(bbox)

            # If track_id is new, attempt to heal by merging a recently-missing track
            if tid_int not in self._loiter_tracks and self._loiter_tracks:
                _try_heal_track_id(tid_int, bbox, feet)

            present_ids.add(tid_int)

            # If still new after healing attempt: initialize state and move on
            if tid_int not in self._loiter_tracks:
                new_state = self._init_track_state(bbox, centroid, feet, config)
                new_state["zone_name"] = self._zone_for_point(feet, zones)
                self._loiter_tracks[tid_int] = new_state
                continue

            st = self._loiter_tracks[tid_int]

            # Presence accumulates in video-time (dt_video)
            st["presence_seconds"] = float(st.get("presence_seconds", 0.0) + dt_video)

            # Reset missing time since we saw it this frame
            st["missing_for_seconds"] = 0.0

            # Use smoothed points as speed reference (reduces jitter spikes)
            prev_centroid = st.get("smoothed_centroid", centroid)
            prev_feet = st.get("smoothed_feet", feet)

            # Exponential moving average smoothing for centroid
            centroid_alpha = float(config.centroid_ema_alpha)
            new_centroid = smooth_point(prev_centroid, centroid, centroid_alpha)

            # Feet point gets a slightly stronger smoothing by default
            feet_alpha = min(0.40, centroid_alpha + 0.10)
            new_feet = smooth_point(prev_feet, feet, float(feet_alpha))

            # Clamp sudden centroid jumps to keep speed stable
            max_jump = float(config.max_centroid_jump_px)
            if dist(prev_centroid, new_centroid) > max_jump:
                dx = new_centroid[0] - prev_centroid[0]
                dy = new_centroid[1] - prev_centroid[1]
                norm = max(1e-6, (dx * dx + dy * dy) ** 0.5)
                scale = max_jump / norm
                new_centroid = (
                    prev_centroid[0] + dx * scale,
                    prev_centroid[1] + dy * scale,
                )

            # Instantaneous speeds (px/sec)
            dt_safe = max(1e-6, dt_video)
            inst_speed_centroid = dist(new_centroid, prev_centroid) / dt_safe
            inst_speed_feet = dist(new_feet, prev_feet) / dt_safe

            st["last_inst_speed_centroid"] = float(inst_speed_centroid)
            st["last_inst_speed_feet"] = float(inst_speed_feet)

            # Zone the track is in this frame, by its (smoothed) feet point (req 1).
            zone_name = self._zone_for_point(new_feet, zones)
            st["zone_name"] = zone_name

            # Loitering is a per-zone concept: a track outside all configured zones is
            # not evaluated. (Under the global-zone fallback every track is in "global",
            # so nobody is excluded when zones aren't configured — req 5.)
            if zone_name is None:
                st["is_loitering"] = False
                self._loiter_tracks[tid_int] = st
                continue

            # Convert speeds into a stationary flag (1.0 or 0.0) using the zone's
            # velocity threshold (req 4).
            stationary = self._is_stationary(inst_speed_feet, inst_speed_centroid, _vth(zone_name))
            slow_flag = 1.0 if stationary else 0.0

            # Update sliding windows
            st["speed_window"].append(float(inst_speed_feet))
            st["slow_flags_window"].append(float(slow_flag))

            # Update last + smoothed anchors
            st["last_bbox"] = bbox
            st["last_centroid"] = centroid
            st["smoothed_centroid"] = new_centroid
            st["last_feet"] = feet
            st["smoothed_feet"] = new_feet

            presence = float(st.get("presence_seconds", 0.0))

            # Do not allow loitering decisions too early (warm-up)
            if presence < _min_presence(zone_name):
                st["is_loitering"] = False
                self._loiter_tracks[tid_int] = st
                continue

            # A minimal window is required for stable behavior stats
            enough_window = (
                len(st["speed_window"]) >= 3
                and len(st["slow_flags_window"]) >= 3
                and min(presence, _behavior_window(zone_name)) >= _min_behavior_window(zone_name)
            )

            # Compute behavior-window statistics
            win_avg_speed = float(np.mean(list(st["speed_window"]))) if st["speed_window"] else 0.0
            win_slow_ratio = float(np.mean(list(st["slow_flags_window"]))) if st["slow_flags_window"] else 0.0

            # Final loiter decision (zone-resolved thresholds — req 4)
            is_loitering = False
            if enough_window:
                is_loitering = (
                    presence >= _loiter_secs(zone_name)
                    and win_slow_ratio >= _ratio(zone_name)
                    and win_avg_speed <= _vth(zone_name)
                )

            # Periodic debug (only after threshold time)
            if presence >= _loiter_secs(zone_name) and (self._total_frame_counter % 50 == 0):
                self.logger.info(
                    f"[LOITER-DEBUG] tid={tid_int} presence={presence:.2f}s "
                    f"avg_speed={win_avg_speed:.2f} slow_ratio={win_slow_ratio:.2f} loiter={is_loitering}"
                )

            st["is_loitering"] = bool(is_loitering)
            self._loiter_tracks[tid_int] = st

        # ---------------------------------------------------------------------
        # Missing track handling (tracks not observed this frame)
        # ---------------------------------------------------------------------
        for tid, st in list(self._loiter_tracks.items()):
            if tid in present_ids:
                continue

            # Accumulate missing time in video-time
            st["missing_for_seconds"] = float(st.get("missing_for_seconds", 0.0) + dt_video)

            # Drop tracks that have been missing too long
            if float(st["missing_for_seconds"]) > float(config.track_timeout_seconds):
                self._loiter_tracks.pop(tid, None)
            else:
                self._loiter_tracks[tid] = st

    # =========================================================================
    # Per-zone counting + incident evaluation + zone_analysis
    # =========================================================================
    def _count_per_zone(
        self,
        enriched_detections: List[Dict[str, Any]],
        zones: Dict[str, Any],
    ) -> Tuple[Dict[str, set], Dict[str, set]]:
        """Return (zone -> current track_ids, zone -> loitering track_ids) for this frame.

        Zone membership is read from the per-track state ``zone_name`` set during
        ``_update_loiter_states`` (feet-point based), so it stays consistent with the
        loitering decision.
        """
        zone_current: Dict[str, set] = {zn: set() for zn in zones}
        zone_loiter: Dict[str, set] = {zn: set() for zn in zones}

        for det in enriched_detections:
            tid_int = self._parse_track_id(det.get("track_id"))
            if tid_int is None or tid_int < 0:
                continue
            st = self._loiter_tracks.get(tid_int)
            if not st:
                continue
            zn = st.get("zone_name")
            if zn is None or zn not in zone_current:
                continue
            zone_current[zn].add(tid_int)
            if bool(det.get("is_loitering", False)):
                zone_loiter[zn].add(tid_int)

        return zone_current, zone_loiter

    def _update_zone_track_ids(self, zone_current_ids: Dict[str, set]) -> None:
        """Store current/cumulative track ids per zone (parity with overcrowding)."""
        for zone_name, ids in zone_current_ids.items():
            self._zone_current_track_ids[zone_name] = set(ids)
            self._zone_total_track_ids.setdefault(zone_name, set()).update(ids)

    def _cleanup_stale_zones(self, active_zones: set) -> None:
        """Drop per-zone state for zones no longer present (parity with overcrowding)."""
        for store in (self._zone_current_track_ids, self._zone_total_track_ids, self._zone_states):
            for z in list(store.keys()):
                if z not in active_zones:
                    del store[z]

    def _compute_severity(self, occupancy_percent: float, is_active: bool, config: LoiteringConfig) -> str:
        """Severity fluctuates with current loiterer occupancy (req 6).

        While active: > critical_severity_percent -> "critical"; else "high".
        Otherwise: "warning" once any loiterer is present, else "normal".
        """
        if is_active:
            return "critical" if occupancy_percent > float(config.critical_severity_percent) else "high"
        if occupancy_percent > 0.0:
            return "warning"
        return "normal"

    def _evaluate_loiter_incidents(
        self,
        zone_loiter_counts: Dict[str, int],
        config: LoiteringConfig,
    ) -> Dict[str, Dict[str, Any]]:
        """Stateful per-zone incident evaluation on loiterer counts (req 6).

        Mirrors the overcrowding hysteresis model: enter after ``persistence_frames``
        at/above ``high_severity_percent``; exit only after ``recovery_frames`` at/below
        ``recovery_ratio * threshold`` so the incident does not flicker.
        """
        high_percent = float(config.high_severity_percent)
        results: Dict[str, Dict[str, Any]] = {}

        for zone, count in zone_loiter_counts.items():
            threshold = config.resolve_loiter_person_threshold(zone)
            recovery_ratio = float(self._zone_param(zone, "recovery_ratio", config.recovery_ratio))
            exit_threshold = threshold * recovery_ratio
            occupancy_percent = (count / threshold * 100.0) if threshold else 0.0

            state = self._zone_states.setdefault(
                zone,
                {"violation_streak": 0, "recovery_streak": 0, "is_active": False, "alerted": False},
            )

            if occupancy_percent >= high_percent:
                state["violation_streak"] += 1
                state["recovery_streak"] = 0
                if state["violation_streak"] >= int(config.persistence_frames) and not state["is_active"]:
                    state["is_active"] = True
            elif count <= exit_threshold:
                state["recovery_streak"] += 1
                state["violation_streak"] = 0
                if state["recovery_streak"] >= int(config.recovery_frames) and state["is_active"]:
                    state["is_active"] = False

            severity = self._compute_severity(occupancy_percent, state["is_active"], config)
            results[zone] = {
                "loitering_count": count,
                "threshold": threshold,
                "occupancy_percent": round(occupancy_percent, 2),
                "severity": severity,
                "is_incident": state["is_active"],
            }
        return results

    def _build_zone_analysis(
        self,
        zone_results: Dict[str, Dict[str, Any]],
        zone_loiter_ids: Dict[str, set],
        config: LoiteringConfig,
    ) -> Dict[str, Any]:
        """Build the per-frame ``zone_analysis`` block (req 3 & 6)."""
        zone_analysis: Dict[str, Any] = {}
        for zone_name, st in (zone_results or {}).items():
            current_ids = sorted(self._zone_current_track_ids.get(zone_name, set()), key=lambda x: str(x))
            total_count = len(self._zone_total_track_ids.get(zone_name, set()))
            loiter_ids = sorted(zone_loiter_ids.get(zone_name, set()), key=lambda x: str(x))
            poly = self._current_zone_polys.get(zone_name)
            zone_coords = poly if isinstance(poly, list) else []
            zone_analysis[zone_name] = {
                "current_count": len(current_ids),
                "loitering_count": st.get("loitering_count", 0),
                "total_count": total_count,
                "current_track_ids": current_ids,
                "loitering_track_ids": loiter_ids,
                # The loiterer-count threshold that raises an incident for this zone (req 6).
                "loiter_person_threshold": st.get("threshold", config.loiter_person_threshold),
                "occupancy_percent": st.get("occupancy_percent", 0.0),
                "severity": st.get("severity", "normal"),
                "is_incident": st.get("is_incident", False),
                # Behavior thresholds in effect for this zone (req 4).
                "loiter_threshold_seconds": self._zone_param(
                    zone_name, "loiter_threshold_seconds", config.loiter_threshold_seconds
                ),
                "velocity_threshold_px_per_sec": self._zone_param(
                    zone_name, "velocity_threshold_px_per_sec", config.velocity_threshold_px_per_sec
                ),
                "stationary_ratio_threshold": self._zone_param(
                    zone_name, "stationary_ratio_threshold", config.stationary_ratio_threshold
                ),
                "zone_coords": zone_coords,
            }
        return zone_analysis

    # =========================================================================
    # Matrice alert helpers (same pattern as intrusion / overcrowding)
    # =========================================================================
    def _primary_alert_type(self, config: LoiteringConfig) -> str:
        at = getattr(config.alert_config, "alert_type", ["Default"]) if config.alert_config else ["Default"]
        if isinstance(at, (list, tuple)) and at:
            return str(at[0])
        return str(at or "Default")

    def _alert_settings_map(self, config: LoiteringConfig) -> Dict[str, Any]:
        if not config.alert_config:
            return {"Default": "JSON"}
        types_ = getattr(config.alert_config, "alert_type", ["Default"])
        values = getattr(config.alert_config, "alert_value", ["JSON"])
        if not isinstance(types_, (list, tuple)):
            types_ = [types_]
        if not isinstance(values, (list, tuple)):
            values = [values]
        return {str(t): v for t, v in zip(types_, values)}

    def _finalize_matrice_alert(
        self,
        alert: Dict[str, Any],
        frame_number: Any,
        config: LoiteringConfig,
        *,
        force_emit: bool = False,
        cooldown_key: str = "default",
    ) -> Dict[str, Any]:
        """Add status/frames/duration/emit fields (same as intrusion / overcrowding).

        ``cooldown_key`` scopes the emission cooldown to one logical alert stream
        (a zone or a track). It must be stable across frames — do not pass an id
        containing the frame number, or the cooldown never applies.
        """
        cur = frame_number if frame_number is not None else self._total_frame_counter
        try:
            cur_int = int(cur)
        except (TypeError, ValueError):
            cur_int = int(self._total_frame_counter)
        alert["status"] = "active"
        alert["start_frame"] = cur_int
        alert["current_frame"] = cur_int
        alert["duration_frames"] = 0
        if force_emit:
            alert["emit"] = True
            return alert
        cooldown = 0.0
        if config.alert_config:
            cooldown = float(getattr(config.alert_config, "alert_cooldown", 0.0) or 0.0)
        now = time.monotonic()
        emit_allowed = True
        if cooldown > 0:
            last = self._last_matrice_alert_emit_monotonic.get(cooldown_key)
            if last is not None and now - last < cooldown:
                emit_allowed = False
        alert["emit"] = emit_allowed
        if emit_allowed:
            self._last_matrice_alert_emit_monotonic[cooldown_key] = now
        return alert

    def _check_alerts(
        self,
        detections: List[Dict[str, Any]],
        frame_key: str,
        config: LoiteringConfig,
        video_time_seconds: float,
        frame_number: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generate loitering alerts — ONE-TIME per track_id (req 7).

        Each track emits exactly one alert, the first frame it is confirmed
        loitering; it never re-alerts (the incident itself persists every frame).
        Alerts carry the Matrice schema (create_alert_object + _finalize_matrice_alert)
        and the track's zone, so they attach to incidents/tracking_stats and flow to
        the incident manager exactly like intrusion_detection.
        """
        alerts: List[Dict[str, Any]] = []

        settings_map = self._alert_settings_map(config)
        alert_type_str = self._primary_alert_type(config)

        for det in detections:
            tid_int = self._parse_track_id(det.get("track_id"))
            if tid_int is None or tid_int < 0:
                if getattr(config, "enable_alerts_debug", False):
                    self.logger.info(f"[LOITER-ALERTS] skipping det without valid track_id: {det.get('track_id')}")
                continue

            st = self._loiter_tracks.get(tid_int)
            if not st:
                if getattr(config, "enable_alerts_debug", False):
                    self.logger.info(f"[LOITER-ALERTS] no state for tid={tid_int}")
                continue

            # Only alert on loitering tracks
            if not bool(st.get("is_loitering", False)):
                continue

            # One-time: each track alerts only once (the first frame it loiters).
            if tid_int in self._alerted_loiter_tracks:
                continue
            self._alerted_loiter_tracks.add(tid_int)
            st["last_alert_video_time"] = float(video_time_seconds)
            self._loiter_tracks[tid_int] = st

            zone_name = st.get("zone_name") or self.GLOBAL_ZONE_NAME
            threshold_seconds = float(
                self._zone_param(zone_name, "loiter_threshold_seconds", config.loiter_threshold_seconds)
            )

            speed_window = list(st.get("speed_window", []))
            slow_flags = list(st.get("slow_flags_window", []))
            win_avg_speed = float(np.mean(speed_window)) if speed_window else 0.0
            win_slow_ratio = float(np.mean(slow_flags)) if slow_flags else 0.0

            alert = self.create_alert_object(
                alert_type=alert_type_str,
                alert_id=f"loitering_alert_{zone_name}_{tid_int}",
                incident_category=str(self.CASE_TYPE),
                threshold_value=threshold_seconds,
                ascending=True,
                settings=settings_map,
            )
            alert["track_id"] = tid_int
            alert["zone_name"] = zone_name
            alert["bounding_box"] = det.get("bounding_box") or det.get("bbox")
            alert["confidence"] = float(det.get("confidence", 0.0))
            alert["category"] = "loitering_person"
            alert["dwell_seconds"] = round(float(st.get("presence_seconds", 0.0)), 2)
            alert["window_slow_ratio"] = round(float(win_slow_ratio), 3)
            alert["avg_speed_px_per_sec"] = round(float(win_avg_speed), 3)
            alert["threshold_seconds"] = threshold_seconds
            alert["event_type"] = str(self.CASE_TYPE)
            # Each track alerts once -> force emit (the one-time semantics are the gate).
            self._finalize_matrice_alert(alert, frame_number, config, force_emit=True)
            alerts.append(alert)
            self.logger.info(f"[LOITER-ALERTS] emitted alert track_id={tid_int} zone={zone_name} frame={frame_key}")

        return alerts

    def _update_tracking_state(self, detections: List[Dict[str, Any]]) -> None:
        """
        Update unique-counting state used in tracking_stats output.

        We maintain:
          - _per_category_total_track_ids: unique ids seen over time
          - _current_frame_track_ids: ids seen in this frame
        """
        categories = self.target_categories + ["loitering_person"]
        if not self._per_category_total_track_ids:
            self._per_category_total_track_ids = {cat: set() for cat in categories}

        self._current_frame_track_ids = {cat: set() for cat in categories}
        self._new_track_ids_this_frame = {cat: set() for cat in categories}

        for det in detections:
            cat = det.get("category")
            tid = det.get("track_id")
            tid_int = self._parse_track_id(tid)
            if cat not in categories or tid_int is None or tid_int < 0:
                continue

            tid = tid_int
            total_set = self._per_category_total_track_ids.setdefault(cat, set())
            if tid not in total_set:
                # First time this category has ever seen this track id.
                self._new_track_ids_this_frame.setdefault(cat, set()).add(tid)
                total_set.add(tid)
            self._current_frame_track_ids[cat].add(tid)

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Count of track ids reported for the FIRST time this frame, per category."""
        return {cat: len(ids) for cat, ids in self._new_track_ids_this_frame.items()}

    def _count_categories(self, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Frame-level raw detection count (not unique-tracks).

        This supports the Matrice agg_summary schema:
          - total_count
          - per_category_count
          - list of detections (minimal schema)
        """
        counts: Dict[str, int] = {}
        for det in detections:
            cat = det.get("category", "unknown")
            counts[cat] = counts.get(cat, 0) + 1

        return {
            "total_count": int(sum(counts.values())),
            "per_category_count": counts,
            "detections": [
                {
                    "bounding_box": det.get("bounding_box"),
                    "category": det.get("category"),
                    "confidence": det.get("confidence"),
                    "track_id": det.get("track_id"),
                    "frame_id": det.get("frame_id"),
                    "is_loitering": bool(det.get("is_loitering", False)),
                }
                for det in detections
            ],
        }

    def _generate_tracking_stats(
        self,
        counting_summary: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        config: LoiteringConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        zone_analysis: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        camera_info = self.get_camera_info_from_stream(stream_info)
        total_counts = [{"category": k, "count": int(v)} for k, v in self.get_total_counts().items()]
        current_counts = [
            {"category": k, "count": int(v)} for k, v in counting_summary.get("per_category_count", {}).items()
        ]

        detections_objs = []
        for det in counting_summary.get("detections", []):
            bbox = det.get("bounding_box", {}) or {}
            category = det.get("category", "unknown") or "unknown"
            detections_objs.append(self.create_detection_object(category, bbox))

        human_text_lines = [
            f"LOITERING @ {self._get_current_timestamp_str(stream_info)}",
            f"Loiterers in frame: {int(counting_summary.get('per_category_count', {}).get('loitering_person', 0))}",
            f"Default threshold: {float(config.loiter_threshold_seconds):.1f}s | "
            f"v_th: {float(config.velocity_threshold_px_per_sec):.1f}px/s | "
            f"ratio_th: {float(config.stationary_ratio_threshold):.2f}",
        ]
        if zone_analysis:
            human_text_lines.append("")
            human_text_lines.append("ZONE ANALYSIS:")
            for zn, zd in zone_analysis.items():
                if not isinstance(zd, dict):
                    continue
                human_text_lines.append(
                    f"\t- Zone '{zn}': loiterers={zd.get('loitering_count', 0)}"
                    f"/{zd.get('loiter_person_threshold', 0)} "
                    f"(occupancy={zd.get('occupancy_percent', 0.0)}%, severity={zd.get('severity', 'normal')})"
                )
        human_text = "\n".join(human_text_lines)

        alert_settings = [
            {
                "alert_type": ["Default"],
                "incident_category": self.CASE_TYPE,
                "threshold_level": {"loitering_person": config.loiter_threshold_seconds},
                "ascending": True,
                "settings": {"Default": "JSON"},
            }
        ]

        if config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_settings.append(
                {
                    "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": getattr(config.alert_config, "count_thresholds", {}) or {},
                    "ascending": True,
                    "settings": {
                        t: v
                        for t, v in zip(
                            getattr(config.alert_config, "alert_type", ["Default"]),
                            getattr(config.alert_config, "alert_value", ["JSON"]),
                        )
                    },
                }
            )

        tracking_stats = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections_objs,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=[
                {
                    "interval_type": "daily",
                    "reset_time": {"value": 9, "time_unit": "hour"},
                }
            ],
            start_time=self._get_current_timestamp_str(stream_info),
            reset_time=self._get_current_timestamp_str(stream_info),
        )
        tracking_stats["target_categories"] = self.target_categories
        new_counts = self.get_new_counts_this_frame()
        tracking_stats["current_new_counts"] = [
            {"category": cat, "count": int(new_counts.get(cat, 0))} for cat in self.target_categories
        ]
        tracking_stats["total_current_counts"] = current_counts

        # ------------------------------------------------------------------ #
        # VOLUME analytics block (consumed by legacy_analytics_bridge).       #
        #   avg/max_loiter_time_seconds = mean / longest ``presence_seconds`` #
        #       across ALL loiterers this session, updated only while        #
        #       ``is_loitering`` and retained after they leave, so the        #
        #       reading stays stable rather than collapsing to 0 the moment   #
        #       the frame empties (same shape as intrusion_detection's own    #
        #       avg/max_intrusion_time_seconds).                              #
        # ------------------------------------------------------------------ #
        for tid, st in self._loiter_tracks.items():
            if st.get("is_loitering"):
                presence = float(st.get("presence_seconds", 0.0))
                if presence > self._loiter_ever_seconds.get(tid, 0.0):
                    self._loiter_ever_seconds[tid] = presence
        loiter_secs = list(self._loiter_ever_seconds.values())
        tracking_stats["loitering_analytics"] = {
            "avg_loiter_time_seconds": (round(sum(loiter_secs) / len(loiter_secs), 2) if loiter_secs else 0.0),
            "max_loiter_time_seconds": round(max(loiter_secs), 2) if loiter_secs else 0.0,
        }
        return tracking_stats

    def _count_loitering_signals(
        self,
        counting_summary: Dict[str, Any],
        config: LoiteringConfig,
    ) -> int:
        """How many loitering / dwell signals are active this frame.

        Uses the broadest reliable signal so incidents are not blocked when the
        strict ``is_loitering`` velocity gate has not flipped yet (common with
        1–2 persons and default ``loiter_person_threshold=3``).
        """
        per_cat = counting_summary.get("per_category_count", {}) or {}
        from_summary = int(per_cat.get("loitering_person", 0))
        persons = int(per_cat.get("person", 0))
        marked = sum(1 for st in self._loiter_tracks.values() if st.get("is_loitering"))
        dwell = sum(
            1
            for st in self._loiter_tracks.values()
            if float(st.get("presence_seconds", 0)) >= float(config.loiter_threshold_seconds)
        )
        early_dwell = sum(
            1
            for st in self._loiter_tracks.values()
            if float(st.get("presence_seconds", 0)) >= float(config.min_presence_seconds)
        )
        tracked = sum(1 for st in self._loiter_tracks.values() if float(st.get("presence_seconds", 0)) > 0.0)
        return max(from_summary, marked, dwell, early_dwell, persons, tracked)

    def _generate_incidents(
        self,
        zone_results: Dict[str, Dict[str, Any]],
        counting_summary: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        config: LoiteringConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Raise a persistent loitering incident for Redis ``incident_res``.

        Triggers (any one — mirrors overcrowding ``zones OR alerts`` and restores
        pre-zone ``loitering_person > 0`` behaviour):
          - zone ``is_incident`` (count threshold + persistence),
          - any loiter / dwell signal in frame,
          - loiter alert emitted this frame.
        """
        zone_results = zone_results or {}
        counting_summary = counting_summary or {}
        loiter_signals = self._count_loitering_signals(counting_summary, config)
        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        incident_zones = [zn for zn, st in zone_results.items() if st.get("is_incident")]
        incident_active = bool(incident_zones) or loiter_signals > 0 or bool(alerts)

        self._ascending_alert_list = (
            self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list
        )

        alert_settings = self._build_incident_alert_settings(alerts, config)

        if not incident_active:
            self._consecutive_loiter_frames = 0
            self._ascending_alert_list.append(0)
            if self._loitering_incident_active and self._loitering_last_incident is not None:
                closing = dict(self._loitering_last_incident)
                closing["end_time"] = current_timestamp
                closing["severity_level"] = "info"
                closing["human_text"] = "INCIDENT DETECTED: loitering_detection severity=info"
                self._loitering_incident_active = False
                self._loitering_last_incident = None
                self.current_incident_end_timestamp = "N/A"
                return closing
            self._loitering_incident_active = False
            return {}

        self._consecutive_loiter_frames += 1
        if self._consecutive_loiter_frames < int(config.min_confirmation_frames):
            return {}

        self.current_incident_end_timestamp = ""
        if not self._loitering_incident_active:
            self._loitering_incident_active = True

        threshold = max(1, int(config.loiter_person_threshold))

        if incident_zones:
            zone_severities = [zone_results[zn].get("severity") for zn in incident_zones]
            level = "critical" if "critical" in zone_severities else "high"
            incident_quant = max(
                (zone_results[zn].get("occupancy_percent", 0.0) for zn in incident_zones),
                default=0.0,
            )
            human_text = f"INCIDENT DETECTED: {self.CASE_TYPE} severity={level}"
            self._ascending_alert_list.append(3)
        else:
            level = "high" if loiter_signals >= threshold else "medium"
            incident_quant = max((loiter_signals / threshold) * 100.0, 5.0)
            human_text = f"INCIDENT DETECTED: {self.CASE_TYPE} severity={level}"
            self._ascending_alert_list.append(2 if level == "medium" else 3)

        incident = self.create_incident(
            incident_id=f"incident_{self.CASE_TYPE}_{self._loitering_incident_id}",
            incident_type=self.CASE_TYPE,
            severity_level=level,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            start_time=self._get_start_timestamp_str(stream_info),
            end_time="",
            level_settings={"low": 1, "medium": 3, "high": 4, "significant": 4, "critical": 7},
        )
        if not incident:
            return {}
        incident["end_time"] = ""
        incident["incident_quant"] = round(incident_quant, 2)
        self._loitering_last_incident = dict(incident)
        return incident

    def _build_incident_alert_settings(
        self, alerts: List[Dict[str, Any]], config: LoiteringConfig
    ) -> List[Dict[str, Any]]:
        """Derive ``alert_settings`` from live alerts, else from alert_config."""
        alert_settings: List[Dict[str, Any]] = []
        if alerts:
            for alert_obj in alerts:
                if not isinstance(alert_obj, dict):
                    continue
                alert_settings.append(
                    {
                        "alert_type": alert_obj.get("alert_type"),
                        "incident_category": self.CASE_TYPE,
                        "threshold_value": alert_obj.get("threshold_value"),
                        "ascending": alert_obj.get("ascending", True),
                        "settings": alert_obj.get("settings", {}),
                    }
                )
        elif config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_settings.append(
                {
                    "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": {"loitering_person": config.loiter_person_threshold},
                    "ascending": True,
                    "settings": self._alert_settings_map(config),
                }
            )
        else:
            alert_settings.append(
                {
                    "alert_type": ["Default"],
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": {"loitering_person": config.loiter_person_threshold},
                    "ascending": True,
                    "settings": {"Default": "JSON"},
                }
            )
        return alert_settings

    def _generate_summary(
        self,
        incidents: Dict[str, Any],
        tracking_stats: Dict[str, Any],
        business_analytics: Dict[str, Any],
    ) -> str:
        lines: List[str] = []
        lines.append(f"Application Name: {self.CASE_TYPE}")
        lines.append(f"Application Version: {self.CASE_VERSION}")
        if tracking_stats:
            lines.append(f"Tracking Statistics:\t{tracking_stats.get('human_text', '')}")
        if incidents:
            lines.append(f"Incidents:\t{incidents.get('human_text', '')}")
        if business_analytics:
            lines.append(f"Business Analytics:\t{business_analytics.get('human_text', '')}")
        return "\n".join(lines)

    def get_total_counts(self) -> Dict[str, int]:
        """Return total unique track_id counts per category."""
        return {cat: len(ids) for cat, ids in self._per_category_total_track_ids.items()}

    # ----------------------------
    # Timestamp helpers (copied style from people_counting)
    # ----------------------------
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
        except Exception:
            # Non-fatal: exception ignored here; execution continues per surrounding logic.
            pass

        return timestamp_clean

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        _precision: bool = False,
        _frame_id: Optional[str] = None,
    ) -> str:
        """
        Canonical UTC timestamp generator.

        Always returns:
            YYYY:MM:DD HH:MM:SS

        Ignores frame-based timestamps to ensure consistency across:
        - cameras
        - pipelines
        - deployments
        """

        _ = (_frame_id, _precision)
        try:
            if stream_info:
                raw = stream_info.get("input_settings", {}).get("stream_time")

                if raw and isinstance(raw, str):
                    # Convert: "2026-03-17-12:05:33.123456 UTC"
                    raw = raw.replace(" UTC", "").strip()

                    if "." in raw:
                        raw = raw.split(".")[0]

                    parts = raw.split("-")
                    if len(parts) >= 6:
                        return f"{parts[0]}:{parts[1]}:{parts[2]} {parts[3]}:{parts[4]}:{parts[5]}"
        except Exception as exc:
            self.logger.debug(
                "Failed to parse stream_time from stream_info in _get_timestamp_str: %r",
                exc,
            )

        # Fallback → current UTC
        return datetime.now(timezone.utc).strftime("%Y:%m:%d %H:%M:%S")

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
