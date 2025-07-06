"""
Basic counting with tracking use case implementation.

This module provides a simplified counting use case that combines basic object counting
with essential tracking and alerting features. It's designed for scenarios where you need
simple counting with track continuity and basic alert notifications.
"""

from typing import Any, Dict, List, Optional
import time

from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol
from ..core.config import BaseConfig, TrackingConfig, AlertConfig
from ..utils import (
    filter_by_confidence,
    apply_category_mapping,
    count_objects_by_category,
    count_objects_in_zones,
    count_unique_tracks,
    calculate_counting_summary,
    match_results_structure
)


class BasicCountingTrackingConfig(BaseConfig):
    """Configuration for basic counting with tracking."""
    
    def __init__(
        self,
        category: str = "general",
        usecase: str = "basic_counting_tracking",
        confidence_threshold: float = 0.5,
        target_categories: List[str] = None,
        zones: Optional[Dict[str, List[List[float]]]] = None,
        enable_tracking: bool = True,
        tracking_method: str = "kalman",
        max_age: int = 30,
        min_hits: int = 3,
        count_thresholds: Optional[Dict[str, int]] = None,
        zone_thresholds: Optional[Dict[str, int]] = None,
        alert_cooldown: float = 60.0,
        enable_unique_counting: bool = True,
        index_to_category: Optional[Dict[int, str]] = None,
        **kwargs
    ):
        """
        Initialize basic counting tracking configuration.
        
        Args:
            category: Use case category
            usecase: Use case name
            confidence_threshold: Minimum confidence for detections
            target_categories: List of categories to count
            zones: Zone definitions for spatial analysis
            enable_tracking: Whether to enable tracking
            tracking_method: Tracking algorithm to use
            max_age: Maximum age for tracks in frames
            min_hits: Minimum hits before confirming track
            count_thresholds: Count thresholds for alerts
            zone_thresholds: Zone occupancy thresholds for alerts
            alert_cooldown: Alert cooldown time in seconds
            enable_unique_counting: Enable unique object counting
            index_to_category: Optional mapping from class indices to category names
            **kwargs: Additional parameters
        """
        super().__init__(
            category=category,
            usecase=usecase,
            confidence_threshold=confidence_threshold,
            enable_tracking=enable_tracking,
            enable_analytics=True,
            **kwargs
        )
        
        # Target categories
        self.target_categories = target_categories or ["person", "people", "object"]
        
        # Zone configuration
        self.zones = zones or {}
        
        # Category mapping
        self.index_to_category = index_to_category
        
        # Tracking configuration
        self.tracking_config = None
        if enable_tracking:
            self.tracking_config = TrackingConfig(
                tracking_method=tracking_method,
                max_age=max_age,
                min_hits=min_hits,
                iou_threshold=0.3,
                target_classes=self.target_categories
            )
        
        # Alert configuration
        self.alert_config = None
        if count_thresholds or zone_thresholds:
            self.alert_config = AlertConfig(
                count_thresholds=count_thresholds or {},
                occupancy_thresholds=zone_thresholds or {},
                alert_cooldown=alert_cooldown
            )
        
        # Counting settings
        self.enable_unique_counting = enable_unique_counting
    
    def validate(self) -> List[str]:
        """Validate configuration."""
        errors = super().validate()
        
        if not self.target_categories:
            errors.append("target_categories cannot be empty")
        
        # Validate zones
        for zone_name, polygon in self.zones.items():
            if len(polygon) < 3:
                errors.append(f"Zone '{zone_name}' must have at least 3 points")
            
            for i, point in enumerate(polygon):
                if len(point) != 2:
                    errors.append(f"Zone '{zone_name}' point {i} must have exactly 2 coordinates")
        
        # Validate nested configurations
        if self.tracking_config:
            errors.extend(self.tracking_config.validate())
        
        if self.alert_config:
            errors.extend(self.alert_config.validate())
        
        return errors


class BasicCountingTrackingUseCase(BaseProcessor):
    """Basic counting with tracking use case."""
    
    def __init__(self):
        """Initialize basic counting tracking use case."""
        super().__init__("basic_counting_tracking")
        self.category = "general"
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Get configuration schema for basic counting tracking."""
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
                "target_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["person", "people", "object"],
                    "description": "Categories to count and track"
                },
                "zones": {
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
                    "description": "Zone definitions as polygons"
                },
                "enable_tracking": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable tracking for unique counting"
                },
                "tracking_method": {
                    "type": "string",
                    "enum": ["kalman", "sort", "deepsort", "bytetrack"],
                    "default": "kalman",
                    "description": "Tracking algorithm to use"
                },
                "max_age": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 30,
                    "description": "Maximum age for tracks in frames"
                },
                "min_hits": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 3,
                    "description": "Minimum hits before confirming track"
                },
                "count_thresholds": {
                    "type": "object",
                    "additionalProperties": {"type": "integer", "minimum": 1},
                    "description": "Count thresholds for alerts"
                },
                "zone_thresholds": {
                    "type": "object",
                    "additionalProperties": {"type": "integer", "minimum": 1},
                    "description": "Zone occupancy thresholds for alerts"
                },
                "alert_cooldown": {
                    "type": "number",
                    "minimum": 0.0,
                    "default": 60.0,
                    "description": "Alert cooldown time in seconds"
                },
                "enable_unique_counting": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable unique object counting using tracking"
                }
            },
            "required": ["confidence_threshold"],
            "additionalProperties": False
        }
    
    def create_default_config(self, **overrides) -> BasicCountingTrackingConfig:
        """Create default configuration with optional overrides."""
        defaults = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.5,
            "enable_tracking": True,
            "enable_unique_counting": True,
            "tracking_method": "kalman",
            "max_age": 30,
            "min_hits": 3,
            "alert_cooldown": 60.0
        }
        defaults.update(overrides)
        return BasicCountingTrackingConfig(**defaults)
    
    def validate_config(self, config: ConfigProtocol) -> bool:
        """Validate configuration for this use case."""
        if not isinstance(config, BasicCountingTrackingConfig):
            return False
        
        errors = config.validate()
        if errors:
            self.logger.warning(f"Configuration validation errors: {errors}")
            return False
        
        return True
    
    def process(self, data: Any, config: ConfigProtocol, 
                context: Optional[ProcessingContext] = None) -> ProcessingResult:
        """
        Process basic counting with tracking.
        
        Args:
            data: Raw model output (detection or tracking format)
            config: Basic counting tracking configuration
            context: Processing context
            
        Returns:
            ProcessingResult: Processing result with counting and tracking analytics
        """
        start_time = time.time()
        
        try:
            # Ensure we have the right config type
            if not isinstance(config, BasicCountingTrackingConfig):
                return self.create_error_result(
                    "Invalid configuration type for basic counting tracking",
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
            
            self.logger.info(f"Processing basic counting tracking with format: {input_format.value}")
            
            # Step 1: Apply confidence filtering
            processed_data = data
            if config.confidence_threshold is not None:
                processed_data = filter_by_confidence(processed_data, config.confidence_threshold)
                self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")
            
            # Step 2: Apply category mapping if provided
            if config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
                self.logger.debug("Applied category mapping")
            
            # Step 3: Calculate basic counting summary
            counting_summary = calculate_counting_summary(
                processed_data,
                zones=config.zones
            )
            
            # Step 4: Zone-based analysis if zones are configured
            zone_analysis = {}
            if config.zones:
                zone_analysis = count_objects_in_zones(processed_data, config.zones)
                self.logger.debug(f"Analyzed {len(config.zones)} zones")
            
            # Step 5: Unique tracking analysis if enabled
            tracking_analysis = {}
            if config.enable_tracking and config.enable_unique_counting:
                tracking_analysis = self._analyze_tracking(processed_data, config)
                self.logger.debug("Performed tracking analysis")
            
            # Step 6: Generate insights and alerts
            insights = self._generate_insights(counting_summary, zone_analysis, tracking_analysis, config)
            alerts = self._check_alerts(counting_summary, zone_analysis, config)
            
            # Step 7: Calculate metrics
            metrics = self._calculate_metrics(counting_summary, zone_analysis, tracking_analysis, config, context)
            
            # Step 8: Extract predictions
            predictions = self._extract_predictions(processed_data)
            
            # Step 9: Generate summary
            summary = self._generate_summary(counting_summary, zone_analysis, tracking_analysis, alerts)
            
            # Mark processing as completed
            context.mark_completed()
            
            # Create successful result
            result = self.create_result(
                data={
                    "counting_summary": counting_summary,
                    "zone_analysis": zone_analysis,
                    "tracking_analysis": tracking_analysis,
                    "alerts": alerts,
                    "total_objects": counting_summary.get("total_objects", 0),
                    "zones_count": len(config.zones) if config.zones else 0,
                    "tracking_enabled": config.enable_tracking
                },
                usecase=self.name,
                category=self.category,
                context=context
            )
            
            # Add human-readable information
            result.summary = summary
            result.insights = insights
            result.predictions = predictions
            result.metrics = metrics
            
            # Add warnings
            if config.confidence_threshold and config.confidence_threshold < 0.3:
                result.add_warning(f"Low confidence threshold ({config.confidence_threshold}) may result in false positives")
            
            if config.enable_tracking and not any(item.get("track_id") for item in self._flatten_data(processed_data)):
                result.add_warning("Tracking enabled but no track IDs found in input data")
            
            self.logger.info(f"Basic counting tracking completed successfully in {result.processing_time:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Basic counting tracking failed: {str(e)}", exc_info=True)
            
            if context:
                context.mark_completed()
            
            return self.create_error_result(
                str(e), 
                type(e).__name__,
                usecase=self.name,
                category=self.category,
                context=context
            )
    
    def _analyze_tracking(self, data: Any, config: BasicCountingTrackingConfig) -> Dict[str, Any]:
        """Analyze tracking data for unique counting."""
        tracking_analysis = {
            "unique_tracks": 0,
            "active_tracks": 0,
            "track_categories": {},
            "track_zones": {}
        }
        
        try:
            if isinstance(data, dict):
                # Frame-based tracking data
                unique_tracks = count_unique_tracks(data)
                tracking_analysis["unique_tracks"] = sum(unique_tracks.values())
                tracking_analysis["track_categories"] = unique_tracks
                
                # Count active tracks in current frame
                latest_frame = max(data.keys()) if data else None
                if latest_frame and isinstance(data[latest_frame], list):
                    active_track_ids = set()
                    for item in data[latest_frame]:
                        track_id = item.get("track_id")
                        if track_id is not None:
                            active_track_ids.add(track_id)
                    tracking_analysis["active_tracks"] = len(active_track_ids)
            
            elif isinstance(data, list):
                # Detection format with track IDs
                unique_track_ids = set()
                track_categories = {}
                
                for item in data:
                    track_id = item.get("track_id")
                    category = item.get("category", "unknown")
                    
                    if track_id is not None:
                        unique_track_ids.add(track_id)
                        if category not in track_categories:
                            track_categories[category] = set()
                        track_categories[category].add(track_id)
                
                tracking_analysis["unique_tracks"] = len(unique_track_ids)
                tracking_analysis["active_tracks"] = len(unique_track_ids)
                tracking_analysis["track_categories"] = {
                    cat: len(tracks) for cat, tracks in track_categories.items()
                }
            
            # Zone-based tracking analysis
            if config.zones:
                zone_tracks = {}
                for zone_name in config.zones:
                    zone_tracks[zone_name] = 0
                
                # This would require more complex zone intersection logic
                # For now, we'll keep it simple
                tracking_analysis["track_zones"] = zone_tracks
        
        except Exception as e:
            self.logger.warning(f"Tracking analysis failed: {str(e)}")
        
        return tracking_analysis
    
    def _generate_insights(self, counting_summary: Dict, zone_analysis: Dict, 
                          tracking_analysis: Dict, config: BasicCountingTrackingConfig) -> List[str]:
        """Generate human-readable insights."""
        insights = []
        
        total_objects = counting_summary.get("total_objects", 0)
        
        if total_objects == 0:
            insights.append("No objects detected in the scene")
            return insights
        
        # Basic counting insights
        insights.append(f"Detected {total_objects} objects in total")
        
        # Category breakdown
        category_counts = counting_summary.get("by_category", {})
        for category, count in category_counts.items():
            if count > 0 and category in config.target_categories:
                percentage = (count / total_objects) * 100
                insights.append(f"Category '{category}': {count} objects ({percentage:.1f}% of total)")
        
        # Zone insights
        if zone_analysis:
            zones_with_objects = sum(1 for zone_counts in zone_analysis.values() 
                                   if (sum(zone_counts.values()) if isinstance(zone_counts, dict) else zone_counts) > 0)
            insights.append(f"Objects detected in {zones_with_objects}/{len(zone_analysis)} zones")
            
            for zone_name, zone_counts in zone_analysis.items():
                zone_total = sum(zone_counts.values()) if isinstance(zone_counts, dict) else zone_counts
                if zone_total > 0:
                    percentage = (zone_total / total_objects) * 100
                    insights.append(f"Zone '{zone_name}': {zone_total} objects ({percentage:.1f}% of total)")
        
        # Tracking insights
        if config.enable_tracking and tracking_analysis:
            unique_tracks = tracking_analysis.get("unique_tracks", 0)
            active_tracks = tracking_analysis.get("active_tracks", 0)
            
            if unique_tracks > 0:
                insights.append(f"Tracking: {unique_tracks} unique objects, {active_tracks} currently active")
                
                if unique_tracks != total_objects:
                    efficiency = (unique_tracks / total_objects) * 100 if total_objects > 0 else 0
                    insights.append(f"Tracking efficiency: {efficiency:.1f}% ({unique_tracks}/{total_objects} tracked)")
                
                # Track category breakdown
                track_categories = tracking_analysis.get("track_categories", {})
                for category, count in track_categories.items():
                    if count > 0:
                        insights.append(f"Tracked '{category}': {count} unique objects")
        
        return insights
    
    def _check_alerts(self, counting_summary: Dict, zone_analysis: Dict, 
                     config: BasicCountingTrackingConfig) -> List[Dict]:
        """Check for alert conditions."""
        alerts = []
        
        if not config.alert_config:
            return alerts
        
        total_objects = counting_summary.get("total_objects", 0)
        
        # Count threshold alerts
        for category, threshold in config.alert_config.count_thresholds.items():
            if category == "all" and total_objects >= threshold:
                alerts.append({
                    "type": "count_threshold",
                    "severity": "warning",
                    "message": f"Total object count ({total_objects}) exceeds threshold ({threshold})",
                    "category": category,
                    "current_count": total_objects,
                    "threshold": threshold,
                    "timestamp": time.time()
                })
            elif category in counting_summary.get("by_category", {}):
                count = counting_summary["by_category"][category]
                if count >= threshold:
                    alerts.append({
                        "type": "count_threshold",
                        "severity": "warning",
                        "message": f"{category} count ({count}) exceeds threshold ({threshold})",
                        "category": category,
                        "current_count": count,
                        "threshold": threshold,
                        "timestamp": time.time()
                    })
        
        # Zone occupancy alerts
        for zone_name, threshold in config.alert_config.occupancy_thresholds.items():
            if zone_name in zone_analysis:
                zone_count = sum(zone_analysis[zone_name].values()) if isinstance(zone_analysis[zone_name], dict) else zone_analysis[zone_name]
                if zone_count >= threshold:
                    alerts.append({
                        "type": "zone_occupancy",
                        "severity": "warning",
                        "message": f"Zone '{zone_name}' occupancy ({zone_count}) exceeds threshold ({threshold})",
                        "zone": zone_name,
                        "current_occupancy": zone_count,
                        "threshold": threshold,
                        "timestamp": time.time()
                    })
        
        return alerts
    
    def _calculate_metrics(self, counting_summary: Dict, zone_analysis: Dict, 
                          tracking_analysis: Dict, config: BasicCountingTrackingConfig, 
                          context: ProcessingContext) -> Dict[str, Any]:
        """Calculate detailed metrics."""
        total_objects = counting_summary.get("total_objects", 0)
        
        metrics = {
            "total_objects": total_objects,
            "processing_time": context.processing_time or 0.0,
            "input_format": context.input_format.value,
            "confidence_threshold": config.confidence_threshold,
            "zones_analyzed": len(zone_analysis),
            "tracking_enabled": config.enable_tracking,
            "unique_counting_enabled": config.enable_unique_counting
        }
        
        # Zone metrics
        if zone_analysis:
            zone_metrics = {}
            for zone_name, zone_counts in zone_analysis.items():
                zone_total = sum(zone_counts.values()) if isinstance(zone_counts, dict) else zone_counts
                zone_metrics[zone_name] = {
                    "count": zone_total,
                    "percentage": (zone_total / total_objects) * 100 if total_objects > 0 else 0
                }
            metrics["zone_metrics"] = zone_metrics
        
        # Tracking metrics
        if config.enable_tracking and tracking_analysis:
            unique_tracks = tracking_analysis.get("unique_tracks", 0)
            active_tracks = tracking_analysis.get("active_tracks", 0)
            
            metrics.update({
                "unique_tracks": unique_tracks,
                "active_tracks": active_tracks,
                "tracking_efficiency": (unique_tracks / total_objects) * 100 if total_objects > 0 else 0,
                "track_categories": tracking_analysis.get("track_categories", {})
            })
        
        # Category metrics
        category_counts = counting_summary.get("by_category", {})
        category_metrics = {}
        for category, count in category_counts.items():
            if category in config.target_categories:
                category_metrics[category] = {
                    "count": count,
                    "percentage": (count / total_objects) * 100 if total_objects > 0 else 0
                }
        metrics["category_metrics"] = category_metrics
        
        return metrics
    
    def _extract_predictions(self, data: Any) -> List[Dict[str, Any]]:
        """Extract predictions from processed data."""
        predictions = []
        
        try:
            flattened_data = self._flatten_data(data)
            for item in flattened_data:
                prediction = self._normalize_prediction(item)
                if prediction:
                    predictions.append(prediction)
        except Exception as e:
            self.logger.warning(f"Failed to extract predictions: {str(e)}")
        
        return predictions
    
    def _flatten_data(self, data: Any) -> List[Dict[str, Any]]:
        """Flatten data structure to list of items."""
        items = []
        
        if isinstance(data, list):
            items.extend(data)
        elif isinstance(data, dict):
            for frame_id, frame_data in data.items():
                if isinstance(frame_data, list):
                    for item in frame_data:
                        if isinstance(item, dict):
                            item["frame_id"] = frame_id
                            items.append(item)
        
        return items
    
    def _normalize_prediction(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize a single prediction item."""
        if not isinstance(item, dict):
            return {}
        
        return {
            "category": item.get("category", item.get("class", "unknown")),
            "confidence": item.get("confidence", item.get("score", 0.0)),
            "bounding_box": item.get("bounding_box", item.get("bbox", {})),
            "track_id": item.get("track_id"),
            "frame_id": item.get("frame_id")
        }
    
    def _generate_summary(self, counting_summary: Dict, zone_analysis: Dict, 
                         tracking_analysis: Dict, alerts: List) -> str:
        """Generate human-readable summary."""
        total_objects = counting_summary.get("total_objects", 0)
        
        if total_objects == 0:
            return "No objects detected"
        
        summary_parts = [f"{total_objects} objects detected"]
        
        # Add tracking info
        if tracking_analysis:
            unique_tracks = tracking_analysis.get("unique_tracks", 0)
            if unique_tracks > 0:
                summary_parts.append(f"{unique_tracks} unique tracks")
        
        # Add zone info
        if zone_analysis:
            zones_with_objects = sum(1 for zone_counts in zone_analysis.values() 
                                   if (sum(zone_counts.values()) if isinstance(zone_counts, dict) else zone_counts) > 0)
            summary_parts.append(f"in {zones_with_objects}/{len(zone_analysis)} zones")
        
        # Add alert info
        if alerts:
            alert_count = len(alerts)
            summary_parts.append(f"with {alert_count} alert{'s' if alert_count != 1 else ''}")
        
        return ", ".join(summary_parts) 