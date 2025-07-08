"""
Customer service use case implementation.

This module provides comprehensive customer service analytics including staff utilization,
service interactions, area occupancy analysis, and business intelligence metrics.
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
    from ..utils import get_bbox_center, point_in_polygon
    for det in detections:
        if det.get('category') == 'person':
            bbox = det.get('bbox', det.get('bounding_box', None))
            if bbox and len(bbox) == 4:
                center = get_bbox_center(bbox)
                # Check staff areas first
                for polygon in staff_areas.values():
                    if point_in_polygon(center, polygon):
                        det['category'] = 'staff'
                        break
                else:
                    # Check customer areas
                    for polygon in customer_areas.values():
                        if point_in_polygon(center, polygon):
                            det['category'] = 'customer'
                            break


class CustomerServiceUseCase(BaseProcessor):
    """Customer service analytics with comprehensive business intelligence."""
    
    def __init__(self):
        """Initialize customer service use case."""
        super().__init__("customer_service")
        self.category = "sales"

        # State tracking for analytics
        self._customer_journeys: Dict[int, Dict] = {}
        self._staff_activities: Dict[int, Dict] = {}
        self._service_interactions: List[Dict] = []
        self._area_occupancy_history: Dict[str, List] = defaultdict(list)

        # --- Persistent sets for global unique counting across chunks ---
        self._global_customer_ids = set()
        self._global_staff_ids = set()
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Get configuration schema for customer service."""
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
                context: Optional[ProcessingContext] = None,
                stream_info: Optional[Any] = None) -> ProcessingResult:
        """
        Process customer service analytics.
        
        Args:
            data: Raw model output (detection or tracking format)
            config: Customer service configuration
            context: Processing context
            stream_info: Stream information containing frame details (optional, for compatibility)
            
        Returns:
            ProcessingResult: Processing result with customer service analytics
        """
        start_time = time.time()
        
        try:
            # Ensure we have the right config type
            if not isinstance(config, CustomerServiceConfig):
                return self.create_error_result(
                    "Invalid configuration type for customer service",
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
            
            self.logger.info(f"Processing customer service with format: {input_format.value}")
            
            # Step 1: Apply confidence filtering
            processed_data = data
            if config.confidence_threshold is not None:
                processed_data = filter_by_confidence(processed_data, config.confidence_threshold)
                self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
            
            # Step 2: Apply category mapping if provided
            if hasattr(config, 'index_to_category') and config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
                self.logger.debug("Applied category mapping")
            
            # Step 3: Extract detections and assign 'person' by area if needed
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
            

            # Step 4: Analyze area occupancy
            area_analysis = self._analyze_area_occupancy(
                staff_detections, customer_detections, config
            )

            # Step 5: Analyze service interactions
            service_interactions = self._analyze_service_interactions(
                staff_detections, customer_detections, config
            )

            # Step 6: Analyze customer journeys
            customer_analytics = self._analyze_customer_journeys(
                customer_detections, config
            )

            # Step 7: Analyze staff utilization
            staff_analytics = self._analyze_staff_utilization(
                staff_detections, service_interactions, config
            )

            # Step 8: Calculate business metrics
            business_metrics = self._calculate_business_metrics(
                area_analysis, service_interactions, customer_analytics, 
                staff_analytics, config
            )

            # Step 9: Generate insights and alerts
            insights = self._generate_insights(
                area_analysis, service_interactions, customer_analytics, 
                staff_analytics, business_metrics
            )
            alerts = self._check_alerts(
                area_analysis, service_interactions, business_metrics, config
            )

            # --- Unique counting logic for summary and analytics ---
            # def unique_track_ids(detections):
            #     return set([d.get('track_id') for d in detections if d.get('track_id') is not None])

            # unique_customer_ids = unique_track_ids(customer_detections)
            # unique_staff_ids = unique_track_ids(staff_detections)

            # --- New: Persistent global unique counting across chunks ---
            current_customer_ids = set([d.get('track_id') for d in customer_detections if d.get('track_id') is not None])
            current_staff_ids = set([d.get('track_id') for d in staff_detections if d.get('track_id') is not None])

            self._global_customer_ids.update(current_customer_ids)
            self._global_staff_ids.update(current_staff_ids)

            # Step 10: Generate human-readable summary
            summary = self._generate_summary(
                len(self._global_staff_ids), len(self._global_customer_ids), 
                len(service_interactions), alerts
            )

            # Step 11: Extract predictions for API compatibility
            predictions = self._extract_predictions(processed_data)

            # Mark processing as completed
            context.mark_completed()

            # Create successful result
            result = self.create_result(
                data={
                    "area_analysis": area_analysis,
                    "service_interactions": service_interactions,
                    "customer_analytics": customer_analytics,
                    "staff_analytics": staff_analytics,
                    "business_metrics": business_metrics,
                    "alerts": alerts,
                    "staff_count": len(self._global_staff_ids),
                    "customer_count": len(self._global_customer_ids),
                    "interaction_count": len(service_interactions)
                },
                usecase=self.name,
                category=self.category,
                context=context
            )

            # Add human-readable information
            result.summary = summary
            result.insights = insights
            result.predictions = predictions
            result.metrics = business_metrics

            # --- Patch: Compose human_text using current chunk counts, not cumulative ---
            human_text_parts = [
                summary,
                f"Detected {len(current_customer_ids)} customers and {len(current_staff_ids)} staff members"
            ]
            if insights:
                human_text_parts.extend(insights[1:])  # skip duplicate count line
            result.human_text = "\n".join(human_text_parts)

            # Add warnings for configuration issues
            if not config.customer_areas and not config.staff_areas:
                result.add_warning("No customer or staff areas defined - using global analysis only")

            if config.service_proximity_threshold > 200:
                result.add_warning(f"High service proximity threshold ({config.service_proximity_threshold}) may miss interactions")

            self.logger.info(f"Customer service analysis completed successfully in {result.processing_time:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Customer service analysis failed: {str(e)}", exc_info=True)
            
            if context:
                context.mark_completed()
            
            return self.create_error_result(
                str(e),
                type(e).__name__,
                usecase=self.name,
                category=self.category,
                context=context
            )
    
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
    
    def _analyze_area_occupancy(self, staff_detections: List[Dict], customer_detections: List[Dict],
                               config: CustomerServiceConfig) -> Dict[str, Any]:
        """Analyze occupancy across different areas."""
        area_analysis = {
            "customer_areas": {},
            "staff_areas": {}, 
            "service_areas": {},
            "total_people": len(staff_detections) + len(customer_detections)
        }
        
        # Analyze customer areas
        for area_name, polygon in config.customer_areas.items():
            count = self._count_people_in_area(customer_detections, polygon)
            area_analysis["customer_areas"][area_name] = {
                "count": count,
                "utilization": min(count / 10, 1.0),  # Assume max capacity of 10
                "occupancy_level": "high" if count > 7 else "medium" if count > 3 else "low"
            }
        
        # Analyze staff areas
        for area_name, polygon in config.staff_areas.items():
            count = self._count_people_in_area(staff_detections, polygon)
            area_analysis["staff_areas"][area_name] = {
                "count": count,
                "availability": count > 0,
                "staffing_level": "adequate" if count >= 2 else "minimal" if count == 1 else "unstaffed"
            }
        
        # Analyze service areas (both staff and customers)
        for area_name, polygon in config.service_areas.items():
            staff_count = self._count_people_in_area(staff_detections, polygon)
            customer_count = self._count_people_in_area(customer_detections, polygon)
            total_count = staff_count + customer_count
            
            area_analysis["service_areas"][area_name] = {
                "staff_count": staff_count,
                "customer_count": customer_count,
                "total_count": total_count,
                "service_ratio": customer_count / max(staff_count, 1),
                "service_quality": "good" if staff_count > 0 and customer_count / max(staff_count, 1) <= 3 else "needs_attention"
            }
        
        return area_analysis
    
    def _count_people_in_area(self, detections: List[Dict], polygon: List[List[float]]) -> int:
        """
        Count unique people (by track_id) in a specific area defined by polygon.
        Previous logic (per-frame count) is commented out below.
        """
        # count = 0
        # for detection in detections:
        #     center = get_bbox_center(detection.get('bbox', detection.get('bounding_box', {})))
        #     if center and point_in_polygon(center, polygon):
        #         count += 1
        # return count

        track_ids = set()
        for detection in detections:
            center = get_bbox_center(detection.get('bbox', detection.get('bounding_box', {})))
            if center and point_in_polygon(center, polygon):
                track_id = detection.get('track_id')
                if track_id is not None:
                    track_ids.add(track_id)
        return len(track_ids)
    
    def _analyze_service_interactions(self, staff_detections: List[Dict], customer_detections: List[Dict],
                                    config: CustomerServiceConfig) -> List[Dict]:
        """Analyze service interactions between staff and customers."""
        interactions = []
        
        for staff in staff_detections:
            staff_center = get_bbox_center(staff.get('bbox', staff.get('bounding_box', {})))
            if not staff_center:
                continue
            
            # Find nearby customers
            nearby_customers = []
            for customer in customer_detections:
                customer_center = get_bbox_center(customer.get('bbox', customer.get('bounding_box', {})))
                if not customer_center:
                    continue
                
                distance = calculate_distance(staff_center, customer_center)
                if distance <= config.service_proximity_threshold:
                    nearby_customers.append({
                        "detection": customer,
                        "distance": distance,
                        "center": customer_center
                    })
            
            if nearby_customers:
                # Sort by distance
                nearby_customers.sort(key=lambda x: x["distance"])
                
                # Create interaction record
                interaction = {
                    "staff_id": staff.get('track_id', f"staff_{hash(str(staff_center))}"),
                    "staff_center": staff_center,
                    "customers": nearby_customers,
                    "customer_count": len(nearby_customers),
                    "min_distance": nearby_customers[0]["distance"],
                    "avg_distance": sum(c["distance"] for c in nearby_customers) / len(nearby_customers),
                    "service_quality": self._calculate_service_quality(nearby_customers),
                    "timestamp": time.time()
                }
                
                interactions.append(interaction)
        
        return interactions
    
    def _calculate_service_quality(self, nearby_customers: List[Dict]) -> Dict[str, Any]:
        """Calculate service quality metrics based on customer proximity and count."""
        if not nearby_customers:
            return {"score": 0.0, "level": "none", "notes": "No customers nearby"}
        
        customer_count = len(nearby_customers)
        min_distance = nearby_customers[0]["distance"]
        avg_distance = sum(c["distance"] for c in nearby_customers) / customer_count
        
        # Base score calculation
        distance_score = max(0, (100 - min_distance) / 100)  # Closer is better
        load_score = max(0, (5 - customer_count) / 5)  # Fewer customers is better
        
        overall_score = (distance_score * 0.6 + load_score * 0.4)
        
        # Determine service level
        if overall_score >= 0.8:
            level = "excellent"
            notes = "Good proximity, manageable customer load"
        elif overall_score >= 0.6:
            level = "good"
            notes = "Reasonable service conditions"
        elif overall_score >= 0.4:
            level = "fair"
            notes = "Service conditions could be improved"
        else:
            level = "poor"
            notes = "High customer load or poor positioning"
        
        return {
            "score": overall_score,
            "level": level,
            "notes": notes,
            "distance_score": distance_score,
            "load_score": load_score,
            "customer_count": customer_count,
            "min_distance": min_distance,
            "avg_distance": avg_distance
        }
    
    def _analyze_customer_journeys(self, customer_detections: List[Dict],
                                  config: CustomerServiceConfig) -> Dict[str, Any]:
        """Analyze customer journey patterns and behavior."""
        # Use global unique customer IDs for total_customers and tracked_customers
        journey_analytics = {
            "total_customers": len(self._global_customer_ids),
            "tracked_customers": len(self._global_customer_ids),
            "area_transitions": [],
            "dwell_times": {},
            "journey_patterns": {}
        }
        
        # Track customers with track_ids
        tracked_customers = [c for c in customer_detections if c.get('track_id')]
        journey_analytics["tracked_customers"] = len(tracked_customers)
        
        if not tracked_customers:
            return journey_analytics
        
        # Group detections by track_id
        customer_tracks = defaultdict(list)
        for detection in tracked_customers:
            customer_tracks[detection['track_id']].append(detection)
        
        # Analyze each customer's journey
        for track_id, detections in customer_tracks.items():
            journey = self._analyze_single_customer_journey(detections, config)
            journey_analytics["journey_patterns"][track_id] = journey
        
        return journey_analytics
    
    def _analyze_single_customer_journey(self, detections: List[Dict],
                                        config: CustomerServiceConfig) -> Dict[str, Any]:
        """Analyze a single customer's journey through the space."""
        journey = {
            "total_detections": len(detections),
            "areas_visited": set(),
            "time_in_areas": defaultdict(float),
            "movement_pattern": "stationary"
        }
        
        # Sort detections by timestamp if available
        sorted_detections = sorted(detections, key=lambda x: x.get('timestamp', 0))
        
        # Track area visits
        all_areas = {**config.customer_areas, **config.service_areas}
        
        for detection in sorted_detections:
            center = get_bbox_center(detection.get('bbox', detection.get('bounding_box', {})))
            if not center:
                continue
            
            # Check which areas the customer is in
            for area_name, polygon in all_areas.items():
                if point_in_polygon(center, polygon):
                    journey["areas_visited"].add(area_name)
                    # Approximate time spent (would need temporal data for accuracy)
                    journey["time_in_areas"][area_name] += 1.0
        
        # Convert set to list for serialization
        journey["areas_visited"] = list(journey["areas_visited"])
        journey["time_in_areas"] = dict(journey["time_in_areas"])
        
        # Determine movement pattern
        if len(journey["areas_visited"]) > 2:
            journey["movement_pattern"] = "mobile"
        elif len(journey["areas_visited"]) == 2:
            journey["movement_pattern"] = "limited_movement"
        
        return journey
    
    def _analyze_staff_utilization(self, staff_detections: List[Dict], service_interactions: List[Dict],
                                  config: CustomerServiceConfig) -> Dict[str, Any]:
        """Analyze staff utilization and efficiency metrics."""
        staff_analytics = {
            # Use global unique staff IDs for total_staff
            "total_staff": len(self._global_staff_ids),
            "active_staff": 0,
            "staff_efficiency": {},
            "coverage_areas": [],
            "utilization_rate": 0.0
        }
        
        if not staff_detections:
            return staff_analytics
        
        # Track staff with interactions
        staff_with_interactions = set()
        staff_interaction_counts = defaultdict(int)
        
        for interaction in service_interactions:
            staff_id = interaction.get("staff_id")
            if staff_id:
                staff_with_interactions.add(staff_id)
                staff_interaction_counts[staff_id] += interaction.get("customer_count", 0)
        
        staff_analytics["active_staff"] = len(staff_with_interactions)
        staff_analytics["utilization_rate"] = len(staff_with_interactions) / len(staff_detections) if staff_detections else 0
        
        # Calculate staff efficiency
        for staff_id, customer_count in staff_interaction_counts.items():
            staff_analytics["staff_efficiency"][staff_id] = {
                "customers_served": customer_count,
                "efficiency_score": min(customer_count / 5.0, 1.0)  # Normalize to max 5 customers
            }
        
        # Determine coverage areas
        staff_positions = []
        for staff in staff_detections:
            center = get_bbox_center(staff.get('bbox', staff.get('bounding_box', {})))
            if center:
                staff_positions.append(center)
        
        # Check coverage of service areas
        for area_name, polygon in config.service_areas.items():
            covered = any(point_in_polygon(pos, polygon) for pos in staff_positions)
            if covered:
                staff_analytics["coverage_areas"].append(area_name)
        
        return staff_analytics
    
    def _calculate_business_metrics(self, area_analysis: Dict, service_interactions: List[Dict],
                                   customer_analytics: Dict, staff_analytics: Dict,
                                   config: CustomerServiceConfig) -> Dict[str, Any]:
        """Calculate comprehensive business intelligence metrics."""
        total_customers = customer_analytics.get("total_customers", 0)
        total_staff = staff_analytics.get("total_staff", 0)
        
        metrics = {
            "customer_to_staff_ratio": total_customers / max(total_staff, 1),
            "service_coverage": len(staff_analytics.get("coverage_areas", [])) / max(len(config.service_areas), 1),
            "interaction_rate": len(service_interactions) / max(total_customers, 1),
            "staff_utilization": staff_analytics.get("utilization_rate", 0.0),
            "area_utilization": self._calculate_area_utilization(area_analysis, config),
            "service_quality_score": 0.0,
            "attention_score": self._calculate_attention_score(service_interactions, total_customers),
            "peak_areas": self._identify_peak_areas(area_analysis),
            "optimization_opportunities": self._identify_optimization_opportunities(area_analysis, staff_analytics),
            "overall_performance": 0.0
        }
        
        # Calculate service quality score
        if service_interactions:
            quality_scores = [
                interaction.get("service_quality", {}).get("score", 0.0)
                for interaction in service_interactions
            ]
            metrics["service_quality_score"] = sum(quality_scores) / len(quality_scores)
        
        # Calculate overall performance score
        metrics["overall_performance"] = self._calculate_overall_performance_score(metrics)
        
        return metrics
    
    def _calculate_area_utilization(self, area_analysis: Dict, config: CustomerServiceConfig) -> Dict[str, float]:
        """Calculate utilization rates for different area types."""
        utilization = {}
        
        # Customer area utilization
        customer_areas = area_analysis.get("customer_areas", {})
        if customer_areas:
            avg_utilization = sum(area.get("utilization", 0) for area in customer_areas.values()) / len(customer_areas)
            utilization["customer_areas"] = avg_utilization
        
        # Service area utilization
        service_areas = area_analysis.get("service_areas", {})
        if service_areas:
            total_people = sum(area.get("total_count", 0) for area in service_areas.values())
            max_capacity = len(service_areas) * 10  # Assume 10 people per service area
            utilization["service_areas"] = min(total_people / max_capacity, 1.0) if max_capacity > 0 else 0.0
        
        return utilization
    
    def _calculate_attention_score(self, service_interactions: List[Dict], total_customers: int) -> float:
        """Calculate how well customers are being attended to."""
        if not total_customers:
            return 1.0
        
        customers_with_attention = sum(interaction.get("customer_count", 0) for interaction in service_interactions)
        return min(customers_with_attention / total_customers, 1.0)
    
    def _identify_peak_areas(self, area_analysis: Dict) -> List[str]:
        """Identify areas with highest occupancy."""
        peak_areas = []
        
        # Check customer areas
        customer_areas = area_analysis.get("customer_areas", {})
        for area_name, area_data in customer_areas.items():
            if area_data.get("occupancy_level") == "high":
                peak_areas.append(f"customer_area:{area_name}")
        
        # Check service areas
        service_areas = area_analysis.get("service_areas", {})
        for area_name, area_data in service_areas.items():
            if area_data.get("total_count", 0) > 5:
                peak_areas.append(f"service_area:{area_name}")
        
        return peak_areas
    
    def _identify_optimization_opportunities(self, area_analysis: Dict, staff_analytics: Dict) -> List[str]:
        """Identify opportunities for service optimization."""
        opportunities = []
        
        # Check for understaffed areas
        service_areas = area_analysis.get("service_areas", {})
        for area_name, area_data in service_areas.items():
            if area_data.get("service_quality") == "needs_attention":
                opportunities.append(f"Increase staffing in service area: {area_name}")
        
        # Check for low staff utilization
        if staff_analytics.get("utilization_rate", 0) < 0.5:
            opportunities.append("Staff utilization is low - consider reassignment")
        
        # Check for high customer-to-staff ratios
        customer_areas = area_analysis.get("customer_areas", {})
        high_occupancy_areas = [
            area_name for area_name, area_data in customer_areas.items()
            if area_data.get("occupancy_level") == "high"
        ]
        
        if high_occupancy_areas:
            opportunities.append(f"High customer density in: {', '.join(high_occupancy_areas)}")
        
        # Check coverage gaps
        uncovered_areas = []
        coverage_areas = staff_analytics.get("coverage_areas", [])
        for area_name in service_areas.keys():
            if area_name not in coverage_areas:
                uncovered_areas.append(area_name)
        
        if uncovered_areas:
            opportunities.append(f"Service areas need coverage: {', '.join(uncovered_areas)}")
        
        return opportunities
    
    def _calculate_overall_performance_score(self, metrics: Dict) -> float:
        """Calculate an overall performance score."""
        # Weight different metrics
        weights = {
            "service_quality_score": 0.3,
            "attention_score": 0.25,
            "staff_utilization": 0.2,
            "service_coverage": 0.15,
            "interaction_rate": 0.1
        }
        
        score = 0.0
        total_weight = 0.0
        
        for metric, weight in weights.items():
            if metric in metrics:
                score += metrics[metric] * weight
                total_weight += weight
        
        return score / total_weight if total_weight > 0 else 0.0
    
    def _check_alerts(self, area_analysis: Dict, service_interactions: List[Dict],
                     business_metrics: Dict, config: CustomerServiceConfig) -> List[Dict]:
        """Check for alert conditions in customer service operations."""
        alerts = []
        
        if not config.alert_config:
            return alerts
        
        # Check customer-to-staff ratio
        ratio = business_metrics.get("customer_to_staff_ratio", 0)
        if ratio > 5:
            alerts.append({
                "type": "high_customer_ratio",
                "severity": "warning",
                "message": f"High customer-to-staff ratio ({ratio:.1f}:1)",
                "ratio": ratio,
                "recommendation": "Consider additional staff deployment"
            })
        
        # Check service coverage
        coverage = business_metrics.get("service_coverage", 0)
        if coverage < 0.7:
            alerts.append({
                "type": "low_service_coverage",
                "severity": "warning", 
                "message": f"Low service area coverage ({coverage:.1%})",
                "coverage": coverage,
                "recommendation": "Deploy staff to uncovered service areas"
            })
        
        # Check for areas needing attention
        service_areas = area_analysis.get("service_areas", {})
        for area_name, area_data in service_areas.items():
            if area_data.get("service_quality") == "needs_attention":
                alerts.append({
                    "type": "service_quality",
                    "severity": "warning",
                    "message": f"Service area '{area_name}' needs attention",
                    "area": area_name,
                    "customer_count": area_data.get("customer_count", 0),
                    "staff_count": area_data.get("staff_count", 0),
                    "recommendation": "Increase staff presence in this area"
                })
        
        # Check overall performance
        performance = business_metrics.get("overall_performance", 0)
        if performance < 0.6:
            alerts.append({
                "type": "low_performance",
                "severity": "critical" if performance < 0.4 else "warning",
                "message": f"Overall service performance is low ({performance:.1%})",
                "performance": performance,
                "recommendation": "Review staffing levels and service processes"
            })
        
        return alerts
    
    def _generate_insights(self, area_analysis: Dict, service_interactions: List[Dict],
                          customer_analytics: Dict, staff_analytics: Dict,
                          business_metrics: Dict) -> List[str]:
        """Generate actionable insights from customer service analysis."""
        insights = []
        
        # Basic counts
        total_staff = staff_analytics.get("total_staff", 0)
        total_customers = customer_analytics.get("total_customers", 0)
        active_staff = staff_analytics.get("active_staff", 0)
        
        if total_customers == 0:
            insights.append("No customers detected in service areas")
            return insights
        
        insights.append(f"Detected {total_customers} customers and {total_staff} staff members")
        
        # Staff utilization insights
        if total_staff > 0:
            utilization = staff_analytics.get("utilization_rate", 0)
            if utilization >= 0.8:
                insights.append(f"✅ High staff utilization ({utilization:.1%}) - staff are actively engaged")
            elif utilization >= 0.5:
                insights.append(f"📊 Moderate staff utilization ({utilization:.1%})")
            else:
                insights.append(f"⚠️ Low staff utilization ({utilization:.1%}) - consider staff redeployment")
        
        # Service interaction insights
        interaction_count = len(service_interactions)
        if interaction_count > 0:
            interaction_rate = business_metrics.get("interaction_rate", 0)
            insights.append(f"Service interactions: {interaction_count} active engagements")
            
            if interaction_rate >= 0.8:
                insights.append("✅ High customer engagement rate")
            elif interaction_rate >= 0.5:
                insights.append("📊 Moderate customer engagement")
            else:
                insights.append("⚠️ Low customer engagement - some customers may not be receiving attention")
        
        # Area occupancy insights
        service_areas = area_analysis.get("service_areas", {})
        busy_areas = [name for name, data in service_areas.items() if data.get("total_count", 0) > 3]
        if busy_areas:
            insights.append(f"High activity in service areas: {', '.join(busy_areas)}")
        
        # Service quality insights
        quality_score = business_metrics.get("service_quality_score", 0)
        if quality_score >= 0.8:
            insights.append("✅ Excellent service quality detected")
        elif quality_score >= 0.6:
            insights.append("📊 Good service quality overall")
        else:
            insights.append("⚠️ Service quality could be improved")
        
        # Coverage insights
        coverage = business_metrics.get("service_coverage", 0)
        if coverage < 0.7:
            uncovered_count = max(0, len(service_areas) - len(staff_analytics.get("coverage_areas", [])))
            if uncovered_count > 0:
                insights.append(f"🚨 {uncovered_count} service area(s) lack staff presence")
        
        # Performance insights
        performance = business_metrics.get("overall_performance", 0)
        if performance >= 0.8:
            insights.append("🌟 Outstanding overall service performance")
        elif performance >= 0.6:
            insights.append("✅ Good overall service performance")
        else:
            insights.append("📈 Service performance has room for improvement")
        
        # Optimization opportunities
        opportunities = business_metrics.get("optimization_opportunities", [])
        if opportunities:
            insights.append(f"💡 Optimization opportunities identified: {len(opportunities)} areas for improvement")
        
        return insights
    
    def _generate_summary(self, staff_count: int, customer_count: int,
                         interaction_count: int, alerts: List) -> str:
        """Generate human-readable summary."""
        if customer_count == 0 and staff_count == 0:
            return "No people detected in service areas"
        
        summary_parts = []
        
        if customer_count > 0:
            summary_parts.append(f"{customer_count} customers")
        
        if staff_count > 0:
            summary_parts.append(f"{staff_count} staff")
        
        if interaction_count > 0:
            summary_parts.append(f"{interaction_count} active service interactions")
        
        summary = "Customer service analysis: " + ", ".join(summary_parts)
        
        if alerts:
            alert_count = len(alerts)
            critical_alerts = sum(1 for alert in alerts if alert.get("severity") == "critical")
            if critical_alerts > 0:
                summary += f" with {critical_alerts} critical alert(s)"
            else:
                summary += f" with {alert_count} alert(s)"
        
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