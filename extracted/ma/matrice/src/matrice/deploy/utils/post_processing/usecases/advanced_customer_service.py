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


class AdvancedCustomerServiceUseCase(BaseProcessor):
    """Advanced customer service analytics with comprehensive business intelligence and journey tracking."""
    
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
            "staff_categories": ["staff", "employee"],
            "customer_categories": ["customer", "person"],
            "service_proximity_threshold": 100.0,
            "max_service_time": 1800.0,
            "buffer_time": 2.0,
        }
        defaults.update(overrides)
        return CustomerServiceConfig(**defaults)
    
    def process(self, data: Any, config: ConfigProtocol,
                context: Optional[ProcessingContext] = None) -> ProcessingResult:
        """
        Process advanced customer service analytics.
        
        Args:
            data: Raw model output (detection or tracking format)
            config: Advanced customer service configuration
            context: Processing context
            
        Returns:
            ProcessingResult: Processing result with comprehensive customer service analytics
        """
        start_time = time.time()
        
        try:
            # Ensure we have the right config type
            if not isinstance(config, CustomerServiceConfig):
                return self.create_error_result(
                    "Invalid configuration type for advanced customer service",
                    usecase=self.name,
                    category=self.category,
                    context=context
                )
            
            # Initialize processing context if not provided
            if context is None:
                context = ProcessingContext()
            
            # Detect input format
            input_format = match_results_structure(data)
            context.input_format = input_format
            context.confidence_threshold = config.confidence_threshold
            context.enable_tracking = config.enable_tracking
            
            self.logger.info(f"Processing advanced customer service with format: {input_format.value}")
            
            # Initialize area tracking
            self._initialize_areas(config.customer_areas, config.staff_areas, config.service_areas)
            
            # Step 1: Apply confidence filtering
            processed_data = data
            if config.confidence_threshold is not None:
                processed_data = filter_by_confidence(processed_data, config.confidence_threshold)
                self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
            
            # Step 2: Apply category mapping if provided
            if hasattr(config, 'index_to_category') and config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
                self.logger.debug("Applied category mapping")
            
            # Step 3: Extract and categorize detections
            detections = self._extract_detections(processed_data)
            staff_detections, customer_detections = self._categorize_detections(
                detections, config.staff_categories, config.customer_categories
            )
            
            self.logger.debug(f"Extracted {len(staff_detections)} staff and {len(customer_detections)} customer detections")
            
            # Step 4: Process comprehensive analytics
            current_time = time.time()
            analytics_results = self._process_comprehensive_analytics(
                staff_detections, customer_detections, config, current_time
            )
            
            # Step 5: Generate insights and alerts
            insights = self._generate_insights(analytics_results, config)
            alerts = self._check_alerts(analytics_results, config)
            
            # Step 6: Generate human-readable summary
            summary = self._generate_summary(analytics_results, alerts)
            
            # Step 7: Extract predictions for API compatibility
            predictions = self._extract_predictions(processed_data)
            
            # Mark processing as completed
            context.mark_completed()
            
            # Create successful result
            result = self.create_result(
                data=analytics_results,
                usecase=self.name,
                category=self.category,
                context=context
            )
            
            # Add human-readable information
            result.summary = summary
            result.insights = insights
            result.predictions = predictions
            result.metrics = analytics_results.get("business_metrics", {})
            
            # Add warnings for configuration issues
            if not config.customer_areas and not config.staff_areas:
                result.add_warning("No customer or staff areas defined - using global analysis only")
            
            if config.service_proximity_threshold > 200:
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
        """Categorize detections into staff and customers."""
        staff_detections = []
        customer_detections = []
        
        for detection in detections:
            category = detection.get('category', detection.get('class', ''))
            
            if category in staff_categories:
                staff_detections.append(detection)
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
            
            # Update staff area occupancy
            for area_name, polygon in self.staff_areas.items():
                if point_in_polygon(staff_center, polygon):
                    self.staff_occupancy[area_name].append({
                        'track_id': track_id,
                        'center': staff_center,
                        'timestamp': current_time
                    })
    
    def _process_customer_detections(self, customer_detections: List[Dict], current_time: float):
        """Process customer detections and update journey tracking."""
        for customer in customer_detections:
            customer_center = get_bbox_center(customer.get('bbox', customer.get('bounding_box', {})))
            if not customer_center:
                continue
            
            track_id = customer.get('track_id', f"customer_{hash(str(customer_center))}")
            
            # Initialize customer journey if new
            if track_id not in self.customer_journey:
                self._initialize_customer_journey(track_id, current_time)
            
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
        
        elif journey['state'] == self.JOURNEY_STATES['BEING_SERVED']:
            # Check if service is completed
            if not self._is_customer_being_served(track_id, current_time):
                journey['state'] = self.JOURNEY_STATES['COMPLETED']
                journey['service_end_time'] = current_time
                if journey['service_start_time']:
                    journey['total_service_time'] = current_time - journey['service_start_time']
    
    def _is_customer_being_served(self, customer_track_id: int, current_time: float) -> bool:
        """Check if customer is currently being served by staff."""
        customer_journey = self.customer_journey.get(customer_track_id)
        if not customer_journey or not customer_journey['positions']:
            return False
        
        customer_center = customer_journey['positions'][-1]['center']
        
        # Find nearest staff
        nearest_staff = self._find_nearest_staff(customer_center)
        if nearest_staff:
            staff_id, distance = nearest_staff
            return distance <= self.service_proximity_threshold
        
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
                        
                        # Record interaction
                        interaction = {
                            'customer_id': customer_id,
                            'staff_id': staff_id,
                            'distance': distance,
                            'timestamp': current_time
                        }
                        
                        journey['staff_interactions'].append(interaction)
                        self.staff_service_count[staff_id] += 1
    
    def _compile_analytics_results(self, current_time: float) -> Dict[str, Any]:
        """Compile comprehensive analytics results."""
        return {
            "customer_queue_analytics": self._get_customer_queue_results(),
            "staff_management_analytics": self._get_staff_management_results(),
            "service_area_analytics": self._get_service_area_results(),
            "customer_journey_analytics": self._get_customer_journey_results(),
            "business_metrics": self._calculate_analytics(current_time),
            "real_time_occupancy": {
                "customer_areas": self.customer_occupancy,
                "staff_areas": self.staff_occupancy,
                "service_areas": self.service_occupancy
            },
            "processing_timestamp": current_time
        }
    
    def _get_customer_queue_results(self) -> Dict[str, Any]:
        """Get customer queue analytics."""
        queue_analytics = {
            "active_customers": len(self.customer_journey),
            "customers_queuing": 0,
            "customers_being_served": 0,
            "customers_completed": 0,
            "average_wait_time": 0.0,
            "queue_lengths_by_area": {}
        }
        
        wait_times = []
        for journey in self.customer_journey.values():
            if journey['state'] == self.JOURNEY_STATES['QUEUING']:
                queue_analytics["customers_queuing"] += 1
            elif journey['state'] == self.JOURNEY_STATES['BEING_SERVED']:
                queue_analytics["customers_being_served"] += 1
            elif journey['state'] == self.JOURNEY_STATES['COMPLETED']:
                queue_analytics["customers_completed"] += 1
                if journey['total_wait_time'] > 0:
                    wait_times.append(journey['total_wait_time'])
        
        if wait_times:
            queue_analytics["average_wait_time"] = sum(wait_times) / len(wait_times)
        
        # Calculate queue lengths by area
        for area_name, occupants in self.customer_occupancy.items():
            queue_analytics["queue_lengths_by_area"][area_name] = len(occupants)
        
        return queue_analytics
    
    def _get_staff_management_results(self) -> Dict[str, Any]:
        """Get staff management analytics."""
        staff_analytics = {
            "total_staff": sum(len(staff_list) for staff_list in self.staff_occupancy.values()),
            "staff_distribution": {},
            "staff_efficiency": {},
            "staff_utilization": 0.0
        }
        
        # Calculate staff distribution
        for area_name, staff_list in self.staff_occupancy.items():
            staff_analytics["staff_distribution"][area_name] = len(staff_list)
        
        # Calculate staff efficiency
        total_services = sum(self.staff_service_count.values())
        active_staff = len(self.staff_service_count)
        
        for staff_id, service_count in self.staff_service_count.items():
            staff_analytics["staff_efficiency"][staff_id] = {
                "services_handled": service_count,
                "efficiency_score": service_count / max(total_services, 1)
            }
        
        # Calculate overall utilization
        total_staff_count = staff_analytics["total_staff"]
        if total_staff_count > 0:
            staff_analytics["staff_utilization"] = active_staff / total_staff_count
        
        return staff_analytics
    
    def _get_service_area_results(self) -> Dict[str, Any]:
        """Get service area analytics."""
        service_analytics = {
            "service_areas_status": {},
            "total_active_services": 0,
            "service_efficiency": {}
        }
        
        for area_name, polygon in self.service_areas.items():
            # Count customers and staff in service area
            customers_in_area = len(self.customer_occupancy.get(area_name, []))
            staff_in_area = len(self.staff_occupancy.get(area_name, []))
            
            service_analytics["service_areas_status"][area_name] = {
                "customers": customers_in_area,
                "staff": staff_in_area,
                "service_ratio": customers_in_area / max(staff_in_area, 1),
                "status": "active" if staff_in_area > 0 else "inactive"
            }
            
            if staff_in_area > 0:
                service_analytics["total_active_services"] += 1
        
        return service_analytics
    
    def _get_customer_journey_results(self) -> Dict[str, Any]:
        """Get customer journey analytics."""
        journey_analytics = {
            "total_journeys": len(self.customer_journey),
            "journey_states": {state: 0 for state in self.JOURNEY_STATES.values()},
            "average_journey_time": 0.0,
            "popular_areas": {},
            "journey_patterns": {}
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
        total_staff = sum(len(staff_list) for staff_list in self.staff_occupancy.values())
        
        metrics = {
            "customer_to_staff_ratio": total_customers / max(total_staff, 1),
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
        customers_queuing = sum(1 for j in self.customer_journey.values() 
                              if j['state'] == self.JOURNEY_STATES['QUEUING'])
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
        queue_analytics = analytics_results.get("customer_queue_analytics", {})
        staff_analytics = analytics_results.get("staff_management_analytics", {})
        
        active_customers = queue_analytics.get("active_customers", 0)
        total_staff = staff_analytics.get("total_staff", 0)
        
        if active_customers == 0 and total_staff == 0:
            return "No activity detected in service areas"
        
        summary_parts = []
        
        if active_customers > 0:
            summary_parts.append(f"{active_customers} active customers")
            
            customers_queuing = queue_analytics.get("customers_queuing", 0)
            customers_being_served = queue_analytics.get("customers_being_served", 0)
            
            if customers_queuing > 0:
                summary_parts.append(f"{customers_queuing} queuing")
            
            if customers_being_served > 0:
                summary_parts.append(f"{customers_being_served} being served")
        
        if total_staff > 0:
            summary_parts.append(f"{total_staff} staff deployed")
        
        summary = "Advanced customer service: " + ", ".join(summary_parts)
        
        if alerts:
            critical_alerts = sum(1 for alert in alerts if alert.get("severity") == "critical")
            if critical_alerts > 0:
                summary += f" with {critical_alerts} critical alert(s)"
            else:
                summary += f" with {len(alerts)} alert(s)"
        
        return summary
    
    def _extract_predictions(self, data: Any) -> List[Dict[str, Any]]:
        """Extract predictions from processed data for API compatibility."""
        predictions = []
        
        try:
            if isinstance(data, list):
                # Detection format
                for item in data:
                    if isinstance(item, dict):
                        prediction = {
                            "category": item.get("category", item.get("class", "unknown")),
                            "confidence": item.get("confidence", item.get("score", 0.0)),
                            "bounding_box": item.get("bounding_box", item.get("bbox", {})),
                            "track_id": item.get("track_id")
                        }
                        predictions.append(prediction)
            
            elif isinstance(data, dict):
                # Frame-based or tracking format
                for frame_id, items in data.items():
                    if isinstance(items, list):
                        for item in items:
                            if isinstance(item, dict):
                                prediction = {
                                    "frame_id": frame_id,
                                    "category": item.get("category", item.get("class", "unknown")),
                                    "confidence": item.get("confidence", item.get("score", 0.0)),
                                    "bounding_box": item.get("bounding_box", item.get("bbox", {})),
                                    "track_id": item.get("track_id")
                                }
                                predictions.append(prediction)
        
        except Exception as e:
            self.logger.warning(f"Failed to extract predictions: {str(e)}")
        
        return predictions 