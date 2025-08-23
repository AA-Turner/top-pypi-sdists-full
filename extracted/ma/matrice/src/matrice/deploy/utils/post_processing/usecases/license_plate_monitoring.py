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
# External dependencies
import cv2
import numpy as np
#import torch
import re

# Fast license-plate OCR (replaces EasyOCR)
# Attempt to import fast_plate_ocr; fall back to a stub if unavailable
try:
    from fast_plate_ocr import LicensePlateRecognizer  # type: ignore
except ImportError:  # pragma: no cover – optional dependency may be absent
    class LicensePlateRecognizer:  # type: ignore
        """Stub fallback when fast_plate_ocr is not installed."""
        def __init__(self, *args, **kwargs):
            raise ImportError("fast_plate_ocr is required for LicensePlateMonitorUseCase but is not installed.")

# Internal utilities that are still required
from ..ocr.preprocessing import ImagePreprocessor
from ..core.config import BaseConfig, AlertConfig, ZoneConfig

# (Catch import errors early in the logs)
try:
    _ = LicensePlateRecognizer  # noqa: B018 – reference to quiet linters
except Exception as _e:
    print(f"Warning: fast_plate_ocr could not be imported ⇒ {_e}")


@dataclass
class LicensePlateMonitorConfig(BaseConfig):
    """Configuration for License plate detection use case in License plate monitoring."""
    enable_smoothing: bool = False
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.565
    frame_skip: int = 1
    fps: Optional[float] = None
    bbox_format: str = "auto"
    usecase_categories: List[str] = field(default_factory=lambda: ['license_plate'])
    target_categories: List[str] = field(default_factory=lambda: ['license_plate'])
    alert_config: Optional[AlertConfig] = None
    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: {0: "license_plate"})
    language: List[str] = field(default_factory=lambda: ['en'])
    country: str = field(default_factory=lambda: 'us')

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
    CATEGORY_DISPLAY = {"license_plate": "license_plate"}
    
    # --------------------------------------------------------------
    # Shared resources (initialised once per process)
    # --------------------------------------------------------------
    _ocr_model: Optional[LicensePlateRecognizer] = None  # Fast plate OCR
    

    
    def __init__(self):
        super().__init__("license_plate_monitor")
        self.category = "license_plate_monitor"
        self.target_categories = ['license_plate']
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
        # Containers for text stability & uniqueness
        self._unique_plate_texts: Dict[str, str] = {}  # cleaned_text -> original (longest)
        self.image_preprocessor = ImagePreprocessor()
        # Fast OCR model (shared across instances)
        if LicensePlateMonitorUseCase._ocr_model is None:
            try:
                LicensePlateMonitorUseCase._ocr_model = LicensePlateRecognizer('cct-s-v1-global-model')
                self.logger.info("LicensePlateRecognizer loaded successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialise LicensePlateRecognizer: {e}")
        self.ocr_model = LicensePlateMonitorUseCase._ocr_model
        # OCR text history for stability checks (text → consecutive frame count)
        self._text_history: Dict[str, int] = {}

        self.start_timer = None
        #self.reset_timer = "2025-08-19-04:22:47.187574 UTC"

        # Minimum length for a valid plate (after cleaning)
        self._min_plate_len = 5
        # number of consecutive frames a plate must appear to be considered "stable"
        self._stable_frames_required = 3
        self._non_alnum_regex = re.compile(r"[^A-Za-z0-9]+")
        self._ocr_mode = "numeric" # "alphanumeric" or "numeric" or "alphabetic"

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
        self._text_history = {}
        self._unique_plate_texts = {}
        self.logger.info("Plate tracking state reset")

    def reset_all_tracking(self) -> None:
        """Reset both advanced tracker and plate tracking state."""
        self.reset_tracker()
        self.reset_plate_tracking()
        self.logger.info("All plate tracking state reset")

    def process(self, data: Any, config: ConfigProtocol, input_bytes: Optional[bytes] = None, 
                context: Optional[ProcessingContext] = None, stream_info: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        processing_start = time.time()
        try:
            if not isinstance(config, LicensePlateMonitorConfig):
                return self.create_error_result("Invalid configuration type for license plate monitoring",
                                               usecase=self.name, category=self.category, context=context)
            
            if context is None:
                context = ProcessingContext()
            
            if not input_bytes:
                return self.create_error_result("input_bytes (video/image) is required for license plate monitoring",
                                               usecase=self.name, category=self.category, context=context)
            
            # Initialize OCR extractor if not already done
            if self.ocr_model is None:
                self.logger.info("Lazy initialisation fallback (should rarely happen)")
                try:
                    LicensePlateMonitorUseCase._ocr_model = LicensePlateRecognizer('cct-s-v1-global-model')
                    self.ocr_model = LicensePlateMonitorUseCase._ocr_model
                except Exception as e:
                    return self.create_error_result(
                        f"Failed to initialise OCR model: {e}",
                        usecase=self.name,
                        category=self.category,
                        context=context,
                    )
            
            input_format = match_results_structure(data)
            context.input_format = input_format
            context.confidence_threshold = config.confidence_threshold
            
            self.logger.info(f"Processing license plate monitoring with format: {input_format.value}")
            
            # Step 1: Apply confidence filtering 1
            # print("---------CONFIDENCE FILTERING",config.confidence_threshold)
            # print("---------DATA1--------------",data)
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            #self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
            
            # Step 2: Apply category mapping if provided
            if config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
                #self.logger.debug("Applied category mapping")
            #print("---------DATA2--------------",processed_data)
            # Step 3: Filter to target categories
            processed_data = [d for d in processed_data if d.get('category') in self.target_categories]
            #self.logger.debug("Applied category filtering")
            
            raw_processed_data = [copy.deepcopy(det) for det in processed_data]
            #print("---------DATA2--------------",processed_data)
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
                        track_high_thresh=float(config.confidence_threshold-0.1),
                        track_low_thresh=max(0.05, float(config.confidence_threshold) / 2),
                        new_track_thresh=float(config.confidence_threshold-0.1)
                    )
                    self.tracker = AdvancedTracker(tracker_config)
                    self.logger.info(f"Initialized AdvancedTracker with thresholds: high={tracker_config.track_high_thresh}, "
                                     f"low={tracker_config.track_low_thresh}, new={tracker_config.new_track_thresh}")
                processed_data = self.tracker.update(processed_data)
            except Exception as e:
                self.logger.warning(f"AdvancedTracker failed: {e}")
            #print("---------DATA3--------------",processed_data)
            # Step 6: Update tracking state
            self._update_tracking_state(processed_data)
            #print("---------DATA4--------------",processed_data)
            # Step 7: Attach masks to detections
            processed_data = self._attach_masks_to_detections(processed_data, raw_processed_data)
            #print("---------DATA5--------------",processed_data)
            # Step 8: Perform OCR on media
            ocr_analysis = self._analyze_ocr_in_media(processed_data, input_bytes, config)

            #print("ocr_analysis", ocr_analysis)
            
            # Step 9: Update plate texts
            #print("---------DATA6--------------",processed_data)
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
            proc_time = time.time() - processing_start
            processing_latency_ms = proc_time * 1000.0
            processing_fps = (1.0 / proc_time) if proc_time > 0 else None
            # Log the performance metrics using the module-level logger
            print("latency in ms:",processing_latency_ms,"| Throughput fps:",processing_fps,"| Frame_Number:",self._total_frame_counter)

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
        return self._analyze_ocr_in_image(data, media_bytes, config)


    def _analyze_ocr_in_image(self, data: Any, image_bytes: bytes, config: LicensePlateMonitorConfig) -> List[Dict[str, Any]]:
        """Analyze OCR in a single image."""
        image_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
        
        if image is None:
            raise RuntimeError("Failed to decode image from bytes")
        
        rgb_image = image #cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ocr_analysis = []
        detections = self._get_frame_detections(data, "0")

        #print("OCR-detections", detections)
        
        for detection in detections:
            #print("---------OCR DETECTION",detection)
            if detection.get("confidence", 1.0) < config.confidence_threshold:
                continue

            bbox = detection.get("bounding_box", detection.get("bbox"))
            #print("---------OCR BBOX",bbox)
            if not bbox:
                continue

            crop = self._crop_bbox(rgb_image, bbox, config.bbox_format)
            #print("---------OCR CROP SIZEE",crop.size)
            if crop.size == 0:
                continue
            
            plate_text_raw = self._run_ocr(crop)
            #print("---------OCR PLATE TEXT",plate_text_raw)
            plate_text = plate_text_raw if plate_text_raw else None

            ocr_record = {
                "frame_id": "0",
                "timestamp": 0.0,
                "category": detection.get("category", ""),
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

    # ------------------------------------------------------------------
    # Fast OCR helpers
    # ------------------------------------------------------------------
    def _clean_text(self, text: str) -> str:
        """Sanitise OCR output to keep only alphanumerics and uppercase."""
        if not text:
            return ""
        return self._non_alnum_regex.sub('', text).upper()

    def _run_ocr(self, crop: np.ndarray) -> str:
        """Run OCR on a cropped plate image and return cleaned text or empty string."""
        # print("---------OCR CROP22",crop)
        # print("---------OCR CROP SIZE22",crop.size)

        if crop is None or crop.size == 0 or self.ocr_model is None:
            return ""
        try:
            # fast_plate_ocr expects RGB
            #rgb_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
            res = self.ocr_model.run(crop)
            if isinstance(res, list):
                res = res[0] if res else ""
            cleaned_text = self._clean_text(str(res))
            if cleaned_text and len(cleaned_text) >= self._min_plate_len:
                if self._ocr_mode == "numeric":
                    response = all(ch.isdigit() for ch in cleaned_text) 
                elif self._ocr_mode == "alphabetic":
                    response = all(ch.isalpha() for ch in cleaned_text)
                elif self._ocr_mode == "alphanumeric":
                    response = True
                
                if response:
                    return cleaned_text
            else:
                return ""
        except Exception as exc:
            self.logger.warning(f"OCR failed: {exc}")
            return ""

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
        #print("---------UPDATE DETECTIONS WITH OCR",ocr_analysis)
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
                #self.logger.info(f"OCR record: track_id={track_id}, plate_text={rec.get('plate_text')}, bbox={rec.get('bbox')}")
        
        #print("---------UPDATE DETECTIONS WITH OCR -II",ocr_dict)
        for det in detections:
            track_id = det.get("track_id")
            bbox_key = tuple(sorted(det.get("bounding_box", det.get("bbox", {})).items())) if det.get("bounding_box") or det.get("bbox") else None
            plate_text = None
            if track_id is not None and track_id in ocr_dict:
                plate_text = ocr_dict[track_id]
            elif bbox_key and bbox_key in ocr_dict:
                plate_text = ocr_dict[bbox_key]
            det["plate_text"] = plate_text
            #self.logger.info(f"Detection track_id={track_id}, bbox={det.get('bounding_box')}: Assigned plate_text={plate_text}")
        return detections

    def _count_categories(self, detections: List[Dict], config: LicensePlateMonitorConfig) -> Dict[str, Any]:
        """Count unique licence-plate texts per frame and attach detections."""
        unique_texts: set = set()
        valid_detections: List[Dict[str, Any]] = []

        #print("---------SUMMARY COUNT CATEGORIES",detections)
        for det in detections:
            if not all(k in det for k in ['category', 'confidence', 'bounding_box']):
                continue

            cat = det.get('category', '')
            plate_text_raw = det.get('plate_text', '')
            #print("---------SUMMARY COUNT CATEGORIES PLATE TEXT RAW",plate_text_raw)
            #print("---------SUMMARY COUNT CATEGORIES PLATE TEXT RAW",det)
            cleaned_text = plate_text_raw #self._clean_text(plate_text_raw)

            # Consider as unique only if meets criteria
            if cleaned_text and len(cleaned_text) >= self._min_plate_len:
                unique_texts.add(cleaned_text)

            valid_detections.append({
                "bounding_box": det.get("bounding_box"),
                "category": cat,
                "confidence": det.get("confidence"),
                "track_id": det.get('track_id'),
                "frame_id": det.get("frame_id"),
                "masks": det.get("masks", []),
                "plate_text": plate_text_raw
            })

        counts = {"License_Plate": len(unique_texts)} if unique_texts else {}

        # print("---------SUMMARY COUNT CATEGORIES VALID DETECTIONS",valid_detections)
        # print(len(unique_texts),'per_cat_count',counts)

        return {
            "total_count": len(unique_texts),
            "per_category_count": counts,
            "detections": valid_detections
        }

    def _generate_tracking_stats(self, counting_summary: Dict, alerts: Any, config: LicensePlateMonitorConfig,
                                frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """Generate structured tracking stats with frame-based keys."""
        tracking_stats = []
        total_detections = counting_summary.get("total_count", 0)
        total_counts = counting_summary.get("total_counts", {})
        cumulative_total = sum(set(total_counts.values())) if total_counts else 0
        per_category_count = counting_summary.get("per_category_count", {})
        track_ids_info = self._get_track_ids_info(counting_summary.get("detections", []))
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)
        camera_info = self.get_camera_info_from_stream(stream_info)
        
        human_text_lines = []
        #print("counting_summary", counting_summary)
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        if total_detections > 0:
            category_counts = [f"{count} {cat}" for cat, count in per_category_count.items()]
            detection_text = category_counts[0] + " detected" if len(category_counts) == 1 else f"{', '.join(category_counts[:-1])}, and {category_counts[-1]} detected"
            human_text_lines.append(f"\t- {detection_text}")
            # Deduplicate plate texts for the current frame while preserving order -
            seen_cleaned = set()
            display_texts = []
            for det in counting_summary.get("detections", []):
                raw = det.get("plate_text", "")
                cleaned = self._clean_text(raw)
                if cleaned and cleaned not in seen_cleaned:
                    seen_cleaned.add(cleaned)
                    # Display the longest raw variant seen in this frame for that cleaned text
                    longest_variant = max(
                        [d.get("plate_text", "") for d in counting_summary.get("detections", []) if self._clean_text(d.get("plate_text", "")) == cleaned],
                        key=len,
                    )
                    display_texts.append(longest_variant)
            if display_texts:
                human_text_lines.append(f"\t- License Plates: {', '.join(display_texts)}")
        else:
            human_text_lines.append(f"\t- No detections")
        
        human_text_lines.append("")
        human_text_lines.append(f"TOTAL SINCE {start_timestamp}:")
        human_text_lines.append(f"\t- Total Detected: {cumulative_total}")

        if self._unique_plate_texts:
            human_text_lines.append("\t- Unique License Plates:")
            for text in sorted(self._unique_plate_texts.values()):
                human_text_lines.append(f"\t\t- {text}")

        current_counts = [{"category": cat, "count": count} for cat, count in per_category_count.items() if count > 0 or total_detections > 0]
        total_counts_list = [{"category": cat, "count": count} for cat, count in total_counts.items() if count > 0 or cumulative_total > 0]
        
        human_text = "\n".join(human_text_lines)
        detections = []
        for detection in counting_summary.get("detections", []):
            raw = detection.get("plate_text", "")
            cleaned = self._clean_text(raw)
            # if cleaned and cleaned not in seen_cleaned2:
            #     seen_cleaned2.add(cleaned)
            #     # Display the longest raw variant seen in this frame for that cleaned text
            if cleaned:
                #print("---------CLEANED-------------",cleaned)
                plate_text = max(
                    [d.get("plate_text", "") for d in counting_summary.get("detections", []) if self._clean_text(d.get("plate_text", "")) == cleaned],
                    key=len,
                )
            else:
                plate_text = "license_plate"
            
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "license_plate")
            #plate_text = detection.get("plate_text", "")
            segmentation = detection.get("masks", detection.get("segmentation", detection.get("mask", [])))
            detection_obj = self.create_detection_object(category, bbox, segmentation=None, plate_text=plate_text)
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
            human_text_lines.append(f"Alerts: {alerts[0].get('settings', {})}")
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
        """
        Generate a human_text string for the tracking_stat, incident, business analytics and alerts.
        """
        lines = []
        lines.append("Application Name: "+self.CASE_TYPE)
        lines.append("Application Version: "+self.CASE_VERSION)
        if len(incidents) > 0:
            lines.append("Incidents: "+f"\n\t{incidents[0].get('human_text', 'No incidents detected')}")
        if len(tracking_stats) > 0:
            lines.append("Tracking Statistics: "+f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}")
        if len(business_analytics) > 0:
            lines.append("Business Analytics: "+f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}")

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines.append("Summary: "+"No Summary Data")

        return ["\n".join(lines)]

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
                # Clean text again to guarantee consistency
                text = self._clean_text(text)
                if len(text) < self._min_plate_len:
                    continue  # Too short to be a valid plate

                # ----------------------------------------------------------
                # Update consecutive frame appearance counter
                # ----------------------------------------------------------
                self._text_history[text] = self._text_history.get(text, 0) + 1

                # Accept plate as stable only after N consecutive frames
                if self._text_history[text] >= self._stable_frames_required:
                    # Track longest string variant per track_id
                    current_text = self._tracked_plate_texts.get(track_id, '')
                    if len(text) > len(current_text):
                        self._tracked_plate_texts[track_id] = text
                    # Maintain global unique mapping (cleaned -> original longest)
                    longest_variant = self._unique_plate_texts.get(text, '')
                    if len(text) > len(longest_variant):
                        self._unique_plate_texts[text] = text
                   # self.logger.debug(f"Stable plate confirmed: {text} (track_id={track_id})")

        # Reset counters for texts not seen in this frame
        current_frame_texts = {self._clean_text(det.get('plate_text', '')) for det in detections if det.get('plate_text')}
        for t in list(self._text_history.keys()):
            if t not in current_frame_texts:
                self._text_history[t] = 0

    def get_total_counts(self):
        """Return total unique license plate texts encountered so far."""
        return {'License_Plate': len(self._unique_plate_texts)}

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
            timestamp = datetime.fromtimestamp(timestamp, timezone.utc).strftime(
                '%Y-%m-%d-%H:%M:%S.%f UTC'
            )

        # Ensure we are working with a string from here on
        if not isinstance(timestamp, str):
            return str(timestamp)

        # If there is no fractional component, simply return the original string
        if '.' not in timestamp:
            return timestamp

        # Split out the main portion (up to the decimal point)
        main_part, fractional_and_suffix = timestamp.split('.', 1)

        # Separate fractional digits from the suffix (typically ' UTC')
        if ' ' in fractional_and_suffix:
            fractional_part, suffix = fractional_and_suffix.split(' ', 1)
            suffix = ' ' + suffix  # Re-attach the space removed by split
        else:
            fractional_part, suffix = fractional_and_suffix, ''

        # Guarantee exactly two digits for the fractional part
        fractional_part = (fractional_part + '00')[:2]

        return f"{main_part}.{fractional_part}{suffix}"

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
        
        if not stream_info:
            return "00:00:00.00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)
                stream_time_str = self._format_timestamp_for_video(start_time)
                
                return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            if frame_id:
                start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
            else:
                start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)

            stream_time_str = self._format_timestamp_for_video(start_time)
           

            return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
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