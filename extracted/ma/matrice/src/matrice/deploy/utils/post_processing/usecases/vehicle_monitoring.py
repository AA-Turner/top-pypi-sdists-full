"""
Vehicle Monitoring Use Case for Post-Processing

This module provides vehicle monitoring functionality with congestion detection,
zone analysis, and alert generation.

"""

from typing import Any, Dict, List, Optional
from dataclasses import asdict
import time
from datetime import datetime, timezone

from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol, ResultFormat
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
from dataclasses import dataclass, field
from ..core.config import BaseConfig, AlertConfig, ZoneConfig

@dataclass
class VehicleMonitoringConfig(BaseConfig):
    """Configuration for license plate detection use case in vehicle monitoring."""
    # Smoothing configuration
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    
    # Vehicle confidence thresholds
    confidence_threshold: float = 0.6

    
    vehicle_categories: List[str] = field(
        default_factory=lambda: ['bicycle', 'car', 'motorbike', 'auto rickshaw', 'bus',  'garbagevan', 'truck', 'minibus', 'army vehicle', 'pickup', 'policecar', 'rickshaw', 'scooter', 'suv', 'taxi', 'three wheelers -CNG-', 'human hauler', 'van', 'wheelbarrow']
    )

    target_vehicle_categories: List[str] = field(
        default_factory=lambda: ['car', 'bicycle', 'bus', 'garbagevan', 'truck', 'motorbike', 'van']
    )


    alert_config: Optional[AlertConfig] = None
    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            1: "bicycle",
            2: "car",
            3: "motorbike",
            4: "auto rickshaw",
            5: "bus",
            6: "garbagevan",
            7: "truck",
            8: "minibus",
            10: "army vehicle",
            11: "pickup",
            12: "policecar",
            13: "rickshaw",
            14: "scooter",
            15: "suv",
            16: "taxi",
            17: "three wheelers -CNG-",
            18: "human hauler",
            19: "van",
            20: "wheelbarrow",
        }
    )

class VehicleMonitoringUseCase(BaseProcessor):
    def _get_track_ids_info(self, detections: list) -> Dict[str, Any]:
        """
        Get detailed information about track IDs for Vehicles (per frame).
        """
        # Collect all track_ids in this frame
        frame_track_ids = set()
        for det in detections:
            tid = det.get('track_id')
            if tid is not None:
                frame_track_ids.add(tid)
        # Use persistent total set for unique counting
        total_track_ids = set()
        for s in getattr(self, '_vehicle_total_track_ids', {}).values():
            total_track_ids.update(s)
        return {
            "total_count": len(total_track_ids),
            "current_frame_count": len(frame_track_ids),
            "total_unique_track_ids": len(total_track_ids),
            "current_frame_track_ids": list(frame_track_ids),
            "last_update_time": time.time(),
            "total_frames_processed": getattr(self, '_total_frame_counter', 0)
        }

    @staticmethod
    def _iou(bbox1, bbox2):
        """Compute IoU between two bboxes (dicts with xmin/ymin/xmax/ymax)."""
        x1 = max(bbox1["xmin"], bbox2["xmin"])
        y1 = max(bbox1["ymin"], bbox2["ymin"])
        x2 = min(bbox1["xmax"], bbox2["xmax"])
        y2 = min(bbox1["ymax"], bbox2["ymax"])
        inter_w = max(0, x2 - x1)
        inter_h = max(0, y2 - y1)
        inter_area = inter_w * inter_h
        area1 = (bbox1["xmax"] - bbox1["xmin"]) * (bbox1["ymax"] - bbox1["ymin"])
        area2 = (bbox2["xmax"] - bbox2["xmin"]) * (bbox2["ymax"] - bbox2["ymin"])
        union = area1 + area2 - inter_area
        if union == 0:
            return 0.0
        return inter_area / union

    @staticmethod
    def _deduplicate_vehicles(detections, iou_thresh=0.7):
        """Suppress duplicate/overlapping vehicles with same label and high IoU."""
        filtered = []
        used = [False] * len(detections)
        for i, det in enumerate(detections):
            if used[i]:
                continue
            group = [i]
            for j in range(i+1, len(detections)):
                if used[j]:
                    continue
                if det.get("category") == detections[j].get("category"):
                    bbox1 = det.get("bounding_box")
                    bbox2 = detections[j].get("bounding_box")
                    if bbox1 and bbox2:
                        iou = VehicleMonitoringUseCase._iou(bbox1, bbox2)
                        if iou > iou_thresh:
                            used[j] = True
                            group.append(j)
            # Keep the highest confidence detection in the group
            best_idx = max(group, key=lambda idx: detections[idx].get("confidence", 0))
            filtered.append(detections[best_idx])
            used[best_idx] = True
        return filtered
    def _update_vehicle_tracking_state(self, detections: list):
        """
        Track unique vehicle track_ids per category for total count after tracking.
        """
        self._vehicle_total_track_ids = getattr(self, '_vehicle_total_track_ids', {cat: set() for cat in self.vehicle_categories})
        self._vehicle_current_frame_track_ids = {cat: set() for cat in self.vehicle_categories}
        for det in detections:
            cat = det.get('category')
            track_id = det.get('track_id')
            if cat in self.vehicle_categories and track_id is not None:
                self._vehicle_total_track_ids[cat].add(track_id)
                self._vehicle_current_frame_track_ids[cat].add(track_id)

    def get_total_vehicle_counts(self):
        """
        Return total unique track_id count for each vehicle category.
        """
        return {cat: len(ids) for cat, ids in getattr(self, '_vehicle_total_track_ids', {}).items()}

    """Vehicle Monitoring use case with vehicle smoothing and alerting."""

    def __init__(self):
        super().__init__("vehicle_monitoring")
        self.category = "traffic"
        
        # List of vehicle categories to track
        self.vehicle_categories = ['bicycle', 'car', 'motorbike', 'auto rickshaw', 'bus',  'garbagevan', 'truck', 'minibus', 'army vehicle', 'pickup', 'policecar', 'rickshaw', 'scooter', 'suv', 'taxi', 'three wheelers -CNG-', 'human hauler', 'van', 'wheelbarrow']
        
        # Initialize smoothing tracker
        self.smoothing_tracker = None
        
        # Initialize advanced tracker (will be created on first use)
        self.tracker = None
        
        # Initialize tracking state variables
        self._total_frame_counter = 0
        self._global_frame_offset = 0

    def process(self, data: Any, config: ConfigProtocol, context: Optional[ProcessingContext] = None, stream_info: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        """
        Main entry point for Vehicle Monitoring post-processing.
        Applies category mapping, vehicle smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        start_time = time.time()
        # Ensure config is correct type
        if not isinstance(config, VehicleMonitoringConfig):
            return self.create_error_result("Invalid config type", usecase=self.name, category=self.category, context=context)
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
                self.logger.debug(f"Did not apply confidence filtering with threshold since nothing was provided")
            
        # Step 2: Apply category mapping if provided
        if config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
                self.logger.debug("Applied category mapping")


        if config.target_vehicle_categories:
                processed_data = [d for d in processed_data if d.get('category') in self.vehicle_categories]
                self.logger.debug(f"Applied vehicle category filtering")

        # Apply bbox smoothing if enabled
        if config.enable_smoothing:
            if self.smoothing_tracker is None:
                smoothing_config = BBoxSmoothingConfig(
                    smoothing_algorithm=config.smoothing_algorithm,
                    window_size=config.smoothing_window_size,
                    cooldown_frames=config.smoothing_cooldown_frames,
                    confidence_threshold=config.confidence_threshold,  # Use mask threshold as default
                    confidence_range_factor=config.smoothing_confidence_range_factor,
                    enable_smoothing=True
                )
                self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
            smoothed_vehicles = bbox_smoothing(processed_data, self.smoothing_tracker.config, self.smoothing_tracker)
            processed_data = smoothed_vehicles

        # Advanced tracking (BYTETracker-like)
        try:
            from ..advanced_tracker import AdvancedTracker
            from ..advanced_tracker.config import TrackerConfig
            
            # Create tracker instance if it doesn't exist (preserves state across frames)
            if self.tracker is None:
                tracker_config = TrackerConfig()
                self.tracker = AdvancedTracker(tracker_config)
                self.logger.info("Initialized AdvancedTracker for Vehicle Monitoring and tracking")
            
            # The tracker expects the data in the same format as input
            # It will add track_id and frame_id to each detection
            processed_data = self.tracker.update(processed_data)
            
        except Exception as e:
            # If advanced tracker fails, fallback to unsmoothed detections
            self.logger.warning(f"AdvancedTracker failed: {e}")

        # Deduplicate overlapping vehicles (same label, high IoU)
        # processed_data = self._deduplicate_vehicles(processed_data, iou_thresh=0.92)

        # Update vehicle tracking state for total count per label
        self._update_vehicle_tracking_state(processed_data)
        
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
        general_counting_summary = calculate_counting_summary(data)
        counting_summary = self._count_categories(processed_data, config)
        # Add total unique vehicle counts after tracking using only local state
        total_vehicle_counts = self.get_total_vehicle_counts()
        counting_summary['total_vehicle_counts'] = total_vehicle_counts
        insights = self._generate_insights(counting_summary, config)
        alerts = self._check_alerts(counting_summary, config)
        predictions = self._extract_predictions(processed_data)
        summary = self._generate_summary(counting_summary, alerts)

        # Step: Generate structured events and tracking stats with frame-based keys
        events_list = self._generate_events(counting_summary, alerts, config, frame_number)
        tracking_stats_list = self._generate_tracking_stats(counting_summary, insights, summary, config, frame_number)

        # Extract frame-based dictionaries from the lists
        events = events_list[0] if events_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}

        context.mark_completed()

        # Build result object
        result = self.create_result(
            data={
                "counting_summary": counting_summary,
                "general_counting_summary": general_counting_summary,
                "alerts": alerts,
                "total_vehicles": counting_summary.get("total_count", 0),
                "events": events,
                "tracking_stats": tracking_stats,
            },
            usecase=self.name,
            category=self.category,
            context=context
        )
        result.summary = summary
        result.insights = insights
        result.predictions = predictions
        return result
    
    def reset_tracker(self) -> None:
        """
        Reset the advanced tracker instance.
        
        This should be called when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        """
        if self.tracker is not None:
            self.tracker.reset()
            self.logger.info("AdvancedTracker reset for new tracking session")
    
    def reset_vehicle_tracking(self) -> None:
        """
        Reset vehicle tracking state (total counts, track IDs, etc.).
        
        This should be called when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        """
        self._vehicle_total_track_ids = {cat: set() for cat in self.vehicle_categories}
        self._total_frame_counter = 0
        self._global_frame_offset = 0
        self.logger.info("Vehicle Monitoring tracking state reset")
    
    def reset_all_tracking(self) -> None:
        """
        Reset both advanced tracker and vehicle tracking state.
        """
        self.reset_tracker()
        self.reset_vehicle_tracking()
        self.logger.info("All Vehicles tracking state reset")
        
    def _generate_events(self, counting_summary: Dict, alerts: List, config: VehicleMonitoringConfig, frame_number: Optional[int] = None) -> List[Dict]:
        """Generate structured events for the output format with frame-based keys."""
        from datetime import datetime, timezone

        # Use frame number as key, fallback to 'current_frame' if not available
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        events = [{frame_key: []}]
        frame_events = events[0][frame_key]
        total_vehicles = counting_summary.get("total_count", 0)

        if total_vehicles > 0:
            # Determine event level based on thresholds
            level = "info"
            intensity = 5.0
            if config.alert_config and config.alert_config.count_thresholds:
                threshold = config.alert_config.count_thresholds.get("all", 15)
                intensity = min(10.0, (total_vehicles / threshold) * 10)
                
                if intensity >= 7:
                    level = "critical"
                elif intensity >= 5:
                    level = "warning"
                else:
                    level = "info"
            else:
                if total_vehicles > 25:
                    level = "critical"
                    intensity = 9.0
                elif total_vehicles > 15:
                    level = "warning" 
                    intensity = 7.0
                else:
                    level = "info"
                    intensity = min(10.0, total_vehicles / 3.0)

            event = {
                "type": "vehicle_monitoring",
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": level,
                "intensity": round(intensity, 1),
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7}
                },
                "application_name": "Vehicle Monitoring System",
                "application_version": "1.2",
                "location_info": None,
                "human_text": f"{total_vehicles} vehicles detected"
            }
            frame_events.append(event)

        # Add alert events
        for alert in alerts:
            total_vehicles = counting_summary.get("total_count", 0)
            intensity_message = "ALERT: Low congestion in the scene"
            if config.alert_config and config.alert_config.count_thresholds:
                threshold = config.alert_config.count_thresholds.get("all", 15)
                percentage = (total_vehicles / threshold) * 100 if threshold > 0 else 0
                if percentage < 20:
                    intensity_message = "ALERT: Low congestion in the scene"
                elif percentage <= 50:
                    intensity_message = "ALERT: Moderate congestion in the scene"
                elif percentage <= 70:
                    intensity_message = "ALERT: Heavy congestion in the scene"
                else:
                    intensity_message = "ALERT: Severe congestion in the scene"
            else:
                if total_vehicles > 15:
                    intensity_message = "ALERT: Heavy congestion in the scene"
                elif total_vehicles == 1:
                    intensity_message = "ALERT: Low congestion in the scene"
                else:
                    intensity_message = "ALERT: Moderate congestion in the scene"

            alert_event = {
                "type": alert.get("type", "congestion_alert"),
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": alert.get("severity", "warning"),
                "intensity": 8.0,
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7}
                },
                "application_name": "Congestion Alert System",
                "application_version": "1.2",
                "location_info": alert.get("zone"),
                "human_text": f"{datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC')} : {intensity_message}"
            }
            frame_events.append(alert_event)

        return events


    def _generate_tracking_stats(self, counting_summary: Dict, insights: List[str], summary: str, config: VehicleMonitoringConfig, frame_number: Optional[int] = None) -> List[Dict]:
        """Generate structured tracking stats for the output format with frame-based keys, including track_ids_info."""
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        tracking_stats = [{frame_key: []}]
        frame_tracking_stats = tracking_stats[0][frame_key]
        total_vehicles = counting_summary.get("total_count", 0)

        if total_vehicles > 0:
            # Add detailed track_ids_info (like people_counting)
            track_ids_info = self._get_track_ids_info(counting_summary.get("detections", []))
            tracking_stat = {
                "type": "vehicle_tracking",
                "category": "vehicle",
                "count": total_vehicles,
                "insights": insights,
                "summary": summary,
                "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC'),
                "human_text": summary,
                "track_ids_info": track_ids_info,
                "global_frame_offset": getattr(self, '_global_frame_offset', 0),
                "local_frame_id": frame_key
            }
            frame_tracking_stats.append(tracking_stat)

        return tracking_stats



    def _count_categories(self, detections: list, config: VehicleMonitoringConfig) -> dict:
        """
        Count the number of detections per category and return a summary dict.
        The detections list is expected to have 'track_id' (from tracker), 'category', 'bounding_box', etc.
        Output structure will include 'track_id' for each detection as per AdvancedTracker output.
        """
        counts = {}
        for det in detections:
            cat = det.get('category', 'unknown')
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
                    "frame_id": det.get("frame_id")
                }
                for det in detections
            ]
        }

    # Human-friendly display names for vehicle categories
    CATEGORY_DISPLAY = {
        "Bicycle": "bicycle",
        "Car": "car",
        "Motorbike": "motorbike",
        "Tuk-Tuk": "auto rickshaw",
        "Bus": "bus",
        "Garbage Van": "garbagevan",
        "Truck": "truck",
        "Minibus": "minibus",
        "Army Vehicle": "army vehicle",
        "Pickup": "pickup",
        "Police Car": "policecar",
        "Tuk-Tuk": "rickshaw",
        "Scooter Bike": "scooter",
        "SUV": "suv",
        "Taxi": "taxi",
        "Three Wheeler CNG": "three wheelers -CNG-",
        "Human Hauler": "human hauler",
        "Van": "van",
        "Wheelbarrow": "wheelbarrow",
        }

    def _generate_insights(self, summary: dict, config: VehicleMonitoringConfig) -> List[str]:
        """
        Generate human-readable insights for each vehicle category.
        """
        insights = []
        per_cat = summary.get("per_category_count", {})
        total_vehicles = summary.get("total_count", 0)

        if total_vehicles == 0:
            insights.append("No vehicles detected in the scene")
            return insights
        insights.append(f"EVENT: Detected {total_vehicles} vehicles in the scene")
        # Intensity calculation based on threshold percentage
        intensity_threshold = None
        if (config.alert_config and 
            config.alert_config.count_thresholds and 
            "all" in config.alert_config.count_thresholds):
            intensity_threshold = config.alert_config.count_thresholds["all"]
        
        if intensity_threshold is not None:
            # Calculate percentage relative to threshold
            percentage = (total_vehicles / intensity_threshold) * 100
            
            if percentage < 20:
                insights.append(f"INTENSITY: Low congestion in the scene ({percentage:.1f}% of capacity)")
            elif percentage <= 50:
                insights.append(f"INTENSITY: Moderate congestion in the scene ({percentage:.1f}% of capacity)")
            elif percentage <= 70:
                insights.append(f"INTENSITY:  Heavy congestion in the scene ({percentage:.1f}% of capacity)")
            else:
                insights.append(f"INTENSITY: Severe congestion in the scene ({percentage:.1f}% of capacity)")
        # else:
        #     # Fallback to hardcoded thresholds if no alert config is set
        #     if total_vehicles > 15:
        #         insights.append(f"INTENSITY: Heavy congestion in the scene with {total_vehicles} vehicles")
        #     elif total_vehicles == 1:
        #         insights.append(f"INTENSITY: Low congestion in the scene")

        for cat, count in per_cat.items():
            display = self.CATEGORY_DISPLAY.get(cat, cat)
            insights.append(f"{display}:{count}")
        return insights

    def _check_alerts(self, summary: dict, config: VehicleMonitoringConfig) -> List[Dict]:
        """
        Check if any alert thresholds are exceeded and return alert dicts.
        """
        alerts = []
        if not config.alert_config:
            return alerts
        total = summary.get("total_count", 0)
        if config.alert_config.count_thresholds:
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "all" and total >= threshold:
                    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC')
                    alert_description = f"Vehicles count ({total}) exceeds threshold ({threshold})"
                    alerts.append({
                        "type": "count_threshold",
                    "severity": "warning",
                    "message": f"Total vehicle count ({total}) exceeds threshold ({threshold})",
                    "category": category,
                    "current_count": total,
                    "threshold": threshold
                    })
                elif category in summary.get("per_category_count", {}):
                    count = summary.get("per_category_count", {})[category]
                    if count >= threshold:
                        alerts.append({
                            "type": "count_threshold",
                            "severity": "warning",
                            "message": f"{category} count ({count}) exceeds threshold ({threshold})",
                            "category": category,
                            "current_count": count,
                            "threshold": threshold
                        })
        return alerts

    def _extract_predictions(self, detections: list) -> List[Dict[str, Any]]:
        """
        Extract prediction details for output (category, confidence, bounding box).
        """
        return [
            {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", {})
            }
            for det in detections
        ]

    def _generate_summary(self, summary: dict, alerts: List) -> str:
        """
        Generate a human_text string for the result, including per-category insights if available.
        Adds a tab before each vehicle label for better formatting.
        Also always includes the cumulative vehicle count so far.
        """
        total = summary.get("total_count", 0)
        per_cat = summary.get("per_category_count", {})
        cumulative = summary.get("total_vehicle_counts", {}) 
        cumulative_total = sum(cumulative.values()) if cumulative else 0
        lines = []
        if total > 0:
            lines.append(f"{total} Vehicle(s) detected")
            if per_cat:
                lines.append("Vehicles:")
                for cat, count in per_cat.items():
                    lines.append(f"\t{cat}:{count}")
        else:
            lines.append("No vehicle detected")
        lines.append(f"Total vehicles detected: {cumulative_total}")
        if alerts:
            lines.append(f"{len(alerts)} alert(s)")
        return "\n".join(lines)


