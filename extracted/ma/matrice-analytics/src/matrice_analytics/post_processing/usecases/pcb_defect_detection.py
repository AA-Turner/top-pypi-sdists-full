import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig
from ..Trackers import ConfigDrivenTracker, TrackerProfile  # noqa: E402
from ..utils import (
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    apply_category_mapping,
    bbox_smoothing,
    filter_by_confidence,
    match_results_structure,
)
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory


@dataclass
class PCBDefectConfig(BaseConfig):
    """Configuration for PCB Defect Detection use case."""

    # Smoothing configuration
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # confidence thresholds
    confidence_threshold: float = 0.3

    usecase_categories: List[str] = field(
        default_factory=lambda: [
            "Missing_Hole",
            "MouseBite",
            "Open_Circuit",
            "Short_Circuit",
            "Spur",
            "Spurious_Cooper",
        ]
    )

    target_categories: List[str] = field(
        default_factory=lambda: [
            "Missing_Hole",
            "MouseBite",
            "Open_Circuit",
            "Short_Circuit",
            "Spur",
            "Spurious_Cooper",
        ]
    )

    alert_config: Optional[AlertConfig] = None

    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            0: "Missing_Hole",
            1: "MouseBite",
            2: "Open_Circuit",
            3: "Short_Circuit",
            4: "Spur",
            5: "Spurious_Cooper",
        }
    )


class PCBDefectUseCase(BaseProcessor):
    # Human-friendly display names for categories

    def __init__(self):
        super().__init__("pcb_defect_detection")
        self.category = "manufacturing"

        self.CASE_TYPE: Optional[str] = "pcb_defect_detection"
        self.CASE_VERSION: Optional[str] = "1.2"
        # List of  categories to track
        self.target_categories = [
            "Missing_Hole",
            "MouseBite",
            "Open_Circuit",
            "Short_Circuit",
            "Spur",
            "Spurious_Cooper",
        ]

        # Initialize smoothing tracker
        self.smoothing_tracker = None

        # Initialize advanced tracker (will be created on first use)
        self.tracker = None
        self._tracker_seam = ConfigDrivenTracker()
        # Initialize tracking state variables
        self._total_frame_counter = 0
        self._global_frame_offset = 0

        # Track start time for "TOTAL SINCE" calculation
        self._tracking_start_time = None

        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        # Tunable parameters – adjust if necessary for specific scenarios
        self._track_merge_iou_threshold: float = 0.05  # IoU ≥ 0.05 →
        self._track_merge_time_window: float = 7.0  # seconds within which to merge

        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"
        self.start_timer = None

        # Track IDs seen for the first time in the current frame, per category.
        # Populated by _update_tracking_state; drives current_new_counts.
        self._new_track_ids_this_frame: Dict[str, set] = {cat: set() for cat in self.target_categories}

        # Presence counters backing defect_presence (active frames / frames * 100)
        # and the max_continuous_seconds field of quality_analytics.
        self._active_frames = 0
        self._active_streak = 0
        self._max_active_streak = 0

        # -----------------------------
        # Incident lifecycle (see _generate_incidents)
        # -----------------------------
        self._incident_active = False
        # Stable for the whole episode; the old f"{CASE_TYPE}_{frame_number}" id
        # changed every frame so nothing downstream could ever correlate a close.
        self._incident_id: Optional[str] = None
        # Last active incident, re-emitted once with a real end_time on the frame
        # the episode ends. Without this the close is never published.
        self._last_incident_snapshot: Optional[Dict[str, Any]] = None

        # -----------------------------
        # Incident Manager (see the wiring section below)
        # -----------------------------
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._incident_manager_initialized: bool = False
        # Cameras whose severity thresholds were already registered.
        self._thresholds_registered: set = set()

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        start_time = time.time()
        # Ensure config is correct type
        if not isinstance(config, PCBDefectConfig):
            self._debug_elapsed_since(start_time)
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )
        if context is None:
            context = ProcessingContext()

        # Detect input format and store in context
        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
        else:
            processed_data = data

            self.logger.debug("Did not apply confidence filtering with threshold since nothing was provided")

        # Step 2: Apply category mapping if provided
        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)
            self.logger.debug("Applied category mapping")

        if config.target_categories:
            processed_data = [d for d in processed_data if d.get("category") in self.target_categories]
            self.logger.debug("Applied  category filtering")

        # Apply bbox smoothing if enabled
        if config.enable_smoothing:
            if self.smoothing_tracker is None:
                smoothing_config = BBoxSmoothingConfig(
                    smoothing_algorithm=config.smoothing_algorithm,
                    window_size=config.smoothing_window_size,
                    cooldown_frames=config.smoothing_cooldown_frames,
                    confidence_threshold=config.confidence_threshold,  # Use mask threshold as default
                    confidence_range_factor=config.smoothing_confidence_range_factor,
                    enable_smoothing=True,
                )
                self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
            processed_data = bbox_smoothing(processed_data, self.smoothing_tracker.config, self.smoothing_tracker)

        # Advanced tracking (BYTETracker-like)
        try:
            # Create tracker instance if it doesn't exist (preserves state across frames)
            if self.tracker is None:
                self.tracker = self._tracker_seam.get_shared_tracker(
                    config, stream_info, profile=TrackerProfile.DEFAULT
                )

            # The tracker expects the data in the same format as input
            # It will add track_id and frame_id to each detection
            processed_data = self.tracker.update(processed_data)

        except Exception as e:
            # If advanced tracker fails, fallback to unsmoothed detections
            self.logger.warning(f"AdvancedTracker failed: {e}")

        # Initialize the incident manager once, after config validation.
        self._initialize_incident_manager_once(config)

        # Update  tracking state for total count per label
        self._update_tracking_state(processed_data)

        # Update frame counter
        self._total_frame_counter += 1

        # Presence bookkeeping for defect_presence / max_continuous_seconds.
        # Counted on EVERY frame including idle ones -- _total_frame_counter is
        # the denominator, so skipping idle frames would peg presence at 100%.
        if processed_data:
            self._active_frames += 1
            self._active_streak += 1
            self._max_active_streak = max(self._max_active_streak, self._active_streak)
        else:
            self._active_streak = 0

        # Extract frame information from stream_info
        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            # If start and end frame are the same, it's a single frame
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        # Compute summaries and alerts
        counting_summary = self._count_categories(processed_data, config)
        # Add total unique  counts after tracking using only local state
        total_counts = self.get_total_counts()
        counting_summary["total_counts"] = total_counts

        alerts = self._check_alerts(counting_summary, frame_number, config)
        self._extract_predictions(processed_data)
        incidents_list = self._generate_incidents(counting_summary, alerts, config, frame_number, stream_info)
        tracking_stats_list = self._generate_tracking_stats(counting_summary, alerts, config, frame_number, stream_info)
        business_analytics_list = self._generate_business_analytics(
            counting_summary, alerts, config, stream_info, is_empty=True
        )
        summary_list = self._generate_summary(
            counting_summary,
            incidents_list,
            tracking_stats_list,
            business_analytics_list,
            alerts,
        )

        # Extract frame-based dictionaries from the lists
        incidents = incidents_list[0] if incidents_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
        business_analytics = business_analytics_list[0] if business_analytics_list else {}
        summary = summary_list[0] if summary_list else {}
        # Feed EVERY frame (empty dict included) so the manager can count idle
        # frames and publish the close. Also sets
        # context.metadata["incident_published_via_manager"], which stops the
        # legacy bridge from republishing the same incident under a second id.
        self._send_incident_to_manager(incidents, stream_info, context=context)

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

        # Build result object following the new pattern

        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

        self._debug_elapsed_since(start_time)
        return result

    def _check_alerts(self, summary: dict, frame_number: Any, config) -> List[Dict]:
        """Build canonical alert objects for exceeded count thresholds.

        Alerts are produced by ``BaseProcessor.create_alert_object``, so every
        entry carries the canonical keys -- notably ``threshold_value``, which is
        what ``_build_alert_settings`` reads and what the base helper emits. The
        previous hand-rolled dicts used ``threshold_level`` and a list-valued
        ``alert_type``, so alerts[] and alert_settings[] disagreed on both the
        key name and the value shape.
        """

        def get_trend(data, lookback=900, threshold=0.6):
            """Ascending/descending trend over the recent severity history."""
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True  # not enough data to determine trend
            increasing = sum(1 for i in range(1, len(window)) if window[i] >= window[i - 1])
            total = len(window) - 1
            ratio = increasing / total if total else 1.0
            if ratio >= threshold:
                return True
            if ratio <= (1 - threshold):
                return False
            return None

        alerts: List[Dict] = []
        if not config.alert_config:
            return alerts

        count_thresholds = getattr(config.alert_config, "count_thresholds", None) or {}
        if not count_thresholds:
            return alerts

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alert_types = getattr(config.alert_config, "alert_type", ["Default"]) or ["Default"]
        alert_values = getattr(config.alert_config, "alert_value", ["JSON"]) or ["JSON"]
        settings_map = {t: v for t, v in zip(alert_types, alert_values)}
        ascending = get_trend(self._ascending_alert_list, lookback=900, threshold=0.8)

        total = summary.get("total_count", 0)
        per_category_count = summary.get("per_category_count", {}) or {}

        for category, threshold in count_thresholds.items():
            if category == "all":
                observed = total
            elif category in per_category_count:
                observed = per_category_count[category]
            else:
                continue
            # Fires when the threshold is REACHED, not exceeded. bottle/phone use
            # the same `>=` rule, so all five siblings agree. With `>` a
            # count_threshold of 1 -- the natural setting for a defect count --
            # would need 2 defects before alerting and never fire on a single one.
            if observed < threshold:
                continue
            alerts.append(
                self.create_alert_object(
                    alert_type=alert_types[0],
                    alert_id="alert_" + str(category) + "_" + frame_key,
                    incident_category=self.CASE_TYPE,
                    threshold_value=threshold,
                    ascending=ascending,
                    settings=settings_map,
                )
            )

        return alerts

    def _generate_incidents(
        self,
        counting_summary: Dict,
        alerts: List,
        config: PCBDefectConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        """Generate structured incidents for the output format with frame-based keys."""

        incidents = []
        total_detections = counting_summary.get("total_count", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        self._ascending_alert_list = (
            self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list
        )

        if total_detections > 0:
            # Determine event level based on thresholds
            start_timestamp = self._get_start_timestamp_str(stream_info)
            self._debug_stream_timing("start_timestamp", start_timestamp)

            # end_time is held at "" for the WHOLE active episode; the closing
            # timestamp is emitted once, on the frame the episode ends (else
            # branch below).
            #
            # The previous logic set end_time to a real `current_timestamp` while
            # detections were still arriving, whenever the trailing severity
            # average dipped below 1.5. Any real timestamp is read downstream as
            # "closed" (incident_res_format.is_valid_incident_end_time), so an
            # active incident was being closed mid-episode and then reopened.
            self.current_incident_end_timestamp = ""

            if not self._incident_active:
                self._incident_active = True
                # Stable id for the whole episode -- the old
                # f"{CASE_TYPE}_{frame_number}" changed every frame, so each frame
                # published a brand-new incident that never closed.
                self._incident_id = f"{self.CASE_TYPE}_{uuid.uuid4().hex[:8]}"

            # Reference defect count that maps to full severity. Mirrors
            # pcb-defect.yaml `count_threshold: 15`, and stays defined on both
            # branches so incident_quant can be computed once below.
            threshold_count = 15
            if config.alert_config and config.alert_config.count_thresholds:
                threshold_count = int(config.alert_config.count_thresholds.get("all", 15) or 15)
                intensity = min(10.0, (total_detections / max(1, threshold_count)) * 10)

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

            # Generate human text in new format
            human_text_lines = [f"INCIDENTS DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            human_text = "\n".join(human_text_lines)

            event = self.create_incident(
                incident_id=self._incident_id,
                incident_type=self.CASE_TYPE,
                severity_level=level,
                human_text=human_text,
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=self._build_alert_settings(config, alerts),
                start_time=start_timestamp,
                end_time=self.current_incident_end_timestamp,
                level_settings={"low": 1, "medium": 3, "significant": 4, "critical": 7},
            )
            # create_incident computes `end_time or timestamp`, which turns "" back
            # into start_time -- a real timestamp, i.e. every active frame would
            # look like a close. Force the exact lifecycle value.
            event["end_time"] = self.current_incident_end_timestamp
            # incident_quant on the 0-100 scale the manifest's thresholds use
            # (pcb-defect.yaml: count_based, count_threshold 15), NOT the 0-10
            # `intensity` scale the level bands above were written against.
            event["incident_quant"] = min(100.0, (total_detections / max(1, threshold_count)) * 100.0)
            incidents.append(event)
            # Snapshot so the closing frame can re-emit it with a real end_time.
            self._last_incident_snapshot = dict(event)

        else:
            self._ascending_alert_list.append(0)
            if self._incident_active and self._last_incident_snapshot is not None:
                # Episode just ended: re-emit the last incident ONCE carrying a
                # real end_time. This extra frame is the only thing that ever
                # publishes a closing timestamp -- without it the incident simply
                # stopped appearing in agg_summary and stayed open forever.
                closing = dict(self._last_incident_snapshot)
                closing["end_time"] = current_timestamp
                closing["human_text"] = "PCB defect incident closed"
                incidents.append(closing)
                self._last_incident_snapshot = None
            else:
                incidents.append({})
            self._incident_active = False
            self.current_incident_end_timestamp = "N/A"

        return incidents

    # ============================================================
    # Incident Manager wiring
    #   Follows app-migrations/docs/LEGACY_INCIDENT_USECASE_ADOPTION.md, same
    #   shape as pipe_corrosion_detection / loitering_detection.
    # ============================================================

    # Severity bands against incident_quant (0-100), from app-migrations/quality/pcb-defect/pcb-defect.yaml
    # (incident.incidentTypes). Registered per camera so the manager's severity
    # agrees with the manifest; backend config polling overrides these when present.
    _INCIDENT_THRESHOLDS = (
        {"level": "low", "percentage": 10},
        {"level": "medium", "percentage": 30},
        {"level": "significant", "percentage": 40},
        {"level": "critical", "percentage": 70},
    )

    def _initialize_incident_manager_once(self, config: ConfigProtocol) -> None:
        """Initialize the incident manager ONCE (on first process() invocation)."""
        if self._incident_manager_initialized:
            return
        try:
            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=self.logger)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            if not self._incident_manager:
                self.logger.warning("[INCIDENT_MANAGER] Not available; incidents won't be published")
        except Exception as e:  # pragma: no cover - defensive
            self.logger.error("[INCIDENT_MANAGER] Initialization failed: %s", e, exc_info=True)
        finally:
            self._incident_manager_initialized = True

    @staticmethod
    def _resolve_camera_id(stream_info: Optional[Dict[str, Any]]) -> str:
        """Resolve camera_id from stream_info (camera_info -> top-level -> topic).

        Never hardcode "camera": per-camera manager state keys off this value, so a
        constant would collapse every camera's incident lifecycle into one.
        """
        camera_id = ""
        if stream_info:
            camera_info = stream_info.get("camera_info", {}) or {}
            camera_id = camera_info.get("camera_id", "") or camera_info.get("cameraId", "")
            if not camera_id:
                camera_id = stream_info.get("camera_id", "") or stream_info.get("cameraId", "")
            if not camera_id:
                topic = stream_info.get("topic", "")
                if topic:
                    for suffix in ("_input_topic", "_input-topic"):
                        if suffix in topic:
                            camera_id = topic.split(suffix)[0]
                            break
        return camera_id or "default_camera"

    def _register_incident_thresholds(self, camera_id: str) -> None:
        """Register the manifest severity bands for a camera (once per camera)."""
        if camera_id in self._thresholds_registered:
            return
        self._thresholds_registered.add(camera_id)
        if not self._incident_manager:
            return
        try:
            self._incident_manager.set_thresholds_for_camera(
                camera_id=camera_id,
                thresholds=[dict(b) for b in self._INCIDENT_THRESHOLDS],
                incident_type=self.name,
            )
        except Exception as e:  # pragma: no cover - defensive
            self.logger.warning("[INCIDENT_MANAGER] threshold registration failed: %s", e)

    def _send_incident_to_manager(
        self,
        incident: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]] = None,
        context: Optional[ProcessingContext] = None,
    ) -> None:
        """Feed this frame's incident (or ``{}`` when idle) to the manager.

        ``incident or {}`` goes in on EVERY frame -- including idle ones -- so the
        manager can count empty frames and publish the close event
        (``severity_level: "info"`` + ``end_time``). An early return on an empty
        incident would strand every episode open.

        The context flag is set FIRST and unconditionally: it tells
        ``post_processor._publish_legacy_frame_analytics`` to skip the
        legacy-bridge ``incident_res`` fallback. Without it the bridge profile
        (``publish_incidents=True``) republishes the same incident under a second
        incident_id, producing a double open that never closes.
        """
        if context is not None:
            context.metadata["incident_published_via_manager"] = bool(self._incident_manager)
        if not self._incident_manager:
            return
        camera_id = self._resolve_camera_id(stream_info)
        self._register_incident_thresholds(camera_id)
        try:
            self._incident_manager.process_incident(
                camera_id=camera_id,
                incident_data=incident or {},
                stream_info=stream_info,
            )
        except Exception as e:  # pragma: no cover - defensive
            self.logger.error("[INCIDENT_MANAGER] Error sending incident: %s", e, exc_info=True)

    def _build_alert_settings(self, config: PCBDefectConfig, alerts: List) -> List[Dict[str, Any]]:
        """Canonical ``alert_settings`` entries.

        Mirrors intrusion_detection: prefer the real alert objects when present
        (so the published settings match what actually fired), else fall back to
        the deployment's AlertConfig. Uses ``threshold_value`` -- the key
        ``BaseProcessor.create_alert_object`` emits -- so alerts[] and
        alert_settings[] agree on one spelling.
        """
        if alerts:
            return [
                {
                    "alert_type": a.get("alert_type"),
                    "incident_category": self.CASE_TYPE,
                    "threshold_value": a.get("threshold_value"),
                    "ascending": a.get("ascending", True),
                    "settings": a.get("settings", {}),
                }
                for a in alerts
                if isinstance(a, dict)
            ]
        if config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_types = getattr(config.alert_config, "alert_type", ["Default"]) or ["Default"]
            alert_values = getattr(config.alert_config, "alert_value", ["JSON"]) or ["JSON"]
            return [
                {
                    "alert_type": alert_types,
                    "incident_category": self.CASE_TYPE,
                    "threshold_value": getattr(config.alert_config, "count_thresholds", None),
                    "ascending": True,
                    "settings": {t: v for t, v in zip(alert_types, alert_values)},
                }
            ]
        return []

    def _generate_tracking_stats(
        self,
        counting_summary: Dict,
        alerts: List,
        config: PCBDefectConfig,
        _frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        """Generate structured tracking stats matching eg.json format."""
        _ = (_frame_number,)
        camera_info = self.get_camera_info_from_stream(stream_info)

        # frame_key = str(frame_number) if frame_number is not None else "current_frame"
        # tracking_stats = [{frame_key: []}]
        # frame_tracking_stats = tracking_stats[0][frame_key]
        tracking_stats = []

        total_detections = counting_summary.get("total_count", 0)  # CURRENT total count of all classes
        total_counts_dict = counting_summary.get("total_counts", {})  # TOTAL cumulative counts per class
        per_category_count = counting_summary.get("per_category_count", {})  # CURRENT count per class

        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        self._debug_stream_timing("start_timestamp", start_timestamp)

        # Create high precision timestamps for input_timestamp and reset_timestamp
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        # Build total_counts array in expected format
        total_counts = []
        for cat, count in total_counts_dict.items():
            if count > 0:
                total_counts.append({"category": cat, "count": count})

        # Build current_counts array in expected format
        current_counts = []
        for cat, count in per_category_count.items():
            if count > 0 or total_detections > 0:  # Include even if 0 when there are detections
                current_counts.append({"category": cat, "count": count})

        # current_new_counts: canonical track_ids seen for the FIRST time this
        # frame, per defect type. Emitted for every target category (zeros
        # included) so the bridge's per-category accumulator stays stable and
        # ANALYTICS_WARN stays quiet.
        new_counts_dict = self.get_new_counts_this_frame()
        current_new_counts = [{"category": cat, "count": new_counts_dict.get(cat, 0)} for cat in self.target_categories]

        # Prepare detections without confidence scores (as per eg.json)
        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "person")
            # Include segmentation if available (like in eg.json)
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
            detections.append(detection_obj)

        # Same builder the incident uses, so alerts[] / alert_settings[] carry one
        # spelling of the threshold key across both payloads.
        alert_settings = self._build_alert_settings(config, alerts)

        # Generate human_text in expected format
        human_text_lines = ["Tracking Statistics:"]
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        if total_detections > 0:
            category_counts = [f"{count} {cat}" for cat, count in per_category_count.items()]
            if len(category_counts) == 1:
                detection_text = category_counts[0] + " detected"
            elif len(category_counts) == 2:
                detection_text = f"{category_counts[0]} and {category_counts[1]} detected"
            else:
                detection_text = f"{', '.join(category_counts[:-1])}, and {category_counts[-1]} detected"
            human_text_lines.append(f"\t- {detection_text}")
        else:
            human_text_lines.append("\t- No detections")

        human_text_lines.append(f"TOTAL SINCE {start_timestamp}")
        # `cumulative_total` was undefined here and raised NameError on every
        # frame (the `# noqa: F821` silenced the linter, not the interpreter).
        # The intended value is the sum of cumulative UNIQUE defect track IDs.
        cumulative_total = sum(total_counts_dict.values())
        human_text_lines.append(f"Total Defect Detected:- {cumulative_total}")
        for cat, count in total_counts_dict.items():
            if count > 0:
                human_text_lines.append(f"\t{cat}: {count}")

        if alerts:
            for alert in alerts:
                human_text_lines.append(f"Alerts: {alert.get('settings', {})} sent @ {current_timestamp}")
        else:
            human_text_lines.append("Alerts: None")

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
        # current_new_counts: track_ids seen for the first time this frame.
        tracking_stat["current_new_counts"] = current_new_counts
        # total_current_counts: alias of current_counts, kept because the bridge
        # reads it as an occupancy fallback (legacy_analytics_bridge line ~1197).
        tracking_stat["total_current_counts"] = current_counts
        # Side-channel QUALITY block for legacy_analytics_bridge (results-agg).
        tracking_stat["quality_analytics"] = self._compute_quality_analytics(
            counting_summary.get("detections", []), stream_info
        )

        tracking_stats.append(tracking_stat)
        return tracking_stats

    # ------------------------------------------------------------------ #
    # QUALITY analytics block (results-agg via legacy_analytics_bridge)  #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _get_fps(stream_info: Optional[Dict[str, Any]]) -> float:
        """Stream FPS for frame->seconds conversion; 30.0 when unavailable."""
        if stream_info:
            try:
                fps = (stream_info.get("input_settings", {}) or {}).get("original_fps")
                if fps and float(fps) > 1e-6:
                    return float(fps)
            except (TypeError, ValueError, AttributeError):
                pass
        return 30.0

    def _compute_quality_analytics(
        self, detections: List[Dict[str, Any]], stream_info: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Per-frame QUALITY block stored at ``tracking_stats["quality_analytics"]``.

        Emitted on EVERY frame, including idle ones -- ``total_frames`` is the
        presence denominator, so skipping idle frames would make
        ``defect_presence`` read 100% for any intermittent defect.

        Field set is a SUPERSET of the two existing bridge contracts (pipe family
        ``_ingest_pipe_defect_analytics`` + car damage
        ``_ingest_car_damage_quality``) so one hook can serve this app either
        way. Same contract as bottle / phone-screen / solar.

        Mapping to the manifest metrics (pcb-defect.yaml):
          defect_count       <- union of frame_defect_ids over the window (agg sum)
          total_defect_count <- total_unique_count                       (agg last)
          defect_presence    <- active frames / frames in window * 100    (agg avg)

        All six PCB classes are defect types, so ``total_inspected`` equals
        ``defect_count`` and ``defect_rate`` is pinned at 1.0 -- both are carried
        for contract parity only, which is why the manifest publishes
        ``defect_presence`` as the working denominator instead.

        Unlike every sibling app there is NO bbox merge step here, so
        ``current_count`` is a genuine per-board defect count rather than a merge
        artefact -- it is what backs count_based incident severity.
        """
        defect_ids: set = set()
        defect_count = 0

        for det in detections:
            if det.get("category") not in self.target_categories:
                continue
            defect_count += 1
            tid = det.get("track_id")
            if tid is not None:
                defect_ids.add(tid)

        current_count = len(detections)
        fps = self._get_fps(stream_info)
        frame_seconds = 1.0 / fps
        # Cumulative UNIQUE defect track IDs across all six defect types.
        total_unique = sum(self.get_total_counts().values())
        new_ids_all: set = set()
        for ids in getattr(self, "_new_track_ids_this_frame", {}).values():
            new_ids_all.update(ids)

        return {
            # ---- pipe-family parity fields ----
            "current_count": current_count,
            "total_unique_count": total_unique,
            "frame_new_ids": sorted(new_ids_all),
            "is_active": current_count > 0,
            "frame_seconds": round(frame_seconds, 6),
            "max_continuous_seconds": round(self._max_active_streak * frame_seconds, 3),
            # ---- car-damage / QUALITY-doc parity fields ----
            "defect_count": defect_count,
            "total_inspected": defect_count,
            "defect_rate": 1.0 if defect_count > 0 else 0.0,
            "frame_defect_ids": sorted(defect_ids),
            "frame_inspected_ids": sorted(defect_ids),
            # ---- session-cumulative reference values ----
            "active_frames": self._active_frames,
            "total_frames": self._total_frame_counter,
            "presence_ratio": self._active_frames / max(1, self._total_frame_counter),
            # Per-defect-type breakdown. Not published as metrics today (see the
            # "PER-TYPE BREAKDOWN" note in pcb-defect.yaml) but carried here so a
            # per-type metric can be added in the manifest + resolver without
            # touching this use case again.
            "per_type_new_counts": {
                cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()
            },
            "per_type_total_counts": dict(self.get_total_counts()),
        }

    def _generate_business_analytics(
        self,
        _counting_summary: Dict,
        _alerts: Any,
        _config: PCBDefectConfig,
        _stream_info: Optional[Dict[str, Any]] = None,
        is_empty=False,
    ) -> List[Dict]:
        """Generate standardized business analytics for the agg_summary structure."""
        _ = (_alerts, _config, _counting_summary, _stream_info)
        if is_empty:
            return []

        # -----IF YOUR USECASE NEEDS BUSINESS ANALYTICS, YOU CAN USE THIS FUNCTION------#
        # camera_info = self.get_camera_info_from_stream(stream_info)
        # business_analytics = self.create_business_analytics(nalysis_name, statistics,
        #                          human_text, camera_info=camera_info, alerts=alerts, alert_settings=alert_settings,
        #                          reset_settings)
        # return business_analytics

        return None

    def _generate_summary(
        self,
        _summary: dict,
        incidents: List,
        tracking_stats: List,
        business_analytics: List,
        _alerts: List,
    ) -> List[str]:
        """
        Generate a human_text string for the tracking_stat, incident, business analytics and alerts.
        """
        _ = (_alerts, _summary)
        lines = {}
        lines["Application Name"] = self.CASE_TYPE
        lines["Application Version"] = self.CASE_VERSION
        if len(incidents) > 0:
            lines["Incidents:"] = f"\n\t{incidents[0].get('human_text', 'No incidents detected')}\n"
        if len(tracking_stats) > 0:
            lines["Tracking Statistics:"] = (
                f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}\n"
            )
        if len(business_analytics) > 0:
            lines["Business Analytics:"] = (
                f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}\n"
            )

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines["Summary"] = "No Summary Data"

        return [lines]

    def _get_track_ids_info(self, detections: list) -> Dict[str, Any]:
        """
        Get detailed information about track IDs (per frame).
        """
        # Collect all track_ids in this frame
        frame_track_ids = set()
        for det in detections:
            tid = det.get("track_id")
            if tid is not None:
                frame_track_ids.add(tid)
        # Use persistent total set for unique counting
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

    def _update_tracking_state(self, detections: list):
        """
        Track unique categories track_ids per category for total count after tracking.
        Applies canonical ID merging to avoid duplicate counting when the underlying
        tracker loses an object temporarily and assigns a new ID.

        Also records which canonical IDs were seen for the FIRST time this frame,
        which is what ``current_new_counts`` (and therefore the bridge's
        deduplicated window counts) is built from.
        """
        # Lazily initialise storage dicts
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        new_ids = {cat: set() for cat in self.target_categories}

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.target_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            # Propagate canonical ID back to detection so downstream logic uses it
            det["track_id"] = canonical_id

            seen = self._per_category_total_track_ids.setdefault(cat, set())
            # First-seen check must happen BEFORE the add, or new_ids is always empty.
            if canonical_id not in seen:
                new_ids.setdefault(cat, set()).add(canonical_id)
            seen.add(canonical_id)
            self._current_frame_track_ids[cat].add(canonical_id)

        self._new_track_ids_this_frame = new_ids

    def get_total_counts(self):
        """
        Return total unique track_id count for each category.
        """
        return {cat: len(ids) for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()}

    def get_new_counts_this_frame(self):
        """
        Return the count of track_ids seen for the FIRST time this frame, per category.
        """
        return {cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()}

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp so that exactly two digits follow the decimal point (milliseconds).

        The input can be either:
        1. A numeric Unix timestamp (``float`` / ``int``) – it will first be converted to a
           string in the format ``YYYY-MM-DD-HH:MM:SS.ffffff UTC``.
        2. A string already following the same layout.

        The returned value preserves the overall format of the input but truncates or pads
        the fractional seconds portion to **exactly two digits**.

        Example
        -------
        >>> self._format_timestamp("2025-08-19-04:22:47.187574 UTC")
        '2025-08-19-04:22:47.18 UTC'
        """

        # Convert numeric timestamps to the expected string representation first
        if isinstance(timestamp, (int, float)):
            timestamp = datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        # Ensure we are working with a string from here on
        if not isinstance(timestamp, str):
            return str(timestamp)

        # If there is no fractional component, simply return the original string
        if "." not in timestamp:
            return timestamp

        # Split out the main portion (up to the decimal point)
        main_part, fractional_and_suffix = timestamp.split(".", 1)

        # Separate fractional digits from the suffix (typically ' UTC')
        if " " in fractional_and_suffix:
            fractional_part, suffix = fractional_and_suffix.split(" ", 1)
            suffix = " " + suffix  # Re-attach the space removed by split
        else:
            fractional_part, suffix = fractional_and_suffix, ""

        # Guarantee exactly two digits for the fractional part
        fractional_part = (fractional_part + "00")[:2]

        return f"{main_part}.{fractional_part}{suffix}"

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
                self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
                return self._format_timestamp(self.start_timer)
            elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
                self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
                return self._format_timestamp(self.start_timer)
            else:
                return self._format_timestamp(self.start_timer)

        if self.start_timer is None:
            self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
            return self._format_timestamp(self.start_timer)
        elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
            self.start_timer = stream_info.get("input_settings", {}).get("stream_time", "NA")
            return self._format_timestamp(self.start_timer)

        else:
            if self.start_timer is not None:
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

    def _count_categories(self, detections: list, _config: PCBDefectConfig) -> dict:
        """
        Count the number of detections per category and return a summary dict.
        The detections list is expected to have 'track_id' (from tracker), 'category', 'bounding_box', etc.
        Output structure will include 'track_id' for each detection as per AdvancedTracker output.
        """
        _ = (_config,)
        counts = {}
        for det in detections:
            cat = det.get("category", "unknown")
            counts[cat] = counts.get(cat, 0) + 1
        # Each detection dict will now include 'track_id' (and possibly 'frame_id')
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
        """
        Extract prediction details for output (category, confidence, bounding box).
        """
        return [
            {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", {}),
            }
            for det in detections
        ]

    # ------------------------------------------------------------------ #
    # Canonical ID helpers                                               #
    # ------------------------------------------------------------------ #
    def _compute_iou(self, box1: Any, box2: Any) -> float:
        """Compute IoU between two bounding boxes which may be dicts or lists.
        Falls back to 0 when insufficient data is available."""

        # Helper to convert bbox (dict or list) to [x1, y1, x2, y2]
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
                # Fallback: first four numeric values
                values = [v for v in bbox.values() if isinstance(v, (int, float))]
                return values[:4] if len(values) >= 4 else []
            return []

        l1 = _bbox_to_list(box1)
        l2 = _bbox_to_list(box2)
        if len(l1) < 4 or len(l2) < 4:
            return 0.0
        x1_min, y1_min, x1_max, y1_max = l1
        x2_min, y2_min, x2_max, y2_max = l2

        # Ensure correct order
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
        """Return a stable canonical ID for a raw tracker ID, merging fragmented
        tracks when IoU and temporal constraints indicate they represent the
        same physical."""
        if raw_id is None or bbox is None:
            # Nothing to merge
            return raw_id

        now = time.time()

        # Fast path – raw_id already mapped
        if raw_id in self._track_aliases:
            canonical_id = self._track_aliases[raw_id]
            track_info = self._canonical_tracks.get(canonical_id)
            if track_info is not None:
                track_info["last_bbox"] = bbox
                track_info["last_update"] = now
                track_info["raw_ids"].add(raw_id)
            return canonical_id

        # Attempt to merge with an existing canonical track
        for canonical_id, info in self._canonical_tracks.items():
            # Only consider recently updated tracks
            if now - info["last_update"] > self._track_merge_time_window:
                continue
            iou = self._compute_iou(bbox, info["last_bbox"])
            if iou >= self._track_merge_iou_threshold:
                # Merge
                self._track_aliases[raw_id] = canonical_id
                info["last_bbox"] = bbox
                info["last_update"] = now
                info["raw_ids"].add(raw_id)
                return canonical_id

        # No match – register new canonical track
        canonical_id = raw_id
        self._track_aliases[raw_id] = canonical_id
        self._canonical_tracks[canonical_id] = {
            "last_bbox": bbox,
            "last_update": now,
            "raw_ids": {raw_id},
        }
        return canonical_id
