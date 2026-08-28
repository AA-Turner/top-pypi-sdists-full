import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

try:
    import torch
except ImportError:
    torch = None

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)

# Emotion labels order (must match index_to_category: 0..6)
EMOTION_LABELS = [
    "Surprise",
    "Fear",
    "Disgust",
    "Happiness",
    "Sadness",
    "Anger",
    "Neutral",
]


def _softmax(x: np.ndarray) -> np.ndarray:
    """Softmax over last axis via torch (batch-safe)."""
    t = torch.from_numpy(np.asarray(x, dtype=np.float32))
    if t.dim() == 1:
        t = t.unsqueeze(0)
    return torch.softmax(t, dim=1).cpu().numpy()[0]


def _normalize_predict_output(data: Any) -> Tuple[Any, Optional[Dict[str, int]]]:
    """
    - If data has frame_resolution + detections and detections have predictor_output (7 logits),
      convert to emotion_probs (softmax) and set category from argmax (temporary; smoothing will apply Sadness logic).
    - Returns (processed_data, frame_resolution). processed_data is list of detections or original data; frame_resolution is dict or None.
    """
    frame_resolution = None
    if isinstance(data, dict) and "detections" in data:
        frame_resolution = data.get("frame_resolution")
        detections = data["detections"]
    elif isinstance(data, list):
        detections = data
    else:
        return data, None

    for det in detections:
        if not isinstance(det, dict):
            continue
        # Old MiVolo flow: raw 7 logits in predictor_output → softmax here.
        if "predictor_output" in det:
            logits = np.array(det["predictor_output"], dtype=np.float64)
            if logits.size < 7:
                continue
            logits = logits[:7]
            probs = _softmax(logits)
            det["emotion_probs"] = probs.tolist()
            det["category"] = EMOTION_LABELS[int(np.argmax(probs))]
            continue
        # G7 refactored enrichment (classification0 port): the emotion node already decoded the head, so it
        # carries the winning `label` + the full 7-way `top_k` (probs), not raw logits. Rebuild the
        # emotion_probs vector (ordered by EMOTION_LABELS) from top_k and set category from the winning label,
        # so the downstream smoothing / Sadness-suppression / counting (which key off category+emotion_probs) work.
        top_k = det.get("top_k")
        if top_k:
            probs = [0.0] * len(EMOTION_LABELS)
            for entry in top_k:
                if isinstance(entry, dict) and entry.get("label") in EMOTION_LABELS:
                    probs[EMOTION_LABELS.index(entry["label"])] = float(entry.get("confidence", 0.0) or 0.0)
            det["emotion_probs"] = probs
            det["category"] = (
                EMOTION_LABELS[int(np.argmax(probs))] if any(probs) else det.get("label", det.get("category"))
            )
        elif det.get("label") in EMOTION_LABELS:
            det["category"] = det["label"]

    out_data = detections if isinstance(data, dict) else data
    return out_data, frame_resolution


from dataclasses import dataclass, field  # noqa: E402

from ..core.config import AlertConfig, BaseConfig  # noqa: E402
from ..Trackers import ConfigDrivenTracker, TrackerProfile  # noqa: E402
from ..utils import (  # noqa: E402
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    apply_category_mapping,
    bbox_smoothing,
    filter_by_confidence,
    match_results_structure,
)


@dataclass
class FaceEmotionConfig(BaseConfig):
    """Configuration for Face Emotion detection use case in Face Emotion monitoring."""

    # Smoothing configuration
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # confidence thresholds
    confidence_threshold: float = 0.4

    usecase_categories: List[str] = field(
        default_factory=lambda: [
            "Surprise",
            "Fear",
            "Disgust",
            "Happiness",
            "Sadness",
            "Anger",
            "Neutral",
        ]
    )

    target_categories: List[str] = field(
        default_factory=lambda: [
            "Surprise",
            "Fear",
            "Disgust",
            "Happiness",
            "Sadness",
            "Anger",
            "Neutral",
        ]
    )

    alert_config: Optional[AlertConfig] = None

    # Face size filter: only faces passing this are used in analytics/summary.
    # UI shows all bboxes; labels only for faces passing the filter.
    min_face_width_ratio: float = 0.03  # min width as fraction of frame width (when frame size present)
    min_face_height_ratio: float = 0.05  # min height as fraction of frame height (when frame size present)
    min_face_width_px: int = 35  # when frame size absent: require bbox at least this wide
    min_face_height_px: int = 35  # when frame size absent: require bbox at least this tall

    # Temporal smoothing for emotion predictions per track_id: smooth = current_weight * prob + prev_weight * prev
    emotion_smooth_current_weight: float = 0.3
    emotion_smooth_prev_weight: float = 0.7

    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            0: "Surprise",
            1: "Fear",
            2: "Disgust",
            3: "Happiness",
            4: "Sadness",
            5: "Anger",
            6: "Neutral",
        }
    )


class FaceEmotionUseCase(BaseProcessor):
    # Human-friendly display names for categories
    CATEGORY_DISPLAY = {
        "Surprise": "Surprise",
        "Fear": "Fear",
        "Disgust": "Disgust",
        "Happiness": "Happiness",
        "Sadness": "Sadness",
        "Anger": "Anger",
        "Neutral": "Neutral",
    }

    def __init__(self):
        super().__init__("face_emotion")
        self.category = "general"

        self.CASE_TYPE: Optional[str] = "face_emotion"
        self.CASE_VERSION: Optional[str] = "1.3"

        # List of  categories to track
        self.target_categories = [
            "Surprise",
            "Fear",
            "Disgust",
            "Happiness",
            "Sadness",
            "Anger",
            "Neutral",
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

        # Per-track_id smoothed emotion probabilities for temporal smoothing
        self._emotion_prev_probs: Dict[Any, Optional[np.ndarray]] = {}

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
        if not isinstance(config, FaceEmotionConfig):
            self._debug_elapsed_since(start_time)
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )
        if context is None:
            context = ProcessingContext()

        # Normalize predict.py output: predictor_output (7 logits) -> emotion_probs + category; capture frame_resolution
        data, frame_res_from_data = _normalize_predict_output(data)
        if frame_res_from_data is not None:
            context.frame_resolution = frame_res_from_data

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

        # Temporal smoothing of emotion predictions per track_id
        processed_data = self._apply_emotion_smoothing(processed_data, config)

        # Frame dimensions for face size filter (analytics vs UI label). From stream_info or from predict.py frame_resolution.
        frame_w = 0
        frame_h = 0
        if stream_info:
            res = (
                stream_info.get("input_settings", {}).get("stream_resolution")
                or stream_info.get("stream_resolution")
                or {}
            )
            w, h = res.get("width"), res.get("height")
            if w is not None and h is not None:
                frame_w, frame_h = int(w), int(h)
        if frame_w <= 0 or frame_h <= 0:
            res = getattr(context, "frame_resolution", None)
            if isinstance(res, dict):
                frame_w = int(res.get("width", 0) or 0)
                frame_h = int(res.get("height", 0) or 0)

        # Mark each detection: show_label = True only if face passes size filter
        for det in processed_data:
            det["show_label"] = self._face_passes_size_filter(
                det,
                frame_w,
                frame_h,
                min_width_ratio=config.min_face_width_ratio,
                min_height_ratio=config.min_face_height_ratio,
                min_width_px=config.min_face_width_px,
                min_height_px=config.min_face_height_px,
            )

        # Only detections passing size filter are used for analytics/summary
        processed_data_for_analytics = [d for d in processed_data if d.get("show_label")]

        # Update tracking state for total count per label (analytics only)
        self._update_tracking_state(processed_data_for_analytics)

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

        # Compute summaries and alerts (from filtered detections only)
        counting_summary = self._count_categories(processed_data_for_analytics, config)
        # All detections for UI: every bbox drawn; show_label controls whether label is shown
        counting_summary["detections_for_ui"] = processed_data
        # Add total unique  counts after tracking using only local state
        total_counts = self.get_total_counts()
        counting_summary["total_counts"] = total_counts

        alerts = self._check_alerts(counting_summary, frame_number, config)
        self._extract_predictions(processed_data_for_analytics)
        incidents_list = self._generate_incidents(counting_summary, alerts, config, frame_number, stream_info)
        tracking_stats_list = self._generate_tracking_stats(counting_summary, alerts, config, frame_number, stream_info)
        # business_analytics_list = self._generate_business_analytics(counting_summary, alerts, config, frame_number, stream_info)
        business_analytics_list = []
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

    def _check_alerts(self, summary: dict, frame_number: Any, config: FaceEmotionConfig) -> List[Dict]:
        """
        Check if any alert thresholds are exceeded and return alert dicts.
        """

        def get_trend(data, lookback=900, threshold=0.6):
            """
            Determine if the trend is ascending or descending based on actual value progression.
            Now works with values 0,1,2,3 (not just binary).
            """
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True  # not enough data to determine trend
            increasing = 0
            total = 0
            for i in range(1, len(window)):
                if window[i] >= window[i - 1]:
                    increasing += 1
                total += 1
            ratio = increasing / total
            if ratio >= threshold:
                return True
            elif ratio <= (1 - threshold):
                return False
            return None

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts = []

        if not config.alert_config:
            return alerts

        total = summary.get("total_count", 0)
        # self._ascending_alert_list
        if hasattr(config.alert_config, "count_thresholds") and config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total > threshold:
                    alerts.append(
                        {
                            "alert_type": (
                                getattr(config.alert_config, "alert_type", ["Default"])
                                if hasattr(config.alert_config, "alert_type")
                                else ["Default"]
                            ),
                            "alert_id": "alert_" + category + "_" + frame_key,
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                            "settings": {
                                t: v
                                for t, v in zip(
                                    (
                                        getattr(
                                            config.alert_config,
                                            "alert_type",
                                            ["Default"],
                                        )
                                        if hasattr(config.alert_config, "alert_type")
                                        else ["Default"]
                                    ),
                                    (
                                        getattr(config.alert_config, "alert_value", ["JSON"])
                                        if hasattr(config.alert_config, "alert_value")
                                        else ["JSON"]
                                    ),
                                )
                            },
                        }
                    )
                elif category in summary.get("per_category_count", {}):
                    count = summary.get("per_category_count", {})[category]
                    if count > threshold:  # Fixed logic: alert when EXCEEDING threshold
                        alerts.append(
                            {
                                "alert_type": (
                                    getattr(config.alert_config, "alert_type", ["Default"])
                                    if hasattr(config.alert_config, "alert_type")
                                    else ["Default"]
                                ),
                                "alert_id": "alert_" + category + "_" + frame_key,
                                "incident_category": self.CASE_TYPE,
                                "threshold_level": threshold,
                                "ascending": get_trend(
                                    self._ascending_alert_list,
                                    lookback=900,
                                    threshold=0.8,
                                ),
                                "settings": {
                                    t: v
                                    for t, v in zip(
                                        (
                                            getattr(
                                                config.alert_config,
                                                "alert_type",
                                                ["Default"],
                                            )
                                            if hasattr(config.alert_config, "alert_type")
                                            else ["Default"]
                                        ),
                                        (
                                            getattr(
                                                config.alert_config,
                                                "alert_value",
                                                ["JSON"],
                                            )
                                            if hasattr(config.alert_config, "alert_value")
                                            else ["JSON"]
                                        ),
                                    )
                                },
                            }
                        )
        else:
            pass
        return alerts

    def _generate_incidents(
        self,
        counting_summary: Dict,
        alerts: List,
        config: FaceEmotionConfig,
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

            # Generate human text in new format
            human_text_lines = [f"INCIDENTS DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            human_text = "\n".join(human_text_lines)

            alert_settings = []
            if config.alert_config and hasattr(config.alert_config, "alert_type"):
                alert_settings.append(
                    {
                        "alert_type": (
                            getattr(config.alert_config, "alert_type", ["Default"])
                            if hasattr(config.alert_config, "alert_type")
                            else ["Default"]
                        ),
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
                                (
                                    getattr(config.alert_config, "alert_type", ["Default"])
                                    if hasattr(config.alert_config, "alert_type")
                                    else ["Default"]
                                ),
                                (
                                    getattr(config.alert_config, "alert_value", ["JSON"])
                                    if hasattr(config.alert_config, "alert_value")
                                    else ["JSON"]
                                ),
                            )
                        },
                    }
                )

            event = self.create_incident(
                incident_id=self.CASE_TYPE + "_" + str(frame_number),
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
        alerts: List,
        config: FaceEmotionConfig,
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

        # Prepare detections for UI: all bboxes; show_label = True only for size-passing faces (label shown)
        detections = []
        for detection in counting_summary.get("detections_for_ui", counting_summary.get("detections", [])):
            detection_data = {
                "category": detection.get("category"),
                "bounding_box": detection.get("bounding_box", {}),
                "show_label": detection.get("show_label", True),
            }
            # Include segmentation if available (like in eg.json)
            if detection.get("masks"):
                detection_data["masks"] = detection.get("masks", [])
            if detection.get("segmentation"):
                detection_data["segmentation"] = detection.get("segmentation")
            if detection.get("mask"):
                detection_data["mask"] = detection.get("mask")
            detections.append(detection_data)

        # Build alert_settings array in expected format
        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_settings.append(
                {
                    "alert_type": (
                        getattr(config.alert_config, "alert_type", ["Default"])
                        if hasattr(config.alert_config, "alert_type")
                        else ["Default"]
                    ),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": (
                        config.alert_config.count_thresholds if hasattr(config.alert_config, "count_thresholds") else {}
                    ),
                    "ascending": True,
                    "settings": {
                        t: v
                        for t, v in zip(
                            (
                                getattr(config.alert_config, "alert_type", ["Default"])
                                if hasattr(config.alert_config, "alert_type")
                                else ["Default"]
                            ),
                            (
                                getattr(config.alert_config, "alert_value", ["JSON"])
                                if hasattr(config.alert_config, "alert_value")
                                else ["JSON"]
                            ),
                        )
                    },
                }
            )

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

        tracking_stats.append(tracking_stat)
        return tracking_stats

    def _generate_business_analytics(
        self,
        _counting_summary: Dict,
        _zone_analysis: Dict,
        _config: FaceEmotionConfig,
        _stream_info: Optional[Dict[str, Any]] = None,
        is_empty=True,
    ) -> List[Dict]:
        """Generate standardized business analytics for the agg_summary structure."""
        _ = (_config, _counting_summary, _stream_info, _zone_analysis)
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

    def _apply_emotion_smoothing(
        self,
        processed_data: List[Dict[str, Any]],
        config: "FaceEmotionConfig",
    ) -> List[Dict[str, Any]]:
        """
        Apply temporal smoothing of emotion predictions per track_id.
        smooth = current_weight * prob + prev_weight * prev_probs[track_id]
        Final prediction for that face in that frame is argmax(smooth).
        """
        n_classes = 7
        idx_to_label = config.index_to_category or {}
        labels = [idx_to_label.get(i, str(i)) for i in range(n_classes)]
        label_to_index = {lb: i for i, lb in enumerate(labels)}
        w_cur = config.emotion_smooth_current_weight
        w_prev = config.emotion_smooth_prev_weight

        current_track_ids = set()
        for det in processed_data:
            track_id = det.get("track_id")
            if track_id is None:
                continue
            current_track_ids.add(track_id)

            # Get current-frame probability vector (length n_classes)
            prob = None
            if det.get("emotion_probs") is not None:
                p = np.asarray(det["emotion_probs"], dtype=np.float64)
                if p.size >= n_classes:
                    prob = p[:n_classes].astype(np.float64)
            if prob is None and det.get("probabilities") is not None:
                p = np.asarray(det["probabilities"], dtype=np.float64)
                if p.size >= n_classes:
                    prob = p[:n_classes].astype(np.float64)
            if prob is None:
                # Build from category + confidence (one-hot-like)
                cat = det.get("category", "Neutral")
                idx = label_to_index.get(cat, 6)
                conf = float(det.get("confidence", 1.0))
                prob = np.zeros(n_classes, dtype=np.float64)
                prob[idx] = conf
                remainder = max(0.0, 1.0 - conf) / max(1, n_classes - 1)
                for i in range(n_classes):
                    if i != idx:
                        prob[i] = remainder
                prob = prob / (prob.sum() or 1.0)

            prev = self._emotion_prev_probs.get(track_id)
            if prev is None:
                smooth = np.array(prob, copy=True)
            else:
                smooth = w_cur * prob + w_prev * prev

            self._emotion_prev_probs[track_id] = smooth

            # Sadness-specific logic: only accept Sadness if it is strong and clear
            sad_idx = labels.index("Sadness") if "Sadness" in labels else -1
            sorted_idx = np.argsort(smooth)[::-1]
            top1, top2 = int(sorted_idx[0]), int(sorted_idx[1])
            if sad_idx >= 0 and top1 == sad_idx:
                if smooth[sad_idx] < 0.8 or (smooth[sad_idx] - smooth[top2]) < 0.15:
                    cls = top2  # suppress weak or ambiguous Sadness
                else:
                    cls = sad_idx
            else:
                cls = top1

            det["category"] = labels[cls]
            det["confidence"] = float(smooth[cls])

        # Prune stale track_ids to avoid unbounded memory
        stale_tids = [tid for tid in self._emotion_prev_probs if tid not in current_track_ids]
        for tid in stale_tids:
            del self._emotion_prev_probs[tid]

        return processed_data

    def _bbox_to_xyxy(self, bbox: Any) -> Optional[List[float]]:
        """Convert bbox (dict or list) to [x1, y1, x2, y2]. Returns None if invalid."""
        if bbox is None:
            return None
        if isinstance(bbox, list):
            return bbox[:4] if len(bbox) >= 4 else None
        if isinstance(bbox, dict):
            if "xmin" in bbox:
                return [bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]]
            if "x1" in bbox:
                return [bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]]
            values = [v for v in bbox.values() if isinstance(v, (int, float))]
            return values[:4] if len(values) >= 4 else None
        return None

    def _face_passes_size_filter(
        self,
        det: Dict[str, Any],
        frame_w: int,
        frame_h: int,
        min_width_ratio: float = 0.03,
        min_height_ratio: float = 0.05,
        min_width_px: int = 35,
        min_height_px: int = 35,
    ) -> bool:
        """
        Return True if this face detection should be used in analytics and show a label in UI.
        When frame size is present: pass if NOT (width < ratio*w and height < ratio*h).
        When frame size is absent: pass if bbox is at least min_width_px x min_height_px.

        Handles both absolute-pixel and normalized (0..1) bounding boxes. Normalized
        boxes must NOT be int-truncated (int(0.63) == 0 collapses every box to zero
        width and drops all faces from analytics); they are denormalized with the
        frame size when available, or compared directly against the ratio thresholds
        (a normalized width/height IS its frame fraction) when the frame size is absent.
        """
        bbox = det.get("bounding_box", det.get("bbox"))
        xyxy = self._bbox_to_xyxy(bbox)
        if not xyxy:
            return False
        x1, y1, x2, y2 = (float(v) for v in xyxy)
        w1 = x2 - x1
        h1 = y2 - y1
        if w1 <= 0 or h1 <= 0:
            return False
        # Normalized coords never exceed the unit square; absolute pixel coords do.
        normalized = x2 <= 1.0 and y2 <= 1.0
        if frame_w > 0 and frame_h > 0:
            if normalized:
                w1 *= frame_w
                h1 *= frame_h
            if w1 < min_width_ratio * frame_w and h1 < min_height_ratio * frame_h:
                return False
        elif normalized:
            # No frame size, but normalized w/h are already frame fractions, so the
            # ratio test applies directly (pixel minimums need a frame size we lack).
            if w1 < min_width_ratio and h1 < min_height_ratio:
                return False
        else:
            if w1 < min_width_px or h1 < min_height_px:
                return False
        return True

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

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.target_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            # Propagate canonical ID back to detection so downstream logic uses it
            det["track_id"] = canonical_id

            self._per_category_total_track_ids.setdefault(cat, set()).add(canonical_id)
            self._current_frame_track_ids[cat].add(canonical_id)

    def get_total_counts(self):
        """
        Return total unique track_id count for each category.
        """
        return {cat: len(ids) for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()}

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        """Format timestamp for video chunks (HH:MM:SS.ms format)."""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        """Format timestamp for streams (YYYY:MM:DD HH:MM:SS format)."""
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

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

    def _count_categories(self, detections: list, _config: FaceEmotionConfig) -> dict:
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
