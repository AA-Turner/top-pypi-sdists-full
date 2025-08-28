"""
Face Recognition with Track ID Cache Optimization

This module includes an optimization that caches face recognition results by track ID
to reduce redundant API calls. When a face detection is processed:

1. It checks the cache for existing results using track_id
2. If track_id found in cache, uses cached result instead of API call
3. If track_id not found, makes API call and caches the result
4. Cache includes automatic cleanup with TTL and size limits

Configuration options:
- enable_track_id_cache: Enable/disable the optimization
- cache_max_size: Maximum number of cached track IDs (default: 1000)
- cache_ttl: Cache time-to-live in seconds (default: 3600)
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import asdict
import time
import base64
import cv2
import numpy as np
from datetime import datetime, timezone

from ..core.base import (
    BaseProcessor,
    ProcessingContext,
    ProcessingResult,
    ConfigProtocol,
    ResultFormat,
)
from ..utils import (
    filter_by_confidence,
    filter_by_categories,
    apply_category_mapping,
    calculate_counting_summary,
    match_results_structure,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
)
from dataclasses import dataclass, field
from ..core.config import BaseConfig, AlertConfig
from .face_recognition_client import FacialRecognitionClient
from .people_activity_logging import PeopleActivityLogging
from .embedding_manager import EmbeddingManager, EmbeddingConfig


@dataclass
class FaceRecognitionEmbeddingConfig(BaseConfig):
    """Configuration for face recognition with embeddings use case."""

    # Smoothing configuration
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # Base confidence threshold (separate from embedding similarity threshold)
    confidence_threshold: float = 0.6
    
    # Face recognition optional features
    enable_face_tracking: bool = True  # Enable advanced face tracking
    enable_auto_enrollment: bool = False  # Enable auto-enrollment of unknown faces
    enable_face_recognition: bool = (
        True  # Enable face recognition (requires credentials)
    )
    enable_unknown_face_processing: bool = (
        True  # TODO: Unable when we will be saving unkown faces # Enable unknown face cropping/uploading (requires frame data)
    )

    usecase_categories: List[str] = field(default_factory=lambda: ["face"])

    target_categories: List[str] = field(default_factory=lambda: ["face"])

    alert_config: Optional[AlertConfig] = None

    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {0: "face"}
    )

    facial_recognition_server_id: str = ""
    session: Any = None  # Matrice session for face recognition client
    
    # Embedding configuration
    embedding_config: Optional[Any] = None  # Will be set to EmbeddingConfig instance
    
    # Similarity and confidence thresholds
    similarity_threshold: float = 0.6
    confidence_threshold: float = 0.6
    
    # Track ID cache optimization settings
    enable_track_id_cache: bool = True
    cache_max_size: int = 3000
    cache_ttl: int = 3600  # Cache time-to-live in seconds (1 hour)
    
    # Search settings
    search_limit: int = 5
    search_collection: str = "staff_enrollment"


class FaceRecognitionEmbeddingUseCase(BaseProcessor):
    # Human-friendly display names for categories
    CATEGORY_DISPLAY = {"face": "face"}

    def __init__(self):
        super().__init__("face_recognition")
        self.category = "security"

        self.CASE_TYPE: Optional[str] = "face_recognition"
        self.CASE_VERSION: Optional[str] = "1.0"
        # List of categories to track
        self.target_categories = ["face"]

        # Initialize smoothing tracker
        self.smoothing_tracker = None

        # Initialize advanced tracker (will be created on first use)
        self.tracker = None
        # Initialize tracking state variables
        self._total_frame_counter = 0
        self._global_frame_offset = 0

        # Track start time for "TOTAL SINCE" calculation
        self._tracking_start_time = datetime.now(
            timezone.utc
        )  # Store as datetime object for UTC

        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        # Tunable parameters – adjust if necessary for specific scenarios
        self._track_merge_iou_threshold: float = 0.05  # IoU ≥ 0.05 →
        self._track_merge_time_window: float = 7.0  # seconds within which to merge

        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"

        # Face recognition specific counters
        self.current_recognized_count = 0
        self.current_unknown_count = 0
        self.total_recognized_count = 0
        self.total_unknown_count = 0
        self.recognized_persons = {}
        self.current_frame_staff_details = {}  # Store staff details for current frame

        # Person tracking: {person_id: [{"camera_id": str, "timestamp": str}, ...]}
        self.person_tracking: Dict[str, List[Dict[str, str]]] = {}

        self.face_client = None

        # COMMENTED OUT: People activity logging functionality removed
        # Initialize PeopleActivityLogging without face client initially
        # self.people_activity_logging = None
        self.people_activity_logging = None  # Kept as None - functionality disabled

        # Initialize EmbeddingManager - will be configured in process method
        self.embedding_manager = None

    def _get_facial_recognition_client(
        self, config: FaceRecognitionEmbeddingConfig
    ) -> FacialRecognitionClient:
        """Get facial recognition client"""
        # Initialize face recognition client if not already done
        if self.face_client is None:
            self.logger.info(
                f"Initializing face recognition client with server ID: {config.facial_recognition_server_id}"
            )
            self.face_client = FacialRecognitionClient(
                server_id=config.facial_recognition_server_id, session=config.session
            )
            self.logger.info("Face recognition client initialized")

        return self.face_client

    async def process(
        self,
        data: Any,
        config: ConfigProtocol,
        input_bytes: Optional[bytes] = None,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        """
        Main entry point for face recognition with embeddings post-processing.
        Applies all standard processing plus face recognition and auto-enrollment.
        """
        start_time = time.time()
        # Ensure config is correct type
        if not isinstance(config, FaceRecognitionEmbeddingConfig):
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )
        if context is None:
            context = ProcessingContext()

        if not self.face_client:
            self.face_client = self._get_facial_recognition_client(config)

        # COMMENTED OUT: People activity logging functionality disabled
        # if not self.people_activity_logging:
        #     self.people_activity_logging = PeopleActivityLogging(self.face_client)
        #     self.people_activity_logging.start_background_processing()

        # Initialize EmbeddingManager if not already done
        if not self.embedding_manager:
            # Create default embedding config if not provided
            if not config.embedding_config:
                config.embedding_config = EmbeddingConfig(
                    similarity_threshold=config.similarity_threshold,
                    confidence_threshold=config.confidence_threshold,
                    enable_track_id_cache=config.enable_track_id_cache,
                    cache_max_size=config.cache_max_size,
                    cache_ttl=3600
                )
            self.embedding_manager = EmbeddingManager(config.embedding_config, self.face_client)

        # Detect input format and store in context
        input_format = match_results_structure(data)
        context.input_format = input_format

        # Validate input format for face recognition # Disabled to return frame results even if no faces detected
        # if input_format != ResultFormat.FACE_RECOGNITION:
        #     return self.create_error_result(
        #         f"Invalid input format for face recognition. Expected FACE_RECOGNITION, got {input_format.value}",
        #         usecase=self.name,
        #         category=self.category,
        #         context=context,
        #     )
        context.confidence_threshold = config.confidence_threshold

        # Parse face recognition model output format (with embeddings)
        processed_data = self._parse_face_model_output(data)

        # Apply standard confidence filtering
        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(
                processed_data, config.confidence_threshold
            )
            self.logger.debug(
                f"Applied confidence filtering with threshold {config.confidence_threshold}"
            )
        else:
            self.logger.debug(
                "Did not apply confidence filtering since threshold not provided"
            )

        # Apply category mapping if provided
        if config.index_to_category:
            processed_data = apply_category_mapping(
                processed_data, config.index_to_category
            )
            self.logger.debug("Applied category mapping")

        # Apply category filtering
        if config.target_categories:
            processed_data = filter_by_categories(
                processed_data, config.target_categories
            )
            self.logger.debug("Applied category filtering")

        # Apply bbox smoothing if enabled
        if config.enable_smoothing:
            if self.smoothing_tracker is None:
                smoothing_config = BBoxSmoothingConfig(
                    smoothing_algorithm=config.smoothing_algorithm,
                    window_size=config.smoothing_window_size,
                    cooldown_frames=config.smoothing_cooldown_frames,
                    confidence_threshold=config.confidence_threshold,
                    confidence_range_factor=config.smoothing_confidence_range_factor,
                    enable_smoothing=True,
                )
                self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)
            processed_data = bbox_smoothing(
                processed_data, self.smoothing_tracker.config, self.smoothing_tracker
            )

        # Advanced tracking (BYTETracker-like) - only if enabled
        if config.enable_face_tracking:
            try:
                from ..advanced_tracker import AdvancedTracker
                from ..advanced_tracker.config import TrackerConfig

                # Create tracker instance if it doesn't exist (preserves state across frames)
                if self.tracker is None:
                    if config.confidence_threshold is not None:
                        tracker_config = TrackerConfig(
                            track_high_thresh=float(config.confidence_threshold),
                            # Allow even lower detections to participate in secondary association
                            track_low_thresh=max(
                                0.05, float(config.confidence_threshold) / 2
                            ),
                            new_track_thresh=float(config.confidence_threshold),
                        )
                    else:
                        tracker_config = TrackerConfig()
                    self.tracker = AdvancedTracker(tracker_config)
                    self.logger.info(
                        "Initialized AdvancedTracker for Face Recognition with thresholds: "
                        f"high={tracker_config.track_high_thresh}, "
                        f"low={tracker_config.track_low_thresh}, "
                        f"new={tracker_config.new_track_thresh}"
                    )

                # The tracker expects the data in the same format as input
                # It will add track_id and frame_id to each detection
                processed_data = self.tracker.update(processed_data)

            except Exception as e:
                # If advanced tracker fails, fallback to unsmoothed detections
                self.logger.warning(f"AdvancedTracker failed: {e}")
        else:
            self.logger.debug("Advanced face tracking disabled in configuration")

        # Process face recognition for each detection (if enabled)
        if config.enable_face_recognition:
            processed_data = await self._process_face_recognition(
                processed_data, config, stream_info, input_bytes
            )
        else:
            # Just add default face recognition fields without actual recognition
            for detection in processed_data:
                detection["person_id"] = None
                detection["person_name"] = "Unknown"
                detection["recognition_status"] = "disabled"
                detection["enrolled"] = False

        # Update tracking state for total count per label
        self._update_tracking_state(processed_data)

        # Update frame counter
        self._total_frame_counter += 1

        # Extract frame information from stream_info
        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            # If start and end frame are the same, it's a single frame
            if (
                start_frame is not None
                and end_frame is not None
                and start_frame == end_frame
            ):
                frame_number = start_frame

        # Compute summaries and alerts
        general_counting_summary = calculate_counting_summary(data)
        counting_summary = self._count_categories(processed_data, config)
        # Add total unique counts after tracking using only local state
        total_counts = self.get_total_counts()
        counting_summary["total_counts"] = total_counts

        # NEW: Add face recognition summary
        counting_summary.update(self._get_face_recognition_summary())

        # Add detections to the counting summary (standard pattern for detection use cases)
        counting_summary["detections"] = processed_data

        alerts = self._check_alerts(counting_summary, frame_number, config)
        predictions = self._extract_predictions(processed_data)

        # Step: Generate structured incidents, tracking stats and business analytics with frame-based keys
        incidents_list = self._generate_incidents(
            counting_summary, alerts, config, frame_number, stream_info
        )
        tracking_stats_list = self._generate_tracking_stats(
            counting_summary, alerts, config, frame_number, stream_info
        )
        business_analytics_list = self._generate_business_analytics(
            counting_summary, alerts, config, stream_info, is_empty=True
        )
        summary_list = self._generate_summary(
            counting_summary,
            incidents_list,
            tracking_stats_list,
            business_analytics_list,
            alerts,
        )

        # Extract frame-based dictionaries from the lists
        incidents = incidents_list[0] if incidents_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
        business_analytics = (
            business_analytics_list[0] if business_analytics_list else {}
        )
        summary = summary_list[0] if summary_list else {}
        agg_summary = {
            str(frame_number): {
                "incidents": incidents,
                "tracking_stats": tracking_stats,
                "business_analytics": business_analytics,
                "alerts": alerts,
                "human_text": summary,
                "person_tracking": self.get_person_tracking_summary(),
            }
        }

        context.mark_completed()

        # Build result object following the standard pattern - same structure as people counting
        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

        return result

    def _parse_face_model_output(self, data: Any) -> List[Dict]:
        """Parse face recognition model output to standard detection format, preserving embeddings"""
        processed_data = []

        if isinstance(data, dict):
            # Handle frame-based format: {"0": [...], "1": [...]}
            for frame_id, frame_detections in data.items():
                if isinstance(frame_detections, list):
                    for detection in frame_detections:
                        if isinstance(detection, dict):
                            # Convert to standard format but preserve face-specific fields
                            standard_detection = {
                                "category": detection.get("category", "face"),
                                "confidence": detection.get("confidence", 0.0),
                                "bounding_box": detection.get("bounding_box", {}),
                                "track_id": detection.get("track_id", ""),
                                "frame_id": detection.get("frame_id", frame_id),
                                # Preserve face-specific fields
                                "embedding": detection.get("embedding", []),
                                "landmarks": detection.get("landmarks", None),
                                "fps": detection.get("fps", 30),
                            }
                            processed_data.append(standard_detection)
        elif isinstance(data, list):
            # Handle list format
            for detection in data:
                if isinstance(detection, dict):
                    # Convert to standard format and ensure all required fields exist
                    standard_detection = {
                        "category": detection.get("category", "face"),
                        "confidence": detection.get("confidence", 0.0),
                        "bounding_box": detection.get("bounding_box", {}),
                        "track_id": detection.get("track_id", ""),
                        "frame_id": detection.get("frame_id", 0),
                        # Preserve face-specific fields
                        "embedding": detection.get("embedding", []),
                        "landmarks": detection.get("landmarks", None),
                        "fps": detection.get("fps", 30),
                        "metadata": detection.get("metadata", {}),
                    }
                    processed_data.append(standard_detection)

        return processed_data

    def _extract_frame_from_data(self, input_bytes: bytes) -> Optional[np.ndarray]:
        """
        Extract frame from original model data

        Args:
            original_data: Original data from model (same format as model receives)

        Returns:
            np.ndarray: Frame data or None if not found
        """
        try:
            try:
                if isinstance(input_bytes, str):
                    frame_bytes = base64.b64decode(input_bytes)
                else:
                    frame_bytes = input_bytes
                nparr = np.frombuffer(frame_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                return frame
            except Exception as e:
                self.logger.debug(f"Could not decode direct frame data: {e}")

            return None

        except Exception as e:
            self.logger.debug(f"Error extracting frame from data: {e}")
            return None

    def _calculate_bbox_area_percentage(self, detection: Dict, current_frame: Optional[np.ndarray] = None) -> float:
        """Calculate the percentage of image area occupied by the bounding box"""
        try:
            bbox = detection.get("bounding_box", {})
            if not bbox:
                return 0.0
            
            # Extract bbox coordinates
            xmin = bbox.get("xmin", 0)
            ymin = bbox.get("ymin", 0) 
            xmax = bbox.get("xmax", 0)
            ymax = bbox.get("ymax", 0)
            
            # Calculate bbox area
            bbox_width = abs(xmax - xmin)
            bbox_height = abs(ymax - ymin)
            bbox_area = bbox_width * bbox_height
            
            # Get image dimensions - try from frame first, then estimate
            if current_frame is not None:
                img_height, img_width = current_frame.shape[:2]
                img_area = img_width * img_height
            else:
                # Estimate image area based on typical coordinates (assume normalized 0-1 or pixel coords)
                if max(xmax, ymax) <= 1.0:
                    # Normalized coordinates (0-1 range)
                    img_area = 1.0
                else:
                    # Pixel coordinates - estimate common resolutions
                    img_area = 1920 * 1080  # Default to Full HD
            
            # Calculate percentage
            area_percentage = (bbox_area / img_area) * 100
            return area_percentage
            
        except Exception as e:
            self.logger.warning(f"Error calculating bbox area percentage: {e}")
            return 0.0

    async def _process_face_recognition(
        self,
        detections: List[Dict],
        config: FaceRecognitionEmbeddingConfig,
        stream_info: Optional[Dict[str, Any]] = None,
        input_bytes: Optional[bytes] = None,
    ) -> List[Dict]:
        """Process face recognition for each detection with embeddings"""

        # Initialize face client only when needed and if credentials are available
        if not self.face_client:
            try:
                self.face_client = self._get_facial_recognition_client(config)
            except Exception as e:
                self.logger.warning(
                    f"Could not initialize face recognition client: {e}"
                )
                # No client available, return empty list (no results)
                return []

        # Reset current frame counters
        self.current_recognized_count = 0
        self.current_unknown_count = 0
        self.recognized_persons = {}
        self.current_frame_staff_details = {}

        # Initialize unknown faces storage if not exists
        if not hasattr(self, "unknown_faces_storage"):
            self.unknown_faces_storage = {}

        # Initialize frame availability warning flag to avoid spam
        if not hasattr(self, "_frame_warning_logged"):
            self._frame_warning_logged = False

        # Initialize unique staff tracking set if not exists
        if not hasattr(self, "unique_recognized_staff"):
            self.unique_recognized_staff = set()

        if not hasattr(self, "unique_unknown_faces"):
            self.unique_unknown_faces = set()

        # Extract frame from original data for cropping unknown faces
        current_frame = (
            self._extract_frame_from_data(input_bytes) if input_bytes else None
        )

        # Log frame availability once per session
        if current_frame is None and not self._frame_warning_logged:
            if config.enable_unknown_face_processing:
                self.logger.info(
                    "Frame data not available in model output - unknown face cropping/uploading will be skipped. "
                    "To disable this feature entirely, set enable_unknown_face_processing=False"
                )
            self._frame_warning_logged = True

        # Get location from stream_info
        location = (
            stream_info.get("camera_location", "unknown") if stream_info else "unknown"
        )

        # Generate current timestamp
        current_timestamp = datetime.now(timezone.utc).isoformat()

        final_detections = []
        for detection in detections:
            # Filter faces by bbox size - only process faces larger than 5% of image area
            # bbox_area_percentage = self._calculate_bbox_area_percentage(detection, current_frame)
            # if bbox_area_percentage < 1:
            #     self.logger.debug(f"Skipping face with bbox area {bbox_area_percentage:.1f}% (< 5%)")
            #     continue
            
            processed_detection = await self._process_face(
                detection, current_frame, location, current_timestamp
            )
            # Include both known and unknown faces in final detections
            if processed_detection:
                final_detections.append(processed_detection)

        return final_detections

    async def _process_face(
        self,
        detection: Dict,
        current_frame: np.ndarray,
        location: str = "",
        current_timestamp: str = "",
    ) -> Dict:

        # Extract and validate embedding using EmbeddingManager
        detection, embedding = self.embedding_manager.extract_embedding_from_detection(detection)
        if not embedding:
            return None

        # Get track_id for caching
        track_id = detection.get("track_id")
        if not track_id:
            self.logger.warning("No track_id found in detection - cannot use cache optimization")

        # Search for face using EmbeddingManager
        search_result = await self.embedding_manager.search_face_embedding(
            embedding=embedding,
            track_id=track_id,
            location=location,
            timestamp=current_timestamp
        )

        if not search_result:
            return None

        # Extract variables from search result
        employee_id = search_result.employee_id
        staff_id = search_result.staff_id
        detection_type = search_result.detection_type
        staff_details = search_result.staff_details
        person_name = search_result.person_name
        similarity_score = search_result.similarity_score

        # Update detection object with the search result variables
        detection = self.embedding_manager.update_detection_with_search_result(search_result, detection)
        if not detection:
            return None

        # Update local tracking based on detection type and person name
        # Count as unknown if detection_type is "unknown" OR person_name starts with "Unknown"
        is_truly_unknown = (detection_type == "unknown" or 
                           (person_name and person_name.startswith("Unknown")))
        
        if not is_truly_unknown and detection_type == "known":
            # This is a recognized person
            self.current_frame_staff_details[staff_id] = person_name
            self._track_person(staff_id)
            self.current_recognized_count += 1
            if staff_id not in self.unique_recognized_staff:
                self.unique_recognized_staff.add(staff_id)
                self.total_recognized_count += 1
            self.recognized_persons[staff_id] = (
                self.recognized_persons.get(staff_id, 0) + 1
            )
        else:
            # This is an unknown person
            self.current_unknown_count += 1
            if employee_id and employee_id not in self.unique_unknown_faces:
                self.unique_unknown_faces.add(employee_id)
                self.total_unknown_count += 1

        # COMMENTED OUT: Background logging functionality removed
        # Enqueue detection for background logging with all required parameters
        try:
            # TODO: Check if should log the unknown faces if not how to logs their face data
            if detection["recognition_status"] != "unknown" and self.people_activity_logging:
                await self.people_activity_logging.enqueue_detection(
                    detection=detection,
                    current_frame=current_frame,
                    location=location,
                )
        except Exception as e:
            self.logger.error(f"Error enqueueing detection for activity logging: {e}")

        return detection



    def _return_error_detection(
        self,
        detection: Dict,
        person_id: str,
        person_name: str,
        recognition_status: str,
        enrolled: bool,
        category: str,
        error: str,
    ) -> Dict:
        """Return error detection"""
        detection["person_id"] = person_id
        detection["person_name"] = person_name
        detection["recognition_status"] = recognition_status
        detection["enrolled"] = enrolled
        detection["category"] = category
        detection["error"] = error
        return detection

    def _track_person(self, person_id: str) -> None:
        """Track person with camera ID and UTC timestamp"""
        if person_id not in self.person_tracking:
            self.person_tracking[person_id] = []

        # Add current detection
        detection_record = {
            "camera_id": "test_camera_001",  # TODO: Get from stream_info in production
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        self.person_tracking[person_id].append(detection_record)

    def get_person_tracking_summary(self) -> Dict:
        """Get summary of tracked persons with camera IDs and timestamps"""
        return dict(self.person_tracking)

    def get_unknown_faces_storage(self) -> Dict[str, bytes]:
        """Get stored unknown face images as bytes"""
        if self.people_activity_logging:
            return self.people_activity_logging.get_unknown_faces_storage()
        return {}

    def clear_unknown_faces_storage(self) -> None:
        """Clear stored unknown face images"""
        if self.people_activity_logging:
            self.people_activity_logging.clear_unknown_faces_storage()

    def _get_face_recognition_summary(self) -> Dict:
        """Get face recognition summary for current frame"""
        recognition_rate = 0.0
        total_current = self.current_recognized_count + self.current_unknown_count
        if total_current > 0:
            recognition_rate = (self.current_recognized_count / total_current) * 100

        return {
            "face_recognition_summary": {
                "current_frame": {
                    "recognized": self.current_recognized_count,
                    "unknown": self.current_unknown_count,
                    "total": total_current,
                    "recognized_persons": dict(self.recognized_persons),
                    "recognition_rate": round(recognition_rate, 1),
                },
                "session_totals": {
                    "total_recognized": self.total_recognized_count,
                    "total_unknown": self.total_unknown_count,
                    "total_processed": self.total_recognized_count
                    + self.total_unknown_count,
                },
                "person_tracking": self.get_person_tracking_summary(),
            }
        }

    def _check_alerts(
        self, summary: dict, frame_number: Any, config: FaceRecognitionEmbeddingConfig
    ) -> List[Dict]:
        """
        Check if any alert thresholds are exceeded and return alert dicts.
        """

        def get_trend(data, lookback=900, threshold=0.6):
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True  # not enough data to determine trend
            increasing = 0
            total = 0
            for i in range(1, len(window)):
                if window[i] >= window[i - 1]:
                    increasing += 1
                total += 1
            ratio = increasing / total
            if ratio >= threshold:
                return True
            elif ratio <= (1 - threshold):
                return False

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts = []
        total_detections = summary.get("total_count", 0)
        face_summary = summary.get("face_recognition_summary", {})
        current_unknown = face_summary.get("current_frame", {}).get("unknown", 0)

        if not config.alert_config:
            return alerts

        if (
            hasattr(config.alert_config, "count_thresholds")
            and config.alert_config.count_thresholds
        ):
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "unknown_faces" and current_unknown > threshold:
                    alerts.append(
                        {
                            "alert_type": (
                                getattr(config.alert_config, "alert_type", ["Default"])
                                if hasattr(config.alert_config, "alert_type")
                                else ["Default"]
                            ),
                            "alert_id": f"alert_unknown_faces_{frame_key}",
                            "incident_category": "unknown_face_detection",
                            "threshold_level": threshold,
                            "current_count": current_unknown,
                            "ascending": get_trend(
                                self._ascending_alert_list, lookback=900, threshold=0.8
                            ),
                            "settings": {
                                t: v
                                for t, v in zip(
                                    (
                                        getattr(
                                            config.alert_config,
                                            "alert_type",
                                            ["Default"],
                                        )
                                        if hasattr(config.alert_config, "alert_type")
                                        else ["Default"]
                                    ),
                                    (
                                        getattr(
                                            config.alert_config, "alert_value", ["JSON"]
                                        )
                                        if hasattr(config.alert_config, "alert_value")
                                        else ["JSON"]
                                    ),
                                )
                            },
                        }
                    )
                elif category == "all" and total_detections > threshold:
                    alerts.append(
                        {
                            "alert_type": (
                                getattr(config.alert_config, "alert_type", ["Default"])
                                if hasattr(config.alert_config, "alert_type")
                                else ["Default"]
                            ),
                            "alert_id": "alert_" + category + "_" + frame_key,
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(
                                self._ascending_alert_list, lookback=900, threshold=0.8
                            ),
                            "settings": {
                                t: v
                                for t, v in zip(
                                    (
                                        getattr(
                                            config.alert_config,
                                            "alert_type",
                                            ["Default"],
                                        )
                                        if hasattr(config.alert_config, "alert_type")
                                        else ["Default"]
                                    ),
                                    (
                                        getattr(
                                            config.alert_config, "alert_value", ["JSON"]
                                        )
                                        if hasattr(config.alert_config, "alert_value")
                                        else ["JSON"]
                                    ),
                                )
                            },
                        }
                    )

        return alerts

    def _generate_tracking_stats(
        self,
        counting_summary: Dict,
        alerts: List,
        config: FaceRecognitionEmbeddingConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        """Generate structured tracking stats matching eg.json format with face recognition data."""
        camera_info = self.get_camera_info_from_stream(stream_info)
        tracking_stats = []

        total_detections = counting_summary.get("total_count", 0)
        total_counts_dict = counting_summary.get("total_counts", {})
        cumulative_total = sum(total_counts_dict.values()) if total_counts_dict else 0
        per_category_count = counting_summary.get("per_category_count", {})
        face_summary = counting_summary.get("face_recognition_summary", {})

        current_timestamp = self._get_current_timestamp_str(
            stream_info, precision=False
        )
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)

        # Create high precision timestamps for input_timestamp and reset_timestamp
        high_precision_start_timestamp = self._get_current_timestamp_str(
            stream_info, precision=True
        )
        high_precision_reset_timestamp = self._get_start_timestamp_str(
            stream_info, precision=True
        )

        # Build total_counts array in expected format
        total_counts = []
        for cat, count in total_counts_dict.items():
            if count > 0:
                total_counts.append({"category": cat, "count": count})

        # Add face recognition specific total counts
        session_totals = face_summary.get("session_totals", {})
        total_counts.extend(
            [
                {
                    "category": "recognized_faces",
                    "count": session_totals.get("total_recognized", 0),
                },
                {
                    "category": "unknown_faces",
                    "count": session_totals.get("total_unknown", 0),
                },
            ]
        )

        # Build current_counts array in expected format
        current_counts = []
        for cat, count in per_category_count.items():
            if count > 0 or total_detections > 0:
                current_counts.append({"category": cat, "count": count})

        # Add face recognition specific current counts
        current_frame = face_summary.get("current_frame", {})
        current_counts.extend(
            [
                {
                    "category": "recognized_faces",
                    "count": current_frame.get("recognized", 0),
                },
                {"category": "unknown_faces", "count": current_frame.get("unknown", 0)},
            ]
        )

        # Prepare detections with face recognition info
        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "face")

            detection_obj = self.create_detection_object(category, bbox)
            # Add face recognition specific fields
            detection_obj.update(
                {
                    "person_id": detection.get("person_id"),
                    "person_name": detection.get("person_name", "Unknown"),
                    "recognition_status": detection.get(
                        "recognition_status", "unknown"
                    ),
                    "enrolled": detection.get("enrolled", False),
                }
            )
            detections.append(detection_obj)

        # Build alert_settings array in expected format
        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_settings.append(
                {
                    "alert_type": (
                        getattr(config.alert_config, "alert_type", ["Default"])
                        if hasattr(config.alert_config, "alert_type")
                        else ["Default"]
                    ),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": (
                        config.alert_config.count_thresholds
                        if hasattr(config.alert_config, "count_thresholds")
                        else {}
                    ),
                    "ascending": True,
                    "settings": {
                        t: v
                        for t, v in zip(
                            (
                                getattr(config.alert_config, "alert_type", ["Default"])
                                if hasattr(config.alert_config, "alert_type")
                                else ["Default"]
                            ),
                            (
                                getattr(config.alert_config, "alert_value", ["JSON"])
                                if hasattr(config.alert_config, "alert_value")
                                else ["JSON"]
                            ),
                        )
                    },
                }
            )

        # Generate human_text in specified format
        current_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC")
        start_timestamp = self._tracking_start_time.strftime("%Y-%m-%d-%H:%M:%S UTC")

        human_text_lines = [f"CURRENT FRAME @ {current_timestamp}"]

        current_recognized = current_frame.get("recognized", 0)
        current_unknown = current_frame.get("unknown", 0)
        recognized_persons = current_frame.get("recognized_persons", {})
        total_current = current_recognized + current_unknown

        # Show staff names and IDs being recognized in current frame (with tabs)
        if recognized_persons:
            for person_id in recognized_persons.keys():
                # Get actual staff name from current frame processing
                staff_name = self.current_frame_staff_details.get(
                    person_id, f"Staff {person_id}"
                )
                human_text_lines.append(f"\t{staff_name} (ID: {person_id})")

        # Show current frame counts only (with tabs)
        human_text_lines.append(f"\tTotal Faces: {total_current}")
        human_text_lines.append(f"\tRecognized: {current_recognized}")
        human_text_lines.append(f"\tUnknown: {current_unknown}")

        human_text = "\n".join(human_text_lines)

        if alerts:
            for alert in alerts:
                human_text_lines.append(
                    f"Alerts: {alert.get('settings', {})} sent @ {current_timestamp}"
                )
        else:
            human_text_lines.append("Alerts: None")

        human_text = "\n".join(human_text_lines)
        reset_settings = [
            {"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}
        ]

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
            reset_time=high_precision_reset_timestamp,
        )

        tracking_stats.append(tracking_stat)
        return tracking_stats

    # Copy all other methods from face_recognition.py but add face recognition info to human text
    def _generate_incidents(
        self,
        counting_summary: Dict,
        alerts: List,
        config: FaceRecognitionEmbeddingConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        """Generate structured incidents for the output format with frame-based keys."""

        incidents = []
        total_detections = counting_summary.get("total_count", 0)
        face_summary = counting_summary.get("face_recognition_summary", {})
        current_frame = face_summary.get("current_frame", {})

        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        self._ascending_alert_list = (
            self._ascending_alert_list[-900:]
            if len(self._ascending_alert_list) > 900
            else self._ascending_alert_list
        )

        if total_detections > 0:
            # Determine event level based on unknown faces ratio
            level = "low"
            intensity = 5.0
            start_timestamp = self._get_start_timestamp_str(stream_info)
            if start_timestamp and self.current_incident_end_timestamp == "N/A":
                self.current_incident_end_timestamp = "Incident still active"
            elif (
                start_timestamp
                and self.current_incident_end_timestamp == "Incident still active"
            ):
                if (
                    len(self._ascending_alert_list) >= 15
                    and sum(self._ascending_alert_list[-15:]) / 15 < 1.5
                ):
                    self.current_incident_end_timestamp = current_timestamp
            elif (
                self.current_incident_end_timestamp != "Incident still active"
                and self.current_incident_end_timestamp != "N/A"
            ):
                self.current_incident_end_timestamp = "N/A"

            # Base intensity on unknown faces
            current_unknown = current_frame.get("unknown", 0)
            unknown_ratio = (
                current_unknown / total_detections if total_detections > 0 else 0
            )
            intensity = min(10.0, unknown_ratio * 10 + (current_unknown / 3))

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

            # Generate human text in new format with face recognition info
            current_recognized = current_frame.get("recognized", 0)
            human_text_lines = [f"FACE RECOGNITION INCIDENTS @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE,level)}")
            human_text_lines.append(f"\tRecognized Faces: {current_recognized}")
            human_text_lines.append(f"\tUnknown Faces: {current_unknown}")
            human_text_lines.append(f"\tTotal Faces: {total_detections}")
            human_text = "\n".join(human_text_lines)

            alert_settings = []
            if config.alert_config and hasattr(config.alert_config, "alert_type"):
                alert_settings.append(
                    {
                        "alert_type": (
                            getattr(config.alert_config, "alert_type", ["Default"])
                            if hasattr(config.alert_config, "alert_type")
                            else ["Default"]
                        ),
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": (
                            config.alert_config.count_thresholds
                            if hasattr(config.alert_config, "count_thresholds")
                            else {}
                        ),
                        "ascending": True,
                        "settings": {
                            t: v
                            for t, v in zip(
                                (
                                    getattr(
                                        config.alert_config, "alert_type", ["Default"]
                                    )
                                    if hasattr(config.alert_config, "alert_type")
                                    else ["Default"]
                                ),
                                (
                                    getattr(
                                        config.alert_config, "alert_value", ["JSON"]
                                    )
                                    if hasattr(config.alert_config, "alert_value")
                                    else ["JSON"]
                                ),
                            )
                        },
                    }
                )

            event = self.create_incident(
                incident_id=self.CASE_TYPE + "_" + str(frame_number),
                incident_type=self.CASE_TYPE,
                severity_level=level,
                human_text=human_text,
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=alert_settings,
                start_time=start_timestamp,
                end_time=self.current_incident_end_timestamp,
                level_settings={"low": 1, "medium": 3, "significant": 4, "critical": 7},
            )
            incidents.append(event)

        else:
            self._ascending_alert_list.append(0)
            incidents.append({})

        return incidents

    def _generate_business_analytics(
        self,
        counting_summary: Dict,
        alerts: Any,
        config: FaceRecognitionEmbeddingConfig,
        stream_info: Optional[Dict[str, Any]] = None,
        is_empty=False,
    ) -> List[Dict]:
        """Generate standardized business analytics for the agg_summary structure."""
        if is_empty:
            return []
        return []

    def _generate_summary(
        self,
        summary: dict,
        incidents: List,
        tracking_stats: List,
        business_analytics: List,
        alerts: List,
    ) -> List[str]:
        """
        Generate a human_text string for the tracking_stat, incident, business analytics and alerts.
        """
        lines = {}
        lines["Application Name"] = self.CASE_TYPE
        lines["Application Version"] = self.CASE_VERSION
        if len(incidents) > 0:
            lines["Incidents:"] = (
                f"\n\t{incidents[0].get('human_text', 'No incidents detected')}\n"
            )
        if len(tracking_stats) > 0:
            lines["Tracking Statistics:"] = (
                f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}\n"
            )
        if len(business_analytics) > 0:
            lines["Business Analytics:"] = (
                f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}\n"
            )

        if (
            len(incidents) == 0
            and len(tracking_stats) == 0
            and len(business_analytics) == 0
        ):
            lines["Summary"] = "No Summary Data"

        return [lines]

    # Include all the standard helper methods from face_recognition.py...
    def _count_categories(
        self, detections: list, config: FaceRecognitionEmbeddingConfig
    ) -> dict:
        """
        Count the number of detections per category and return a summary dict.
        The detections list is expected to have 'track_id' (from tracker), 'category', 'bounding_box', etc.
        Output structure will include 'track_id' for each detection as per AdvancedTracker output.
        """
        counts = {}
        for det in detections:
            cat = det.get("category", "unknown")
            counts[cat] = counts.get(cat, 0) + 1
        # Each detection dict will now include 'track_id' and face recognition fields
        return {
            "total_count": sum(counts.values()),
            "per_category_count": counts,
            "detections": [
                {
                    "bounding_box": det.get("bounding_box"),
                    "category": det.get("category"),
                    "confidence": det.get("confidence"),
                    "track_id": det.get("track_id"),
                    "frame_id": det.get("frame_id"),
                    # Face recognition fields
                    "person_id": det.get("person_id"),
                    "person_name": det.get("person_name"),
                    "recognition_status": det.get("recognition_status"),
                    "enrolled": det.get("enrolled"),
                    "embedding": det.get("embedding", []),
                    "landmarks": det.get("landmarks"),
                    "staff_details": det.get(
                        "staff_details"
                    ),  # Full staff information from API
                }
                for det in detections
            ],
        }

    def _extract_predictions(self, detections: list) -> List[Dict[str, Any]]:
        """
        Extract prediction details for output (category, confidence, bounding box, face recognition info).
        """
        return [
            {
                "category": det.get("category", "unknown"),
                "confidence": det.get("confidence", 0.0),
                "bounding_box": det.get("bounding_box", {}),
                "person_id": det.get("person_id"),
                "person_name": det.get("person_name"),
                "recognition_status": det.get("recognition_status"),
                "staff_details": det.get("staff_details"),
            }
            for det in detections
        ]

    # Copy all standard tracking, IoU, timestamp methods from face_recognition.py
    def _update_tracking_state(self, detections: list):
        """Track unique categories track_ids per category for total count after tracking."""
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {
                cat: set() for cat in self.target_categories
            }
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.target_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id

            self._per_category_total_track_ids.setdefault(cat, set()).add(canonical_id)
            self._current_frame_track_ids[cat].add(canonical_id)

    def get_total_counts(self):
        """Return total unique track_id count for each category."""
        return {
            cat: len(ids)
            for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()
        }

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        """Format timestamp for streams (YYYY:MM:DD HH:MM:SS format)."""
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        """Format timestamp for video chunks (HH:MM:SS.ms format)."""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision=False,
        frame_id: Optional[str] = None,
    ) -> str:
        """Get formatted current timestamp based on stream type."""
        if not stream_info:
            return "00:00:00.00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id) / stream_info.get(
                        "input_settings", {}
                    ).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get(
                        "start_frame", 30
                    ) / stream_info.get("input_settings", {}).get("original_fps", 30)
                stream_time_str = self._format_timestamp_for_video(start_time)
                return stream_time_str
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            if frame_id:
                start_time = int(frame_id) / stream_info.get("input_settings", {}).get(
                    "original_fps", 30
                )
            else:
                start_time = stream_info.get("input_settings", {}).get(
                    "start_frame", 30
                ) / stream_info.get("input_settings", {}).get("original_fps", 30)
            stream_time_str = self._format_timestamp_for_video(start_time)
            return stream_time_str
        else:
            stream_time_str = (
                stream_info.get("input_settings", {})
                .get("stream_info", {})
                .get("stream_time", "")
            )
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

    def _get_start_timestamp_str(
        self, stream_info: Optional[Dict[str, Any]], precision=False
    ) -> str:
        """Get formatted start timestamp for 'TOTAL SINCE' based on stream type."""
        if not stream_info:
            return "00:00:00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                return "00:00:00"
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            return "00:00:00"
        else:
            if self._tracking_start_time is None:
                stream_time_str = (
                    stream_info.get("input_settings", {})
                    .get("stream_info", {})
                    .get("stream_time", "")
                )
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(
                            tzinfo=timezone.utc
                        ).timestamp()
                    except:
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()

            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _compute_iou(self, box1: Any, box2: Any) -> float:
        """Compute IoU between two bounding boxes which may be dicts or lists."""

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
        """Return a stable canonical ID for a raw tracker ID."""
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

    def __del__(self):
        """Cleanup when object is destroyed"""
        try:
            if hasattr(self, "people_activity_logging") and self.people_activity_logging:
                self.people_activity_logging.stop_background_processing()
        except:
            pass
