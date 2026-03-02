from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone
import tempfile
import os
import cv2
import numpy as np
from collections import defaultdict
import time
from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol, ResultFormat
from ..utils import (
    filter_by_confidence, 
    filter_by_categories, 
    apply_category_mapping, 
    match_results_structure,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker
)

from ..core.config import BaseConfig, AlertConfig, ZoneConfig
from dataclasses import dataclass, field

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
    
    CATEGORY_DISPLAY = {
        "BadFlare": "BadFlare",
        "GoodFlare": "GoodFlare"
    }

    def __init__(self):
        super().__init__("flare_analysis")
        self.category = "flare_detection"
        self.CASE_TYPE: Optional[str] = 'flare_detection'
        self.CASE_VERSION: Optional[str] = '1.2'
        self.target_categories = ['BadFlare', 'GoodFlare']
        self.tracker = None
        self.smoothing_tracker = None
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._tracking_start_time = None
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        self._track_merge_iou_threshold: float = 0.05
        self._track_merge_time_window: float = 7.0
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"

    def reset_tracker(self) -> None:
        if self.tracker is not None:
            self.tracker.reset()
            self.logger.info("AdvancedTracker reset for new flare analysis session")

    def reset_flare_tracking(self) -> None:
        self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self._track_aliases = {}
        self._canonical_tracks = {}
        self._ascending_alert_list = []
        self.current_incident_end_timestamp = "N/A"
        self.logger.info("Flare tracking state reset")

    def reset_all_tracking(self) -> None:
        self.reset_tracker()
        self.reset_flare_tracking()
        self.logger.info("All flare tracking state reset")

    @staticmethod
    def _compute_iou(bbox1, bbox2) -> float:
        if not bbox1 or not bbox2:
            return 0.0
        if "xmin" in bbox1:
            x1_min, y1_min, x1_max, y1_max = bbox1["xmin"], bbox1["ymin"], bbox1["xmax"], bbox1["ymax"]
            x2_min, y2_min, x2_max, y2_max = bbox2["xmin"], bbox2["ymin"], bbox2["xmax"], bbox2["ymax"]
        else:
            x1_min, y1_min = bbox1["x"], bbox1["y"]
            x1_max, y1_max = x1_min + bbox1["width"], y1_min + bbox1["height"]
            x2_min, y2_min = bbox2["x"], bbox2["y"]
            x2_max, y2_max = x2_min + bbox2["width"], y2_min + bbox2["height"]
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
            iou = self._compute_iou(bbox, info["last_bbox"])
            if iou >= self._track_merge_iou_threshold:
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

    def _update_tracking_state(self, detections: List[Dict]):
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.target_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id
            self._per_category_total_track_ids.setdefault(cat, set()).add(canonical_id)
            self._current_frame_track_ids[cat].add(canonical_id)

    def get_total_counts(self):
        return {cat: len(ids) for cat, ids in self._per_category_total_track_ids.items()}

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        """Format timestamp for video chunks (HH:MM:SS.ms format)."""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60),2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp_for_stream(self, timestamp: float, precision: bool = False) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d-%H:%M:%S.%f UTC" if precision else "%Y:%m:%d %H:%M:%S")

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False, frame_id: Optional[str]=None) -> str:
        """Get formatted current timestamp based on stream type."""
        if not stream_info:
            return "00:00:00.00"
        # is_video_chunk = stream_info.get("input_settings", {}).get("is_video_chunk", False)
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)
                stream_time_str = self._format_timestamp_for_video(start_time)
                return stream_time_str
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)
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
                except:
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
                    except:
                        # Fallback to current time if parsing fails
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()

            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            # Reset minutes and seconds to 00:00 for "TOTAL SINCE" format
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _get_track_ids_info(self, detections: List[Dict]) -> Dict[str, Any]:
        frame_track_ids = set(det.get('track_id') for det in detections if det.get('track_id') is not None)
        total_track_ids = set()
        for s in self._per_category_total_track_ids.values():
            total_track_ids.update(s)
        return {
            "total_count": len(total_track_ids),
            "current_frame_count": len(frame_track_ids),
            "total_unique_track_ids": len(total_track_ids),
            "current_frame_track_ids": list(frame_track_ids),
            "last_update_time": time.time(),
            "total_frames_processed": self._total_frame_counter
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

            if config.enable_smoothing:
                if self.smoothing_tracker is None:
                    smoothing_config = BBoxSmoothingConfig(
                        smoothing_algorithm=config.smoothing_algorithm,
                        window_size=config.smoothing_window_size,
                        cooldown_frames=config.smoothing_cooldown_frames,
                        confidence_threshold=config.confidence_threshold,
                        confidence_range_factor=config.smoothing_confidence_range_factor,
                        enable_smoothing=True
                    )
                    self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
                flare_processed_data = bbox_smoothing(flare_processed_data, self.smoothing_tracker.config, self.smoothing_tracker)

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

            self._update_tracking_state(flare_processed_data)
            self._total_frame_counter += 1

            frame_number = None
            if stream_info:
                input_settings = stream_info.get("input_settings", {})
                start_frame = input_settings.get("start_frame")
                end_frame = input_settings.get("end_frame")
                if start_frame is not None and end_frame is not None and start_frame == end_frame:
                    frame_number = start_frame

            flare_analysis = self._analyze_flares_in_media(flare_processed_data, input_bytes, config)
            counting_summary = self._count_categories(flare_analysis, config)
            counting_summary['total_counts'] = self.get_total_counts()
            alerts = self._check_alerts(counting_summary, frame_number, config)
            incidents_list = self._generate_incidents(counting_summary, alerts, config, frame_number, stream_info)
            tracking_stats_list = self._generate_tracking_stats(counting_summary, alerts, config, frame_number, stream_info)
            business_analytics_list = self._generate_business_analytics(counting_summary, alerts, config, stream_info)
            summary_list = self._generate_summary(counting_summary, incidents_list, tracking_stats_list, business_analytics_list, alerts)

            incidents = incidents_list[0] if incidents_list else {}
            tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
            business_analytics = business_analytics_list[0] if business_analytics_list else {}
            agg_summary = {str(frame_number) if frame_number is not None else "current_frame": {
                "incidents": incidents,
                "tracking_stats": tracking_stats,
                "business_analytics": business_analytics,
                "alerts": alerts,
                "human_text": summary_list[0] if summary_list else {}
            }}

            context.mark_completed()
            result = self.create_result(
                data={"agg_summary": agg_summary},
                usecase=self.name,
                category=self.category,
                context=context
            )
            result.processing_time = context.processing_time or time.time() - start_time
            self.logger.info(f"Flare analysis completed in {result.processing_time:.2f}s")
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
            major_colors = [()] #extract_major_colors(crop, k=config.top_k_colors)
            main_color = major_colors[0][0] if major_colors else "unknown"
            flare_record = {
                "frame_id": "0",
                "timestamp": 0.0,
                "category": detection.get("category", "unknown"),
                "confidence": round(detection.get("confidence", 0.0), 3),
                "main_color": main_color,
                "major_colors": major_colors,
                "bounding_box": bbox,
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
            x_center = (xmin + xmax) / 2
            x_offset = (xmax - xmin) / 4
            y_center = (ymin + ymax) / 2
            y_offset = (ymax - ymin) / 4
            new_xmin = max(0, int(x_center - x_offset))
            new_xmax = min(w, int(x_center + x_offset))
            new_ymin = max(0, int(y_center - y_offset))
            new_ymax = min(h, int(y_center + y_offset))
        elif bbox_format == "x_y_width_height":
            x = max(0, int(bbox["x"]))
            y = max(0, int(bbox["y"]))
            width = int(bbox["width"])
            height = int(bbox["height"])
            xmax = min(w, x + width)
            ymax = min(h, y + height)
            x_center = (x + xmax) / 2
            x_offset = (xmax - x) / 4
            y_center = (y + ymax) / 2
            y_offset = (ymax - y) / 4
            new_xmin = max(0, int(x_center - x_offset))
            new_xmax = min(w, int(x_center + x_offset))
            new_ymin = max(0, int(y_center - y_offset))
            new_ymax = min(h, int(y_center + y_offset))
        else:
            return np.zeros((0, 0, 3), dtype=np.uint8)
        return image[new_ymin:new_ymax, new_xmin:new_xmax]

    def _count_categories(self, detections: List[Dict], config: FlareAnalysisConfig) -> Dict[str, Any]:
        counts = {}
        detections_list = []
        category_colors = defaultdict(lambda: defaultdict(int))
        for det in detections:
            cat = det.get("category", "unknown")
            counts[cat] = counts.get(cat, 0) + 1
            main_color = det.get("main_color", "unknown")
            category_colors[cat][main_color] += 1
            detections_list.append({
                "bounding_box": det.get("bounding_box"),
                "category": cat,
                "confidence": det.get("confidence"),
                "track_id": det.get("track_id"),
                "frame_id": det.get("frame_id"),
                "main_color": main_color
            })
        return {
            "total_count": sum(counts.values()),
            "per_category_count": counts,
            "detections": detections_list,
            "color_distribution": {cat: dict(colors) for cat, colors in category_colors.items()}
        }

    def _check_alerts(self, summary: Dict, frame_number: Optional[int], config: FlareAnalysisConfig) -> List[Dict]:
        def get_trend(data, lookback=900, threshold=0.8):
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True
            increasing = 0
            total = 0
            for i in range(1, len(window)):
                if window[i] >= window[i - 1]:
                    increasing += 1
                total += 1
            return increasing / total >= threshold

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts = []
        total_detections = summary.get("total_count", 0)
        total_counts_dict = summary.get("total_counts", {})
        per_category_count = summary.get("per_category_count", {})

        if not config.alert_config:
            return alerts

        if hasattr(config.alert_config, 'count_thresholds') and config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total_detections > threshold:
                    alerts.append({
                        "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                        "alert_id": f"alert_{category}_{frame_key}",
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": threshold,
                        "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                        "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']),
                                                        getattr(config.alert_config, 'alert_value', ['JSON']))}
                    })
                elif category in per_category_count:
                    count = per_category_count[category]
                    if count > threshold:
                        alerts.append({
                            "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                            "alert_id": f"alert_{category}_{frame_key}",
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                            "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']),
                                                            getattr(config.alert_config, 'alert_value', ['JSON']))}
                        })
        return alerts

    def _generate_incidents(self, counting_summary: Dict, alerts: List, config: FlareAnalysisConfig, frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        incidents = []
        total_detections = counting_summary.get("total_count", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)
        self._ascending_alert_list = self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list

        if total_detections > 0:
            level = "low"
            intensity = 5.0
            start_timestamp = self._get_start_timestamp_str(stream_info)
            if start_timestamp and self.current_incident_end_timestamp == 'N/A':
                self.current_incident_end_timestamp = 'Incident still active'
            elif start_timestamp and self.current_incident_end_timestamp == 'Incident still active':
                if len(self._ascending_alert_list) >= 15 and sum(self._ascending_alert_list[-15:]) / 15 < 1.5:
                    self.current_incident_end_timestamp = current_timestamp
            elif self.current_incident_end_timestamp != 'Incident still active' and self.current_incident_end_timestamp != 'N/A':
                self.current_incident_end_timestamp = 'N/A'

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
                    self._ascending_alert_list.append(0)
            else:
                if total_detections > 30:
                    level = "critical"
                    intensity = 10.0
                    self._ascending_alert_list.append(3)
                elif total_detections > 25:
                    level = "significant"
                    intensity = 9.0
                    self._ascending_alert_list.append(2)
                elif total_detections > 15:
                    level = "medium"
                    intensity = 7.0
                    self._ascending_alert_list.append(1)
                else:
                    level = "low"
                    intensity = min(10.0, total_detections / 3.0)
                    self._ascending_alert_list.append(0)

            human_text_lines = [f"INCIDENTS DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            for cat, count in counting_summary.get("per_category_count", {}).items():
                if count > 0:
                    human_text_lines.append(f"\t{cat}: {count}")
            human_text = "\n".join(human_text_lines)

            alert_settings = []
            if config.alert_config and hasattr(config.alert_config, 'alert_type'):
                alert_settings.append({
                    "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": config.alert_config.count_thresholds,
                    "ascending": True,
                    "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']),
                                                    getattr(config.alert_config, 'alert_value', ['JSON']))}
                })

            event = self.create_incident(
                incident_id=f"{self.CASE_TYPE}_{frame_number if frame_number is not None else 'current_frame'}",
                incident_type=self.CASE_TYPE,
                severity_level=level,
                human_text=human_text,
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=alert_settings,
                start_time=start_timestamp,
                end_time=self.current_incident_end_timestamp,
                level_settings={"low": 1, "medium": 3, "significant": 4, "critical": 7}
            )
            incidents.append(event)
        else:
            self._ascending_alert_list.append(0)
            incidents.append({})
        return incidents

    def _generate_tracking_stats(self, counting_summary: Dict, alerts: List, config: FlareAnalysisConfig, frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        tracking_stats = []
        total_detections = counting_summary.get("total_count", 0)
        total_counts_dict = counting_summary.get("total_counts", {})
        per_category_count = counting_summary.get("per_category_count", {})
        color_distribution = counting_summary.get("color_distribution", {})
        current_timestamp = self._get_current_timestamp_str(stream_info)
        start_timestamp = self._get_start_timestamp_str(stream_info)
        high_precision_start_timestamp = self._get_start_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)
        camera_info = self.get_camera_info_from_stream(stream_info)

        total_counts = [{"category": cat, "count": count} for cat, count in total_counts_dict.items() if count > 0]
        current_counts = [{"category": cat, "count": count} for cat, count in per_category_count.items() if count > 0 or total_detections > 0]

        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "unknown")
            detection_obj = self.create_detection_object(category, bbox)  # Remove main_color parameter
            detection_obj["main_color"] = detection.get("main_color", "unknown")  # Add main_color afterward
            detections.append(detection_obj)

        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, 'alert_type'):
            alert_settings.append({
                "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                "incident_category": self.CASE_TYPE,
                "threshold_level": config.alert_config.count_thresholds,
                "ascending": True,
                "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']),
                                                getattr(config.alert_config, 'alert_value', ['JSON']))}
            })

        human_text_lines = [f"Tracking Statistics:"]
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}")
        for cat, count in per_category_count.items():
            if count > 0:
                colors = color_distribution.get(cat, {})
                dominant_color = max(colors.items(), key=lambda x: x[1])[0] if colors else "unknown"
                human_text_lines.append(f"\t{cat}: {count}, Dominant Color: {dominant_color}")
        if total_detections == 0:
            human_text_lines.append("\tNo Flares detected")
        human_text_lines.append(f"TOTAL SINCE {start_timestamp}")
        for cat, count in total_counts_dict.items():
            if count > 0:
                colors = color_distribution.get(cat, {})
                dominant_color = max(colors.items(), key=lambda x: x[1])[0] if colors else "unknown"
                human_text_lines.append(f"\t{cat}: {count}, Dominant Color: {dominant_color}")
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
            reset_time=high_precision_reset_timestamp
        )
        tracking_stats.append(tracking_stat)
        return tracking_stats

    def _generate_business_analytics(self, counting_summary: Dict, alerts: List, config: FlareAnalysisConfig, stream_info: Optional[Dict[str, Any]] = None, is_empty: bool = False) -> List[Dict]:
        if is_empty:
            return []
        camera_info = self.get_camera_info_from_stream(stream_info)
        total_detections = counting_summary.get("total_count", 0)
        color_distribution = counting_summary.get("color_distribution", {})
        human_text_lines = ["Business Analytics:"]
        if total_detections > 0:
            unique_colors = sum(len(colors) for colors in color_distribution.values())
            human_text_lines.append(f"Total Flares: {total_detections}")
            human_text_lines.append(f"Unique Colors: {unique_colors}")
            for cat, colors in color_distribution.items():
                if colors:
                    dominant_color = max(colors.items(), key=lambda x: x[1])[0]
                    human_text_lines.append(f"{cat}: {sum(colors.values())}, Dominant Color: {dominant_color}")
        else:
            human_text_lines.append("No Flares detected")
        human_text = "\n".join(human_text_lines)
        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, 'alert_type'):
            alert_settings.append({
                "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                "incident_category": self.CASE_TYPE,
                "threshold_level": config.alert_config.count_thresholds,
                "ascending": True,
                "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']),
                                                getattr(config.alert_config, 'alert_value', ['JSON']))}
            })
        reset_settings = [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]
        return [self.create_business_analytics(
            analysis_name="flare_color_analysis",
            statistics={"total_detections": total_detections, "unique_colors": sum(len(colors) for colors in color_distribution.values())},
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=reset_settings
        )]

    def _generate_summary(self, counting_summary: Dict, incidents: List, tracking_stats: List, business_analytics: List, alerts: List) -> List[Dict]:
        lines = {}
        lines["Application Name"] = self.CASE_TYPE
        lines["Application Version"] = self.CASE_VERSION
        if incidents and incidents[0]:
            lines["Incidents"] = f"\n\t{incidents[0].get('human_text', 'No incidents detected')}\n"
        if tracking_stats and tracking_stats[0]:
            lines["Tracking Statistics"] = f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}\n"
        if business_analytics and business_analytics[0]:
            lines["Business Analytics"] = f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}\n"
        if not lines.get("Incidents") and not lines.get("Tracking Statistics") and not lines.get("Business Analytics"):
            lines["Summary"] = "No Summary Data"
        return [lines]

    def _format_timestamp(self, timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    def _get_tracking_start_time(self) -> str:
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        self._tracking_start_time = time.time()