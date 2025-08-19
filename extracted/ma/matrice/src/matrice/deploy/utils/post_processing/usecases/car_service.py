import time
from datetime import datetime, timezone
"""
Advanced car service use case implementation.

This module provides comprehensive car service analytics with advanced tracking,
journey analysis, queue management, and detailed business intelligence metrics.
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import field
import time
import math
from collections import defaultdict

from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol
from ..core.config import CarServiceConfig, TrackingConfig, AlertConfig
from ..utils import (
    filter_by_confidence,
    apply_category_mapping,
    point_in_polygon,
    get_bbox_center,
    calculate_distance,
    match_results_structure,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
)

def assign_person_by_area(detections, car_areas, staff_areas):
    """
    Assigns category detections to 'staff' or 'car' based on their location in area polygons.
    Modifies the detection list in-place.
    Args:
        detections: List of detection dicts.
        car_areas: Dict of area_name -> polygon (list of [x, y]).
        staff_areas: Dict of area_name -> polygon (list of [x, y]).
    """
    # Only process detections with category for staff/car assignment
    staff_track_ids = set()
    # First pass: assign staff and remember their track_ids
    for det in detections:
        if det.get('category') != 'person' and det.get('category') != 'staff':
            # Skip non-person, non-staff objects (e.g., chair, tie, etc.)
            continue
        if det.get('category') == 'person':
            bbox = det.get('bbox', det.get('bounding_box', None))
            if bbox and len(bbox) == 4:
                center = get_bbox_center(bbox)
                for polygon in staff_areas.values():
                    if point_in_polygon(center, polygon):
                        det['category'] = 'staff'
                        if 'track_id' in det:
                            staff_track_ids.add(det['track_id'])
                        break
        elif det.get('category') == 'staff' and 'track_id' in det:
            staff_track_ids.add(det['track_id'])
    # Second pass: assign car only if not a known staff track_id
    for det in detections:
        if det.get('category') != 'person' and det.get('category') != 'car':
            continue
        if det.get('track_id') not in staff_track_ids:
            det['category'] = 'car'
        elif det.get('track_id') in staff_track_ids:
            det['category'] = 'staff'

class CarServiceUseCase(BaseProcessor):
    def _format_timestamp_for_video(self, timestamp: float) -> str:
        """Format timestamp for video chunks (HH:MM:SS.ms format)."""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:04.1f}"

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False, frame_id: Optional[str]=None) -> str:
        """Get formatted current timestamp based on stream type."""
        if not stream_info:
            return "00:00:00.00"
        input_settings = stream_info.get("input_settings", {})
        if precision:
            if input_settings.get("start_frame", "na") != "na":
                if frame_id is not None:
                    start_time = int(frame_id)/input_settings.get("original_fps", 30)
                else:
                    start_time = input_settings.get("start_frame", 30)/input_settings.get("original_fps", 30)
                return self._format_timestamp_for_video(start_time)
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if input_settings.get("start_frame", "na") != "na":
            if frame_id is not None:
                start_time = int(frame_id)/input_settings.get("original_fps", 30)
            else:
                start_time = input_settings.get("start_frame", 30)/input_settings.get("original_fps", 30)
            return self._format_timestamp_for_video(start_time)
        else:
            # For streams, use stream_time from stream_info
            stream_time_str = input_settings.get("stream_info", {}).get("stream_time", "")
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
        input_settings = stream_info.get("input_settings", {})
        if precision:
            if input_settings.get("start_frame", "na") != "na":
                return "00:00:00"
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if input_settings.get("start_frame", "na") != "na":
            return "00:00:00"
        else:
            if not hasattr(self, '_tracking_start_time') or self._tracking_start_time is None:
                stream_time_str = input_settings.get("stream_info", {}).get("stream_time", "")
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
    def get_camera_info_from_stream(self, stream_info):
        """Extract camera_info from stream_info, matching people_counting pattern."""
        if not stream_info:
            return {}
        # Try to get camera_info directly
        camera_info = stream_info.get("camera_info")
        if camera_info:
            return camera_info
        # Fallback: try to extract from nested input_settings
        input_settings = stream_info.get("input_settings", {})
        for key in ["camera_info", "camera_id", "location", "site_id"]:
            if key in input_settings:
                return {key: input_settings[key]}
        return {}
    def _generate_per_frame_agg_summary(self, processed_data, analytics_results, config, context, stream_info=None):
        """
        Generate agg_summary dict with per-frame incidents, tracking_stats, business_analytics, alerts, human_text.
        processed_data: dict of frame_id -> detections (list)
        analytics_results: output of _compile_analytics_results
        """
        agg_summary = {}
        total_frames_processed = getattr(self, '_total_frames_processed', 0)
        global_frame_offset = getattr(self, 'global_frame_offset', 0)

        # Try to get FPS from stream_info or config
        fps = None
        if stream_info:
            fps = stream_info.get('fps') or stream_info.get('frame_rate')
        if not fps:
            fps = getattr(config, 'fps', None) or getattr(config, 'frame_rate', None)
        try:
            fps = float(fps)
            if fps <= 0:
                fps = None
        except Exception:
            fps = None

        # If frame_ids are not sorted, sort them numerically if possible
        try:
            frame_ids = sorted(processed_data.keys(), key=lambda x: int(x))
        except Exception:
            frame_ids = list(processed_data.keys())


        # For real-time fallback, record wall-clock start time
        wallclock_start_time = None
        if not fps:
            wallclock_start_time = time.time()

        for idx, frame_id in enumerate(frame_ids):
            detections = processed_data[frame_id]
            staff_count = sum(1 for d in detections if d.get('category') == 'staff')
            car_count = sum(1 for d in detections if d.get('category') == 'car')
            total_people = staff_count + car_count

            queue_analytics = analytics_results.get("car_queue_analytics", {})
            staff_analytics = analytics_results.get("staff_management_analytics", {})
            service_analytics = analytics_results.get("service_area_analytics", {})
            journey_analytics = analytics_results.get("car_journey_analytics", {})
            business_metrics = analytics_results.get("business_metrics", {})

            # --- Per-frame timestamp logic (robust, never default to 00:00:00.00 except first frame) ---
            current_timestamp = self._get_current_timestamp_str(stream_info)
            start_timestamp = self._get_start_timestamp_str(stream_info)

            # --- Alert settings and alerts for each metric ---
            alert_settings = []
            alerts = []
            # queue length alert
            queue_threshold = getattr(config, "queue_length_threshold", 10)
            if queue_analytics.get("cars_queuing", 0) > queue_threshold:
                alert_settings.append({
                    "alert_type": "email",
                    "incident_category": "car_queue",
                    "threshold_level": queue_threshold,
                    "ascending": True,
                    "settings": {
                        "email_address": getattr(config, "email_address", "john.doe@gmail.com")
                    }
                })
                alerts.append({
                    "alert_type": "email",
                    "alert_id": "email_1",
                    "incident_category": "car_queue",
                    "threshold_value": queue_analytics.get("cars_queuing", 0),
                    "ascending": True,
                    "settings": {
                        "email_address": getattr(config, "email_address", "john.doe@gmail.com")
                    }
                })
            # service efficiency alert
            efficiency_threshold = getattr(config, "service_efficiency_threshold", 0.1)
            if business_metrics.get("service_efficiency", 0) < efficiency_threshold:
                alert_settings.append({
                    "alert_type": "email",
                    "incident_category": "service_efficiency",
                    "threshold_level": efficiency_threshold,
                    "ascending": False,
                    "settings": {
                        "email_address": getattr(config, "email_address", "john.doe@gmail.com")
                    }
                })
                alerts.append({
                    "alert_type": "email",
                    "alert_id": "email_2",
                    "incident_category": "service_efficiency",
                    "threshold_value": business_metrics.get("service_efficiency", 0),
                    "ascending": False,
                    "settings": {
                        "email_address": getattr(config, "email_address", "john.doe@gmail.com")
                    }
                })

            human_text_lines = []
            human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")
            human_text_lines.append(f"\t- Active Cars: {queue_analytics.get('active_cars', 0)}")
            human_text_lines.append(f"\t\t- Queuing: {queue_analytics.get('cars_queuing', 0)}")
            human_text_lines.append(f"\t\t- Being Served: {queue_analytics.get('cars_being_served', 0)}")
            human_text_lines.append(f"\t- Active Staff: {staff_analytics.get('active_staff', 0)}")
            human_text_lines.append(f"\t- Car/Staff Ratio: {business_metrics.get('car_to_staff_ratio', 0):.2f}")
            human_text_lines.append(f"\t- Queue Performance: {business_metrics.get('queue_performance', 0)*100:.1f}%")
            human_text_lines.append(f"\t- Service Areas: {len(service_analytics.get('service_areas_status', {}))}")
            for area_name, area_info in service_analytics.get('service_areas_status', {}).items():
                cars = area_info.get("cars", 0)
                staff = area_info.get("staff", 0)
                status = area_info.get("status", "inactive")
                human_text_lines.append(f"\t\t- {area_name}: {status} with {cars} cars and {staff} staff")
            human_text_lines.append("")
            human_text_lines.append(f"TOTAL SINCE @ {start_timestamp}:")
            human_text_lines.append(f"\t- Total Cars: {journey_analytics.get('total_journeys', 0)}")
            completed_count = journey_analytics.get("journey_states", {}).get("completed", 0)
            human_text_lines.append(f"\t\t- Completed: {completed_count}")
            human_text_lines.append(f"\t- Total Staff: {staff_analytics.get('total_staff', 0)}")
            human_text_lines.append(f"\t- Average Staff Count: {staff_analytics.get('avg_staff_count', 0.0):.2f}")
            human_text_lines.append(f"\t- Average Wait Time: {queue_analytics.get('average_wait_time', 0):.1f}s")
            avg_service_time = 0.0
            if analytics_results.get("service_times"):
                times = [t.get("service_time", 0.0) for t in analytics_results["service_times"]]
                if times:
                    avg_service_time = sum(times) / len(times)
            human_text_lines.append(f"\t- Average Service Time: {avg_service_time:.1f}s")
            human_text_lines.append(f"\t- Business Metrics:")
            human_text_lines.append(f"\t\t- Service Efficiency: {business_metrics.get('service_efficiency', 0)*100:.1f}%")
            human_text_lines.append(f"\t\t- Staff Productivity: {business_metrics.get('staff_productivity', 0):.2f} services/staff")
            human_text = "\n".join(human_text_lines)

            # Build event in incident format
            event = {
                "incident_id": f"CarService_{frame_id}",
                "incident_type": "CarService",
                "severity_level": business_metrics.get("severity_level", "info"),
                "human_text": human_text,
                "start_time": start_timestamp,
                "end_time": "Incident still active",  # or use logic as needed
                "camera_info": stream_info.get("camera_info", {}) if stream_info else {},
                "level_settings": {
                    "low": 1,
                    "medium": 3,
                    "significant": 4,
                    "critical": 7
                },
                "alerts": alerts,
                "alert_settings": alert_settings
            }
            # Harmonize tracking_stats fields with people_counting output
            camera_info = self.get_camera_info_from_stream(stream_info)
            input_timestamp = current_timestamp
            reset_timestamp = start_timestamp
            reset_settings = config.create_default_config() if hasattr(config, "create_default_config") else {}

            # Calculate total_counts (global sum of staff and car)
            total_counts = [
                {"category": "staff", "count": staff_analytics.get("total_staff", 0)},
                {"category": "car", "count": journey_analytics.get("total_journeys", 0)}
            ]
            # Optionally add more categories if needed
            # Calculate current_counts (frame-wise counts)
            current_counts = [
                {"category": "staff", "count": staff_analytics.get("active_staff", 0)},
                {"category": "car", "count": queue_analytics.get("active_cars", 0)}
            ]
            # Detections: include all detections for this frame
            detection_objs = []
            for d in detections:
                bbox = d.get("bounding_box", d.get("bbox", {}))
                detection_objs.append({
                    "category": d.get("category", "person"),
                    "bounding_box": bbox
                })

            # Harmonize reset_settings format 
            reset_settings = [
                {
                    "interval_type": getattr(config, "reset_interval_type", "daily"),
                    "reset_time": {
                        "value": getattr(config, "reset_time_value", 9),
                        "time_unit": getattr(config, "reset_time_unit", "hour")
                    }
                }
            ]

            tracking_stat = {
                "input_timestamp": input_timestamp,
                "reset_timestamp": reset_timestamp,
                "camera_info": camera_info,
                "total_counts": total_counts,
                "current_counts": current_counts,
                "detections": detection_objs,
                "alerts": alerts,
                "alert_settings": alert_settings,
                "reset_settings": reset_settings,
                "human_text": human_text
            }
            # Patch: Build real_time_occupancy with correct service_areas info (not just empty lists)
            real_time_occupancy = analytics_results.get("real_time_occupancy", {}).copy()
            # Overwrite service_areas with per-zone info matching service_areas_status
            service_areas_status = service_analytics.get("service_areas_status", {})
            real_time_occupancy["service_areas"] = {}
            for area_name, area_info in service_areas_status.items():
                real_time_occupancy["service_areas"][area_name] = {
                    "cars": area_info.get("cars", 0),
                    "car_ids": area_info.get("car_ids", []),
                    "staff": area_info.get("staff", 0),
                    "staff_ids": area_info.get("staff_ids", []),
                    "service_ratio": area_info.get("service_ratio", 0.0),
                    "status": area_info.get("status", "inactive"),
                    "service_proximity_threshold": area_info.get("service_proximity_threshold", 230)
                }
            business_analytics = {
                "business_metrics": business_metrics,
                "car_queue_analytics": queue_analytics,
                "staff_management_analytics": staff_analytics,
                "service_area_analytics": service_analytics,
                "car_journey_analytics": journey_analytics,
                "service_times": analytics_results.get("service_times", []),
                "real_time_occupancy": real_time_occupancy,
                "alerts": alerts,
                "alert_settings": alert_settings
            }

            agg_summary[str(frame_id)] = {
                "incidents": event,
                "tracking_stats": tracking_stat,
                "business_analytics": business_analytics,
                "alerts": alerts,
                "human_text": human_text
            }
        return agg_summary
    # --- Chunk tracking for per-chunk analytics ---
    def _init_chunk_tracking(self):
        self._chunk_frame_count = 0
        self._chunk_car_ids = set()
        self._chunk_area_car_ids = defaultdict(set)

    def _update_chunk_tracking(self, car_detections):
        for car in car_detections:
            track_id = car.get('track_id')
            if track_id is not None:
                self._chunk_car_ids.add(track_id)
                # Find all areas this car is in (from current_areas or by geometry)
                if 'current_areas' in car:
                    for area in car['current_areas']:
                        self._chunk_area_car_ids[area].add(track_id)
                else:
                    # fallback: try to infer from bbox and self.car_areas
                    car_center = get_bbox_center(car.get('bbox', car.get('bounding_box', {})))
                    for area_name, polygon in getattr(self, 'car_areas', {}).items():
                        if point_in_polygon(car_center, polygon):
                            self._chunk_area_car_ids[area_name].add(track_id)

    def _maybe_reset_chunk(self):
        if not hasattr(self, '_chunk_frame_count'):
            self._init_chunk_tracking()
        self._chunk_frame_count += 1
        if self._chunk_frame_count > 1:
            self._init_chunk_tracking()
    def __init__(self):
        """Initialize car service use case."""
        super().__init__("car_service")
        self.category = "automobile"

        # Advanced tracking structures
        self.car_occupancy = {}
        self.staff_occupancy = {}
        self.service_occupancy = {}
        self.car_queue_times = {}
        self.car_service_times = {}
        self.car_journey = {}
        self.staff_availability = {}
        self.staff_service_count = defaultdict(int)
        self.staff_active_services = {}

        # Persistent unique staff tracking
        self.global_staff_ids = set()
        self.global_staff_ids_by_area = defaultdict(set)

        # Persistent unique car tracking
        self.global_car_ids = set()

        # Persistent staff ID memory (for cross-frame staff identity)
        self.persistent_staff_ids = set()

        # Analytics
        self.queue_wait_times = defaultdict(list)
        self.service_times = defaultdict(list)
        self.staff_efficiency = defaultdict(list)
        self.peak_occupancy = defaultdict(int)

        # Journey states
        self.JOURNEY_STATES = {
            'ENTERING': 'entering',
            'QUEUING': 'queuing',
            'BEING_SERVED': 'being_served',
            'COMPLETED': 'completed',
            'LEFT': 'left'
        }
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Get configuration schema for car service."""
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {
                    "type": "number",
                    "minimum": 0.0, 
                    "maximum": 1.0,
                    "default": 0.5,
                    "description": "Minimum confidence threshold for detections"
                },
                "car_areas": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 2,
                            "maxItems": 2
                        },
                        "minItems": 3
                    },
                    "description": "Car area definitions as polygons"
                },
                "staff_areas": {
                    "type": "object", 
                    "additionalProperties": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 2,
                            "maxItems": 2
                        },
                        "minItems": 3
                    },
                    "description": "Staff area definitions as polygons"
                },
                "service_areas": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "array",
                        "items": {
                            "type": "array", 
                            "items": {"type": "number"},
                            "minItems": 2,
                            "maxItems": 2
                        },
                        "minItems": 3
                    },
                    "description": "Service area definitions as polygons"
                },
                "staff_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["staff", "employee"],
                    "description": "Category names that represent staff"
                },
                "car_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["car", "person"],
                    "description": "Category names that represent cars"
                },
                "service_proximity_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "default": 100.0,
                    "description": "Distance threshold for service interactions"
                },
                "max_service_time": {
                    "type": "number",
                    "minimum": 0.0,
                    "default": 1800.0,
                    "description": "Maximum expected service time in seconds"
                },
                "buffer_time": {
                    "type": "number",
                    "minimum": 0.0,
                    "default": 2.0,
                    "description": "Buffer time for service calculations"
                },
                "enable_tracking": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable advanced tracking for analytics"
                },
                "enable_journey_analysis": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable car journey analysis"
                },
                "enable_queue_analytics": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable queue management analytics"
                },
                "tracking_config": {
                    "type": "object",
                    "properties": {
                        "tracking_method": {
                            "type": "string",
                            "enum": ["kalman", "sort", "deepsort", "bytetrack"],
                            "default": "kalman"
                        },
                        "max_age": {"type": "integer", "minimum": 1, "default": 30},
                        "min_hits": {"type": "integer", "minimum": 1, "default": 3},
                        "iou_threshold": {"type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.3}
                    }
                },
                "enable_smoothing": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable bounding box smoothing for detections"
                },
                "smoothing_algorithm": {
                    "type": "string",
                    "enum": ["observability", "kalman"],
                    "default": "observability"
                },
                "smoothing_window_size": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 20
                },
                "smoothing_cooldown_frames": {
                    "type": "integer",
                    "minimum": 0,
                    "default": 5
                },
                "smoothing_confidence_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.5
                },
                "smoothing_confidence_range_factor": {
                    "type": "number",
                    "minimum": 0.0,
                    "default": 0.5
                },
                "reset_interval_type": {
                    "type": "string",
                    "default": "daily",
                    "description": "Interval type for resetting analytics (e.g., daily, weekly)"
                },
                "reset_time_value": {
                    "type": "integer",
                    "default": 9,
                    "description": "Time value for reset (e.g., hour of day)"
                },
                "reset_time_unit": {
                    "type": "string",
                    "default": "hour",
                    "description": "Time unit for reset (e.g., hour, minute)"
                },
                "alert_config": {
                    "type": "object",
                    "description": "Custom alert configuration settings"
                },
                "queue_length_threshold": {
                    "type": "integer",
                    "default": 10,
                    "description": "Threshold for queue length alerts"
                },
                "service_efficiency_threshold": {
                    "type": "number",
                    "default": 0.0,
                    "description": "Threshold for service efficiency alerts"
                },
                "email_address": {
                    "type": "string",
                    "default": "john.doe@gmail.com",
                    "description": "Email address for alert notifications"
                },
            },
            "required": ["confidence_threshold"],
            "additionalProperties": False
        }
    
    def create_default_config(self, **overrides) -> CarServiceConfig:
        """Create default configuration with optional overrides."""
        defaults = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.5,
            "enable_tracking": True,
            "enable_analytics": True,
            "enable_journey_analysis": True,
            "enable_queue_analytics": True,
            "staff_categories": ["staff", "employee"],
            "car_categories": ["car"],
            "service_proximity_threshold": 100.0,
            "max_service_time": 1800.0,
            "buffer_time": 2.0,
            "stream_info": {},  
        }
        defaults.update(overrides)
        return CarServiceConfig(**defaults)
    
    def process(self, data: Any, config: ConfigProtocol,
                context: Optional[ProcessingContext] = None, stream_info: Optional[dict] = None) -> ProcessingResult:
        """
        Process advanced car service analytics.
        """
        start_time = time.time()

        try:
            if not isinstance(config, CarServiceConfig):
                return self.create_error_result(
                    "Invalid configuration type for advanced car service",
                    usecase=self.name,
                    category=self.category,
                    context=context
                )

            if stream_info is not None:
                if context is None:
                    context = ProcessingContext()
                context.stream_info = stream_info

            if context is None:
                context = ProcessingContext()

            self._service_proximity_threshold = config.service_proximity_threshold

            input_format = match_results_structure(data)
            context.input_format = input_format
            context.confidence_threshold = config.confidence_threshold
            context.enable_tracking = config.enable_tracking

            self.logger.info(f"Processing advanced car service with format: {input_format.value}")

            self._initialize_areas(config.car_areas, config.staff_areas, config.service_areas)

            processed_data = data
            if config.confidence_threshold is not None:
                processed_data = filter_by_confidence(processed_data, config.confidence_threshold)
                self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")

            if hasattr(config, 'index_to_category') and config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
                self.logger.debug("Applied category mapping")

            # --- Smoothing logic ---
            if getattr(config, "enable_smoothing", False):
                if not hasattr(self, "smoothing_tracker") or self.smoothing_tracker is None:
                    smoothing_config = BBoxSmoothingConfig(
                        smoothing_algorithm=getattr(config, "smoothing_algorithm", "observability"),
                        window_size=getattr(config, "smoothing_window_size", 20),
                        cooldown_frames=getattr(config, "smoothing_cooldown_frames", 5),
                        confidence_threshold=getattr(config, "confidence_threshold", 0.5),
                        confidence_range_factor=getattr(config, "smoothing_confidence_range_factor", 0.5),
                        enable_smoothing=True
                    )
                    self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
                processed_data = bbox_smoothing(processed_data, self.smoothing_tracker.config, self.smoothing_tracker)

            detections = self._extract_detections(processed_data)
            assign_person_by_area(
                detections,
                getattr(config, 'car_areas', {}),
                getattr(config, 'staff_areas', {})
            )
            staff_detections, car_detections = self._categorize_detections(
                detections, config.staff_categories, config.car_categories
            )
            self.logger.debug(f"Extracted {len(staff_detections)} staff and {len(car_detections)} car detections")

            self._maybe_reset_chunk()
            self._update_chunk_tracking(car_detections)

            current_time = time.time()
            analytics_results = self._process_comprehensive_analytics(
                staff_detections, car_detections, config, current_time
            )

            # --- FIX: Ensure agg_summary is top-level and events/tracking_stats are dicts ---
            if isinstance(processed_data, dict):
                agg_summary = self._generate_per_frame_agg_summary(processed_data, analytics_results, config, context, stream_info)
            else:
                agg_summary = {"events": {}, "tracking_stats": {}}

            insights = self._generate_insights(analytics_results, config)
            alerts = self._check_alerts(analytics_results, config)
            summary = self._generate_summary(analytics_results, alerts)
            predictions = self._extract_predictions(processed_data)

            context.mark_completed()

            # Compose result data with harmonized agg_summary structure
            result = self.create_result(
                data={"agg_summary": agg_summary},
                usecase=self.name,
                category=self.category,
                context=context
            )

            result.summary = summary
            result.insights = insights
            result.predictions = predictions
            result.metrics = analytics_results.get("business_metrics", {})

            if not config.car_areas and not config.staff_areas:
                result.add_warning("No car or staff areas defined - using global analysis only")

            if config.service_proximity_threshold > 250:
                result.add_warning(f"High service proximity threshold ({config.service_proximity_threshold}) may miss interactions")

            self.logger.info(f"Advanced car service analysis completed successfully in {result.processing_time:.2f}s")
            return result

        except Exception as e:
            self.logger.error(f"Advanced car service analysis failed: {str(e)}", exc_info=True)

            if context:
                context.mark_completed()

            return self.create_error_result(
                str(e),
                type(e).__name__,
                usecase=self.name,
                category=self.category,
                context=context
            )
    
    def _initialize_areas(self, car_areas: Dict, staff_areas: Dict, service_areas: Dict):
        """Initialize area tracking structures."""
        self.car_areas = car_areas or {}
        self.staff_areas = staff_areas or {}
        self.service_areas = service_areas or {}
        
        # Initialize occupancy tracking
        self.car_occupancy = {name: [] for name in self.car_areas}
        self.staff_occupancy = {name: [] for name in self.staff_areas}
        self.service_occupancy = {name: [] for name in self.service_areas}
        self.staff_availability = {area: [] for area in self.staff_areas}
    
    def _extract_detections(self, data: Any) -> List[Dict[str, Any]]:
        """Extract detections from processed data."""
        detections = []
        
        try:
            if isinstance(data, list):
                # Direct detection list
                detections = [d for d in data if isinstance(d, dict)]
            elif isinstance(data, dict):
                # Frame-based or structured data
                for key, value in data.items():
                    if isinstance(value, list):
                        detections.extend([d for d in value if isinstance(d, dict)])
                    elif isinstance(value, dict) and any(k in value for k in ['bbox', 'bounding_box', 'category']):
                        detections.append(value)
        except Exception as e:
            self.logger.warning(f"Failed to extract detections: {str(e)}")
        
        return detections
    
    def _categorize_detections(self, detections: List[Dict], staff_categories: List[str],
                              car_categories: List[str]) -> Tuple[List[Dict], List[Dict]]:
        """Categorize detections into staff and cars, with persistent staff ID logic. Only include detections whose category is in staff_categories or car_categories."""
        staff_detections = []
        car_detections = []

        for detection in detections:
            track_id = detection.get('track_id')
            category = detection.get('category', detection.get('class', ''))

            # If this track_id was ever staff, always treat as staff
            if track_id is not None and track_id in self.persistent_staff_ids:
                staff_detections.append(detection)
                continue

            # If currently detected as staff, add to persistent set
            if category in staff_categories:
                staff_detections.append(detection)
                if track_id is not None:
                    self.persistent_staff_ids.add(track_id)
            elif category in car_categories:
                car_detections.append(detection)
            # else: skip detection (do not add to either list)

        return staff_detections, car_detections
    
    def _process_comprehensive_analytics(self, staff_detections: List[Dict], car_detections: List[Dict],
                                       config: CarServiceConfig, current_time: float) -> Dict[str, Any]:
        """Process comprehensive car service analytics."""
        # Reset current state
        self._reset_current_state()
        
        # Process staff and car detections
        self._process_staff_detections(staff_detections, current_time)
        self._process_car_detections(car_detections, current_time)
        
        # Update service interactions
        self._update_service_interactions(current_time)
        
        # Compile comprehensive results
        return self._compile_analytics_results(current_time)
    
    def _reset_current_state(self):
        """Reset current state for new processing cycle."""
        # Clear current occupancy (will be repopulated)
        for area_name in self.car_occupancy:
            self.car_occupancy[area_name] = []
        for area_name in self.staff_occupancy:
            self.staff_occupancy[area_name] = []
        for area_name in self.service_occupancy:
            self.service_occupancy[area_name] = []
    
    def _process_staff_detections(self, staff_detections: List[Dict], current_time: float):
        """Process staff detections and update tracking."""
        for staff in staff_detections:
            staff_center = get_bbox_center(staff.get('bbox', staff.get('bounding_box', {})))
            if not staff_center:
                continue
            track_id = staff.get('track_id', f"staff_{hash(str(staff_center))}")
            # Update persistent global staff ids
            self.global_staff_ids.add(track_id)
            # Update staff area occupancy and persistent area staff ids
            for area_name, polygon in self.staff_areas.items():
                if point_in_polygon(staff_center, polygon):
                    self.staff_occupancy[area_name].append({
                        'track_id': track_id,
                        'center': staff_center,
                        'timestamp': current_time
                    })
                    self.global_staff_ids_by_area[area_name].add(track_id)
    
    def _process_car_detections(self, car_detections: List[Dict], current_time: float):
        """Process car detections and update journey tracking."""
        for car in car_detections:
            car_center = get_bbox_center(car.get('bbox', car.get('bounding_box', {})))
            if not car_center:
                continue
            track_id = car.get('track_id', f"car_{hash(str(car_center))}")
            # Update persistent global car ids
            self.global_car_ids.add(track_id)
            # Initialize car journey if new
            is_new_journey = False
            if track_id not in self.car_journey:
                self._initialize_car_journey(track_id, current_time)
                is_new_journey = True
            journey = self.car_journey[track_id]
            # Update car area occupancy
            current_areas = []
            for area_name, polygon in self.car_areas.items():
                if point_in_polygon(car_center, polygon):
                    current_areas.append(area_name)
                    self.car_occupancy[area_name].append({
                        'track_id': track_id,
                        'center': car_center,
                        'timestamp': current_time
                    })
            # Update journey state based on current areas
            journey['current_areas'] = current_areas
            journey['last_seen'] = current_time
            journey['positions'].append({
                'center': car_center,
                'timestamp': current_time,
                'areas': current_areas.copy()
            })
            # --- Staff service count: handle BEING_SERVED at initialization ---
            if is_new_journey and self._is_car_being_served(track_id, current_time):
                # car starts in BEING_SERVED state, increment staff_service_count for the nearest staff
                nearest_staff = self._find_nearest_staff(car_center)
                if nearest_staff:
                    staff_id, _ = nearest_staff
                    self.staff_service_count[staff_id] += 1
            # Update journey state logic
            self._update_car_journey_state(track_id, current_areas, current_time)
    
    def _initialize_car_journey(self, track_id: int, current_time: float):
        """Initialize car journey tracking."""
        self.car_journey[track_id] = {
            'state': self.JOURNEY_STATES['ENTERING'],
            'start_time': current_time,
            'last_seen': current_time,
            'current_areas': [],
            'areas_visited': set(),
            'positions': [],
            'queue_start_time': None,
            'service_start_time': None,
            'service_end_time': None,
            'total_wait_time': 0.0,
            'total_service_time': 0.0,
            'staff_interactions': []
        }
    
    def _update_car_journey_state(self, track_id: int, current_areas: List[str], current_time: float):
        """Update car journey state based on current location."""
        journey = self.car_journey[track_id]
        # Update areas visited
        journey['areas_visited'].update(current_areas)
        # State transition logic
        if journey['state'] == self.JOURNEY_STATES['ENTERING']:
            if current_areas:
                journey['state'] = self.JOURNEY_STATES['QUEUING']
                journey['queue_start_time'] = current_time
        elif journey['state'] == self.JOURNEY_STATES['QUEUING']:
            # Check if car is being served (near staff)
            if self._is_car_being_served(track_id, current_time):
                journey['state'] = self.JOURNEY_STATES['BEING_SERVED']
                journey['service_start_time'] = current_time
                if journey['queue_start_time']:
                    journey['total_wait_time'] = current_time - journey['queue_start_time']
                # --- Staff service count: increment only on QUEUING -> BEING_SERVED transition ---
                car_center = journey['positions'][-1]['center'] if journey['positions'] else None
                if car_center:
                    nearest_staff = self._find_nearest_staff(car_center)
                    if nearest_staff:
                        staff_id, _ = nearest_staff
                        self.staff_service_count[staff_id] += 1
        elif journey['state'] == self.JOURNEY_STATES['BEING_SERVED']:
            # Check if service is completed
            if not self._is_car_being_served(track_id, current_time):
                journey['state'] = self.JOURNEY_STATES['COMPLETED']
                journey['service_end_time'] = current_time
                if journey['service_start_time']:
                    journey['total_service_time'] = current_time - journey['service_start_time']
                    # --- Service time tracking: record in self.service_times ---
                    # Try to associate with staff_id if possible
                    car_center = journey['positions'][-1]['center'] if journey['positions'] else None
                    staff_id = None
                    if car_center:
                        nearest_staff = self._find_nearest_staff(car_center)
                        if nearest_staff:
                            staff_id, _ = nearest_staff
                    # Store as per-car service time (flat list)
                    self.service_times[track_id].append({
                        'car_id': track_id,
                        'service_time': journey['total_service_time'],
                        'service_start_time': journey['service_start_time'],
                        'service_end_time': journey['service_end_time'],
                        'staff_id': staff_id
                    })
    
    def _is_car_being_served(self, car_track_id: int, current_time: float) -> bool:
        """Check if car is currently being served by staff or in overlapping service/car area or proximity."""
        car_journey = self.car_journey.get(car_track_id)
        if not car_journey or not car_journey['positions']:
            return False

        car_center = car_journey['positions'][-1]['center']

        # Get all car areas the car is in
        car_areas_in = set()
        for area_name, polygon in self.car_areas.items():
            if point_in_polygon(car_center, polygon):
                car_areas_in.add(area_name)

        # Get all service areas the car is in
        service_areas_in = set()
        for area_name, polygon in self.service_areas.items():
            if point_in_polygon(car_center, polygon):
                service_areas_in.add(area_name)

        # If any area is both a car area and a service area, consider being served
        if car_areas_in & service_areas_in:
            return True

        # If car is inside any service area (legacy logic)
        if service_areas_in:
            return True

        # If not inside service area, check proximity to staff
        nearest_staff = self._find_nearest_staff(car_center)
        if nearest_staff:
            staff_id, distance = nearest_staff
            if distance <= self._service_proximity_threshold:
                return True

        return False
    
    def _find_nearest_staff(self, car_center: Tuple[float, float]) -> Optional[Tuple[int, float]]:
        """Find nearest staff member to car."""
        nearest_staff = None
        min_distance = float('inf')
        
        for area_name, staff_list in self.staff_occupancy.items():
            for staff_info in staff_list:
                staff_center = staff_info['center']
                distance = calculate_distance(car_center, staff_center)
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_staff = (staff_info['track_id'], distance)
        
        return nearest_staff
    
    def _update_service_interactions(self, current_time: float):
        """Update service interactions between staff and cars."""
        for car_id, journey in self.car_journey.items():
            if journey['state'] == self.JOURNEY_STATES['BEING_SERVED']:
                if journey['positions']:
                    car_center = journey['positions'][-1]['center']
                    nearest_staff = self._find_nearest_staff(car_center)
                    if nearest_staff:
                        staff_id, distance = nearest_staff
                        # Record interaction (do not increment staff_service_count here)
                        interaction = {
                            'car_id': car_id,
                            'staff_id': staff_id,
                            'distance': distance,
                            'timestamp': current_time
                        }
                        journey['staff_interactions'].append(interaction)
        # Note: staff_service_count is now incremented only on state transition or at initialization
    
    def _compile_analytics_results(self, current_time: float) -> Dict[str, Any]:
        """Compile comprehensive analytics results."""
        # --- Previous approach (commented out): ---
        # real_time_occupancy = {
        #     "car_areas": self.car_occupancy,
        #     "staff_areas": self.staff_occupancy,
        #     "service_areas": self.service_occupancy
        # }

        # --- New approach: Only keep the last detection per track_id per area ---
        def get_latest_per_track(area_dict):
            latest = {}
            for area_name, occupants in area_dict.items():
                track_map = {}
                for occ in occupants:
                    tid = occ.get('track_id')
                    ts = occ.get('timestamp', 0)
                    if tid is not None:
                        if tid not in track_map or ts > track_map[tid]['timestamp']:
                            track_map[tid] = occ
                latest[area_name] = list(track_map.values())
            return latest

        real_time_occupancy = {
            "car_areas": get_latest_per_track(self.car_occupancy),
            "staff_areas": get_latest_per_track(self.staff_occupancy),
            "service_areas": get_latest_per_track(self.service_occupancy)
        }


        # --- Service times output: flatten to a list for JSON output (per-car) ---
        service_times_output = []
        for car_id, records in self.service_times.items():
            for rec in records:
                entry = rec.copy()
                service_times_output.append(entry)

        return {
            "car_queue_analytics": self._get_car_queue_results(),
            "staff_management_analytics": self._get_staff_management_results(),
            "service_area_analytics": self._get_service_area_results(),
            "car_journey_analytics": self._get_car_journey_results(),
            "business_metrics": self._calculate_analytics(current_time),
            "real_time_occupancy": real_time_occupancy,
            "service_times": service_times_output,
            "processing_timestamp": current_time
        }
    
    def _get_car_queue_results(self) -> Dict[str, Any]:
        """Get car queue analytics (per chunk of 1 frames)."""
        # Use chunk-based car ids for per-chunk analytics
        active_cars = len(getattr(self, '_chunk_car_ids', set()))
        queue_lengths_by_area = {}
        for area_name in self.car_occupancy:
            queue_lengths_by_area[area_name] = len(getattr(self, '_chunk_area_car_ids', defaultdict(set))[area_name])

        # For state counts, only count journeys whose track_id is in the current chunk
        cars_queuing = 0
        cars_being_served = 0
        cars_completed = 0
        # Collect wait times for all cars who have ever queued in this chunk
        wait_times = []
        chunk_ids = getattr(self, '_chunk_car_ids', set())
        now = time.time()
        for track_id in chunk_ids:
            journey = self.car_journey.get(track_id)
            if not journey:
                continue
            # Only include if car has ever queued (should always be true for chunk ids)
            # Use their total_wait_time if they have left QUEUING state, else ongoing
            if journey['state'] == self.JOURNEY_STATES['QUEUING']:
                cars_queuing += 1
                if journey['queue_start_time']:
                    wait_times.append(now - journey['queue_start_time'])
            elif journey['state'] == self.JOURNEY_STATES['BEING_SERVED']:
                cars_being_served += 1
                if journey['total_wait_time']:
                    wait_times.append(journey['total_wait_time'])
            elif journey['state'] in [self.JOURNEY_STATES['COMPLETED'], self.JOURNEY_STATES['LEFT']]:
                cars_completed += 1
                if journey['total_wait_time']:
                    wait_times.append(journey['total_wait_time'])

        n_total = len(wait_times)
        average_wait_time = sum(wait_times) / n_total if n_total > 0 else 1.0

        queue_analytics = {
            "active_cars": active_cars,
            "cars_queuing": cars_queuing,
            "cars_being_served": cars_being_served,
            "cars_completed": cars_completed,
            "average_wait_time": average_wait_time,
            "queue_lengths_by_area": queue_lengths_by_area
        }
        return queue_analytics
    
    def _get_staff_management_results(self) -> Dict[str, Any]:
        """Get staff management analytics."""
        staff_analytics = {
            "total_staff": len(self.global_staff_ids),
            "staff_distribution": {area_name: len(self.global_staff_ids_by_area[area_name]) for area_name in self.staff_areas},
            "staff_utilization": 0.0,
            "active_staff": 0,
            "avg_staff_count": 0.0
        }

        total_services = sum(self.staff_service_count.values())
        chunk_staff_ids = set()
        for area_staff in self.staff_occupancy.values():
            for staff in area_staff:
                tid = staff.get('track_id')
                if tid is not None:
                    chunk_staff_ids.add(tid)
        staff_analytics["active_staff"] = len(chunk_staff_ids)

        # Calculate overall utilization
        total_staff_count = staff_analytics["total_staff"]
        if total_staff_count > 0:
            staff_analytics["staff_utilization"] = len(chunk_staff_ids) / total_staff_count

        # --- Avg staff count calculation ---
        if not hasattr(self, '_staff_presence_history'):
            self._staff_presence_history = []  # list of (timestamp, staff_count)
        now = time.time()
        staff_count_now = len(chunk_staff_ids)
        self._staff_presence_history.append((now, staff_count_now))
        avg_staff_count = 0.0
        total_time = 0.0
        history = self._staff_presence_history
        if len(history) > 1:
            for i in range(1, len(history)):
                t0, c0 = history[i-1]
                t1, c1 = history[i]
                dt = t1 - t0
                avg_staff_count += c0 * dt
                total_time += dt
            if total_time > 0:
                staff_analytics["avg_staff_count"] = avg_staff_count / total_time
            else:
                staff_analytics["avg_staff_count"] = staff_count_now
        else:
            staff_analytics["avg_staff_count"] = staff_count_now

        staff_efficiency = {}
        for staff_id in self.global_staff_ids:
            service_count = self.staff_service_count.get(staff_id, 0)
            staff_efficiency[staff_id] = {
                "services_handled": service_count,
                "efficiency_score": service_count / max(total_services, 1) if total_services > 0 else 0.0
            }
        self._internal_staff_efficiency = staff_efficiency

        return staff_analytics
    
    def _get_service_area_results(self) -> Dict[str, Any]:
        """Get service area analytics (dynamic: polygon inclusion, overlap, and proximity)."""
        service_analytics = {
            "service_areas_status": {},
            "total_active_services": 0
        }

        service_proximity_threshold = getattr(self, '_service_proximity_threshold', 100.0)

        # Collect all cars and staff (flattened)
        all_cars = []
        for area_list in self.car_occupancy.values():
            all_cars.extend(area_list)
        all_staff = []
        for area_list in self.staff_occupancy.values():
            all_staff.extend(area_list)

        for area_name, polygon in self.service_areas.items():
            cars_in_area = set()
            staff_in_area = set()

            # cars: count only if inside service area polygon
            for occ in all_cars:
                center = occ.get('center')
                tid = occ.get('track_id')
                if center is None or tid is None:
                    continue
                if point_in_polygon(center, polygon):
                    cars_in_area.add(tid)

            # Staff: count only if inside service area polygon
            for occ in all_staff:
                center = occ.get('center')
                tid = occ.get('track_id')
                if center is None or tid is None:
                    continue
                if point_in_polygon(center, polygon):
                    staff_in_area.add(tid)

            service_analytics["service_areas_status"][area_name] = {
                "cars": len(cars_in_area),
                "car_ids": list(cars_in_area),
                "staff": len(staff_in_area),
                "staff_ids": list(staff_in_area),
                "service_ratio": len(cars_in_area) / max(len(staff_in_area), 1),
                "status": "active" if len(staff_in_area) > 0 else "inactive",
                "service_proximity_threshold": service_proximity_threshold
            }

            if len(staff_in_area) > 0:
                service_analytics["total_active_services"] += 1

        return service_analytics
    
    def _get_car_journey_results(self) -> Dict[str, Any]:
        """Get car journey analytics."""
        journey_analytics = {
            "total_journeys": len(self.car_journey),
            "journey_states": {state: 0 for state in self.JOURNEY_STATES.values()},
            "average_journey_time": 0.0,
            "popular_areas": {},
            # "journey_patterns": {}
        }
        
        journey_times = []
        all_areas_visited = []
        
        for journey in self.car_journey.values():
            # Count journey states
            journey_analytics["journey_states"][journey['state']] += 1
            
            # Calculate journey time
            if journey['start_time'] and journey['last_seen']:
                journey_time = journey['last_seen'] - journey['start_time']
                journey_times.append(journey_time)
            
            # Collect areas visited
            all_areas_visited.extend(journey['areas_visited'])
        
        # Calculate average journey time
        if journey_times:
            journey_analytics["average_journey_time"] = sum(journey_times) / len(journey_times)
        
        # Calculate popular areas
        from collections import Counter
        area_counts = Counter(all_areas_visited)
        journey_analytics["popular_areas"] = dict(area_counts.most_common())
        
        return journey_analytics
    
    def _calculate_analytics(self, current_time: float) -> Dict[str, Any]:
        """Calculate comprehensive business metrics."""
        total_cars = len(self.car_journey)
        chunk_ids = getattr(self, '_chunk_car_ids', set())
        cars_queuing = 0
        cars_being_served = 0
        for track_id in chunk_ids:
            journey = self.car_journey.get(track_id)
            if not journey:
                continue
            if journey['state'] == self.JOURNEY_STATES['QUEUING']:
                cars_queuing += 1
            elif journey['state'] == self.JOURNEY_STATES['BEING_SERVED']:
                cars_being_served += 1

        # Use global staff count (unique staff IDs)
        # Use active_staff from staff_management_analytics for real-time ratio
        staff_analytics = self._get_staff_management_results()
        active_staff = staff_analytics.get("active_staff", 0)
        total_staff = staff_analytics.get("total_staff", 0)

        metrics = {
            # Now using per-chunk car count for ratio
            "car_to_staff_ratio": (cars_queuing + cars_being_served) / max(active_staff, 1),
            "service_efficiency": 0.0,
            "queue_performance": 0.0,
            "staff_productivity": 0.0,
            "overall_performance": 0.0
        }

        # Calculate service efficiency
        completed_services = sum(1 for j in self.car_journey.values() 
                               if j['state'] == self.JOURNEY_STATES['COMPLETED'])
        metrics["service_efficiency"] = completed_services / max(total_cars, 1)

        # Calculate queue performance
        metrics["queue_performance"] = max(0, 1 - (cars_queuing / max(total_cars, 1)))

        # Calculate staff productivity
        total_services = sum(self.staff_service_count.values())
        metrics["staff_productivity"] = total_services / max(total_staff, 1)

        # Calculate overall performance
        metrics["overall_performance"] = (
            metrics["service_efficiency"] * 0.4 +
            metrics["queue_performance"] * 0.3 +
            metrics["staff_productivity"] * 0.3
        )

        return metrics
    
    def _check_alerts(self, analytics_results: Dict, config: CarServiceConfig) -> List[Dict]:
        """Check for alert conditions in advanced car service operations."""
        alerts = []
        
        if not config.alert_config:
            return alerts
        
        # Check queue length alerts
        queue_analytics = analytics_results.get("car_queue_analytics", {})
        cars_queuing = queue_analytics.get("cars_queuing", 0)
        
        if cars_queuing > 10:  # Threshold for long queues
            alerts.append({
                "type": "long_queue",
                "severity": "warning",
                "message": f"Long car queue detected ({cars_queuing} cars waiting)",
                "queue_length": cars_queuing,
                "recommendation": "Consider adding more staff or opening additional service points"
            })
        
        # Check service efficiency alerts
        business_metrics = analytics_results.get("business_metrics", {})
        service_efficiency = business_metrics.get("service_efficiency", 0)
        
        if service_efficiency < 0.5:
            alerts.append({
                "type": "low_service_efficiency",
                "severity": "critical" if service_efficiency < 0.3 else "warning",
                "message": f"Low service efficiency detected ({service_efficiency:.1%})",
                "efficiency": service_efficiency,
                "recommendation": "Review service processes and staff allocation"
            })
        
        # Check staff utilization alerts
        staff_analytics = analytics_results.get("staff_management_analytics", {})
        staff_utilization = staff_analytics.get("staff_utilization", 0)
        
        if staff_utilization < 0.6:
            alerts.append({
                "type": "low_staff_utilization",
                "severity": "warning",
                "message": f"Low staff utilization detected ({staff_utilization:.1%})",
                "utilization": staff_utilization,
                "recommendation": "Consider staff redeployment or schedule optimization"
            })
        
        return alerts
    
    def _generate_insights(self, analytics_results: Dict, config: CarServiceConfig) -> List[str]:
        """Generate actionable insights from advanced car service analysis."""
        insights = []
        
        # Queue insights
        queue_analytics = analytics_results.get("car_queue_analytics", {})
        active_cars = queue_analytics.get("active_cars", 0)
        cars_queuing = queue_analytics.get("cars_queuing", 0)
        cars_being_served = queue_analytics.get("cars_being_served", 0)
        
        if active_cars == 0:
            insights.append("No active cars detected in service areas")
            return insights
        
        insights.append(f"Active car analysis: {active_cars} total cars")
        
        if cars_queuing > 0:
            insights.append(f"📊 Queue status: {cars_queuing} cars waiting")
            
            avg_wait_time = queue_analytics.get("average_wait_time", 0)
            if avg_wait_time > 300:  # 5 minutes
                insights.append(f"⚠️ Long average wait time: {avg_wait_time/60:.1f} minutes")
            elif avg_wait_time > 0:
                insights.append(f"⏱️ Average wait time: {avg_wait_time/60:.1f} minutes")
        
        if cars_being_served > 0:
            insights.append(f"🔄 Active services: {cars_being_served} cars being served")
        
        # Staff insights
        staff_analytics = analytics_results.get("staff_management_analytics", {})
        total_staff = staff_analytics.get("total_staff", 0)
        staff_utilization = staff_analytics.get("staff_utilization", 0)
        
        if total_staff > 0:
            insights.append(f"Staff deployment: {total_staff} staff members active")
            
            if staff_utilization >= 0.8:
                insights.append("✅ High staff utilization - team is actively engaged")
            elif staff_utilization >= 0.6:
                insights.append("📊 Good staff utilization")
            else:
                insights.append("⚠️ Low staff utilization - consider redeployment")
        
        # Business performance insights
        business_metrics = analytics_results.get("business_metrics", {})
        overall_performance = business_metrics.get("overall_performance", 0)
        
        if overall_performance >= 0.8:
            insights.append("🌟 Excellent overall service performance")
        elif overall_performance >= 0.6:
            insights.append("✅ Good overall service performance")
        else:
            insights.append("📈 Service performance needs improvement")
        
        # Journey insights
        journey_analytics = analytics_results.get("car_journey_analytics", {})
        avg_journey_time = journey_analytics.get("average_journey_time", 0)
        
        if avg_journey_time > 0:
            insights.append(f"Car journey: average time {avg_journey_time/60:.1f} minutes")
            
            if avg_journey_time > 1800:  # 30 minutes
                insights.append("⚠️ Long car journey times detected")
        
        return insights


    def _get_start_timestamp_str(self, stream_info: Optional[dict]) -> str:
        """Get formatted start timestamp for 'TOTAL SINCE' based on stream type."""
        # For video, use start_video_timestamp if available, else 00:00:00
        if not stream_info:
            return "00:00:00.00"
        input_settings = stream_info.get("input_settings", {})
        stream_type = input_settings.get("stream_type", "video_file")
        if stream_type == "video_file":
            start_video_timestamp = stream_info.get("start_video_timestamp", None)
            if start_video_timestamp:
                return start_video_timestamp[:8]
            else:
                return "00:00:00.00"
        else:
            # For streams, persist the first stream_time as tracking start time
            if not hasattr(self, "_tracking_start_time") or self._tracking_start_time is None:
                stream_time_str = stream_info.get("stream_time", "")
                if stream_time_str:
                    try:
                        from datetime import datetime, timezone
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                    except Exception:
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()
            from datetime import datetime, timezone
            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            return dt.strftime('%Y:%m:%d %H:%M:%S')
    
    def _generate_summary(self, analytics_results: Dict, alerts: List) -> str:
        """Generate human-readable summary."""
        # Beautiful, tabbed, non-technical summary for all major analytics sections
        queue_analytics = analytics_results.get("car_queue_analytics", {})
        staff_analytics = analytics_results.get("staff_management_analytics", {})
        service_analytics = analytics_results.get("service_area_analytics", {})
        journey_analytics = analytics_results.get("car_journey_analytics", {})
        business_metrics = analytics_results.get("business_metrics", {})
        service_times = analytics_results.get("service_times", [])
        occupancy = analytics_results.get("real_time_occupancy", {})

        def tabbed_section(title, dct, omit_keys=None):
            if not dct:
                return f"{title}: None"
            omit_keys = omit_keys or set()
            lines = [f"{title}:"]
            for k, v in dct.items():
                if k in omit_keys:
                    continue
                if isinstance(v, dict):
                    lines.append(f"\t{k}:")
                    for sk, sv in v.items():
                        lines.append(f"\t\t{sk}: {sv}")
                elif isinstance(v, list):
                    lines.append(f"\t{k}: [{len(v)} items]")
                else:
                    lines.append(f"\t{k}: {v}")
            return "\n".join(lines)

        def tabbed_list_section(title, lst):
            if not lst:
                return f"{title}: None"
            lines = [f"{title}:"]
            for i, item in enumerate(lst):
                lines.append(f"\t{i+1}. {item}")
            return "\n".join(lines)

        summary = []
        summary.append(tabbed_section("car_queue_analytics", queue_analytics, omit_keys={"wait_times_completed", "wait_times_ongoing"}))
        summary.append(tabbed_section("staff_management_analytics", staff_analytics, omit_keys={"staff_efficiency"}))
        summary.append(tabbed_section("service_area_analytics", service_analytics))
        summary.append(tabbed_section("car_journey_analytics", journey_analytics))
        summary.append(tabbed_section("business_metrics", business_metrics))
        summary.append(tabbed_section("service_times", {"service_times": service_times}))
        summary.append(tabbed_section("real_time_occupancy", occupancy))

        if alerts:
            critical_alerts = sum(1 for alert in alerts if alert.get("severity") == "critical")
            if critical_alerts > 0:
                summary.append(f"ALERTS: {critical_alerts} critical alert(s)")
            else:
                summary.append(f"ALERTS: {len(alerts)} alert(s)")

        return "\n".join(summary)
    
    def _extract_predictions(self, data: Any) -> Dict[str, List[Dict[str, Any]]]:
        """Extract predictions from processed data for API compatibility, grouped by frame number if available."""
        predictions = {}
        try:
            if isinstance(data, dict):
                # Frame-based or tracking format
                for frame_id, items in data.items():
                    if not isinstance(items, list):
                        continue
                    frame_preds = []
                    for item in items:
                        if isinstance(item, dict):
                            pred = {
                                "category": item.get("category", item.get("class", "unknown")),
                                "confidence": item.get("confidence", item.get("score", 0.0)),
                                "bounding_box": item.get("bounding_box", item.get("bbox", {})),
                                "track_id": item.get("track_id")
                            }
                            frame_preds.append(pred)
                    if frame_preds:
                        predictions[str(frame_id)] = frame_preds
            elif isinstance(data, list):
                # If not frame-based, put all predictions under a generic key
                predictions["0"] = []
                for item in data:
                    if isinstance(item, dict):
                        pred = {
                            "category": item.get("category", item.get("class", "unknown")),
                            "confidence": item.get("confidence", item.get("score", 0.0)),
                            "bounding_box": item.get("bounding_box", item.get("bbox", {})),
                            "track_id": item.get("track_id")
                        }
                        predictions["0"].append(pred)
        except Exception as e:
            self.logger.warning(f"Failed to extract predictions: {str(e)}")
        return predictions