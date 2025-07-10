from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone
import tempfile
import os
import cv2
import numpy as np
from collections import defaultdict
import time
from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol
from ..core.config import BaseConfig, AlertConfig
from ..utils import (
    filter_by_confidence, 
    filter_by_categories, 
    apply_category_mapping, 
    match_results_structure,
    extract_major_colors,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker
)

@dataclass
class FlareAnalysisConfig(BaseConfig):
    """Configuration for flare analysis use case."""
    confidence_threshold: float = 0.5
    top_k_colors: int = 3
    frame_skip: int = 1
    target_categories: List[str] = field(default_factory=lambda: ["BadFlare", "GoodFlare"])
    fps: Optional[float] = None
    bbox_format: str = "auto"
    index_to_category: Dict[int, str] = field(default_factory=lambda: {0: 'BadFlare', 1: 'GoodFlare'})
    alert_config: Optional[AlertConfig] = None
    time_window_minutes: int = 60
    enable_unique_counting: bool = True
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    def validate(self) -> List[str]:
        errors = super().validate()
        if self.confidence_threshold < 0 or self.confidence_threshold > 1:
            errors.append("confidence_threshold must be between 0 and 1")
        if self.top_k_colors <= 0:
            errors.append("top_k_colors must be positive")
        if self.frame_skip <= 0:
            errors.append("frame_skip must be positive")
        if self.bbox_format not in ["auto", "xmin_ymin_xmax_ymax", "x_y_width_height"]:
            errors.append("bbox_format must be one of: auto, xmin_ymin_xmax_ymax, x_y_width_height")
        if self.smoothing_window_size <= 0:
            errors.append("smoothing_window_size must be positive")
        if self.smoothing_cooldown_frames < 0:
            errors.append("smoothing_cooldown_frames cannot be negative")
        if self.smoothing_confidence_range_factor <= 0:
            errors.append("smoothing_confidence_range_factor must be positive")
        return errors

class FlareAnalysisUseCase(BaseProcessor):
    """Flare analysis processor for detecting and analyzing flare colors in video streams."""
    
    def __init__(self):
        super().__init__("flare_analysis")
        self.category = "flare_detection"
        self.tracker = None
        self.smoothing_tracker = None
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._flare_total_track_ids = {}
        self._flare_current_frame_track_ids = {}

    def reset_tracker(self) -> None:
        if self.tracker is not None:
            self.tracker.reset()
            self.logger.info("AdvancedTracker reset for new flare analysis session")

    def reset_flare_tracking(self) -> None:
        self._flare_total_track_ids = {}
        self._flare_current_frame_track_ids = {}
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self.logger.info("Flare tracking state reset")

    def reset_all_tracking(self) -> None:
        self.reset_tracker()
        self.reset_flare_tracking()
        self.logger.info("All flare tracking state reset")

    @staticmethod
    def _iou(bbox1, bbox2):
        if "xmin" in bbox1:
            x1 = max(bbox1["xmin"], bbox2["xmin"])
            y1 = max(bbox1["ymin"], bbox2["ymin"])
            x2 = min(bbox1["xmax"], bbox2["xmax"])
            y2 = min(bbox1["ymax"], bbox2["ymax"])
            area1 = (bbox1["xmax"] - bbox1["xmin"]) * (bbox1["ymax"] - bbox1["ymin"])
            area2 = (bbox2["xmax"] - bbox2["xmin"]) * (bbox2["ymax"] - bbox2["ymin"])
        else:
            x1 = max(bbox1["x"], bbox2["x"])
            y1 = max(bbox1["y"], bbox2["y"])
            x2 = min(bbox1["x"] + bbox1["width"], bbox2["x"] + bbox2["width"])
            y2 = min(bbox1["y"] + bbox1["height"], bbox2["y"] + bbox2["height"])
            area1 = bbox1["width"] * bbox1["height"]
            area2 = bbox2["width"] * bbox2["height"]
        inter_w = max(0, x2 - x1)
        inter_h = max(0, y2 - y1)
        inter_area = inter_w * inter_h
        union = area1 + area2 - inter_area
        return inter_area / union if union > 0 else 0.0

    @staticmethod
    def _deduplicate_detections(detections, iou_thresh=0.7):
        filtered = []
        used = [False] * len(detections)
        for i, det in enumerate(detections):
            if used[i]:
                continue
            group = [i]
            for j in range(i + 1, len(detections)):
                if used[j]:
                    continue
                if det.get("category") == detections[j].get("category"):
                    bbox1 = det.get("bounding_box", det.get("bbox"))
                    bbox2 = detections[j].get("bounding_box", detections[j].get("bbox"))
                    if bbox1 and bbox2 and FlareAnalysisUseCase._iou(bbox1, bbox2) > iou_thresh:
                        used[j] = True
                        group.append(j)
            best_idx = max(group, key=lambda idx: detections[idx].get("confidence", 0))
            filtered.append(detections[best_idx])
            used[best_idx] = True
        return filtered

    def _update_flare_tracking_state(self, detections: List[Dict]):
        self._flare_total_track_ids = getattr(self, '_flare_total_track_ids', defaultdict(set))
        self._flare_current_frame_track_ids = defaultdict(set)
        for det in detections:
            cat = det.get('category')
            color = det.get('main_color')
            track_id = det.get('track_id')
            if cat and color and track_id is not None:
                key = f"{cat}:{color}"
                self._flare_total_track_ids[key].add(track_id)
                self._flare_current_frame_track_ids[key].add(track_id)

    def get_total_flare_counts(self):
        return {key: len(ids) for key, ids in getattr(self, '_flare_total_track_ids', {}).items()}

    def _get_track_ids_info(self, detections: List[Dict]) -> Dict[str, Any]:
        frame_track_ids = set(det.get('track_id') for det in detections if det.get('track_id') is not None)
        total_track_ids = set()
        for s in getattr(self, '_flare_total_track_ids', {}).values():
            total_track_ids.update(s)
        return {
            "total_count": len(total_track_ids),
            "current_frame_count": len(frame_track_ids),
            "total_unique_track_ids": len(total_track_ids),
            "current_frame_track_ids": list(frame_track_ids),
            "last_update_time": time.time(),
            "total_frames_processed": getattr(self, '_total_frame_counter', 0)
        }

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {"type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.5},
                "top_k_colors": {"type": "integer", "minimum": 1, "default": 3},
                "frame_skip": {"type": "integer", "minimum": 1, "default": 1},
                "target_categories": {"type": ["array", "null"], "items": {"type": "string"}, "default": ["BadFlare", "GoodFlare"]},
                "fps": {"type": ["number", "null"], "minimum": 1.0, "default": None},
                "bbox_format": {"type": "string", "enum": ["auto", "xmin_ymin_xmax_ymax", "x_y_width_height"], "default": "auto"},
                "index_to_category": {"type": ["object", "null"], "default": {0: 'BadFlare', 1: 'GoodFlare'}},
                "alert_config": {"type": ["object", "null"], "default": None},
                "time_window_minutes": {"type": "integer", "minimum": 1, "default": 60},
                "enable_unique_counting": {"type": "boolean", "default": True},
                "enable_smoothing": {"type": "boolean", "default": True},
                "smoothing_algorithm": {"type": "string", "default": "observability"},
                "smoothing_window_size": {"type": "integer", "minimum": 1, "default": 20},
                "smoothing_cooldown_frames": {"type": "integer", "minimum": 0, "default": 5},
                "smoothing_confidence_range_factor": {"type": "number", "minimum": 0, "default": 0.5}
            },
            "required": ["confidence_threshold", "top_k_colors"],
            "additionalProperties": False
        }

    def create_default_config(self, **overrides) -> FlareAnalysisConfig:
        defaults = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.5,
            "top_k_colors": 3,
            "frame_skip": 1,
            "target_categories": ["BadFlare", "GoodFlare"],
            "fps": None,
            "bbox_format": "auto",
            "index_to_category": {0: 'BadFlare', 1: 'GoodFlare'},
            "alert_config": None,
            "time_window_minutes": 60,
            "enable_unique_counting": True,
            "enable_smoothing": True,
            "smoothing_algorithm": "observability",
            "smoothing_window_size": 20,
            "smoothing_cooldown_frames": 5,
            "smoothing_confidence_range_factor": 0.5
        }
        defaults.update(overrides)
        return FlareAnalysisConfig(**defaults)

    def process(
        self,
        data: Any, 
        config: ConfigProtocol,
        input_bytes: Optional[bytes] = None,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None
    ) -> ProcessingResult:
        start_time = time.time()
        try:
            if not isinstance(config, FlareAnalysisConfig):
                return self.create_error_result(
                    "Invalid configuration type for flare analysis",
                    usecase=self.name,
                    category=self.category,
                    context=context
                )
            if context is None:
                context = ProcessingContext()
            if not input_bytes:
                return self.create_error_result(
                    "input_bytes (video/image) is required for flare analysis",
                    usecase=self.name,
                    category=self.category,
                    context=context
                )
            if not data:
                return self.create_error_result(
                    "Detection data is required for flare analysis",
                    usecase=self.name,
                    category=self.category,
                    context=context
                )

            input_format = match_results_structure(data)
            context.input_format = input_format
            context.confidence_threshold = config.confidence_threshold
            self.logger.info(f"Processing flare analysis with format: {input_format.value}")

            processed_data = filter_by_confidence(data, config.confidence_threshold)
            if config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
            flare_processed_data = filter_by_categories(processed_data.copy(), config.target_categories)

            # if config.enable_smoothing:
            #     if self.smoothing_tracker is None:
            #         smoothing_config = BBoxSmoothingConfig(
            #             smoothing_algorithm=config.smoothing_algorithm,
            #             window_size=config.smoothing_window_size,
            #             cooldown_frames=config.smoothing_cooldown_frames,
            #             confidence_threshold=config.confidence_threshold,
            #             confidence_range_factor=config.smoothing_confidence_range_factor,
            #             enable_smoothing=True
            #         )
            #         self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
            #     flare_processed_data = bbox_smoothing(flare_processed_data, self.smoothing_tracker.config, self.smoothing_tracker)

            try:
                from ..advanced_tracker import AdvancedTracker
                from ..advanced_tracker.config import TrackerConfig
                if self.tracker is None:
                    tracker_config = TrackerConfig()
                    self.tracker = AdvancedTracker(tracker_config)
                    self.logger.info("Initialized AdvancedTracker for flare analysis tracking")
                flare_processed_data = self.tracker.update(flare_processed_data)
            except Exception as e:
                self.logger.warning(f"AdvancedTracker failed: {e}")

            # flare_processed_data = self._deduplicate_detections(flare_processed_data, iou_thresh=0.7)
            self._update_flare_tracking_state(flare_processed_data)
            self._total_frame_counter += 1

            frame_number = None
            if stream_info:
                input_settings = stream_info.get("input_settings", {})
                start_frame = input_settings.get("start_frame")
                end_frame = input_settings.get("end_frame")
                if start_frame is not None and end_frame is not None and start_frame == end_frame:
                    frame_number = start_frame

            flare_analysis = self._analyze_flares_in_media(flare_processed_data, input_bytes, config)
            flare_summary = self._calculate_flare_summary(flare_analysis, config)
            general_summary = self._calculate_general_summary(processed_data, config)
            flare_summary['total_flare_counts'] = self.get_total_flare_counts()
            insights = self._generate_insights(flare_summary, config)
            alerts = self._check_alerts(flare_summary, config)
            metrics = self._calculate_metrics(flare_analysis, flare_summary, config, context)
            predictions = self._extract_predictions(flare_analysis, config)
            summary = self._generate_summary(flare_summary, general_summary, alerts)

            events_list = self._generate_events(flare_summary, alerts, config, frame_number)
            tracking_stats_list = self._generate_tracking_stats(flare_summary, insights, summary, config, frame_number)
            events = events_list[0] if events_list else {}
            tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}

            context.mark_completed()
            result = self.create_result(
                data={
                    "flare_analysis": flare_analysis,
                    "flare_summary": flare_summary,
                    "general_summary": general_summary,
                    "alerts": alerts,
                    "total_detections": len(flare_analysis),
                    "unique_colors": len(flare_summary.get("color_distribution", {})),
                    "events": events,
                    "tracking_stats": tracking_stats
                },
                usecase=self.name,
                category=self.category,
                context=context
            )
            result.summary = summary
            result.insights = insights
            result.predictions = predictions
            result.metrics = metrics
            if config.confidence_threshold < 0.3:
                result.add_warning(f"Low confidence threshold ({config.confidence_threshold}) may result in false positives")
            processing_time = context.processing_time or time.time() - start_time
            self.logger.info(f"Flare analysis completed in {processing_time:.2f}s")
            return result
        except Exception as e:
            self.logger.error(f"Flare analysis failed: {str(e)}", exc_info=True)
            if context:
                context.mark_completed()
            return self.create_error_result(
                str(e),
                type(e).__name__,
                usecase=self.name,
                category=self.category,
                context=context
            )

    def _is_video_bytes(self, media_bytes: bytes) -> bool:
        video_signatures = [
            b'\x00\x00\x00\x20ftypmp4', b'\x00\x00\x00\x18ftypmp4', b'RIFF', b'\x1aE\xdf\xa3', b'ftyp'
        ]
        for signature in video_signatures:
            if media_bytes.startswith(signature) or signature in media_bytes[:50]:
                return True
        return False

    def _analyze_flares_in_media(self, data: Any, media_bytes: bytes, config: FlareAnalysisConfig) -> List[Dict[str, Any]]:
        is_video = self._is_video_bytes(media_bytes)
        return self._analyze_flares_in_video(data, media_bytes, config) if is_video else self._analyze_flares_in_image(data, media_bytes, config)

    def _analyze_flares_in_video(self, data: Any, video_bytes: bytes, config: FlareAnalysisConfig) -> List[Dict[str, Any]]:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
            temp_video.write(video_bytes)
            video_path = temp_video.name
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise RuntimeError("Failed to open video file")
            fps = config.fps or cap.get(cv2.CAP_PROP_FPS)
            flare_analysis = []
            frame_id = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_id % config.frame_skip != 0:
                    frame_id += 1
                    continue
                frame_key = str(frame_id)
                timestamp = frame_id / fps
                frame_detections = self._get_frame_detections(data, frame_key)
                if not frame_detections:
                    frame_id += 1
                    continue
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                for detection in frame_detections:
                    if detection.get("confidence", 1.0) < config.confidence_threshold:
                        continue
                    bbox = detection.get("bounding_box", detection.get("bbox"))
                    if not bbox:
                        continue
                    crop = self._crop_bbox(rgb_frame, bbox, config.bbox_format)
                    if crop.size == 0:
                        continue
                    major_colors = extract_major_colors(crop, k=config.top_k_colors)
                    main_color = major_colors[0][0] if major_colors else "unknown"
                    flare_record = {
                        "frame_id": frame_key,
                        "timestamp": round(timestamp, 2),
                        "category": detection.get("category", "unknown"),
                        "confidence": round(detection.get("confidence", 0.0), 3),
                        "main_color": main_color,
                        "major_colors": major_colors,
                        "bbox": bbox,
                        "detection_id": detection.get("id", f"det_{len(flare_analysis)}"),
                        "track_id": detection.get("track_id")
                    }
                    flare_analysis.append(flare_record)
                frame_id += 1
            cap.release()
            return flare_analysis
        finally:
            if os.path.exists(video_path):
                os.unlink(video_path)

    def _analyze_flares_in_image(self, data: Any, image_bytes: bytes, config: FlareAnalysisConfig) -> List[Dict[str, Any]]:
        image_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:
            raise RuntimeError("Failed to decode image from bytes")
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        flare_analysis = []
        detections = self._get_frame_detections(data, "0")
        for detection in detections:
            if detection.get("confidence", 1.0) < config.confidence_threshold:
                continue
            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue
            crop = self._crop_bbox(rgb_image, bbox, config.bbox_format)
            if crop.size == 0:
                continue
            major_colors = extract_major_colors(crop, k=config.top_k_colors)
            main_color = major_colors[0][0] if major_colors else "unknown"
            flare_record = {
                "frame_id": "0",
                "timestamp": 0.0,
                "category": detection.get("category", "unknown"),
                "confidence": round(detection.get("confidence", 0.0), 3),
                "main_color": main_color,
                "major_colors": major_colors,
                "bbox": bbox,
                "detection_id": detection.get("id", f"det_{len(flare_analysis)}"),
                "track_id": detection.get("track_id")
            }
            flare_analysis.append(flare_record)
        return flare_analysis

    def _get_frame_detections(self, data: Any, frame_key: str) -> List[Dict[str, Any]]:
        if isinstance(data, dict):
            return data.get(frame_key, [])
        elif isinstance(data, list):
            return data
        return []

    def _crop_bbox(self, image: np.ndarray, bbox: Dict[str, Any], bbox_format: str) -> np.ndarray:
        h, w = image.shape[:2]
        if bbox_format == "auto":
            bbox_format = "xmin_ymin_xmax_ymax" if "xmin" in bbox else "x_y_width_height"
        if bbox_format == "xmin_ymin_xmax_ymax":
            xmin = max(0, int(bbox["xmin"]))
            ymin = max(0, int(bbox["ymin"]))
            xmax = min(w, int(bbox["xmax"]))
            ymax = min(h, int(bbox["ymax"]))
        elif bbox_format == "x_y_width_height":
            xmin = max(0, int(bbox["x"]))
            ymin = max(0, int(bbox["y"]))
            xmax = min(w, int(bbox["x"] + bbox["width"]))
            ymax = min(h, int(bbox["y"] + bbox["height"]))
        else:
            return np.zeros((0, 0, 3), dtype=np.uint8)
        return image[ymin:ymax, xmin:xmax]

    def _calculate_flare_summary(self, flare_analysis: List[Dict], config: FlareAnalysisConfig) -> Dict[str, Any]:
        category_colors = defaultdict(lambda: defaultdict(int))
        total_detections = len(flare_analysis)
        detections = []
        for record in flare_analysis:
            category = record["category"]
            main_color = record["main_color"]
            category_colors[category][main_color] += 1
            detections.append({
                "bounding_box": record["bbox"],
                "category": record["category"],
                "confidence": record["confidence"],
                "track_id": record["track_id"],
                "frame_id": record["frame_id"],
                "main_color": record["main_color"]
            })
        summary = {
            "total_detections": total_detections,
            "categories": dict(category_colors),
            "color_distribution": {},
            "dominant_colors": {},
            "detections": detections
        }
        all_colors = defaultdict(int)
        for category_data in category_colors.values():
            for color, count in category_data.items():
                all_colors[color] += count
        summary["color_distribution"] = dict(all_colors)
        for category, colors in category_colors.items():
            if colors:
                dominant_color = max(colors.items(), key=lambda x: x[1])
                summary["dominant_colors"][category] = {
                    "color": dominant_color[0],
                    "count": dominant_color[1],
                    "percentage": round((dominant_color[1] / sum(colors.values())) * 100, 1)
                }
        return summary

    def _calculate_general_summary(self, processed_data: Any, config: FlareAnalysisConfig) -> Dict[str, Any]:
        category_counts = defaultdict(int)
        total_objects = 0
        if isinstance(processed_data, dict):
            for frame_data in processed_data.values():
                if isinstance(frame_data, list):
                    for detection in frame_data:
                        if detection.get("confidence", 1.0) >= config.confidence_threshold:
                            category = detection.get("category", "unknown")
                            category_counts[category] += 1
                            total_objects += 1
        elif isinstance(processed_data, list):
            for detection in processed_data:
                if detection.get("confidence", 1.0) >= config.confidence_threshold:
                    category = detection.get("category", "unknown")
                    category_counts[category] += 1
                    total_objects += 1
        return {
            "total_objects": total_objects,
            "category_counts": dict(category_counts),
            "categories_detected": list(category_counts.keys())
        }

    def _generate_insights(self, flare_summary: Dict, config: FlareAnalysisConfig) -> List[str]:
        insights = []
        total_detections = flare_summary.get("total_detections", 0)
        if total_detections == 0:
            insights.append("No flares detected for color analysis.")
            return insights
        categories = flare_summary.get("categories", {})
        dominant_colors = flare_summary.get("dominant_colors", {})
        color_distribution = flare_summary.get("color_distribution", {})
        for category, colors in categories.items():
            total = sum(colors.values())
            color_details = ", ".join([f"{color}: {count}" for color, count in colors.items()])
            insights.append(f"{category.capitalize()} colors: {color_details} (Total: {total})")
        for category, info in dominant_colors.items():
            insights.append(
                f"{category.capitalize()} is mostly {info['color']} "
                f"({info['count']} detections, {info['percentage']}%)"
            )
        unique_colors = len(color_distribution)
        if unique_colors > 1:
            insights.append(f"Detected {unique_colors} unique colors across all flare categories.")
        if color_distribution:
            most_common_color = max(color_distribution.items(), key=lambda x: x[1])
            insights.append(
                f"Most common color overall: {most_common_color[0]} ({most_common_color[1]} detections)"
            )
        return insights

    def _check_alerts(self, flare_summary: Dict, config: FlareAnalysisConfig) -> List[Dict]:
        alerts = []
        if not config.alert_config:
            return alerts
        total_detections = flare_summary.get("total_detections", 0)
        if config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total_detections >= threshold:
                    alerts.append({
                        "type": "count_threshold",
                        "severity": "warning",
                        "message": f"Total detections ({total_detections}) exceeds threshold ({threshold})",
                        "category": category,
                        "current_count": total_detections,
                        "threshold": threshold,
                        "timestamp": datetime.now().isoformat()
                    })
                elif category in flare_summary.get("categories", {}):
                    category_total = sum(flare_summary["categories"][category].values())
                    if category_total >= threshold:
                        alerts.append({
                            "type": "count_threshold",
                            "severity": "warning",
                            "message": f"{category} detections ({category_total}) exceeds threshold ({threshold})",
                            "category": category,
                            "current_count": category_total,
                            "threshold": threshold,
                            "timestamp": datetime.now().isoformat()
                        })
        return alerts

    def _calculate_metrics(self, flare_analysis: List[Dict], flare_summary: Dict, config: FlareAnalysisConfig, context: ProcessingContext) -> Dict[str, Any]:
        total_detections = len(flare_analysis)
        unique_colors = len(flare_summary.get("color_distribution", {}))
        metrics = {
            "total_detections": total_detections,
            "unique_colors": unique_colors,
            "categories_analyzed": len(flare_summary.get("categories", {})),
            "processing_time": context.processing_time or 0.0,
            "input_format": context.input_format.value,
            "confidence_threshold": config.confidence_threshold,
            "color_diversity": 0.0,
            "detection_rate": 0.0,
            "average_colors_per_detection": config.top_k_colors
        }
        if total_detections > 0:
            metrics["color_diversity"] = (unique_colors / total_detections) * 100
        if config.time_window_minutes and config.time_window_minutes > 0:
            metrics["detection_rate"] = (total_detections / config.time_window_minutes) * 60
        category_metrics = {}
        for category, colors in flare_summary.get("categories", {}).items():
            category_total = sum(colors.values())
            category_metrics[category] = {
                "count": category_total,
                "unique_colors": len(colors),
                "color_diversity": (len(colors) / category_total) * 100 if category_total > 0 else 0
            }
        metrics["category_metrics"] = category_metrics
        metrics["processing_settings"] = {
            "confidence_threshold": config.confidence_threshold,
            "top_k_colors": config.top_k_colors,
            "frame_skip": config.frame_skip,
            "target_categories": config.target_categories,
            "enable_unique_counting": config.enable_unique_counting
        }
        return metrics

    def _extract_predictions(self, flare_analysis: List[Dict], config: FlareAnalysisConfig) -> List[Dict]:
        predictions = []
        for record in flare_analysis:
            prediction = {
                "category": record["category"],
                "confidence": record["confidence"],
                "bbox": record["bbox"],
                "frame_id": record["frame_id"],
                "timestamp": record["timestamp"],
                "main_color": record["main_color"],
                "major_colors": record["major_colors"]
            }
            if "detection_id" in record:
                prediction["id"] = record["detection_id"]
            predictions.append(prediction)
        return predictions

    def _generate_summary(self, flare_summary: Dict, general_summary: Dict, alerts: List) -> str:
        total_detections = flare_summary.get("total_detections", 0)
        unique_colors = len(flare_summary.get("color_distribution", {}))
        if total_detections == 0:
            return "No flares detected for color analysis"
        summary_parts = [f"{total_detections} flares analyzed for colors"]
        if unique_colors > 0:
            summary_parts.append(f"{unique_colors} unique colors detected")
        categories = flare_summary.get("categories", {})
        if len(categories) > 1:
            summary_parts.append(f"across {len(categories)} categories")
        if alerts:
            alert_count = len(alerts)
            summary_parts.append(f"with {alert_count} alert{'s' if alert_count != 1 else ''}")
        return ", ".join(summary_parts)

    def _generate_events(self, flare_summary: Dict, alerts: List, config: FlareAnalysisConfig, frame_number: Optional[int] = None) -> List[Dict]:
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        events = [{frame_key: []}]
        frame_events = events[0][frame_key]
        
        # Check if BadFlare is detected
        bad_flare_detected = flare_summary.get("categories", {}).get("BadFlare", {})
        total_bad_flare_detections = sum(bad_flare_detected.values()) if bad_flare_detected else 0

        if total_bad_flare_detections > 0:
            level = "info"
            intensity = min(10.0, total_bad_flare_detections / 5.0)
            if config.alert_config and config.alert_config.count_thresholds:
                threshold = config.alert_config.count_thresholds.get("all", 20)
                intensity = min(10.0, (total_bad_flare_detections / threshold) * 10)
                level = "critical" if intensity >= 7 else "warning" if intensity >= 5 else "info"
            elif total_bad_flare_detections > 50:
                level = "critical"
                intensity = 9.0
            elif total_bad_flare_detections > 25:
                level = "warning"
                intensity = 7.0
            event = {
                "type": "flare_detection",
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": level,
                "intensity": round(intensity, 1),
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7}
                },
                "application_name": "Flare Detection System",
                "application_version": "1.2",
                "location_info": None,
                "human_text": (
                    f"Event: BadFlare Detection\nLevel: {level.title()}\n"
                    f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC')}\n"
                    f"Detections: {total_bad_flare_detections} BadFlares analyzed\n"
                    f"Unique Colors: {len(bad_flare_detected) if bad_flare_detected else 0}\n"
                    f"Intensity: {intensity:.1f}/10"
                )
            }
            frame_events.append(event)

        # Generate alert events as in the original logic
        for alert in alerts:
            alert_event = {
                "type": alert.get("type", "flare_alert"),
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": alert.get("severity", "warning"),
                "intensity": 8.0,
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7}
                },
                "application_name": "Flare Detection Alert System",
                "application_version": "1.2",
                "location_info": alert.get("category"),
                "human_text": f"Event: {alert.get('type', 'Flare Alert').title()}\nMessage: {alert.get('message', 'Flare detection alert triggered')}"
            }
            frame_events.append(alert_event)
        
        return events

    def _generate_tracking_stats(self, flare_summary: Dict, insights: List[str], summary: str, config: FlareAnalysisConfig, frame_number: Optional[int] = None) -> List[Dict]:
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        tracking_stats = [{frame_key: []}]
        frame_tracking_stats = tracking_stats[0][frame_key]
        total_detections = flare_summary.get("total_detections", 0)
        track_ids_info = self._get_track_ids_info(flare_summary.get("detections", []))
        tracking_stat = {
            "type": "flare_tracking",
            "category": "flare_detection",
            "count": total_detections,
            "insights": insights,
            "summary": summary,
            "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC'),
            "human_text": self._generate_human_text_for_tracking(total_detections, flare_summary, insights, summary, config),
            "track_ids_info": track_ids_info,
            "global_frame_offset": getattr(self, '_global_frame_offset', 0),
            "local_frame_id": frame_key
        }
        frame_tracking_stats.append(tracking_stat)
        return tracking_stats

    def _generate_human_text_for_tracking(self, total_detections: int, flare_summary: Dict, insights: List[str], summary: str, config: FlareAnalysisConfig) -> str:
        text_parts = []
        if config.time_window_minutes:
            detection_rate_per_hour = (total_detections / config.time_window_minutes) * 60
            # text_parts.append(f"Detection Rate: {detection_rate_per_hour:.1f} flares per hour")
        unique_colors = len(flare_summary.get("color_distribution", {}))
        # text_parts.append(f"Unique Colors Detected: {unique_colors}")
        if total_detections > 0:
            color_diversity = (unique_colors / total_detections) * 100
            # text_parts.append(f"Color Diversity: {color_diversity:.1f}%")
        categories = flare_summary.get("categories", {})
        if categories:
            # text_parts.append(f"Categories Analyzed: {len(categories)}")
            for category, colors in categories.items():
                category_total = sum(colors.values())
                if category_total > 0:
                    dominant_color = max(colors.items(), key=lambda x: x[1])[0] if colors else "unknown"
                    text_parts.append(f"  {category_total} {category.title()} detected, Color: {dominant_color}")
        color_distribution = flare_summary.get("color_distribution", {})
        if color_distribution:
            top_colors = sorted(color_distribution.items(), key=lambda x: x[1], reverse=True)[:3]
            # text_parts.append("Top Colors:")
            for color, count in top_colors:
                percentage = (count / total_detections) * 100
                # text_parts.append(f"  {color.title()}: {count} flares ({percentage:.1f}%)")

        return "\n".join(text_parts)