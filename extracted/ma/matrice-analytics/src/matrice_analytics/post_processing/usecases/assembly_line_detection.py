"""
Assembly Line Detection Use Case

This module provides functionality for detecting assembly lines in images or video streams.

"""

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


@dataclass
class AssemblyLineConfig(BaseConfig):
    """Configuration for assembly line detection use case."""

    # Smoothing configuration
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # confidence thresholds
    confidence_threshold: float = 0.6

    usecase_categories: List[str] = field(
        default_factory=lambda: [
            "metal-plate",
            "robot-arms-2",
            "metal-plate-empty",
            "robot-arms",
            "robot-arms-3",
        ]
    )

    target_categories: List[str] = field(
        default_factory=lambda: [
            "metal-plate",
            "robot-arms-2",
            "metal-plate-empty",
            "robot-arms",
            "robot-arms-3",
        ]
    )

    alert_config: Optional[AlertConfig] = None

    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            0: "metal-plate",
            1: "robot-arms-2",
            2: "metal-plate-empty",
            3: "robot-arms",
            4: "robot-arms-3",
        }
    )


class AssemblyLineUseCase(BaseProcessor):
    # Human-friendly display names for categories
    CATEGORY_DISPLAY = {
        "metal-plate": "Metal Plate",
        "robot-arms-2": "robot-arms-2",
        "metal-plate-empty": "Empty Metal Plate",
        "robot-arms": "robot-arms",
        "robot-arms-3": "robot-arms-3",
    }

    def __init__(self):
        super().__init__("assembly_line_detection")
        self.category = "manufacturing"

        self.CASE_TYPE: Optional[str] = "assembly_line_detection"
        self.CASE_VERSION: Optional[str] = "1.2"

        # List of  categories to track
        self.target_categories = [
            "metal-plate",
            "robot-arms-2",
            "metal-plate-empty",
            "robot-arms",
            "robot-arms-3",
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

        # Track IDs seen for the first time in the current frame, per category.
        # Populated by _update_tracking_state; drives current_new_counts.
        self._new_track_ids_this_frame: Dict[str, set] = {cat: set() for cat in self.target_categories}

    # Domain grouping for the VOLUME metrics declared in
    # app-migrations/volume/assembly-monitoring/assembly-monitoring.yaml.
    # The three robot-arm classes are one physical entity split across three
    # training labels, so they are summed rather than reported separately --
    # per-class arm counts carry no operational meaning (CATEGORY_DISPLAY does
    # not even give robot-arms-2 / robot-arms-3 a human name).
    LOADED_PLATE_CATEGORIES = ("metal-plate",)
    EMPTY_PLATE_CATEGORIES = ("metal-plate-empty",)
    ROBOT_ARM_CATEGORIES = ("robot-arms", "robot-arms-2", "robot-arms-3")

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
        if not isinstance(config, AssemblyLineConfig):
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

        # Update  tracking state for total count per label
        self._update_tracking_state(processed_data)

        # Update frame counter
        self._total_frame_counter += 1

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
        config: AssemblyLineConfig,
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

        # ACTIVITY GATE: configured alerts only.
        # The previous condition was `total_detections > 0`. The robot arms are
        # permanently in frame, so that was true on EVERY frame: one perpetual
        # incident that never closed. Presence is not an incident on a production
        # line -- an alert firing is. With no alert_config nothing is raised,
        # which matches assembly-monitoring.yaml declaring no INCIDENT module.
        total_detections = len(alerts)

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
            # active incident was closed mid-episode and then reopened.
            self.current_incident_end_timestamp = ""

            if not self._incident_active:
                self._incident_active = True
                self._incident_id = f"{self.CASE_TYPE}_{uuid.uuid4().hex[:8]}"

            # Reference count that maps to full severity (line alerts; no INCIDENT module in the manifest yet).
            # Defined on both branches so incident_quant can be computed once below.
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
            # incident_quant on the 0-100 scale the manifest thresholds use, NOT
            # the 0-10 `intensity` scale the level bands above were written against.
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
                closing["human_text"] = "Assembly line incident closed"
                incidents.append(closing)
                self._last_incident_snapshot = None
            else:
                incidents.append({})
            self._incident_active = False
            self.current_incident_end_timestamp = "N/A"

        return incidents

    def _build_alert_settings(self, config, alerts: List) -> List[Dict[str, Any]]:
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
        config: AssemblyLineConfig,
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
        # frame, per class. The bridge sums these into entry_count. Emitted for
        # every target category (zeros included) so the per-category accumulator
        # stays stable and ANALYTICS_WARN stays quiet.
        new_counts_dict = self.get_new_counts_this_frame()
        current_new_counts = [{"category": cat, "count": new_counts_dict.get(cat, 0)} for cat in self.target_categories]

        # Prepare detections without confidence scores (as per eg.json)
        detections = []

        for detection in counting_summary.get("detections", []):
            detection_data = {
                "category": detection.get("category"),
                "bounding_box": detection.get("bounding_box", {}),
            }
            # Include segmentation if available (like in eg.json)
            if detection.get("masks"):
                detection_data["masks"] = detection.get("masks", [])
            if detection.get("segmentation"):
                detection_data["segmentation"] = detection.get("segmentation")
            if detection.get("mask"):
                detection_data["mask"] = detection.get("mask")
            detections.append(detection_data)

        # Same builder the incident uses, so alerts[] / alert_settings[] carry one
        # spelling of the threshold key across both payloads.
        alert_settings = self._build_alert_settings(config, alerts)

        # Generate human_text in expected format
        human_text_lines = ["Tracking Statistics:"]
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}")

        for cat, count in per_category_count.items():
            human_text_lines.append(f"\t{cat}: {count}")

        human_text_lines.append(f"TOTAL SINCE {start_timestamp}")
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
        # Side-channel VOLUME block for legacy_analytics_bridge (results-agg).
        tracking_stat["assembly_analytics"] = self._compute_assembly_analytics(counting_summary.get("detections", []))

        tracking_stats.append(tracking_stat)
        return tracking_stats

    def _generate_business_analytics(
        self,
        _counting_summary: Dict,
        _alerts: Any,
        _config: AssemblyLineConfig,
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
            # First-seen check must happen BEFORE the add, or new_ids is always
            # empty -- and with it plate_throughput, the app's production metric.
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

    # ------------------------------------------------------------------ #
    # VOLUME analytics block (results-agg via legacy_analytics_bridge)   #
    # ------------------------------------------------------------------ #

    def _compute_assembly_analytics(self, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Per-frame VOLUME block stored at ``tracking_stats["assembly_analytics"]``.

        Emitted on EVERY frame, including idle ones, so the bridge's window
        accumulators and denominators stay valid.

        Mapping to the manifest metrics
        (app-migrations/volume/assembly-monitoring/assembly-monitoring.yaml):
          entry_count            <- sum of current_new_counts               (agg sum, native)
          current_occupancy      <- current_counts at window end            (agg last, native)
          plate_throughput       <- union of frame_new_loaded_ids           (agg sum)
          empty_plate_throughput <- union of frame_new_empty_ids            (agg sum)
          line_utilization       <- loaded / (loaded + empty) * 100         (agg avg)
          active_robot_arms      <- max of current_robot_arms in window     (agg max)

        WHY ID LISTS AND NOT COUNTS for the throughput pair: a plate sits in
        frame for many consecutive frames. Shipping a per-frame count would make
        the bridge sum the same plate once per frame; shipping the first-seen
        track_ids lets it union them so each plate counts exactly once per
        window. This is the same reason the pipe family ships ``frame_new_ids``.

        ``line_utilization`` is emitted here as a per-frame convenience value but
        MUST be recomputed by the bridge from the two window-unique throughput
        counts. A per-frame ratio averaged over the window weights a frame
        holding one carrier the same as a frame holding six, and the metric is
        declared ``unit: percent`` (0-100), not a 0-1 ratio.

        ``active_robot_arms`` sums the three robot-arm classes: they are one
        physical entity split across three training labels.
        """
        new_ids = getattr(self, "_new_track_ids_this_frame", {})

        def _new_ids_for(categories):
            out: set = set()
            for cat in categories:
                out.update(new_ids.get(cat, set()))
            return sorted(out)

        def _current_for(categories):
            return sum(1 for d in detections if d.get("category") in categories)

        totals = self.get_total_counts()

        def _total_for(categories):
            return sum(totals.get(cat, 0) for cat in categories)

        frame_new_loaded_ids = _new_ids_for(self.LOADED_PLATE_CATEGORIES)
        frame_new_empty_ids = _new_ids_for(self.EMPTY_PLATE_CATEGORIES)

        current_loaded = _current_for(self.LOADED_PLATE_CATEGORIES)
        current_empty = _current_for(self.EMPTY_PLATE_CATEGORIES)
        current_robot_arms = _current_for(self.ROBOT_ARM_CATEGORIES)

        # Per-frame utilization; see the docstring on why the bridge recomputes it.
        carriers = current_loaded + current_empty
        frame_utilization = (current_loaded / carriers * 100.0) if carriers > 0 else 0.0

        return {
            # Throughput: first-seen track_ids so the bridge can deduplicate.
            "frame_new_loaded_ids": frame_new_loaded_ids,
            "frame_new_empty_ids": frame_new_empty_ids,
            # In-frame counts for the "last"/"max" aggregations.
            "current_loaded_count": current_loaded,
            "current_empty_count": current_empty,
            "current_robot_arms": current_robot_arms,
            "current_total_count": len(detections),
            # Cumulative UNIQUE track IDs since session start.
            "total_unique_loaded": _total_for(self.LOADED_PLATE_CATEGORIES),
            "total_unique_empty": _total_for(self.EMPTY_PLATE_CATEGORIES),
            # Convenience only -- recompute per window in the bridge.
            "frame_line_utilization": round(frame_utilization, 3),
            "is_active": current_loaded > 0,
            "total_frames": self._total_frame_counter,
        }

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
        # is_video_chunk = stream_info.get("input_settings", {}).get("is_video_chunk", False)
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id) / stream_info.get("input_settings", {}).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get("start_frame", 30) / stream_info.get(
                        "input_settings", {}
                    ).get("original_fps", 30)
                stream_time_str = self._format_timestamp_for_video(start_time)
                return stream_time_str
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
            return stream_time_str
        else:
            # For streams, use stream_time from stream_info
            stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
            if stream_time_str:
                # Parse the high precision timestamp string to get timestamp
                try:
                    # Remove " UTC" suffix and parse
                    timestamp_str = stream_time_str.replace(" UTC", "")
                    dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                    return self._format_timestamp_for_stream(timestamp)
                except Exception:
                    # Fallback to current time if parsing fails
                    return self._format_timestamp_for_stream(time.time())
            else:
                return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False) -> str:
        """Get formatted start timestamp for 'TOTAL SINCE' based on stream type."""
        if not stream_info:
            return "00:00:00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                return "00:00:00"
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            # If video format, start from 00:00:00
            return "00:00:00"
        else:
            # For streams, use tracking start time or current time with minutes/seconds reset
            if self._tracking_start_time is None:
                # Try to extract timestamp from stream_time string
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        # Remove " UTC" suffix and parse
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                    except Exception:
                        # Fallback to current time if parsing fails
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()

            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            # Reset minutes and seconds to 00:00 for "TOTAL SINCE" format
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _count_categories(self, detections: list, _config: AssemblyLineConfig) -> dict:
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

    def _format_timestamp(self, timestamp: float) -> str:
        """Format a timestamp for human-readable output."""
        return datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    def _get_tracking_start_time(self) -> str:
        """Get the tracking start time, formatted as a string."""
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        """Set the tracking start time to the current time."""
        self._tracking_start_time = time.time()
