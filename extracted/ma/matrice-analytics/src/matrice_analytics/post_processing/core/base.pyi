"""Auto-generated stub for module: base."""
from typing import Any, Dict, List, Optional, Set, Union

# Constants
logger: Any
registry: Any

# Classes
class BaseProcessor:
    # Base class for all processors with standardized agg_summary generation.

    def __init__(self: Any, name: str) -> None:
        """
        Initialize processor with name.
        """
        ...

    def create_agg_summary(self: Any, frame_id: Union[str, int], incidents: Optional[List[Dict]] = None, tracking_stats: Optional[List[Dict]] = None, business_analytics: Optional[List[Dict]] = None, alerts: Optional[List[Dict]] = None, human_text: str = '') -> Dict[str, Any]:
        """
        Create standardized agg_summary structure following the expected format.
        """
        ...

    def create_agg_summary_for_frame(self: Any, frame_number: Union[int, str], incidents: List[Dict] = None, tracking_stats: List[Dict] = None, business_analytics: List[Dict] = None, alerts: List[Dict] = None, human_text: str = '') -> Dict[str, Any]:
        """
        Create agg_summary structure for a specific frame matching the expected format.
        """
        ...

    def create_alert_object(self: Any, alert_type: str, alert_id: str, incident_category: str, threshold_value: float, ascending: bool = True, settings: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create a standardized alert object.
        """
        ...

    def create_business_analytics(self: Any, analysis_name: str, statistics: Dict[str, Any], human_text: str, camera_info: Optional[Dict[str, Any]] = None, alerts: Optional[List[Dict]] = None, alert_settings: Optional[List[Dict]] = None, reset_settings: Optional[List[Dict]] = None, start_time: Optional[str] = None, reset_time: Optional[str] = None) -> Dict[str, Any]:
        """
        Create standardized business analytics object following the agg_summary format.
        """
        ...

    def create_count_object(self: Any, category: str, count: int) -> Dict[str, Any]:
        """
        Create a standardized count object for total_counts and current_counts.
        """
        ...

    def create_detection_object(self: Any, category: str, bounding_box: Dict[str, Any], _confidence: Optional[float] = None, segmentation: Optional[List] = None, track_id: Optional[Any] = None, plate_text: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a standardized detection object for tracking stats.
        """
        ...

    def create_error_result(self: Any, message: str, error_type: str = 'ProcessingError', usecase: str = '', category: str = '', context: Optional[Any] = None) -> Any:
        """
        Create an error result.
        """
        ...

    def create_frame_wise_agg_summary(self: Any, frame_incidents: Dict[str, List[Dict]], frame_tracking_stats: Dict[str, List[Dict]], frame_business_analytics: Dict[str, List[Dict]], frame_alerts: Dict[str, List[Dict]] = None, frame_human_text: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Create frame-wise agg_summary structure for multiple frames.
        """
        ...

    def create_incident(self: Any, incident_id: str, incident_type: str, severity_level: str, human_text: str = '', camera_info: Optional[Dict[str, Any]] = None, alerts: Optional[List[Dict]] = None, alert_settings: Optional[List[Dict]] = None, start_time: Optional[str] = None, end_time: Optional[str] = None, level_settings: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """
        Create a standardized incident object following the agg_summary format.
        """
        ...

    def create_result(self: Any, data: Any, usecase: str = '', category: str = '', context: Optional[Any] = None) -> Any:
        """
        Create a successful result.
        """
        ...

    def create_structured_business_analytics(self: Any, analysis_name: str, statistics: Dict, camera_info: Dict = None, alerts: List[Dict] = None, alert_settings: List[Dict] = None) -> Dict:
        """
        Create structured business analytics in the required format.
        """
        ...

    def create_structured_event(self: Any, event_type: str, level: str, intensity: float, application_name: str, location_info: str = None, additional_info: str = '', application_version: str = '1.0') -> Dict:
        """
        Create a structured event in the required format.
        """
        ...

    def create_structured_incident(self: Any, incident_id: str, incident_type: str, severity_level: str, start_time: str = None, end_time: str = None, camera_info: Dict = None, alerts: List[Dict] = None, alert_settings: List[Dict] = None) -> Dict:
        """
        Create a structured incident in the required format.
        """
        ...

    def create_structured_tracking_stats(self: Any, _results_data: Dict, human_text: str) -> Dict:
        """
        Create structured tracking stats in the required format.
        """
        ...

    def create_tracking_stats(self: Any, total_counts: List[Dict[str, Any]], current_counts: List[Dict[str, Any]], detections: List[Dict[str, Any]], human_text: str, camera_info: Optional[Dict[str, Any]] = None, alerts: Optional[List[Dict]] = None, alert_settings: Optional[List[Dict]] = None, reset_settings: Optional[List[Dict]] = None, start_time: Optional[str] = None, reset_time: Optional[str] = None) -> Dict[str, Any]:
        """
        Create standardized tracking stats object following the agg_summary format.
        """
        ...

    def detect_frame_structure(self: Any, data: Any) -> bool:
        """
        Detect if data has frame-based structure (multi-frame) or single frame.
        """
        ...

    def determine_event_level_and_intensity(self: Any, count: int, threshold: int = 10) -> tuple:
        """
        Determine event level and intensity based on count and threshold.
        """
        ...

    def determine_severity_level(self: Any, count: int, threshold_low: int = 3, threshold_medium: int = 7, threshold_critical: int = 15) -> str:
        """
        Determine severity level based on count and thresholds.
        """
        ...

    def extract_deployment_ids(self: Any, stream_info: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Extract app_deployment_id and application_id from stream_info.
        
                Uses a priority-based fallback chain identical to the one in
                incident_manager_utils / business_metrics_manager_utils:
        
                    stream_info root  >  input_settings  >  camera_info
        
                Each level checks snake_case and camelCase key variants.
                Returns a dict with ``app_deployment_id`` and ``application_id``
                (empty strings when not found).
        """
        ...

    def extract_frame_ids(self: Any, data: Any) -> List[str]:
        """
        Extract frame IDs from frame-based data structure.
        """
        ...

    def generate_analytics_human_text(self: Any, _analysis_name: str, statistics: Dict[str, Any], current_timestamp: str, reset_timestamp: str, alerts_summary: str = 'None') -> str:
        """
        Generate standardized human text for business analytics.
        """
        ...

    def generate_tracking_human_text(self: Any, current_counts: Dict[str, int], total_counts: Dict[str, int], current_timestamp: str, reset_timestamp: str, alerts_summary: str = 'None') -> str:
        """
        Generate standardized human text for tracking stats.
        """
        ...

    def get_camera_info_from_stream(self: Any, stream_info: Optional[Dict[str, Any]] = None, camera_info: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Extract camera info from stream_info or use provided camera_info.
        
                The returned dict always includes ``app_deployment_id`` and
                ``application_id`` extracted from *stream_info* using a
                priority-based fallback chain (root -> input_settings -> camera_info).
        """
        ...

    def get_default_camera_info(self: Any) -> Dict[str, str]:
        """
        Get default camera info structure.
        """
        ...

    def get_default_level_settings(self: Any) -> Dict[str, int]:
        """
        Get default severity level settings.
        """
        ...

    def get_default_reset_settings(self: Any) -> List[Dict[str, Any]]:
        """
        Get default reset settings.
        """
        ...

    def get_high_precision_timestamp(self: Any) -> str:
        """
        Get high precision timestamp with microsecond granularity.
        """
        ...

    def get_standard_timestamp(self: Any) -> str:
        """
        Get standard timestamp without microseconds.
        """
        ...

    def process(self: Any, _data: Any, _config: Any, _context: Optional[Any] = None) -> Any:
        """
        Process data with given configuration.
        """
        ...

class BaseUseCase:
    # Base class for all use cases.

    def __init__(self: Any, name: str, category: str) -> None:
        """
        Initialize use case with name and category.
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get JSON schema for configuration validation.
        """
        ...

    def validate_config(self: Any, config: Any) -> List[str]:
        """
        Validate configuration for this use case.
        """
        ...

class ConfigProtocol:
    # Protocol for configuration objects.

    def to_dict(self: Any) -> Dict[str, Any]:
        """
        Convert to dictionary.
        """
        ...

    def validate(self: Any) -> List[str]:
        """
        Validate configuration and return list of errors.
        """
        ...

class ProcessingContext:
    # Context information for processing operations.

    def mark_completed(self: Any) -> None:
        """
        Mark processing as completed and calculate processing time, latency in ms, and fps.
        """
        ...

class ProcessingResult:
    # Standardized result container for all post-processing operations.

    def add_insight(self: Any, message: str) -> None:
        """
        Add insight message.
        """
        ...

    def add_warning(self: Any, message: str) -> None:
        """
        Add warning message.
        """
        ...

    def is_success(self: Any) -> bool:
        """
        Check if processing was successful.
        """
        ...

    def set_error(self: Any, message: str, error_type: str = 'ProcessingError', details: Optional[Dict[str, Any]] = None) -> None:
        """
        Set error information.
        """
        ...

    def to_dict(self: Any) -> Dict[str, Any]:
        """
        Convert to dictionary for serialization.
        """
        ...

class ProcessingStatus:
    # Processing status indicators.

    ERROR: str
    PARTIAL: str
    SUCCESS: str
    WARNING: str

class ProcessorProtocol:
    # Protocol for processors.

    def process(self: Any, _data: Any, _config: Any, _context: Optional[Any] = None) -> Any:
        """
        Process data with given configuration.
        """
        ...

class ProcessorRegistry:
    # Registry for processors and use cases.

    def __init__(self: Any) -> None:
        """
        Initialize registry.
        """
        ...

    def get_processor(self: Any, name: str) -> Optional[Any[Any]]:
        """
        Get processor class by name.
        """
        ...

    def get_use_case(self: Any, category: str, name: str) -> Optional[Any[Any]]:
        """
        Get use case class by category and name.
        
                Falls back to searching all categories if the exact category/name
                pair is not found (handles category mismatches like general/footfall
                when footfall is registered under retail).
        """
        ...

    def list_processors(self: Any) -> List[str]:
        """
        List all registered processors.
        """
        ...

    def list_use_cases(self: Any) -> Dict[str, List[str]]:
        """
        List all registered use cases by category.
        """
        ...

    def register_processor(self: Any, name: str, processor_class: Any[Any]) -> None:
        """
        Register a processor class.
        """
        ...

    def register_use_case(self: Any, category: str, name: str, use_case_class: Any[Any]) -> None:
        """
        Register a use case class.
        """
        ...

class ResultFormat:
    # Supported result formats.

    ACTIVITY_RECOGNITION: str
    CLASSIFICATION: str
    DETECTION: str
    FACE_RECOGNITION: str
    INSTANCE_SEGMENTATION: str
    OBJECT_TRACKING: str
    TRACKING: str
    UNKNOWN: str

