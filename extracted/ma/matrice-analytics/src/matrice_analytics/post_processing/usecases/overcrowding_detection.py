"""
Overcrowding Detection Usecase
--------------------------------

Definition:
    Overcrowding occurs when the number of detected persons in a zone
    exceeds a configured threshold for a configured number of frames.

Zone geometry:
    Zones drawn in the UI are stored on the deployment/camera post-processing
    config. When ``stream_info`` and API credentials (or ``set_config_client``)
    are available, zone polygons are resolved to pixel coordinates via the Matrice
    post-processing config API (one or more named zones supported).

Features:
- Zone-based or global detection
- Stateful detection (persistence + recovery)
- Alert cooldown support (AlertConfig)
- Incident lifecycle tracking (start/end)
- Single-frame input: a list of detections per ``process()`` call
- Same tracker stack as ``people_counting`` (``AdvancedTracker`` / optional simple tracker)
- Canonical agg_summary using BaseProcessor helpers

No density logic.
No rolling analytics.
Pure threshold-based safety detection.
"""

from __future__ import annotations

import copy
import os
import threading
import time
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..Trackers import ConfigDrivenTracker, TrackerProfile, legacy_sort_tracker_overrides
from ..utils import (
    ByteTrackWrapper,
    SORTTracker,
    apply_category_mapping,
    filter_by_confidence,
    point_in_polygon,
)
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.post_processing_config_client import (
    GEOMETRY_RETRY_INTERVAL as _GEOMETRY_RETRY_INTERVAL,
)
from ..utils.post_processing_config_client import (
    PostProcessingConfigClient,
)


def _coerce_pos_int(value: Any) -> Optional[int]:
    """Return ``value`` as a positive int, or ``None`` if not coercible / not > 0."""
    try:
        ivalue = int(value)
    except (TypeError, ValueError):
        return None
    return ivalue if ivalue > 0 else None


def lift_ai_camera_zones_into_post_processing(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Fold AI-style payloads into ``postProcessing`` so denormalization and zone extraction work.

    Supported shapes:

    1. Standard Matrice document: ``{"postProcessing": {camera_id: {..., "zone_config": {...}}}}``
    2. AI export (camera id as top-level key)::

           {"<camera_id>": {"zone_config": {"lines": {}, "zones": {"Polygon 1": [[nx,ny],...], ...}}}}

       Polygon / zone labels are kept as the user defined them (e.g. ``Polygon 1``); use the same
       strings in ``count_thresholds`` / ``zone_settings`` when overriding per zone.

    Top-level camera blocks are merged into ``postProcessing`` only for camera ids that are not
    already present under ``postProcessing`` (no overwrite).
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


# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------


@dataclass
class OvercrowdingDetectionConfig(BaseConfig):
    # Overcrowding is evaluated per zone. If ``zone_config`` is omitted, the entire
    # frame is treated as a single implicit ``global`` zone using ``default_capacity``
    # (unless ``require_zones`` is set, in which case zones are compulsory).
    zone_config: Optional[ZoneConfig] = None

    # Per-zone parameters (name -> {param: value}), e.g. {"road": {"capacity": 20}}.
    # In the UI/API/JSON payload these live *inside* ``zone_config`` (sibling of
    # ``zones``); ``__post_init__`` lifts them out to this field so the shared
    # ``ZoneConfig`` in core/config.py is not modified. ``capacity`` here is the
    # PRIMARY source of truth for each zone's capacity (the overcrowding threshold).
    zone_params: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Per-zone capacity (LEGACY). ``zone_params[<zone>]["capacity"]`` takes
    # precedence; this dict is kept as a backward-compatible fallback.
    count_thresholds: Dict[str, int] = field(default_factory=dict)

    # Capacity for the implicit ``global`` zone (whole frame) used when no zones are
    # configured. Also the fallback capacity for any zone with no capacity in
    # ``zone_params`` or ``count_thresholds``.
    default_capacity: int = 10

    # When True, zones are compulsory (no global fallback). When False (default), an
    # absent/empty zone_config falls back to a single ``global`` zone.
    require_zones: bool = False

    # Stability controls
    persistence_frames: int = 3
    recovery_frames: int = 5  # higher = incident persists longer through dips (less flicker/realerting)

    # Severity controls
    warning_ratio: float = 0.8
    recovery_ratio: float = 0.9  # hysteresis exit ratio

    # Incident severity bands, expressed as occupancy percentage (count / capacity * 100).
    # An incident is raised at >= high_severity_percent (100% = count >= capacity).
    # Severity then fluctuates: [high_severity_percent, critical_severity_percent] -> "high",
    # > critical_severity_percent -> "critical".
    high_severity_percent: float = 100.0
    critical_severity_percent: float = 120.0

    # Category mapping
    index_to_category: Optional[Dict[int, str]] = None
    target_categories: List[str] = field(default_factory=lambda: ["person"])

    alert_config: Optional[AlertConfig] = None

    # Optional per-zone overrides (threshold, warning_ratio, recovery_ratio, cooldown).
    # None = omit; same as an empty dict.
    zone_settings: Optional[Dict[str, Dict[str, Any]]] = None

    # Tracking — primary SORT/ByteTrack stack (same as area_utilization). Stamps a
    # persistent integer track_id on each detection for per-zone unique counting.
    enable_tracking: bool = True
    tracking_method: str = "sort"  # "sort" (Kalman + Hungarian) or "bytetrack"
    tracking_max_age: int = 30
    tracking_min_hits: int = 2
    tracking_iou_threshold: float = 0.25

    # Legacy tracker fallbacks (used only when enable_tracking=False).
    enable_advanced_tracker: bool = False
    enable_simple_tracker: bool = False

    def __post_init__(self) -> None:
        """Accept ``zone_config`` as a plain dict (UI/API/JSON payload shape).

        The Matrice UI / post-processing JSON emit ``zone_config`` as a dict with
        ``zones`` (pixel polygons) and ``zone_params`` (per-zone capacity, etc.)
        nested inside it, plus an unused ``lines`` key. Lift ``zones`` into a plain
        :class:`ZoneConfig` (untouched in core/config.py) and hoist ``zone_params``
        onto this config's own field, so behavior is identical whether built in
        Python or loaded from JSON.
        """
        zc = self.zone_config
        if isinstance(zc, dict):
            if not self.zone_params:
                nested = zc.get("zone_params", {})
                if isinstance(nested, dict):
                    self.zone_params = {
                        str(zn): dict(zp) for zn, zp in nested.items() if isinstance(zp, dict)
                    }
            self.zone_config = ZoneConfig(
                zones=zc.get("zones", {}) or {},
                zone_confidence_thresholds=zc.get("zone_confidence_thresholds", {}) or {},
                zone_categories=zc.get("zone_categories", {}) or {},
            )

    def _zone_capacity_raw(self, zone_name: str) -> Optional[int]:
        """Capacity declared for a zone via ``zone_params`` or ``count_thresholds``.

        Returns ``None`` when neither source declares a (positive) capacity — i.e.
        the zone would fall back to ``default_capacity``. Used by validation to
        require an explicit capacity for *named* zones.
        """
        params = (self.zone_params or {}).get(zone_name)
        if isinstance(params, dict) and "capacity" in params:
            cap = _coerce_pos_int(params.get("capacity"))
            if cap is not None:
                return cap
        return _coerce_pos_int(self.count_thresholds.get(zone_name))

    def resolve_capacity(self, zone_name: str) -> int:
        """Resolve a zone's capacity (the overcrowding threshold).

        Lookup order (single source of truth = ``zone_params``):
        1. ``zone_params[<zone>]["capacity"]``
        2. ``count_thresholds[<zone>]`` (legacy)
        3. ``default_capacity``
        """
        cap = self._zone_capacity_raw(zone_name)
        if cap is not None:
            return cap
        return int(self.default_capacity)

    def validate(self) -> List[str]:
        errors = super().validate()

        zones = self.zone_config.zones if (self.zone_config and self.zone_config.zones) else {}

        if not zones and self.require_zones:
            errors.append("zone_config with at least one zone is required (require_zones=True).")

        if zones:
            # When zones are provided, every zone must declare a positive capacity
            # via zone_params[...].capacity (preferred) or count_thresholds (legacy).
            for zone_name in zones:
                params = (self.zone_params or {}).get(zone_name, {})
                declared = params.get("capacity") if isinstance(params, dict) else None
                if declared is None:
                    declared = self.count_thresholds.get(zone_name)
                if declared is None:
                    errors.append(
                        f"capacity is required for zone '{zone_name}' "
                        f"(set zone_params['{zone_name}']['capacity'] or count_thresholds['{zone_name}'])."
                    )
                elif declared <= 0:
                    errors.append(f"capacity for zone '{zone_name}' must be positive.")
        else:
            # No zones: the whole frame is the implicit 'global' zone; needs a capacity.
            if self.default_capacity <= 0:
                errors.append("default_capacity must be positive when no zones are configured.")

        # Any explicit thresholds must be positive.
        for z, t in self.count_thresholds.items():
            if t <= 0:
                errors.append(f"capacity for zone '{z}' must be positive.")

        if self.persistence_frames <= 0:
            errors.append("persistence_frames must be positive.")

        if self.recovery_frames <= 0:
            errors.append("recovery_frames must be positive.")

        if not (0 < self.warning_ratio <= 1.0):
            errors.append("warning_ratio must be between 0 and 1.")

        if not (0 < self.recovery_ratio <= 1.0):
            errors.append("recovery_ratio must be between 0 and 1.")

        if self.zone_config:
            errors.extend(self.zone_config.validate())

        if self.alert_config:
            errors.extend(self.alert_config.validate())

        return errors


# ------------------------------------------------------------------------------
# Processor
# ------------------------------------------------------------------------------


class OvercrowdingDetectionUseCase(BaseProcessor):
    def __init__(self):
        super().__init__("overcrowding_detection")
        self.category = "safety"
        self.CASE_TYPE = "overcrowding_detection"
        self.CASE_VERSION = "1.0"

        self._zone_states: Dict[str, Dict[str, Any]] = {}
        self._frame_counter = 0

        # Pixel polygons of the zones used on the current frame, keyed by zone name
        # (``None`` for the synthetic full-frame "global" zone). Populated in
        # _count_per_zone and surfaced as "zone_coords" in zone_analysis.
        self._current_zone_polys: Dict[str, Any] = {}

        # Per-zone track-id tracking (parity with area_utilization for
        # zone_analysis / zone_stats / current_track_ids).
        self._zone_current_track_ids: Dict[str, set] = {}
        self._zone_total_track_ids: Dict[str, set] = {}

        # Frame-wide track-id tracking for current_new_counts (parity with area_utilization):
        # cumulative ids ever seen, and ids appearing for the first time this frame.
        self._per_category_total_track_ids: Dict[str, set] = {}
        self._new_track_ids_this_frame: Dict[str, set] = {}

        self._config_client: Optional[PostProcessingConfigClient] = None
        self._resolved_geometry_cache: Optional[OvercrowdingDetectionConfig] = None
        self._geometry_thread: Optional[threading.Thread] = None
        self._zone_resolution_attempted: bool = False
        self.tracker: Any = None
        self._tracker_seam = ConfigDrivenTracker()
        self._total_frame_counter: int = 0

        # Timestamp state used by the copied _get_*_timestamp_str helpers.
        self.start_timer = None
        self._tracking_start_time = None
        self.current_incident_end_timestamp: str = "N/A"

        # Incident manager (same wiring as intrusion_detection).
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._incident_manager_initialized: bool = False

        # Single-incident lifecycle + alert state (same pattern as intrusion_detection).
        self._overcrowding_incident_active: bool = False
        self._overcrowding_incident_id: str = "overcrowding_detection"
        self._ascending_alert_list: List[int] = []
        # Alert emission cooldown, keyed per logical alert stream (zone) so one zone's
        # emission never suppresses another's, and stamped with time.monotonic() so a
        # wall-clock step backwards (NTP correction, VM restore) cannot suppress alerts
        # past the cooldown.
        self._last_matrice_alert_emit_monotonic: Dict[str, float] = {}
        # Snapshot of the last active incident, re-emitted (with a real end_time) on
        # the frame the incident ends so the closing timestamp is surfaced.
        self._overcrowding_last_incident: Optional[Dict[str, Any]] = None

    # --------------------------------------------------------------------------
    # API geometry resolution (Matrice post-processing config → pixel zones)
    # --------------------------------------------------------------------------

    def set_config_client(self, client: Optional[PostProcessingConfigClient]) -> None:
        """Set client used to resolve zones from deployment/camera post-processing config."""
        self._config_client = client

    # --------------------------------------------------------------------------
    # Incident Manager (same wiring as intrusion_detection)
    # --------------------------------------------------------------------------

    def _initialize_incident_manager_once(self, config: OvercrowdingDetectionConfig) -> None:
        """Initialize incident manager ONCE (called on first process() invocation)."""
        if self._incident_manager_initialized:
            return
        try:
            self.logger.info(
                "[INCIDENT_MANAGER] Starting incident manager initialization for overcrowding detection..."
            )
            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=self.logger)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            if self._incident_manager:
                self.logger.info(
                    "[INCIDENT_MANAGER] Incident manager initialized successfully for overcrowding detection"
                )
            else:
                self.logger.warning(
                    "[INCIDENT_MANAGER] Incident manager not available, incidents won't be published"
                )
        except Exception as e:
            self.logger.error(
                f"[INCIDENT_MANAGER] Incident manager initialization failed: {e}",
                exc_info=True,
            )
        finally:
            self._incident_manager_initialized = True

    def _send_incident_to_manager(
        self,
        incident: Dict,
        stream_info: Optional[Dict[str, Any]] = None,
        context: Optional[ProcessingContext] = None,
    ) -> None:
        """Send incident to incident manager for level tracking and publishing.

        Sets ``incident_published_via_manager`` on the context so the legacy
        analytics bridge does not double-publish the same incident to
        ``incident_res``.
        """
        if context is not None:
            context.metadata["incident_published_via_manager"] = bool(self._incident_manager)
        if not self._incident_manager:
            self.logger.debug("[INCIDENT_MANAGER] No incident manager available, skipping")
            return
        if not incident:
            return
        camera_id = ""
        if stream_info:
            camera_info = stream_info.get("camera_info", {}) or {}
            camera_id = camera_info.get("camera_id", "") or camera_info.get("cameraId", "")
            if not camera_id:
                camera_id = stream_info.get("camera_id", "") or stream_info.get("cameraId", "")
            if not camera_id:
                topic = stream_info.get("topic", "")
                if topic:
                    if topic.endswith("_input_topic"):
                        camera_id = topic[: -len("_input_topic")]
                    elif topic.endswith("_input-topic"):
                        camera_id = topic[: -len("_input-topic")]
                    elif "_input_topic" in topic:
                        camera_id = topic.split("_input_topic")[0]
                    elif "_input-topic" in topic:
                        camera_id = topic.split("_input-topic")[0]
        if not camera_id:
            camera_id = "default_camera"
        try:
            published = self._incident_manager.process_incident(
                camera_id=camera_id, incident_data=incident, stream_info=stream_info
            )
            if published:
                self.logger.info(f"[INCIDENT_MANAGER] Incident published for camera: {camera_id}")
        except Exception as e:
            self.logger.error(
                f"[INCIDENT_MANAGER] Error sending incident to manager: {e}",
                exc_info=True,
            )

    def _start_geometry_resolver(
        self,
        config: OvercrowdingDetectionConfig,
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
                        self.logger.info("OvercrowdingDetection: zone geometry resolved from API (background thread)")
                        return
                    self.logger.info(
                        "OvercrowdingDetection: API geometry returned None, retrying in %ds",
                        _GEOMETRY_RETRY_INTERVAL,
                    )
                except Exception as exc:
                    self.logger.warning(
                        "OvercrowdingDetection: background geometry resolve error: %s",
                        exc,
                    )
                time.sleep(_GEOMETRY_RETRY_INTERVAL)

        t = threading.Thread(
            target=_resolver,
            daemon=True,
            name="overcrowding-zone-geometry-resolver",
        )
        self._geometry_thread = t
        t.start()
        self.logger.info("OvercrowdingDetection: started background zone geometry resolver thread")

    def _resolve_geometry_from_api(
        self,
        config: OvercrowdingDetectionConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[OvercrowdingDetectionConfig]:
        """Resolve ``zone_config`` from PostProcessingConfigClient (UI zones → pixel coords).

        Supports one or more named zones under ``zone_config.zones``. Returns a new
        config with ``zone_config`` set, or ``None`` if unavailable.
        """
        if stream_info is not None and not isinstance(stream_info, dict):
            self.logger.warning(
                "OvercrowdingDetection: _resolve_geometry_from_api skipped (stream_info must be dict, got %s)",
                type(stream_info).__name__,
            )
            return None

        client = self._config_client or (stream_info.get("config_client") if stream_info else None)
        if not client and stream_info:
            try:
                client = PostProcessingConfigClient(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    self.logger.info(
                        "OvercrowdingDetection: _resolve_geometry_from_api skipped "
                        "(no config_client; set MATRICE_ACCESS_KEY_ID, "
                        "MATRICE_SECRET_ACCESS_KEY, MATRICE_ACCOUNT_NUMBER "
                        "or call set_config_client() for API zone resolution)"
                    )
                    return None
                self._config_client = client
            except Exception as e:
                self.logger.warning(
                    "OvercrowdingDetection: could not create config client from env: %s",
                    e,
                )
                return None

        if not stream_info:
            self.logger.info("OvercrowdingDetection: _resolve_geometry_from_api skipped (no stream_info)")
            return None
        if not client:
            self.logger.info("OvercrowdingDetection: _resolve_geometry_from_api skipped (no config_client)")
            return None

        ids = client.get_stream_identifiers(stream_info)
        app_deployment_id = ids.get("app_deployment_id") or ""
        camera_id = ids.get("camera_id") or ""
        self.logger.info(
            "OvercrowdingDetection: _resolve_geometry_from_api app_deployment_id=%s camera_id=%s",
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

        self.logger.info("_resolve_geometry_from_api: configs=%r", configs)

        filtered = client.filter_configs_by_camera_id(configs, camera_id)
        if not filtered:
            self.logger.info(
                "_resolve_geometry_from_api: returning None (filter_configs_by_camera_id: no config for camera_id=%s)",
                camera_id,
            )
            return None

        doc = filtered[0]
        doc = lift_ai_camera_zones_into_post_processing(doc)
        width, height = client.get_resolution(camera_id)
        if width is None or height is None:
            self.logger.info(
                "_resolve_geometry_from_api: returning None (get_resolution: width=%r, height=%r for camera_id=%s)",
                width,
                height,
                camera_id,
            )
            return None

        self.logger.info("_resolve_geometry_from_api: width=%r, height=%r", width, height)

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

        self.logger.info("_resolve_geometry_from_api: zones_px=%r", zones_px)

        zones_dict: Dict[str, List[List[float]]] = {}
        for name, points in zones_px.items():
            if not isinstance(points, list) or len(points) < 3:
                self.logger.warning(
                    "OvercrowdingDetection: skipping zone %r (need list of >= 3 points)",
                    name,
                )
                continue
            row: List[List[float]] = []
            for pt in points:
                if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                    row.append([float(pt[0]), float(pt[1])])
                else:
                    row = []
                    break
            if len(row) >= 3:
                zones_dict[str(name)] = row
            else:
                self.logger.warning("OvercrowdingDetection: skipping zone %r (invalid point list)", name)
        new_zone_config = ZoneConfig(zones=zones_dict)

        # Per-zone params (capacity, etc.) live as a sibling of "zones" inside
        # "zone_config". Keep them on the config (not on ZoneConfig) so the shared
        # core/config.py ZoneConfig stays untouched.
        zone_params_raw = zone_config_raw.get("zone_params") or {}
        zone_params_dict: Dict[str, Dict[str, Any]] = {
            str(zn): dict(zp) for zn, zp in zone_params_raw.items() if isinstance(zp, dict)
        }

        self.logger.info(
            "OvercrowdingDetection: resolved %d zone(s) from API: %s (zone_params: %s)",
            len(zones_dict),
            list(zones_dict.keys()),
            list(zone_params_dict.keys()),
        )
        return replace(
            config,
            zone_config=new_zone_config,
            zone_params=zone_params_dict or config.zone_params,
        )

    def _normalize_detection_track_ids(self, processed_data: List[Dict[str, Any]]) -> None:
        """Align with ``people_counting``: unify alternate id keys into ``track_id``."""
        for det in processed_data:
            if not isinstance(det, dict):
                continue
            if det.get("track_id") is not None:
                continue
            for key in (
                "tracker_id",
                "tracking_id",
                "trackId",
                "trackID",
                "id",
                "object_id",
            ):
                candidate = det.get(key)
                if candidate is not None:
                    det["track_id"] = candidate
                    break

    def _simple_tracker_update(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Same lightweight fallback as ``people_counting`` (frame-local ids)."""
        for i, det in enumerate(detections):
            if det.get("track_id") is None:
                det["track_id"] = f"simple_{self._total_frame_counter}_{i}"
        return detections

    def _init_tracker(self, config: OvercrowdingDetectionConfig, stream_info: Optional[Dict[str, Any]]) -> None:
        """Initialize the primary SORT/ByteTrack tracker (same stack as area_utilization).

        Stamps a persistent integer ``track_id`` on each detection so downstream
        per-zone unique counts and track-id lists can be built.
        """
        if self.tracker is not None:
            return

        method = str(getattr(config, "tracking_method", "sort")).lower().strip()

        # F10b S9 (consolidation-plan.md Step 9): route the legacy SORT/ByteTrack
        # default onto the AdvancedTracker seam. MATRICE_LEGACY_SORT=1 keeps the
        # pre-migration path alive for one release (kill-switch, plan §7). Uses a
        # fresh ConfigDrivenTracker(), not self._tracker_seam -- that instance is
        # reserved for _apply_tracker_like_people_counting's separate LEGACY_40
        # tracker, and get_shared_tracker() caches one tracker per instance.
        if method in ("sort", "bytetrack") and os.environ.get("MATRICE_LEGACY_SORT") != "1":
            self.tracker = ConfigDrivenTracker().get_shared_tracker(
                profile=TrackerProfile.DEFAULT,
                **legacy_sort_tracker_overrides(config, method),
            )
            self.logger.info("OvercrowdingDetection: initialized AdvancedTracker (seam) for legacy %s method", method)
            return

        if method == "sort":
            self.tracker = SORTTracker(
                iou_threshold=float(getattr(config, "tracking_iou_threshold", 0.25)),
                max_age=int(getattr(config, "tracking_max_age", 30)),
                min_hits=int(getattr(config, "tracking_min_hits", 2)),
            )
            self.logger.info("OvercrowdingDetection: initialized SORTTracker")
            return

        if method == "bytetrack":
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
            self.logger.info("OvercrowdingDetection: initialized ByteTrackWrapper (fps=%s)", fps)
            return

        # Unknown method => no tracking
        self.tracker = None

    def _apply_tracker_like_people_counting(
        self,
        detections: List[Dict[str, Any]],
        config: OvercrowdingDetectionConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Legacy fallback: mirror ``PeopleCountingUseCase`` tracker block (AdvancedTracker + simple)."""
        processed_data = detections
        if getattr(config, "enable_advanced_tracker", True):
            try:
                if self.tracker is None:
                    self.tracker = self._tracker_seam.get_shared_tracker(
                        stream_info=stream_info,
                        profile=TrackerProfile.LEGACY_40,
                        namespace=True,
                        restore=True,
                        max_time_lost=int(1200),
                        frame_rate=25,
                    )
                return self.tracker.update(processed_data)
            except Exception as e:
                self.logger.warning("AdvancedTracker failed: %s", e)
                return processed_data
        elif getattr(config, "enable_simple_tracker", False):
            return self._simple_tracker_update(processed_data)
        return processed_data

    # --------------------------------------------------------------------------
    # Main Entry (single frame per call)
    # --------------------------------------------------------------------------

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        if not isinstance(config, OvercrowdingDetectionConfig):
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        errors = config.validate()
        if errors:
            context.mark_completed()
            return self.create_error_result(
                "Invalid configuration",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        stream_info_dict: Optional[Dict[str, Any]] = stream_info if isinstance(stream_info, dict) else None
        if stream_info is not None and stream_info_dict is None:
            self.logger.warning(
                "OvercrowdingDetection: stream_info must be dict, got %s; continuing without stream metadata",
                type(stream_info).__name__,
            )

        if not self._zone_resolution_attempted:
            self._zone_resolution_attempted = True
            if stream_info_dict:
                self.logger.info(
                    "OvercrowdingDetection: attempting zone geometry resolution from API (first frame, blocking)"
                )
                try:
                    resolved = self._resolve_geometry_from_api(config, stream_info_dict)
                    if resolved is not None:
                        self._resolved_geometry_cache = resolved
                        self.logger.info("OvercrowdingDetection: zone geometry resolved from API and cached")
                    else:
                        self.logger.warning(
                            "OvercrowdingDetection: API returned no zone config on first "
                            "attempt; starting background retry thread (every %ds). "
                            "Using zone_config from user config until resolved.",
                            _GEOMETRY_RETRY_INTERVAL,
                        )
                        self._start_geometry_resolver(config, stream_info_dict)
                except Exception as exc:
                    self.logger.warning(
                        "OvercrowdingDetection: zone geometry resolution raised on first "
                        "attempt (%s); starting background retry thread (every %ds). "
                        "Using zone_config from user config until resolved.",
                        exc,
                        _GEOMETRY_RETRY_INTERVAL,
                    )
                    self._start_geometry_resolver(config, stream_info_dict)
            else:
                self.logger.info(
                    "OvercrowdingDetection: no stream_info on first frame; using zone_config from user config"
                )

        effective_config = config
        if self._resolved_geometry_cache is not None:
            effective_config = self._resolved_geometry_cache
            self.logger.debug("OvercrowdingDetection: using API-resolved zone geometry")

        # One frame: list of detection dicts (legacy: dict of frame_id -> list takes first list)
        if isinstance(data, dict):
            self.logger.warning(
                "OvercrowdingDetection: expected list of detections for one frame; "
                "using first list value from mapping (legacy)"
            )
            frame_data: List[Dict[str, Any]] = []
            for v in data.values():
                if isinstance(v, list):
                    frame_data = v
                    break
        elif isinstance(data, list):
            frame_data = data
        else:
            context.mark_completed()
            return self.create_error_result(
                "Expected a list of detections for one frame",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if self._resolved_geometry_cache is not None:
            effective_config = self._resolved_geometry_cache

        # Initialize incident manager on first call (after zone resolution so the
        # config matches API zones when present) — same as intrusion_detection.
        self._initialize_incident_manager_once(effective_config)

        frame_key = "0"
        frame_number: Optional[int] = None
        if stream_info_dict:
            sf = stream_info_dict.get("input_settings", {}).get("start_frame")
            if sf is not None:
                frame_key = str(sf)
                frame_number = sf

        detections = self._prepare_detections(frame_data, effective_config)
        self._normalize_detection_track_ids(detections)

        # Tracking: assign stable cross-frame track_ids (same stack as area_utilization).
        # Primary path is SORT / ByteTrack via enable_tracking; AdvancedTracker and the
        # simple tracker remain as explicit fallbacks for backward compatibility.
        if getattr(effective_config, "enable_tracking", True):
            self._init_tracker(effective_config, stream_info_dict)
            if self.tracker is not None:
                try:
                    if isinstance(self.tracker, ByteTrackWrapper):
                        detections = self.tracker.update(detections, stream_info=stream_info_dict)
                    else:
                        detections = self.tracker.update(detections)
                except Exception as e:
                    self.logger.warning("OvercrowdingDetection tracker update failed: %s", e)
        elif getattr(effective_config, "enable_advanced_tracker", False):
            detections = self._apply_tracker_like_people_counting(detections, effective_config, stream_info_dict)
        elif getattr(effective_config, "enable_simple_tracker", False):
            detections = self._simple_tracker_update(detections)

        tracking_on = (
            getattr(effective_config, "enable_tracking", True)
            or getattr(effective_config, "enable_advanced_tracker", False)
            or getattr(effective_config, "enable_simple_tracker", False)
        )
        count_unique_tracks = tracking_on and any(d.get("track_id") is not None for d in detections)

        # Record first-appearance track ids this frame (drives current_new_counts).
        self._update_new_track_counts(detections, list(effective_config.target_categories or ["person"]))

        zone_counts = self._count_per_zone(
            detections,
            effective_config,
            count_unique_tracks=count_unique_tracks,
        )

        self._cleanup_stale_zones(zone_counts)

        zone_results = self._evaluate_overcrowding(zone_counts, effective_config)
        alerts = self._generate_alerts(zone_results, effective_config, frame_number)
        incidents_list = self._generate_incidents(
            zone_results, alerts, effective_config, frame_number, stream_info_dict
        )
        tracking_stats_list = self._generate_tracking_stats(
            detections, zone_results, alerts, effective_config, stream_info_dict
        )
        business_analytics_list = self._generate_business_analytics(zone_results, alerts, stream_info_dict)

        summary_list = self._generate_summary(incidents_list, tracking_stats_list, business_analytics_list)

        zone_analysis = self._build_zone_analysis(zone_results)

        self._frame_counter += 1
        self._total_frame_counter += 1

        # Align with area_utilization: incidents/tracking_stats/business_analytics
        # are emitted as single objects (first element), not lists.
        incidents_item = incidents_list[0] if incidents_list else {}
        tracking_item = tracking_stats_list[0] if tracking_stats_list else {}
        business_item = business_analytics_list[0] if business_analytics_list else {}
        summary_str = summary_list[0] if summary_list else ""

        # Publish to the incident manager for level tracking (same as intrusion_detection).
        self._send_incident_to_manager(incidents_item, stream_info_dict, context=context)

        agg_summary: Dict[str, Any] = {
            frame_key: {
                "incidents":          incidents_item,
                "tracking_stats":     tracking_item,
                "business_analytics": business_item,
                "alerts":             alerts,
                "human_text":         summary_str,
            }
        }
        if zone_analysis:
            agg_summary[frame_key]["zone_analysis"] = zone_analysis

        context.mark_completed()

        return self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

    # --------------------------------------------------------------------------
    # Detection Preparation
    # --------------------------------------------------------------------------

    def _prepare_detections(self, data, config):
        detections: List[Dict[str, Any]] = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    detections.append(item)
                elif isinstance(item, list):
                    detections.extend(d for d in item if isinstance(d, dict))
        elif isinstance(data, dict):
            for value in data.values():
                if isinstance(value, list):
                    detections.extend(d for d in value if isinstance(d, dict))
                    break

        if config.confidence_threshold is not None:
            detections = filter_by_confidence(detections, config.confidence_threshold)

        if config.index_to_category:
            detections = apply_category_mapping(detections, config.index_to_category)

        detections = [d for d in detections if isinstance(d, dict) and d.get("category") in config.target_categories]

        return detections

    # --------------------------------------------------------------------------
    # Zone Counting
    # --------------------------------------------------------------------------

    def _count_per_zone(
        self,
        detections: List[Dict[str, Any]],
        config: OvercrowdingDetectionConfig,
        *,
        count_unique_tracks: bool = False,
    ) -> Dict[str, int]:
        if config.zone_config and config.zone_config.zones:
            zones = config.zone_config.zones
        else:
            zones = {"global": None}

        # Remember the polygons used this frame so _build_zone_analysis can emit
        # them under "zone_coords".
        self._current_zone_polys = dict(zones)

        counts: Dict[str, int] = {}

        for zone_name, polygon in zones.items():
            if polygon is None:
                if count_unique_tracks:
                    tids = {d["track_id"] for d in detections if d.get("track_id") is not None}
                    counts[zone_name] = len(tids)
                    self._record_zone_track_ids(zone_name, tids)
                else:
                    counts[zone_name] = len(detections)
                    self._record_zone_track_ids(zone_name, set())
                continue

            poly_points = [(p[0], p[1]) for p in polygon]

            if count_unique_tracks:
                in_zone: set[Any] = set()
                for det in detections:
                    tid = det.get("track_id")
                    if tid is None:
                        continue
                    bbox = det.get("bounding_box") or det.get("bbox")
                    if not bbox:
                        continue
                    cx, cy = self._bbox_center(bbox)
                    if point_in_polygon((cx, cy), poly_points):
                        in_zone.add(tid)
                counts[zone_name] = len(in_zone)
                self._record_zone_track_ids(zone_name, in_zone)
            else:
                count = 0
                for det in detections:
                    bbox = det.get("bounding_box") or det.get("bbox")
                    if not bbox:
                        continue
                    cx, cy = self._bbox_center(bbox)
                    if point_in_polygon((cx, cy), poly_points):
                        count += 1
                counts[zone_name] = count
                self._record_zone_track_ids(zone_name, set())

        return counts

    def _record_zone_track_ids(self, zone_name: str, current_ids: set) -> None:
        """Store current/total track ids for a zone (parity with area_utilization)."""
        self._zone_current_track_ids[zone_name] = set(current_ids)
        if zone_name not in self._zone_total_track_ids:
            self._zone_total_track_ids[zone_name] = set()
        self._zone_total_track_ids[zone_name].update(current_ids)

    def _zone_track_ids(self, zone_name: str) -> Tuple[List[Any], int]:
        """Return ``(current_track_ids, total_count)`` for a zone (parity with area_utilization)."""
        current = sorted(self._zone_current_track_ids.get(zone_name, set()), key=lambda x: str(x))
        total_count = len(self._zone_total_track_ids.get(zone_name, set()))
        return current, total_count

    def _update_new_track_counts(self, detections: List[Dict[str, Any]], target_categories: List[str]) -> None:
        """Record track ids appearing for the FIRST time this frame (drives current_new_counts).

        Same semantics as area_utilization: a track id counts as "new" the first frame
        its category has ever seen it; thereafter it only contributes to totals.
        """
        self._new_track_ids_this_frame = {cat: set() for cat in target_categories}
        for det in detections:
            if not isinstance(det, dict):
                continue
            cat = det.get("category")
            track_id = det.get("track_id")
            if cat not in target_categories or track_id is None:
                continue
            total_set = self._per_category_total_track_ids.setdefault(cat, set())
            if track_id not in total_set:
                self._new_track_ids_this_frame.setdefault(cat, set()).add(track_id)
                total_set.add(track_id)

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Count of track ids reported for the FIRST time this frame, per category."""
        return {cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()}

    # --------------------------------------------------------------------------
    # Stateful Evaluation
    # --------------------------------------------------------------------------

    def _compute_severity(self, occupancy_percent: float, is_active: bool, warning_ratio: float, config):
        """Severity fluctuates with current occupancy (rule 3).

        While the incident is active:
            occupancy > critical_severity_percent  -> "critical"
            otherwise (>= high band, incl. hysteresis) -> "high"
        Below the incident threshold: "warning" near capacity, else "normal".
        """
        critical_percent = getattr(config, "critical_severity_percent", 120.0)
        if is_active:
            return "critical" if occupancy_percent > critical_percent else "high"
        if occupancy_percent >= warning_ratio * 100.0:
            return "warning"
        return "normal"

    def _evaluate_overcrowding(self, zone_counts, config):
        results = {}
        # An incident is raised when occupancy reaches high_severity_percent (rule 1).
        high_percent = getattr(config, "high_severity_percent", 100.0)
        for zone, count in zone_counts.items():
            # --- Per-zone capacity + optional overrides ---
            # Capacity (the overcrowding threshold) resolves from zone_params first,
            # then count_thresholds (legacy), then default_capacity. A zone_settings
            # "threshold" override still wins if present.
            zone_cfg = (config.zone_settings or {}).get(zone, {})
            threshold = zone_cfg.get("threshold", config.resolve_capacity(zone))

            warning_ratio = zone_cfg.get("warning_ratio", config.warning_ratio)
            recovery_ratio = zone_cfg.get("recovery_ratio", config.recovery_ratio)

            exit_threshold = threshold * recovery_ratio
            ratio = count / threshold if threshold else 0.0
            occupancy_percent = ratio * 100.0

            if zone not in self._zone_states:
                self._zone_states[zone] = {
                    "violation_streak": 0,
                    "recovery_streak": 0,
                    "is_active": False,
                    "start_timestamp": None,
                    "alerted": False,
                }

            state = self._zone_states[zone]

            # ENTER: rule 1 — occupancy >= high_severity_percent (i.e. count >= capacity).
            if occupancy_percent >= high_percent:
                state["violation_streak"] += 1
                state["recovery_streak"] = 0

                if state["violation_streak"] >= config.persistence_frames and not state["is_active"]:
                    state["is_active"] = True
                    state["start_timestamp"] = time.time()
                    state["alerted"] = False  # new episode — alert is allowed once (rule 2)

            # EXIT (Hysteresis)
            elif count <= exit_threshold:
                state["recovery_streak"] += 1
                state["violation_streak"] = 0

                if state["recovery_streak"] >= config.recovery_frames and state["is_active"]:
                    state["is_active"] = False
                    state["alerted"] = False  # reset so the next episode can alert again

            severity = self._compute_severity(occupancy_percent, state["is_active"], warning_ratio, config)

            results[zone] = {
                "count": count,
                "threshold": threshold,
                "ratio": round(ratio, 3),
                "occupancy_percent": round(occupancy_percent, 2),
                "severity": severity,
                "is_overcrowded": state["is_active"],
            }
        return results

    # --------------------------------------------------------------------------
    # Alert helpers (same pattern as intrusion_detection)
    # --------------------------------------------------------------------------

    def _primary_alert_type(self, config) -> str:
        at = getattr(config.alert_config, "alert_type", ["Default"]) if config.alert_config else ["Default"]
        if isinstance(at, (list, tuple)) and at:
            return str(at[0])
        return str(at or "Default")

    def _alert_settings_map(self, config) -> Dict[str, Any]:
        if not config.alert_config:
            return {}
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
        config,
        *,
        force_emit: bool = False,
        cooldown_key: str = "default",
    ) -> Dict[str, Any]:
        """Add status/frames/duration/emit fields (same as intrusion_detection).

        ``cooldown_key`` scopes the emission cooldown to one logical alert stream
        (a zone). It must be stable across frames — do not pass an id containing
        the frame number, or the cooldown never applies.
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

    # --------------------------------------------------------------------------
    # Alert Generation (same pattern as intrusion_detection)
    # --------------------------------------------------------------------------

    def _generate_alerts(self, zone_results, config, frame_number):
        alerts: List[Dict[str, Any]] = []

        if not config.alert_config:
            return alerts

        settings_map = self._alert_settings_map(config)
        alert_type_str = self._primary_alert_type(config)

        # Rule 2: alert ONCE per overcrowding episode. The incident itself persists
        # every frame (see _generate_incidents), but a zone emits a single alert at
        # onset; the per-zone "alerted" flag is reset on recovery in _evaluate_overcrowding.
        for zone, stats in zone_results.items():
            if not stats["is_overcrowded"]:
                continue
            state = self._zone_states.get(zone, {})
            if state.get("alerted"):
                continue
            alert = self.create_alert_object(
                alert_type=alert_type_str,
                alert_id=f"overcrowding_{zone}",
                incident_category=f"{self.CASE_TYPE}_{zone}",
                threshold_value=float(stats["threshold"]),
                ascending=True,
                settings=settings_map,
            )
            alert["zone"] = zone
            alert["current_value"] = stats["count"]
            alert["capacity"] = stats["threshold"]
            alert["occupancy_percent"] = stats.get("occupancy_percent", round(stats["ratio"] * 100.0, 2))
            alert["severity_level"] = stats["severity"]
            alert["event_type"] = self.CASE_TYPE
            self._finalize_matrice_alert(alert, frame_number, config, force_emit=True)
            alerts.append(alert)
            state["alerted"] = True  # mark this episode as alerted

        return alerts

    # --------------------------------------------------------------------------
    # Incident Generation (single aggregated incident, same as intrusion_detection)
    # --------------------------------------------------------------------------

    def _generate_incidents(self, zone_results, alerts, config, frame_number, stream_info):
        camera_info = self.get_camera_info_from_stream(stream_info)
        incidents: List[Dict[str, Any]] = []

        overcrowded_zones = [z for z, s in zone_results.items() if s.get("is_overcrowded")]
        overcrowding_active = bool(overcrowded_zones) or bool(alerts)

        current_timestamp = self._get_current_timestamp_str(
            stream_info, frame_id=str(frame_number) if frame_number is not None else None
        )
        self._ascending_alert_list = (
            self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list
        )

        # alert_settings derived from the live alerts (same as intrusion_detection).
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
                    "threshold_value": getattr(config, "count_thresholds", None),
                    "ascending": True,
                    "settings": dict(
                        zip(
                            getattr(config.alert_config, "alert_type", ["Default"]),
                            getattr(config.alert_config, "alert_value", ["JSON"]),
                        )
                    ),
                }
            )

        if overcrowding_active:
            start_timestamp = self._get_start_timestamp_str(stream_info)
            self._debug_stream_timing("start_timestamp", start_timestamp)
            # While an incident is active, end_time is always "" — the closing timestamp
            # is emitted on the frame the incident ends (see the else branch below).
            self.current_incident_end_timestamp = ""

            # Rule 3: incident severity fluctuates with occupancy. Use the worst
            # zone severity this frame ("critical" if any zone is critical, else "high").
            zone_severities = [zone_results[z].get("severity") for z in overcrowded_zones]
            level = "critical" if "critical" in zone_severities else "high"
            self._ascending_alert_list.append(3)
            if not self._overcrowding_incident_active:
                self._overcrowding_incident_active = True
            incident_id = self._overcrowding_incident_id

            # Worst-zone occupancy drives the quantitative severity for the manager.
            incident_quant = max(
                (zone_results[z].get("occupancy_percent", zone_results[z].get("ratio", 0.0) * 100.0)
                 for z in overcrowded_zones),
                default=0.0,
            )

            human_text_lines = [f"OVERCROWDING DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            for zn in overcrowded_zones:
                st = zone_results[zn]
                human_text_lines.append(
                    f"\t- Zone '{zn}': {st.get('count', 0)}/{st.get('threshold', 0)} "
                    f"(occupancy={round(st.get('ratio', 0.0) * 100.0, 1)}%)"
                )
            human_text = "\n".join(human_text_lines)

            event = self.create_incident(
                incident_id=incident_id,
                incident_type=self.CASE_TYPE,
                severity_level=level,
                human_text=human_text,
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=alert_settings,
                start_time=start_timestamp,
                end_time=self.current_incident_end_timestamp,
                # Overcrowding emits "high"/"critical"; keep legacy keys for any
                # downstream consumer that still references them.
                level_settings={"low": 1, "medium": 3, "high": 4, "significant": 4, "critical": 7},
            )
            # create_incident does `end_time or timestamp`, which would swallow an
            # empty string; force the exact lifecycle value (e.g. "" while active).
            event["end_time"] = self.current_incident_end_timestamp
            # incident_quant lets the incident manager map severity via thresholds.
            event["incident_quant"] = round(incident_quant, 2)
            incidents.append(event)
            # Remember this active incident so we can emit a closing snapshot on the
            # frame the incident ends (same severity, with a real end_time).
            self._overcrowding_last_incident = dict(event)
        else:
            if self._overcrowding_incident_active and self._overcrowding_last_incident is not None:
                # Incident just ended this frame: re-emit it with a real end_time.
                closing = dict(self._overcrowding_last_incident)
                closing["end_time"] = current_timestamp
                incidents.append(closing)
                self._overcrowding_last_incident = None
            else:
                incidents.append({})
            self._overcrowding_incident_active = False
            self.current_incident_end_timestamp = "N/A"  # reset lifecycle for the next episode
            self._ascending_alert_list.append(0)

        return incidents

    # --------------------------------------------------------------------------
    # Tracking Stats
    # --------------------------------------------------------------------------

    def _generate_tracking_stats(self, detections, zone_results, alerts, config, stream_info):
        camera_info = self.get_camera_info_from_stream(stream_info)
        target_categories = list(getattr(config, "target_categories", ["person"]) or ["person"])
        total_count = len(detections)

        start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        detections_objs = []
        for d in detections:
            bbox = d.get("bounding_box") or d.get("bbox")
            category = d.get("category", "person")
            detection_obj = self.create_detection_object(category, bbox, track_id=d.get("track_id"))
            # preserve optional fields for downstream consumers (parity with area_utilization)
            if d.get("confidence") is not None:
                detection_obj["confidence"] = d.get("confidence")
            detections_objs.append(detection_obj)

        alert_settings = self._build_alert_settings(config)
        reset_settings = [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]
        current_counts = [{"category": "person", "count": total_count}]

        tracking_stat = self.create_tracking_stats(
            total_counts=[{"category": "person", "count": total_count}],
            current_counts=current_counts,
            detections=detections_objs,
            human_text=self._build_human_text(zone_results),
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=reset_settings,
            start_time=start_timestamp,
            reset_time=reset_timestamp,
        )

        tracking_stat["target_categories"] = target_categories
        # Per-zone metrics are surfaced once, in the frame-level ``zone_analysis``
        # block (see _build_zone_analysis). It is a superset of the legacy
        # ``zone_statistics`` (raw zone_results dict) and ``zone_stats`` (per-zone
        # track-id list) that used to be duplicated here — occupancy_percent is now
        # carried in zone_analysis too — so those keys were removed.
        new_counts = self.get_new_counts_this_frame()
        tracking_stat["current_new_counts"] = [
            {"category": cat, "count": new_counts.get(cat, 0)} for cat in target_categories
        ]
        tracking_stat["total_current_counts"] = current_counts

        # ------------------------------------------------------------------ #
        # VOLUME analytics block (consumed by legacy_analytics_bridge).       #
        # Compact snapshot read directly by the bridge, which derives         #
        # current/peak/avg occupancy (last/max/mean) and the mean             #
        # occupancy_percentage over the 60s window from these raw values.     #
        # Whole-area aggregate across ALL zones (for the no-zones deployment  #
        # there is a single implicit "global" zone, so this collapses to it): #
        #   current_occupancy    = total people across all zones now.          #
        #   occupancy_percentage = total_count / total_capacity * 100          #
        #                          (sum of per-zone capacities).               #
        #   unique_visitors      = cumulative unique tracks across all zones.  #
        # NOTE: the INCIDENT severity still keys off the worst single zone     #
        # (max occupancy_percent) in _generate_incidents — that is the alert   #
        # signal; these VOLUME tiles are the whole-area view.                  #
        # ------------------------------------------------------------------ #
        total_count = 0
        total_capacity = 0
        for st in (zone_results or {}).values():
            if not isinstance(st, dict):
                continue
            total_count += int(st.get("count", 0) or 0)
            total_capacity += int(st.get("threshold", 0) or 0)
        current_occ = total_count
        occ_pct = round(total_count / total_capacity * 100.0, 2) if total_capacity > 0 else 0.0

        unique_visitors = 0
        for zone_name in (zone_results or {}):
            try:
                unique_visitors += int(self._zone_track_ids(zone_name)[1])
            except Exception:
                pass

        tracking_stat["overcrowding_analytics"] = {
            "current_occupancy": current_occ,
            "occupancy_percentage": occ_pct,
            "unique_visitors": int(unique_visitors),
        }

        return [tracking_stat]

    # --------------------------------------------------------------------------
    # Business Analytics
    # --------------------------------------------------------------------------

    def _generate_business_analytics(self, zone_results, alerts, stream_info):
        camera_info = self.get_camera_info_from_stream(stream_info)

        analytics = self.create_business_analytics(
            analysis_name="overcrowding",
            statistics=zone_results,
            human_text=self._build_human_text(zone_results),
            camera_info=camera_info,
            alerts=alerts,
        )

        return [analytics]

    # --------------------------------------------------------------------------
    # Zone Analysis (top-level key, parity with area_utilization)
    # --------------------------------------------------------------------------

    def _build_zone_analysis(self, zone_results: Dict[str, Any]) -> Dict[str, Any]:
        """Build the frame-level ``zone_analysis`` block (parity with area_utilization)."""
        zone_analysis: Dict[str, Any] = {}
        for zone_name, st in (zone_results or {}).items():
            if not isinstance(st, dict):
                continue
            current_ids, total_count = self._zone_track_ids(zone_name)
            # Pixel polygon of the zone (None for the synthetic full-frame
            # "global" zone -> emit an empty list).
            poly = self._current_zone_polys.get(zone_name)
            zone_coords = poly if isinstance(poly, list) else []
            zone_analysis[zone_name] = {
                "current_count":     st.get("count", 0),
                "total_count":       total_count,
                "current_track_ids": current_ids,
                "original_counts":   {},
                "threshold":         st.get("threshold", 0),
                "ratio":             st.get("ratio", 0.0),
                "occupancy_percent": st.get("occupancy_percent", 0.0),
                "severity":          st.get("severity", "normal"),
                "is_overcrowded":    st.get("is_overcrowded", False),
                "zone_coords":       zone_coords,
            }
        return zone_analysis

    # --------------------------------------------------------------------------
    # Alert settings (shared by tracking_stats + incidents, parity with area_utilization)
    # --------------------------------------------------------------------------

    def _build_alert_settings(self, config) -> List[Dict[str, Any]]:
        """Build the ``alert_settings`` list from config (parity with area_utilization)."""
        alert_config = getattr(config, "alert_config", None)
        if not (alert_config and hasattr(alert_config, "alert_type")):
            return []
        alert_type_cfg = getattr(alert_config, "alert_type", ["Default"])
        alert_value_cfg = getattr(alert_config, "alert_value", ["JSON"])
        return [
            {
                "alert_type": alert_type_cfg,
                "incident_category": self.CASE_TYPE,
                "threshold_value": getattr(config, "count_thresholds", {}) or {},
                "ascending": True,
                "settings": dict(zip(alert_type_cfg, alert_value_cfg)),
            }
        ]

    # --------------------------------------------------------------------------
    # Human Text
    # --------------------------------------------------------------------------

    def _build_human_text(self, zone_results):
        lines = ["Overcrowding Status:"]
        for zone, stats in zone_results.items():
            lines.append(
                f"{zone}: {stats['count']}/{stats['threshold']} (ratio={stats['ratio']}) severity={stats['severity']}"
            )
        return "\n".join(lines)

    def _generate_summary(self, incidents, tracking_stats, business_analytics) -> List[str]:
        """Frame-level human_text summary (parity with area_utilization)."""
        lines: List[str] = []
        lines.append("Application Name: " + self.CASE_TYPE)
        lines.append("Application Version: " + self.CASE_VERSION)

        if tracking_stats:
            lines.append("Tracking Statistics: " + f"\t{tracking_stats[0].get('human_text', '')}")
        if business_analytics:
            lines.append("Business Analytics: " + f"\t{business_analytics[0].get('human_text', '')}")

        if not incidents and not tracking_stats and not business_analytics:
            lines.append("Summary: " + "No Summary Data")

        return ["\n".join(lines)]

    # --------------------------------------------------------------------------
    # Cleanup
    # --------------------------------------------------------------------------

    def _cleanup_stale_zones(self, zone_counts):
        active_zones = set(zone_counts.keys())

        for z in list(self._zone_states.keys()):
            if z not in active_zones:
                del self._zone_states[z]

        for z in list(self._zone_current_track_ids.keys()):
            if z not in active_zones:
                del self._zone_current_track_ids[z]

        for z in list(self._zone_total_track_ids.keys()):
            if z not in active_zones:
                del self._zone_total_track_ids[z]

    def _bbox_center(self, bbox: Any) -> Tuple[float, float]:
        """
        bbox formats supported:
        - dict xmin,ymin,xmax,ymax
        - dict x1,y1,x2,y2
        - list [x1,y1,x2,y2]
        """
        if not bbox:
            return (0.0, 0.0)

        if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
            x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
            return ((float(x1) + float(x2)) / 2.0, (float(y1) + float(y2)) / 2.0)

        if isinstance(bbox, dict):
            if "xmin" in bbox:
                return (
                    (float(bbox.get("xmin", 0)) + float(bbox.get("xmax", 0))) / 2.0,
                    (float(bbox.get("ymin", 0)) + float(bbox.get("ymax", 0))) / 2.0,
                )
            if "x1" in bbox:
                return (
                    (float(bbox.get("x1", 0)) + float(bbox.get("x2", 0))) / 2.0,
                    (float(bbox.get("y1", 0)) + float(bbox.get("y2", 0))) / 2.0,
                )

        return (0.0, 0.0)

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
