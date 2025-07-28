"""
Template Use Case for creating new standardized use cases.

This template shows how to create a new use case that follows the standardized
agg_summary structure. Copy this file and modify it for your specific use case.

Example use case: Fire Detection
"""

from typing import Any, Dict, List, Optional, Union
from dataclasses import asdict
import time

from ..core.base import BaseProcessor, ProcessingContext, ProcessingResult, ConfigProtocol, ResultFormat
from ..core.config import BaseConfig
from ..utils import (
    filter_by_confidence,
    filter_by_categories,
    apply_category_mapping,
    count_objects_by_category,
    calculate_counting_summary,
    match_results_structure
)


class TemplateUseCaseConfig(BaseConfig):
    """Configuration for Template Use Case."""
    
    def __init__(self, 
                 usecase: str = "template_usecase",
                 category: str = "general",
                 confidence_threshold: float = 0.5,
                 target_categories: List[str] = None,
                 enable_analytics: bool = True,
                 alert_threshold: int = 5,
                 **kwargs):
        super().__init__(usecase=usecase, category=category, **kwargs)
        self.confidence_threshold = confidence_threshold
        self.target_categories = target_categories or ["fire", "smoke"]  # Example categories
        self.enable_analytics = enable_analytics
        self.alert_threshold = alert_threshold
    
    def validate(self) -> List[str]:
        """Validate configuration."""
        errors = super().validate()
        
        if not 0.0 <= self.confidence_threshold <= 1.0:
            errors.append("confidence_threshold must be between 0.0 and 1.0")
        
        if self.alert_threshold < 1:
            errors.append("alert_threshold must be positive")
            
        return errors


class TemplateUseCase(BaseProcessor):
    """Template use case showing how to implement standardized agg_summary structure."""
    
    def __init__(self):
        """Initialize template use case."""
        super().__init__("template_usecase")
        self.category = "general"
        
        # Add any state tracking variables here
        self._detection_count = 0
        self._total_detections = 0
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Get configuration schema for template use case."""
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
                    "default": ["fire", "smoke"],
                    "description": "Target categories to detect"
                },
                "enable_analytics": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable analytics generation"
                },
                "alert_threshold": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 5,
                    "description": "Threshold for generating alerts"
                }
            },
            "required": ["confidence_threshold"],
            "additionalProperties": False
        }
    
    def create_default_config(self, **overrides) -> TemplateUseCaseConfig:
        """Create default configuration with optional overrides."""
        defaults = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.5,
            "target_categories": ["fire", "smoke"],
            "enable_analytics": True,
            "alert_threshold": 5,
        }
        defaults.update(overrides)
        return TemplateUseCaseConfig(**defaults)
    
    def process(self, data: Any, config: ConfigProtocol, 
                context: Optional[ProcessingContext] = None, 
                stream_info: Optional[Any] = None) -> ProcessingResult:
        """
        Process data using template use case - automatically detects single or multi-frame structure.
        
        Args:
            data: Raw model output (detection or tracking format)
            config: Template use case configuration
            context: Processing context
            stream_info: Stream information (optional)
            
        Returns:
            ProcessingResult: Processing result with standardized agg_summary structure
        """
        try:
            # Ensure we have the right config type
            if not isinstance(config, TemplateUseCaseConfig):
                return self.create_error_result(
                    "Invalid configuration type for template use case",
                    usecase=self.name,
                    category=self.category,
                    context=context
                )
            
            # Initialize processing context if not provided
            if context is None:
                context = ProcessingContext()
            
            # Detect frame structure automatically
            is_multi_frame = self.detect_frame_structure(data)
            
            self.logger.info(f"Processing template use case - Multi-frame: {is_multi_frame}")
            
            # Process based on frame structure
            if is_multi_frame:
                agg_summary = self._process_multi_frame(data, config, stream_info)
            else:
                agg_summary = self._process_single_frame(data, config, stream_info)
            
            # Mark processing as completed
            context.mark_completed()
            
            # Create result with standardized agg_summary
            return self.create_result(
                data={"agg_summary": agg_summary},
                usecase=self.name,
                category=self.category,
                context=context
            )
                
        except Exception as e:
            self.logger.error(f"Template use case failed: {str(e)}", exc_info=True)
            
            if context:
                context.mark_completed()
            
            return self.create_error_result(
                str(e), 
                type(e).__name__,
                usecase=self.name,
                category=self.category,
                context=context
            )
    
    def _process_multi_frame(self, data: Dict, config: TemplateUseCaseConfig, 
                           stream_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process multi-frame data to generate frame-wise agg_summary."""
        
        frame_incidents = {}
        frame_tracking_stats = {}
        frame_business_analytics = {}
        frame_human_text = {}
        
        # Process each frame individually
        for frame_key, frame_detections in data.items():
            frame_id = str(frame_key)
            
            # Process this single frame's detections
            incidents, tracking_stats, business_analytics, summary = self._process_frame_detections(
                frame_detections, config, frame_id, stream_info
            )
            
            # Store frame-wise results
            if incidents:
                frame_incidents[frame_id] = incidents
            if tracking_stats:
                frame_tracking_stats[frame_id] = tracking_stats
            if business_analytics:
                frame_business_analytics[frame_id] = business_analytics
            if summary:
                frame_human_text[frame_id] = summary
        
        # Create frame-wise agg_summary
        return self.create_frame_wise_agg_summary(
            frame_incidents, frame_tracking_stats, frame_business_analytics,
            frame_human_text=frame_human_text
        )
    
    def _process_single_frame(self, data: Any, config: TemplateUseCaseConfig, 
                            stream_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process single frame data and return standardized agg_summary."""
        
        # Process frame data
        incidents, tracking_stats, business_analytics, summary = self._process_frame_detections(
            data, config, "current_frame", stream_info
        )
        
        # Create single-frame agg_summary
        return self.create_agg_summary(
            "current_frame", incidents, tracking_stats, business_analytics, human_text=summary
        )
    
    def _process_frame_detections(self, frame_data: Any, config: TemplateUseCaseConfig, 
                                frame_id: str, stream_info: Optional[Dict[str, Any]] = None) -> tuple:
        """Process detections from a single frame and return standardized components."""
        
        # Convert frame_data to list if it's not already
        if isinstance(frame_data, list):
            detections = frame_data
        else:
            # Handle other formats as needed
            detections = []
        
        # Step 1: Apply confidence filtering
        if config.confidence_threshold is not None:
            detections = [d for d in detections if d.get("confidence", 0) >= config.confidence_threshold]
        
        # Step 2: Apply category mapping if provided
        if config.index_to_category:
            detections = apply_category_mapping(detections, config.index_to_category)
        
        # Step 3: Filter to target categories
        if config.target_categories:
            detections = [d for d in detections if d.get("category") in config.target_categories]
        
        # Step 4: Update internal state
        current_count = len(detections)
        self._detection_count = current_count
        self._total_detections += current_count
        
        # Step 5: Generate standardized components
        incidents = self._generate_incidents(detections, config, frame_id, stream_info)
        tracking_stats = self._generate_tracking_stats(detections, config, stream_info)
        business_analytics = self._generate_business_analytics(detections, config, stream_info) if config.enable_analytics else []
        summary = self._generate_summary(detections, config)
        
        return incidents, tracking_stats, business_analytics, summary
    
    def _generate_incidents(self, detections: List[Dict], config: TemplateUseCaseConfig, 
                          frame_id: str, stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """Generate standardized incidents."""
        incidents = []
        
        if len(detections) > 0:
            # Determine severity level based on detection count
            severity_level = self.determine_severity_level(
                len(detections), threshold_low=1, threshold_medium=3, threshold_critical=config.alert_threshold
            )
            
            # Get camera info
            camera_info = self.get_camera_info_from_stream(stream_info)
            
            # Create incident
            incident_id = f"template_detection_{frame_id}_{int(time.time())}"
            incident_text = f"Template detection event with {len(detections)} detections [Severity: {severity_level}]"
            
            incident = self.create_incident(
                incident_id, "template_detection", severity_level, 
                incident_text, camera_info
            )
            incidents.append(incident)
        
        return incidents
    
    def _generate_tracking_stats(self, detections: List[Dict], config: TemplateUseCaseConfig,
                               stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """Generate standardized tracking stats."""
        
        # Get camera info
        camera_info = self.get_camera_info_from_stream(stream_info)
        
        # Build total_counts and current_counts
        total_counts = []
        current_counts = []
        
        for category in config.target_categories:
            category_current = sum(1 for d in detections if d.get("category") == category)
            category_total = self._total_detections  # This would be category-specific in real implementation
            
            if category_current > 0:
                current_counts.append(self.create_count_object(category, category_current))
            if category_total > 0:
                total_counts.append(self.create_count_object(category, category_total))
        
        # Prepare detections for tracking stats (without confidence and track_id)
        tracking_detections = []
        for detection in detections:
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "unknown")
            
            detection_obj = self.create_detection_object(category, bbox)
            tracking_detections.append(detection_obj)
        
        # Generate human text
        current_timestamp = self.get_high_precision_timestamp()
        human_text = self.generate_tracking_human_text(
            {cat: sum(1 for d in detections if d.get("category") == cat) for cat in config.target_categories},
            {cat: self._total_detections for cat in config.target_categories},  # Simplified
            current_timestamp, current_timestamp
        )
        
        # Create tracking stats
        tracking_stat = self.create_tracking_stats(
            total_counts, current_counts, tracking_detections, human_text, camera_info
        )
        
        return [tracking_stat]
    
    def _generate_business_analytics(self, detections: List[Dict], config: TemplateUseCaseConfig,
                                   stream_info: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """Generate standardized business analytics."""
        
        # Get camera info
        camera_info = self.get_camera_info_from_stream(stream_info)
        
        # Calculate analytics statistics
        analytics_stats = {
            "detection_count": len(detections),
            "total_detections": self._total_detections,
            "detection_rate": len(detections) / max(1, self._total_detections) * 100
        }
        
        # Add category breakdown
        for category in config.target_categories:
            category_count = sum(1 for d in detections if d.get("category") == category)
            analytics_stats[f"{category}_count"] = category_count
        
        # Generate human text
        current_timestamp = self.get_high_precision_timestamp()
        analytics_human_text = self.generate_analytics_human_text(
            "template_analytics", analytics_stats, current_timestamp, current_timestamp
        )
        
        # Create business analytics
        analytics = self.create_business_analytics(
            "template_analytics", analytics_stats, analytics_human_text, camera_info
        )
        
        return [analytics]
    
    def _generate_summary(self, detections: List[Dict], config: TemplateUseCaseConfig) -> str:
        """Generate human-readable summary."""
        if len(detections) == 0:
            return "No detections found"
        
        category_counts = {}
        for detection in detections:
            category = detection.get("category", "unknown")
            category_counts[category] = category_counts.get(category, 0) + 1
        
        summary_parts = []
        for category, count in category_counts.items():
            summary_parts.append(f"{count} {category} detection{'s' if count != 1 else ''}")
        
        return f"Template Use Case: {', '.join(summary_parts)} detected" 