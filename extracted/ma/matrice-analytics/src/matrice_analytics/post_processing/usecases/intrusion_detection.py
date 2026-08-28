"""
Intrusion detection use case implementation.

Production-ready implementation with AdvancedTracker integration, confirmed-new
tracking, proper timestamp handling, track ID normalization, performance logging,
zone-based analysis, and incident manager integration.
"""

import threading
import time
from dataclasses import asdict, replace
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import IntrusionAdvancedTrackerConfig, IntrusionConfig, ZoneConfig
from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..utils import (
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    apply_category_mapping,
    bbox_smoothing,
    calculate_iou,
    count_objects_in_zones,
    filter_by_confidence,
    match_results_structure,
)
from ..utils.geometry_utils import get_bbox_bottom_center, point_in_polygon, to_zone_test_point
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.post_processing_config_client import (
    GEOMETRY_RETRY_INTERVAL,
    PostProcessingConfigClient,
)


class IntrusionUseCase(BaseProcessor):
    """Intrusion Detection use case with zone analysis, alerting, and incident manager."""

    def __init__(self):
        super().__init__("intrusion_detection")
        self.category = "security"
        self.CASE_TYPE: Optional[str] = "intrusion_detection"
        self.CASE_VERSION: Optional[str] = "1.4"
        self.target_categories = ["person"]
        self.smoothing_tracker = None
        self.tracker = None
        self._tracker_seam = None
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        # Post-tracker merge: lower = accept weaker box overlap when mapping flickering raw IDs to canonical IDs.
        self._track_merge_iou_threshold: float = 0.15
        self._track_merge_time_window: float = 8.0
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"
        self.start_timer = None

        # Zone-based tracking storage
        self._zone_current_track_ids: Dict[str, set] = {}
        self._zone_total_track_ids: Dict[str, set] = {}
        self._zone_current_counts: Dict[str, int] = {}
        self._zone_total_counts: Dict[str, int] = {}

        # track_id -> longest continuous in-zone frame count observed for that
        # intruder (persists after they leave). Drives avg/max intrusion time so
        # those metrics reflect ALL intruders' time-in-zone, not just whoever is
        # inside at the current instant. Mirrors dwell_detection._track_dwell_seconds.
        self._intruder_zone_frames: Dict[Any, int] = {}

        # Per-category tracking state
        self._per_category_total_track_ids: Dict[str, set] = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids: Dict[str, set] = {cat: set() for cat in self.target_categories}
        self._previous_frame_track_ids: Dict[str, set] = {cat: set() for cat in self.target_categories}
        self._new_track_ids_this_frame: Dict[str, set] = {}

        # Confirmed-new tracking state
        self._consecutive_track_frames: Dict[str, Dict[Any, int]] = {}
        self._min_confirm_frames: int = 3

        # Incident manager
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._incident_manager_initialized: bool = False

        # Zone temporal stability (aligned with hazard_zone_entry)
        self._zone_inside_frames: Dict[str, Dict[Any, int]] = {}
        self._zone_outside_frames: Dict[str, Dict[Any, int]] = {}
        self._zone_alerted_tracks: Dict[str, set] = {}
        # Sticky intruder labelling: once a track is confirmed an intruder it keeps the
        # "intruder" label until it leaves the frame. Bounded — a track is evicted from
        # the latch after being absent for exit_grace_frames (see _update_zone_tracking),
        # so these dicts never grow without bound during prolonged streaming.
        self._latched_intruder_tracks: Dict[Any, str] = {}   # track_id -> zone_name
        self._latched_absent_frames: Dict[Any, int] = {}     # track_id -> consecutive absent frames
        # Stable incident id for an active intrusion episode.
        self._intrusion_incident_active: bool = False
        self._intrusion_incident_id: str = "intrusion_detection"
        # Snapshot of the last active incident, re-emitted (with a real end_time)
        # on the frame the incident ends so the closing timestamp is surfaced.
        self._intrusion_last_incident: Optional[Dict[str, Any]] = None
        self._frame_intruder_entry_events: List[Dict[str, Any]] = []

        # Matrice alert emission cooldown (count/occupancy alerts; intruder alerts use emit=True).
        # Keyed per logical alert stream (category / zone) so one stream's emission never
        # suppresses another's, and stamped with time.monotonic() so a wall-clock step
        # backwards (NTP correction, VM restore) cannot suppress alerts past the cooldown.
        self._last_matrice_alert_emit_monotonic: Dict[str, float] = {}

        # API-based zone geometry (same flow as hazard_zone_entry)
        self._config_client: Optional[PostProcessingConfigClient] = None
        self._resolved_geometry_cache: Optional[IntrusionConfig] = None
        self._geometry_thread: Optional[threading.Thread] = None
        self._zone_resolution_attempted: bool = False

        # Per-zone parameter overrides (name -> {param: value}), e.g. min_inside_frames,
        # exit_grace_frames. In the UI/API/JSON payload these live *inside* zone_config
        # (sibling of "zones"). Kept on the use case (not on IntrusionConfig, which lives
        # in core/config.py) so the shared config module is not modified. Hoisted from a
        # dict zone_config in process() and from the API in _resolve_geometry_from_api.
        self._zone_params: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------ #
    # API geometry resolution (zones from UI via PostProcessingConfigClient)
    # ------------------------------------------------------------------ #

    def set_config_client(self, client: Optional[PostProcessingConfigClient]) -> None:
        """Set the PostProcessingConfigClient used to resolve zones from API (by_app_deployment, camera_id)."""
        self._config_client = client

    def _start_geometry_resolver(self, config: IntrusionConfig, stream_info: Dict[str, Any]) -> None:
        """Spawn a daemon thread that resolves zone geometry from the API."""
        if self._geometry_thread is not None:
            return

        def _resolver():
            while True:
                try:
                    result = self._resolve_geometry_from_api(config, stream_info)
                    if result is not None:
                        self._resolved_geometry_cache = result
                        self.logger.info("IntrusionDetection: zone geometry resolved from API (background thread)")
                        return
                    self.logger.info(
                        "IntrusionDetection: API geometry returned None, retrying in %ds",
                        GEOMETRY_RETRY_INTERVAL,
                    )
                except Exception as exc:
                    self.logger.warning("IntrusionDetection: background geometry resolve error: %s", exc)
                time.sleep(GEOMETRY_RETRY_INTERVAL)

        t = threading.Thread(target=_resolver, daemon=True, name="intrusion-zone-geometry-resolver")
        self._geometry_thread = t
        t.start()
        self.logger.info("IntrusionDetection: started background zone geometry resolver thread")

    def _resolve_geometry_from_api(
        self,
        config: IntrusionConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[IntrusionConfig]:
        """Resolve zone_config from PostProcessingConfigClient (Matrice post-processing API)."""
        client = self._config_client or (stream_info.get("config_client") if stream_info else None)
        if not client and stream_info:
            try:
                client = PostProcessingConfigClient(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    self.logger.info(
                        "IntrusionDetection: _resolve_geometry_from_api skipped (no config_client; set "
                        "MATRICE_ACCESS_KEY_ID, MATRICE_SECRET_ACCESS_KEY, MATRICE_ACCOUNT_NUMBER "
                        "or call set_config_client() for API zone geometry resolution)"
                    )
                    return None
                self._config_client = client
            except Exception as e:
                self.logger.warning(
                    "IntrusionDetection: _resolve_geometry_from_api could not create config client from env: %s",
                    e,
                )
                return None

        if not stream_info:
            self.logger.info("IntrusionDetection: _resolve_geometry_from_api skipped (no stream_info)")
            return None
        if not client:
            self.logger.info(
                "IntrusionDetection: _resolve_geometry_from_api skipped (no config_client; set "
                "MATRICE_* env or call set_config_client() for API zone geometry resolution)"
            )
            return None

        ids = client.get_stream_identifiers(stream_info)
        app_deployment_id = ids.get("app_deployment_id") or ""
        camera_id = ids.get("camera_id") or ""
        self.logger.info(
            "IntrusionDetection: _resolve_geometry_from_api app_deployment_id=%s camera_id=%s",
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

        # Per-zone params (min_inside_frames, exit_grace_frames, ...) live as a sibling
        # of "zones" inside "zone_config". Store on the use case (IntrusionConfig in
        # core/config.py has no zone_params field and must not be modified).
        zone_params_raw = zone_config_raw.get("zone_params") or {}
        if isinstance(zone_params_raw, dict) and zone_params_raw:
            self._zone_params = {
                str(zn): dict(zp) for zn, zp in zone_params_raw.items() if isinstance(zp, dict)
            }

        self.logger.info(
            "IntrusionDetection: resolved %d zone(s) from API: %s (zone_params: %s)",
            len(zones_dict),
            list(zones_dict.keys()),
            list(self._zone_params.keys()),
        )
        return replace(config, zone_config=new_zone_config)

    # ------------------------------------------------------------------ #
    # Incident Manager                                                    #
    # ------------------------------------------------------------------ #

    def _initialize_incident_manager_once(self, config: IntrusionConfig) -> None:
        """Initialize incident manager ONCE (called on first process() invocation)."""
        if self._incident_manager_initialized:
            return
        try:
            self.logger.info("[INCIDENT_MANAGER] Starting incident manager initialization for intrusion detection...")
            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=self.logger)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            if self._incident_manager:
                self.logger.info("[INCIDENT_MANAGER] Incident manager initialized successfully for intrusion detection")
            else:
                self.logger.warning("[INCIDENT_MANAGER] Incident manager not available, incidents won't be published")
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

    # ------------------------------------------------------------------ #
    # Main process()                                                      #
    # ------------------------------------------------------------------ #

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        processing_start = time.time()

        if not isinstance(config, IntrusionConfig):
            return self.create_error_result(
                "Invalid configuration type for intrusion detection",
                usecase=self.name,
                category=self.category,
                context=context,
            )
        if context is None:
            context = ProcessingContext()

        # Accept zone_config as a raw dict (UI/API/JSON shape: zones + zone_params +
        # unused lines). Normalize it to a ZoneConfig and hoist zone_params onto the
        # use case, so IntrusionConfig in core/config.py is not modified.
        self._normalize_zone_config_and_params(config)

        self._track_merge_iou_threshold = float(config.track_merge_iou_threshold)
        self._track_merge_time_window = float(config.track_merge_time_window_seconds)

        # Zone geometry from API (first frame blocking; background retry on failure — same as hazard_zone_entry)
        if not self._zone_resolution_attempted:
            self._zone_resolution_attempted = True
            if stream_info:
                self.logger.info(
                    "IntrusionDetection: attempting zone geometry resolution from API (first frame, blocking)"
                )
                try:
                    resolved = self._resolve_geometry_from_api(config, stream_info)
                    if resolved is not None:
                        self._resolved_geometry_cache = resolved
                        self.logger.info("IntrusionDetection: zone geometry resolved from API and cached")
                    else:
                        self.logger.warning(
                            "IntrusionDetection: API returned no zone config on first frame; "
                            "starting background retry thread (retrying every %ds). "
                            "Using zone_config from user config file until resolved.",
                            GEOMETRY_RETRY_INTERVAL,
                        )
                        self._start_geometry_resolver(config, stream_info)
                except Exception as exc:
                    self.logger.warning(
                        "IntrusionDetection: zone geometry resolution raised on first frame (%s); "
                        "starting background retry thread (retrying every %ds). "
                        "Using zone_config from user config file until resolved.",
                        exc,
                        GEOMETRY_RETRY_INTERVAL,
                    )
                    self._start_geometry_resolver(config, stream_info)
            else:
                self.logger.info(
                    "IntrusionDetection: no stream_info on first frame; using zone_config from user config file"
                )

        if self._resolved_geometry_cache is not None:
            config = self._resolved_geometry_cache
            self.logger.debug("IntrusionDetection: using API-resolved zone geometry")

        # Initialize incident manager on first call (after zone resolution so config matches API zones when present)
        self._initialize_incident_manager_once(config)

        # If no zones are configured, treat the whole frame as a single "global"
        # secure zone so detection still runs (everyone present is evaluated).
        config = self._apply_global_zone_fallback(config, stream_info)

        has_zones = bool(config.zone_config and config.zone_config.zones)

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        # Confidence filtering
        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, config.confidence_threshold)
        else:
            processed_data = data

        # Category mapping
        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)

        # Category filtering (include "intruder" once temporally confirmed in-zone)
        filter_cats = set(config.person_categories or self.target_categories) | {"intruder"}
        processed_data = [d for d in processed_data if d.get("category") in filter_cats]

        # Track ID normalization
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

        # Bbox smoothing
        if config.enable_smoothing:
            if self.smoothing_tracker is None:
                smoothing_config = BBoxSmoothingConfig(
                    smoothing_algorithm=config.smoothing_algorithm,
                    window_size=config.smoothing_window_size,
                    cooldown_frames=config.smoothing_cooldown_frames,
                    confidence_threshold=config.confidence_threshold or 0.5,
                    confidence_range_factor=config.smoothing_confidence_range_factor,
                    enable_smoothing=True,
                )
                self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
            processed_data = bbox_smoothing(processed_data, self.smoothing_tracker.config, self.smoothing_tracker)

        # Snapshot model boxes before tracker so export cannot include stale tracker ghosts.
        model_input_snapshots = self._snapshot_detections_for_export_filter(processed_data)

        # AdvancedTracker
        if getattr(config, "enable_advanced_tracker", True):
            try:
                if self.tracker is None:
                    # F10b S6/S7 gap closure: this site is bespoke -- config.advanced_tracker_config
                    # (an IntrusionAdvancedTrackerConfig, 14 fields, user-overridable) overrides every
                    # matching field on the DEFAULT profile's own dataclass baseline via **asdict(adv),
                    # reproducing this site's original dataclasses.replace(...) construction exactly.
                    # derive_from_confidence=False is load-bearing: BaseConfig.confidence_threshold
                    # defaults to 0.5 (not None), so the seam's own confidence-derivation step would
                    # otherwise silently overwrite this site's 0.35/0.03/0.25 thresholds.
                    adv = config.advanced_tracker_config or IntrusionAdvancedTrackerConfig()
                    if self._tracker_seam is None:
                        self._tracker_seam = ConfigDrivenTracker()
                    self.tracker = self._tracker_seam.get_shared_tracker(
                        stream_info=stream_info,
                        profile=TrackerProfile.DEFAULT,
                        namespace=True,
                        restore=True,
                        derive_from_confidence=False,
                        **asdict(adv),
                    )
                    self.logger.info("Initialized AdvancedTracker for Intrusion Detection (namespace=seam)")
                processed_data = self.tracker.update(processed_data)
            except Exception as e:
                self.logger.warning(f"AdvancedTracker failed: {e}")
        elif getattr(config, "enable_simple_tracker", False):
            for i, det in enumerate(processed_data):
                if det.get("track_id") is None:
                    det["track_id"] = f"simple_{self._total_frame_counter}_{i}"

        # Confirmed-new tracking config
        try:
            self._min_confirm_frames = max(1, int(getattr(config, "min_hits_for_new_track", 5)))
        except Exception:
            self._min_confirm_frames = 3

        self._update_tracking_state(processed_data, _has_zones=has_zones)
        self._total_frame_counter += 1

        # Frame number extraction
        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        # Counting
        counting_summary = self._count_categories(processed_data, config)
        self._filter_export_detections_to_model_input(counting_summary, model_input_snapshots)
        live_detections = counting_summary.get("detections") or []

        total_counts = self.get_total_counts()
        counting_summary["total_counts"] = total_counts

        # Zone analysis
        zone_analysis = {}
        if has_zones:
            # stream_info threaded through so _is_detection_in_zone can scale a
            # normalized detection point to the zone polygon's pixel space (both
            # are otherwise silently mismatched -- see geometry_utils.to_zone_test_point).
            zone_analysis = count_objects_in_zones(live_detections, config.zone_config.zones, stream_info)
            if zone_analysis:
                # This is the call that actually decides membership on the wire --
                # its return value overwrites every count_objects_in_zones()
                # entry below. stream_info threaded through for the same reason
                # as the count_objects_in_zones call above.
                enhanced = self._update_zone_tracking(
                    zone_analysis, live_detections, config, stream_info
                )
                for zone_name, enhanced_data in enhanced.items():
                    zone_analysis[zone_name] = enhanced_data

        self._rebuild_counting_summary_category_totals(counting_summary)

        # Generate outputs
        alerts = self._check_alerts(counting_summary, zone_analysis, config, frame_number)
        incidents_list = self._generate_incidents(
            counting_summary, zone_analysis, alerts, config, frame_number, stream_info
        )
        tracking_stats_list = self._generate_tracking_stats(
            counting_summary, zone_analysis, config, frame_number, alerts, stream_info
        )
        business_analytics_list = self._generate_business_analytics(
            counting_summary,
            zone_analysis,
            config,
            frame_number,
            stream_info,
            is_empty=True,
        )
        summary_list = self._generate_summary(
            counting_summary,
            incidents_list,
            tracking_stats_list,
            business_analytics_list,
            alerts,
        )

        # Send incident to incident manager
        incidents = incidents_list[0] if incidents_list else {}
        self._send_incident_to_manager(incidents, stream_info, context=context)

        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
        business_analytics = business_analytics_list[0] if business_analytics_list else {}
        summary = summary_list[0] if summary_list else {}

        agg_summary = {
            str(frame_number): {
                "incidents": incidents,
                "tracking_stats": tracking_stats,
                "business_analytics": business_analytics,
                "alerts": alerts,
                "human_text": summary,
            }
        }
        if zone_analysis:
            agg_summary[str(frame_number)]["zone_analysis"] = zone_analysis

        context.mark_completed()
        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )
        proc_time = time.time() - processing_start
        processing_latency_ms = proc_time * 1000.0
        processing_fps = (1.0 / proc_time) if proc_time > 0 else None
        print(
            f"[PERF] F{self._total_frame_counter} | latency={processing_latency_ms:.1f}ms fps={processing_fps:.1f}"
            if processing_fps
            else f"[PERF] F{self._total_frame_counter} | latency={processing_latency_ms:.1f}ms"
        )
        return result

    # ------------------------------------------------------------------ #
    # Tracking state management                                           #
    # ------------------------------------------------------------------ #

    def _update_tracking_state(self, detections: list, _has_zones: bool = False):
        _ = (_has_zones,)
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        if not hasattr(self, "_previous_frame_track_ids"):
            self._previous_frame_track_ids = {cat: set() for cat in self.target_categories}
        if not hasattr(self, "_consecutive_track_frames"):
            self._consecutive_track_frames = {cat: {} for cat in self.target_categories}
        if not hasattr(self, "_min_confirm_frames"):
            self._min_confirm_frames = 3

        min_hits = max(1, int(getattr(self, "_min_confirm_frames", 3)))

        # 1) Build current frame track ID sets
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        missing_track_ids = 0
        allowed_cats = set(self.target_categories) | {"intruder"}
        for det in detections:
            cat = det.get("category")
            if cat not in allowed_cats:
                continue
            raw_tid = det.get("track_id")
            if raw_tid is None:
                missing_track_ids += 1
                continue
            bbox = det.get("bounding_box")
            canonical_tid = self._merge_or_register_track(raw_tid, bbox)
            det["track_id"] = canonical_tid
            self._current_frame_track_ids[cat].add(canonical_tid)

        if missing_track_ids > 0:
            print(
                f"[WARN_TRACKING] F{self._total_frame_counter} | "
                f"{missing_track_ids}/{len(detections)} detections missing track_id!"
            )

        # 2) Update consecutive presence counters and derive total/new
        self._new_track_ids_this_frame = {cat: set() for cat in self.target_categories}

        for cat in self.target_categories:
            current_ids = self._current_frame_track_ids.get(cat, set())
            prev_counts = self._consecutive_track_frames.get(cat, {})
            next_counts: Dict[Any, int] = {}

            for tid in current_ids:
                next_counts[tid] = min(min_hits, prev_counts.get(tid, 0) + 1)

            # Soft decay for IDs not seen this frame
            for tid, prev in prev_counts.items():
                if tid in current_ids:
                    continue
                decayed = max(0, prev - 1)
                if decayed > 0:
                    next_counts[tid] = decayed

            self._consecutive_track_frames[cat] = next_counts

            confirmed_total = self._per_category_total_track_ids.setdefault(cat, set())
            for tid, consec in next_counts.items():
                if consec >= min_hits and tid not in confirmed_total:
                    confirmed_total.add(tid)
                    self._new_track_ids_this_frame[cat].add(tid)

        self._previous_frame_track_ids = {cat: set(ids) for cat, ids in self._current_frame_track_ids.items()}

        # 3) Diagnostics
        person_curr = len(self._current_frame_track_ids.get("person", set()))
        person_new = len(self._new_track_ids_this_frame.get("person", set()))
        person_total = len(self._per_category_total_track_ids.get("person", set()))
        print(
            f"[TRACK] F{self._total_frame_counter} | curr_ids={person_curr} "
            f"confirmed_new={person_new} confirmed_total={person_total} min_hits={min_hits}"
        )

    def get_total_counts(self):
        return {cat: len(ids) for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Get count of CONFIRMED new track IDs reported for the first time this frame."""
        return {cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()}

    def get_current_frame_counts(self) -> Dict[str, int]:
        """Get count of ALL track IDs currently in this frame."""
        return {cat: len(ids) for cat, ids in getattr(self, "_current_frame_track_ids", {}).items()}

    # ------------------------------------------------------------------ #
    # Track merging                                                       #
    # ------------------------------------------------------------------ #

    def _compute_iou(self, box1: Any, box2: Any) -> float:
        if isinstance(box1, dict) and isinstance(box2, dict):
            return calculate_iou(box1, box2)

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
                values = list(bbox.values())
                return values[:4] if len(values) >= 4 else []
            return []

        list1 = _bbox_to_list(box1)
        list2 = _bbox_to_list(box2)
        if len(list1) < 4 or len(list2) < 4:
            return 0.0
        x1_min, y1_min, x1_max, y1_max = list1
        x2_min, y2_min, x2_max, y2_max = list2
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

        # Remove stale canonical tracks
        to_delete = [
            cid
            for cid, info in self._canonical_tracks.items()
            if now - info["last_update"] > self._track_merge_time_window
        ]
        for cid in to_delete:
            del self._canonical_tracks[cid]

        for canonical_id, info in self._canonical_tracks.items():
            time_diff = now - info["last_update"]
            if time_diff > self._track_merge_time_window:
                continue
            prev_bbox = info["last_bbox"]
            if prev_bbox is None or bbox is None:
                continue

            iou = self._compute_iou(bbox, prev_bbox)

            def center(b):
                if isinstance(b, dict):
                    return (
                        (b.get("xmin", 0) + b.get("xmax", 0)) / 2,
                        (b.get("ymin", 0) + b.get("ymax", 0)) / 2,
                    )
                return (0, 0)

            cx1, cy1 = center(prev_bbox)
            cx2, cy2 = center(bbox)
            center_dist = ((cx1 - cx2) ** 2 + (cy1 - cy2) ** 2) ** 0.5

            def area(b):
                if isinstance(b, dict):
                    return abs((b.get("xmax", 0) - b.get("xmin", 0)) * (b.get("ymax", 0) - b.get("ymin", 0)))
                return 0

            a1, a2 = area(prev_bbox), area(bbox)
            size_ratio = min(a1, a2) / max(a1, a2) if max(a1, a2) > 0 else 0

            if iou >= self._track_merge_iou_threshold or (
                center_dist < 50 and size_ratio > 0.45
            ):
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

    # ------------------------------------------------------------------ #
    # Counting                                                            #
    # ------------------------------------------------------------------ #

    def _count_categories(self, detections: list, _config: IntrusionConfig) -> dict:
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
                }
                for det in detections
            ],
        }

    def _extract_predictions(self, detections: list) -> List[Dict[str, Any]]:
        return [
            {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", {}),
            }
            for det in detections
        ]

    # ------------------------------------------------------------------ #
    # Timestamp helpers                                                   #
    # ------------------------------------------------------------------ #

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(float(timestamp), tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format timestamp to YYYY:MM:DD HH:MM:SS."""
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
        _frame_id: Optional[str] = None,
    ) -> str:
        _ = (_frame_id,)
        if not stream_info:
            return "00:00:00.00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
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

    # ------------------------------------------------------------------ #
    # Zone tracking (temporal stability + intruder labeling)
    # ------------------------------------------------------------------ #

    def _snapshot_detections_for_export_filter(self, detections: List[Dict]) -> List[Dict[str, float]]:
        """BBox snapshots from model output before AdvancedTracker (live-input anchor)."""
        snaps: List[Dict[str, float]] = []
        for det in detections or []:
            if not isinstance(det, dict):
                continue
            bb = det.get("bounding_box", det.get("bbox"))
            snap = self._snapshot_bbox(bb)
            if snap is not None:
                snaps.append(snap)
        return snaps

    def _detection_overlaps_model_input(
        self, detection: Dict[str, Any], model_snapshots: List[Dict[str, float]], *, iou_thresh: float = 0.2
    ) -> bool:
        if not model_snapshots:
            return False
        bb = detection.get("bounding_box", detection.get("bbox"))
        if not bb:
            return False
        for snap in model_snapshots:
            if self._compute_iou(bb, snap) >= iou_thresh:
                return True
        return False

    def _filter_export_detections_to_model_input(
        self,
        counting_summary: Dict[str, Any],
        model_snapshots: List[Dict[str, float]],
        *,
        iou_thresh: float = 0.2,
    ) -> None:
        """Export only tracker rows that overlap a current-frame model detection (no ghost boxes)."""
        dets = counting_summary.get("detections")
        if not isinstance(dets, list):
            return
        if not model_snapshots:
            if dets:
                self.logger.debug(
                    "IntrusionDetection: no model detections; clearing %s export rows",
                    len(dets),
                )
            counting_summary["detections"] = []
            return

        live = [
            d
            for d in dets
            if isinstance(d, dict) and self._detection_overlaps_model_input(d, model_snapshots, iou_thresh=iou_thresh)
        ]
        if len(live) < len(dets):
            self.logger.debug(
                "IntrusionDetection: export filter model-anchor %s -> %s (model_boxes=%s)",
                len(dets),
                len(live),
                len(model_snapshots),
            )
        counting_summary["detections"] = live

    @staticmethod
    def _snapshot_bbox(bbox: Any) -> Optional[Dict[str, float]]:
        if not bbox or not isinstance(bbox, dict):
            return None
        xmin = bbox.get("xmin", bbox.get("x1"))
        ymin = bbox.get("ymin", bbox.get("y1"))
        xmax = bbox.get("xmax", bbox.get("x2"))
        ymax = bbox.get("ymax", bbox.get("y2"))
        if xmin is None or ymin is None or xmax is None or ymax is None:
            return None
        return {
            "xmin": float(xmin),
            "ymin": float(ymin),
            "xmax": float(xmax),
            "ymax": float(ymax),
        }

    def _sync_intruder_labels_to_counting_summary(
        self,
        counting_summary: Dict[str, Any],
        processed_data: List[Dict],
    ) -> None:
        """Copy intruder / event markers from live detections into counting_summary copies."""
        by_tid: Dict[Any, Dict] = {}
        for det in processed_data:
            if not isinstance(det, dict):
                continue
            tid = det.get("track_id")
            if tid is not None:
                by_tid[tid] = det
        for cd in counting_summary.get("detections", []) or []:
            if not isinstance(cd, dict):
                continue
            tid = cd.get("track_id")
            src = by_tid.get(tid)
            if not src:
                continue
            if src.get("security_label"):
                cd["security_label"] = src["security_label"]
            if src.get("category") == "intruder":
                cd["category"] = "intruder"
            if src.get("_secure_zone"):
                cd["_secure_zone"] = src["_secure_zone"]
            if src.get("_intruder_event"):
                cd["_intruder_event"] = dict(src["_intruder_event"])

    def _rebuild_counting_summary_category_totals(self, counting_summary: Dict[str, Any]) -> None:
        """Refresh per-category and total counts after intruder relabeling."""
        counts: Dict[str, int] = {}
        for det in counting_summary.get("detections", []) or []:
            if not isinstance(det, dict):
                continue
            cat = det.get("category", "unknown")
            counts[cat] = counts.get(cat, 0) + 1
        counting_summary["per_category_count"] = counts
        counting_summary["total_count"] = sum(counts.values())

    def _primary_alert_type(self, config: IntrusionConfig) -> str:
        at = getattr(config.alert_config, "alert_type", ["Default"]) if config.alert_config else ["Default"]
        if isinstance(at, (list, tuple)) and at:
            return str(at[0])
        return str(at or "Default")

    def _alert_settings_map(self, config: IntrusionConfig) -> Dict[str, Any]:
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
        config: IntrusionConfig,
        *,
        force_emit: bool = False,
        cooldown_key: str = "default",
    ) -> Dict[str, Any]:
        """Add pipe_gas_leak_detection-style fields: status, frames, duration, emit.

        ``cooldown_key`` scopes the emission cooldown to one logical alert stream
        (a category or a zone). It must be stable across frames — do not pass an
        id containing the frame number, or the cooldown never applies.
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

    def _normalize_zone_config_and_params(self, config: IntrusionConfig) -> None:
        """Accept ``zone_config`` as a raw dict and hoist nested ``zone_params``.

        The UI/API/JSON payload nests ``zone_params`` (and an unused ``lines`` key)
        inside ``zone_config`` alongside ``zones``. Since ``IntrusionConfig`` lives in
        core/config.py (which we must not modify) and ``ZoneConfig`` has no
        ``zone_params``, we convert a dict ``zone_config`` to a plain ``ZoneConfig``
        here and store ``zone_params`` on the use case. No-op once already normalized.
        """
        zc = getattr(config, "zone_config", None)
        if isinstance(zc, dict):
            if not self._zone_params:
                nested = zc.get("zone_params", {})
                if isinstance(nested, dict):
                    self._zone_params = {
                        str(zn): dict(zp) for zn, zp in nested.items() if isinstance(zp, dict)
                    }
            config.zone_config = ZoneConfig(
                zones=zc.get("zones", {}) or {},
                zone_confidence_thresholds=zc.get("zone_confidence_thresholds", {}) or {},
                zone_categories=zc.get("zone_categories", {}) or {},
            )

    def _zone_param(self, zone_name: str, key: str, default: Any) -> Any:
        """Return a per-zone override from ``self._zone_params`` or the global default."""
        params = (self._zone_params or {}).get(zone_name)
        if isinstance(params, dict) and key in params:
            return params[key]
        return default

    @staticmethod
    def _frame_dims(stream_info: Optional[Dict[str, Any]]) -> tuple:
        """Best-effort frame (width, height) from stream_info; large fallback box."""
        if isinstance(stream_info, dict):
            candidates = [
                stream_info.get("stream_resolution"),
                (stream_info.get("input_settings") or {}).get("stream_resolution"),
            ]
            for src in candidates:
                if isinstance(src, dict):
                    w = int(src.get("width") or 0)
                    h = int(src.get("height") or 0)
                    if w > 0 and h > 0:
                        return w, h
        return 10000, 10000

    def _apply_global_zone_fallback(
        self, config: IntrusionConfig, stream_info: Optional[Dict[str, Any]]
    ) -> IntrusionConfig:
        """When no zones are configured, treat the whole frame as one ``global`` zone.

        Returns a config whose ``zone_config`` holds a single full-frame ``global``
        polygon, so the existing zone pipeline (counting, tracking, zone_coords)
        runs unchanged. No-op when zones are already configured.
        """
        if config.zone_config and getattr(config.zone_config, "zones", None):
            return config
        w, h = self._frame_dims(stream_info)
        self.logger.info(
            "IntrusionDetection: no zones configured; using full-frame 'global' zone (%dx%d)", w, h
        )
        global_poly = [[0, 0], [w, 0], [w, h], [0, h]]
        return replace(config, zone_config=ZoneConfig(zones={"global": global_poly}))

    def _update_zone_tracking(
        self,
        zone_analysis: Dict[str, Dict[str, int]],
        detections: List[Dict],
        config: IntrusionConfig,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Dict[str, Any]]:
        """Update zone tracking with current frame data.

        This is the code path that actually determines the wire-visible
        ``zone_analysis[...].current_count``/``total_count`` and the
        ``person`` -> ``intruder`` relabeling -- its return value overwrites
        whatever ``count_objects_in_zones`` (module-level, `counting_utils.py`)
        computed at the call site below the count_objects_in_zones call runs
        first only to seed the per-zone dict; this method is the one that
        actually decides membership.

        ``stream_info`` lets a normalized detection point be scaled to match a
        pixel-space zone polygon (``config.zone_config.zones`` resolved via
        ``_resolve_geometry_from_api``'s ``denormalize_config`` call is always
        pixel coordinates) -- see ``geometry_utils.to_zone_test_point``. Optional
        and defaulted so an existing caller that has no stream_info keeps today's
        behaviour rather than raising.
        """
        if not zone_analysis or not config.zone_config or not config.zone_config.zones:
            return {}

        zones = config.zone_config.zones
        enhanced_zone_analysis: Dict[str, Dict[str, Any]] = {}
        current_frame_zone_tracks: Dict[str, set] = {}

        # Global defaults; per-zone overrides come from zone_params (see _zone_param).
        min_inside_global = max(1, int(getattr(config, "min_inside_frames", 3)))
        exit_grace_global = max(1, int(getattr(config, "exit_grace_frames", 3)))

        def _mi(zone_name: str) -> int:
            return max(1, int(self._zone_param(zone_name, "min_inside_frames", min_inside_global)))

        def _eg(zone_name: str) -> int:
            return max(1, int(self._zone_param(zone_name, "exit_grace_frames", exit_grace_global)))

        for zone_name in zones.keys():
            current_frame_zone_tracks[zone_name] = set()
            if zone_name not in self._zone_total_track_ids:
                self._zone_total_track_ids[zone_name] = set()
            if zone_name not in self._zone_alerted_tracks:
                self._zone_alerted_tracks[zone_name] = set()
            if zone_name not in self._zone_inside_frames:
                self._zone_inside_frames[zone_name] = {}
            if zone_name not in self._zone_outside_frames:
                self._zone_outside_frames[zone_name] = {}

        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None:
                continue
            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue
            center_point = get_bbox_bottom_center(bbox)
            # `zone_polygon` is pixel-space (denormalized from the API against the
            # camera's real resolution); `bbox` may be normalized 0-1 (the newer
            # coordinate-frame convention). Scale to match, or this never matches.
            center_point = to_zone_test_point(center_point, bbox, stream_info)

            zones_inside_geom: Set[str] = set()
            for zone_name, zone_polygon in zones.items():
                polygon_points = [(point[0], point[1]) for point in zone_polygon]
                if point_in_polygon(center_point, polygon_points):
                    zones_inside_geom.add(zone_name)

            for zone_name, zone_polygon in zones.items():
                polygon_points = [(point[0], point[1]) for point in zone_polygon]
                inside_geom = zone_name in zones_inside_geom

                if inside_geom:
                    current_frame_zone_tracks[zone_name].add(track_id)

                    prev = self._zone_inside_frames[zone_name].get(track_id, 0)
                    self._zone_inside_frames[zone_name][track_id] = prev + 1
                    self._zone_outside_frames[zone_name].pop(track_id, None)

                    inside_count = self._zone_inside_frames[zone_name][track_id]

                    if inside_count >= _mi(zone_name):
                        detection["category"] = "intruder"
                        detection["security_label"] = "intruder"
                        detection["_secure_zone"] = zone_name

                    if (
                        inside_count == _mi(zone_name)
                        and track_id not in self._zone_alerted_tracks[zone_name]
                        and track_id not in self._latched_intruder_tracks
                    ):
                        detection["_intruder_event"] = {
                            "zone_name": zone_name,
                            "track_id": track_id,
                        }
                else:
                    outside = self._zone_outside_frames[zone_name].get(track_id, 0) + 1
                    self._zone_outside_frames[zone_name][track_id] = outside

                    if outside >= _eg(zone_name) and track_id not in current_frame_zone_tracks[zone_name]:
                        self._zone_inside_frames[zone_name].pop(track_id, None)
                        self._zone_outside_frames[zone_name].pop(track_id, None)
                        self._zone_alerted_tracks[zone_name].discard(track_id)

            confirmed_in_zone = any(
                zn in zones_inside_geom
                and self._zone_inside_frames.get(zn, {}).get(track_id, 0) >= _mi(zn)
                for zn in zones
            )
            if confirmed_in_zone:
                for zn in zones_inside_geom:
                    if self._zone_inside_frames.get(zn, {}).get(track_id, 0) >= _mi(zn):
                        detection["_secure_zone"] = zn
                        self._latched_intruder_tracks[track_id] = zn  # latch on confirmation
                        break
            elif track_id in self._latched_intruder_tracks:
                # STICKY: once an intruder, remain an intruder until the track leaves the
                # frame (even after stepping out of the zone).
                detection["category"] = "intruder"
                detection["security_label"] = "intruder"
                detection["_secure_zone"] = self._latched_intruder_tracks[track_id]
            else:
                detection["category"] = "person"
                detection.pop("security_label", None)
                detection.pop("_secure_zone", None)
                detection.pop("_intruder_event", None)

        # Bounded latch cleanup: evict tracks that have been absent from the frame for
        # exit_grace frames so the latch never grows without bound during long streams.
        current_ids = {
            d.get("track_id") for d in detections if isinstance(d, dict) and d.get("track_id") is not None
        }
        for tid in list(self._latched_intruder_tracks.keys()):
            if tid in current_ids:
                self._latched_absent_frames[tid] = 0
            else:
                absent = self._latched_absent_frames.get(tid, 0) + 1
                self._latched_absent_frames[tid] = absent
                if absent >= exit_grace_global:
                    self._latched_intruder_tracks.pop(tid, None)
                    self._latched_absent_frames.pop(tid, None)
                    for zn in zones:
                        self._zone_inside_frames.get(zn, {}).pop(tid, None)
                        self._zone_outside_frames.get(zn, {}).pop(tid, None)
                        self._zone_alerted_tracks.get(zn, set()).discard(tid)

        for zone_name, zone_counts in zone_analysis.items():
            geom_tracks = current_frame_zone_tracks.get(zone_name, set())
            confirmed_tracks = {
                tid
                for tid in geom_tracks
                if self._zone_inside_frames.get(zone_name, {}).get(tid, 0) >= _mi(zone_name)
            }
            current_tracks = confirmed_tracks
            self._zone_current_track_ids[zone_name] = current_tracks
            self._zone_total_track_ids[zone_name].update(current_tracks)
            self._zone_current_counts[zone_name] = len(current_tracks)
            self._zone_total_counts[zone_name] = len(self._zone_total_track_ids[zone_name])

            # NOTE: the cumulative ``total_track_ids`` list is intentionally NOT
            # emitted — on long-running / crowded live streams it grows without
            # bound and would bloat every frame's output. ``total_count`` (the
            # len of that set) carries the same information in O(1) size. The
            # backing set ``self._zone_total_track_ids`` is still maintained
            # internally to compute that count.
            enhanced_zone_analysis[zone_name] = {
                "current_count": self._zone_current_counts[zone_name],
                "total_count": self._zone_total_counts[zone_name],
                "current_track_ids": list(current_tracks),
                "original_counts": zone_counts,
                "zone_coords": list(zones.get(zone_name, [])),  # pixel polygon
            }

        return enhanced_zone_analysis

    # ------------------------------------------------------------------ #
    # Alerts                                                              #
    # ------------------------------------------------------------------ #

    def _check_alerts(
        self,
        counting_summary: Dict,
        zone_analysis: Dict,
        config: IntrusionConfig,
        frame_number: Any,
    ) -> List[Dict]:
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
            ratio = increasing / total if total else 0.0
            if ratio >= threshold:
                return True
            if ratio <= (1 - threshold):
                return False
            return True

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts: List[Dict[str, Any]] = []

        if config.alert_config:
            settings_map = self._alert_settings_map(config)
            alert_type_str = self._primary_alert_type(config)
        else:
            settings_map = {"Default": "JSON"}
            alert_type_str = "Default"

        min_inside = float(max(1, int(getattr(config, "min_inside_frames", 3))))

        self._frame_intruder_entry_events = []
        for det in counting_summary.get("detections", []) or []:
            evt = det.get("_intruder_event") if isinstance(det, dict) else None
            if not evt:
                continue
            self._frame_intruder_entry_events.append(dict(evt))
            self._zone_alerted_tracks.setdefault(evt["zone_name"], set()).add(evt["track_id"])
            det.pop("_intruder_event", None)

        # Persistent critical alerts per secure zone while confirmed intruder(s) are inside.
        intruder_track_ids_by_zone: Dict[str, List[Any]] = {}
        for det in counting_summary.get("detections", []) or []:
            if not isinstance(det, dict) or det.get("category") != "intruder":
                continue
            zone_name = det.get("_secure_zone")
            if not zone_name:
                continue
            track_id = det.get("track_id")
            bucket = intruder_track_ids_by_zone.setdefault(str(zone_name), [])
            if track_id is not None and track_id not in bucket:
                bucket.append(track_id)

        intruder_zones_alerted: Set[str] = set()
        for zone_name, track_ids in intruder_track_ids_by_zone.items():
            # Stable alert_id per zone (not per frame) so downstream can dedupe one logical intrusion.
            alert = self.create_alert_object(
                alert_type=alert_type_str,
                alert_id=f"intrusion_intruder_{zone_name}",
                incident_category=str(self.CASE_TYPE or "intrusion_detection"),
                threshold_value=min_inside,
                ascending=True,
                settings=settings_map,
            )
            alert["secure_zone"] = zone_name
            alert["security_label"] = "intruder"
            alert["intruder_count"] = len(track_ids)
            alert["intruder_track_ids"] = list(track_ids)
            if track_ids:
                alert["intruder_track_id"] = track_ids[0]
            alert["event_type"] = "intrusion_detection"
            alert["severity_level"] = "critical"
            self._finalize_matrice_alert(alert, frame_number, config, force_emit=True)
            alerts.append(alert)
            intruder_zones_alerted.add(zone_name)

        total_people = counting_summary.get("total_count", 0)

        if not config.alert_config:
            return alerts

        if hasattr(config.alert_config, "count_thresholds") and config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                thr = float(threshold)
                if category == "all" and total_people >= threshold:
                    tr = get_trend(self._ascending_alert_list, lookback=900, threshold=0.8)
                    asc = True if tr is None else bool(tr)
                    alert = self.create_alert_object(
                        alert_type=alert_type_str,
                        alert_id=f"alert_{category}_{frame_key}",
                        incident_category=str(self.CASE_TYPE or "intrusion_detection"),
                        threshold_value=thr,
                        ascending=asc,
                        settings=settings_map,
                    )
                    alerts.append(
                        self._finalize_matrice_alert(
                            alert, frame_number, config, cooldown_key=f"count_{category}"
                        )
                    )
                elif category in counting_summary.get("per_category_count", {}):
                    count = counting_summary["per_category_count"][category]
                    if count >= threshold:
                        tr = get_trend(
                            self._ascending_alert_list,
                            lookback=900,
                            threshold=0.8,
                        )
                        asc = True if tr is None else bool(tr)
                        alert = self.create_alert_object(
                            alert_type=alert_type_str,
                            alert_id=f"alert_{category}_{frame_key}",
                            incident_category=str(self.CASE_TYPE or "intrusion_detection"),
                            threshold_value=thr,
                            ascending=asc,
                            settings=settings_map,
                        )
                        alerts.append(
                            self._finalize_matrice_alert(
                                alert, frame_number, config, cooldown_key=f"count_{category}"
                            )
                        )

        if hasattr(config.alert_config, "occupancy_thresholds") and config.alert_config.occupancy_thresholds:
            for zone_name, threshold in config.alert_config.occupancy_thresholds.items():
                if zone_name in intruder_zones_alerted:
                    continue
                if zone_name not in zone_analysis:
                    continue
                zone_data = zone_analysis[zone_name]
                if isinstance(zone_data, dict) and "current_count" in zone_data:
                    zone_count = zone_data.get("current_count", 0)
                else:
                    zone_count = self._robust_zone_total(zone_data)
                if zone_count >= threshold:
                    tr = get_trend(
                        self._ascending_alert_list,
                        lookback=900,
                        threshold=0.8,
                    )
                    asc = True if tr is None else bool(tr)
                    alert = self.create_alert_object(
                        alert_type=alert_type_str,
                        alert_id=f"alert_zone_{zone_name}_{frame_key}",
                        incident_category=f"{self.CASE_TYPE}_{zone_name}",
                        threshold_value=float(threshold),
                        ascending=asc,
                        settings=settings_map,
                    )
                    alerts.append(
                        self._finalize_matrice_alert(
                            alert, frame_number, config, cooldown_key=f"zone_{zone_name}"
                        )
                    )

        return alerts

    def _robust_zone_total(self, zone_count):
        if isinstance(zone_count, dict):
            total = 0
            for v in zone_count.values():
                if isinstance(v, int):
                    total += v
                elif isinstance(v, list):
                    total += len(v)
            return total
        elif isinstance(zone_count, list):
            return len(zone_count)
        elif isinstance(zone_count, int):
            return zone_count
        return 0

    # ------------------------------------------------------------------ #
    # Incidents                                                           #
    # ------------------------------------------------------------------ #

    def _generate_incidents(
        self,
        counting_summary: Dict,
        zone_analysis: Dict,
        alerts: List,
        config: IntrusionConfig,
        frame_id: Any,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        zone_analysis = zone_analysis or {}
        camera_info = self.get_camera_info_from_stream(stream_info)
        incidents = []
        intruder_now = int((counting_summary.get("per_category_count") or {}).get("intruder", 0) or 0)
        zone_occupied = any(
            isinstance(zd, dict) and int(zd.get("current_count", 0) or 0) > 0
            for zd in zone_analysis.values()
        )
        intrusion_active = intruder_now > 0 or zone_occupied or bool(alerts)
        current_timestamp = self._get_current_timestamp_str(
            stream_info, _frame_id=str(frame_id) if frame_id is not None else None
        )
        self._ascending_alert_list = (
            self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list
        )

        alert_settings = []
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
                    "threshold_value": getattr(config.alert_config, "count_thresholds", None),
                    "ascending": True,
                    "settings": dict(
                        zip(
                            getattr(config.alert_config, "alert_type", ["Default"]),
                            getattr(config.alert_config, "alert_value", ["JSON"]),
                        )
                    ),
                }
            )

        if intrusion_active:
            start_timestamp = self._get_start_timestamp_str(stream_info)
            self._debug_stream_timing("start_timestamp", start_timestamp)
            # While an incident is active, end_time is always "" — the closing timestamp
            # is emitted on the frame the incident ends (see the else branch below).
            self.current_incident_end_timestamp = ""

            level = "critical"
            self._ascending_alert_list.append(3)
            if not self._intrusion_incident_active:
                self._intrusion_incident_active = True
            incident_id = self._intrusion_incident_id

            human_text_lines = [f"INCIDENTS DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            if intruder_now:
                human_text_lines.append(f"\t- Intruder in secure zone(s) now: {intruder_now}")
            if zone_occupied:
                for zn, zd in zone_analysis.items():
                    if isinstance(zd, dict) and int(zd.get("current_count", 0) or 0) > 0:
                        human_text_lines.append(
                            f"\t- Currently inside secure zone '{zn}': {zd.get('current_count', 0)}"
                        )
            if self._frame_intruder_entry_events:
                human_text_lines.append("\t- INTRUSION ENTRY EVENTS (this frame):")
                for evt in self._frame_intruder_entry_events:
                    human_text_lines.append(
                        f"\t\t- Zone: {evt.get('zone_name')} track_id={evt.get('track_id')}"
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
                level_settings={"low": 1, "medium": 3, "significant": 4, "critical": 7},
            )
            # create_incident does `end_time or timestamp`, which would swallow an
            # empty string; force the exact lifecycle value ("" while active).
            event["end_time"] = self.current_incident_end_timestamp
            incidents.append(event)
            # Snapshot so we can emit a closing incident (real end_time) on end.
            self._intrusion_last_incident = dict(event)
        else:
            if self._intrusion_incident_active and self._intrusion_last_incident is not None:
                # Incident just ended this frame: re-emit it with a real end_time.
                closing = dict(self._intrusion_last_incident)
                closing["end_time"] = current_timestamp
                incidents.append(closing)
                self._intrusion_last_incident = None
            else:
                incidents.append({})
            self._intrusion_incident_active = False
            self.current_incident_end_timestamp = "N/A"  # reset lifecycle for the next episode
            self._ascending_alert_list.append(0)

        self._frame_intruder_entry_events = []
        return incidents

    # ------------------------------------------------------------------ #
    # Tracking stats                                                      #
    # ------------------------------------------------------------------ #

    def _generate_tracking_stats(
        self,
        counting_summary: Dict,
        zone_analysis: Dict,
        config: IntrusionConfig,
        frame_number: Any,
        alerts: Any = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        if alerts is None:
            alerts = []
        camera_info = self.get_camera_info_from_stream(stream_info)
        total_detections = counting_summary.get("total_count", 0)
        total_counts_dict = counting_summary.get("total_counts", {})
        per_category_count = counting_summary.get("per_category_count", {})
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        self._debug_stream_timing("start_timestamp", start_timestamp)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        new_counts_dict = self.get_new_counts_this_frame()

        # Detection count by category from raw detections
        raw_detections = counting_summary.get("detections", [])
        detection_count_by_category = {}
        for det in raw_detections:
            cat = det.get("category", "person")
            detection_count_by_category[cat] = detection_count_by_category.get(cat, 0) + 1

        total_counts = [{"category": cat, "count": count} for cat, count in total_counts_dict.items() if count > 0]
        current_counts = [{"category": cat, "count": count} for cat, count in detection_count_by_category.items()]
        if not current_counts and total_detections > 0:
            current_counts = [{"category": cat, "count": count} for cat, count in per_category_count.items()]
        current_new_counts = [{"category": cat, "count": count} for cat, count in new_counts_dict.items()]

        # Stats summary
        curr_total = sum(c.get("count", 0) for c in current_counts)
        new_total = sum(c.get("count", 0) for c in current_new_counts)
        total_total = sum(c.get("count", 0) for c in total_counts)
        print(f"[STATS] F{frame_number} | current={curr_total} new={new_total} total={total_total}")

        if new_total > total_total:
            print(
                f"[BUG_DETECTED] F{frame_number} | new({new_total}) > total({total_total})! "
                f"new_counts_dict={new_counts_dict}, total_counts_dict={total_counts_dict}"
            )

        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "person")
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
                detection_obj = self.create_detection_object(
                    category, bbox, track_id=detection.get("track_id")
                )
            if detection.get("_secure_zone"):
                detection_obj["_secure_zone"] = detection["_secure_zone"]
            if detection.get("security_label"):
                detection_obj["security_label"] = detection["security_label"]
            detections.append(detection_obj)

        alert_settings = []
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
                    "threshold_value": getattr(config.alert_config, "count_thresholds", None),
                    "ascending": True,
                    "settings": dict(
                        zip(
                            getattr(config.alert_config, "alert_type", ["Default"]),
                            getattr(config.alert_config, "alert_value", ["JSON"]),
                        )
                    ),
                }
            )

        human_text_lines = []
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        for cat, count in detection_count_by_category.items():
            new_count = new_counts_dict.get(cat, 0)
            human_text_lines.append(f"\t- Total People in Frame: {count}")
            human_text_lines.append(f"\t- New People (just entered): {new_count}")

        if zone_analysis:
            human_text_lines.append("")
            human_text_lines.append("ZONE ANALYSIS:")
            for zone_name, zone_data in zone_analysis.items():
                if isinstance(zone_data, dict) and "total_count" in zone_data:
                    total_count = zone_data.get("total_count", 0)
                    current_count = zone_data.get("current_count", 0)
                    human_text_lines.append(f"\t- Zone: {zone_name} | current={current_count} total={total_count}")
                else:
                    zone_total = self._robust_zone_total(zone_data)
                    human_text_lines.append(f"\t- Zone: {zone_name} | count={zone_total}")

        human_text_lines.append("")
        human_text = "\n".join(human_text_lines)

        reset_settings = [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]
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
        tracking_stat["current_new_counts"] = current_new_counts
        tracking_stat["total_current_counts"] = current_counts

        # ------------------------------------------------------------------ #
        # VOLUME analytics block (consumed by legacy_analytics_bridge).       #
        # Compact snapshot read directly by the bridge; the six keys match    #
        # intrusion-detection-metrics.json exactly.                           #
        #   people_in_frame            = person + intruder detections now.     #
        #   active_intruders           = intruder (confirmed / latched) now.   #
        #   unique_intruders           = unique tracks ever confirmed in a     #
        #                                secure zone.                          #
        #   intrusion_percentage       = intruder / (person + intruder) * 100. #
        #   avg/max_intrusion_time_seconds = mean / longest time-in-zone across #
        #       ALL intruders this session (per-track longest continuous        #
        #       presence in frames / FPS), so the values stay stable and don't  #
        #       collapse to 0 when the zone is momentarily empty.               #
        # ------------------------------------------------------------------ #
        try:
            fps = int(stream_info.get("input_settings", {}).get("original_fps", 30)) if stream_info else 30
            if fps <= 0:
                fps = 30
        except Exception:
            fps = 30

        person_now = int(per_category_count.get("person", 0))
        intruder_now = int(per_category_count.get("intruder", 0))
        people_now = person_now + intruder_now
        if people_now == 0:
            people_now = int(total_detections)

        unique_intruders = (
            len(set().union(*self._zone_total_track_ids.values())) if self._zone_total_track_ids else 0
        )

        # Update each currently-in-zone intruder's longest continuous presence,
        # retained after they leave so avg/max cover every intruder seen.
        for zn, ids in self._zone_current_track_ids.items():
            frames_map = self._zone_inside_frames.get(zn, {})
            for tid in ids:
                f = int(frames_map.get(tid, 0))
                if f > self._intruder_zone_frames.get(tid, 0):
                    self._intruder_zone_frames[tid] = f
        all_secs = [f / fps for f in self._intruder_zone_frames.values() if f > 0]

        tracking_stat["intrusion_analytics"] = {
            "people_in_frame": int(people_now),
            "active_intruders": int(intruder_now),
            "unique_intruders": int(unique_intruders),
            "intrusion_percentage": (
                round(intruder_now / people_now * 100.0, 2) if people_now > 0 else 0.0
            ),
            "avg_intrusion_time_seconds": (
                round(sum(all_secs) / len(all_secs), 2) if all_secs else 0.0
            ),
            "max_intrusion_time_seconds": round(max(all_secs), 2) if all_secs else 0.0,
        }
        return [tracking_stat]

    # ------------------------------------------------------------------ #
    # Business analytics & summary                                        #
    # ------------------------------------------------------------------ #

    def _generate_business_analytics(
        self,
        _counting_summary: Dict,
        _zone_analysis: Dict,
        _config: IntrusionConfig,
        _frame_id: Any,
        _stream_info: Optional[Dict[str, Any]] = None,
        is_empty=False,
    ) -> List[Dict]:
        _ = (_config, _counting_summary, _frame_id, _stream_info, _zone_analysis)
        if is_empty:
            return []
        return []

    def _generate_summary(
        self,
        _summary: dict,
        incidents: List,
        tracking_stats: List,
        business_analytics: List,
        _alerts: List,
    ) -> List[str]:
        _ = (_alerts, _summary)
        lines = []
        lines.append("Application Name: " + self.CASE_TYPE)
        lines.append("Application Version: " + self.CASE_VERSION)
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

    # ------------------------------------------------------------------ #
    # Utility helpers                                                     #
    # ------------------------------------------------------------------ #

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
