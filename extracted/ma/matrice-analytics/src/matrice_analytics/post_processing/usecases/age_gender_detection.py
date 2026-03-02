from typing import Any, Dict, List, Optional
from dataclasses import asdict, dataclass, field
import time
from datetime import datetime, timezone
import copy
import tempfile
import os
import json
import zipfile
import os
import requests
import logging
from io import BytesIO
from collections import Counter
from matrice_analytics.post_processing.core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol
from matrice_analytics.post_processing.utils import (
    filter_by_confidence,
    filter_by_categories,
    # apply_category_mapping,
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
from matrice_analytics.post_processing.core.config import BaseConfig, AlertConfig, ZoneConfig

# Try to import optional age/gender dependencies (fail gracefully if missing)
ort = None
Image = None

try:
    import onnxruntime as ort
    from PIL import Image
    print("✓ Age/Gender dependencies available (onnxruntime, PIL)")
except ImportError as e:
    error_msg = str(e)
    print(f"⚠ Age/Gender dependencies not available: {e}")

    # Check if it's a NumPy version mismatch issue and provide helpful message
    if "NumPy" in error_msg and ("1.x" in error_msg or "2." in error_msg):
        print("→ DETECTED: NumPy version mismatch!")
        print("  onnxruntime was compiled with NumPy 1.x but NumPy 2.x is installed")
        print("  To fix manually: pip install 'numpy<2' --force-reinstall")
    else:
        print("  To enable manually: pip install onnxruntime-gpu pillow")

    print("→ Age/Gender detection will be disabled")
except Exception as e:
    print(f"⚠ Error importing Age/Gender dependencies: {e}")
    print("→ Age/Gender detection will be disabled")


def apply_category_mapping(results: Any, index_to_category: Dict[str, str]) -> Any:
    """
    Apply category index to name mapping.

    Args:
        results: Detection or tracking results
        index_to_category: Mapping from category index to category name

    Returns:
        Results with mapped category names
    """

    def map_detection(
        detection: Dict[str, Any], index_to_category: Dict[str, str]
    ) -> Dict[str, Any]:
        """Map a single detection."""
        detection = detection.copy()
        category_id = str(detection.get("class_id", detection.get("class_id")))
        index_to_category = {str(k): str(v) for k, v in index_to_category.items()}
        if category_id in index_to_category:
            detection["category"] = index_to_category[category_id]
            detection["class_id"] = category_id
        return detection

    if isinstance(results, list):
        # Detection format
        return [map_detection(r, index_to_category) for r in results]

    elif isinstance(results, dict):
        # Check if it's a simple classification result
        if "category" in results or "class_id" in results:
            return map_detection(results, index_to_category)

        # Frame-based format
        mapped_results = {}
        for frame_id, detections in results.items():
            if isinstance(detections, list):
                mapped_results[frame_id] = [
                    map_detection(d, index_to_category) for d in detections
                ]
            else:
                mapped_results[frame_id] = detections

        return mapped_results

    return results

def load_model_from_checkpoint(checkpoint_path,local_path):
    """
    Load a model from checkpoint URL
    """
    if ort is None:
        raise RuntimeError(
            "onnxruntime is not available. Cannot load age/gender detection models.\n"
            "Please install: pip install onnxruntime-gpu\n"
            "Or downgrade numpy: pip install 'numpy<2'"
        )

    try:
        print(f"Loading model from checkpoint: {checkpoint_path}")

        # Check if checkpoint is a URL
        if checkpoint_path.startswith(('http://', 'https://')):
            # Download checkpoint from URL
            response = requests.get(checkpoint_path, timeout = (30,200))
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                checkpoint_path = local_path
                print(f"Downloaded checkpoint to {local_path}")
            else:
                print(f"Failed to download checkpoint from {checkpoint_path}")
                return None
        
        # Load the model from the checkpoint
        model = ort.InferenceSession(checkpoint_path, providers=["CUDAExecutionProvider"])
        print(f"{local_path} Model loaded successfully from checkpoint")
        return model
        
    except Exception as e:
        print(f"Error loading model from checkpoint: {e}")
        return None


@dataclass
class AgeGenderConfig(BaseConfig):
    """Configuration for age and gender detection use case in age and gender detection."""
    enable_smoothing: bool = False
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.2
    frame_skip: int = 1
    fps: Optional[float] = None
    bbox_format: str = "auto"
    age_url:Any = "https://s3.us-west-2.amazonaws.com/testing.resources/datasets/age_detection_prod_model.onnx"
    gender_url:Any = "https://s3.us-west-2.amazonaws.com/testing.resources/datasets/gender_detection_prod_model.onnx"
    usecase_categories: List[str] = field(default_factory=lambda: ['FACE'])
    target_categories: List[str] = field(default_factory=lambda: ['FACE'])
    alert_config: Optional[AlertConfig] = None
    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: {0: "FACE"})

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

    def __post_init__(self):
        if self.gender_url and self.age_url:
            try:
                self.age_url = load_model_from_checkpoint(self.age_url, "age_detection_prod_model.onnx")
                self.gender_url = load_model_from_checkpoint(self.gender_url, "gender_detection_prod_model.onnx")
                print("✓ Age and Gender models loaded successfully")
            except RuntimeError as e:
                print(f"✗ Failed to load Age/Gender models: {e}")
                print("→ Age/Gender detection will be disabled")
                self.age_url = None
                self.gender_url = None
            except Exception as e:
                print(f"✗ Unexpected error loading Age/Gender models: {e}")
                import traceback
                traceback.print_exc()
                self.age_url = None
                self.gender_url = None
        else:
            print("⚠ Age and Gender model URLs not provided - detection will be disabled")
            self.age_url = None
            self.gender_url = None
        

class AgeGenderUseCase(BaseProcessor):
    def __init__(self):
        super().__init__("age_gender_detection")
        self.category = "age_gender_detection"
        self.target_categories = ['FACE']
        self.CASE_TYPE: Optional[str] = 'age_gender_detection'
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
        self.all_track_data: List[str] = []

        self.start_timer = None
        self.age: Dict[str:Any] = {}
        self.gender: Dict[str:Any] = {}
        #self.reset_timer = "2025-08-19-04:22:47.187574 UTC"

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
    
    def helper(self,detections, input_bytes, config):
        for det in detections:
            bbox = det.get('bounding_box')
            xmin = int(bbox.get('xmin'))
            xmax = int(bbox.get('xmax'))
            ymin = int(bbox.get('ymin'))
            ymax = int(bbox.get('xmax'))
            track_id = det.get('track_id')
            print(xmin,xmax,ymin,ymax)
            
            nparr = np.frombuffer(input_bytes, np.uint8)        # convert bytes to numpy array
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)      # decode image

            # Step 2: Convert PIL → NumPy array
            rgb_image = np.array(image)
            
            face = rgb_image[ymin:ymax,xmin:xmax]
            if face.size == 0:
                continue
            face_resized = cv2.resize(face, (224, 224))
            face_resized = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
            face_resized = np.expand_dims(face_resized, axis=0).astype(np.float32) / 255.0
            
            # Age Prediction
            age_preds = config.age_url.run(None, {"input": face_resized})[0][0]
            predicted_age = int(np.sum(age_preds * np.arange(0, 101)))
            confidence_age = float(np.max(age_preds))
            # Gender prediction
            gender_preds = config.gender_url.run(None, {"input": face_resized})[0][0]
            predicted_gender = "Man" if np.argmax(gender_preds) == 1 else "Woman"
            confidence_gen = float(np.max(gender_preds))
            
            print("________________________CHECK_______________________________________")
            print(predicted_age, predicted_gender)
            print("________________________CHECK_______________________________________")
            
            if track_id:
                track_id = str(track_id)

                if track_id not in self.gender:
                    self.gender[track_id] = []
                self.gender[track_id].append(predicted_gender)

                if track_id not in self.age:
                    self.age[track_id] = []
                self.age[track_id].append(predicted_age)
        return {"Age Data":self.age,"Gender Data":self.gender}

    def process(self, data: Any, config: ConfigProtocol, input_bytes: Optional[bytes] = None, 
                context: Optional[ProcessingContext] = None, stream_info: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        processing_start = time.time()
        
        try:
            if config.age_url is None and config.gender_url is None:
                return self.create_error_result("Model not loaded",
                                            usecase=self.name, category=self.category, context=context)
                
            if not isinstance(config, AgeGenderConfig):
                return self.create_error_result("Invalid configuration type for age gender detection",
                                            usecase=self.name, category=self.category, context=context)
            
            if context is None:
                context = ProcessingContext()
            
            if not input_bytes:
                return self.create_error_result("input_bytes (video/image) is required for age gender detection",
                                            usecase=self.name, category=self.category, context=context)
            
            if isinstance(getattr(config, 'alert_config', None), dict):
                try:
                    config.alert_config = AlertConfig(**config.alert_config)  # type: ignore[arg-type]
                except Exception:
                    pass
            
            input_format = match_results_structure(data)
            context.input_format = input_format
            context.confidence_threshold = config.confidence_threshold
            
            self.logger.info(f"Processing age gender detection with format: {input_format.value}")
            
            # Step 1: Apply confidence filtering 1
            print("---------CONFIDENCE FILTERING",config.confidence_threshold)
            
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            print("---------DATA1--------------",processed_data)
            self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
            
            # Step 2: Apply category mapping if provided
            if config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
                self.logger.debug("Applied category mapping")
                print("---------DATA2--------------",processed_data)
            # Step 3: Filter to target categories
            if self.target_categories:
                processed_data = [d for d in processed_data if d.get('category') in self.target_categories]
                self.logger.debug(f"Applied category filtering")
            
            # effective_targets = getattr(config, 'target_categories', self.target_categories) or self.target_categories
            # targets_lower = {str(cat).lower() for cat in effective_targets}
            # processed_data = [d for d in processed_data if str(d.get('category', '')).lower() in targets_lower]

            self.logger.debug("Applied category filtering")
            
            raw_processed_data = [copy.deepcopy(det) for det in processed_data]
            print("---------DATA2--------------",processed_data)
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
                from matrice_analytics.post_processing.advanced_tracker import AdvancedTracker
                from matrice_analytics.post_processing.advanced_tracker import TrackerConfig
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
            print("---------DATA3--------------",processed_data)
            # Step 6: Update tracking state
            self._update_tracking_state(processed_data)
            print("---------DATA4--------------",processed_data)
            # Step 7: Attach masks to detections
            processed_data = self._attach_masks_to_detections(processed_data, raw_processed_data)
            
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
            
            det = self.helper(processed_data,input_bytes,config)
            print("----------------------HELPER--------------------------------")
            print(det)
            print("----------------------HELPER--------------------------------")
            
            counting_summary = self._count_categories(processed_data, config,det)
            counting_summary['total_counts'] = self.get_total_counts()
            
            print("---------------------------------COUNTING SUMMARY------------------------------")
            print(counting_summary)
            print("---------------------------------COUNTING SUMMARY------------------------------")
            
            # Step 13: Generate alerts and summaries
            alerts = self._check_alerts(counting_summary, frame_number, config)
            incidents_list = self._generate_incidents(counting_summary, alerts, config, frame_number, stream_info)
            tracking_stats_list = self._generate_tracking_stats(counting_summary, alerts, config, frame_number, stream_info)
            business_analytics_list = []
            summary_list = self._generate_summary(counting_summary, incidents_list, tracking_stats_list, business_analytics_list, alerts)
            track_ids_info = self._get_track_ids_info(counting_summary.get("detections", []))
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
                "human_text": summary,
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
            self.logger.error(f"Age and Gender Detection failed: {str(e)}", exc_info=True)
            if context:
                context.mark_completed()
            return self.create_error_result(str(e), type(e).__name__, usecase=self.name, category=self.category, context=context)    
    
    def _get_frame_detections(self, data: Any, frame_key: str) -> List[Dict[str, Any]]:
        """Extract detections for a specific frame from data."""
        if isinstance(data, dict):
            return data.get(frame_key, [])
        elif isinstance(data, list):
            return data
        else:
            return []

    def _count_categories(self, detections: List[Dict], config: AgeGenderConfig, data) -> Dict[str, Any]:
        """Count unique licence-plate texts per frame and attach detections."""
        total_count = set()
        valid_detections: List[Dict[str, Any]] = []
        for det in detections:
            if not all(k in det for k in ['category', 'confidence', 'bounding_box']):
                continue
            cat = det.get('category', 'Person')
            track_id = det['track_id']
            total_count.add(det['track_id'])
            
            if track_id not in self.all_track_data:
                self.all_track_data.append(track_id)
            
            counts = {"Person": len(total_count)} if total_count else {}
            
            valid_detections.append({
                "bounding_box": det.get("bounding_box"),
                "category": cat,
                "confidence": det.get("confidence"),
                "track_id": det.get('track_id'),
                "frame_id": det.get("frame_id"),
                "masks": det.get("masks", []),
            })
            
        print(data)
        # Case 1: if data is a single dict
        if isinstance(data, dict):
            cats = [data]   # wrap in list so loop works
        # Case 2: if data is already a list of dicts
        elif isinstance(data, list):
            cats = data
        else:
            raise TypeError(f"Unexpected type for data: {type(data)}")
        
        results = []
        latest_result = {}
        for cat in cats:
            age_data = cat.get("Age Data", {})
            gender_data = cat.get("Gender Data", {})
            
            latest_age = {track_id: preds[-1] for track_id, preds in age_data.items() if preds}
            latest_gender = {track_id: preds[-1] for track_id, preds in gender_data.items() if preds}
            latest_result.update({
                "Latest Age": latest_age,
                "Latest Gender": latest_gender
            })

            # --- Most common gender ---
            most_common_gender = {}
            for track_id, preds in gender_data.items():
                counter = Counter(preds)
                most_common, count = counter.most_common(1)[0]
                most_common_gender[track_id] = [most_common]

            # --- Mean age ---
            mean_age = {}
            for track_id, preds in age_data.items():
                if preds:  # make sure list not empty
                    mean_age[track_id] = int(np.mean(preds))

            results.append({
                "Mean Age": mean_age,
                "Most Common Gender": most_common_gender
            })


        return {
            "total_count": len(total_count),
            "per_category_count": counts,
            "detections": valid_detections,
            "Age_Gender_Data": results[0] if isinstance(data, dict) else results,
            "latest": latest_result
        }

    def _generate_tracking_stats(self, counting_summary: Dict, alerts: Any, config: AgeGenderConfig,
                                frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """Generate structured tracking stats with frame-based keys."""
        tracking_stats = []
        total_detections = counting_summary.get("total_count", 0)
        total_counts = counting_summary.get("total_count", {})
        # cumulative_total = sum(set(total_counts.values())) if total_counts else 0
        per_category_count = counting_summary.get("per_category_count", {})
        track_ids_info = self._get_track_ids_info(counting_summary.get("detections", []))
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)
        camera_info = self.get_camera_info_from_stream(stream_info)
        age_gender_data = counting_summary.get("Age_Gender_Data")
        curr_frame_data = counting_summary.get("latest")
        current_counts = [f"{curr_frame_data['Latest Age'][track_id]}-{curr_frame_data['Latest Gender'].get(track_id, 'Unknown')}"
                            for track_id in curr_frame_data['Latest Age']
                            ]
        
        human_text_lines = []
        print("counting_summary", counting_summary)
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        human_text_lines.append(f"\tPerson Detected: {len(current_counts)}")
        if total_detections > 0:
            for track_id in curr_frame_data['Latest Age']:
                age = curr_frame_data['Latest Age'][track_id]
                gender = curr_frame_data['Latest Gender'].get(track_id, "Unknown")
                human_text_lines.append(f"\t\t{age}-{gender}")
        else:
            human_text_lines.append(f"\t- No detections")
        age_gender_pairs = [
                f"{age_gender_data['Mean Age'][tid]}-{age_gender_data['Most Common Gender'][tid][0]}"
                for tid in age_gender_data['Mean Age']
            ]
        pair_counts = Counter(age_gender_pairs)
        result_list = [(pair,count) for pair, count in pair_counts.items()]
        human_text_lines.append("")
        human_text_lines.append(f"TOTAL SINCE {start_timestamp}:")
        human_text_lines.append(f"\t- Total Detected: {len(age_gender_data['Mean Age'])}")
        for pair, count in result_list:
            human_text_lines.append(f"\t\t{pair}:{count}")

        # total_counts_list = [{"category": cat, "count": count} for cat, count in total_counts.items() if count > 0 or cumulative_total > 0]
        
        human_text = "\n".join(human_text_lines)
        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "FACE")
            if category == "FACE":
                category = "Person"
            #plate_text = detection.get("plate_text", "")
            segmentation = detection.get("masks", detection.get("segmentation", detection.get("mask", [])))
            detection_obj = self.create_detection_object(category, bbox, segmentation=None)
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
        print(tracking_stats)
        return tracking_stats

    def _check_alerts(self, summary: Dict, frame_number: Any, config: AgeGenderConfig) -> List[Dict]:
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
        # total_counts_dict = summary.get("total_counts", {})
        # cumulative_total = sum(total_counts_dict.values()) if total_counts_dict else 0
        per_category_count = summary.get("per_category_count", {})

        if not config.alert_config:
            return alerts

        # Extract thresholds regardless of dict/dataclass
        _alert_cfg = config.alert_config
        _thresholds = getattr(_alert_cfg, 'count_thresholds', None) if not isinstance(_alert_cfg, dict) else _alert_cfg.get('count_thresholds')
        _types = getattr(_alert_cfg, 'alert_type', None) if not isinstance(_alert_cfg, dict) else _alert_cfg.get('alert_type')
        _values = getattr(_alert_cfg, 'alert_value', None) if not isinstance(_alert_cfg, dict) else _alert_cfg.get('alert_value')
        _types = _types if isinstance(_types, list) else (list(_types) if _types is not None else ['Default'])
        _values = _values if isinstance(_values, list) else (list(_values) if _values is not None else ['JSON'])
        if _thresholds:
            for category, threshold in _thresholds.items():
                if category == "all" and total_detections > threshold:
                    alerts.append({
                        "alert_type": _types,
                        "alert_id": f"alert_{category}_{frame_key}",
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": threshold,
                        "ascending": get_trend(self._ascending_alert_list),
                        "settings": {t: v for t, v in zip(_types, _values)}
                    })
                elif category in per_category_count and per_category_count[category] > threshold:
                    alerts.append({
                        "alert_type": _types,
                        "alert_id": f"alert_{category}_{frame_key}",
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": threshold,
                        "ascending": get_trend(self._ascending_alert_list),
                        "settings": {t: v for t, v in zip(_types, _values)}
                    })
        return alerts

    def _generate_incidents(self, counting_summary: Dict, alerts: List, config: AgeGenderConfig,
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
            if config.alert_config:
                _alert_cfg = config.alert_config
                _types = getattr(_alert_cfg, 'alert_type', None) if not isinstance(_alert_cfg, dict) else _alert_cfg.get('alert_type')
                _values = getattr(_alert_cfg, 'alert_value', None) if not isinstance(_alert_cfg, dict) else _alert_cfg.get('alert_value')
                _thresholds = getattr(_alert_cfg, 'count_thresholds', None) if not isinstance(_alert_cfg, dict) else _alert_cfg.get('count_thresholds')
                _types = _types if isinstance(_types, list) else (list(_types) if _types is not None else ['Default'])
                _values = _values if isinstance(_values, list) else (list(_values) if _values is not None else ['JSON'])
                alert_settings.append({
                    "alert_type": _types,
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": _thresholds or {},
                    "ascending": True,
                    "settings": {t: v for t, v in zip(_types, _values)}
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


    def get_total_counts(self):
        """Return total unique age-gender encountered so far."""
        return {'FACE': len(self.all_track_data)}

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
