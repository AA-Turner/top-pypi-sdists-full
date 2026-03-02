from typing import Any, Dict, List, Optional, Tuple
from collections import deque  # FIXED: Added missing import
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
from ..utils.geometry_utils import get_bbox_center, point_in_polygon, get_bbox_bottom25_center

@dataclass
class StoppedVehicleMonitoringConfig(BaseConfig):
    """Minimal configuration - only essential tunable parameters"""
    
    # Core detection parameters
    min_stop_time_sec: float = 10.0
    short_term_displacement_threshold_px: float = 20.0
    long_term_drift_threshold_px: float = 25.0
    
    # Zone configuration
    zone_config: Optional[Dict[str, List[List[float]]]] = None
    zone_iou_threshold: float = 0.3
    
    # Inherited from base
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    confidence_threshold: float = 0.25
    
    # Class aggregation
    enable_class_aggregation: bool = True
    class_aggregation_window_size: int = 30
    
    # Categories
    usecase_categories: List[str] = field(
        default_factory=lambda: ['bicycle', 'motorcycle', 'car', 'van', 'bus', 'truck']
    )
    target_categories: List[str] = field(
        default_factory=lambda: ['bicycle', 'motorcycle', 'car', 'van', 'bus', 'truck']
    )
    
    alert_config: Optional[AlertConfig] = None
    
    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            0: "bicycle",
            1: "motorcycle", 
            2: "car",
            3: "van",
            4: "bus",
            5: "truck"
        }
    )

class StoppedVehicleMonitoringUseCase(BaseProcessor):
    """
    Stopped vehicle detection use case.
    Detects vehicles that have stopped for configurable duration.
    """
    
    def __init__(self):
        super().__init__("stopped_vehicle_monitoring")
        self.category = "traffic"
        self.CASE_TYPE: Optional[str] = 'stopped_vehicle_monitoring'
        self.CASE_VERSION: Optional[str] = '1.0'
        self.target_categories = ['bicycle', 'motorcycle', 'car', 'van', 'bus', 'truck']
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
        self.start_timer = None

        # Stopped vehicle specific state
        self._stopped_vehicle_trackers: Dict[int, 'StoppedVehicleTracker'] = {}
        self._total_stop_events = 0
        self._cleanup_old_trackers_thresholds_sec = 30.0  # Time after which old trackers are removed
        
        # Track ID storage for total count calculation
        self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._tracked_in_zones = set()
        self._total_count = 0
        self._last_update_time = time.time()
        self._total_count_list = []
        
        # Zone-based tracking storage
        self._zone_current_track_ids = {}
        self._zone_total_track_ids = {}
        self._zone_current_counts = {}
        self._zone_total_counts = {}

    def process(self, data: Any, config: ConfigProtocol, context: Optional[ProcessingContext] = None,
                stream_info: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        processing_start = time.time()
        
        # Config validation
        is_valid_config = (
            isinstance(config, StoppedVehicleMonitoringConfig) or
            (hasattr(config, 'usecase') and config.usecase == 'stopped_vehicle_monitoring' and
             hasattr(config, 'category') and config.category == 'traffic')
        )
        if not is_valid_config:
            self.logger.error(
                f"Config validation failed. "
                f"Got type={type(config).__name__}, module={type(config).__module__}"
            )
            return self.create_error_result(
                f"Invalid config type: expected StoppedVehicleMonitoringConfig",
                usecase=self.name, category=self.category, context=context
            )
        
        if context is None:
            context = ProcessingContext()

        # Determine if zones are configured
        has_zones = bool(config.zone_config and config.zone_config.get('zones'))

        # Normalize YOLO outputs
        data = self._normalize_yolo_results(data, getattr(config, 'index_to_category', None))

        input_format = match_results_structure(data)
        context.input_format = input_format
        context.confidence_threshold = config.confidence_threshold
        config.confidence_threshold = 0.25
        # TODO : Threshold param to be updated in config

        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(data, config.confidence_threshold)
            self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
        else:
            processed_data = data
            self.logger.debug("Did not apply confidence filtering since no threshold provided")

        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)
            self.logger.debug("Applied category mapping")

        processed_data = [d for d in processed_data if d.get('category') in self.target_categories]
        if config.target_categories:
            processed_data = [d for d in processed_data if d.get('category') in self.target_categories]


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

            # Advanced tracking
        try:
            from ..advanced_tracker import AdvancedTracker
            from ..advanced_tracker.config import TrackerConfig
            if self.tracker is None:
                tracker_config = TrackerConfig(
                    enable_class_aggregation=config.enable_class_aggregation,
                    class_aggregation_window_size=config.class_aggregation_window_size
                )
                self.tracker = AdvancedTracker(tracker_config)
                self.logger.info(
                    f"Initialized AdvancedTracker for Stopped Vehicle Monitoring "
                    f"(class_aggregation={config.enable_class_aggregation})"
                )
            processed_data = self.tracker.update(processed_data)
        except Exception as e:
            self.logger.warning(f"AdvancedTracker failed: {e}")

        # STOPPED VEHICLE DETECTION 
        current_time = time.time()
        stopped_vehicles = self._detect_stopped_vehicles(
            processed_data, config, current_time, stream_info
        )

        self._update_tracking_state(processed_data, has_zones=has_zones)
        self._total_frame_counter += 1

        # Build stopped vehicle analytics
        stopped_vehicle_analytics = self._build_stopped_vehicle_analytics(
            stopped_vehicles, config, current_time, stream_info
        )

        # Extract frame number
        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        # Standard counting summary
        general_counting_summary = calculate_counting_summary(data)
        counting_summary = self._count_categories(processed_data, config)
        total_counts = self.get_total_counts()
        counting_summary['total_counts'] = total_counts
        counting_summary['categories'] = {}
        for detection in processed_data:
            category = detection.get("category", "unknown")
            counting_summary["categories"][category] = counting_summary["categories"].get(category, 0) + 1

        # Zone analysis
        zone_analysis = {}
        if has_zones:
            frame_data = processed_data
            zone_analysis = count_objects_in_zones(frame_data, config.zone_config['zones'], stream_info)

            if zone_analysis:
                enhanced_zone_analysis = self._update_zone_tracking(zone_analysis, processed_data, config)
                for zone_name, enhanced_data in enhanced_zone_analysis.items():
                    zone_analysis[zone_name] = enhanced_data

                per_category_count = {cat: len(self._current_frame_track_ids.get(cat, set())) for cat in self.target_categories}
                counting_summary['per_category_count'] = {k: v for k, v in per_category_count.items() if v > 0}
                counting_summary['total_count'] = sum(per_category_count.values())

        # Alerts and predictions
        alerts = self._check_alerts(counting_summary, zone_analysis, frame_number, config)
        predictions = self._extract_predictions(processed_data)

        # Generate outputs
        incidents_list = self._generate_incidents(counting_summary, zone_analysis, alerts, config, frame_number, stream_info)
        incidents_list = []
        tracking_stats_list = self._generate_tracking_stats(counting_summary, zone_analysis, alerts, config, frame_number, stream_info)
        business_analytics_list = self._generate_business_analytics(counting_summary, zone_analysis, alerts, config, stream_info, is_empty=True)
        summary_list = self._generate_summary(counting_summary, zone_analysis, incidents_list, tracking_stats_list, business_analytics_list, alerts)

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
            "stopped_vehicle_analytics": stopped_vehicle_analytics,  
            "human_text": summary}
        }

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
        print("latency in ms:", processing_latency_ms, "| Throughput fps:", processing_fps, "| Frame_Number:", self._total_frame_counter)
        return result
    
    def _detect_stopped_vehicles(self, detections: List[Dict], config: StoppedVehicleMonitoringConfig,
                             current_time: float, stream_info: Optional[Dict]) -> List[Dict]:
        """
        Core stopped vehicle detection logic.

        Returns list of stopped vehicle dictionaries with:
        - track_id
        - category
        - bbox
        - stationary_duration_sec
        - zone_id (if applicable)
        """
        zones = config.zone_config.get('zones', {}) if config.zone_config else {}

        # Track current frame's track IDs
        current_track_ids = set()
        stopped_vehicles = []

        for det in detections:
            track_id = det.get('track_id')
            if track_id is None:
                continue
            
            current_track_ids.add(track_id)
            bbox = det.get('bounding_box', det.get('bbox'))
            category = det.get('category', 'vehicle')
            
            # Determine zone membership
            zone_name = None
            if zones:
                zone_name = self._compute_zone_membership(bbox, zones)
            
            # Update or create tracker
            if track_id not in self._stopped_vehicle_trackers:
                # New track
                tracker = StoppedVehicleTracker(track_id, bbox, current_time, zone_name)
                tracker.category = category
                self._stopped_vehicle_trackers[track_id] = tracker
            else:
                # Existing track - update
                tracker = self._stopped_vehicle_trackers[track_id]
                tracker.category = category
                
                # Store previous state before update
                was_stopped_before = tracker.stop_confirmed
                
                # Update tracker
                tracker.update(bbox, current_time, zone_name)
                
                # If newly confirmed as stopped, increment total events
                if tracker.stop_confirmed and not was_stopped_before:
                    self._total_stop_events += 1
            
            # Collect stopped vehicles
            tracker = self._stopped_vehicle_trackers[track_id]
            if tracker.stop_confirmed:
                stopped_vehicles.append({
                    'track_id': track_id,
                    'category': category,
                    'bbox': bbox,
                    'stationary_duration_sec': tracker.get_stationary_duration(current_time),
                    'zone_id': zone_name
                })

        # Clean up trackers for tracks that are no longer detected
        self._cleanup_old_trackers(current_track_ids, current_time)

        return stopped_vehicles

    def _cleanup_old_trackers(self, current_track_ids: set, current_time: float):
        """Remove trackers for tracks not seen recently"""
        to_remove = []
        for track_id, tracker in self._stopped_vehicle_trackers.items():
            if track_id not in current_track_ids:
                # Track not in current frame
                time_since_seen = current_time - tracker.last_seen
                if time_since_seen > self._cleanup_old_trackers_thresholds_sec:  
                    to_remove.append(track_id)

        for track_id in to_remove:
            del self._stopped_vehicle_trackers[track_id]

    def _build_stopped_vehicle_analytics(self, stopped_vehicles: List[Dict], 
                                     config: StoppedVehicleMonitoringConfig,
                                     current_time: float,
                                     stream_info: Optional[Dict]) -> Dict:
        """
        Build stopped vehicle analytics output.
        
        Output format:
        {
            "active_tracks": [...],
            "total_events": int,
            "current_count": int,
            "zone_analytics": {...}  # Optional - only if zones configured
        }
        """
        analytics = {
            "active_tracks": stopped_vehicles,
            "total_events": self._total_stop_events,
            "current_count": len(stopped_vehicles)
        }
        
        # Add zone-specific analytics if zones are configured
        zones = config.zone_config.get('zones', {}) if config.zone_config else {}
        if zones:
            zone_analytics = {}
            for zone_name in zones.keys():
                zone_stopped = [v for v in stopped_vehicles if v.get('zone_id') == zone_name]
                
                if zone_stopped:
                    durations = [v['stationary_duration_sec'] for v in zone_stopped]
                    zone_analytics[zone_name] = {
                        "current_stopped": len(zone_stopped),
                        "avg_stop_duration_sec": sum(durations) / len(durations),
                        "longest_stop_sec": max(durations)
                    }
                else:
                    zone_analytics[zone_name] = {
                        "current_stopped": 0,
                        "avg_stop_duration_sec": 0.0,
                        "longest_stop_sec": 0.0
                    }
            
            analytics["zone_analytics"] = zone_analytics
        
        return analytics
    
    def _update_zone_tracking(self, zone_analysis: Dict[str, Dict[str, int]], detections: List[Dict], 
                             config: StoppedVehicleMonitoringConfig) -> Dict[str, Dict[str, Any]]:
        """
        Update zone tracking with current frame data.
        
        Args:
            zone_analysis: Current zone analysis results
            detections: List of detections with track IDs
            
        Returns:
            Enhanced zone analysis with tracking information
        """
        if not zone_analysis or not config.zone_config or not config.zone_config['zones']:
            return {}
        
        enhanced_zone_analysis = {}
        zones = config.zone_config['zones']
        
        # Get track to category mapping
        track_to_cat = {det.get('track_id'): det.get('category') for det in detections if det.get('track_id') is not None}
        
        # Get current frame track IDs in each zone
        current_frame_zone_tracks = {}
        
        # Initialize zone tracking for all zones
        for zone_name in zones.keys():
            current_frame_zone_tracks[zone_name] = set()
            if zone_name not in self._zone_current_track_ids:
                self._zone_current_track_ids[zone_name] = set()
            if zone_name not in self._zone_total_track_ids:
                self._zone_total_track_ids[zone_name] = set()
        
        # Check each detection against each zone
        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None:
                continue
            
            # Get detection bbox
            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue
            
            # Get detection center point
            center_point = get_bbox_bottom25_center(bbox)
            
            # Flag to check if this track is in any zone this frame
            in_any_zone = False
            
            # Check which zone this detection is in using actual zone polygons
            for zone_name, zone_polygon in zones.items():
                # Convert polygon points to tuples for point_in_polygon function
                polygon_points = [(point[0], point[1]) for point in zone_polygon]
                
                # Check if detection center is inside the zone polygon
                if point_in_polygon(center_point, polygon_points):
                    current_frame_zone_tracks[zone_name].add(track_id)
                    in_any_zone = True
                    if track_id not in self._total_count_list:
                        self._total_count_list.append(track_id)
            
            # If in any zone, update global current and total
            if in_any_zone:
                cat = track_to_cat.get(track_id)
                if cat:
                    # Update current frame global (union across zones)
                    self._current_frame_track_ids.setdefault(cat, set()).add(track_id)
                    
                    # Update global cumulative if first time in any zone
                    if track_id not in self._tracked_in_zones:
                        self._tracked_in_zones.add(track_id)
                        self._per_category_total_track_ids.setdefault(cat, set()).add(track_id)

        # Update zone tracking for each zone
        for zone_name, zone_counts in zone_analysis.items():
            # Get current frame tracks for this zone
            current_tracks = current_frame_zone_tracks.get(zone_name, set())
            
            # Update current zone tracks
            self._zone_current_track_ids[zone_name] = current_tracks
            
            # Update total zone tracks
            self._zone_total_track_ids[zone_name].update(current_tracks)
            
            # Update counts
            self._zone_current_counts[zone_name] = len(current_tracks)
            self._zone_total_counts[zone_name] = len(self._zone_total_track_ids[zone_name])

            # Create enhanced zone analysis
            enhanced_zone_analysis[zone_name] = {
                "current_count": self._zone_current_counts[zone_name],
                "total_count": self._zone_total_counts[zone_name],
                "current_track_ids": list(current_tracks),
                "total_track_ids": list(self._zone_total_track_ids[zone_name]),
                "original_counts": zone_counts
            }
        
        return enhanced_zone_analysis
        
    def _compute_zone_membership(self, bbox: Dict, zones: Dict[str, List[List[float]]]) -> Optional[str]:
        """
        Determine which zone (if any) the vehicle belongs to.
        
        Strategy:
        1. Compute IOU between bbox and zone bounding box
        2. If IOU >= 0.5: definitely in zone
        3. If 0.1 <= IOU < 0.5: use centroid check as tiebreaker
        4. If IOU < 0.1: not in zone
        
        Returns zone_name or None
        """
        if not zones:
            return None
        
        vehicle_bbox = self._normalize_bbox(bbox)
        best_zone = None
        best_iou = 0.0
        
        for zone_name, zone_polygon in zones.items():
            # Compute zone bounding box
            zone_bbox = self._polygon_to_bbox(zone_polygon)
            
            # Compute IOU
            iou = self._compute_iou_bbox(vehicle_bbox, zone_bbox)
            
            if iou >= 0.5:
                # High overlap - definitely in this zone
                if iou > best_iou:
                    best_iou = iou
                    best_zone = zone_name
            elif iou >= 0.1:
                # Moderate overlap - check centroid as tiebreaker
                centroid = get_bbox_center(bbox)
                polygon_points = [(p[0], p[1]) for p in zone_polygon]
                if point_in_polygon(centroid, polygon_points):
                    if iou > best_iou:
                        best_iou = iou
                        best_zone = zone_name
        
        return best_zone

    def _polygon_to_bbox(self, polygon: List[List[float]]) -> Dict:
        """Convert polygon to axis-aligned bounding box"""
        xs = [p[0] for p in polygon]
        ys = [p[1] for p in polygon]
        return {
            'xmin': min(xs),
            'ymin': min(ys),
            'xmax': max(xs),
            'ymax': max(ys)
        }
    

    def _compute_iou_bbox(self, bbox1: Dict, bbox2: Dict) -> float:
        """Compute IOU between two bboxes"""
        x1_min, y1_min = bbox1['xmin'], bbox1['ymin']
        x1_max, y1_max = bbox1['xmax'], bbox1['ymax']
        x2_min, y2_min = bbox2['xmin'], bbox2['ymin']
        x2_max, y2_max = bbox2['xmax'], bbox2['ymax']
        
        inter_xmin = max(x1_min, x2_min)
        inter_ymin = max(y1_min, y2_min)
        inter_xmax = min(x1_max, x2_max)
        inter_ymax = min(y1_max, y2_max)
        
        if inter_xmax < inter_xmin or inter_ymax < inter_ymin:
            return 0.0
        
        inter_area = (inter_xmax - inter_xmin) * (inter_ymax - inter_ymin)
        area1 = (x1_max - x1_min) * (y1_max - y1_min)
        area2 = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = area1 + area2 - inter_area
        
        return inter_area / union_area if union_area > 0 else 0.0

    def _normalize_bbox(self, bbox: Dict) -> Dict:
        """
        FIXED: Added missing method
        Normalize bbox to xmin/ymin/xmax/ymax format.
        
        Args:
            bbox: Bounding box in various formats
            
        Returns:
            Normalized bbox dict with xmin, ymin, xmax, ymax keys
        """
        if 'xmin' in bbox and 'xmax' in bbox:
            return {
                'xmin': bbox['xmin'],
                'ymin': bbox['ymin'],
                'xmax': bbox['xmax'],
                'ymax': bbox['ymax']
            }
        elif 'x1' in bbox and 'x2' in bbox:
            return {
                'xmin': bbox['x1'],
                'ymin': bbox['y1'],
                'xmax': bbox['x2'],
                'ymax': bbox['y2']
            }
        else:
            values = [v for v in bbox.values() if isinstance(v, (int, float))]
            if len(values) >= 4:
                return {
                    'xmin': values[0],
                    'ymin': values[1],
                    'xmax': values[2],
                    'ymax': values[3]
                }
            return {'xmin': 0, 'ymin': 0, 'xmax': 0, 'ymax': 0}
        

    def _normalize_yolo_results(self, data: Any, index_to_category: Optional[Dict[int, str]] = None) -> Any:
        """
        Normalize YOLO-style outputs to internal detection schema.
        """
        def to_bbox_dict(d: Dict[str, Any]) -> Dict[str, Any]:
            if "bounding_box" in d and isinstance(d["bounding_box"], dict):
                return d["bounding_box"]
            if "bbox" in d:
                bbox = d["bbox"]
                if isinstance(bbox, dict):
                    return bbox
                if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
                    x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
                    return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
            if "xyxy" in d and isinstance(d["xyxy"], (list, tuple)) and len(d["xyxy"]) >= 4:
                x1, y1, x2, y2 = d["xyxy"][0], d["xyxy"][1], d["xyxy"][2], d["xyxy"][3]
                return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
            if "xywh" in d and isinstance(d["xywh"], (list, tuple)) and len(d["xywh"]) >= 4:
                cx, cy, w, h = d["xywh"][0], d["xywh"][1], d["xywh"][2], d["xywh"][3]
                x1, y1, x2, y2 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
                return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
            return {}

        def resolve_category(d: Dict[str, Any]) -> Tuple[str, Optional[int]]:
            raw_cls = d.get("category", d.get("category_id", d.get("class", d.get("cls"))))
            label_name = d.get("name")
            if isinstance(raw_cls, int):
                if index_to_category and raw_cls in index_to_category:
                    return index_to_category[raw_cls], raw_cls
                return str(raw_cls), raw_cls
            if isinstance(raw_cls, str):
                return raw_cls, None
            if label_name:
                return str(label_name), None
            return "unknown", None

        def normalize_det(det: Dict[str, Any]) -> Dict[str, Any]:
            category_name, category_id = resolve_category(det)
            confidence = det.get("confidence", det.get("conf", det.get("score", 0.0)))
            bbox = to_bbox_dict(det)
            normalized = {
                "category": category_name,
                "confidence": confidence,
                "bounding_box": bbox,
            }
            if category_id is not None:
                normalized["category_id"] = category_id
            for key in ("track_id", "frame_id", "masks", "segmentation"):
                if key in det:
                    normalized[key] = det[key]
            return normalized

        if isinstance(data, list):
            return [normalize_det(d) if isinstance(d, dict) else d for d in data]
        if isinstance(data, dict):
            normalized_dict: Dict[str, Any] = {}
            for k, v in data.items():
                if isinstance(v, list):
                    normalized_dict[k] = [normalize_det(d) if isinstance(d, dict) else d for d in v]
                elif isinstance(v, dict):
                    normalized_dict[k] = normalize_det(v)
                else:
                    normalized_dict[k] = v
            return normalized_dict
        return data
    

    def _check_alerts(self, summary: dict, zone_analysis: Dict, frame_number: Any, 
                     config: StoppedVehicleMonitoringConfig) -> List[Dict]:
        """Check if alert thresholds are exceeded"""
        def get_trend(data, lookback=900, threshold=0.6):
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True
            increasing = 0
            total = 0
            for i in range(1, len(window)):
                if window[i] >= window[i - 1]:
                    increasing += 1
                total += 1
            ratio = increasing / total
            return ratio >= threshold

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
                elif category in per_category_count and per_category_count[category] > threshold:
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
    

    def _generate_incidents(self, counting_summary: Dict, zone_analysis: Dict, alerts: List, 
                           config: StoppedVehicleMonitoringConfig,
                           frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """
        FIXED: Updated to include stopped vehicle information
        """
        incidents = []
        total_detections = counting_summary.get("total_count", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        self._ascending_alert_list = self._ascending_alert_list[-900:] if len(self._ascending_alert_list) > 900 else self._ascending_alert_list

        # FIXED: Get stopped vehicle count
        stopped_confirmed_count = sum(1 for t in self._stopped_vehicle_trackers.values() if t.stop_confirmed)
        
        if total_detections > 0 or stopped_confirmed_count > 0:
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

            # FIXED: Consider stopped vehicles in severity calculation
            effective_count = total_detections + stopped_confirmed_count
            
            if config.alert_config and hasattr(config.alert_config, 'count_thresholds') and config.alert_config.count_thresholds:
                threshold = config.alert_config.count_thresholds.get("all", 15)
                intensity = min(10.0, (effective_count / threshold) * 10)
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
                if effective_count > 30:
                    level = "critical"
                    intensity = 10.0
                    self._ascending_alert_list.append(3)
                elif effective_count > 25:
                    level = "significant"
                    intensity = 9.0
                    self._ascending_alert_list.append(2)
                elif effective_count > 15:
                    level = "medium"
                    intensity = 7.0
                    self._ascending_alert_list.append(1)
                else:
                    level = "low"
                    intensity = min(10.0, effective_count / 3.0)
                    self._ascending_alert_list.append(0)

            human_text_lines = [f"STOPPED VEHICLE INCIDENTS DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            
            # FIXED: Add stopped vehicle details
            if stopped_confirmed_count > 0:
                human_text_lines.append(f"\tStopped Vehicles: {stopped_confirmed_count}")
                # List longest stopped durations
                sorted_trackers = sorted(
                    [t for t in self._stopped_vehicle_trackers.values() if t.stop_confirmed],
                    key=lambda t: t.get_stationary_duration(time.time()),
                    reverse=True
                )
                if sorted_trackers:
                    longest = sorted_trackers[0]
                    duration = longest.get_stationary_duration(time.time())
                    human_text_lines.append(f"\tLongest Stop: {duration:.1f}s (Track ID: {longest.track_id})")
            
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
                incident_id=f"{self.CASE_TYPE}_{frame_number}",
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
    

    def _generate_tracking_stats(self, counting_summary: Dict, zone_analysis: Dict, alerts: List, 
                                config: StoppedVehicleMonitoringConfig,
                                frame_number: Optional[int] = None, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """
        FIXED: Updated to include stopped vehicle information in human text
        """
        camera_info = self.get_camera_info_from_stream(stream_info)
        tracking_stats = []
        total_detections = counting_summary.get("total_count", 0)
        total_counts_dict = counting_summary.get("total_counts", {})
        per_category_count = counting_summary.get("per_category_count", {})
        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        total_counts = [{"category": cat, "count": count} for cat, count in total_counts_dict.items() if count > 0]
        current_counts = [{"category": cat, "count": count} for cat, count in per_category_count.items() if count > 0 or total_detections > 0]

        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "vehicle")
            if detection.get("masks"):
                segmentation = detection.get("masks", [])
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            elif detection.get("segmentation"):
                segmentation = detection.get("segmentation")
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            elif detection.get("mask"):
                segmentation = detection.get("mask")
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            else:
                detection_obj = self.create_detection_object(category, bbox)
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

        # Generate human text
        human_text_lines = []
        human_text_lines.append(f"CURRENT FRAME @ {current_timestamp}:")

        # Display current counts - zone-wise or category-wise
        if zone_analysis:
            human_text_lines.append("\t- Vehicles Detected by Zone:")
            for zone_name, zone_data in zone_analysis.items():
                current_count = 0
                if isinstance(zone_data, dict):
                    if "current_count" in zone_data:
                        current_count = zone_data.get("current_count", 0)
                    else:
                        counts_dict = zone_data.get("original_counts") if isinstance(zone_data.get("original_counts"), dict) else zone_data
                        current_count = counts_dict.get(
                            "total",
                            sum(v for v in counts_dict.values() if isinstance(v, (int, float)))
                        )
                human_text_lines.append(f"\t\t- {zone_name}: {int(current_count)}")
        else:
            human_text_lines.append(f"\t- Vehicles Detected: {total_detections}")
            if per_category_count:
                for cat, count in per_category_count.items():
                    if count > 0:
                        human_text_lines.append(f"\t\t- {cat}: {count}")

        # FIXED: Add stopped vehicle information
        stopped_count = len(self._stopped_vehicle_trackers)
        stopped_confirmed_count = sum(1 for t in self._stopped_vehicle_trackers.values() if t.stop_confirmed)
        
        if stopped_confirmed_count > 0:
            human_text_lines.append("")
            human_text_lines.append(f"\t- Stopped Vehicles: {stopped_confirmed_count}")
            
            # Group by zone if zones are configured
            if zone_analysis:
                zone_stopped = {}
                for track_id, tracker in self._stopped_vehicle_trackers.items():
                    if tracker.stop_confirmed and tracker.current_zone:
                        zone_stopped.setdefault(tracker.current_zone, []).append(tracker)
                
                if zone_stopped:
                    for zone_name, trackers in zone_stopped.items():
                        avg_duration = sum(t.get_stationary_duration(time.time()) for t in trackers) / len(trackers)
                        human_text_lines.append(f"\t\t- {zone_name}: {len(trackers)} (avg duration: {avg_duration:.1f}s)")

        human_text_lines.append("")

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
        tracking_stat['target_categories'] = self.target_categories
        
        # FIXED: Add stopped vehicle analytics to tracking_stat
        tracking_stat['stopped_vehicle_count'] = stopped_confirmed_count
        tracking_stat['stopped_vehicle_trackers'] = stopped_count
        
        tracking_stats.append(tracking_stat)
        return tracking_stats

    def _generate_business_analytics(self, counting_summary: Dict, zone_analysis: Dict, alerts: Any, 
                                     config: StoppedVehicleMonitoringConfig,
                                     stream_info: Optional[Dict[str, Any]] = None, is_empty=False) -> List[Dict]:
        """Generate business analytics (placeholder)"""
        if is_empty:
            return []

    def _generate_summary(self, counting_summary: Dict, zone_analysis: Dict, incidents: List, 
                         tracking_stats: List, business_analytics: List, alerts: List) -> List[str]:
        """
        FIXED: Parameter name changed from 'summary' to 'counting_summary'
        Generate a human_text string for the tracking_stat, incident, business analytics and alerts.
        """
        lines = []
        lines.append("Application Name: " + self.CASE_TYPE)
        lines.append("Application Version: " + self.CASE_VERSION)
        if len(incidents) > 0:
            lines.append("Incidents: " + f"\n\t{incidents[0].get('human_text', 'No incidents detected')}")
        if len(tracking_stats) > 0:
            lines.append("Tracking Statistics: " + f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}")
        if len(business_analytics) > 0:
            lines.append("Business Analytics: " + f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}")

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines.append("Summary: " + "No Summary Data")

        return ["\n".join(lines)]
    

    def _get_track_ids_info(self, detections: list) -> Dict[str, Any]:
        """Get track ID statistics"""
        frame_track_ids = set()
        for det in detections:
            tid = det.get('track_id')
            if tid is not None:
                frame_track_ids.add(tid)
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

    def _update_tracking_state(self, detections: list, has_zones: bool = False):
        """Update tracking state for category counting"""
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
            if not has_zones:
                self._per_category_total_track_ids.setdefault(cat, set()).add(canonical_id)
            self._current_frame_track_ids.setdefault(cat, set()).add(canonical_id)

    def get_total_counts(self):
        """Get total unique counts per category"""
        return {cat: len(ids) for cat, ids in getattr(self, '_per_category_total_track_ids', {}).items()}

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        """Format timestamp for stream display"""
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        """Format timestamp for video display"""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp to match the current timestamp format: YYYY:MM:DD HH:MM:SS."""
        # Convert numeric timestamps to datetime first
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp, timezone.utc)
            return dt.strftime('%Y:%m:%d %H:%M:%S')

        if not isinstance(timestamp, str):
            return str(timestamp)

        timestamp_clean = timestamp.replace(' UTC', '').strip()

        if '.' in timestamp_clean:
            timestamp_clean = timestamp_clean.split('.')[0]

        try:
            if timestamp_clean.count('-') >= 2:
                parts = timestamp_clean.split('-')
                if len(parts) >= 4:
                    formatted = f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
                    return formatted
        except Exception:
            pass

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
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
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

    def _count_categories(self, detections: list, config: StoppedVehicleMonitoringConfig) -> dict:
        """Count detections by category"""
        counts = {}
        for det in detections:
            cat = det.get('category', 'unknown')
            counts[cat] = counts.get(cat, 0) + 1
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

    def _extract_predictions(self, detections: list) -> List[Dict[str, Any]]:
        """Extract prediction details"""
        return [
            {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", {})
            }
            for det in detections
        ]
    

    def _compute_iou(self, box1: Any, box2: Any) -> float:
        """Compute IOU between two bounding boxes"""
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
        """Merge or register track for canonical ID management"""
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

    def _get_tracking_start_time(self) -> str:
        """Get tracking start time as formatted string"""
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        """Set tracking start time to current time"""
        self._tracking_start_time = time.time()


class StoppedVehicleTracker:
    """
    Per-track state for stopped vehicle detection.
    Uses hybrid approach: displacement buffer for jitter + EWMA for drift.
    """
    
    def __init__(self, track_id: int, initial_bbox: Dict, timestamp: float, 
                 zone_name: Optional[str] = None):
        self.track_id = track_id
        self.category = None
        
        # Motion analysis
        self.position_buffer = deque(maxlen=30)  # Last 30 positions
        self.position_buffer.append(self._bbox_to_position(initial_bbox))
        
        # EWMA smoothing
        self.ewma_centroid = self._compute_centroid(initial_bbox)
        self.ewma_alpha = 0.3  # Smoothing factor
        
        # Timing
        self.first_seen = timestamp
        self.last_seen = timestamp
        self.stationary_start_time = timestamp  # When became stationary
        self.frame_count = 1
        
        # State
        self.is_stopped = False
        self.stop_confirmed = False
        
        # Zone tracking
        self.current_zone = zone_name
        self.zone_entry_time = timestamp if zone_name else None
        self.last_bbox = initial_bbox
        
    def _bbox_to_position(self, bbox: Dict) -> Tuple[float, float, float, float]:
        """Extract (x_center, y_center, width, height)"""
        if 'xmin' in bbox:
            x = (bbox['xmin'] + bbox['xmax']) / 2
            y = (bbox['ymin'] + bbox['ymax']) / 2
            w = bbox['xmax'] - bbox['xmin']
            h = bbox['ymax'] - bbox['ymin']
        else:  # x1, y1, x2, y2
            x = (bbox['x1'] + bbox['x2']) / 2
            y = (bbox['y1'] + bbox['y2']) / 2
            w = bbox['x2'] - bbox['x1']
            h = bbox['y2'] - bbox['y1']
        return (x, y, w, h)
    
    def _compute_centroid(self, bbox: Dict) -> Tuple[float, float]:
        """Get bbox center"""
        pos = self._bbox_to_position(bbox)
        return (pos[0], pos[1])
    
    def update(self, bbox: Dict, timestamp: float, zone_name: Optional[str] = None) -> bool:
        """
        Update track state and return True if vehicle is confirmed stopped.
        
        Algorithm:
        1. Update position buffer
        2. Update EWMA centroid
        3. Check short-term jitter (buffer analysis)
        4. Check long-term drift (EWMA analysis)
        5. Confirm stopped state if both conditions met
        """
        current_pos = self._bbox_to_position(bbox)
        current_centroid = (current_pos[0], current_pos[1])
        
        # Update buffers
        self.position_buffer.append(current_pos)
        self.last_bbox = bbox
        self.last_seen = timestamp
        self.frame_count += 1
        
        # Update EWMA centroid
        self.ewma_centroid = (
            self.ewma_alpha * current_centroid[0] + (1 - self.ewma_alpha) * self.ewma_centroid[0],
            self.ewma_alpha * current_centroid[1] + (1 - self.ewma_alpha) * self.ewma_centroid[1]
        )
        
        # Zone tracking
        if zone_name != self.current_zone:
            if zone_name:  # Entering zone
                self.zone_entry_time = timestamp
            else:  # Leaving zone
                self.zone_entry_time = None
            self.current_zone = zone_name
        
        # Check if stationary
        is_stationary_now = self._check_stationary()
        
        if is_stationary_now:
            if not self.is_stopped:
                # Just became stationary
                self.stationary_start_time = timestamp
                self.is_stopped = True
        else:
            # Vehicle is moving
            if self.is_stopped:
                # Reset stopped state
                self.is_stopped = False
                self.stop_confirmed = False
                self.stationary_start_time = timestamp
        
        # Confirm stopped if stationary for minimum duration
        if self.is_stopped:
            stationary_duration = timestamp - self.stationary_start_time
            if stationary_duration >= 10.0 and not self.stop_confirmed:  # 10 seconds
                self.stop_confirmed = True
        
        return self.stop_confirmed
    
    def _check_stationary(self) -> bool:
        """
        Hybrid motion check:
        - Short-term: Max displacement in buffer < 20px
        - Long-term: EWMA drift from initial < 25px
        """
        if len(self.position_buffer) < 10:  # Need minimum history
            return False
        
        # Short-term jitter check (buffer analysis)
        positions = list(self.position_buffer)
        max_displacement = 0.0
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                dx = positions[i][0] - positions[j][0]
                dy = positions[i][1] - positions[j][1]
                dist = (dx**2 + dy**2) ** 0.5
                max_displacement = max(max_displacement, dist)
        
        short_term_stationary = max_displacement < 20.0  # pixels
        
        # Long-term drift check (EWMA vs initial position)
        initial_pos = self.position_buffer[0]
        dx = self.ewma_centroid[0] - initial_pos[0]
        dy = self.ewma_centroid[1] - initial_pos[1]
        ewma_drift = (dx**2 + dy**2) ** 0.5
        
        long_term_stationary = ewma_drift < 25.0  # pixels
        
        return short_term_stationary and long_term_stationary
    
    def get_stationary_duration(self, current_time: float) -> float:
        """Get time since vehicle became stationary (seconds)"""
        if self.is_stopped:
            return current_time - self.stationary_start_time
        return 0.0