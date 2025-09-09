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
import threading
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


# ---- Lightweight identity tracking and temporal smoothing (adapted from compare_similarity.py) ---- #
from collections import deque, defaultdict


def _normalize_embedding(vec: List[float]) -> List[float]:
    """Normalize an embedding vector to unit length (L2). Returns float32 list."""
    try:
        arr = np.asarray(vec, dtype=np.float32)
        if arr.size == 0:
            return []
        n = np.linalg.norm(arr)
        if n > 0:
            arr = arr / n
        return arr.tolist()
    except Exception:
        return []


class FaceTracker:
    """
    Embedding-based face tracker:
    - Matches new face embeddings to existing tracks via cosine similarity
    - Creates a new track when no match exceeds the similarity threshold

    Note: AdvancedTracker is still the primary tracker for bounding boxes.
    This class is available as a lightweight fallback when external tracking is disabled.
    """

    def __init__(self, similarity_threshold: float = 0.60) -> None:
        self.similarity_threshold = similarity_threshold
        self.tracks: Dict[str, Dict[str, object]] = {}
        self.track_counter: int = 1

    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        a = np.asarray(vec1, dtype=np.float32)
        b = np.asarray(vec2, dtype=np.float32)
        if a.size == 0 or b.size == 0:
            return 0.0
        an = np.linalg.norm(a)
        bn = np.linalg.norm(b)
        if an == 0.0 or bn == 0.0:
            return 0.0
        sim = float(np.dot(a, b) / (an * bn))
        if sim > 1.0:
            sim = 1.0
        elif sim < -1.0:
            sim = -1.0
        return sim

    def _find_matching_track(self, new_embedding: List[float]) -> Optional[str]:
        if not new_embedding:
            return None
        best_similarity: float = 0.0
        best_track_id: Optional[str] = None
        for track_id, data in self.tracks.items():
            stored_embedding = data.get("embedding")
            if stored_embedding:
                sim = self._cosine_similarity(new_embedding, stored_embedding)  # type: ignore
                if sim > self.similarity_threshold and sim > best_similarity:
                    best_similarity = sim
                    best_track_id = track_id
        return best_track_id

    def assign_track_id(self, embedding: List[float], frame_id: Optional[int] = None) -> str:
        match_id = self._find_matching_track(embedding)
        if match_id is not None and match_id in self.tracks:
            self.tracks[match_id]["last_seen_frame"] = frame_id
            return match_id

        new_id = f"face_id_{self.track_counter}"
        self.tracks[new_id] = {
            "embedding": _normalize_embedding(embedding),
            "created_frame": frame_id,
            "last_seen_frame": frame_id,
        }
        self.track_counter += 1
        return new_id


class TemporalIdentityManager:
    """
    Maintains stable identity labels per tracker ID using temporal smoothing and embedding history.

    Adaptation for production: _compute_best_identity queries the face recognition API
    via search_similar_faces(embedding, threshold=0.01, limit=1) to obtain top-1 match and score.
    """

    def __init__(
        self,
        face_client: FacialRecognitionClient,
        recognition_threshold: float = 0.35,
        history_size: int = 20,
        unknown_patience: int = 7,
        switch_patience: int = 5,
        fallback_margin: float = 0.05,
    ) -> None:
        self.face_client = face_client
        self.threshold = float(recognition_threshold)
        self.history_size = int(history_size)
        self.unknown_patience = int(unknown_patience)
        self.switch_patience = int(switch_patience)
        self.fallback_margin = float(fallback_margin)
        self.tracks: Dict[Any, Dict[str, object]] = {}

    def _ensure_track(self, track_id: Any) -> None:
        if track_id not in self.tracks:
            self.tracks[track_id] = {
                "stable_staff_id": None,
                "stable_person_name": None,
                "stable_employee_id": None,
                "stable_score": 0.0,
                "stable_staff_details": {},
                "label_votes": defaultdict(int),  # staff_id -> votes
                "embedding_history": deque(maxlen=self.history_size),
                "unknown_streak": 0,
                "streaks": defaultdict(int),  # staff_id -> consecutive frames
            }

    async def _compute_best_identity(self, emb: List[float], location: str = "", timestamp: str = "") -> Tuple[Optional[str], str, float, Optional[str], Dict[str, Any], str]:
        """
        Query backend for top-1 match for the given embedding.
        Returns (staff_id, person_name, score, employee_id, staff_details, detection_type).
        Robust to varying response shapes.
        """
        if not emb or not isinstance(emb, list):
            return None, "Unknown", 0.0, None, {}, "unknown"
        try:
            resp = await self.face_client.search_similar_faces(
                face_embedding=emb,
                threshold=0.01,  # low threshold to always get top-1
                limit=1,
                collection="staff_enrollment",
                location=location,
                timestamp=timestamp,
            )
        except Exception:
            return None, "Unknown", 0.0, None, {}, "unknown"

        try:
            results: List[Any] = []
            if isinstance(resp, dict):
                if isinstance(resp.get("data"), list):
                    results = resp.get("data", [])
                elif isinstance(resp.get("results"), list):
                    results = resp.get("results", [])
                elif isinstance(resp.get("items"), list):
                    results = resp.get("items", [])
            elif isinstance(resp, list):
                results = resp

            if not results:
                return None, "Unknown", 0.0, None, {}, "unknown"

            item = results[0] if isinstance(results, list) else results
            # Be defensive with keys and types
            staff_id = item.get("staffId") if isinstance(item, dict) else None
            employee_id = str(item.get("_id")) if isinstance(item, dict) and item.get("_id") is not None else None
            score = float(item.get("score", 0.0)) if isinstance(item, dict) else 0.0
            detection_type = str(item.get("detectionType", "unknown")) if isinstance(item, dict) else "unknown"
            staff_details = item.get("staffDetails", {}) if isinstance(item, dict) else {}
            # Extract a person name from staff_details
            person_name = "Unknown"
            if isinstance(staff_details, dict) and staff_details:
                first_name = staff_details.get("firstName")
                last_name = staff_details.get("lastName")
                name = staff_details.get("name")
                if name:
                    person_name = str(name)
                else:
                    if first_name or last_name:
                        person_name = f"{first_name or ''} {last_name or ''}".strip() or "Unknown"
            # If API says unknown or missing staff_id, treat as unknown
            if not staff_id or detection_type == "unknown":
                return None, "Unknown", float(score), employee_id, staff_details if isinstance(staff_details, dict) else {}, "unknown"
            return str(staff_id), person_name, float(score), employee_id, staff_details if isinstance(staff_details, dict) else {}, "known"
        except Exception:
            return None, "Unknown", 0.0, None, {}, "unknown"

    async def _compute_best_identity_from_history(self, track_state: Dict[str, object], location: str = "", timestamp: str = "") -> Tuple[Optional[str], str, float, Optional[str], Dict[str, Any], str]:
        hist: deque = track_state.get("embedding_history", deque())  # type: ignore
        if not hist:
            return None, "Unknown", 0.0, None, {}, "unknown"
        try:
            proto = np.mean(np.asarray(list(hist), dtype=np.float32), axis=0)
            proto_list = proto.tolist() if isinstance(proto, np.ndarray) else list(proto)
        except Exception:
            proto_list = []
        return await self._compute_best_identity(proto_list, location=location, timestamp=timestamp)

    async def update(
        self,
        track_id: Any,
        emb: List[float],
        eligible_for_recognition: bool,
        location: str = "",
        timestamp: str = "",
    ) -> Tuple[Optional[str], str, float, Optional[str], Dict[str, Any], str]:
        """
        Update temporal identity state for a track and return a stabilized identity.
        Returns (staff_id, person_name, score, employee_id, staff_details, detection_type).
        """
        self._ensure_track(track_id)
        s = self.tracks[track_id]

        # Update embedding history
        if emb:
            try:
                history: deque = s["embedding_history"]  # type: ignore
                history.append(_normalize_embedding(emb))
            except Exception:
                pass

        # Defaults for return values
        stable_staff_id = s.get("stable_staff_id")
        stable_person_name = s.get("stable_person_name")
        stable_employee_id = s.get("stable_employee_id")
        stable_score = float(s.get("stable_score", 0.0))
        stable_staff_details = s.get("stable_staff_details", {}) if isinstance(s.get("stable_staff_details"), dict) else {}

        if eligible_for_recognition and emb:
            staff_id, person_name, inst_score, employee_id, staff_details, det_type = await self._compute_best_identity(
                emb, location=location, timestamp=timestamp
            )

            is_inst_known = staff_id is not None and inst_score >= self.threshold
            if is_inst_known:
                s["label_votes"][staff_id] += 1  # type: ignore
                s["streaks"][staff_id] += 1  # type: ignore
                s["unknown_streak"] = 0

                # Initialize stable if not set
                if stable_staff_id is None:
                    s["stable_staff_id"] = staff_id
                    s["stable_person_name"] = person_name
                    s["stable_employee_id"] = employee_id
                    s["stable_score"] = float(inst_score)
                    s["stable_staff_details"] = staff_details
                    return staff_id, person_name, float(inst_score), employee_id, staff_details, "known"

                # If same as stable, keep it and update score
                if staff_id == stable_staff_id:
                    s["stable_score"] = float(inst_score)
                    # prefer latest name/details if present
                    if person_name and person_name != stable_person_name:
                        s["stable_person_name"] = person_name
                    if isinstance(staff_details, dict) and staff_details:
                        s["stable_staff_details"] = staff_details
                    if employee_id:
                        s["stable_employee_id"] = employee_id
                    return staff_id, s.get("stable_person_name") or person_name, float(inst_score), s.get("stable_employee_id") or employee_id, s.get("stable_staff_details", {}), "known"

                # Competing identity: switch only if sustained and with slight margin
                if s["streaks"][staff_id] >= self.switch_patience and inst_score >= (self.threshold + 0.02):  # type: ignore
                    s["stable_staff_id"] = staff_id
                    s["stable_person_name"] = person_name
                    s["stable_employee_id"] = employee_id
                    s["stable_score"] = float(inst_score)
                    s["stable_staff_details"] = staff_details
                    # reset other streaks
                    try:
                        for k in list(s["streaks"].keys()):  # type: ignore
                            if k != staff_id:
                                s["streaks"][k] = 0  # type: ignore
                    except Exception:
                        pass
                    return staff_id, person_name, float(inst_score), employee_id, staff_details, "known"

                # Do not switch yet; keep stable but return instant score/name
                return stable_staff_id, stable_person_name or person_name, float(inst_score), stable_employee_id or employee_id, stable_staff_details, "known" if stable_staff_id else "unknown"

            # Instantaneous is unknown or low score
            s["unknown_streak"] = int(s.get("unknown_streak", 0)) + 1
            if stable_staff_id is not None and s["unknown_streak"] <= self.unknown_patience:  # type: ignore
                return stable_staff_id, stable_person_name or "Unknown", float(inst_score), stable_employee_id, stable_staff_details, "known"

            # Fallback: use prototype from history
            fb_staff_id, fb_name, fb_score, fb_employee_id, fb_details, fb_type = await self._compute_best_identity_from_history(s, location=location, timestamp=timestamp)
            if fb_staff_id is not None and fb_score >= max(0.0, self.threshold - self.fallback_margin):
                s["label_votes"][fb_staff_id] += 1  # type: ignore
                s["stable_staff_id"] = fb_staff_id
                s["stable_person_name"] = fb_name
                s["stable_employee_id"] = fb_employee_id
                s["stable_score"] = float(fb_score)
                s["stable_staff_details"] = fb_details
                s["unknown_streak"] = 0
                return fb_staff_id, fb_name, float(fb_score), fb_employee_id, fb_details, "known"

            # No confident identity
            s["stable_staff_id"] = stable_staff_id
            s["stable_person_name"] = stable_person_name
            s["stable_employee_id"] = stable_employee_id
            s["stable_score"] = float(stable_score)
            s["stable_staff_details"] = stable_staff_details
            return None, "Unknown", float(inst_score), None, {}, "unknown"

        # Not eligible or no embedding; keep stable if present
        if stable_staff_id is not None:
            return stable_staff_id, stable_person_name or "Unknown", float(stable_score), stable_employee_id, stable_staff_details, "known"
        return None, "Unknown", 0.0, None, {}, "unknown"


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
    similarity_threshold: float = 0.45
    # Base confidence threshold (separate from embedding similarity threshold)
    confidence_threshold: float = 0.1
    
    # Face recognition optional features
    enable_face_tracking: bool = True  # Enable advanced face tracking
    enable_auto_enrollment: bool = False  # Enable auto-enrollment of unknown faces
    enable_face_recognition: bool = (
        True  # Enable face recognition (requires credentials)
    )
    enable_unknown_face_processing: bool = (
        True  # TODO: Unable when we will be saving unkown faces # Enable unknown face cropping/uploading (requires frame data)
    )
    enable_people_activity_logging: bool = True  # Enable logging of known face activities

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

        # Global tracking state (thread-safe for totals only)
        self._total_recognized_count = 0
        self._total_unknown_count = 0
        self._unique_recognized_staff = set()
        self._unique_unknown_faces = set()
        self._tracking_lock = threading.Lock()

        # Person tracking: {person_id: [{"camera_id": str, "timestamp": str}, ...]}
        self.person_tracking: Dict[str, List[Dict[str, str]]] = {}

        self.face_client = None

        # Initialize PeopleActivityLogging without face client initially
        self.people_activity_logging = None

        # Initialize EmbeddingManager - will be configured in process method
        self.embedding_manager = None
        # Temporal identity manager for API-based top-1 identity smoothing
        self.temporal_identity_manager = None
        # Lightweight face tracker as fallback if external tracker disabled
        self.simple_face_tracker = None
        # Optional gating similar to compare_similarity
        self._track_first_seen: Dict[int, int] = {}
        self._probation_frames: int = 260  # default gate ~4 seconds at 60 fps; tune per stream
        self._min_face_w: int = 30
        self._min_face_h: int = 30

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
        
        Thread-safe: Uses local variables for per-request state and locks for global totals.
        Order-preserving: Processes detections sequentially to maintain input order.
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

        # Initialize People activity logging if enabled
        if config.enable_people_activity_logging and not self.people_activity_logging:
            self.people_activity_logging = PeopleActivityLogging(self.face_client)
            self.people_activity_logging.start_background_processing()
            self.logger.info("People activity logging enabled and started")

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

        # Initialize TemporalIdentityManager (top-1 via API with smoothing)
        if not self.temporal_identity_manager:
            self.temporal_identity_manager = TemporalIdentityManager(
                face_client=self.face_client,
                recognition_threshold=float(getattr(config, "similarity_threshold", 0.35) or 0.35),
                history_size=20,
                unknown_patience=7,
                switch_patience=5,
                fallback_margin=0.05,
            )

        # Initialize lightweight tracker only if advanced tracking disabled
        if not config.enable_face_tracking and self.simple_face_tracker is None:
            self.simple_face_tracker = FaceTracker(similarity_threshold=0.60)

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
        if True:#config.enable_face_tracking:
            try:
                from ..advanced_tracker import AdvancedTracker
                from ..advanced_tracker.config import TrackerConfig

                # Create tracker instance if it doesn't exist (preserves state across frames)
                if self.tracker is None:
                    if config.confidence_threshold is not None:
                        tracker_config = TrackerConfig(
                                        track_high_thresh=0.5,
                                        track_low_thresh=0.05,
                                        new_track_thresh=0.5,
                                        match_thresh=0.8,
                                        track_buffer=int(300),  # allow short occlusions
                                        max_time_lost=int(150),
                                        fuse_score=True,
                                        enable_gmc=False,
                                        frame_rate=int(20)
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
            # Assign track IDs using lightweight FaceTracker based on embeddings
            if self.simple_face_tracker is None:
                self.simple_face_tracker = FaceTracker(similarity_threshold=0.60)
            for det in processed_data:
                try:
                    emb = det.get("embedding", []) or []
                    assigned_id = self.simple_face_tracker.assign_track_id(emb, frame_id=det.get("frame_id", 0))
                    det["track_id"] = assigned_id
                except Exception:
                    # Leave track_id as-is if assignment fails
                    pass

        # Initialize local recognition summary variables
        current_recognized_count = 0
        current_unknown_count = 0
        recognized_persons = {}
        current_frame_staff_details = {}

        # Process face recognition for each detection (if enabled)
        if config.enable_face_recognition:
            face_recognition_result = await self._process_face_recognition(
                processed_data, config, stream_info, input_bytes
            )
            processed_data, current_recognized_count, current_unknown_count, recognized_persons, current_frame_staff_details = face_recognition_result
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
        counting_summary.update(self._get_face_recognition_summary(
            current_recognized_count, current_unknown_count, recognized_persons
        ))

        # Add detections to the counting summary (standard pattern for detection use cases)
        counting_summary["detections"] = processed_data

        alerts = self._check_alerts(counting_summary, frame_number, config)
        predictions = self._extract_predictions(processed_data)

        # Step: Generate structured incidents, tracking stats and business analytics with frame-based keys
        incidents_list = self._generate_incidents(
            counting_summary, alerts, config, frame_number, stream_info
        )
        tracking_stats_list = self._generate_tracking_stats(
            counting_summary, alerts, config, frame_number, stream_info, current_frame_staff_details
        )
        business_analytics_list = self._generate_business_analytics(
            counting_summary, alerts, config, stream_info, is_empty=True
        )
        summary_list = self._generate_summary(incidents_list, tracking_stats_list, business_analytics_list)

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

        # Initialize unknown faces storage if not exists
        if not hasattr(self, "unknown_faces_storage"):
            self.unknown_faces_storage = {}

        # Initialize frame availability warning flag to avoid spam
        if not hasattr(self, "_frame_warning_logged"):
            self._frame_warning_logged = False

        # Initialize per-request tracking (thread-safe)
        current_recognized_count = 0
        current_unknown_count = 0
        recognized_persons = {}
        current_frame_staff_details = {}  # Store staff details for current frame

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
        # Process detections sequentially to preserve order
        for detection in detections:
            # Filter faces by bbox size - only process faces larger than 5% of image area
            # bbox_area_percentage = self._calculate_bbox_area_percentage(detection, current_frame)
            # if bbox_area_percentage < 1:
            #     self.logger.debug(f"Skipping face with bbox area {bbox_area_percentage:.1f}% (< 5%)")
            #     continue
            
            # Process each detection sequentially with await to preserve order
            processed_detection = await self._process_face(
                detection, current_frame, location, current_timestamp, config,
                current_recognized_count, current_unknown_count, 
                recognized_persons, current_frame_staff_details
            )
            # Include both known and unknown faces in final detections (maintains original order)
            if processed_detection:
                final_detections.append(processed_detection)
                # Update local counters based on processed detection
                if processed_detection.get("recognition_status") == "known":
                    staff_id = processed_detection.get("person_id")
                    if staff_id:
                        current_frame_staff_details[staff_id] = processed_detection.get("person_name", "Unknown")
                        current_recognized_count += 1
                        recognized_persons[staff_id] = recognized_persons.get(staff_id, 0) + 1
                elif processed_detection.get("recognition_status") == "unknown":
                    current_unknown_count += 1

        return final_detections, current_recognized_count, current_unknown_count, recognized_persons, current_frame_staff_details

    async def _process_face(
        self,
        detection: Dict,
        current_frame: np.ndarray,
        location: str = "",
        current_timestamp: str = "",
        config: FaceRecognitionEmbeddingConfig = None,
        current_recognized_count: int = 0,
        current_unknown_count: int = 0,
        recognized_persons: Dict = None,
        current_frame_staff_details: Dict = None,
    ) -> Dict:

        # Extract and validate embedding using EmbeddingManager
        detection, embedding = self.embedding_manager.extract_embedding_from_detection(detection)
        if not embedding:
            return None

        # Get track_id for caching
        track_id = detection.get("track_id")
        if not track_id:
            self.logger.warning("No track_id found in detection - cannot use cache optimization")

        # Determine if detection is eligible for recognition (similar to compare_similarity gating)
        bbox = detection.get("bounding_box", {}) or {}
        x1 = int(bbox.get("xmin", bbox.get("x1", 0)))
        y1 = int(bbox.get("ymin", bbox.get("y1", 0)))
        x2 = int(bbox.get("xmax", bbox.get("x2", 0)))
        y2 = int(bbox.get("ymax", bbox.get("y2", 0)))
        w_box = max(1, x2 - x1)
        h_box = max(1, y2 - y1)
        frame_id = detection.get("frame_id", None)

        # Track probation age if we have a track_id
        if track_id is not None:
            if track_id not in self._track_first_seen:
                try:
                    self._track_first_seen[track_id] = int(frame_id) if frame_id is not None else self._total_frame_counter
                except Exception:
                    self._track_first_seen[track_id] = self._total_frame_counter
            age_frames = (int(frame_id) if frame_id is not None else self._total_frame_counter) - int(self._track_first_seen.get(track_id, 0)) + 1
        else:
            age_frames = 1

        eligible_for_recognition = (w_box >= self._min_face_w and h_box >= self._min_face_h)

        # Primary: API-based identity smoothing via TemporalIdentityManager
        staff_id = None
        person_name = "Unknown"
        similarity_score = 0.0
        employee_id = None
        staff_details: Dict[str, Any] = {}
        detection_type = "unknown"
        try:
            if self.temporal_identity_manager:
                staff_id, person_name, similarity_score, employee_id, staff_details, detection_type = await self.temporal_identity_manager.update(
                    track_id=track_id if track_id is not None else f"no_track_{id(detection)}",
                    emb=embedding,
                    eligible_for_recognition=eligible_for_recognition,
                    location=location,
                    timestamp=current_timestamp,
                )
        except Exception as e:
            self.logger.warning(f"TemporalIdentityManager update failed: {e}")

        # Fallback: if still unknown and we have an EmbeddingManager, use local search
        if (staff_id is None or detection_type == "unknown") and self.embedding_manager is not None:
            try:
                search_result = await self.embedding_manager.search_face_embedding(
                    embedding=embedding,
                    track_id=track_id,
                    location=location,
                    timestamp=current_timestamp,
                )
                if search_result:
                    employee_id = search_result.employee_id
                    staff_id = search_result.staff_id
                    detection_type = search_result.detection_type
                    staff_details = search_result.staff_details
                    person_name = search_result.person_name
                    similarity_score = search_result.similarity_score
            except Exception as e:
                self.logger.warning(f"Local embedding search fallback failed: {e}")

        # Update detection object directly (avoid relying on SearchResult type)
        detection = detection.copy()
        detection["person_id"] = staff_id
        detection["person_name"] = person_name or "Unknown"
        detection["recognition_status"] = "known" if staff_id else "unknown"
        detection["employee_id"] = employee_id
        detection["staff_details"] = staff_details if isinstance(staff_details, dict) else {}
        detection["similarity_score"] = float(similarity_score)
        if staff_id:
            detection["enrolled"] = True
            detection["category"] = f"{(person_name or 'Unknown').replace(' ', '_')}_{staff_id}"
        else:
            detection["enrolled"] = False
            detection["category"] = "unrecognized"

        # Update global tracking using thread-safe operations
        # Count as unknown if detection_type is "unknown" OR person_name starts with "Unknown"
        is_truly_unknown = (detection.get("recognition_status") == "unknown" or 
                           (person_name and str(person_name).startswith("Unknown")))
        
        if not is_truly_unknown and detection_type == "known":
            # This is a recognized person - track globally
            self._track_person(staff_id)
            with self._tracking_lock:
                if staff_id not in self._unique_recognized_staff:
                    self._unique_recognized_staff.add(staff_id)
                    self._total_recognized_count += 1
        else:
            # This is an unknown person - track globally
            if employee_id:
                with self._tracking_lock:
                    if employee_id not in self._unique_unknown_faces:
                        self._unique_unknown_faces.add(employee_id)
                        self._total_unknown_count += 1

        # Enqueue detection for background logging with all required parameters
        try:
            # Log known faces for activity tracking
            if (detection["recognition_status"] == "known" and 
                self.people_activity_logging and 
                config and 
                getattr(config, 'enable_people_activity_logging', True)):
                await self.people_activity_logging.enqueue_detection(
                    detection=detection,
                    current_frame=current_frame,
                    location=location,
                )
                self.logger.debug(f"Enqueued known face detection for activity logging: {detection.get('person_name', 'Unknown')}")
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

    def _get_face_recognition_summary(self, current_recognized_count: int, current_unknown_count: int, recognized_persons: Dict) -> Dict:
        """Get face recognition summary for current frame"""
        recognition_rate = 0.0
        total_current = current_recognized_count + current_unknown_count
        if total_current > 0:
            recognition_rate = (current_recognized_count / total_current) * 100

        # Get thread-safe global totals
        with self._tracking_lock:
            total_recognized = self._total_recognized_count
            total_unknown = self._total_unknown_count

        return {
            "face_recognition_summary": {
                "current_frame": {
                    "recognized": current_recognized_count,
                    "unknown": current_unknown_count,
                    "total": total_current,
                    "recognized_persons": dict(recognized_persons),
                    "recognition_rate": round(recognition_rate, 1),
                },
                "session_totals": {
                    "total_recognized": total_recognized,
                    "total_unknown": total_unknown,
                    "total_processed": total_recognized + total_unknown,
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
        current_frame_staff_details: Dict = None,
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
                staff_name = (current_frame_staff_details or {}).get(
                    person_id, f"Staff {person_id}"
                )
                human_text_lines.append(f"\t{staff_name} (ID: {person_id})")

        # Show current frame counts only (with tabs)
        human_text_lines.append(f"\tTotal Faces: {total_current}")
        human_text_lines.append(f"\tRecognized: {current_recognized}")
        human_text_lines.append(f"\tUnknown: {current_unknown}")
        # Additional counts similar to compare_similarity HUD
        try:
            human_text_lines.append(f"\tCurrent Faces (detections): {total_detections}")
            human_text_lines.append(f"\tTotal Unique Tracks: {cumulative_total}")
        except Exception:
            pass

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

    def _generate_summary(self, incidents: List, tracking_stats: List, business_analytics: List) -> List[str]:
        """
        Generate a human_text string for the tracking_stat, incident, business analytics and alerts.
        """
        lines = []
        lines.append("Application Name: "+self.CASE_TYPE)
        lines.append("Application Version: "+self.CASE_VERSION)
        if len(incidents) > 0:
            lines.append("Incidents: "+f"\n\t{incidents[0].get('human_text', 'No incidents detected')}")
        if len(tracking_stats) > 0:
            lines.append("Tracking Statistics: "+f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}")
        if len(business_analytics) > 0:
            lines.append("Business Analytics: "+f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}")

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines.append("Summary: "+"No Summary Data")

        return ["\n".join(lines)]

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
