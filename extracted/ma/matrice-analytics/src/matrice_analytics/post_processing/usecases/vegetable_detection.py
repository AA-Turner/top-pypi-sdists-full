import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
    ResultFormat,
)
from ..core.config import AlertConfig, BaseConfig
from ..utils import (
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    apply_category_mapping,
    bbox_smoothing,
    count_objects_by_category,
    filter_by_categories,
    filter_by_confidence,
    match_results_structure,
)


@dataclass
class VegetableDetectionConfig(BaseConfig):
    """Configuration for vegetable detection use case."""

    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.5
    enable_unique_counting: bool = True
    enable_advanced_tracker: bool = True
    enable_simple_tracker: bool = False
    min_hits_for_new_track: int = 3
    target_categories: List[str] = field(
        default_factory=lambda: [
            "avocado",
            "beans",
            "beet",
            "bell pepper",
            "broccoli",
            "brus capusta",
            "cabbage",
            "carrot",
            "cayliflower",
            "celery",
            "corn",
            "cucumber",
            "eggplant",
            "fasol",
            "garlic",
            "hot pepper",
            "onion",
            "peas",
            "potato",
            "pumpkin",
            "rediska",
            "redka",
            "salad",
            "squash-patisson",
            "tomato",
            "vegetable marrow",
        ]
    )
    alert_config: Optional[AlertConfig] = None
    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            0: "avocado",
            1: "beans",
            2: "beet",
            3: "bell pepper",
            4: "broccoli",
            5: "brus capusta",
            6: "cabbage",
            7: "carrot",
            8: "cayliflower",
            9: "celery",
            10: "corn",
            11: "cucumber",
            12: "eggplant",
            13: "fasol",
            14: "garlic",
            15: "hot pepper",
            16: "onion",
            17: "peas",
            18: "potato",
            19: "pumpkin",
            20: "rediska",
            21: "redka",
            22: "salad",
            23: "squash-patisson",
            24: "tomato",
            25: "vegetable marrow",
        }
    )


class VegetableDetectionUseCase(BaseProcessor):
    """Vegetable detection processor for post-processing model outputs."""

    def __init__(self):
        super().__init__("vegetable_detection")
        self.category = "agriculture"
        self.CASE_TYPE: Optional[str] = "vegetable_detection"
        self.CASE_VERSION: Optional[str] = "1.0"
        self.target_categories = [
            "avocado",
            "beans",
            "beet",
            "bell pepper",
            "broccoli",
            "brus capusta",
            "cabbage",
            "carrot",
            "cayliflower",
            "celery",
            "corn",
            "cucumber",
            "eggplant",
            "fasol",
            "garlic",
            "hot pepper",
            "onion",
            "peas",
            "potato",
            "pumpkin",
            "rediska",
            "redka",
            "salad",
            "squash-patisson",
            "tomato",
            "vegetable marrow",
        ]
        self.smoothing_tracker = None
        self.tracker = None
        self._total_frame_counter = 0
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        self._track_merge_iou_threshold: float = 0.05
        self._track_merge_time_window: float = 7.0
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        """Process vegetable detections and generate agg_summary output."""
        processing_start = time.time()

        if not isinstance(config, VegetableDetectionConfig):
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        if isinstance(data, dict) and "detections" in data:
            data = data["detections"]

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold

        processed_data = data
        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(processed_data, config.confidence_threshold)
            self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")

        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)
            self.logger.debug("Applied category mapping")

        if config.target_categories:
            processed_data = filter_by_categories(processed_data, config.target_categories)
            self.logger.debug("Applied target category filtering")

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
            self.logger.debug("Applied bbox smoothing")

        try:
            from ..advanced_tracker import AdvancedTracker
            from ..advanced_tracker.config import TrackerConfig

            if self.tracker is None:
                if config.confidence_threshold is not None:
                    tracker_config = TrackerConfig(
                        track_high_thresh=float(config.confidence_threshold),
                        track_low_thresh=max(0.05, float(config.confidence_threshold) / 2),
                        new_track_thresh=float(config.confidence_threshold),
                    )
                else:
                    tracker_config = TrackerConfig()
                self.tracker = AdvancedTracker(tracker_config)
            processed_data = self.tracker.update(processed_data)
            self.logger.debug("Applied advanced tracking")
        except Exception as e:
            self.logger.warning(f"AdvancedTracker failed: {e}")

        # Minimum consecutive frames before a track is counted as "new"
        try:
            self._min_confirm_frames = max(1, int(getattr(config, "min_hits_for_new_track", 5)))
        except Exception:
            self._min_confirm_frames = 3

        self._update_tracking_state(processed_data)
        self._total_frame_counter += 1

        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        counting_summary = self._count_categories(processed_data)
        total_counts = self.get_total_counts()
        counting_summary["total_counts"] = total_counts

        alerts = self._check_alerts(counting_summary, frame_number, config)
        predictions = self._extract_predictions(processed_data)

        incidents = self._generate_incidents(counting_summary, alerts, config, frame_number, stream_info)
        tracking_stats = self._generate_tracking_stats(counting_summary, alerts, predictions, config, stream_info)
        summary = self._generate_summary(counting_summary, incidents, tracking_stats, alerts)

        agg_summary = self.create_agg_summary(
            frame_number or "current_frame",
            incidents=incidents,
            tracking_stats=tracking_stats,
            business_analytics=[],
            alerts=alerts,
            human_text=summary,
        )

        context.mark_completed()
        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

        result.predictions = predictions
        result.metrics = {
            "category_counts": counting_summary.get("per_category_count", {}),
            "total_count": counting_summary.get("total_count", 0),
            "processing_time": time.time() - processing_start,
            "input_format": input_format.value if isinstance(input_format, ResultFormat) else str(input_format),
        }

        return result

    def _check_alerts(
        self,
        summary: Dict[str, Any],
        frame_number: Any,
        config: VegetableDetectionConfig,
    ) -> List[Dict[str, Any]]:
        alerts: List[Dict[str, Any]] = []
        if not config.alert_config:
            return alerts

        total_count = summary.get("total_count", 0)
        if hasattr(config.alert_config, "count_thresholds") and config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total_count > threshold:
                    alerts.append(
                        self.create_alert_object(
                            alert_type=getattr(config.alert_config, "alert_type", ["Default"])[0],
                            alert_id=f"alert_all_{frame_number}",
                            incident_category=self.CASE_TYPE,
                            threshold_value=threshold,
                            ascending=True,
                            settings={},
                        )
                    )
                else:
                    if summary.get("per_category_count", {}).get(category, 0) > threshold:
                        alerts.append(
                            self.create_alert_object(
                                alert_type=getattr(config.alert_config, "alert_type", ["Default"])[0],
                                alert_id=f"alert_{category}_{frame_number}",
                                incident_category=self.CASE_TYPE,
                                threshold_value=threshold,
                                ascending=True,
                                settings={},
                            )
                        )
        return alerts

    def _generate_incidents(
        self,
        summary: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        config: VegetableDetectionConfig,
        frame_number: Optional[int],
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        if summary.get("total_count", 0) == 0:
            return []

        human_text = (
            f"Vegetable incident: {summary.get('total_count', 0)} detections "
            f"across categories {list(summary.get('per_category_count', {}).keys())}."
        )
        return [
            {
                "incident_id": f"vegetable_detection_{frame_number or 'current'}",
                "incident_type": self.CASE_TYPE,
                "severity_level": "medium" if summary.get("total_count", 0) > 10 else "low",
                "human_text": human_text,
                "alerts": alerts,
            }
        ]

    def _generate_tracking_stats(
        self,
        summary: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        predictions: List[Dict[str, Any]],
        config: VegetableDetectionConfig,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        total_counts = [self.create_count_object(cat, count) for cat, count in summary.get("total_counts", {}).items()]
        current_counts = [
            self.create_count_object(cat, count) for cat, count in summary.get("per_category_count", {}).items()
        ]
        human_text = (
            f"Vegetable tracking: {summary.get('total_count', 0)} items, "
            f"categories {list(summary.get('per_category_count', {}).keys())}."
        )
        return [
            self.create_tracking_stats(
                total_counts=total_counts,
                current_counts=current_counts,
                detections=predictions,
                human_text=human_text,
                camera_info=self.get_default_camera_info(),
                alerts=alerts,
                alert_settings=[],
                reset_settings=self.get_default_reset_settings(),
                start_time=self.get_high_precision_timestamp(),
                reset_time=self.get_high_precision_timestamp(),
            )
        ]

    def _generate_summary(
        self,
        summary: Dict[str, Any],
        incidents: List[Dict[str, Any]],
        tracking_stats: List[Dict[str, Any]],
        alerts: List[Dict[str, Any]],
    ) -> str:
        lines = [f"Vegetable detection summary: {summary.get('total_count', 0)} total items."]
        if summary.get("per_category_count"):
            lines.append(f"Counts: {summary.get('per_category_count')}")
        if alerts:
            lines.append(f"Alerts: {len(alerts)}")
        return " ".join(lines)

    def _count_categories(self, detections: Any) -> Dict[str, Any]:
        counts = count_objects_by_category(detections)
        return {
            "total_count": sum(counts.values()),
            "per_category_count": counts,
            "detections": [
                {
                    "bounding_box": det.get("bounding_box", det.get("bbox")),
                    "category": det.get("category"),
                    "confidence": det.get("confidence"),
                    "track_id": det.get("track_id"),
                }
                for det in detections
                if isinstance(det, dict)
            ],
        }

    def _extract_predictions(self, detections: Any) -> List[Dict[str, Any]]:
        if isinstance(detections, dict):
            flattened: List[Dict[str, Any]] = []
            for frame_detections in detections.values():
                if isinstance(frame_detections, list):
                    flattened.extend(frame_detections)
            detections = flattened

        return [
            {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", det.get("bbox", {})),
                "track_id": det.get("track_id"),
            }
            for det in detections
            if isinstance(det, dict)
        ]

    def _update_tracking_state(self, detections: Any) -> None:
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        if not hasattr(self, "_consecutive_track_frames"):
            self._consecutive_track_frames = {cat: {} for cat in self.target_categories}
        if not hasattr(self, "_min_confirm_frames"):
            self._min_confirm_frames = 3

        min_hits = max(1, int(getattr(self, "_min_confirm_frames", 3)))

        # ------------------------------------------------------------------
        # 1) Build current frame track ID sets
        # ------------------------------------------------------------------
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._new_track_ids_this_frame = {cat: set() for cat in self.target_categories}

        for det in detections if isinstance(detections, list) else []:
            if not isinstance(det, dict):
                continue
            cat = det.get("category")
            track_id = det.get("track_id")
            if cat not in self.target_categories or track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(track_id, bbox)
            det["track_id"] = canonical_id
            self._current_frame_track_ids[cat].add(canonical_id)

        # ------------------------------------------------------------------
        # 2) Update consecutive presence counters and derive confirmed tracks
        # ------------------------------------------------------------------
        for cat in self.target_categories:
            current_ids = self._current_frame_track_ids.get(cat, set())
            prev_counts = self._consecutive_track_frames.get(cat, {})
            next_counts: Dict[Any, int] = {}

            # Increment consecutive counts for IDs present this frame
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

            # Promote newly confirmed IDs into cumulative total set
            confirmed_total = self._per_category_total_track_ids.setdefault(cat, set())
            for tid, consec in next_counts.items():
                if consec >= min_hits and tid not in confirmed_total:
                    confirmed_total.add(tid)
                    self._new_track_ids_this_frame[cat].add(tid)

        # Snapshot current -> previous for next call
        self._previous_frame_track_ids = {cat: set(ids) for cat, ids in self._current_frame_track_ids.items()}

    def get_total_counts(self) -> Dict[str, int]:
        return {cat: len(ids) for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()}

    def _compute_iou(self, box1: Any, box2: Any) -> float:
        def _bbox_to_list(bbox: Any) -> List[float]:
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

        area1 = max(0.0, (x1_max - x1_min) * (y1_max - y1_min))
        area2 = max(0.0, (x2_max - x2_min) * (y2_max - y2_min))
        union_area = area1 + area2 - inter_area
        return inter_area / union_area if union_area > 0 else 0.0

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

        for canonical_id, info in self._canonical_tracks.items():
            if now - info["last_update"] > self._track_merge_time_window:
                continue
            if self._compute_iou(bbox, info["last_bbox"]) >= self._track_merge_iou_threshold:
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
