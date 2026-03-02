from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone
import tempfile
import os
import cv2
import copy
import numpy as np
from collections import defaultdict
import time
from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol
from ..core.config import BaseConfig, AlertConfig, ZoneConfig
from ..utils import (
    filter_by_confidence, 
    filter_by_categories, 
    apply_category_mapping, 
    match_results_structure,
    count_objects_by_category,
    calculate_counting_summary,
    match_results_structure,
    count_objects_in_zones,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker
)
from ..utils.geometry_utils import get_bbox_center, point_in_polygon, get_bbox_bottom25_center
from ..usecases.color.clip import ClipProcessor
import sys
from pathlib import Path
import logging
import subprocess
import shutil

@dataclass
class ColorDetectionConfig(BaseConfig):
    """Configuration for color detection use case."""
    confidence_threshold: float = 0.9
    top_k_colors: int = 3
    frame_skip: int = 1
    usecase: str = "color_detection"
    usecase_categories: List[str] = field(
        default_factory=lambda: [
            "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
            "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog",
            "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
            "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
            "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
            "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich",
            "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
            "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote",
            "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book",
            "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
        ]
    )
    target_categories: List[str] = field(
        default_factory=lambda: [
            "car", "bicycle", "bus", "motorcycle"]
    )
    fps: Optional[float] = None
    bbox_format: str = "auto"
    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
                0: "person", 1: "bicycle", 2: "car", 3: "motorcycle", 4: "airplane", 5: "bus",
                6: "train", 7: "truck", 8: "boat", 9: "traffic light", 10: "fire hydrant",
                11: "stop sign", 12: "parking meter", 13: "bench", 14: "bird", 15: "cat",
                16: "dog", 17: "horse", 18: "sheep", 19: "cow", 20: "elephant", 21: "bear",
                22: "zebra", 23: "giraffe", 24: "backpack", 25: "umbrella", 26: "handbag",
                27: "tie", 28: "suitcase", 29: "frisbee", 30: "skis", 31: "snowboard",
                32: "sports ball", 33: "kite", 34: "baseball bat", 35: "baseball glove",
                36: "skateboard", 37: "surfboard", 38: "tennis racket", 39: "bottle",
                40: "wine glass", 41: "cup", 42: "fork", 43: "knife", 44: "spoon", 45: "bowl",
                46: "banana", 47: "apple", 48: "sandwich", 49: "orange", 50: "broccoli",
                51: "carrot", 52: "hot dog", 53: "pizza", 54: "donut", 55: "cake", 56: "chair",
                57: "couch", 58: "potted plant", 59: "bed", 60: "dining table", 61: "toilet",
                62: "tv", 63: "laptop", 64: "mouse", 65: "remote", 66: "keyboard",
                67: "cell phone", 68: "microwave", 69: "oven", 70: "toaster", 71: "sink",
                72: "refrigerator", 73: "book", 74: "clock", 75: "vase", 76: "scissors",
                77: "teddy bear", 78: "hair drier", 79: "toothbrush"
            }
    )
    alert_config: Optional[AlertConfig] = None
    time_window_minutes: int = 60
    enable_unique_counting: bool = True
    enable_smoothing: bool = False
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    enable_detector: bool = True

    #JBK_720_GATE POLYGON = [[86, 328], [844, 317], [1277, 520], [1273, 707], [125, 713]]
    zone_config: Optional[Dict[str, List[List[float]]]] = None #field(
#     default_factory=lambda: {
#         "zones": {
#             "Interest_Region": [[86, 328], [844, 317], [1277, 520], [1273, 707], [125, 713]],
#         }
#     }
# )
    # true_import: bool = False

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
    
    # def __post_init__(self):
    #     # Lazy initialization: the ClipProcessor will be created once by the use case
    #     # to avoid repeated model downloads and to ensure GPU session reuse.
    #     # log_file = open("pip_jetson_bt.log", "w")
    #     # cmd = ["pip", "install", "--force-reinstall", "huggingface_hub", "regex", "safetensors"]
    #     # subprocess.Popen(
    #     #         cmd,
    #     #         stdout=log_file,
    #     #         stderr=subprocess.STDOUT,
    #     #         preexec_fn=os.setpgrp   
    #     #     )
    #     print("Came to post_init and libraries installed!!!")
    #     if self.detector:
    #         self.detector = ClipProcessor()
    #         print("ClipProcessor Loaded Successfully!!") 
    #     else:
    #         print("Clip color detector disabled by config")
    #         self.detector = None


class ColorDetectionUseCase(BaseProcessor):
    """Color detection processor for analyzing object colors in video streams with tracking."""
    CATEGORY_DISPLAY = {
        "bicycle": "Bicycle", "car": "Car", "motorbike": "Motorbike", "auto rickshaw": "Auto Rickshaw",
        "bus": "Bus", "garbagevan": "Garbage Van", "truck": "Truck", "minibus": "Minibus",
        "army vehicle": "Army Vehicle", "pickup": "Pickup", "policecar": "Police Car",
        "rickshaw": "Rickshaw", "scooter": "Scooter", "suv": "SUV", "taxi": "Taxi",
        "three wheelers -CNG-": "Three Wheelers (CNG)", "human hauler": "Human Hauler",
        "van": "Van", "wheelbarrow": "Wheelbarrow"
    }

    def __init__(self):
        super().__init__("color_detection")
        self.category = "visual_appearance"

        self.target_categories = ["car", "bicycle", "bus", "motorcycle"]

        self.CASE_TYPE: Optional[str] = 'color_detection'
        self.CASE_VERSION: Optional[str] = '1.3'

        self.tracker = None  # AdvancedTracker instance
        self.smoothing_tracker = None  # BBoxSmoothingTracker instance
        self._total_frame_counter = 0  # Total frames processed
        self._global_frame_offset = 0  # Frame offset for new sessions
        self._color_total_track_ids = defaultdict(set)  # Cumulative track IDs per category-color
        self._color_current_frame_track_ids = defaultdict(set)  # Per-frame track IDs per category-color

        self._tracking_start_time = None

        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        # Tunable parameters – adjust if necessary for specific scenarios
        self._track_merge_iou_threshold: float = 0.05  # IoU ≥ 0.05 →
        self._track_merge_time_window: float = 7.0  # seconds within which to merge

        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"
        self.color_det_dict = {}
        self.start_timer = None
        # Zone-based tracking storage
        self._zone_current_track_ids = {}  # zone_name -> set of current track IDs in zone
        self._zone_total_track_ids = {}  # zone_name -> set of all track IDs that have been in zone
        self._zone_current_counts = {}  # zone_name -> current count in zone
        self._zone_total_counts = {}  # zone_name -> total count that have been in zone
        self.logger.info("Initialized ColorDetectionUseCase with tracking")
        self.detector = None  # Will be initialized on first use
        self.all_color_data = {}
        self.all_color_counts = {}
        self.total_category_count = {}
        self.category_color = {}
        self.vehicle_tracks = {}
        self.vehicle_stats = defaultdict(lambda: defaultdict(int))
        self.zone_vehicle_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        #self.jpeg = TurboJPEG()
        # data, config, ProcessingContext(), stream_info,input_bytes
    def process(
        self,
        data: Any, 
        config: ConfigProtocol,
        input_bytes: Optional[bytes] = None,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None
    ) -> ProcessingResult:
        processing_start = time.time()

        try:
            cwd = os.getcwd()
            print("Current working directory:", cwd)
            if not isinstance(config, ColorDetectionConfig):
                return self.create_error_result(
                    "Invalid configuration type for color detection",
                    usecase=self.name,
                    category=self.category,
                    context=context
                )

            # if config.true_import and self.detector is None:
            #     self.detector = ClipProcessor()
            #     self.logger.info("Initialized ClipProcessor for color detection")

            if context is None:
                context = ProcessingContext()

            if not input_bytes:
                self.logger.warning("input_bytes is required for color detection")

            if not data:
                self.logger.warning("Detection data is required for color detection")

            input_format = match_results_structure(data)
            context.input_format = input_format
            context.confidence_threshold = config.confidence_threshold

            self.logger.info(f"Processing color detection with format: {input_format.value}")

            # Step 1: Apply confidence filtering
            processed_data = filter_by_confidence(data, config.confidence_threshold)

            # Step 2: Apply category mapping if provided
            if config.index_to_category:
                color_processed_data = apply_category_mapping(processed_data, config.index_to_category)

            color_processed_data = [d for d in color_processed_data if d['category'] in self.target_categories]

            raw_processed_data = [copy.deepcopy(det) for det in color_processed_data]
            # Step 3: Apply bounding box smoothing if enabled
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
                color_processed_data = bbox_smoothing(color_processed_data, self.smoothing_tracker.config, self.smoothing_tracker)

            # Step 4: Apply advanced tracking
            try:
                from ..advanced_tracker import AdvancedTracker
                from ..advanced_tracker.config import TrackerConfig

                if self.tracker is None:
                    tracker_config = TrackerConfig()
                    self.tracker = AdvancedTracker(tracker_config)
                    self.logger.info("Initialized AdvancedTracker for color detection tracking")

                color_processed_data = self.tracker.update(color_processed_data)

            except Exception as e:
                self.logger.warning(f"AdvancedTracker failed: {e}")


            color_processed_data = self._attach_masks_to_detections(color_processed_data, raw_processed_data)
            self._total_frame_counter += 1

            frame_number = None
            if stream_info:
                input_settings = stream_info.get("input_settings", {})
                start_frame = input_settings.get("start_frame")
                end_frame = input_settings.get("end_frame")
                # If start and end frame are the same, it's a single frame
                if start_frame is not None and end_frame is not None and start_frame == end_frame:
                    frame_number = start_frame

            # Step 7: Analyze colors in media
            color_analysis = self._analyze_colors_in_media(
                color_processed_data,
                input_bytes,
                config
            )
            if config.zone_config:
                color_processed_data = self._is_in_zone_robust(color_processed_data,config.zone_config)
            print(color_processed_data)
            
            # Initialize detector lazily on first use if enabled
            try:
                self.logger.debug("About to call process_color_in_frame...")

                if config.enable_detector and self.detector is None:
                    self.logger.info("Initializing ClipProcessor for color detection...")
                    try:
                        self.detector = ClipProcessor()
                        self.logger.info("ClipProcessor loaded successfully!")
                    except Exception as init_error:
                        self.logger.error(f"Failed to initialize ClipProcessor: {init_error}")
                        self.detector = None

                if self.detector is None:
                    self.logger.warning("Detector is disabled or failed to initialize, skipping color detection")
                    curr_frame_color = {}
                else:
                    self.logger.debug(f"Processing {len(color_processed_data)} detections for color classification")
                    curr_frame_color = self.detector.process_color_in_frame(
                        color_processed_data,
                        input_bytes,
                        config.zone_config,
                        stream_info,
                    )
                    self.logger.debug("process_color_in_frame completed successfully")
            except Exception as e:
                self.logger.error(f"ERROR in process_color_in_frame: {e}", exc_info=True)
                curr_frame_color = {}

            self.update_vehicle_stats(curr_frame_color)
            self._update_color_tracking_state_from_analysis(color_analysis)

            # Step 9: Calculate summaries
            color_summary = self._calculate_color_summary(color_analysis, config)
            totals = self.get_total_color_counts()
            if not totals:
                tmp = defaultdict(set)
                for rec in color_analysis:
                    color = rec.get('main_color')
                    tid = rec.get('track_id') or rec.get('detection_id')
                    if color and tid is not None:
                        tmp[color].add(tid)
                totals = {color: len(ids) for color, ids in tmp.items()}
            total_category_counts = self.get_total_category_counts(color_processed_data)
            color_summary['total_color_counts'] = totals
            color_summary['total_category_counts'] = total_category_counts

            general_summary = self._calculate_general_summary(processed_data, config)
            new_color_summary = self.merge_color_summary(color_processed_data,curr_frame_color)

            # Step 10: Zone analysis
            self.color_helper(curr_frame_color)

            zone_analysis = {}
            if config.zone_config and config.zone_config['zones']:
                frame_data = color_processed_data
                zone_analysis = count_objects_in_zones(frame_data, config.zone_config['zones'], stream_info)
                if zone_analysis and config.enable_unique_counting:
                    enhanced_zone_analysis = self._update_zone_tracking(zone_analysis, color_processed_data, config)
                    for zone_name, enhanced_data in enhanced_zone_analysis.items():
                        zone_analysis[zone_name] = enhanced_data



            # Step 11: Generate alerts, incidents, tracking stats, and summary
            alerts = self._check_alerts(color_summary, frame_number, config)

            incidents_list = self._generate_incidents(color_summary, alerts, config, frame_number, stream_info)
            incidents_list = []

            tracking_stats_list = self._generate_tracking_stats(new_color_summary,color_summary, alerts, config,curr_frame_color, frame_number, stream_info)

            business_analytics_list = []
            summary_list = self._generate_summary(color_summary, incidents_list, tracking_stats_list, business_analytics_list, alerts)


            incidents = incidents_list[0] if incidents_list else {}
            tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
            business_analytics = business_analytics_list[0] if business_analytics_list else {}
            summary = summary_list[0] if summary_list else {}
            agg_summary = {str(frame_number): {
                "incidents": incidents,
                "tracking_stats": tracking_stats,
                "business_analytics": business_analytics,
                "alerts": alerts,
                "zone_analysis": zone_analysis,
                "human_text": summary}
            }

            context.mark_completed()

            # Build result object following the new pattern

            result = self.create_result(
                data={"agg_summary": agg_summary},
                usecase=self.name,
                category=self.category,
                context=context
            )
            proc_time = time.time() - processing_start
            processing_latency_ms = proc_time * 1000.0
            processing_fps = (1.0 / proc_time) if proc_time > 0 else None
            print("latency in ms:",processing_latency_ms,"| Throughput fps:",processing_fps,"| Frame_Number:",self._total_frame_counter)
            return result

        except Exception as e:
            self.logger.error(f"Color detection failed: {str(e)}", exc_info=True)
            if context:
                context.mark_completed()
            return self.create_error_result(
                str(e),
                type(e).__name__,
                usecase=self.name,
                category=self.category,
                context=context
            )

    def update_vehicle_stats(self, frame_detections: dict):
        """
        Update global vehicle statistics ensuring uniqueness per track_id and per zone.
        If the same vehicle (track_id) is seen again:
            - Ignore if confidence is lower.
            - Update its color if confidence is higher.
        """

        # Ensure zone-level data structures exist
        if not hasattr(self, "zone_vehicle_stats"):
            self.zone_vehicle_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        for _, det in frame_detections.items():
            track_id = det.get('track_id')
            if track_id is None:
                continue

            vehicle_type = det.get('object_label', 'unknown').lower()
            color = det.get('color', 'unknown').lower()
            conf = det.get('confidence', 0.0)
            zone = det.get('zone_name', 'Unknown_Zone')

            # If this track_id is new → add and count
            if track_id not in self.vehicle_tracks:
                self.vehicle_tracks[track_id] = {
                    'object_label': vehicle_type,
                    'color': color,
                    'confidence': conf,
                    'zone': zone
                }
                self.vehicle_stats[vehicle_type][color] += 1
                self.zone_vehicle_stats[zone][vehicle_type][color] += 1

            else:
                existing = self.vehicle_tracks[track_id]
                if conf > existing['confidence']:
                    old_color = existing['color']
                    old_zone = existing.get('zone', zone)
                    old_type = existing.get('object_label', vehicle_type)

                    # Decrease old counts
                    self.vehicle_stats[old_type][old_color] -= 1
                    if self.vehicle_stats[old_type][old_color] <= 0:
                        del self.vehicle_stats[old_type][old_color]

                    self.zone_vehicle_stats[old_zone][old_type][old_color] -= 1
                    if self.zone_vehicle_stats[old_zone][old_type][old_color] <= 0:
                        del self.zone_vehicle_stats[old_zone][old_type][old_color]

                    # Update track info
                    self.vehicle_tracks[track_id].update({
                        'color': color,
                        'confidence': conf,
                        'zone': zone,
                    })

                    # Increase new counts
                    self.vehicle_stats[vehicle_type][color] += 1
                    self.zone_vehicle_stats[zone][vehicle_type][color] += 1


    def merge_color_summary(self,detections_data: List[Dict[str, Any]], curr_frame_color: Dict[int, Dict[str, Any]]) -> Dict[str, Any]:
          """
          Combine base detections with current frame color information and produce a color summary.
          Returns structure similar to _calculate_color_summary().
          """

          category_colors = defaultdict(lambda: defaultdict(int))
          detections = []
          counts = {}

          # Merge detections with color info
          for record in detections_data:
              track_id = record.get("track_id")
              category = record.get("category", "unknown")
              conf = record.get("confidence", 0.0)
              bbox = record.get("bounding_box", {})
              frame_id = record.get("frame_id")
              zone_name = record.get("zone_name", "Unknown")

              # Get color from curr_frame_color
              main_color = "unknown"
              if track_id in curr_frame_color:
                  main_color = curr_frame_color[track_id].get("color", "unknown")

              category_colors[category][main_color] += 1
              counts[category] = counts.get(category, 0) + 1

              detections.append({
                  "bounding_box": bbox,
                  "category": category,
                  "confidence": conf,
                  "track_id": track_id,
                  "frame_id": frame_id,
                  "main_color": main_color,
                  "zone_name": zone_name
              })

          # Flatten color distribution
          all_colors = defaultdict(int)
          for category_data in category_colors.values():
              for color, count in category_data.items():
                  all_colors[color] += count

          # Find dominant color per category
          dominant_colors = {}
          for category, colors in category_colors.items():
              if colors:
                  color, count = max(colors.items(), key=lambda x: x[1])
                  dominant_colors[category] = {
                      "color": color,
                      "count": count,
                      "percentage": round((count / sum(colors.values())) * 100, 1)
                  }

          # Final summary dict
          summary = {
              "total_count": sum(counts.values()),
              "per_category_count": counts,
              "detections": detections,
              "color_distribution": dict(all_colors),
              "dominant_colors": dominant_colors
          }

          return summary

    def get_vehicle_stats(self):
        """Return the current global vehicle statistics as a normal dictionary."""
        return {vtype: dict(colors) for vtype, colors in self.vehicle_stats.items()}

    def _is_in_zone_robust(self,detections,zones):
        if not detections:
          return {}
        new_data = []
        for det in detections:
          bbox = det.get('bounding_box')
          cx,cy = get_bbox_bottom25_center(bbox)
          for zone, region in zones.items():
            for reg, poly in region.items():
              if point_in_polygon((cx,cy),poly):
                det['zone_name'] = reg
                new_data.append(det)
        return new_data

    def color_helper(self, curr_data):
        if curr_data is None:
            return
        for tid, data in curr_data.items():
            if tid not in self.all_color_data:
                # First time seeing this track
                self.all_color_data[tid] = {
                    "color": data.get("color"),
                    "confidence": data.get("confidence"),
                }

                # update color counts
                color = data.get("color")
                if color:
                    self.all_color_counts[color] = self.all_color_counts.get(color, 0) + 1

            else:
                # Update only if new confidence is higher
                if data.get("confidence", 0) > self.all_color_data[tid]["confidence"]:
                    old_color = self.all_color_data[tid]["color"]
                    new_color = data.get("color")

                    if new_color != old_color:
                        # decrease old color count
                        if old_color in self.all_color_counts:
                            self.all_color_counts[old_color] -= 1
                            if self.all_color_counts[old_color] <= 0:
                                del self.all_color_counts[old_color]

                        # increase new color count
                        if new_color:
                            self.all_color_counts[new_color] = self.all_color_counts.get(new_color, 0) + 1

                    # update track info
                    self.all_color_data[tid]["color"] = new_color
                    self.all_color_data[tid]["confidence"] = data.get("confidence")
        # return self.all_color_data

    def _analyze_colors_in_media(
        self,
        data: Any,
        media_bytes: bytes,
        config: ColorDetectionConfig
    ) -> List[Dict[str, Any]]:
        """Analyze colors of detected objects in video frames or images."""
        return self._analyze_colors_in_image(data, media_bytes, config)

    def _update_color_tracking_state_from_analysis(self, color_analysis: List[Dict[str, Any]]) -> None:
        """Update total tracking store using analyzed color results.
        Ensures totals are populated even if pre-analysis detections lacked colors/track_ids."""
        existing_store = getattr(self, '_color_total_track_ids', None)
        if not isinstance(existing_store, defaultdict):
            existing_store = {} if existing_store is None else dict(existing_store)
            self._color_total_track_ids = defaultdict(set, existing_store)
        else:
            self._color_total_track_ids = existing_store
        # Reset current frame tracking for this frame
        self._color_current_frame_track_ids = defaultdict(set)

        for rec in color_analysis:
            cat = rec.get('category')
            color = rec.get('main_color')
            track_id = rec.get('track_id')
            major_colors = rec.get('major_colors') or []
            # Safely extract color confidence
            if major_colors and isinstance(major_colors[0], (list, tuple)) and len(major_colors[0]) > 2:
                color_conf = major_colors[0][2]
            else:
                color_conf = 0.0
            if track_id is None:
                track_id = rec.get('detection_id')
            if cat and track_id is not None:
                # Update the color_det_dict with the actual color
                if color and track_id in self.color_det_dict:
                    existing_color, existing_conf = self.color_det_dict.get(track_id, [None, -1])
                    if color_conf > existing_conf and color != existing_color:
                        # Move this track_id from any previous color bucket(s) to the new one
                        for k in list(self._color_total_track_ids.keys()):
                            if track_id in self._color_total_track_ids[k]:
                                self._color_total_track_ids[k].discard(track_id)
                        # Update assignment
                        self.color_det_dict[track_id] = [color, color_conf]
                        new_key = f"{cat}:{color}" if color else cat
                        self._color_total_track_ids[new_key].add(track_id)
                        # Update current frame tracking
                        self._color_current_frame_track_ids[new_key].add(track_id)
                    elif color_conf > existing_conf:
                        # Confidence improved but color unchanged; update confidence only
                        self.color_det_dict[track_id] = [existing_color, color_conf]
                        same_key = f"{cat}:{existing_color}" if existing_color else cat
                        self._color_current_frame_track_ids[same_key].add(track_id)
                    else:
                        # No improvement; still reflect in current frame under existing color
                        same_key = f"{cat}:{existing_color}" if existing_color else cat
                        self._color_current_frame_track_ids[same_key].add(track_id)
                elif color and track_id not in self.color_det_dict:
                    # First assignment for this track
                    self.color_det_dict[track_id] = [color, color_conf]
                    key = f"{cat}:{color}" if color else cat
                    self._color_total_track_ids[key].add(track_id)
                    # Also update current frame tracking
                    self._color_current_frame_track_ids[key].add(track_id)

    def _is_video_bytes(self, media_bytes: bytes) -> bool:
        """Determine if bytes represent a video file."""
        # Check common video file signatures
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


    def _analyze_colors_in_image(
        self,
        data: Any,
        image_bytes: bytes,
        config: ColorDetectionConfig
    ) -> List[Dict[str, Any]]:
        image_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        #image = self.jpeg.decode(image_bytes, pixel_format=TJPF_RGB)

        if image is None:
            raise RuntimeError("Failed to decode image from bytes")

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        color_analysis = []
        detections = self._get_frame_detections(data, "0")

        for detection in detections:
            if detection.get("confidence", 1.0) < config.confidence_threshold:
                continue

            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue

            # Check all zones
            zones = config.zone_config['zones'] if config.zone_config else {}
            in_any_zone = not zones
            zone_name = None
            for z_name, zone_polygon in zones.items():
                if self._is_in_zone(bbox, zone_polygon):
                    in_any_zone = True
                    zone_name = z_name
                    break
            if not in_any_zone:
                continue  # Skip detections outside zones

            # crop = self._crop_bbox(rgb_image, bbox, config.bbox_format)
            # if crop.size == 0:
            #     continue

            # major_colors = extract_major_colors(crop, k=config.top_k_colors)
            # main_color = major_colors[0][0] if major_colors else "unknown"
            main_color = "unknown"
            major_colors = []

            color_record = {
                "frame_id": "0",
                "timestamp": 0.0,
                "category": detection.get("category", "unknown"),
                "confidence": round(detection.get("confidence", 0.0), 3),
                "main_color": main_color,
                "major_colors": major_colors,
                "bbox": bbox,
                "detection_id": detection.get("id", f"det_{len(color_analysis)}"),
                "track_id": detection.get("track_id"),
                "zone_name": zone_name
            }
            color_analysis.append(color_record)

        return color_analysis


    def _get_frame_detections(self, data: Any, frame_key: str) -> List[Dict[str, Any]]:
        """Extract detections for a specific frame from data."""
        if isinstance(data, dict):
            # Frame-based format
            return data.get(frame_key, [])
        elif isinstance(data, list):
            # List format (single frame or all detections)
            return data
        else:
            return []

    def _crop_bbox(self, image: np.ndarray, bbox: Dict[str, Any], bbox_format: str) -> np.ndarray:
        """Crop bounding box region from image."""
        h, w = image.shape[:2]

        # Auto-detect bbox format
        if bbox_format == "auto":
            if "xmin" in bbox:
                bbox_format = "xmin_ymin_xmax_ymax"
            elif "x" in bbox:
                bbox_format = "x_y_width_height"
            else:
                return np.zeros((0, 0, 3), dtype=np.uint8)

        # Extract coordinates based on format
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

    def _calculate_color_summary(self, color_analysis: List[Dict], config: ColorDetectionConfig) -> Dict[str, Any]:
        category_colors = defaultdict(lambda: defaultdict(int))
        total_detections = len(color_analysis)
        detections = []
        counts = {}
        for record in color_analysis:
            category = record["category"]
            main_color = record["main_color"]
            category_colors[category][main_color] += 1
            counts[category] = counts.get(category, 0) + 1
            detections.append({
                "bounding_box": record["bbox"],
                "category": record["category"],
                "confidence": record["confidence"],
                "track_id": record["track_id"],
                "frame_id": record["frame_id"],
                "main_color": record["main_color"]
            })


        self.logger.debug(f"Valid detections after filtering: {len(detections)}")
        summary = {
            "total_count": sum(counts.values()),
            "per_category_count": counts,
            "detections": detections,
            "dominant_colors": {},
            "zone_counts": self._zone_current_counts if config.zone_config and config.zone_config['zones'] else {}
        }


        all_colors = defaultdict(int)
        for category_data in category_colors.values():
            for color, count in category_data.items():
                all_colors[color] += count
        summary["color_distribution"] = dict(all_colors)


        for category, colors in category_colors.items():
            if colors:
                if "dominant_colors" not in summary:
                    summary["dominant_colors"] = {}
                else:
                    dominant_color = max(colors.items(), key=lambda x: x[1])
                    summary["dominant_colors"][category] = {
                        "color": dominant_color[0],
                        "count": dominant_color[1],
                        "percentage": round((dominant_color[1] / sum(colors.values())) * 100, 1)
                    }


        return summary

    def _calculate_general_summary(self, processed_data: Any, config: ColorDetectionConfig) -> Dict[str, Any]:
        """Calculate general detection summary."""

        # Count objects by category
        category_counts = defaultdict(int)
        total_objects = 0

        if isinstance(processed_data, dict):
            # Frame-based format
            for frame_data in processed_data.values():
                if isinstance(frame_data, list):
                    for detection in frame_data:
                        if detection.get("confidence", 1.0) >= config.confidence_threshold:
                            category = detection.get("category", "unknown")
                            category_counts[category] += 1
                            total_objects += 1
        elif isinstance(processed_data, list):
            # List format
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

    def _calculate_metrics(self, color_analysis: List[Dict], color_summary: Dict, config: ColorDetectionConfig, context: ProcessingContext) -> Dict[str, Any]:
        """Calculate detailed metrics for analytics."""
        total_detections = len(color_analysis)
        unique_colors = len(color_summary.get("color_distribution", {}))

        metrics = {
            "total_detections": total_detections,
            "unique_colors": unique_colors,
            "categories_analyzed": len(color_summary.get("categories", {})),
            "processing_time": context.processing_time or 0.0,
            "input_format": context.input_format.value,
            "confidence_threshold": config.confidence_threshold,
            "color_diversity": 0.0,
            "detection_rate": 0.0,
            "average_colors_per_detection": config.top_k_colors
        }

        # Calculate color diversity
        if total_detections > 0:
            metrics["color_diversity"] = (unique_colors / total_detections) * 100

        # Calculate detection rate
        if config.time_window_minutes and config.time_window_minutes > 0:
            metrics["detection_rate"] = (total_detections / config.time_window_minutes) * 60

        # Per-category metrics
        if color_summary.get("categories"):
            category_metrics = {}
            for category, colors in color_summary["categories"].items():
                category_total = sum(colors.values())
                category_metrics[category] = {
                    "count": category_total,
                    "unique_colors": len(colors),
                    "color_diversity": (len(colors) / category_total) * 100 if category_total > 0 else 0
                }
            metrics["category_metrics"] = category_metrics

        # Processing settings
        metrics["processing_settings"] = {
            "confidence_threshold": config.confidence_threshold,
            "top_k_colors": config.top_k_colors,
            "frame_skip": config.frame_skip,
            "target_categories": config.target_categories,
            "enable_unique_counting": config.enable_unique_counting
        }

        return metrics

    def _extract_predictions(self, color_analysis: List[Dict], config: ColorDetectionConfig) -> List[Dict]:
        """Extract predictions in standard format."""

        predictions = []
        for record in color_analysis:
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

    def _generate_summary(self, summary: dict, incidents: List, tracking_stats: List, business_analytics: List, alerts: List) -> List[str]:
        """
        Generate a human_text string for the tracking_stat, incident, business analytics and alerts.
        """
        lines = []
        lines.append("Application Name: "+self.CASE_TYPE)
        lines.append("Application Version: "+self.CASE_VERSION)
        if len(incidents) > 0:
            lines.append("Incidents: "+f"\n\t{incidents[0].get('human_text', 'No incidents detected')}")
        if len(tracking_stats) > 0:
            lines.append(f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}")
        if len(business_analytics) > 0:
            lines.append("Business Analytics: "+f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}")

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines.append("Summary: "+"No Summary Data")

        return ["\n".join(lines)]

    def _generate_events(self, color_summary: Dict, alerts: List, config: ColorDetectionConfig, frame_number: Optional[int] = None) -> List[Dict]:
        """Generate structured events with frame-based keys."""
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        events = [{frame_key: []}]
        frame_events = events[0][frame_key]
        total_detections = color_summary.get("total_detections", 0)

        if total_detections > 0:
            level = "info"
            intensity = min(10.0, total_detections / 5.0)
            if config.alert_config and hasattr(config.alert_config, 'count_thresholds') and config.alert_config.count_thresholds:
                threshold = config.alert_config.count_thresholds.get("all", 20)
                intensity = min(10.0, (total_detections / threshold) * 10)
                level = "critical" if intensity >= 7 else "warning" if intensity >= 5 else "info"
            elif total_detections > 50:
                level = "critical"
                intensity = 9.0
            elif total_detections > 25:
                level = "warning"
                intensity = 7.0

            event = {
                "type": "color_detection",
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": level,
                "intensity": round(intensity, 1),
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7}
                },
                "application_name": "Color Detection System",
                "application_version": "1.2",
                "location_info": None,
                "human_text": (
                    f"Event: Color Detection\nLevel: {level.title()}\n"
                    f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC')}\n"
                    f"Detections: {total_detections} objects analyzed\n"
                    f"Unique Colors: {len(color_summary.get('color_distribution', {}))}\n"
                    f"Intensity: {intensity:.1f}/10"
                )
            }
            frame_events.append(event)

        for alert in alerts:
            alert_event = {
                "type": alert.get("type", "color_alert"),
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": alert.get("severity", "warning"),
                "intensity": 8.0,
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7}
                },
                "application_name": "Color Detection Alert System",
                "application_version": "1.2",
                "location_info": alert.get("category"),
                "human_text": f"Event: {alert.get('type', 'Color Alert').title()}\nMessage: {alert.get('message', 'Color detection alert triggered')}"
            }
            frame_events.append(alert_event)

        return events

    def _generate_tracking_stats(
            self,
            new_color_summary: Dict,
            counting_summary: Dict,
            alerts: Any,
            config: ColorDetectionConfig,
            curr_frame_color: Any,
            total_color_data: Any,
            frame_number: Optional[int] = None,
            stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        """Generate structured tracking stats for the output format with frame-based keys, including track_ids_info and detections with masks."""
        # frame_key = str(frame_number) if frame_number is not None else "current_frame"
        # tracking_stats = [{frame_key: []}]
        # frame_tracking_stats = tracking_stats[0][frame_key]
        tracking_stats = []

        total_detections = counting_summary.get("total_count", 0)
        total_color_counts_dict = counting_summary.get("total_color_counts", {})
        total_category_counts_dict = counting_summary.get("total_category_counts", {})
        # cumulative_total = sum(total_color_counts_dict.values()) if total_color_counts_dict else 0
        per_category_count = counting_summary.get("per_category_count", {})

        # Compute current color counts from detections
        current_color_count: Dict[str, int] = {}
        for det in counting_summary.get("detections", []):
            color = det.get("main_color")
            if color:
                current_color_count[color] = current_color_count.get(color, 0) + 1

        track_ids_info = self._get_track_ids_info(counting_summary.get("detections", []))

        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)

        # Create high precision timestamps for input_timestamp and reset_timestamp
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        camera_info = self.get_camera_info_from_stream(stream_info)
        # total_color_data = self.color_helper(curr_frame_color)

        human_text_lines = []
        color_counts = {}

        if curr_frame_color:
            for tid, data in curr_frame_color.items():
                color = data.get("color")
                if color not in color_counts:
                    color_counts[color] = 0
                color_counts[color] += 1
        zone_frame_data = {}
        if curr_frame_color:
            for tid, data in curr_frame_color.items():
                zone = data.get("zone_name", "Unknown_Zone")
                color = data.get("color", "unknown")
                category = data.get("object_label", "unknown")

                if zone not in zone_frame_data:
                    zone_frame_data[zone] = {
                        "color_counts": {},
                        "category_counts": {}
                    }

                # Count colors
                zone_frame_data[zone]["color_counts"][color] = (
                    zone_frame_data[zone]["color_counts"].get(color, 0) + 1
                )

                # Count vehicle types
                zone_frame_data[zone]["category_counts"][category] = (
                    zone_frame_data[zone]["category_counts"].get(category, 0) + 1
                )

        # CURRENT FRAME section
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
        if not curr_frame_color or total_detections == 0:
            human_text_lines.append(f"\t- No detections")
        else:
            for zone_name, stats in zone_frame_data.items():
                color_counts = stats["color_counts"]
                per_category_count = stats["category_counts"]
                if config.zone_config:
                    human_text_lines.append(f"\t{zone_name}:")
                if per_category_count:
                    category_counts = [f"{count} {cat}" for cat, count in per_category_count.items()]
                    if len(category_counts) == 1:
                        detection_text = category_counts[0] + " detected"
                    elif len(category_counts) == 2:
                        detection_text = f"{category_counts[0]} and {category_counts[1]} detected"
                    else:
                        detection_text = f"{', '.join(category_counts[:-1])}, and {category_counts[-1]} detected"
                    human_text_lines.append(f"\t\t- {detection_text}")

                if color_counts:
                    color_counts_text = ", ".join([f"{count} {color}" for color, count in color_counts.items()])
                    human_text_lines.append(f"\t\t- Colors: {color_counts_text}")

        human_text_lines.append("")  # spacing

        cumulative_total = sum(self.all_color_counts.values())
        stats = self.zone_vehicle_stats

        # TOTAL SINCE section
        # human_text_lines.append(f"TOTAL SINCE {start_timestamp}:")
        # for zone_name, vehicles in stats.items():
        #     total_in_zone = sum(sum(colors.values()) for colors in vehicles.values())
        #     if config.zone_config:
        #         human_text_lines.append(f"\t{zone_name}:")
        #     human_text_lines.append(f"\t\t- Total Detected: {total_in_zone}")

        #     for vehicle_type, colors in vehicles.items():
        #         total_type_count = sum(colors.values())
        #         human_text_lines.append(f"\t\t- {vehicle_type}: {total_type_count}")
        #         for color, count in colors.items():
        #             human_text_lines.append(f"\t\t\t- {color}: {count}")

        current_counts_categories = []
        for cat, count in per_category_count.items():
            if count > 0 or total_detections > 0:
                current_counts_categories.append({"category": cat, "count": count})
        current_counts_colors = []
        for color, count in current_color_count.items():
            if count > 0 or total_detections > 0:
                current_counts_colors.append({"color": color, "count": count})
        total_counts_categories = []
        for cat, count in total_category_counts_dict.items():
            if count > 0 or cumulative_total > 0:
                total_counts_categories.append({"category": cat, "count": count})
        total_counts_colors = []
        for color, count in total_color_counts_dict.items():
            if count > 0 or cumulative_total > 0:
                total_counts_colors.append({"category": color, "count": count})

        human_text = "\n".join(human_text_lines)

        # Include detections with masks from counting_summary
        # Prepare detections without confidence scores (as per eg.json)
        detections = []
        for detection in new_color_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("main_color", "No_color")
            # Include segmentation if available (like in eg.json)
            if detection.get("masks"):
                segmentation= detection.get("masks", [])
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            elif detection.get("segmentation"):
                segmentation= detection.get("segmentation")
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            elif detection.get("mask"):
                segmentation= detection.get("mask")
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            else:
                detection_obj = self.create_detection_object(category, bbox)
            detections.append(detection_obj)

        # Build alert_settings array in expected format
        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, 'alert_type'):
            alert_settings.append({
                "alert_type": getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                "incident_category": self.CASE_TYPE,
                "threshold_level": config.alert_config.count_thresholds if hasattr(config.alert_config, 'count_thresholds') else {},
                "ascending": True,
                "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                                    getattr(config.alert_config, 'alert_value', ['JSON']) if hasattr(config.alert_config, 'alert_value') else ['JSON'])
                            }
            })

        # if alerts:
        #     for alert in alerts:
        #         human_text_lines.append(f"Alerts: {alert.get('settings', {})} sent @ {current_timestamp}")
        # else:
        #     human_text_lines.append("Alerts: None")

        # human_text = "\n".join(human_text_lines)
        reset_settings = [
                {
                    "interval_type": "daily",
                    "reset_time": {
                        "value": 9,
                        "time_unit": "hour"
                    }
                }
            ]


        # Keep backward-compat: put colors into total_counts and categories into current_counts
        tracking_stat=self.create_tracking_stats(total_counts=total_counts_colors, current_counts=current_counts_categories,
                            detections=detections, human_text=human_text, camera_info=camera_info, alerts=alerts, alert_settings=alert_settings,
                            reset_settings=reset_settings, start_time=high_precision_start_timestamp ,
                            reset_time=high_precision_reset_timestamp)
        tracking_stat['target_categories'] = self.target_categories

        tracking_stats.append(tracking_stat)
        return tracking_stats


    def reset_tracker(self) -> None:
        """Reset the advanced tracker instance."""
        if self.tracker is not None:
            self.tracker.reset()
            self.logger.info("AdvancedTracker reset for new tracking session")

    def reset_color_tracking(self) -> None:
        """Reset color tracking state."""
        self._color_total_track_ids = defaultdict(set)
        self._color_current_frame_track_ids = defaultdict(set)
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self.logger.info("Color tracking state reset")

    def reset_all_tracking(self) -> None:
        """Reset both advanced tracker and color tracking state."""
        self.reset_tracker()
        self.reset_color_tracking()
        self.logger.info("All color tracking state reset")

    def _is_in_zone(self, bbox: Dict[str, Any], zone_polygon: List[List[int]]) -> bool:
        """Check if the bottom 25% center point of a bounding box lies within the given zone polygon."""
        if not zone_polygon or not isinstance(bbox, dict):
            return True  # No zone defined, or invalid bbox, process all detections
        try:
            # Get bottom 25% center point
            center_point = get_bbox_bottom25_center(bbox)
            # Convert zone polygon to list of tuples
            polygon_points = [(point[0], point[1]) for point in zone_polygon]
            # Check if point is inside polygon
            in_zone = point_in_polygon(center_point, polygon_points)
            self.logger.debug(f"BBox center {center_point} in zone: {in_zone}")
            return in_zone
        except (KeyError, TypeError) as e:
            self.logger.warning(f"Failed to check zone for bbox {bbox}: {e}")
            return False

    @staticmethod
    def _iou(bbox1, bbox2):
        """Compute IoU between two bboxes (dicts with xmin/ymin/xmax/ymax or x/y/width/height)."""
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
        """Suppress duplicate/overlapping detections with same category and high IoU."""
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
                    if bbox1 and bbox2 and ColorDetectionUseCase._iou(bbox1, bbox2) > iou_thresh:
                        used[j] = True
                        group.append(j)
            best_idx = max(group, key=lambda idx: detections[idx].get("confidence", 0))
            filtered.append(detections[best_idx])
            used[best_idx] = True
        return filtered

    def get_config_schema(self) -> Dict[str, Any]:
        """Get JSON schema for configuration validation."""
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {"type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.5},
                "top_k_colors": {"type": "integer", "minimum": 1, "default": 3},
                "frame_skip": {"type": "integer", "minimum": 1, "default": 1},
                "target_categories": {"type": ["array", "null"], "items": {"type": "string"}, "default": [
                    "car", "bicycle", "bus", "motorcycle"
                ]},
                "fps": {"type": ["number", "null"], "minimum": 1.0, "default": None},
                "bbox_format": {"type": "string", "enum": ["auto", "xmin_ymin_xmax_ymax", "x_y_width_height"], "default": "auto"},
                "index_to_category": {"type": ["object", "null"], "default": None},
                "alert_config": {"type": ["object", "null"], "default": None}
            },
            "required": ["confidence_threshold", "top_k_colors"],
            "additionalProperties": False
        }

    def create_default_config(self, **overrides) -> ColorDetectionConfig:
        """Create default configuration with optional overrides."""
        defaults = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.5,
            "top_k_colors": 3,
            "frame_skip": 1,
            "target_categories": [
                "car", "bicycle", "bus", "motorcycle"
            ],
            "fps": None,
            "bbox_format": "auto",
            "index_to_category": None,
            "alert_config": None
        }
        defaults.update(overrides)
        return ColorDetectionConfig(**defaults)

    def _update_color_tracking_state(self, detections: List[Dict]):
        """Track unique track_ids per category and color for total count."""
        # Ensure storage is a defaultdict(set) to allow safe .add()
        existing_store = getattr(self, '_color_total_track_ids', None)
        if not isinstance(existing_store, defaultdict):
            existing_store = {} if existing_store is None else dict(existing_store)
            self._color_total_track_ids = defaultdict(set, existing_store)
        else:
            self._color_total_track_ids = existing_store
        self._color_current_frame_track_ids = defaultdict(set)
        for det in detections:
            cat = det.get('category')
            color = det.get('main_color')
            track_id = det.get('track_id')
            if cat and track_id is not None:
                key = f"{cat}:{color}" if color else cat
                self._color_total_track_ids[key].add(track_id)
                self._color_current_frame_track_ids[key].add(track_id)

    def get_total_color_counts(self):
        """Return total unique track_id count per color (across all categories)."""
        store = getattr(self, '_color_total_track_ids', {})
        if not isinstance(store, dict):
            return {}
        color_to_ids = defaultdict(set)
        for key, id_set in store.items():
            if isinstance(key, str) and ':' in key:
                _, color = key.split(':', 1)
            else:
                color = None
            # Support both set and iterable
            ids = id_set if isinstance(id_set, set) else set(id_set or [])
            if color:
                color_to_ids[color].update(ids)
        return {color: len(ids) for color, ids in color_to_ids.items()}

    def get_total_category_counts(self,data):
        """Return total unique track_id count per category (across all colors)."""
        for det in data:
            track_id = det.get("track_id")
            category = det.get("category")
            if track_id and category:
                if category not in self.total_category_count:
                    self.total_category_count[category] = set()
                self.total_category_count[category].add(track_id)

        # Convert sets to counts
        return {cat: len(track_ids) for cat, track_ids in self.total_category_count.items()}


    def _get_track_ids_info(self, detections: List[Dict]) -> Dict[str, Any]:
        """Get detailed information about track IDs for color detections (per frame)."""
        frame_track_ids = set(det.get('track_id') for det in detections if det.get('track_id') is not None)
        total_track_ids = set()
        for s in getattr(self, '_color_total_track_ids', {}).values():
            total_track_ids.update(s)
        return {
            "total_count": len(total_track_ids),
            "current_frame_count": len(frame_track_ids),
            "total_unique_track_ids": len(total_track_ids),
            "current_frame_track_ids": list(frame_track_ids),
            "last_update_time": time.time(),
            "total_frames_processed": getattr(self, '_total_frame_counter', 0)
        }

    def _attach_masks_to_detections(
            self,
            processed_detections: List[Dict[str, Any]],
            raw_detections: List[Dict[str, Any]],
            iou_threshold: float = 0.5,
        ) -> List[Dict[str, Any]]:
            """
            Attach segmentation masks from the original `raw_detections` list to the
            `processed_detections` list returned after smoothing/tracking.

            Matching between detections is performed using Intersection-over-Union
            (IoU) of the bounding boxes. For each processed detection we select the
            raw detection with the highest IoU above `iou_threshold` and copy its
            `masks` (or `mask`) field. If no suitable match is found, the detection
            keeps an empty list for `masks` to maintain a consistent schema.
            """

            if not processed_detections or not raw_detections:
                # Nothing to do – ensure masks key exists for downstream logic.
                for det in processed_detections:
                    det.setdefault("masks", [])
                return processed_detections

            # Track which raw detections have already been matched to avoid
            # assigning the same mask to multiple processed detections.
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
                    # No adequate match – default to empty list to keep schema consistent.
                    det.setdefault("masks", ["EMPTY"])

            return processed_detections

    def _generate_incidents(self, counting_summary: Dict, alerts: List, config: ColorDetectionConfig,
                        frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """Generate structured events for the output format with frame-based keys."""

        # Use frame number as key, fallback to 'current_frame' if not available
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        incidents=[]
        total_detections = counting_summary.get("total_count", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        self._ascending_alert_list = self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list

        if total_detections > 0:
            # Determine event level based on thresholds
            level = "low"
            intensity = 5.0
            start_timestamp = self._get_start_timestamp_str(stream_info)
            if start_timestamp and self.current_incident_end_timestamp=='N/A':
                self.current_incident_end_timestamp = 'Incident still active'
            elif start_timestamp and self.current_incident_end_timestamp=='Incident still active':
                if len(self._ascending_alert_list) >= 15 and sum(self._ascending_alert_list[-15:]) / 15 < 1.5:
                    self.current_incident_end_timestamp = current_timestamp
            elif self.current_incident_end_timestamp!='Incident still active' and self.current_incident_end_timestamp!='N/A':
                self.current_incident_end_timestamp = 'N/A'

            if config.alert_config and hasattr(config.alert_config, 'count_thresholds') and config.alert_config.count_thresholds:
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

            # Generate human text in new format
            human_text_lines = [f"INCIDENTS DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE,level)}")
            human_text = "\n".join(human_text_lines)

            alert_settings=[]
            if config.alert_config and hasattr(config.alert_config, 'alert_type'):
                alert_settings.append({
                    "alert_type": getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": config.alert_config.count_thresholds if hasattr(config.alert_config, 'count_thresholds') else {},
                    "ascending": True,
                    "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                                        getattr(config.alert_config, 'alert_value', ['JSON']) if hasattr(config.alert_config, 'alert_value') else ['JSON'])
                                }
                })

            event= self.create_incident(incident_id=self.CASE_TYPE+'_'+str(frame_number), incident_type=self.CASE_TYPE,
                        severity_level=level, human_text=human_text, camera_info=camera_info, alerts=alerts, alert_settings=alert_settings,
                        start_time=start_timestamp, end_time=self.current_incident_end_timestamp,
                        level_settings= {"low": 1, "medium": 3, "significant":4, "critical": 7})
            incidents.append(event)

        else:
            self._ascending_alert_list.append(0)
            incidents.append({})

        return incidents

    def _check_alerts(self, summary: dict, frame_number:Any, config: ColorDetectionConfig) -> List[Dict]:
        """
        Check if any alert thresholds are exceeded and return alert dicts.
        """
        def get_trend(data, lookback=900, threshold=0.6):
            '''
            Determine if the trend is ascending or descending based on actual value progression.
            Now works with values 0,1,2,3 (not just binary).
            '''
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

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts = []
        total_detections = summary.get("total_count", 0) #CURRENT combined total count of all classes
        total_counts_dict = summary.get("total_color_counts", {}) #TOTAL cumulative counts per class
        if isinstance(total_counts_dict, int):
            total_counts_dict = {}
        cumulative_total = sum(total_counts_dict.values()) if total_counts_dict else 0 #TOTAL combined cumulative count
        per_category_count = summary.get("per_category_count", {}) #CURRENT count per class

        if not config.alert_config:
            return alerts

        total = summary.get("total_count", 0)
        #self._ascending_alert_list
        if hasattr(config.alert_config, 'count_thresholds') and config.alert_config.count_thresholds:

            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total > threshold:

                    alerts.append({
                        "alert_type": getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                        "alert_id": "alert_"+category+'_'+frame_key,
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": threshold,
                        "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                        "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                                    getattr(config.alert_config, 'alert_value', ['JSON']) if hasattr(config.alert_config, 'alert_value') else ['JSON'])
                                }
                    })
                elif category in summary.get("per_category_count", {}):
                    count = summary.get("per_category_count", {})[category]
                    if count > threshold:  # Fixed logic: alert when EXCEEDING threshold
                        alerts.append({
                            "alert_type": getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                            "alert_id": "alert_"+category+'_'+frame_key,
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                            "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                                    getattr(config.alert_config, 'alert_value', ['JSON']) if hasattr(config.alert_config, 'alert_value') else ['JSON'])
                                }
                        })
        else:
            pass
        return alerts

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        """Format timestamp for streams (YYYY:MM:DD HH:MM:SS format)."""
        dt = datetime.fromtimestamp(float(timestamp), tz=timezone.utc)
        return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        """Format timestamp for video chunks (HH:MM:SS.ms format)."""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60),2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp to match the current timestamp format: YYYY:MM:DD HH:MM:SS.

        The input can be either:
        1. A numeric Unix timestamp (``float`` / ``int``) – it will be converted to datetime.
        2. A string in the format ``YYYY-MM-DD-HH:MM:SS.ffffff UTC``.

        The returned value will be in the format: YYYY:MM:DD HH:MM:SS (no milliseconds, no UTC suffix).

        Example
        -------
        >>> self._format_timestamp("2025-10-27-19:31:20.187574 UTC")
        '2025:10:27 19:31:20'
        """

        # Convert numeric timestamps to datetime first
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp, timezone.utc)
            return dt.strftime('%Y:%m:%d %H:%M:%S')

        # Ensure we are working with a string from here on
        if not isinstance(timestamp, str):
            return str(timestamp)

        # Remove ' UTC' suffix if present
        timestamp_clean = timestamp.replace(' UTC', '').strip()

        # Remove milliseconds if present (everything after the last dot)
        if '.' in timestamp_clean:
            timestamp_clean = timestamp_clean.split('.')[0]

        # Parse the timestamp string and convert to desired format
        try:
            # Handle format: YYYY-MM-DD-HH:MM:SS
            if timestamp_clean.count('-') >= 2:
                # Replace first two dashes with colons for date part, third with space
                parts = timestamp_clean.split('-')
                if len(parts) >= 4:
                    # parts = ['2025', '10', '27', '19:31:20']
                    formatted = f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
                    return formatted
        except Exception:
            pass

        # If parsing fails, return the cleaned string as-is
        return timestamp_clean

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
            # Prefer direct input_settings.stream_time if available and not NA
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                # Fallback to nested stream_info.stream_time used by current timestamp path
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(self._tracking_start_time, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                    except:
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
                    except:
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

    def _update_zone_tracking(self, zone_analysis: Dict[str, Dict[str, int]], detections: List[Dict], config: ColorDetectionConfig) -> Dict[str, Dict[str, Any]]:
        """Update zone tracking with current frame data."""
        if not zone_analysis or not config.zone_config or not config.zone_config['zones']:
            return {}

        enhanced_zone_analysis = {}
        zones = config.zone_config['zones']

        # Initialize current frame zone tracks
        current_frame_zone_tracks = {zone_name: set() for zone_name in zones.keys()}

        # Initialize zone tracking storage
        for zone_name in zones.keys():
            if zone_name not in self._zone_current_track_ids:
                self._zone_current_track_ids[zone_name] = set()
            if zone_name not in self._zone_total_track_ids:
                self._zone_total_track_ids[zone_name] = set()

        # Check each detection against each zone
        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None:
                continue

            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue

            # Check which zone this detection is in
            for zone_name, zone_polygon in zones.items():
                if self._is_in_zone(bbox, zone_polygon):
                    current_frame_zone_tracks[zone_name].add(track_id)
                    if track_id not in self.color_det_dict:  # Use color_det_dict for consistency
                        self.color_det_dict[track_id] = [detection.get("main_color", "unknown"), detection.get("confidence", 0.0)]

        # Update zone tracking for each zone
        for zone_name, zone_counts in zone_analysis.items():
            current_tracks = current_frame_zone_tracks.get(zone_name, set())
            self._zone_current_track_ids[zone_name] = current_tracks
            self._zone_total_track_ids[zone_name].update(current_tracks)
            self._zone_current_counts[zone_name] = len(current_tracks)
            self._zone_total_counts[zone_name] = len(self._zone_total_track_ids[zone_name])

            enhanced_zone_analysis[zone_name] = {
                "current_count": self._zone_current_counts[zone_name],
                "total_count": self._zone_total_counts[zone_name],
                "current_track_ids": list(current_tracks),
                "total_track_ids": list(self._zone_total_track_ids[zone_name]),
                "original_counts": zone_counts
            }

        return enhanced_zone_analysis

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