"""
Advanced customer service use case implementation.

This module provides comprehensive customer service analytics with advanced tracking,
journey analysis, queue management, and detailed business intelligence metrics.
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import field
import time
import math
from collections import defaultdict

from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol
from ..core.config import CustomerServiceConfig, TrackingConfig, AlertConfig
from ..utils import (
    filter_by_confidence,
    apply_category_mapping,
    point_in_polygon,
    get_bbox_center,
    calculate_distance,
    match_results_structure
)

def assign_person_by_area(detections, customer_areas, staff_areas):
    """
    Assigns category 'person' detections to 'staff' or 'customer' based on their location in area polygons.
    Modifies the detection list in-place.
    Args:
        detections: List of detection dicts.
        customer_areas: Dict of area_name -> polygon (list of [x, y]).
        staff_areas: Dict of area_name -> polygon (list of [x, y]).
    """
    # Track staff by track_id so staff status persists even if they enter customer area
    staff_track_ids = set()
    # First pass: assign staff and remember their track_ids
    for det in detections:
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
    # Second pass: assign customer only if not a known staff track_id
    for det in detections:
        if det.get('category') == 'person' and det.get('track_id') not in staff_track_ids:
            det['category'] = 'customer'
        elif det.get('category') == 'person' and det.get('track_id') in staff_track_ids:
            det['category'] = 'staff'

class AdvancedCustomerServiceUseCase(BaseProcessor):
    def _generate_per_frame_agg_summary(self, processed_data, analytics_results, config, context, stream_info=None):
        """
        Generate agg_summary dict with per-frame events and tracking_stats.
        processed_data: dict of frame_id -> detections (list)
        analytics_results: output of _compile_analytics_results 
        """
        import datetime
        frame_events = {}
        frame_tracking_stats = {}
        # For total_frames_processed, use a counter or fallback to len(processed_data)
        total_frames_processed = getattr(self, '_total_frames_processed', 0)
        global_frame_offset = getattr(self, 'global_frame_offset', 0)
        # For each frame, build event and tracking_stats dicts
        for frame_id, detections in processed_data.items():
            # Count staff/customers in this frame
            staff_count = sum(1 for d in detections if d.get('category') == 'staff')
            customer_count = sum(1 for d in detections if d.get('category') == 'customer')
            total_people = staff_count + customer_count
            # Event (match people_counting)
            event = {
                "type": "advanced_customer_service",
                "stream_time": datetime.datetime.utcnow().strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "application_name": "Advanced Customer Service System",
                "application_version": "1.0",
                "location_info": None,
                "human_text": f"EVENTS DETECTED:\n\t- Staff Detected: {staff_count}\n\t- Customers Detected: {customer_count}",
                "frame_id": str(frame_id)
            }
            frame_events[str(frame_id)] = [event]
            # Tracking stats (match people_counting fields)
            # Use the full summary for each frame's human_text, but exclude queue_lengths_by_area, service_proximity_threshold, and real_time_occupancy
            # Prepare a filtered analytics_results for summary
            filtered_analytics = dict(analytics_results)
            if "customer_queue_analytics" in filtered_analytics:
                filtered_analytics["customer_queue_analytics"] = dict(filtered_analytics["customer_queue_analytics"])
                filtered_analytics["customer_queue_analytics"].pop("queue_lengths_by_area", None)
            if "service_area_analytics" in filtered_analytics:
                filtered_analytics["service_area_analytics"] = dict(filtered_analytics["service_area_analytics"])
                filtered_analytics["service_area_analytics"].pop("service_proximity_threshold", None)
            filtered_analytics.pop("real_time_occupancy", None)
            full_summary = self._generate_summary(filtered_analytics, [])
            tracking_stat = {
                "tracking_start_time": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
                "all_results_for_tracking": {
                    "total_people": total_people,
                    "staff_count": staff_count,
                    "customer_count": customer_count,
                    "detections": detections,
                    "business_metrics": analytics_results.get("business_metrics", {}),
                    "customer_queue_analytics": filtered_analytics.get("customer_queue_analytics", {}),
                    "staff_management_analytics": analytics_results.get("staff_management_analytics", {}),
                    "service_area_analytics": filtered_analytics.get("service_area_analytics", {}),
                    "customer_journey_analytics": analytics_results.get("customer_journey_analytics", {}),
                    # "real_time_occupancy": analytics_results.get("real_time_occupancy", {}),
                    "service_times": analytics_results.get("service_times", []),
                    "global_frame_offset": global_frame_offset,
                    "local_frame_id": str(frame_id)
                },
                "human_text": full_summary,
                "frame_id": str(frame_id),
                "frames_in_this_call": 1,
                "total_frames_processed": total_frames_processed + int(frame_id),
                "current_frame_number": str(frame_id),
                "global_frame_offset": global_frame_offset
            }
            frame_tracking_stats[str(frame_id)] = [tracking_stat]
        return {"events": frame_events, "tracking_stats": frame_tracking_stats}
    # --- Chunk tracking for per-chunk analytics ---
    def _init_chunk_tracking(self):
        self._chunk_frame_count = 0
        self._chunk_customer_ids = set()
        self._chunk_area_customer_ids = defaultdict(set)

    def _update_chunk_tracking(self, customer_detections):
        for customer in customer_detections:
            track_id = customer.get('track_id')
            if track_id is not None:
                self._chunk_customer_ids.add(track_id)
                # Find all areas this customer is in (from current_areas or by geometry)
                if 'current_areas' in customer:
                    for area in customer['current_areas']:
                        self._chunk_area_customer_ids[area].add(track_id)
                else:
                    # fallback: try to infer from bbox and self.customer_areas
                    customer_center = get_bbox_center(customer.get('bbox', customer.get('bounding_box', {})))
                    for area_name, polygon in getattr(self, 'customer_areas', {}).items():
                        if point_in_polygon(customer_center, polygon):
                            self._chunk_area_customer_ids[area_name].add(track_id)

    def _maybe_reset_chunk(self):
        if not hasattr(self, '_chunk_frame_count'):
            self._init_chunk_tracking()
        self._chunk_frame_count += 1
        if self._chunk_frame_count > 10:
            self._init_chunk_tracking()
    def __init__(self):
        """Initialize advanced customer service use case."""
        super().__init__("advanced_customer_service")
        self.category = "sales"

        # Advanced tracking structures
        self.customer_occupancy = {}
        self.staff_occupancy = {}
        self.service_occupancy = {}
        self.customer_queue_times = {}
        self.customer_service_times = {}
        self.customer_journey = {}
        self.staff_availability = {}
        self.staff_service_count = defaultdict(int)
        self.staff_active_services = {}

        # Persistent unique staff tracking
        self.global_staff_ids = set()
        self.global_staff_ids_by_area = defaultdict(set)

        # Persistent unique customer tracking
        self.global_customer_ids = set()

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
        """Get configuration schema for advanced customer service."""
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
                "customer_areas": {
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
                    "description": "Customer area definitions as polygons"
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
                "customer_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["customer", "person"],
                    "description": "Category names that represent customers"
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
                    "description": "Enable customer journey analysis"
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
                }
            },
            "required": ["confidence_threshold"],
            "additionalProperties": False
        }
    
    def create_default_config(self, **overrides) -> CustomerServiceConfig:
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
            "customer_categories": ["customer", "person"],
            "service_proximity_threshold": 100.0,
            "max_service_time": 1800.0,
            "buffer_time": 2.0,
            "stream_info": {},  
        }
        defaults.update(overrides)
        return CustomerServiceConfig(**defaults)
    
    def process(self, data: Any, config: ConfigProtocol,
                context: Optional[ProcessingContext] = None, stream_info: Optional[dict] = None) -> ProcessingResult:
        """
        Process advanced customer service analytics.
        """
        start_time = time.time()

        try:
            if not isinstance(config, CustomerServiceConfig):
                return self.create_error_result(
                    "Invalid configuration type for advanced customer service",
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

            self.logger.info(f"Processing advanced customer service with format: {input_format.value}")

            self._initialize_areas(config.customer_areas, config.staff_areas, config.service_areas)

            processed_data = data
            if config.confidence_threshold is not None:
                processed_data = filter_by_confidence(processed_data, config.confidence_threshold)
                self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")

            if hasattr(config, 'index_to_category') and config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
                self.logger.debug("Applied category mapping")

            detections = self._extract_detections(processed_data)
            assign_person_by_area(
                detections,
                getattr(config, 'customer_areas', {}),
                getattr(config, 'staff_areas', {})
            )
            staff_detections, customer_detections = self._categorize_detections(
                detections, config.staff_categories, config.customer_categories
            )
            self.logger.debug(f"Extracted {len(staff_detections)} staff and {len(customer_detections)} customer detections")

            self._maybe_reset_chunk()
            self._update_chunk_tracking(customer_detections)

            current_time = time.time()
            analytics_results = self._process_comprehensive_analytics(
                staff_detections, customer_detections, config, current_time
            )

            # --- FIX: Ensure agg_summary is top-level and events/tracking_stats are dicts ---
            if isinstance(processed_data, dict):
                agg_summary = self._generate_per_frame_agg_summary(processed_data, analytics_results, config, context, stream_info)
            else:
                agg_summary = {"events": {}, "tracking_stats": {}}

            # --- FIX: Ensure raw_output is always a list ---
            if not isinstance(analytics_results.get("raw_output", []), list):
                analytics_results["raw_output"] = [analytics_results.get("raw_output", {})]

            insights = self._generate_insights(analytics_results, config)
            alerts = self._check_alerts(analytics_results, config)
            summary = self._generate_summary(analytics_results, alerts)
            predictions = self._extract_predictions(processed_data)

            context.mark_completed()



            # --- REPLACE outer agg_summary with inner if present ---
            # If analytics_results contains processed_data.agg_summary, use that as the output agg_summary
            inner_agg_summary = None
            if "processed_data" in analytics_results and isinstance(analytics_results["processed_data"], dict):
                pd = analytics_results["processed_data"]
                if "agg_summary" in pd and isinstance(pd["agg_summary"], dict):
                    inner_agg_summary = pd["agg_summary"]
            if inner_agg_summary:
                agg_summary = inner_agg_summary

            # Ensure tracking_stats and events are dicts keyed by frame_id
            if "tracking_stats" in agg_summary and isinstance(agg_summary["tracking_stats"], list):
                # If tracking_stats is a list with a dict containing tracking_stats, flatten
                for item in agg_summary["tracking_stats"]:
                    if isinstance(item, dict) and "tracking_stats" in item:
                        agg_summary["tracking_stats"] = item["tracking_stats"]
                        break

            if "events" in agg_summary and isinstance(agg_summary["events"], list):
                for item in agg_summary["events"]:
                    if isinstance(item, dict) and "events" in item:
                        agg_summary["events"] = item["events"]
                        break

            # Compose result data with flattened agg_summary
            result_data = dict(analytics_results)
            result_data["agg_summary"] = agg_summary


            # Ensure raw_output is always a list, including inside model_output
            if "model_output" in result_data:
                mo = result_data["model_output"]
                if isinstance(mo, dict) and "raw_output" in mo and not isinstance(mo["raw_output"], list):
                    mo["raw_output"] = [mo["raw_output"]]
            if not isinstance(result_data.get("raw_output", []), list):
                result_data["raw_output"] = [result_data.get("raw_output", {})]

            result = self.create_result(
                data=result_data,
                usecase=self.name,
                category=self.category,
                context=context
            )

            result.summary = summary
            result.insights = insights
            result.predictions = predictions
            result.metrics = analytics_results.get("business_metrics", {})

            if not config.customer_areas and not config.staff_areas:
                result.add_warning("No customer or staff areas defined - using global analysis only")

            if config.service_proximity_threshold > 250:
                result.add_warning(f"High service proximity threshold ({config.service_proximity_threshold}) may miss interactions")

            self.logger.info(f"Advanced customer service analysis completed successfully in {result.processing_time:.2f}s")
            return result

        except Exception as e:
            self.logger.error(f"Advanced customer service analysis failed: {str(e)}", exc_info=True)

            if context:
                context.mark_completed()

            return self.create_error_result(
                str(e),
                type(e).__name__,
                usecase=self.name,
                category=self.category,
                context=context
            )
    
    def _initialize_areas(self, customer_areas: Dict, staff_areas: Dict, service_areas: Dict):
        """Initialize area tracking structures."""
        self.customer_areas = customer_areas or {}
        self.staff_areas = staff_areas or {}
        self.service_areas = service_areas or {}
        
        # Initialize occupancy tracking
        self.customer_occupancy = {name: [] for name in self.customer_areas}
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
                              customer_categories: List[str]) -> Tuple[List[Dict], List[Dict]]:
        """Categorize detections into staff and customers, with persistent staff ID logic."""
        staff_detections = []
        customer_detections = []

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
            elif category in customer_categories:
                customer_detections.append(detection)
            else:
                # Default to customer if category is unknown
                customer_detections.append(detection)

        return staff_detections, customer_detections
    
    def _process_comprehensive_analytics(self, staff_detections: List[Dict], customer_detections: List[Dict],
                                       config: CustomerServiceConfig, current_time: float) -> Dict[str, Any]:
        """Process comprehensive customer service analytics."""
        # Reset current state
        self._reset_current_state()
        
        # Process staff and customer detections
        self._process_staff_detections(staff_detections, current_time)
        self._process_customer_detections(customer_detections, current_time)
        
        # Update service interactions
        self._update_service_interactions(current_time)
        
        # Compile comprehensive results
        return self._compile_analytics_results(current_time)
    
    def _reset_current_state(self):
        """Reset current state for new processing cycle."""
        # Clear current occupancy (will be repopulated)
        for area_name in self.customer_occupancy:
            self.customer_occupancy[area_name] = []
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
    
    def _process_customer_detections(self, customer_detections: List[Dict], current_time: float):
        """Process customer detections and update journey tracking."""
        for customer in customer_detections:
            customer_center = get_bbox_center(customer.get('bbox', customer.get('bounding_box', {})))
            if not customer_center:
                continue
            track_id = customer.get('track_id', f"customer_{hash(str(customer_center))}")
            # Update persistent global customer ids
            self.global_customer_ids.add(track_id)
            # Initialize customer journey if new
            is_new_journey = False
            if track_id not in self.customer_journey:
                self._initialize_customer_journey(track_id, current_time)
                is_new_journey = True
            journey = self.customer_journey[track_id]
            # Update customer area occupancy
            current_areas = []
            for area_name, polygon in self.customer_areas.items():
                if point_in_polygon(customer_center, polygon):
                    current_areas.append(area_name)
                    self.customer_occupancy[area_name].append({
                        'track_id': track_id,
                        'center': customer_center,
                        'timestamp': current_time
                    })
            # Update journey state based on current areas
            journey['current_areas'] = current_areas
            journey['last_seen'] = current_time
            journey['positions'].append({
                'center': customer_center,
                'timestamp': current_time,
                'areas': current_areas.copy()
            })
            # --- Staff service count: handle BEING_SERVED at initialization ---
            if is_new_journey and self._is_customer_being_served(track_id, current_time):
                # Customer starts in BEING_SERVED state, increment staff_service_count for the nearest staff
                nearest_staff = self._find_nearest_staff(customer_center)
                if nearest_staff:
                    staff_id, _ = nearest_staff
                    self.staff_service_count[staff_id] += 1
            # Update journey state logic
            self._update_customer_journey_state(track_id, current_areas, current_time)
    
    def _initialize_customer_journey(self, track_id: int, current_time: float):
        """Initialize customer journey tracking."""
        self.customer_journey[track_id] = {
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
    
    def _update_customer_journey_state(self, track_id: int, current_areas: List[str], current_time: float):
        """Update customer journey state based on current location."""
        journey = self.customer_journey[track_id]
        # Update areas visited
        journey['areas_visited'].update(current_areas)
        # State transition logic
        if journey['state'] == self.JOURNEY_STATES['ENTERING']:
            if current_areas:
                journey['state'] = self.JOURNEY_STATES['QUEUING']
                journey['queue_start_time'] = current_time
        elif journey['state'] == self.JOURNEY_STATES['QUEUING']:
            # Check if customer is being served (near staff)
            if self._is_customer_being_served(track_id, current_time):
                journey['state'] = self.JOURNEY_STATES['BEING_SERVED']
                journey['service_start_time'] = current_time
                if journey['queue_start_time']:
                    journey['total_wait_time'] = current_time - journey['queue_start_time']
                # --- Staff service count: increment only on QUEUING -> BEING_SERVED transition ---
                customer_center = journey['positions'][-1]['center'] if journey['positions'] else None
                if customer_center:
                    nearest_staff = self._find_nearest_staff(customer_center)
                    if nearest_staff:
                        staff_id, _ = nearest_staff
                        self.staff_service_count[staff_id] += 1
        elif journey['state'] == self.JOURNEY_STATES['BEING_SERVED']:
            # Check if service is completed
            if not self._is_customer_being_served(track_id, current_time):
                journey['state'] = self.JOURNEY_STATES['COMPLETED']
                journey['service_end_time'] = current_time
                if journey['service_start_time']:
                    journey['total_service_time'] = current_time - journey['service_start_time']
                    # --- Service time tracking: record in self.service_times ---
                    # Try to associate with staff_id if possible
                    customer_center = journey['positions'][-1]['center'] if journey['positions'] else None
                    staff_id = None
                    if customer_center:
                        nearest_staff = self._find_nearest_staff(customer_center)
                        if nearest_staff:
                            staff_id, _ = nearest_staff
                    # Store as per-customer service time (flat list)
                    self.service_times[track_id].append({
                        'customer_id': track_id,
                        'service_time': journey['total_service_time'],
                        'service_start_time': journey['service_start_time'],
                        'service_end_time': journey['service_end_time'],
                        'staff_id': staff_id
                    })
    
    def _is_customer_being_served(self, customer_track_id: int, current_time: float) -> bool:
        """Check if customer is currently being served by staff or in overlapping service/customer area or proximity."""
        customer_journey = self.customer_journey.get(customer_track_id)
        if not customer_journey or not customer_journey['positions']:
            return False

        customer_center = customer_journey['positions'][-1]['center']

        # Get all customer areas the customer is in
        customer_areas_in = set()
        for area_name, polygon in self.customer_areas.items():
            if point_in_polygon(customer_center, polygon):
                customer_areas_in.add(area_name)

        # Get all service areas the customer is in
        service_areas_in = set()
        for area_name, polygon in self.service_areas.items():
            if point_in_polygon(customer_center, polygon):
                service_areas_in.add(area_name)

        # If any area is both a customer area and a service area, consider being served
        if customer_areas_in & service_areas_in:
            return True

        # If customer is inside any service area (legacy logic)
        if service_areas_in:
            return True

        # If not inside service area, check proximity to staff
        nearest_staff = self._find_nearest_staff(customer_center)
        if nearest_staff:
            staff_id, distance = nearest_staff
            if distance <= self._service_proximity_threshold:
                return True

        return False
    
    def _find_nearest_staff(self, customer_center: Tuple[float, float]) -> Optional[Tuple[int, float]]:
        """Find nearest staff member to customer."""
        nearest_staff = None
        min_distance = float('inf')
        
        for area_name, staff_list in self.staff_occupancy.items():
            for staff_info in staff_list:
                staff_center = staff_info['center']
                distance = calculate_distance(customer_center, staff_center)
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_staff = (staff_info['track_id'], distance)
        
        return nearest_staff
    
    def _update_service_interactions(self, current_time: float):
        """Update service interactions between staff and customers."""
        for customer_id, journey in self.customer_journey.items():
            if journey['state'] == self.JOURNEY_STATES['BEING_SERVED']:
                if journey['positions']:
                    customer_center = journey['positions'][-1]['center']
                    nearest_staff = self._find_nearest_staff(customer_center)
                    if nearest_staff:
                        staff_id, distance = nearest_staff
                        # Record interaction (do not increment staff_service_count here)
                        interaction = {
                            'customer_id': customer_id,
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
        #     "customer_areas": self.customer_occupancy,
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
            "customer_areas": get_latest_per_track(self.customer_occupancy),
            "staff_areas": get_latest_per_track(self.staff_occupancy),
            "service_areas": get_latest_per_track(self.service_occupancy)
        }


        # --- Service times output: flatten to a list for JSON output (per-customer) ---
        service_times_output = []
        for customer_id, records in self.service_times.items():
            for rec in records:
                entry = rec.copy()
                service_times_output.append(entry)

        return {
            "customer_queue_analytics": self._get_customer_queue_results(),
            "staff_management_analytics": self._get_staff_management_results(),
            "service_area_analytics": self._get_service_area_results(),
            "customer_journey_analytics": self._get_customer_journey_results(),
            "business_metrics": self._calculate_analytics(current_time),
            "real_time_occupancy": real_time_occupancy,
            "service_times": service_times_output,
            "processing_timestamp": current_time
        }
    
    def _get_customer_queue_results(self) -> Dict[str, Any]:
        """Get customer queue analytics (per chunk of 10 frames)."""
        # Use chunk-based customer ids for per-chunk analytics
        active_customers = len(getattr(self, '_chunk_customer_ids', set()))
        queue_lengths_by_area = {}
        for area_name in self.customer_occupancy:
            queue_lengths_by_area[area_name] = len(getattr(self, '_chunk_area_customer_ids', defaultdict(set))[area_name])

        # For state counts, only count journeys whose track_id is in the current chunk
        customers_queuing = 0
        customers_being_served = 0
        customers_completed = 0
        wait_times_completed = []  # completed customers' wait times (list of dict)
        wait_times_ongoing = []    # current customers still in queue (list of dict)
        chunk_ids = getattr(self, '_chunk_customer_ids', set())
        now = time.time()
        for track_id in chunk_ids:
            journey = self.customer_journey.get(track_id)
            if not journey:
                continue
            if journey['state'] == self.JOURNEY_STATES['QUEUING']:
                customers_queuing += 1
                # Ongoing: time since queue_start_time
                if journey['queue_start_time']:
                    wait_times_ongoing.append({"track_id": track_id, "wait_time": now - journey['queue_start_time']})
            elif journey['state'] == self.JOURNEY_STATES['BEING_SERVED']:
                customers_being_served += 1
            elif journey['state'] == self.JOURNEY_STATES['COMPLETED']:
                customers_completed += 1
                if journey['total_wait_time'] > 0:
                    wait_times_completed.append({"track_id": track_id, "wait_time": journey['total_wait_time']})

        # Calculate average_wait_time: (sum of completed + ongoing) / total
        total_waits = [w['wait_time'] for w in wait_times_completed] + [w['wait_time'] for w in wait_times_ongoing]
        n_total = customers_completed + customers_queuing
        average_wait_time = sum(total_waits) / n_total if n_total > 0 else 0.0

        queue_analytics = {
            "active_customers": active_customers,
            "customers_queuing": customers_queuing,
            "customers_being_served": customers_being_served,
            "customers_completed": customers_completed,
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
            "active_staff": 0
        }

        # Calculate staff efficiency (do not include in output, but keep for internal use)
        total_services = sum(self.staff_service_count.values())
        # Improved logic: active_staff = all staff present in the chunk (not just those with services handled)
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

        # Internal: staff_efficiency (not shown in output)
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

        # Collect all customers and staff (flattened)
        all_customers = []
        for area_list in self.customer_occupancy.values():
            all_customers.extend(area_list)
        all_staff = []
        for area_list in self.staff_occupancy.values():
            all_staff.extend(area_list)

        for area_name, polygon in self.service_areas.items():
            customers_in_area = set()
            staff_in_area = set()

            # Customers: count if inside service area polygon OR within proximity threshold OR in overlapping area
            for occ in all_customers:
                center = occ.get('center')
                tid = occ.get('track_id')
                if center is None or tid is None:
                    continue
                # Check polygon inclusion
                in_polygon = point_in_polygon(center, polygon)
                in_proximity = any(
                    math.hypot(center[0] - pt[0], center[1] - pt[1]) <= service_proximity_threshold for pt in polygon
                )
                # Check if this area is also a customer area (overlap)
                in_overlap = False
                for cust_area_name, cust_polygon in self.customer_areas.items():
                    if area_name == cust_area_name and point_in_polygon(center, cust_polygon):
                        in_overlap = True
                        break
                if in_polygon or in_proximity or in_overlap:
                    customers_in_area.add(tid)

            # Staff: count if inside service area polygon OR within proximity threshold OR in overlapping area
            for occ in all_staff:
                center = occ.get('center')
                tid = occ.get('track_id')
                if center is None or tid is None:
                    continue
                in_polygon = point_in_polygon(center, polygon)
                in_proximity = any(
                    math.hypot(center[0] - pt[0], center[1] - pt[1]) <= service_proximity_threshold for pt in polygon
                )
                # Check if this area is also a staff area (overlap)
                in_overlap = False
                for staff_area_name, staff_polygon in self.staff_areas.items():
                    if area_name == staff_area_name and point_in_polygon(center, staff_polygon):
                        in_overlap = True
                        break
                if in_polygon or in_proximity or in_overlap:
                    staff_in_area.add(tid)

            service_analytics["service_areas_status"][area_name] = {
                "customers": len(customers_in_area),
                "customer_ids": list(customers_in_area),
                "staff": len(staff_in_area),
                "staff_ids": list(staff_in_area),
                "service_ratio": len(customers_in_area) / max(len(staff_in_area), 1),
                "status": "active" if len(staff_in_area) > 0 else "inactive",
                "service_proximity_threshold": service_proximity_threshold
            }

            if len(staff_in_area) > 0:
                service_analytics["total_active_services"] += 1

        return service_analytics
    
    def _get_customer_journey_results(self) -> Dict[str, Any]:
        """Get customer journey analytics."""
        journey_analytics = {
            "total_journeys": len(self.customer_journey),
            "journey_states": {state: 0 for state in self.JOURNEY_STATES.values()},
            "average_journey_time": 0.0,
            "popular_areas": {},
            # "journey_patterns": {}
        }
        
        journey_times = []
        all_areas_visited = []
        
        for journey in self.customer_journey.values():
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
        total_customers = len(self.customer_journey)
        chunk_ids = getattr(self, '_chunk_customer_ids', set())
        customers_queuing = 0
        customers_being_served = 0
        for track_id in chunk_ids:
            journey = self.customer_journey.get(track_id)
            if not journey:
                continue
            if journey['state'] == self.JOURNEY_STATES['QUEUING']:
                customers_queuing += 1
            elif journey['state'] == self.JOURNEY_STATES['BEING_SERVED']:
                customers_being_served += 1

        # Use global staff count (unique staff IDs)
        total_staff = len(self.global_staff_ids)

        metrics = {
            # Now using per-chunk customer count for ratio
            "customer_to_staff_ratio": (customers_queuing + customers_being_served) / max(total_staff, 1),
            "service_efficiency": 0.0,
            "queue_performance": 0.0,
            "staff_productivity": 0.0,
            "overall_performance": 0.0
        }

        # Calculate service efficiency
        completed_services = sum(1 for j in self.customer_journey.values() 
                               if j['state'] == self.JOURNEY_STATES['COMPLETED'])
        metrics["service_efficiency"] = completed_services / max(total_customers, 1)

        # Calculate queue performance
        metrics["queue_performance"] = max(0, 1 - (customers_queuing / max(total_customers, 1)))

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
    
    def _check_alerts(self, analytics_results: Dict, config: CustomerServiceConfig) -> List[Dict]:
        """Check for alert conditions in advanced customer service operations."""
        alerts = []
        
        if not config.alert_config:
            return alerts
        
        # Check queue length alerts
        queue_analytics = analytics_results.get("customer_queue_analytics", {})
        customers_queuing = queue_analytics.get("customers_queuing", 0)
        
        if customers_queuing > 10:  # Threshold for long queues
            alerts.append({
                "type": "long_queue",
                "severity": "warning",
                "message": f"Long customer queue detected ({customers_queuing} customers waiting)",
                "queue_length": customers_queuing,
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
    
    def _generate_insights(self, analytics_results: Dict, config: CustomerServiceConfig) -> List[str]:
        """Generate actionable insights from advanced customer service analysis."""
        insights = []
        
        # Queue insights
        queue_analytics = analytics_results.get("customer_queue_analytics", {})
        active_customers = queue_analytics.get("active_customers", 0)
        customers_queuing = queue_analytics.get("customers_queuing", 0)
        customers_being_served = queue_analytics.get("customers_being_served", 0)
        
        if active_customers == 0:
            insights.append("No active customers detected in service areas")
            return insights
        
        insights.append(f"Active customer analysis: {active_customers} total customers")
        
        if customers_queuing > 0:
            insights.append(f"📊 Queue status: {customers_queuing} customers waiting")
            
            avg_wait_time = queue_analytics.get("average_wait_time", 0)
            if avg_wait_time > 300:  # 5 minutes
                insights.append(f"⚠️ Long average wait time: {avg_wait_time/60:.1f} minutes")
            elif avg_wait_time > 0:
                insights.append(f"⏱️ Average wait time: {avg_wait_time/60:.1f} minutes")
        
        if customers_being_served > 0:
            insights.append(f"🔄 Active services: {customers_being_served} customers being served")
        
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
        journey_analytics = analytics_results.get("customer_journey_analytics", {})
        avg_journey_time = journey_analytics.get("average_journey_time", 0)
        
        if avg_journey_time > 0:
            insights.append(f"Customer journey: average time {avg_journey_time/60:.1f} minutes")
            
            if avg_journey_time > 1800:  # 30 minutes
                insights.append("⚠️ Long customer journey times detected")
        
        return insights
    
    def _generate_summary(self, analytics_results: Dict, alerts: List) -> str:
        """Generate human-readable summary."""
        # Beautiful, tabbed, non-technical summary for all major analytics sections
        queue_analytics = analytics_results.get("customer_queue_analytics", {})
        staff_analytics = analytics_results.get("staff_management_analytics", {})
        service_analytics = analytics_results.get("service_area_analytics", {})
        journey_analytics = analytics_results.get("customer_journey_analytics", {})
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
        summary.append(tabbed_section("customer_queue_analytics", queue_analytics, omit_keys={"wait_times_completed", "wait_times_ongoing"}))
        summary.append(tabbed_section("staff_management_analytics", staff_analytics, omit_keys={"staff_efficiency"}))
        summary.append(tabbed_section("service_area_analytics", service_analytics))
        summary.append(tabbed_section("customer_journey_analytics", journey_analytics))
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