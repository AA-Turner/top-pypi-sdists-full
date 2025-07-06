"""
Base classes and interfaces for the post-processing system.

This module provides the core abstractions that all post-processing components should follow.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Type, Protocol, runtime_checkable
from enum import Enum
import time
import logging

logger = logging.getLogger(__name__)


class ResultFormat(Enum):
    """Supported result formats."""
    DETECTION = "detection"
    TRACKING = "tracking"
    OBJECT_TRACKING = "object_tracking"
    CLASSIFICATION = "classification"
    INSTANCE_SEGMENTATION = "instance_segmentation"
    ACTIVITY_RECOGNITION = "activity_recognition"
    UNKNOWN = "unknown"


class ProcessingStatus(Enum):
    """Processing status indicators."""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    PARTIAL = "partial"


@dataclass
class ProcessingContext:
    """Context information for processing operations."""
    
    # Input information
    input_format: ResultFormat = ResultFormat.UNKNOWN
    input_size: Optional[int] = None
    timestamp: float = field(default_factory=time.time)
    
    # Processing configuration
    confidence_threshold: Optional[float] = None
    enable_tracking: bool = False
    enable_counting: bool = False
    enable_analytics: bool = False
    
    # Performance tracking
    processing_start: float = field(default_factory=time.time)
    processing_time: Optional[float] = None
    
    # Additional context
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def mark_completed(self) -> None:
        """Mark processing as completed and calculate processing time."""
        self.processing_time = time.time() - self.processing_start


@dataclass
class ProcessingResult:
    """Standardized result container for all post-processing operations."""
    
    # Core data
    data: Any
    status: ProcessingStatus = ProcessingStatus.SUCCESS
    
    # Metadata
    usecase: str = ""
    category: str = ""
    processing_time: float = 0.0
    timestamp: float = field(default_factory=time.time)
    
    # Human-readable information
    summary: str = ""
    insights: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    # Error information
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    error_details: Dict[str, Any] = field(default_factory=dict)
    
    # Additional context
    context: Optional[ProcessingContext] = None
    predictions: List[Dict[str, Any]] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    def is_success(self) -> bool:
        """Check if processing was successful."""
        return self.status == ProcessingStatus.SUCCESS
    
    def add_insight(self, message: str) -> None:
        """Add insight message."""
        self.insights.append(message)
    
    def add_warning(self, message: str) -> None:
        """Add warning message."""
        self.warnings.append(message)
        if self.status == ProcessingStatus.SUCCESS:
            self.status = ProcessingStatus.WARNING
    
    def set_error(self, message: str, error_type: str = "ProcessingError", 
                  details: Optional[Dict[str, Any]] = None) -> None:
        """Set error information."""
        self.error_message = message
        self.error_type = error_type
        self.error_details = details or {}
        self.status = ProcessingStatus.ERROR
        self.summary = f"Processing failed: {message}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "data": self.data,
            "status": self.status.value,
            "usecase": self.usecase,
            "category": self.category,
            "processing_time": self.processing_time,
            "timestamp": self.timestamp,
            "summary": self.summary,
            "insights": self.insights,
            "warnings": self.warnings,
            "error_message": self.error_message,
            "error_type": self.error_type,
            "error_details": self.error_details,
            "predictions": self.predictions,
            "metrics": self.metrics,
            "context": self.context.__dict__ if self.context else None
        }


@runtime_checkable
class ConfigProtocol(Protocol):
    """Protocol for configuration objects."""
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        ...
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        ...


@runtime_checkable
class ProcessorProtocol(Protocol):
    """Protocol for processors."""
    
    def process(self, data: Any, config: ConfigProtocol, context: Optional[ProcessingContext] = None) -> ProcessingResult:
        """Process data with given configuration."""
        ...


class BaseProcessor(ABC):
    """Base class for all processors."""
    
    def __init__(self, name: str):
        """Initialize processor with name."""
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")
    
    @abstractmethod
    def process(self, data: Any, config: ConfigProtocol, context: Optional[ProcessingContext] = None) -> ProcessingResult:
        """Process data with given configuration."""
        pass
    
    def create_result(self, data: Any, usecase: str = "", category: str = "", 
                     context: Optional[ProcessingContext] = None) -> ProcessingResult:
        """Create a successful result."""
        result = ProcessingResult(
            data=data,
            usecase=usecase,
            category=category,
            context=context
        )
        
        if context:
            result.processing_time = context.processing_time or 0.0
        
        return result
    
    def create_error_result(self, message: str, error_type: str = "ProcessingError",
                           usecase: str = "", category: str = "",
                           context: Optional[ProcessingContext] = None) -> ProcessingResult:
        """Create an error result."""
        result = ProcessingResult(
            data={},
            usecase=usecase,
            category=category,
            context=context
        )
        result.set_error(message, error_type)
        
        if context:
            result.processing_time = context.processing_time or 0.0
        
        return result
    
    def create_structured_event(self, event_type: str, level: str, intensity: float, 
                               application_name: str, location_info: str = None, 
                               additional_info: str = "", application_version: str = "1.0") -> Dict:
        """Create a structured event in the required format."""
        from datetime import datetime, timezone
        
        return {
            "type": event_type,
            "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
            "level": level,
            "intensity": round(intensity, 1),
            "config": {
                "min_value": 0,
                "max_value": 10,
                "level_settings": {"info": 2, "warning": 5, "critical": 7}
            },
            "application_name": application_name,
            "application_version": application_version,
            "location_info": location_info,
            "human_text": f"Event: {event_type.replace('_', ' ').title()}\nLevel: {level.title()}\nTime: {datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC')}\n{additional_info}"
        }
    
    def create_structured_tracking_stats(self, results_data: Dict, human_text: str) -> Dict:
        """Create structured tracking stats in the required format."""
        from datetime import datetime, timezone
        
        return {
            "tracking_start_time": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "all_results_for_tracking": results_data,
            "human_text": human_text
        }
    
    def determine_event_level_and_intensity(self, count: int, threshold: int = 10) -> tuple:
        """Determine event level and intensity based on count and threshold."""
        if threshold > 0:
            intensity = min(10.0, (count / threshold) * 10)
        else:
            intensity = min(10.0, count / 2.0)
        
        if intensity >= 7:
            level = "critical"
        elif intensity >= 5:
            level = "warning"
        else:
            level = "info"
            
        return level, intensity


class BaseUseCase(ABC):
    """Base class for all use cases."""
    
    def __init__(self, name: str, category: str):
        """Initialize use case with name and category."""
        self.name = name
        self.category = category
        self.logger = logging.getLogger(f"{__name__}.{name}")
    
    @abstractmethod
    def get_config_schema(self) -> Dict[str, Any]:
        """Get JSON schema for configuration validation."""
        pass
    
    @abstractmethod
    def create_default_config(self, **overrides) -> ConfigProtocol:
        """Create default configuration with optional overrides."""
        pass
    
    def validate_config(self, config: ConfigProtocol) -> List[str]:
        """Validate configuration for this use case."""
        return config.validate()
    

class ProcessorRegistry:
    """Registry for processors and use cases."""
    
    def __init__(self):
        """Initialize registry."""
        self._processors: Dict[str, Type[BaseProcessor]] = {}
        self._use_cases: Dict[str, Dict[str, Type[BaseUseCase]]] = {}
    
    def register_processor(self, name: str, processor_class: Type[BaseProcessor]) -> None:
        """Register a processor class."""
        self._processors[name] = processor_class
        logger.debug(f"Registered processor: {name}")
    
    def register_use_case(self, category: str, name: str, use_case_class: Type[BaseUseCase]) -> None:
        """Register a use case class."""
        if category not in self._use_cases:
            self._use_cases[category] = {}
        self._use_cases[category][name] = use_case_class
        logger.debug(f"Registered use case: {category}/{name}")
    
    def get_processor(self, name: str) -> Optional[Type[BaseProcessor]]:
        """Get processor class by name."""
        return self._processors.get(name)
    
    def get_use_case(self, category: str, name: str) -> Optional[Type[BaseUseCase]]:
        """Get use case class by category and name."""
        return self._use_cases.get(category, {}).get(name)
    
    def list_processors(self) -> List[str]:
        """List all registered processors."""
        return list(self._processors.keys())
    
    def list_use_cases(self) -> Dict[str, List[str]]:
        """List all registered use cases by category."""
        return {category: list(use_cases.keys()) for category, use_cases in self._use_cases.items()}


# Global registry instance
registry = ProcessorRegistry() 