from typing import Any, Dict, List, Optional
from dataclasses import asdict, dataclass, field
import time
from datetime import datetime, timezone
import copy
import tempfile
import os
from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol
from ..utils import (
    filter_by_confidence,
    filter_by_categories,
    apply_category_mapping,
    count_objects_by_category,
    count_objects_in_zones,
    calculate_counting_summary,
    match_results_structure,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker
)
try:
    import cv2
    import numpy as np
    import torch
    from ..ocr.easyocr_extractor import EasyOCRExtractor
    from ..ocr.postprocessing import TextPostprocessor 
    from ..ocr.preprocessing import ImagePreprocessor
    from ..core.config import BaseConfig, AlertConfig, ZoneConfig
    
except:
    print("test-------------------------------------------------")



@dataclass
class LicensePlateMonitorConfig(BaseConfig):
    """Configuration for License plate detection use case in License plate monitoring."""
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.6
    frame_skip: int = 1
    fps: Optional[float] = None
    bbox_format: str = "auto"
    usecase_categories: List[str] = field(default_factory=lambda: ['License_Plate'])
    target_categories: List[str] = field(default_factory=lambda: ['License_Plate'])
    alert_config: Optional[AlertConfig] = None
    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: {0: "License_Plate"})
    language: List[str] = field(default_factory=lambda: ['en', 'ar'])
    country: str = field(default_factory=lambda: 'qatar')

    def validate(self) -> List[str]:
        """Validate configuration parameters."""
        errors = super().validate()
        if self.confidence_threshold < 0 or self.confidence_threshold > 1:
            errors.append("confidence_threshold must be between 0 and 1")
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

class LicensePlateMonitorUseCase(BaseProcessor):
    CATEGORY_DISPLAY = {"License_Plate": "License Plate"}
    
    def __init__(self):
        super().__init__("license_plate_monitor")
        self.category = "license_plate_monitor"
        self.target_categories = ['License_Plate']
        self.CASE_TYPE: Optional[str] = 'license_plate_monitor'
        self.CASE_VERSION: Optional[str] = '1.3'
        self.smoothing_tracker = None
        self.tracker = None
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self._tracking_start_time = None
        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        self._track_merge_iou_threshold: float = 0.05
        self._track_merge_time_window: float = 7.0
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"
        self._seen_plate_texts = set()
        # CHANGE: Added _tracked_plate_texts to store the longest plate_text per track_id
        self._tracked_plate_texts: Dict[Any, str] = {}
        self.image_preprocessor = ImagePreprocessor()
        self.ocr_extractor = None  # Initialized in process
        self.text_postprocessor = TextPostprocessor()

    def reset_tracker(self) -> None:
        """Reset the advanced tracker instance."""
        if self.tracker is not None:
            self.tracker.reset()
            self.logger.info("AdvancedTracker reset for new tracking session")

    def reset_plate_tracking(self) -> None:
        """Reset plate tracking state."""
        self._seen_plate_texts = set()
        # CHANGE: Reset _tracked_plate_texts
        self._tracked_plate_texts = {}
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self.logger.info("Plate tracking state reset")

    def reset_all_tracking(self) -> None:
        """Reset both advanced tracker and plate tracking state."""
        self.reset_tracker()
        self.reset_plate_tracking()
        self.logger.info("All plate tracking state reset")

    def process(self, data: Any, config: ConfigProtocol, input_bytes: Optional[bytes] = None, 
                context: Optional[ProcessingContext] = None, stream_info: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        start_time = time.time()
        
        try:
            if not isinstance(config, LicensePlateMonitorConfig):
                return self.create_error_result("Invalid configuration type for license plate monitoring",
                                               usecase=self.name, category=self.category, context=context)
            
            if context is None:
                context = ProcessingContext()
            
            if not input_bytes:
                return self.create_error_result("input_bytes (video/image) is required for license plate monitoring",
                                               usecase=self.name, category=self.category, context=context)
            
            # if not data:
            #     return self.create_result(
            #     data={"agg_summary": {}},
            #     usecase=self.name,
            #     category=self.category,
            #     context=context
            # )
                # return self.create_error_result("Detection data is required for license plate monitoring",
                #                                usecase=self.name, category=self.category, context=context)
            
            # Initialize OCR extractor if not already done
            if self.ocr_extractor is None:
                self.ocr_extractor = EasyOCRExtractor(lang=config.language, gpu=torch.cuda.is_available(), verbose=False)
            
            input_format = match_results_structure(data)
            context.input_format = input_format
            context.confidence_threshold = config.confidence_threshold
            
            self.logger.info(f"Processing license plate monitoring with format: {input_format.value}")
            
            # Step 1: Apply confidence filtering
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
            
            # Step 2: Apply category mapping if provided
            if config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
                self.logger.debug("Applied category mapping")
            
            # Step 3: Filter to target categories
            processed_data = [d for d in processed_data if d.get('category') in self.target_categories]
            self.logger.debug("Applied category filtering")
            
            raw_processed_data = [copy.deepcopy(det) for det in processed_data]
            
            # Step 4: Apply bounding box smoothing if enabled
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
                processed_data = bbox_smoothing(processed_data, self.smoothing_tracker.config, self.smoothing_tracker)
            
            # Step 5: Apply advanced tracking
            try:
                from ..advanced_tracker import AdvancedTracker
                from ..advanced_tracker.config import TrackerConfig
                if self.tracker is None:
                    tracker_config = TrackerConfig(
                        track_high_thresh=float(config.confidence_threshold),
                        track_low_thresh=max(0.05, float(config.confidence_threshold) / 2),
                        new_track_thresh=float(config.confidence_threshold)
                    )
                    self.tracker = AdvancedTracker(tracker_config)
                    self.logger.info(f"Initialized AdvancedTracker with thresholds: high={tracker_config.track_high_thresh}, "
                                     f"low={tracker_config.track_low_thresh}, new={tracker_config.new_track_thresh}")
                processed_data = self.tracker.update(processed_data)
            except Exception as e:
                self.logger.warning(f"AdvancedTracker failed: {e}")
            
            # Step 6: Update tracking state
            self._update_tracking_state(processed_data)
            
            # Step 7: Attach masks to detections
            processed_data = self._attach_masks_to_detections(processed_data, raw_processed_data)
            
            # Step 8: Perform OCR on media
            ocr_analysis = self._analyze_ocr_in_media(processed_data, input_bytes, config)
            
            # Step 9: Update plate texts
            processed_data = self._update_detections_with_ocr(processed_data, ocr_analysis)
            self._update_plate_texts(processed_data)
            
            # Step 10: Update frame counter
            self._total_frame_counter += 1
            
            # Step 11: Extract frame information
            frame_number = None
            if stream_info:
                input_settings = stream_info.get("input_settings", {})
                start_frame = input_settings.get("start_frame")
                end_frame = input_settings.get("end_frame")
                if start_frame is not None and end_frame is not None and start_frame == end_frame:
                    frame_number = start_frame
            
            # Step 12: Calculate summaries
            counting_summary = self._count_categories(processed_data, config)
            counting_summary['total_counts'] = self.get_total_counts()
            
            # Step 13: Generate alerts and summaries
            alerts = self._check_alerts(counting_summary, frame_number, config)
            incidents_list = self._generate_incidents(counting_summary, alerts, config, frame_number, stream_info)
            tracking_stats_list = self._generate_tracking_stats(counting_summary, alerts, config, frame_number, stream_info)
            business_analytics_list = []
            summary_list = self._generate_summary(counting_summary, incidents_list, tracking_stats_list, business_analytics_list, alerts)
            
            # Step 14: Build result
            incidents = incidents_list[0] if incidents_list else {}
            tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
            business_analytics = business_analytics_list[0] if business_analytics_list else {}
            summary = summary_list[0] if summary_list else {}
            agg_summary = {str(frame_number): {
                "incidents": incidents,
                "tracking_stats": tracking_stats,
                "business_analytics": business_analytics,
                "alerts": alerts,
                "human_text": summary
            }}
            
            context.mark_completed()
            result = self.create_result(
                data={"agg_summary": agg_summary},
                usecase=self.name,
                category=self.category,
                context=context
            )
            return result
            
        except Exception as e:
            self.logger.error(f"License plate monitoring failed: {str(e)}", exc_info=True)
            if context:
                context.mark_completed()
            return self.create_error_result(str(e), type(e).__name__, usecase=self.name, category=self.category, context=context)

    def _is_video_bytes(self, media_bytes: bytes) -> bool:
        """Determine if bytes represent a video file."""
        video_signatures = [
            b'\x00\x00\x00\x20ftypmp4',  # MP4
            b'\x00\x00\x00\x18ftypmp4',  # MP4 variant
            b'RIFF',  # AVI
            b'\x1aE\xdf\xa3',  # MKV/WebM
            b'ftyp',  # General MP4 family
        ]
        for signature in video_signatures:
            if media_bytes.startswith(signature) or signature in media_bytes[:50]:
                return True
        return False

    def _analyze_ocr_in_media(self, data: Any, media_bytes: bytes, config: LicensePlateMonitorConfig) -> List[Dict[str, Any]]:
        """Analyze OCR of license plates in video frames or images."""
        is_video = self._is_video_bytes(media_bytes)
        if is_video:
            return self._analyze_ocr_in_video(data, media_bytes, config)
        else:
            return self._analyze_ocr_in_image(data, media_bytes, config)

    def _analyze_ocr_in_video(self, data: Any, video_bytes: bytes, config: LicensePlateMonitorConfig) -> List[Dict[str, Any]]:
        """Analyze OCR in video frames."""
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
            temp_video.write(video_bytes)
            video_path = temp_video.name

        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise RuntimeError("Failed to open video file")

            fps = config.fps or cap.get(cv2.CAP_PROP_FPS)
            ocr_analysis = []
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

                    preprocessed_crop = self.image_preprocessor.preprocess(crop, grayscale=True)
                    ocr_results = self.ocr_extractor.extract(preprocessed_crop, detail=1, paragraph=False)
                    texts = [r['text'] for r in ocr_results]
                    confs = [r['confidence'] for r in ocr_results]
                    processed = self.text_postprocessor.postprocess(texts, confs, task="license_plate", region=config.country, confidence_threshold=0.3)
                    valid_processed = [p for p in processed if p[2]]
                    plate_text = valid_processed[0][0] if valid_processed else None

                    ocr_record = {
                        "frame_id": frame_key,
                        "timestamp": round(timestamp, 2),
                        "category": detection.get("category", "License_Plate"),
                        "confidence": round(detection.get("confidence", 0.0), 3),
                        "plate_text": plate_text,
                        "bbox": bbox,
                        "detection_id": detection.get("id", f"det_{len(ocr_analysis)}"),
                        "track_id": detection.get("track_id")
                    }
                    ocr_analysis.append(ocr_record)

                frame_id += 1

            cap.release()
            return ocr_analysis

        finally:
            if os.path.exists(video_path):
                os.unlink(video_path)

    def _analyze_ocr_in_image(self, data: Any, image_bytes: bytes, config: LicensePlateMonitorConfig) -> List[Dict[str, Any]]:
        """Analyze OCR in a single image."""
        image_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        if image is None:
            raise RuntimeError("Failed to decode image from bytes")
        
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ocr_analysis = []
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

            preprocessed_crop = self.image_preprocessor.preprocess(crop, grayscale=True)
            ocr_results = self.ocr_extractor.extract(preprocessed_crop, detail=1, paragraph=False)
            texts = [r['text'] for r in ocr_results]
            confs = [r['confidence'] for r in ocr_results]
            processed = self.text_postprocessor.postprocess(texts, confs, task="license_plate", region=config.country, confidence_threshold=0.3)
            valid_processed = [p for p in processed if p[2]]
            plate_text = valid_processed[0][0] if valid_processed else None

            ocr_record = {
                "frame_id": "0",
                "timestamp": 0.0,
                "category": detection.get("category", "License_Plate"),
                "confidence": round(detection.get("confidence", 0.0), 3),
                "plate_text": plate_text,
                "bbox": bbox,
                "detection_id": detection.get("id", f"det_{len(ocr_analysis)}"),
                "track_id": detection.get("track_id")
            }
            ocr_analysis.append(ocr_record)
        
        return ocr_analysis

    def _crop_bbox(self, image: np.ndarray, bbox: Dict[str, Any], bbox_format: str) -> np.ndarray:
        """Crop bounding box region from image."""
        h, w = image.shape[:2]
        
        if bbox_format == "auto":
            if "xmin" in bbox:
                bbox_format = "xmin_ymin_xmax_ymax"
            elif "x" in bbox:
                bbox_format = "x_y_width_height"
            else:
                return np.zeros((0, 0, 3), dtype=np.uint8)
                
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

    def _get_frame_detections(self, data: Any, frame_key: str) -> List[Dict[str, Any]]:
        """Extract detections for a specific frame from data."""
        if isinstance(data, dict):
            return data.get(frame_key, [])
        elif isinstance(data, list):
            return data
        else:
            return []

    def _update_detections_with_ocr(self, detections: List[Dict[str, Any]], ocr_analysis: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Update detections with OCR results using track_id or bounding box for matching."""
        ocr_dict = {}
        for rec in ocr_analysis:
            if rec.get("plate_text"):
                # Primary key: track_id
                track_id = rec.get("track_id")
                if track_id is not None:
                    ocr_dict[track_id] = rec["plate_text"]
                # Fallback key: bounding box as tuple
                else:
                    bbox_key = tuple(sorted(rec["bbox"].items())) if rec.get("bbox") else None
                    if bbox_key:
                        ocr_dict[bbox_key] = rec["plate_text"]
                self.logger.debug(f"OCR record: track_id={track_id}, plate_text={rec.get('plate_text')}, bbox={rec.get('bbox')}")
        
        for det in detections:
            track_id = det.get("track_id")
            bbox_key = tuple(sorted(det.get("bounding_box", det.get("bbox", {})).items())) if det.get("bounding_box") or det.get("bbox") else None
            plate_text = None
            if track_id is not None and track_id in ocr_dict:
                plate_text = ocr_dict[track_id]
            elif bbox_key and bbox_key in ocr_dict:
                plate_text = ocr_dict[bbox_key]
            det["plate_text"] = plate_text
            self.logger.debug(f"Detection track_id={track_id}, bbox={det.get('bounding_box')}: Assigned plate_text={plate_text}")
        return detections

    def _count_categories(self, detections: List[Dict], config: LicensePlateMonitorConfig) -> Dict[str, Any]:
        """Count detections per category and include plate texts."""
        counts = {}
        valid_detections = []
        for det in detections:
            if not all(k in det for k in ['category', 'confidence', 'bounding_box']):
                self.logger.warning(f"Skipping invalid detection: {det}")
                continue
            cat = det.get('category', 'License_Plate')
            counts[cat] = counts.get(cat, 0) + 1
            valid_detections.append({
                "bounding_box": det.get("bounding_box"),
                "category": cat,
                "confidence": det.get("confidence"),
                "track_id": det.get("track_id"),
                "frame_id": det.get("frame_id"),
                "masks": det.get("masks", []),
                "plate_text": det.get("plate_text")
            })
        self.logger.debug(f"Valid detections after filtering: {len(valid_detections)}")
        return {
            "total_count": sum(counts.values()),
            "per_category_count": counts,
            "detections": valid_detections
        }

    def _generate_tracking_stats(self, counting_summary: Dict, alerts: Any, config: LicensePlateMonitorConfig,
                                frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """Generate structured tracking stats with frame-based keys."""
        tracking_stats = []
        total_detections = counting_summary.get("total_count", 0)
        total_counts = counting_summary.get("total_counts", {})
        cumulative_total = sum(total_counts.values()) if total_counts else 0
        per_category_count = counting_summary.get("per_category_count", {})
        track_ids_info = self._get_track_ids_info(counting_summary.get("detections", []))
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)
        camera_info = self.get_camera_info_from_stream(stream_info)
        
        human_text_lines = []
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        if total_detections > 0:
            category_counts = [f"{count} {cat}" for cat, count in per_category_count.items()]
            detection_text = category_counts[0] + " detected" if len(category_counts) == 1 else f"{', '.join(category_counts[:-1])}, and {category_counts[-1]} detected"
            human_text_lines.append(f"\t- {detection_text}")
            plate_texts = [det.get("plate_text") for det in counting_summary.get("detections", []) if det.get("plate_text")]
            if plate_texts:
                human_text_lines.append(f"\t- License Plates: {', '.join(plate_texts)}")
        else:
            human_text_lines.append(f"\t- No detections")
        
        human_text_lines.append("")
        human_text_lines.append(f"TOTAL SINCE {start_timestamp}:")
        human_text_lines.append(f"\t- Total Detected: {cumulative_total}")
        # if total_counts:
        #     for cat, count in total_counts.items():
        #         if count > 0:
        #             human_text_lines.append(f"\t- {cat}: {count}")
        # CHANGE: Use _tracked_plate_texts instead of _seen_plate_texts for TOTAL SINCE
        
        if self._tracked_plate_texts:
            human_text_lines.append("\t- Unique License Plates:")
            for text in sorted(self._tracked_plate_texts.values()):
                human_text_lines.append(f"\t\t- {text}")
        
        current_counts = [{"category": cat, "count": count} for cat, count in per_category_count.items() if count > 0 or total_detections > 0]
        total_counts_list = [{"category": cat, "count": count} for cat, count in total_counts.items() if count > 0 or cumulative_total > 0]
        
        human_text = "\n".join(human_text_lines)
        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "License_Plate")
            plate_text = detection.get("plate_text", "")
            segmentation = detection.get("masks", detection.get("segmentation", detection.get("mask", [])))
            detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation, plate_text=plate_text)
            detections.append(detection_obj)
        
        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, 'alert_type'):
            alert_settings.append({
                "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                "incident_category": self.CASE_TYPE,
                "threshold_level": config.alert_config.count_thresholds if hasattr(config.alert_config, 'count_thresholds') else {},
                "ascending": True,
                "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']), 
                                                  getattr(config.alert_config, 'alert_value', ['JSON']))}
            })
        
        if alerts:
            human_text_lines.append(f"Alerts: {alerts[0].get('settings', {})} sent @ {current_timestamp}")
        else:
            human_text_lines.append("Alerts: None")
        
        human_text = "\n".join(human_text_lines)
        reset_settings = [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]
        
        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts_list,
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

    def _check_alerts(self, summary: Dict, frame_number: Any, config: LicensePlateMonitorConfig) -> List[Dict]:
        """Check if any alert thresholds are exceeded."""
        def get_trend(data, lookback=900, threshold=0.6):
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True
            increasing = sum(1 for i in range(1, len(window)) if window[i] >= window[i - 1])
            return increasing / (len(window) - 1) >= threshold

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts = []
        total_detections = summary.get("total_count", 0)
        total_counts_dict = summary.get("total_counts", {})
        cumulative_total = sum(total_counts_dict.values()) if total_counts_dict else 0
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
                        "ascending": get_trend(self._ascending_alert_list),
                        "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']), 
                                                          getattr(config.alert_config, 'alert_value', ['JSON']))}
                    })
                elif category in per_category_count and per_category_count[category] > threshold:
                    alerts.append({
                        "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                        "alert_id": f"alert_{category}_{frame_key}",
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": threshold,
                        "ascending": get_trend(self._ascending_alert_list),
                        "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']), 
                                                          getattr(config.alert_config, 'alert_value', ['JSON']))}
                    })
        return alerts

    def _generate_incidents(self, counting_summary: Dict, alerts: List, config: LicensePlateMonitorConfig,
                           frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """Generate structured incidents."""
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        incidents = []
        total_detections = counting_summary.get("total_count", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        camera_info = self.get_camera_info_from_stream(stream_info)
        
        self._ascending_alert_list = self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list

        if total_detections > 0:
            level = "low"
            intensity = 5.0
            start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
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
                    level = "low"
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
            human_text = "\n".join(human_text_lines)

            alert_settings = []
            if config.alert_config and hasattr(config.alert_config, 'alert_type'):
                alert_settings.append({
                    "alert_type": getattr(config.alert_config, 'alert_type', ['Default']),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": config.alert_config.count_thresholds if hasattr(config.alert_config, 'count_thresholds') else {},
                    "ascending": True,
                    "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']), 
                                                      getattr(config.alert_config, 'alert_value', ['JSON']))}
                })
        
            event = self.create_incident(
                incident_id=f"{self.CASE_TYPE}_{frame_key}",
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

    def _generate_summary(self, summary: Dict, incidents: List, tracking_stats: List, business_analytics: List, alerts: List) -> List[Dict]:
        """Generate a human-readable summary."""
        lines = {
            "Application Name": self.CASE_TYPE,
            "Application Version": self.CASE_VERSION
        }
        if incidents:
            lines["Incidents"] = f"\n\t{incidents[0].get('human_text', 'No incidents detected')}\n"
        if tracking_stats:
            lines["Tracking Statistics"] = f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}\n"
        if business_analytics:
            lines["Business Analytics"] = f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}\n"
        if not incidents and not tracking_stats and not business_analytics:
            lines["Summary"] = "No Summary Data"
        return [lines]

    def _update_tracking_state(self, detections: List[Dict]):
        """Track unique track_ids per category."""
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
            det["track_id"] = canonical_id
            self._per_category_total_track_ids.setdefault(cat, set()).add(canonical_id)
            self._current_frame_track_ids[cat].add(canonical_id)

    def _update_plate_texts(self, detections: List[Dict]):
        """Update set of seen plate texts and track the longest plate_text per track_id."""
        for det in detections:
            text = det.get('plate_text')
            track_id = det.get('track_id')
            if text and track_id is not None:
                # CHANGE: Update _tracked_plate_texts with the longest text for this track_id
                current_text = self._tracked_plate_texts.get(track_id, '')
                if len(text) > len(current_text):
                    self._tracked_plate_texts[track_id] = text
                    self.logger.debug(f"Updated track_id={track_id} with new longest plate_text={text}")
                # Maintain _seen_plate_texts for compatibility
                self._seen_plate_texts.add(text)
                self.logger.debug(f"Added plate_text={text} for track_id={track_id} to seen texts")

    def get_total_counts(self):
        """Return total unique track_id count for each category."""
        # CHANGE: Count unique track_ids in _tracked_plate_texts instead of _seen_plate_texts
        return {'License_Plate': len(self._tracked_plate_texts)}

    def _get_track_ids_info(self, detections: List[Dict]) -> Dict[str, Any]:
        """Get detailed information about track IDs."""
        frame_track_ids = {det.get('track_id') for det in detections if det.get('track_id') is not None}
        total_track_ids = set()
        for s in getattr(self, '_per_category_total_track_ids', {}).values():
            total_track_ids.update(s)
        return {
            "total_count": len(total_track_ids),
            "current_frame_count": len(frame_track_ids),
            "total_unique_track_ids": len(total_track_ids),
            "current_frame_track_ids": list(frame_track_ids),
            "last_update_time": time.time(),
            "total_frames_processed": getattr(self, '_total_frame_counter', 0)
        }

    def _compute_iou(self, box1: Any, box2: Any) -> float:
        """Compute IoU between two bounding boxes."""
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

    def _merge_or_register_track(self, raw_id: Any, bbox: Any) -> Any:
        """Return a stable canonical ID for a raw tracker ID."""
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

    def _format_timestamp(self, timestamp: float) -> str:
        """Format a timestamp for human-readable output."""
        return datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    
    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        """Format timestamp for streams (YYYY:MM:DD HH:MM:SS format)."""
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        """Format timestamp for video chunks (HH:MM:SS.ms format)."""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False, frame_id: Optional[str]=None) -> str:
        """Get formatted current timestamp based on stream type."""
        print('STREAM INFO-------------------------------')
        print(stream_info)
        if not stream_info:
            return "00:00:00.00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)
                stream_time_str = self._format_timestamp_for_video(start_time)
                print('CURRENTTTT TIME-------------------------------',stream_info.get("input_settings", {}).get("stream_time", "NA"))

                return stream_info.get("input_settings", {}).get("stream_time", "NA")
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            if frame_id:
                start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
            else:
                start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)

            stream_time_str = self._format_timestamp_for_video(start_time)
            print('CURRENTTTT TIME-------------------------------',stream_info.get("input_settings", {}).get("stream_time", "NA"))

            return stream_info.get("input_settings", {}).get("stream_time", "NA")
        else:
            stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
            if stream_time_str:
                try:
                    timestamp_str = stream_time_str.replace(" UTC", "")
                    dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                    return self._format_timestamp_for_stream(timestamp)
                except:
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
            return "00:00:00"
        else:
            if self._tracking_start_time is None:
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                    except:
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()

            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _get_tracking_start_time(self) -> str:
        """Get the tracking start time, formatted as a string."""
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        """Set the tracking start time to the current time."""
        self._tracking_start_time = time.time()

    def _attach_masks_to_detections(self, processed_detections: List[Dict[str, Any]], raw_detections: List[Dict[str, Any]], 
                                    iou_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Attach segmentation masks from raw detections to processed detections."""
        if not processed_detections or not raw_detections:
            for det in processed_detections:
                det.setdefault("masks", [])
            return processed_detections

        used_raw_indices = set()
        for det in processed_detections:
            best_iou = 0.0
            best_idx = None
            for idx, raw_det in enumerate(raw_detections):
                if idx in used_raw_indices:
                    continue
                iou = self._compute_iou(det.get("bounding_box"), raw_det.get("bounding_box"))
                if iou > best_iou:
                    best_iou = iou
                    best_idx = idx
            if best_idx is not None and best_iou >= iou_threshold:
                raw_det = raw_detections[best_idx]
                masks = raw_det.get("masks", raw_det.get("mask"))
                if masks is not None:
                    det["masks"] = masks
                used_raw_indices.add(best_idx)
            else:
                det.setdefault("masks", ["EMPTY"])
        return processed_detections