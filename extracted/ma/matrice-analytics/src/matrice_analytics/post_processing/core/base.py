"""
Base classes and interfaces for the post-processing system.

This module provides the core abstractions that all post-processing components should follow.
"""

import importlib
import logging
import threading
import time
from abc import ABC, abstractmethod
from collections.abc import Iterator, MutableMapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, Type, Union, runtime_checkable

logger = logging.getLogger(__name__)


class ResultFormat(Enum):
    """Supported result formats."""

    DETECTION = "detection"
    TRACKING = "tracking"
    OBJECT_TRACKING = "object_tracking"
    CLASSIFICATION = "classification"
    INSTANCE_SEGMENTATION = "instance_segmentation"
    ACTIVITY_RECOGNITION = "activity_recognition"
    FACE_RECOGNITION = "face_recognition"
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

    # Performance tracking.
    # processing_start is a DURATION anchor, not a timestamp: it uses perf_counter()
    # so a wall-clock step (NTP correction, VM restore) cannot yield a negative
    # processing_time. perf_counter rather than monotonic because on Windows
    # monotonic() is GetTickCount64 (15.6 ms resolution), far too coarse for a
    # per-frame step. Use ``timestamp`` above for anything that needs a real date.
    processing_start: float = field(default_factory=time.perf_counter)
    processing_time: Optional[float] = None

    # Added for latency measurement
    processing_latency_ms: Optional[float] = None
    fps: Optional[float] = None

    # Additional context
    metadata: Dict[str, Any] = field(default_factory=dict)

    def mark_completed(self) -> None:
        """Mark processing as completed and calculate processing time, latency in ms, and fps."""
        # Monotonic on both ends (see processing_start) so this can never go negative.
        self.processing_time = time.perf_counter() - self.processing_start
        # Latency in milliseconds and the throughput this step could sustain in
        # isolation. NOTE: this is not the stream's frame rate -- see
        # engine.primitives.base.FrameContext.fps for that.
        self.processing_latency_ms = self.processing_time * 1000.0
        self.fps = (1.0 / self.processing_time) if self.processing_time > 0 else None
        # Per-frame performance metrics, logged at DEBUG.
        #
        # This is the highest-frequency line of code in the data path: it runs once
        # per frame from all 132 use-case processors, i.e. thousands of records per
        # second per device. At INFO it saturated the logging pipeline and, on
        # eMMC-backed edge hardware (Jetson), consumed the flash write budget.
        # The isEnabledFor() guard also skips the string formatting and LogRecord
        # allocation entirely when DEBUG is off, which is the normal production case.
        # The metrics themselves are unchanged and remain on the context object
        # (processing_time / processing_latency_ms / fps) for downstream telemetry.
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                "Processing completed in %.2f ms (%.2f fps)",
                self.processing_latency_ms,
                self.fps or 0.0,
            )


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

    def set_error(
        self,
        message: str,
        error_type: str = "ProcessingError",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
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
            "context": self.context.__dict__ if self.context else None,
        }


@runtime_checkable
class ConfigProtocol(Protocol):
    """Protocol for configuration objects."""

    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        pass


@runtime_checkable
class ProcessorProtocol(Protocol):
    """Protocol for processors."""

    # codeql[py/unused-parameter]
    def process(
        self,
        _data: Any,
        _config: ConfigProtocol,
        _context: Optional[ProcessingContext] = None,
    ) -> ProcessingResult:
        """Process data with given configuration."""
        pass


class BaseProcessor(ABC):
    """Base class for all processors with standardized agg_summary generation."""

    def __init__(self, name: str):
        """Initialize processor with name."""
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")

    @abstractmethod
    # codeql[py/unused-parameter]
    def process(
        self,
        _data: Any,
        _config: ConfigProtocol,
        _context: Optional[ProcessingContext] = None,
    ) -> ProcessingResult:
        """Process data with given configuration."""
        raise NotImplementedError(
            f"{self.__class__.__name__}.process() must be implemented by subclasses."
        )

    def create_result(
        self,
        data: Any,
        usecase: str = "",
        category: str = "",
        context: Optional[ProcessingContext] = None,
    ) -> ProcessingResult:
        """Create a successful result."""
        result = ProcessingResult(data=data, usecase=usecase, category=category, context=context)

        if context:
            result.processing_time = context.processing_time or 0.0

        return result

    def create_error_result(
        self,
        message: str,
        error_type: str = "ProcessingError",
        usecase: str = "",
        category: str = "",
        context: Optional[ProcessingContext] = None,
    ) -> ProcessingResult:
        """Create an error result."""
        result = ProcessingResult(data={}, usecase=usecase, category=category, context=context)
        result.set_error(message, error_type)

        if context:
            result.processing_time = context.processing_time or 0.0

        return result

    def _debug_stream_timing(self, label: str, value: Any) -> None:
        """Log stream/timestamp-related values at DEBUG (keeps timing locals meaningful when debugging)."""
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("%s %s=%r", self.name, label, value)

    def _debug_elapsed_since(self, start_time: float, label: str = "process") -> None:
        """Log wall-clock seconds since ``start_time`` at DEBUG.

        The wall clock here is DEBUG-only telemetry, never control logic -- an NTP
        step can make one logged duration absurd, and nothing branches on it.

        It cannot be converted in isolation: all 161 call sites across 74 use-case
        modules derive ``start_time`` from ``time.time()``, so swapping only this
        line would subtract a wall-clock reading from a monotonic one and print a
        number that is wrong every time rather than occasionally. Converting the
        pair is a 74-file change that belongs in its own PR, not in one that happens
        to touch this file -- the hook only fires here because semgrep inspects
        changed files.
        """
        if self.logger.isEnabledFor(logging.DEBUG):
            # nosemgrep: py-duration-from-wallclock
            self.logger.debug("%s.%s elapsed_s=%.4f", self.name, label, time.time() - start_time)

    # ===============================================================================
    # STANDARDIZED AGG_SUMMARY STRUCTURE METHODS
    # ===============================================================================

    def get_high_precision_timestamp(self) -> str:
        """Get high precision timestamp with microsecond granularity."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

    def get_standard_timestamp(self) -> str:
        """Get standard timestamp without microseconds."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC")

    def get_default_camera_info(self) -> Dict[str, str]:
        """Get default camera info structure."""
        return {
            "camera_name": "camera_1",
            "camera_group": "camera_group_1",
            "location": "Location TBD",
            "app_deployment_id": "",
            "application_id": "",
        }

    def get_default_level_settings(self) -> Dict[str, int]:
        """Get default severity level settings."""
        return {"low": 1, "medium": 3, "significant": 4, "critical": 7}

    def get_default_reset_settings(self) -> List[Dict[str, Any]]:
        """Get default reset settings."""
        return [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]

    def extract_deployment_ids(
        self, stream_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """Extract app_deployment_id and application_id from stream_info.

        Uses a priority-based fallback chain identical to the one in
        incident_manager_utils / business_metrics_manager_utils:

            stream_info root  >  input_settings  >  camera_info

        Each level checks snake_case and camelCase key variants.
        Returns a dict with ``app_deployment_id`` and ``application_id``
        (empty strings when not found).
        """
        result = {"app_deployment_id": "", "application_id": ""}
        if not stream_info or not isinstance(stream_info, dict):
            return result

        input_settings = stream_info.get("input_settings", {}) or {}
        if not isinstance(input_settings, dict):
            input_settings = {}
        cam_info = stream_info.get("camera_info", {}) or {}
        if not isinstance(cam_info, dict):
            cam_info = {}

        result["app_deployment_id"] = (
            stream_info.get("app_deployment_id", "")
            or stream_info.get("appDeploymentId", "")
            or stream_info.get("app_deploymentId", "")
            or input_settings.get("app_deployment_id", "")
            or input_settings.get("appDeploymentId", "")
            or cam_info.get("app_deployment_id", "")
            or cam_info.get("appDeploymentId", "")
            or ""
        )

        result["application_id"] = (
            stream_info.get("application_id", "")
            or stream_info.get("applicationId", "")
            or stream_info.get("app_id", "")
            or input_settings.get("application_id", "")
            or input_settings.get("applicationId", "")
            or cam_info.get("application_id", "")
            or cam_info.get("applicationId", "")
            or ""
        )

        return result

    def get_camera_info_from_stream(
        self,
        stream_info: Optional[Dict[str, Any]] = None,
        camera_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, str]:
        """Extract camera info from stream_info or use provided camera_info.

        The returned dict always includes ``app_deployment_id`` and
        ``application_id`` extracted from *stream_info* using a
        priority-based fallback chain (root -> input_settings -> camera_info).
        """
        default_camera_info = self.get_default_camera_info()

        if camera_info:
            result = default_camera_info.copy()
            result.update(camera_info)
        elif stream_info and stream_info.get("camera_info"):
            result = default_camera_info.copy()
            result.update(stream_info["camera_info"])
        else:
            result = default_camera_info.copy()

        if stream_info and isinstance(stream_info, dict):
            deployment_ids = self.extract_deployment_ids(stream_info)
            if deployment_ids.get("app_deployment_id") and not result.get("app_deployment_id"):
                result["app_deployment_id"] = deployment_ids["app_deployment_id"]
            if deployment_ids.get("application_id") and not result.get("application_id"):
                result["application_id"] = deployment_ids["application_id"]

        return result

    def create_incident(
        self,
        incident_id: str,
        incident_type: str,
        severity_level: str,
        human_text: str = "",
        camera_info: Optional[Dict[str, Any]] = None,
        alerts: Optional[List[Dict]] = None,
        alert_settings: Optional[List[Dict]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        level_settings: Optional[Dict[str, int]] = None,
    ) -> Dict[str, Any]:
        """Create a standardized incident object following the agg_summary format."""
        timestamp = start_time or self.get_high_precision_timestamp()

        return {
            "incident_id": incident_id,
            "incident_type": incident_type,
            "severity_level": severity_level,
            "human_text": human_text
            or f"{incident_type} detected. [Severity Level: {severity_level}]",
            "start_time": timestamp,
            "end_time": end_time or timestamp,
            "camera_info": camera_info or self.get_default_camera_info(),
            "level_settings": level_settings or self.get_default_level_settings(),
            "alerts": alerts or [],
            "alert_settings": alert_settings or [],
        }

    def create_tracking_stats(
        self,
        total_counts: List[Dict[str, Any]],
        current_counts: List[Dict[str, Any]],
        detections: List[Dict[str, Any]],
        human_text: str,
        camera_info: Optional[Dict[str, Any]] = None,
        alerts: Optional[List[Dict]] = None,
        alert_settings: Optional[List[Dict]] = None,
        reset_settings: Optional[List[Dict]] = None,
        start_time: Optional[str] = None,
        reset_time: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create standardized tracking stats object following the agg_summary format."""
        start_timestamp = start_time or self.get_high_precision_timestamp()
        reset_timestamp = reset_time or start_timestamp

        return {
            "input_timestamp": start_timestamp,
            "reset_timestamp": reset_timestamp,
            "camera_info": camera_info or self.get_default_camera_info(),
            "total_counts": total_counts,
            "current_counts": current_counts,
            "detections": detections,
            "alerts": alerts or [],
            "alert_settings": alert_settings or [],
            "reset_settings": reset_settings or self.get_default_reset_settings(),
            "human_text": human_text,
        }

    def create_business_analytics(
        self,
        analysis_name: str,
        statistics: Dict[str, Any],
        human_text: str,
        camera_info: Optional[Dict[str, Any]] = None,
        alerts: Optional[List[Dict]] = None,
        alert_settings: Optional[List[Dict]] = None,
        reset_settings: Optional[List[Dict]] = None,
        start_time: Optional[str] = None,
        reset_time: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create standardized business analytics object following the agg_summary format."""
        start_timestamp = start_time or self.get_high_precision_timestamp()
        reset_timestamp = reset_time or start_timestamp

        return {
            "analysis_name": analysis_name,
            "input_timestamp": start_timestamp,
            "reset_timestamp": reset_timestamp,
            "camera_info": camera_info or self.get_default_camera_info(),
            "statistics": statistics,
            "alerts": alerts or [],
            "alert_settings": alert_settings or [],
            "reset_settings": reset_settings or self.get_default_reset_settings(),
            "human_text": human_text,
        }

    def create_agg_summary(
        self,
        frame_id: Union[str, int],
        incidents: Optional[List[Dict]] = None,
        tracking_stats: Optional[List[Dict]] = None,
        business_analytics: Optional[List[Dict]] = None,
        alerts: Optional[List[Dict]] = None,
        human_text: str = "",
    ) -> Dict[str, Any]:
        """Create standardized agg_summary structure following the expected format."""
        frame_key = str(frame_id)

        return {
            frame_key: {
                "incidents": incidents or {},
                "tracking_stats": tracking_stats or {},
                "business_analytics": business_analytics or {},
                "alerts": alerts or [],
                "human_text": human_text,
            }
        }

    def create_detection_object(
        self,
        category: str,
        bounding_box: Dict[str, Any],
        _confidence: Optional[float] = None,
        segmentation: Optional[List] = None,
        track_id: Optional[Any] = None,
        plate_text: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a standardized detection object for tracking stats."""
        _ = (_confidence,)
        detection = {"category": category, "bounding_box": bounding_box}
        if plate_text:
            detection["category"] = plate_text

        if segmentation is not None:
            detection["segmentation"] = segmentation

        if track_id is not None:
            detection["track_id"] = track_id

        return detection

    def create_count_object(self, category: str, count: int) -> Dict[str, Any]:
        """Create a standardized count object for total_counts and current_counts."""
        return {"category": category, "count": count}

    def create_alert_object(
        self,
        alert_type: str,
        alert_id: str,
        incident_category: str,
        threshold_value: float,
        ascending: bool = True,
        settings: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Create a standardized alert object."""
        return {
            "alert_type": alert_type,
            "alert_id": alert_id,
            "incident_category": incident_category,
            "threshold_value": threshold_value,
            "ascending": ascending,
            "settings": settings or {},
        }

    def determine_severity_level(
        self,
        count: int,
        threshold_low: int = 3,
        threshold_medium: int = 7,
        threshold_critical: int = 15,
    ) -> str:
        """Determine severity level based on count and thresholds."""
        if count >= threshold_critical:
            return "critical"
        elif count >= threshold_medium:
            return "significant"
        elif count >= threshold_low:
            return "medium"
        else:
            return "low"

    def generate_tracking_human_text(
        self,
        current_counts: Dict[str, int],
        total_counts: Dict[str, int],
        current_timestamp: str,
        reset_timestamp: str,
        alerts_summary: str = "None",
    ) -> str:
        """Generate standardized human text for tracking stats."""
        lines = ["Tracking Statistics:"]
        lines.append(f"CURRENT FRAME @ {current_timestamp}")

        for category, count in current_counts.items():
            lines.append(f"\t{category}: {count}")

        lines.append(f"TOTAL SINCE {reset_timestamp}")
        for category, count in total_counts.items():
            lines.append(f"\t{category}: {count}")

        lines.append(f"Alerts: {alerts_summary}")

        return "\n".join(lines)

    def generate_analytics_human_text(
        self,
        _analysis_name: str,
        statistics: Dict[str, Any],
        current_timestamp: str,
        reset_timestamp: str,
        alerts_summary: str = "None",
    ) -> str:
        """Generate standardized human text for business analytics."""
        _ = (_analysis_name,)
        lines = ["Analytics Statistics:"]
        lines.append(f"CURRENT FRAME @ {current_timestamp}")

        for key, value in statistics.items():
            lines.append(f"\t{key}: {value}")

        lines.append(f"TOTAL SINCE {reset_timestamp}")
        for key, value in statistics.items():
            lines.append(f"\t{key}: {value}")

        lines.append(f"Alerts: {alerts_summary}")

        return "\n".join(lines)

    def detect_frame_structure(self, data: Any) -> bool:
        """Detect if data has frame-based structure (multi-frame) or single frame."""
        if isinstance(data, dict):
            # Check if all keys are numeric (frame IDs) and values are lists
            return all(isinstance(k, (str, int)) for k in data.keys() if str(k).isdigit())
        return False

    def extract_frame_ids(self, data: Any) -> List[str]:
        """Extract frame IDs from frame-based data structure."""
        if isinstance(data, dict):
            return [str(k) for k in data.keys() if str(k).isdigit() or k.startswith("frame")]
        return ["current_frame"]

    def create_frame_wise_agg_summary(
        self,
        frame_incidents: Dict[str, List[Dict]],
        frame_tracking_stats: Dict[str, List[Dict]],
        frame_business_analytics: Dict[str, List[Dict]],
        frame_alerts: Dict[str, List[Dict]] = None,
        frame_human_text: Dict[str, str] = None,
    ) -> Dict[str, Any]:
        """Create frame-wise agg_summary structure for multiple frames."""
        agg_summary = {}

        # Get all frame IDs from all sources
        all_frame_ids = set()
        all_frame_ids.update(frame_incidents.keys())
        all_frame_ids.update(frame_tracking_stats.keys())
        all_frame_ids.update(frame_business_analytics.keys())
        if frame_alerts:
            all_frame_ids.update(frame_alerts.keys())

        for frame_id in all_frame_ids:
            agg_summary[str(frame_id)] = {
                "incidents": frame_incidents.get(frame_id, {}),
                "tracking_stats": frame_tracking_stats.get(frame_id, {}),
                "business_analytics": frame_business_analytics.get(frame_id, {}),
                "alerts": frame_alerts.get(frame_id, []) if frame_alerts else [],
                "human_text": frame_human_text.get(frame_id, "") if frame_human_text else "",
            }

        return agg_summary

    # ===============================================================================
    # LEGACY HELPER METHODS (DEPRECATED - USE NEW STANDARDIZED METHODS ABOVE)
    # ===============================================================================

    def create_structured_event(
        self,
        event_type: str,
        level: str,
        intensity: float,
        application_name: str,
        location_info: str = None,
        additional_info: str = "",
        application_version: str = "1.0",
    ) -> Dict:
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
                "level_settings": {"info": 2, "warning": 5, "critical": 7},
            },
            "application_name": application_name,
            "application_version": application_version,
            "location_info": location_info,
            "human_text": f"Event: {event_type.replace('_', ' ').title()}\nLevel: {level.title()}\nTime: {datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC')}\n{additional_info}",
        }

    def create_structured_tracking_stats(self, _results_data: Dict, human_text: str) -> Dict:
        """Create structured tracking stats in the required format."""
        _ = (_results_data,)
        from datetime import datetime, timezone

        return {
            "input_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC"),
            "reset_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC"),
            "camera_info": None,  # Should be populated from stream info
            "total_counts": [],
            "current_counts": [],
            "detections": [],
            "alerts": [],
            "alert_settings": [],
            "reset_settings": [
                {
                    "interval_type": "daily",
                    "reset_time": {"value": 9, "time_unit": "hour"},
                }
            ],
            "human_text": human_text,
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

    def create_agg_summary_for_frame(
        self,
        frame_number: Union[int, str],
        incidents: List[Dict] = None,
        tracking_stats: List[Dict] = None,
        business_analytics: List[Dict] = None,
        alerts: List[Dict] = None,
        human_text: str = "",
    ) -> Dict[str, Any]:
        """Create agg_summary structure for a specific frame matching the expected format."""
        frame_key = str(frame_number)

        return {
            frame_key: {
                "incidents": incidents or [],
                "tracking_stats": tracking_stats or [],
                "business_analytics": business_analytics or [],
                "alerts": alerts or [],
                "human_text": human_text,
            }
        }

    def create_structured_incident(
        self,
        incident_id: str,
        incident_type: str,
        severity_level: str,
        start_time: str = None,
        end_time: str = None,
        camera_info: Dict = None,
        alerts: List[Dict] = None,
        alert_settings: List[Dict] = None,
    ) -> Dict:
        """Create a structured incident in the required format."""
        from datetime import datetime, timezone

        if start_time is None:
            start_time = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
        if end_time is None:
            end_time = start_time

        return {
            "incident_id": incident_id,
            "incident_type": incident_type,
            "severity_level": severity_level,
            "human_text": f"{incident_type} detected @ {start_time} [Severity Level: {severity_level}]",
            "start_time": start_time,
            "end_time": end_time,
            "camera_info": camera_info
            or {
                "camera_name": "No Camera Name",
                "camera_group": "No Camera Group",
                "location": "No Location",
            },
            "level_settings": {"low": 1, "medium": 3, "significant": 4, "critical": 7},
            "alerts": alerts or [],
            "alert_settings": alert_settings or [],
        }

    def create_structured_business_analytics(
        self,
        analysis_name: str,
        statistics: Dict,
        camera_info: Dict = None,
        alerts: List[Dict] = None,
        alert_settings: List[Dict] = None,
    ) -> Dict:
        """Create structured business analytics in the required format."""
        from datetime import datetime, timezone

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        return {
            "analysis_name": analysis_name,
            "input_timestamp": timestamp,
            "reset_timestamp": timestamp,
            "camera_info": camera_info
            or {
                "camera_name": "No Camera Name",
                "camera_group": "No Camera Group",
                "location": "No Location",
            },
            "statistics": statistics,
            "alerts": alerts or [],
            "alert_settings": alert_settings or [],
            "reset_settings": [
                {
                    "interval_type": "daily",
                    "reset_time": {"value": 9, "time_unit": "hour"},
                }
            ],
            "human_text": f"Analytics Statistics:\nCURRENT FRAME @ {timestamp}\n\t{analysis_name}: {statistics}\nTOTAL SINCE {timestamp}\n\t{analysis_name}: {statistics}\nAlerts: None",
        }


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
        _ = (overrides,)

    def validate_config(self, config: ConfigProtocol) -> List[str]:
        """Validate configuration for this use case."""
        return config.validate()


class UseCaseLoadError(ImportError):
    """A registered use case exists in the catalogue but its module would not load.

    Subclasses :class:`ImportError` so existing ``except ImportError`` handlers --
    including the one ml-codebases wraps its analytics import in -- keep working.
    """


class _LazyCategoryMap(MutableMapping):
    """The ``name -> class`` half of ``ProcessorRegistry._use_cases``.

    Iteration, ``len`` and ``in`` answer from the static catalogue and import
    nothing; only ``registry["category"]["name"]`` actually loads a module.  This
    is what lets callers keep reading ``registry._use_cases`` -- which several
    tests and ``engine/migration/harness.py`` do -- without resurrecting the eager
    import of every use-case module.
    """

    def __init__(self, registry: "ProcessorRegistry", category: str) -> None:
        self._registry = registry
        self._category = category

    def _names(self) -> set:
        return set(self._registry._concrete.get(self._category, {})) | set(
            self._registry._lazy.get(self._category, {})
        )

    def __getitem__(self, name: str) -> Type[BaseUseCase]:
        resolved = self._registry._resolve(self._category, name)
        if resolved is None:
            raise KeyError(name)
        return resolved

    def __setitem__(self, name: str, value: Type[BaseUseCase]) -> None:
        self._registry.register_use_case(self._category, name, value)

    def __delitem__(self, name: str) -> None:
        with self._registry._lock:
            self._registry._concrete.get(self._category, {}).pop(name, None)
            self._registry._lazy.get(self._category, {}).pop(name, None)

    def __iter__(self) -> Iterator:
        return iter(sorted(self._names()))

    def __len__(self) -> int:
        return len(self._names())

    def __repr__(self) -> str:
        return f"<lazy use cases for {self._category!r}: {len(self)}>"


class _LazyUseCaseMap(MutableMapping):
    """The ``category -> {name: class}`` view exposed as ``_use_cases``."""

    def __init__(self, registry: "ProcessorRegistry") -> None:
        self._registry = registry

    def _categories(self) -> set:
        return set(self._registry._concrete) | set(self._registry._lazy)

    def __getitem__(self, category: str) -> _LazyCategoryMap:
        if category not in self._categories():
            raise KeyError(category)
        return _LazyCategoryMap(self._registry, category)

    def __setitem__(self, category: str, value: Dict[str, Type[BaseUseCase]]) -> None:
        for name, use_case_class in dict(value).items():
            self._registry.register_use_case(category, name, use_case_class)

    def __delitem__(self, category: str) -> None:
        with self._registry._lock:
            self._registry._concrete.pop(category, None)
            self._registry._lazy.pop(category, None)

    def __iter__(self) -> Iterator:
        return iter(sorted(self._categories()))

    def __len__(self) -> int:
        return len(self._categories())

    def __repr__(self) -> str:
        return f"<lazy use-case registry: {len(self)} categories>"


class ProcessorRegistry:
    """Registry for processors and use cases.

    Use cases may be registered either eagerly (a class object) or lazily (a
    ``"module:ClassName"`` spec resolved on first lookup).  Lazy registration is
    what keeps ``import matrice_analytics.post_processing`` from executing the
    whole use-case catalogue -- see ``core/_usecase_table.py``.
    """

    def __init__(self):
        """Initialize registry."""
        self._processors: Dict[str, Type[BaseProcessor]] = {}
        #: Classes already resolved -- the storage the eager API always used.
        self._concrete: Dict[str, Dict[str, Type[BaseUseCase]]] = {}
        #: ``category -> name -> "module:ClassName"``, resolved on demand.
        self._lazy: Dict[str, Dict[str, str]] = {}
        self._lock = threading.Lock()
        #: Back-compatible view; ``registry._use_cases`` is read by callers
        #: outside this module, so it keeps behaving like the plain nested dict.
        self._use_cases = _LazyUseCaseMap(self)

    def register_processor(self, name: str, processor_class: Type[BaseProcessor]) -> None:
        """Register a processor class."""
        self._processors[name] = processor_class
        logger.debug(f"Registered processor: {name}")

    def register_use_case(
        self, category: str, name: str, use_case_class: Type[BaseUseCase]
    ) -> None:
        """Register a use case class."""
        with self._lock:
            self._concrete.setdefault(category, {})[name] = use_case_class
        logger.debug(f"Registered use case: {category}/{name}")

    def register_use_case_lazy(self, category: str, name: str, spec: str) -> None:
        """Register a use case by ``"module:ClassName"``, loaded on first lookup.

        ``module`` is an absolute module path, e.g.
        ``"matrice_analytics.post_processing.usecases.people_counting:PeopleCountingUseCase"``.
        """
        with self._lock:
            self._lazy.setdefault(category, {})[name] = spec

    def register_use_cases_lazy(self, table: Dict[str, Dict[str, str]]) -> None:
        """Seed the registry from a whole ``category -> {name: spec}`` catalogue."""
        with self._lock:
            for category, entries in table.items():
                self._lazy.setdefault(category, {}).update(entries)

    def _load(self, category: str, name: str, spec: str) -> Type[BaseUseCase]:
        """Import and return the class named by a ``"module:ClassName"`` spec.

        ``module`` is absolute, e.g.
        ``"matrice_analytics.post_processing.usecases.people_counting:PeopleCountingUseCase"``.

        A failure is re-raised naming the registry key, because the bare
        ``ModuleNotFoundError`` says which module is missing but not which use case
        asked for it -- and under lazy resolution the caller is a
        ``get_use_case(category, name)`` several frames away, not an import statement
        the reader can see.
        """
        module_name, _, qualname = spec.partition(":")
        try:
            return getattr(importlib.import_module(module_name), qualname)
        except (ImportError, AttributeError) as exc:
            raise UseCaseLoadError(
                f"use case '{category}/{name}' could not be loaded from '{spec}': {exc}"
            ) from exc

    def _resolve(self, category: str, name: str) -> Optional[Type[BaseUseCase]]:
        """Return the class for an exact ``category``/``name``, loading if needed."""
        resolved = self._concrete.get(category, {}).get(name)
        if resolved is not None:
            return resolved
        spec = self._lazy.get(category, {}).get(name)
        if spec is None:
            return None
        # Import OUTSIDE the lock: taking our lock around an import would nest it
        # inside CPython's per-module import lock, which deadlocks if any use-case
        # module touches the registry while being imported.  Two threads racing the
        # same spec both get the identical object out of sys.modules, so the
        # last-write-wins insert below is correct.
        use_case_class = self._load(category, name, spec)
        with self._lock:
            self._concrete.setdefault(category, {})[name] = use_case_class
        return use_case_class

    def get_processor(self, name: str) -> Optional[Type[BaseProcessor]]:
        """Get processor class by name."""
        return self._processors.get(name)

    def get_use_case(self, category: str, name: str) -> Optional[Type[BaseUseCase]]:
        """Get use case class by category and name.

        Falls back to searching all categories if the exact category/name
        pair is not found (handles category mismatches like general/footfall
        when footfall is registered under retail).
        """
        result = self._resolve(category, name)
        if result is not None:
            return result
        # The fallback must scan the lazy catalogue as well as the resolved one:
        # against the resolved dict alone it would search a nearly empty map and
        # silently stop finding exactly the mismatches it exists to paper over.
        for cat in sorted(set(self._concrete) | set(self._lazy)):
            if cat == category:
                continue
            try:
                found = self._resolve(cat, name)
            except UseCaseLoadError as exc:
                # One unloadable entry must not abort the scan.  Before lazy
                # resolution this loop walked an already-populated dict and could not
                # raise at all -- a module that failed to import took the whole
                # package down at import time, so it was simply absent here.  Letting
                # the exception escape would let one broken use case break lookups for
                # every unrelated one that happens to sort after it.
                logger.warning(f"skipping unloadable use case while searching for '{name}': {exc}")
                continue
            if found is not None:
                logger.warning(
                    f"Use case '{name}' not found under '{category}', found under '{cat}' instead"
                )
                return found
        return None

    def list_processors(self) -> List[str]:
        """List all registered processors."""
        return list(self._processors.keys())

    def list_use_cases(self) -> Dict[str, List[str]]:
        """List all registered use cases by category.

        Answers from the catalogue; imports nothing.
        """
        categories = set(self._concrete) | set(self._lazy)
        return {
            category: sorted(
                set(self._concrete.get(category, {})) | set(self._lazy.get(category, {}))
            )
            for category in sorted(categories)
        }


# Global registry instance
registry = ProcessorRegistry()

# Seed the full legacy catalogue as lazy specs.  This is the single authoritative
# source (PY-22) and costs one dict literal -- no use-case module is imported until
# something actually asks for one.
from ._usecase_table import USE_CASE_TABLE  # noqa: E402  (must follow `registry`)

registry.register_use_cases_lazy(USE_CASE_TABLE)
