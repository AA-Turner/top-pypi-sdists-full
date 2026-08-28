import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig
from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..utils import (
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    apply_category_mapping,
    bbox_smoothing,
    count_objects_in_zones,
    filter_by_confidence,
    match_results_structure,
)
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon
from ..utils.parking_analytics_tracker import ParkingAnalyticsTracker
from ..utils.post_processing_config_client import (
    GEOMETRY_RETRY_INTERVAL as _GEOMETRY_RETRY_INTERVAL,
)
from ..utils.post_processing_config_client import (
    PostProcessingConfigClient,
)


@dataclass
class ParkingLotAnalyticsConfig(BaseConfig):
    """Configuration for vehicle detection use case in parking lot analytics (parking time)."""

    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.6

    # Class Aggregation: Configuration parameters
    enable_class_aggregation: bool = True
    class_aggregation_window_size: int = 30  # 30 frames ≈ 1 second at 30 FPS

    # Parking Analytics Specific Parameters
    enable_parking_analytics: bool = True
    parked_threshold_seconds: float = 15.0
    movement_threshold_percent: float = 5.0
    movement_window_frames: int = 60
    max_history_size: int = 100
    assumed_fps: float = 30.0

    # JBK_720_GATE POLYGON = [[86, 328], [844, 317], [1277, 520], [1273, 707], [125, 713]]
    # Zones are used PURELY for occupancy counting (how many vehicles are
    # currently / have ever been inside the polygon). They have no notion of
    # "in" or "out" themselves. This is unchanged.
    #
    #   zone_config = {
    #       "zones": {"zone": [[x1, y1], [x2, y2], ...]},          # polygon(s)
    #   }
    zone_config: Optional[Dict[str, Any]] = None  # field(
    #     default_factory=lambda: {
    #         "zones": {
    #             "Interest_Region": [[86, 328], [844, 317], [1277, 520], [1273, 707], [125, 713]],
    #         },
    #     }
    # )

    # AB-line corridor for in/out counting — completely independent of
    # zone_config. The two lines (line_a, line_b) bound the monitored area:
    # region 2 = between the lines. Counting is occupancy-style on that
    # between-region, symmetric in both lines:
    #   entering region 2 from EITHER side (1->2 or 3->2)  = IN  +1
    #   leaving region 2 to EITHER side   (2->1 or 2->3)  = OUT +1
    # so a car that stops between the lines has registered IN, and a full
    # pass-through (1->2->3 or 3->2->1, or a direct 1->3 / 3->1 skip)
    # registers in+1 AND out+1.
    #   line_config = {
    #       "line_a": [[x1, y1], [x2, y2]],
    #       "line_b": [[x1, y1], [x2, y2]],
    #       "in_direction": "A_to_B",   # optional and IGNORED — counting is
    #                                   # symmetric; kept for config compat
    #   }
    # Coordinates are in pixel space, same as zone polygons (0-1 static configs
    # are scaled up to pixels via the embedded resolution key at load time).
    line_config: Optional[Dict[str, Any]] = None

    # A track must remain in its newly observed corridor region for at least
    # this many seconds of elapsed stream time before the region change is
    # confirmed and counted. This debounces detection/bbox flicker (a
    # foot-point bouncing back and forth near a line) so it doesn't register
    # as a false IN/OUT — only a region held steadily for a full second
    # counts.
    # Elapsed time is derived from stream_info's frame timestamp
    # (input_settings.start_frame / input_settings.original_fps), with a
    # consecutive-frame fallback so a missing/stuck stream clock can't block
    # confirmations entirely.
    line_crossing_debounce_seconds: float = 2.0

    # If a track disappears (drives out of view / tracker loses it) while a
    # region change is still pending, wait this long before finalizing it.
    # Finalizing emits the crossing if the pending change completes a full
    # corridor traversal — e.g. a car that crossed line A on its way out and
    # immediately left the frame, before the debounce could confirm. Without
    # this, exiting vehicles are systematically undercounted.
    line_lost_track_grace_seconds: float = 2.0

    # Counter reset schedule reported in tracking_stats; override per deployment.
    reset_settings: List[Dict[str, Any]] = field(
        default_factory=lambda: [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]
    )

    usecase_categories: List[str] = field(
        default_factory=lambda: ["bicycle", "motorcycle", "car", "van", "bus", "truck"]
    )
    target_categories: List[str] = field(
        default_factory=lambda: ["bicycle", "motorcycle", "car", "van", "bus", "truck"]
    )
    alert_config: Optional[AlertConfig] = None
    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            0: "bicycle",
            1: "motorcycle",
            2: "car",
            3: "van",
            4: "bus",
            5: "truck",
        }
    )


class ParkingLotAnalyticsUseCase(BaseProcessor):
    CATEGORY_DISPLAY = {
        "bicycle": "Bicycle",
        "motorcycle": "Motorcycle",
        "car": "Car",
        "van": "Van",
        "bus": "Bus",
        "truck": "Truck",
    }

    def __init__(self):
        super().__init__("parking_lot_analytics")
        self.category = "traffic"
        self.CASE_TYPE: Optional[str] = "parking_lot_analytics"
        self.CASE_VERSION: Optional[str] = "1.0"
        self.target_categories = ["bicycle", "motorcycle", "car", "van", "bus", "truck"]
        self.smoothing_tracker = None
        self.tracker = None
        self._tracker_seam = ConfigDrivenTracker()
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        # High enough that neighbouring parked cars (typically <0.2 IoU)
        # don't merge into one ID; low enough to re-associate the same
        # vehicle after a tracker ID switch.
        self._track_merge_iou_threshold: float = 0.3
        self._track_merge_time_window: float = 7.0
        # Stable internal IDs minted for upstream "untracked_*" placeholder
        # IDs; offset well above the AdvancedTracker's integer ID range.
        self._next_internal_track_id: int = 100000
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"
        self.start_timer = None

        # Parking analytics tracker
        self.parking_analytics_tracker = None

        # Track ID storage for total count calculation
        self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._tracked_in_zones = set()  # New: Unique track IDs that have entered any zone
        self._total_count = 0  # Cached total count
        self._last_update_time = time.time()  # Track when last updated
        self._total_count_list = []

        # Zone-based tracking storage (pure occupancy — current/total counts only)
        self._zone_current_track_ids: Dict[str, set] = {}  # zone_name -> track IDs in zone this frame
        self._zone_total_track_ids: Dict[str, set] = {}  # zone_name -> all track IDs ever in zone
        self._zone_current_counts: Dict[str, int] = {}
        self._zone_total_counts: Dict[str, int] = {}

        # AB-line directional corridor storage (footfall-style). line_a and
        # line_b (from config.line_config) split the frame into 3 regions:
        #   region 1 = before line A, region 2 = between A and B (corridor),
        #   region 3 = beyond line B.
        # Per track, we store the last CONFIRMED region plus any PENDING
        # region-change that hasn't yet persisted long enough (in real
        # elapsed time, derived from stream_info frame timestamps) to be
        # confirmed (debouncing against single-frame jitter).
        #   _track_region_state[tid] = {
        #       "confirmed_region": 1|2|3,
        #       "pending_region": 1|2|3|None,
        #       "pending_since": float seconds | None,
        #       "pending_frames": int,   # consecutive frames in pending region
        #       "last_seen_frame": int,  # for lost-track finalization/cleanup
        #       "last_confirmed_point": (x, y),  # last foot-point in confirmed
        #                                # region; path from here must cross a
        #                                # drawn segment for a count to register
        #       "last_point": (x, y),    # most recent foot-point
        #   }
        self._track_region_state: Dict[Any, Dict[str, Any]] = {}
        self._line_in_counts: Dict[str, int] = {}
        self._line_out_counts: Dict[str, int] = {}
        self._line_new_in: Dict[str, int] = {}
        self._line_new_out: Dict[str, int] = {}

        # ------------------------------------------------------------------ #
        # API-based zone geometry resolution (same pattern as dwell_detection)#
        # ------------------------------------------------------------------ #
        self._config_client: Optional[PostProcessingConfigClient] = None
        self._resolved_geometry_cache: Optional[ParkingLotAnalyticsConfig] = None
        self._geometry_thread: Optional[threading.Thread] = None
        self._zone_resolution_attempted: bool = False
        # Guards background resolver writes vs. process() reads
        self._geometry_lock = threading.Lock()

    # ------------------------------------------------------------------ #
    # Public API — zone geometry injection                                #
    # ------------------------------------------------------------------ #

    def set_config_client(self, client: Optional[PostProcessingConfigClient]) -> None:
        """Inject a ``PostProcessingConfigClient`` for API-based zone resolution.

        Must be called before the first ``process()`` invocation.  When a
        client is provided the use case resolves zone polygons drawn in the
        Matrice UI, falling back to ``zone_config`` in ``ParkingLotAnalyticsConfig``
        if the API is unavailable.
        """
        self._config_client = client

    # ------------------------------------------------------------------ #
    # Background zone-geometry resolver                                   #
    # ------------------------------------------------------------------ #

    def _start_geometry_resolver(
        self,
        config: "ParkingLotAnalyticsConfig",
        stream_info: Dict[str, Any],
    ) -> None:
        """Spawn a daemon thread that retries API zone resolution until success."""
        if self._geometry_thread is not None:
            return  # already running

        def _resolver() -> None:
            while True:
                try:
                    result = self._resolve_geometry_from_api(config, stream_info)
                    if result is not None:
                        with self._geometry_lock:
                            self._resolved_geometry_cache = result
                        self.logger.info("ParkingLotUseCase: zone geometry resolved from API (background thread)")
                        return
                    self.logger.info(
                        "ParkingLotUseCase: API returned no zone config, retrying in %ds",
                        _GEOMETRY_RETRY_INTERVAL,
                    )
                except Exception as exc:
                    self.logger.warning("ParkingLotUseCase: background geometry resolve error: %s", exc)
                time.sleep(_GEOMETRY_RETRY_INTERVAL)

        t = threading.Thread(target=_resolver, daemon=True, name="parking-zone-geometry-resolver")
        self._geometry_thread = t
        t.start()
        self.logger.info("ParkingLotUseCase: started background zone geometry resolver thread")

    def _resolve_geometry_from_api(
        self,
        config: "ParkingLotAnalyticsConfig",
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional["ParkingLotAnalyticsConfig"]:
        """Resolve zone polygons from the Matrice post-processing config API.

        Mirrors the pattern in ``DwellUseCase._resolve_geometry_from_api``.
        Zone/line coordinates are resolved to **pixel** space (via
        ``denormalize_config``) so they match the pixel-space bounding boxes
        used throughout the analytics pipeline — the same contract as every
        other zone use case (dwell, intrusion, hazard, etc.).

        Returns a new ``ParkingLotAnalyticsConfig`` with ``zone_config`` (and
        optionally ``line_config``) populated, or ``None`` when zones cannot
        be resolved.
        """
        client = self._config_client or (stream_info.get("config_client") if stream_info else None)
        if not client and stream_info:
            try:
                client = PostProcessingConfigClient(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    self.logger.info(
                        "ParkingLotUseCase: _resolve_geometry_from_api skipped — no session. "
                        "Set MATRICE_ACCESS_KEY_ID / MATRICE_SECRET_ACCESS_KEY / "
                        "MATRICE_ACCOUNT_NUMBER or call set_config_client() to enable API zone resolution."
                    )
                    return None
                self._config_client = client
            except Exception as exc:
                self.logger.warning("ParkingLotUseCase: cannot create PostProcessingConfigClient: %s", exc)
                return None

        if not stream_info or not client:
            return None

        ids = client.get_stream_identifiers(stream_info)
        app_deployment_id = ids.get("app_deployment_id") or ""
        camera_id = ids.get("camera_id") or ""
        self.logger.info(
            "ParkingLotUseCase: _resolve_geometry_from_api app_deployment_id=%s camera_id=%s",
            app_deployment_id or "(empty)",
            camera_id or "(empty)",
        )

        if not app_deployment_id or not camera_id:
            self.logger.info("ParkingLotUseCase: _resolve_geometry_from_api skipped — missing identifiers")
            return None

        configs, err, _ = client.get_post_processing_configs_by_app_deployment(app_deployment_id)
        if err or not configs:
            self.logger.info(
                "ParkingLotUseCase: _resolve_geometry_from_api — fetch failed (err=%r, count=%s)",
                err,
                len(configs) if configs else 0,
            )
            return None

        filtered = client.filter_configs_by_camera_id(configs, camera_id)
        if not filtered:
            self.logger.info(
                "ParkingLotUseCase: _resolve_geometry_from_api — no config for camera_id=%s",
                camera_id,
            )
            return None

        doc = filtered[0]

        # ── Step 1: read raw zone_config to check embedded resolution ──────── #
        # The Matrice API includes a "resolution" key inside zone_config.  We   #
        # need the resolution BEFORE calling denormalize_config, so we read the  #
        # raw (not-yet-denormalized) doc first.                                  #
        post_raw = doc.get("postProcessing") or {}
        cam_cfg_raw = post_raw.get(camera_id) or {}
        zone_config_raw_check = cam_cfg_raw.get("zone_config") or {}
        zones_pre = zone_config_raw_check.get("zones") or {}

        if not isinstance(zones_pre, dict) or not zones_pre:
            self.logger.info(
                "ParkingLotUseCase: _resolve_geometry_from_api — no zones in raw doc for camera_id=%s",
                camera_id,
            )
            return None

        # ── Step 2: get resolution — camera API first, embedded key as fallback #
        width, height = client.get_resolution(camera_id)
        if width is None or height is None:
            embedded_res = zone_config_raw_check.get("resolution") or {}
            w_fb = embedded_res.get("width") or embedded_res.get("Width")
            h_fb = embedded_res.get("height") or embedded_res.get("Height")
            if w_fb and h_fb:
                width, height = int(w_fb), int(h_fb)
                self.logger.info(
                    "ParkingLotUseCase: using embedded resolution %dx%d from zone_config "
                    "(CameraManagement unavailable)",
                    width,
                    height,
                )
            else:
                self.logger.info(
                    "ParkingLotUseCase: _resolve_geometry_from_api — no resolution for camera_id=%s "
                    "(get_resolution failed and no 'resolution' key in zone_config)",
                    camera_id,
                )
                return None

        # ── Step 3: denormalize (handles both 0-1 and already-pixel coords) ── #
        # _denormalize_points checks _is_normalized_points — pixel coords (> 1) #
        # are returned as-is; 0-1 coords are scaled to pixel space.             #
        doc_px = client.denormalize_config(doc, width, height)
        post = doc_px.get("postProcessing") or {}
        cam_cfg = post.get(camera_id) or {}
        zone_config_raw = cam_cfg.get("zone_config") or {}
        zones_px = zone_config_raw.get("zones") or {}

        if not isinstance(zones_px, dict) or not zones_px:
            self.logger.info(
                "ParkingLotUseCase: _resolve_geometry_from_api — no zones after denorm for camera_id=%s",
                camera_id,
            )
            return None

        # ── Step 4: keep zones in PIXEL space ────────────────────────────── #
        # Detection bounding boxes flow through the pipeline in pixel coords   #
        # (get_bbox_bottom25_center returns the raw bbox coords unchanged), so  #
        # zone polygons must stay in pixel space too — same contract as        #
        # DwellUseCase. denormalize_config (Step 3) already produced pixels.    #
        zones_dict = {name: [list(pt) for pt in points] for name, points in zones_px.items()}
        self.logger.info(
            "ParkingLotUseCase: resolved %d zone(s) from API: %s",
            len(zones_dict),
            list(zones_dict.keys()),
        )

        # Optionally resolve line_config (stored inside zone_config or at camera level)
        lines_px = zone_config_raw.get("lines") or cam_cfg.get("line_config") or {}
        line_config_resolved = None
        if isinstance(lines_px, dict) and lines_px:
            line_config_resolved = {name: [list(pt) for pt in pts] for name, pts in lines_px.items()}
            self.logger.info(
                "ParkingLotUseCase: resolved %d line(s) from API: %s",
                len(line_config_resolved),
                list(line_config_resolved.keys()),
            )

        from dataclasses import replace as _replace

        return _replace(
            config,
            zone_config={"zones": zones_dict},
            line_config=(line_config_resolved if line_config_resolved is not None else config.line_config),
        )

    def _apply_zone_denormalization(self, config: "ParkingLotAnalyticsConfig") -> None:
        """Resolve static-JSON zone/line coordinates to **pixel** space.

        When ``zone_config`` contains a ``"resolution": {"width": W, "height": H}`` entry
        (the format used in static JSON configs like ``parking_config.json``), any zone
        polygon or embedded ``"lines"`` supplied in normalized 0-1 coordinates are scaled
        up to pixel space so they match the pixel-space bounding boxes fed to
        ``get_bbox_bottom25_center`` / ``point_in_polygon``. Polygons already given in
        pixel coordinates are left untouched. This mirrors ``_is_normalized_points`` /
        ``_denormalize_points`` in ``PostProcessingConfigClient``.

        The ``resolution`` and embedded ``lines`` keys are consumed (popped) so the
        remaining ``zone_config`` carries only ``zones``. Subsequent calls are no-ops.
        """
        zone_cfg = config.zone_config
        if not isinstance(zone_cfg, dict):
            return
        resolution = zone_cfg.pop("resolution", None)
        # Lines may be embedded inside zone_config in static configs; lift them out
        # regardless of whether a resolution key is present.
        lines = zone_cfg.pop("lines", None)

        w = resolution.get("width") if isinstance(resolution, dict) else None
        h = resolution.get("height") if isinstance(resolution, dict) else None

        def _to_pixel(pts: List) -> List:
            # A polygon is normalized only when EVERY coordinate is within [0, 1];
            # if any coordinate exceeds 1 it is already in pixel space (leave as-is).
            valid = [p for p in pts if isinstance(p, (list, tuple)) and len(p) >= 2]
            is_norm = bool(valid) and all(0.0 <= float(p[0]) <= 1.0 and 0.0 <= float(p[1]) <= 1.0 for p in valid)
            if is_norm and w and h:
                return [[float(p[0]) * w, float(p[1]) * h] for p in valid]
            return [[float(p[0]), float(p[1])] for p in valid]

        zones = zone_cfg.get("zones") or {}
        zone_cfg["zones"] = {name: _to_pixel(pts) for name, pts in zones.items()}

        if isinstance(lines, dict) and lines:
            existing_lines = config.line_config if isinstance(config.line_config, dict) else {}
            if not (existing_lines.get("line_a") and existing_lines.get("line_b")):
                config.line_config = {name: _to_pixel(pts) for name, pts in lines.items()}

        if w and h:
            self.logger.info(
                "ParkingLotUseCase: resolved static zone polygons to pixel space (resolution %dx%d)",
                int(w),
                int(h),
            )

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        processing_start = time.time()
        # Relaxed check: Accept ParkingLotAnalyticsConfig OR any config with matching usecase/category
        # This handles multiprocessing module path mismatches while maintaining type safety
        is_valid_config = isinstance(config, ParkingLotAnalyticsConfig) or (
            hasattr(config, "usecase")
            and config.usecase == "vehicle_monitoring_parking_lot"
            and hasattr(config, "category")
            and config.category == "traffic"
        )
        if not is_valid_config:
            self.logger.error(
                f"Config validation failed in vehicle_monitoring_parking_lot. "
                f"Got type={type(config).__name__}, module={type(config).__module__}, "
                f"usecase={getattr(config, 'usecase', 'N/A')}, category={getattr(config, 'category', 'N/A')}"
            )
            return self.create_error_result(
                f"Invalid config type: expected ParkingLotAnalyticsConfig or config with usecase='vehicle_monitoring_parking_lot', "
                f"got {type(config).__name__} with usecase={getattr(config, 'usecase', 'N/A')}",
                usecase=self.name,
                category=self.category,
                context=context,
            )
        if context is None:
            context = ProcessingContext()

        # ------------------------------------------------------------------ #
        # API-based zone resolution (same pattern as dwell_detection)         #
        # First frame: blocking attempt → background retry if it fails.       #
        # Every frame: apply cached result from the background thread.        #
        # ------------------------------------------------------------------ #
        if not self._zone_resolution_attempted:
            self._zone_resolution_attempted = True
            _api_result = self._resolve_geometry_from_api(config, stream_info)
            if _api_result is not None:
                with self._geometry_lock:
                    self._resolved_geometry_cache = _api_result
                self.logger.info("ParkingLotUseCase: zone geometry resolved from API on first frame")
            else:
                self._start_geometry_resolver(config, stream_info)

        # Apply any geometry cached by the background thread
        with self._geometry_lock:
            _cached = self._resolved_geometry_cache
        if _cached is not None:
            config.zone_config = _cached.zone_config
            if _cached.line_config is not None:
                config.line_config = _cached.line_config

        # Resolve static JSON zone coords to pixel space (scale up any 0-1
        # polygons via the embedded resolution key; e.g. parking_config.json).
        self._apply_zone_denormalization(config)

        # Determine if zones are configured
        has_zones = bool(config.zone_config and config.zone_config.get("zones"))
        has_lines = bool(
            config.line_config
            and isinstance(config.line_config, dict)
            and config.line_config.get("line_a")
            and config.line_config.get("line_b")
        )

        # Normalize typical YOLO outputs (COCO pretrained) to internal schema
        data = self._normalize_yolo_results(data, getattr(config, "index_to_category", None))

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
        else:
            processed_data = data
            self.logger.debug("Did not apply confidence filtering since no threshold provided")

        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)
            self.logger.debug("Applied category mapping")

        allowed_categories = set(self.target_categories)
        if config.target_categories:
            allowed_categories &= set(config.target_categories)
        processed_data = [d for d in processed_data if d.get("category") in allowed_categories]
        self.logger.debug("Applied category filtering")

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
            processed_data = bbox_smoothing(processed_data, self.smoothing_tracker.config, self.smoothing_tracker)

        try:
            if self.tracker is None:
                self.tracker = self._tracker_seam.get_shared_tracker(
                    profile=TrackerProfile.DEFAULT,
                    enable_class_aggregation=config.enable_class_aggregation,
                    class_aggregation_window_size=config.class_aggregation_window_size,
                )
                self.logger.info("Initialized AdvancedTracker for Parking Lot Analytics use case")

                if config.enable_class_aggregation:
                    self.logger.info(
                        f"AdvancedTracker initialized with class aggregation "
                        f"(window_size={config.class_aggregation_window_size})"
                    )
                else:
                    self.logger.info("AdvancedTracker initialized without class aggregation")

            processed_data = self.tracker.update(processed_data)
        except Exception:
            self.logger.error(
                "AdvancedTracker failed; falling back to IoU-merged placeholder track IDs (count quality degraded)",
                exc_info=True,
            )

        # Line crossings are decoupled from zones: snapshot detections BEFORE
        # zone gating so a vehicle exiting the lot keeps feeding the corridor
        # counter even after its foot-point leaves every zone polygon. Zone
        # gating would otherwise cut the reverse traversal short and OUT
        # events would never complete.
        line_counting_data = processed_data

        # Zone gating: when zones are drawn, all zone-scoped analytics
        # (counting, parking analytics, alerts, incidents, tracking stats)
        # operate exclusively on vehicles whose foot-point lies inside at
        # least one zone polygon. Vehicles outside every zone are dropped
        # here, before those analytics consume the detections. With multiple
        # zones, being inside ANY one of them counts. Line crossings are the
        # exception — they use the pre-filter snapshot above.
        if has_zones:
            pre_zone_filter_count = len(processed_data)
            processed_data = self._filter_detections_by_zones(processed_data, config)
            if len(processed_data) != pre_zone_filter_count:
                self.logger.debug(
                    f"Zone filter: kept {len(processed_data)}/{pre_zone_filter_count} "
                    f"detections inside configured zones"
                )

        # Parking Analytics Update
        parking_analytics = None
        if config.enable_parking_analytics and processed_data:
            if self.parking_analytics_tracker is None:
                self.parking_analytics_tracker = ParkingAnalyticsTracker(
                    parked_threshold_frames=int(config.parked_threshold_seconds * config.assumed_fps),
                    movement_threshold_percent=config.movement_threshold_percent,
                    movement_window_frames=config.movement_window_frames,
                    fps=config.assumed_fps,
                )
                self.logger.info(
                    f"Initialized ParkingAnalyticsTracker: "
                    f"parked_threshold={config.parked_threshold_seconds}s, "
                    f"movement_threshold={config.movement_threshold_percent}%"
                )

            current_timestamp = self._get_current_timestamp_str(stream_info)
            parking_analytics = self.parking_analytics_tracker.update(
                detections=processed_data,
                current_frame=self._total_frame_counter,
                current_timestamp=current_timestamp,
            )

            # Log summary
            pa_summary = parking_analytics.get("summary", {})
            self.logger.info(
                f"[Frame {self._total_frame_counter}] Parking Analytics: "
                f"active={pa_summary.get('total_active', 0)}, "
                f"parked={pa_summary.get('total_parked', 0)}, "
                f"avg_dwell={pa_summary.get('average_dwell_time', 0)}s"
            )

        self._update_tracking_state(processed_data, has_zones=has_zones)
        self._total_frame_counter += 1

        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        counting_summary = self._count_categories(processed_data, config)
        total_counts = self.get_total_counts()
        counting_summary["total_counts"] = total_counts
        counting_summary["categories"] = {}
        for detection in processed_data:
            category = detection.get("category", "unknown")
            counting_summary["categories"][category] = counting_summary["categories"].get(category, 0) + 1

        zone_analysis = {}
        if has_zones:
            # Convert single frame to format expected by count_objects_in_zones
            frame_data = processed_data  # [frame_detections]
            zone_analysis = count_objects_in_zones(frame_data, config.zone_config["zones"], stream_info)

            if zone_analysis:
                enhanced_zone_analysis = self._update_zone_tracking(zone_analysis, processed_data, config)
                # Merge enhanced zone analysis with original zone analysis
                for zone_name, enhanced_data in enhanced_zone_analysis.items():
                    zone_analysis[zone_name] = enhanced_data

                # Adjust counting_summary for zones (current counts based on union across zones)
                per_category_count = {
                    cat: len(self._current_frame_track_ids.get(cat, set())) for cat in self.target_categories
                }
                counting_summary["per_category_count"] = {k: v for k, v in per_category_count.items() if v > 0}
                counting_summary["total_count"] = sum(per_category_count.values())

        # Independent in/out line-crossing counting, decoupled from zones.
        # The two lines bound a between-region: entering it from either side
        # counts IN, leaving it to either side counts OUT.
        line_analysis = {}
        if has_lines:
            line_analysis = self._update_line_counts(
                line_counting_data,
                config,
                stream_info,
            )

        alerts = self._check_alerts(counting_summary, zone_analysis, frame_number, config)
        predictions = self._extract_predictions(processed_data)
        _ = self._generate_incidents(counting_summary, zone_analysis, alerts, config, frame_number, stream_info)
        incidents_list = []
        tracking_stats_list = self._generate_tracking_stats(
            counting_summary,
            zone_analysis,
            alerts,
            config,
            frame_number,
            stream_info,
            parking_analytics,
            line_analysis,
        )

        business_analytics_list = self._generate_business_analytics(
            counting_summary, zone_analysis, alerts, config, stream_info, is_empty=True
        )
        summary_list = self._generate_summary(
            counting_summary,
            zone_analysis,
            incidents_list,
            tracking_stats_list,
            business_analytics_list,
            alerts,
        )

        incidents = incidents_list[0] if incidents_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
        business_analytics = business_analytics_list[0] if business_analytics_list else {}
        summary = summary_list[0] if summary_list else {}
        agg_summary = {
            str(frame_number): {
                "incidents": incidents,
                "tracking_stats": tracking_stats,
                "business_analytics": business_analytics,
                "alerts": alerts,
                "zone_analysis": zone_analysis,
                "line_analysis": line_analysis,
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
        result.predictions = predictions
        proc_time = time.time() - processing_start
        processing_latency_ms = proc_time * 1000.0
        processing_fps = (1.0 / proc_time) if proc_time > 0 else None
        self.logger.debug(
            "latency in ms: %s | Throughput fps: %s | Frame_Number: %s",
            processing_latency_ms,
            processing_fps,
            self._total_frame_counter,
        )
        return result

    def _filter_detections_by_zones(
        self,
        detections: List[Dict],
        config: ParkingLotAnalyticsConfig,
    ) -> List[Dict]:
        """
        Keep only detections whose foot-point (bottom-25% bbox center — the
        same point used for zone occupancy hit-testing) falls inside at least
        one configured zone polygon.

        Called once per frame when zones are configured, before any analytics
        run, so vehicles outside every zone are invisible to the entire
        pipeline. Detections without a bounding box are dropped too, since
        zone membership can't be established for them.
        """
        zones = (config.zone_config or {}).get("zones") or {}
        zone_items = [
            (name, [(pt[0], pt[1]) for pt in polygon])
            for name, polygon in zones.items()
            if polygon and len(polygon) >= 3
        ]
        if not zone_items:
            return detections

        filtered = []
        for detection in detections:
            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue
            point = get_bbox_bottom25_center(bbox)
            for zone_name, polygon_points in zone_items:
                if point_in_polygon(point, polygon_points):
                    # Shallow-copy detection and stamp the matching zone name so
                    # downstream analytics (tracking_stats, agg_summary) can
                    # report which zone each vehicle was detected in.
                    det = dict(detection)
                    det["zone_name"] = zone_name
                    filtered.append(det)
                    break  # first matching zone wins; no double-counting
        return filtered

    def _update_zone_tracking(
        self,
        zone_analysis: Dict[str, Dict[str, int]],
        detections: List[Dict],
        config: ParkingLotAnalyticsConfig,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Per-zone occupancy tracking.

        Zones answer one question only: "how many vehicles are currently /
        have ever been inside this polygon?". They have no concept of in/out
        direction — that's handled entirely by `_update_line_counts` via
        independent line segments defined in config.line_config.
        """
        if not zone_analysis or not config.zone_config or not config.zone_config.get("zones"):
            return {}

        enhanced_zone_analysis = {}
        zones = config.zone_config["zones"]
        zone_names = list(zones.keys())

        track_to_cat = {
            det.get("track_id"): det.get("category") for det in detections if det.get("track_id") is not None
        }

        # Initialize per-zone state
        for zone_name in zone_names:
            self._zone_current_track_ids.setdefault(zone_name, set())
            self._zone_total_track_ids.setdefault(zone_name, set())

        # Build current-frame zone membership via polygon hit-test
        current_frame_zone_tracks: Dict[str, set] = {zn: set() for zn in zone_names}

        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None:
                continue
            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue
            center_point = get_bbox_bottom25_center(bbox)
            for zone_name, zone_polygon in zones.items():
                polygon_points = [(pt[0], pt[1]) for pt in zone_polygon]
                if point_in_polygon(center_point, polygon_points):
                    current_frame_zone_tracks[zone_name].add(track_id)
                    if track_id not in self._total_count_list:
                        self._total_count_list.append(track_id)

        # Update global category totals from zone union
        for zone_name, current_tracks in current_frame_zone_tracks.items():
            for track_id in current_tracks:
                cat = track_to_cat.get(track_id)
                if cat:
                    self._current_frame_track_ids.setdefault(cat, set()).add(track_id)
                    if track_id not in self._tracked_in_zones:
                        self._tracked_in_zones.add(track_id)
                        self._per_category_total_track_ids.setdefault(cat, set()).add(track_id)

        # --- Update per-zone occupancy and build output ---
        for zone_name, zone_counts in zone_analysis.items():
            current_tracks = current_frame_zone_tracks.get(zone_name, set())

            self._zone_current_track_ids[zone_name] = current_tracks
            self._zone_total_track_ids[zone_name].update(current_tracks)
            self._zone_current_counts[zone_name] = len(current_tracks)
            self._zone_total_counts[zone_name] = len(self._zone_total_track_ids[zone_name])

            enhanced_zone_analysis[zone_name] = {
                "current_count": self._zone_current_counts[zone_name],
                "total_count": self._zone_total_counts[zone_name],
                "current_track_ids": list(current_tracks),
                "total_track_ids": list(self._zone_total_track_ids[zone_name]),
                "original_counts": zone_counts,
            }

        return enhanced_zone_analysis

    @staticmethod
    def _orientation(p: Tuple[float, float], q: Tuple[float, float], r: Tuple[float, float]) -> int:
        """Orientation of the ordered triplet (p, q, r): 0 collinear, +1/-1 for the two turn directions."""
        val = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        if val > 0:
            return 1
        if val < 0:
            return -1
        return 0

    @staticmethod
    def _point_on_segment(p: Tuple[float, float], q: Tuple[float, float], r: Tuple[float, float]) -> bool:
        """Whether q (already known collinear with p-r) lies within segment p-r's bounds."""
        return min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1])

    def _segments_intersect(
        self,
        p1: Tuple[float, float],
        p2: Tuple[float, float],
        q1: Tuple[float, float],
        q2: Tuple[float, float],
    ) -> bool:
        """
        Whether the FINITE segments p1-p2 and q1-q2 intersect (touching
        counts). Used to verify that a track's movement path physically
        crossed a drawn counting line — the region side-tests alone use
        infinite lines, which also trigger far beyond the drawn segment's
        endpoints (e.g. a car maneuvering deep inside the lot).
        """
        o1 = self._orientation(p1, p2, q1)
        o2 = self._orientation(p1, p2, q2)
        o3 = self._orientation(q1, q2, p1)
        o4 = self._orientation(q1, q2, p2)
        if o1 != o2 and o3 != o4:
            return True
        if o1 == 0 and self._point_on_segment(p1, q1, p2):
            return True
        if o2 == 0 and self._point_on_segment(p1, q2, p2):
            return True
        if o3 == 0 and self._point_on_segment(q1, p1, q2):
            return True
        if o4 == 0 and self._point_on_segment(q1, p2, q2):
            return True
        return False

    @staticmethod
    def _side_of_line(p1: Tuple[float, float], p2: Tuple[float, float], point: Tuple[float, float]) -> int:
        """
        Returns which side of the line p1->p2 a point lies on, via the sign of
        the 2D cross product: +1, -1, or 0 (exactly on the line).
        """
        x1, y1 = p1
        x2, y2 = p2
        px, py = point
        cross = (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)
        if cross > 0:
            return 1
        if cross < 0:
            return -1
        return 0

    def _side_sign_relative(
        self,
        p1: Tuple[float, float],
        p2: Tuple[float, float],
        point: Tuple[float, float],
        reference: Tuple[float, float],
    ) -> int:
        """
        Returns +1 if `point` is on the same side of line p1->p2 as
        `reference`, -1 if on the opposite side, 0 if either is exactly on
        the line (ambiguous).
        """
        s_point = self._side_of_line(p1, p2, point)
        s_ref = self._side_of_line(p1, p2, reference)
        if s_point == 0 or s_ref == 0:
            return 0
        return 1 if s_point == s_ref else -1

    def _resolve_line_definitions(self, config: ParkingLotAnalyticsConfig) -> Optional[Dict[str, Any]]:
        """
        Validate and return the AB-line corridor definition from
        config.line_config:
            {
                "line_a": [[x1, y1], [x2, y2]],
                "line_b": [[x1, y1], [x2, y2]],
                "in_direction": ...,   # optional, ignored (symmetric counting)
            }
        Returns None (and logs a warning) if the config is missing or either
        line is absent / malformed. "in_direction" is accepted for backward
        compatibility but has no effect: entering the between-lines region
        from either side is IN, leaving it to either side is OUT.
        """
        line_config = config.line_config
        if not line_config or not isinstance(line_config, dict):
            return None

        line_a = line_config.get("line_a")
        line_b = line_config.get("line_b")

        if not line_a or not line_b:
            self.logger.warning("line_config missing 'line_a' and/or 'line_b'; AB-line counting disabled")
            return None
        if len(line_a) != 2 or len(line_b) != 2:
            self.logger.warning(
                f"line_a/line_b must each have exactly 2 points (got {len(line_a)} and {len(line_b)}); "
                "AB-line counting disabled"
            )
            return None

        return {"line_a": line_a, "line_b": line_b}

    def _get_corridor_region(
        self,
        line_a: Tuple[Tuple[float, float], Tuple[float, float]],
        line_b: Tuple[Tuple[float, float], Tuple[float, float]],
        mid_a: Tuple[float, float],
        mid_b: Tuple[float, float],
        point: Tuple[float, float],
    ) -> Optional[int]:
        """
        Classify `point` into one of 3 corridor regions formed by line_a and
        line_b:
            region 1 = before line A (hasn't reached the corridor yet)
            region 2 = between line A and line B (inside the corridor)
            region 3 = beyond line B (has exited the corridor)
        Returns None if the point lies ambiguously on either line (resolve
        on a future frame instead of guessing).
        """
        a1, a2 = line_a
        b1, b2 = line_b

        # +1 means point is on the same side of A as B's midpoint (i.e.
        # "ahead" of A, heading toward/through the corridor).
        side_a = self._side_sign_relative(a1, a2, point, mid_b)
        if side_a == 0:
            return None
        if side_a < 0:
            return 1

        # Past line A. Now check position relative to B: +1 means still on
        # the same side as A's midpoint (i.e. still behind B == inside the
        # corridor); -1 means beyond B (exited the corridor).
        side_b = self._side_sign_relative(b1, b2, point, mid_a)
        if side_b == 0:
            return None
        return 2 if side_b > 0 else 3

    def _emit_corridor_event(
        self,
        is_in: bool,
        track_id: Any,
        debounce_seconds: float,
        new_in: Dict[str, int],
        new_out: Dict[str, int],
        corridor_key: str,
    ) -> None:
        """
        A confirmed entry into (is_in=True) or exit from (is_in=False) the
        between-lines region — counting is symmetric, so which line was
        crossed doesn't matter.
        """
        if is_in:
            self._line_in_counts[corridor_key] += 1
            new_in[corridor_key] += 1
            self.logger.debug(
                "Corridor IN (confirmed after %ss): tid=%s total_in=%d",
                debounce_seconds,
                track_id,
                self._line_in_counts[corridor_key],
            )
        else:
            self._line_out_counts[corridor_key] += 1
            new_out[corridor_key] += 1
            self.logger.debug(
                "Corridor OUT (confirmed after %ss): tid=%s total_out=%d",
                debounce_seconds,
                track_id,
                self._line_out_counts[corridor_key],
            )

    def _process_region_transition(
        self,
        prev_region: int,
        new_region: int,
        crossed_a: bool,
        crossed_b: bool,
        track_id: Any,
        debounce_seconds: float,
        new_in: Dict[str, int],
        new_out: Dict[str, int],
        corridor_key: str,
    ) -> None:
        """
        Apply the confirmed region transition (prev_region -> new_region),
        counting occupancy of region 2 (between the lines) symmetrically:
            1 -> 2  or  3 -> 2   = IN  (entered the between-lines area)
            2 -> 1  or  2 -> 3   = OUT (left it, either side)
            1 -> 3  or  3 -> 1   = IN + OUT (passed straight through)

        `crossed_a` / `crossed_b` report whether the track's actual movement
        path intersected the DRAWN line_a / line_b segment. A transition only
        counts when the physical boundary line for that transition was really
        crossed — region flips caused by movement beyond the segments'
        endpoints (the side-tests use infinite lines) are region bookkeeping
        only and never emit IN/OUT.
        """
        if new_region == 2 and prev_region in (1, 3):
            if crossed_a if prev_region == 1 else crossed_b:
                self._emit_corridor_event(True, track_id, debounce_seconds, new_in, new_out, corridor_key)
        elif prev_region == 2 and new_region in (1, 3):
            if crossed_a if new_region == 1 else crossed_b:
                self._emit_corridor_event(False, track_id, debounce_seconds, new_in, new_out, corridor_key)
        elif (prev_region, new_region) in ((1, 3), (3, 1)):
            if crossed_a and crossed_b:
                self._emit_corridor_event(True, track_id, debounce_seconds, new_in, new_out, corridor_key)
                self._emit_corridor_event(False, track_id, debounce_seconds, new_in, new_out, corridor_key)

    def _update_line_counts(
        self,
        detections: List[Dict],
        config: ParkingLotAnalyticsConfig,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Dict[str, Any]]:
        """
        AB-line corridor counter, debounced over a short timeframe using
        real elapsed time (derived from stream_info frame timestamps) with
        a consecutive-frame fallback.

        The two lines (line_a, line_b) from config.line_config split the
        frame into 3 regions: before A (1), between A and B (2), and beyond
        B (3). Counting is occupancy of region 2, symmetric in both lines —
        no direction or line naming is involved:
            1 -> 2  or  3 -> 2   = IN  +1 (entered the between-lines area)
            2 -> 1  or  2 -> 3   = OUT +1 (left it, either side)
            1 -> 3  or  3 -> 1   = IN +1 and OUT +1 (passed straight through)
        A car that stops between the lines therefore counts IN, and a full
        pass-through (1->2->3 or 3->2->1) counts in+1 AND out+1.

        A count registers ONLY on a physical crossing of a drawn line: the
        track's foot-point path must intersect the finite line_a / line_b
        SEGMENT for that boundary. The region side-tests use infinite lines
        (needed to classify every point in the frame), so vehicles moving
        around inside the area — or anywhere beyond the segments' endpoints
        — can flip regions without crossing a drawn line; those flips update
        region bookkeeping but never emit IN/OUT.

        A region change only confirms once it holds steady for at least
        `config.line_crossing_debounce_seconds` of elapsed stream time — or
        the equivalent number of consecutive frames, so a missing/stuck
        stream clock can't block confirmations — filtering out single-frame
        detection jitter near either line.

        Tracks that disappear mid-traversal (drove out of view before the
        debounce confirmed their last region change) are finalized after
        `config.line_lost_track_grace_seconds`: a pending change that
        completes a full traversal is emitted rather than dropped, so
        exiting vehicles that leave the frame right after crossing the
        outer line still count.
        """
        line_analysis: Dict[str, Dict[str, Any]] = {}
        line_def = self._resolve_line_definitions(config)
        if line_def is None:
            return line_analysis

        line_a = [(float(p[0]), float(p[1])) for p in line_def["line_a"]]
        line_b = [(float(p[0]), float(p[1])) for p in line_def["line_b"]]
        mid_a = ((line_a[0][0] + line_a[1][0]) / 2.0, (line_a[0][1] + line_a[1][1]) / 2.0)
        mid_b = ((line_b[0][0] + line_b[1][0]) / 2.0, (line_b[0][1] + line_b[1][1]) / 2.0)

        debounce_seconds = (
            config.line_crossing_debounce_seconds if config.line_crossing_debounce_seconds is not None else 0.5
        )

        # Derive elapsed stream time from stream_info's frame timestamp
        # rather than frame counting or wall-clock time, so debounce timing
        # tracks the video's own timeline.
        frame_timestamp_seconds = 0.0
        fps_for_debounce = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            frame_id = input_settings.get("start_frame", 0)
            fps = input_settings.get("original_fps", 30)

            if fps and fps > 0:
                fps_for_debounce = fps
                if frame_id:
                    frame_timestamp_seconds = frame_id / fps
        if not fps_for_debounce or fps_for_debounce <= 0:
            fps_for_debounce = getattr(config, "assumed_fps", 30.0) or 30.0

        # Consecutive-frame fallback for the debounce: if start_frame is
        # missing or stuck, frame_timestamp_seconds never advances and no
        # region change would ever confirm (blocking IN and OUT alike).
        # Counting consecutive frames spent in the pending region gives an
        # equivalent threshold that always advances.
        debounce_frames = max(1, int(round(debounce_seconds * fps_for_debounce)))
        current_frame = self._total_frame_counter

        # Internal accumulator key — the corridor produces ONE combined
        # in/out count (it's a single trap formed by both lines together),
        # but that count is exposed under BOTH "line_a" and "line_b" in the
        # returned line_analysis so each line can be reported/annotated
        # independently downstream.
        accumulator_key = "ab_corridor"
        self._line_in_counts.setdefault(accumulator_key, 0)
        self._line_out_counts.setdefault(accumulator_key, 0)
        new_in: Dict[str, int] = {accumulator_key: 0}
        new_out: Dict[str, int] = {accumulator_key: 0}

        seen_track_ids = set()
        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None:
                continue
            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue
            point = get_bbox_bottom25_center(bbox)
            region = self._get_corridor_region(line_a, line_b, mid_a, mid_b, point)
            if region is None:
                continue  # ambiguous (exactly on a line); resolve on a future frame
            seen_track_ids.add(track_id)

            state = self._track_region_state.get(track_id)
            if state is None:
                # First time we've seen this track — just establish its
                # confirmed region, no transition possible yet.
                self._track_region_state[track_id] = {
                    "confirmed_region": region,
                    "pending_region": None,
                    "pending_since": None,
                    "pending_frames": 0,
                    "last_seen_frame": current_frame,
                    # Last foot-point observed while in the confirmed region;
                    # the segment from here to the current point is what must
                    # physically cross a drawn line for a count to register.
                    "last_confirmed_point": point,
                    "last_point": point,
                }
                continue

            state["last_seen_frame"] = current_frame
            state["last_point"] = point
            confirmed_region = state["confirmed_region"]

            if region == confirmed_region:
                # Back to the confirmed region — any pending change was noise.
                state["pending_region"] = None
                state["pending_since"] = None
                state["pending_frames"] = 0
                state["last_confirmed_point"] = point
                continue

            if state["pending_region"] == region and state["pending_since"] is not None:
                # Same candidate region as before — check how long it's held.
                elapsed = frame_timestamp_seconds - state["pending_since"]
                state["pending_frames"] = state.get("pending_frames", 0) + 1
            else:
                # New candidate region — restart the debounce window.
                state["pending_region"] = region
                state["pending_since"] = frame_timestamp_seconds
                state["pending_frames"] = 1
                elapsed = 0.0

            if elapsed >= debounce_seconds or state["pending_frames"] >= debounce_frames:
                # The new region has held steady long enough — confirm it.
                # Counting additionally requires that the movement path
                # (last point in the old region -> current point) physically
                # crossed the drawn segment; a region flip alone (movement
                # past the segments' endpoints, or drift inside the area
                # over an infinite-line extension) never counts.
                path_start = state.get("last_confirmed_point", point)
                crossed_a = self._segments_intersect(path_start, point, line_a[0], line_a[1])
                crossed_b = self._segments_intersect(path_start, point, line_b[0], line_b[1])
                self._process_region_transition(
                    confirmed_region,
                    region,
                    crossed_a,
                    crossed_b,
                    track_id,
                    debounce_seconds,
                    new_in,
                    new_out,
                    accumulator_key,
                )
                state["confirmed_region"] = region
                state["pending_region"] = None
                state["pending_since"] = None
                state["pending_frames"] = 0
                state["last_confirmed_point"] = point

        # Finalize tracks that have disappeared (drove out of view / lost by
        # the tracker) for longer than the grace period. If a lost track
        # still had a pending region change that completes a full corridor
        # traversal — the classic case is a car that crossed line A on its
        # way out and immediately left the frame, before the debounce could
        # confirm — emit that crossing now instead of silently dropping it.
        # Deleting the state afterwards also keeps _track_region_state from
        # growing without bound.
        grace_seconds = getattr(config, "line_lost_track_grace_seconds", 2.0)
        grace_frames = max(1, int(round(grace_seconds * fps_for_debounce)))
        for tid in list(self._track_region_state.keys()):
            if tid in seen_track_ids:
                continue
            st = self._track_region_state[tid]
            last_seen = st.get("last_seen_frame")
            if last_seen is None:
                st["last_seen_frame"] = current_frame
                continue
            if current_frame - last_seen < grace_frames:
                continue
            pending = st.get("pending_region")
            if (
                pending is not None
                and pending != st.get("confirmed_region")
                # A single-frame flicker followed by track loss must not
                # count: only finalize a pending change that was observed on
                # at least 2 consecutive frames before the track vanished.
                and st.get("pending_frames", 0) >= 2
            ):
                # Emit the pending entry/exit so e.g. a car that crossed the
                # outer line on its way out and left the frame before the
                # full debounce elapsed still counts OUT — subject to the
                # same physical-crossing requirement as the live path.
                path_start = st.get("last_confirmed_point")
                path_end = st.get("last_point")
                if path_start is not None and path_end is not None:
                    crossed_a = self._segments_intersect(path_start, path_end, line_a[0], line_a[1])
                    crossed_b = self._segments_intersect(path_start, path_end, line_b[0], line_b[1])
                    self._process_region_transition(
                        st["confirmed_region"],
                        pending,
                        crossed_a,
                        crossed_b,
                        tid,
                        debounce_seconds,
                        new_in,
                        new_out,
                        accumulator_key,
                    )
            del self._track_region_state[tid]

        # Expose the single combined corridor count under both line names —
        # "line_a" and "line_b" — rather than a generic "corridor" key, so
        # downstream consumers can key off each line's own name directly.
        shared_fields = {
            # Counting is symmetric (region-2 occupancy); key kept so
            # downstream consumers reading in_direction don't break.
            "in_direction": "symmetric",
            "in_count": self._line_in_counts[accumulator_key],
            "out_count": self._line_out_counts[accumulator_key],
            "new_in": new_in[accumulator_key],
            "new_out": new_out[accumulator_key],
        }
        line_analysis["line_a"] = {**shared_fields, "points": [list(p) for p in line_a]}
        line_analysis["line_b"] = {**shared_fields, "points": [list(p) for p in line_b]}

        self._line_new_in = new_in
        self._line_new_out = new_out
        return line_analysis

    def _normalize_yolo_results(self, data: Any, index_to_category: Optional[Dict[int, str]] = None) -> Any:
        """
        Normalize YOLO-style outputs to internal detection schema:
        - category/category_id: prefer string label using COCO mapping if available
        - confidence: map from 'conf'/'score' to 'confidence'
        - bounding_box: ensure dict with keys (x1,y1,x2,y2) or (xmin,ymin,xmax,ymax)
        - supports list of detections and frame_id -> detections dict
        """

        def to_bbox_dict(d: Dict[str, Any]) -> Dict[str, Any]:
            if "bounding_box" in d and isinstance(d["bounding_box"], dict):
                return d["bounding_box"]
            if "bbox" in d:
                bbox = d["bbox"]
                if isinstance(bbox, dict):
                    return bbox
                if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
                    x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
                    return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
            if "xyxy" in d and isinstance(d["xyxy"], (list, tuple)) and len(d["xyxy"]) >= 4:
                x1, y1, x2, y2 = d["xyxy"][0], d["xyxy"][1], d["xyxy"][2], d["xyxy"][3]
                return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
            if "xywh" in d and isinstance(d["xywh"], (list, tuple)) and len(d["xywh"]) >= 4:
                cx, cy, w, h = d["xywh"][0], d["xywh"][1], d["xywh"][2], d["xywh"][3]
                x1, y1, x2, y2 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
                return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
            return {}

        def resolve_category(d: Dict[str, Any]) -> Tuple[str, Optional[int]]:
            raw_cls = d.get("category", d.get("category_id", d.get("class", d.get("cls"))))
            label_name = d.get("name")
            if isinstance(raw_cls, int):
                if index_to_category and raw_cls in index_to_category:
                    return index_to_category[raw_cls], raw_cls
                return str(raw_cls), raw_cls
            if isinstance(raw_cls, str):
                # Some YOLO exports provide string labels directly
                return raw_cls, None
            if label_name:
                return str(label_name), None
            return "unknown", None

        def normalize_det(det: Dict[str, Any]) -> Dict[str, Any]:
            category_name, category_id = resolve_category(det)
            if isinstance(category_name, str):
                # Models sometimes emit labels with stray whitespace
                # (e.g. "truck ") which would fail target-category filtering.
                category_name = category_name.strip()
            confidence = det.get("confidence", det.get("conf", det.get("score", 0.0)))
            bbox = to_bbox_dict(det)
            normalized = {
                "category": category_name,
                "confidence": confidence,
                "bounding_box": bbox,
            }
            if category_id is not None:
                normalized["category_id"] = category_id
            # Preserve optional fields
            for key in ("track_id", "frame_id", "masks", "segmentation"):
                if key in det:
                    normalized[key] = det[key]
            return normalized

        if isinstance(data, list):
            return [normalize_det(d) if isinstance(d, dict) else d for d in data]
        if isinstance(data, dict):
            # Detect tracking style dict: frame_id -> list of detections
            normalized_dict: Dict[str, Any] = {}
            for k, v in data.items():
                if isinstance(v, list):
                    normalized_dict[k] = [normalize_det(d) if isinstance(d, dict) else d for d in v]
                elif isinstance(v, dict):
                    normalized_dict[k] = normalize_det(v)
                else:
                    normalized_dict[k] = v
            return normalized_dict
        return data

    def _check_alerts(
        self,
        summary: dict,
        _zone_analysis: Dict,
        frame_number: Any,
        config: ParkingLotAnalyticsConfig,
    ) -> List[Dict]:
        _ = (_zone_analysis,)

        def get_trend(data, lookback=900, threshold=0.6):
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True
            increasing = 0
            total = 0
            for i in range(1, len(window)):
                if window[i] >= window[i - 1]:
                    increasing += 1
                total += 1
            ratio = increasing / total
            return ratio >= threshold

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts = []
        total_detections = summary.get("total_count", 0)
        per_category_count = summary.get("per_category_count", {})

        if not config.alert_config:
            return alerts

        if hasattr(config.alert_config, "count_thresholds") and config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total_detections > threshold:
                    alerts.append(
                        {
                            "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                            "alert_id": f"alert_{category}_{frame_key}",
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                            "settings": {
                                t: v
                                for t, v in zip(
                                    getattr(config.alert_config, "alert_type", ["Default"]),
                                    getattr(config.alert_config, "alert_value", ["JSON"]),
                                )
                            },
                        }
                    )
                elif category in per_category_count and per_category_count[category] > threshold:
                    alerts.append(
                        {
                            "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                            "alert_id": f"alert_{category}_{frame_key}",
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                            "settings": {
                                t: v
                                for t, v in zip(
                                    getattr(config.alert_config, "alert_type", ["Default"]),
                                    getattr(config.alert_config, "alert_value", ["JSON"]),
                                )
                            },
                        }
                    )
        return alerts

    def _generate_incidents(
        self,
        counting_summary: Dict,
        _zone_analysis: Dict,
        alerts: List,
        config: ParkingLotAnalyticsConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        _ = (_zone_analysis,)
        incidents = []
        total_detections = counting_summary.get("total_count", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        self._ascending_alert_list = (
            self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list
        )

        if total_detections > 0:
            start_timestamp = self._get_start_timestamp_str(stream_info)
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

            if (
                config.alert_config
                and hasattr(config.alert_config, "count_thresholds")
                and config.alert_config.count_thresholds
            ):
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

            human_text_lines = [f"VEHICLE INCIDENTS DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            human_text = "\n".join(human_text_lines)

            alert_settings = []
            if config.alert_config and hasattr(config.alert_config, "alert_type"):
                alert_settings.append(
                    {
                        "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": (
                            config.alert_config.count_thresholds
                            if hasattr(config.alert_config, "count_thresholds")
                            else {}
                        ),
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

            event = self.create_incident(
                incident_id=f"{self.CASE_TYPE}_{frame_number}",
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
            incidents.append({})
        return incidents

    def _generate_tracking_stats(
        self,
        counting_summary: Dict,
        zone_analysis: Dict,
        alerts: List,
        config: ParkingLotAnalyticsConfig,
        _frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        parking_analytics: Optional[Dict] = None,
        line_analysis: Optional[Dict] = None,  # NEW PARAMETER — independent in/out lines
    ) -> List[Dict]:
        _ = (_frame_number,)
        camera_info = self.get_camera_info_from_stream(stream_info)
        tracking_stats = []
        total_detections = counting_summary.get("total_count", 0)
        total_counts_dict = counting_summary.get("total_counts", {})
        per_category_count = counting_summary.get("per_category_count", {})
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        self._debug_stream_timing("start_timestamp", start_timestamp)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        total_counts = [{"category": cat, "count": count} for cat, count in total_counts_dict.items() if count > 0]
        current_counts = [
            {"category": cat, "count": count}
            for cat, count in per_category_count.items()
            if count > 0 or total_detections > 0
        ]

        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "vehicle")
            if detection.get("masks"):
                segmentation = detection.get("masks", [])
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            elif detection.get("segmentation"):
                segmentation = detection.get("segmentation")
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            elif detection.get("mask"):
                segmentation = detection.get("mask")
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            else:
                detection_obj = self.create_detection_object(category, bbox)

            # Attach track_id if available
            track_id = detection.get("track_id")
            if track_id is not None:
                if isinstance(detection_obj, dict):
                    detection_obj["track_id"] = track_id
                else:
                    try:
                        detection_obj.track_id = track_id
                    except Exception:
                        pass
                    if hasattr(detection_obj, "__dict__"):
                        try:
                            detection_obj.__dict__["track_id"] = track_id
                        except Exception:
                            pass

            # Attach zone_name — the polygon this vehicle was detected inside
            zone_name = detection.get("zone_name")
            if zone_name is not None:
                if isinstance(detection_obj, dict):
                    detection_obj["zone_name"] = zone_name
                else:
                    try:
                        detection_obj.zone_name = zone_name
                    except Exception:
                        pass
                    if hasattr(detection_obj, "__dict__"):
                        try:
                            detection_obj.__dict__["zone_name"] = zone_name
                        except Exception:
                            pass

            detections.append(detection_obj)

        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_settings.append(
                {
                    "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": (
                        config.alert_config.count_thresholds if hasattr(config.alert_config, "count_thresholds") else {}
                    ),
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

        # Generate human text similar to people_counting format
        human_text_lines = []
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")

        # Zone occupancy — purely "how many are inside", no direction
        if zone_analysis:
            human_text_lines.append("\t- Vehicles Detected by Zone (occupancy):")
            for zone_name, zone_data in zone_analysis.items():
                if not isinstance(zone_data, dict):
                    continue
                current_count = zone_data.get("current_count", 0)
                total_count = zone_data.get("total_count", 0)
                human_text_lines.append(f"\t\t- {zone_name}: current={int(current_count)} total={int(total_count)}")
        else:
            human_text_lines.append(f"\t- Vehicles Detected: {total_detections}")
            if per_category_count:
                for cat, count in per_category_count.items():
                    if count > 0:
                        human_text_lines.append(f"\t\t- {cat}: {count}")

        # Line crossings — AB-line directional corridor, decoupled from zones
        if line_analysis:
            human_text_lines.append("\t- Line Crossings:")
            for line_name, line_data in line_analysis.items():
                if not isinstance(line_data, dict):
                    continue
                in_direction = line_data.get("in_direction", "A_to_B")
                in_count = line_data.get("in_count", 0)
                out_count = line_data.get("out_count", 0)
                n_in = line_data.get("new_in", 0)
                n_out = line_data.get("new_out", 0)
                human_text_lines.append(
                    f"\t\t- {line_name} (in_direction={in_direction}): IN={in_count} OUT={out_count}"
                    f"  (+{n_in} in / +{n_out} out this frame)"
                )

        human_text_lines.append("")
        human_text = "\n".join(human_text_lines)

        # getattr: the relaxed config check admits duck-typed configs that
        # may predate the reset_settings field.
        reset_settings = getattr(config, "reset_settings", None) or [
            {"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}
        ]
        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts,
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

        # Get new track IDs count (vehicles that appeared for FIRST TIME - requires tracker to be enabled)
        new_counts_dict = self.get_new_counts_this_frame()
        current_new_counts = [{"category": cat, "count": count} for cat, count in new_counts_dict.items()]
        tracking_stat["current_new_counts"] = current_new_counts

        # Pure zone occupancy counts (no in/out — that's line_counts now)
        if zone_analysis:
            tracking_stat["zone_counts"] = {
                zone_name: {
                    "current_count": zd.get("current_count", 0),
                    "total_count": zd.get("total_count", 0),
                }
                for zone_name, zd in zone_analysis.items()
                if isinstance(zd, dict)
            }

        # AB-line directional corridor in/out totals
        if line_analysis:
            tracking_stat["line_counts"] = {
                line_name: {
                    "in_direction": ld.get("in_direction", "A_to_B"),
                    "total_in": ld.get("in_count", 0),
                    "total_out": ld.get("out_count", 0),
                    "new_in": ld.get("new_in", 0),
                    "new_out": ld.get("new_out", 0),
                }
                for line_name, ld in line_analysis.items()
                if isinstance(ld, dict)
            }

        # Add parking analytics to output
        if parking_analytics:
            pa_summary = parking_analytics.get("summary", {})
            tracking_stat["parking_analytics"] = {
                "per_vehicle": parking_analytics.get("active_vehicles", []),
                "summary": pa_summary,
                "parked_vehicles_count": pa_summary.get("total_parked", 0),
                "average_dwell_time_seconds": pa_summary.get("average_dwell_time", 0.0),
                "max_parked_time_seconds": pa_summary.get("max_parked_time_seconds", 0.0),
                "newly_parked_total": parking_analytics.get("newly_parked_total", 0),
                "newly_parked_by_category": parking_analytics.get("newly_parked_by_category", {}),
            }

            self.logger.debug(f"Added parking analytics: {len(parking_analytics.get('active_vehicles', []))} vehicles")

        tracking_stats.append(tracking_stat)
        return tracking_stats

    def _generate_business_analytics(
        self,
        _counting_summary: Dict,
        _zone_analysis: Dict,
        _alerts: Any,
        _config: ParkingLotAnalyticsConfig,
        _stream_info: Optional[Dict[str, Any]] = None,
        is_empty=False,
    ) -> List[Dict]:
        _ = (_alerts, _config, _counting_summary, _stream_info, _zone_analysis)
        if is_empty:
            return []

        return None

    def _generate_summary(
        self,
        _summary: dict,
        _zone_analysis: Dict,
        incidents: List,
        tracking_stats: List,
        business_analytics: List,
        _alerts: List,
    ) -> List[str]:
        """
        Generate a human_text string for the tracking_stat, incident, business analytics and alerts.
        """
        _ = (_alerts, _summary, _zone_analysis)
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

    def _get_track_ids_info(self, detections: list) -> Dict[str, Any]:
        frame_track_ids = set()
        for det in detections:
            tid = det.get("track_id")
            if tid is not None:
                frame_track_ids.add(tid)
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

    def _update_tracking_state(self, detections: list, has_zones: bool = False):
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        if not hasattr(self, "_previous_frame_track_ids"):
            self._previous_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._prune_stale_track_merge_state(time.time())

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.target_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id
            if not has_zones:
                self._per_category_total_track_ids.setdefault(cat, set()).add(canonical_id)
            # For current frame, add unconditionally here; will be overridden/adjusted if has_zones in _update_zone_tracking
            self._current_frame_track_ids.setdefault(cat, set()).add(canonical_id)

        # NEW track IDs = present in current frame but NOT in previous frame
        self._new_track_ids_this_frame = {
            cat: (self._current_frame_track_ids.get(cat, set()) - self._previous_frame_track_ids.get(cat, set()))
            for cat in self.target_categories
        }

        # Snapshot current -> previous for next call
        self._previous_frame_track_ids = {cat: set(ids) for cat, ids in self._current_frame_track_ids.items()}

    def get_total_counts(self):
        return {cat: len(ids) for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Get count of NEW track IDs that appeared in this frame/aggregation vs the previous one."""
        return {cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()}

    def get_current_frame_counts(self) -> Dict[str, int]:
        """Get count of ALL track IDs currently in this frame (existing + new)."""
        return {cat: len(ids) for cat, ids in getattr(self, "_current_frame_track_ids", {}).items()}

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
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
            # Non-fatal: exception ignored here; execution continues per surrounding logic.
            pass

        # If parsing fails, return the cleaned string as-is
        return timestamp_clean

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision=False,
        frame_id: Optional[str] = None,
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

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False) -> str:
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

    def _count_categories(self, detections: list, _config: ParkingLotAnalyticsConfig) -> dict:
        _ = (_config,)
        counts = {}
        for det in detections:
            cat = det.get("category", "unknown")
            counts[cat] = counts.get(cat, 0) + 1
        return {
            "total_count": sum(counts.values()),
            "per_category_count": counts,
            "detections": [
                {
                    "bounding_box": det.get("bounding_box"),
                    "category": det.get("category"),
                    "confidence": det.get("confidence"),
                    "track_id": det.get("track_id"),
                    "frame_id": det.get("frame_id"),
                    "zone_name": det.get("zone_name"),
                }
                for det in detections
            ],
        }

    def _extract_predictions(self, detections: list) -> List[Dict[str, Any]]:
        predictions = []
        for det in detections:
            prediction = {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", {}),
            }
            # Keep the tracker-assigned ID so downstream consumers don't
            # fall back to per-frame "untracked_*" placeholder IDs.
            if det.get("track_id") is not None:
                prediction["track_id"] = det["track_id"]
            predictions.append(prediction)
        return predictions

    def _compute_iou(self, box1: Any, box2: Any) -> float:
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

    @staticmethod
    def _is_placeholder_track_id(raw_id: Any) -> bool:
        """Per-frame fallback IDs ("untracked_<frame>_<idx>") that change every frame."""
        return isinstance(raw_id, str) and raw_id.startswith("untracked")

    def _prune_stale_track_merge_state(self, now: float) -> None:
        """Drop canonical tracks idle past the merge window.

        The IoU scan already skips them, so keeping them only grows the
        per-detection scan and memory without bound on long streams.
        Aliases for real tracker IDs are kept so a revived ID still maps
        back to its canonical ID.
        """
        stale = [
            cid
            for cid, info in self._canonical_tracks.items()
            if now - info["last_update"] > self._track_merge_time_window
        ]
        for cid in stale:
            del self._canonical_tracks[cid]

    def _merge_or_register_track(self, raw_id: Any, bbox: Any) -> Any:
        if raw_id is None or bbox is None:
            return raw_id
        now = time.time()
        is_placeholder = self._is_placeholder_track_id(raw_id)
        if raw_id in self._track_aliases:
            canonical_id = self._track_aliases[raw_id]
            track_info = self._canonical_tracks.get(canonical_id)
            if track_info is not None:
                track_info["last_bbox"] = bbox
                track_info["last_update"] = now
                track_info["raw_ids"].add(raw_id)
            return canonical_id
        for canonical_id, info in self._canonical_tracks.items():
            if now - info["last_update"] > self._track_merge_time_window:
                continue
            iou = self._compute_iou(bbox, info["last_bbox"])
            if iou >= self._track_merge_iou_threshold:
                # Placeholder raw IDs never recur, so storing an alias for
                # each one would grow memory every frame for no benefit.
                if not is_placeholder:
                    self._track_aliases[raw_id] = canonical_id
                    info["raw_ids"].add(raw_id)
                info["last_bbox"] = bbox
                info["last_update"] = now
                return canonical_id
        canonical_id = raw_id
        # Placeholder IDs must never become the permanent canonical ID —
        # mint a stable internal ID instead. Offset keeps it clear of the
        # AdvancedTracker's own integer ID range.
        if is_placeholder:
            self._next_internal_track_id += 1
            canonical_id = self._next_internal_track_id
        else:
            self._track_aliases[raw_id] = canonical_id
        self._canonical_tracks[canonical_id] = {
            "last_bbox": bbox,
            "last_update": now,
            "raw_ids": set() if is_placeholder else {raw_id},
        }
        return canonical_id

    def _get_tracking_start_time(self) -> str:
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        self._tracking_start_time = time.time()
