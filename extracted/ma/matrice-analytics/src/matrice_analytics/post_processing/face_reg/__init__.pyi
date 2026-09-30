"""Stub file for post_processing.face_reg directory."""
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from . import bounded_state
from ...clients import bootstrap, identity
from ...clients.analytics_client import AnalyticsClient
from ...clients.fr_client import FRClient
from ...clients.models import build_people_activity
from ...clients.response import CallFailure
from ..Trackers.integration import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_categories, filter_by_confidence, match_results_structure
from ..utils.format_utils import face_landmarks
from ..utils.geometry_utils import bbox_is_normalized, bbox_xyxy_pixels, resolve_frame_dims
from ..utils.geometry_utils import bbox_xyxy_pixels
from ..utils.location_name_cache import LocationNameCache
from ..utils.post_processing_config_client import is_resolvable_location_id
from ..utils.public_ip import resolve_public_ip_once
from .embedding_manager import EmbeddingConfig, EmbeddingManager
from .people_activity_logging import PeopleActivityLogging

# Constants
FACE_TRACK_MAX: int = ...  # From bounded_state
FACE_TRACK_TTL_S: float = ...  # From bounded_state
PERSON_SIGHTINGS_MAX_PERSONS: int = ...  # From bounded_state
PERSON_SIGHTINGS_PER_PERSON: int = ...  # From bounded_state
PERSON_SIGHTINGS_TTL_S: float = ...  # From bounded_state
ALIGN: bool = ...  # From compare_similarity
DETECTOR_BACKEND: str = ...  # From compare_similarity
MODEL_NAME: str = ...  # From compare_similarity
ACTIVITY_BBOX_GRID: int = ...  # From people_activity_logging
ACTIVITY_DROP_LOG_INTERVAL_S: float = ...  # From people_activity_logging
ACTIVITY_QUEUE_MAXSIZE: int = ...  # From people_activity_logging

# Functions
# From bounded_state
def begin_frame() -> None:
    """
    Start collecting the current frame's sightings; earlier frames' are no longer reported.
    """
    ...

# From bounded_state
def idle_index(owner: Any, attr: str, max_entries: int, ttl_s: float) -> Any:
    """
    Return the index stored on ``owner`` under ``attr``, creating it on first use.
    """
    ...

# From bounded_state
def prune_track_state(owner: Any, track_id: Any, *maps: Any) -> None:
    """
    Refresh ``track_id`` in ``owner``'s per-track index and drop idle tracks from ``maps``.
    """
    ...

# From bounded_state
def record_sighting(owner: Any, person_id: str, record: Dict[str, str]) -> None:
    """
    Append one sighting to ``owner.person_tracking``.
    
        Keeps at most PERSON_SIGHTINGS_PER_PERSON sightings per person and forgets
        persons not seen for PERSON_SIGHTINGS_TTL_S or beyond PERSON_SIGHTINGS_MAX_PERSONS.
    """
    ...

# From bounded_state
def sightings_summary(tracking: Any[str, Any], frame_counts: Any[str, int] | None = None) -> Dict[str, List[Dict[str, str]]]:
    """
    ``{person_id: [sighting, ...]}`` in the historical shape.
    
        With ``frame_counts`` (the persons counted in the current frame) only the
        sightings recorded since the last :func:`begin_frame` are returned, for those
        persons, so the per-frame payload is bounded by the frame's detections rather
        than by uptime. A person counted without a sighting this frame is left out.
    """
    ...

# From bounded_state
def touch_and_prune(index: Any, key: Any, *maps: Any) -> None:
    """
    Refresh ``key`` and drop every evicted key from ``maps``.
    """
    ...

# From compare_similarity
def compare_identity_and_samples(identity_folder: str, sample_folder: str, threshold: float = 0.82) -> Any:
    """
    Compare each sample image against all identities (subdirectories) using average similarity.
    """
    ...

# From compare_similarity
def compute_pairwise_similarities(embeddings: List[List[float]]) -> Dict[Tuple[int, int], float]:
    """
    Computes pairwise cosine similarities for a list of embeddings using NumPy.
    """
    ...

# From compare_similarity
def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Cosine similarity using NumPy operations with numeric safety.
    """
    ...

# From compare_similarity
def detect_identity_in_video(video_path: str, identity_folder: str, output_path: str = 'output_identity_detection.mp4', threshold: float = 0.75, person_to_embs: Any = None) -> Any: ...

# From compare_similarity
def get_embedding(image_path: str) -> List[float]:
    """
    Return the first face embedding from an image using DeepFace.represent, normalized to unit length.
    """
    ...

# From compare_similarity
def get_embeddings_from_folder(folder_path: str, max_images: Optional[int] = None) -> Tuple[List[List[float]], List[str]]: ...

# From compare_similarity
def get_embeddings_per_person(identity_root: str, max_images_per_person: Optional[int] = None) -> Dict[str, List[List[float]]]:
    """
    Build a mapping: person (subdirectory name) -> list of embeddings from all images inside it.
    """
    ...

# From compare_similarity
def normalize_embedding(vec: List[float]) -> List[float]:
    """
    Normalize an embedding vector to unit length (L2).
    
        Returns a float32 list to ensure consistent downstream math and JSON safety.
    """
    ...

# Classes
# From bounded_state
class IdleEvictionIndex:
    # Last-touch times per key, with an idle TTL and an LRU cap.
    #
    #     ``touch`` refreshes a key and returns the keys that must now be dropped: any
    #     key idle for longer than ``ttl_s`` (monotonic clock), and the least recently
    #     touched keys beyond ``max_entries``. The key just touched is never returned.
    #     Each call costs O(1 + number of evicted keys).

    def __init__(self: Any, max_entries: int, ttl_s: float, clock: Callable[[], float] = time.monotonic) -> None: ...

    def touch(self: Any, key: Any) -> List[Any]: ...


# From compare_similarity
class FaceTracker:
    # Embedding-based face tracker (mirrors tracker logic in face_recognition_model.py):
    # - Matches new face embeddings to existing tracks via cosine similarity
    # - Creates a new track when no match exceeds the similarity threshold

    def __init__(self: Any, similarity_threshold: float = 0.6) -> None: ...

    def assign_track_id(self: Any, embedding: List[float], frame_id: Optional[int] = None) -> str: ...


# From compare_similarity
class TemporalIdentityManager:
    # Maintains stable identity labels per track using temporal smoothing and embedding history.
    #
    # - Suppresses brief misclassifications (1-2 frames)
    # - Holds previous identity during short UNKNOWN gaps using unknown_patience
    # - Fallback: when current is UNKNOWN, match the prototype (mean) embedding history to identities

    def __init__(self: Any, person_to_embs: Dict[str, List[List[float]]], recognition_threshold: float = 0.7, history_size: int = 20, unknown_patience: int = 7, switch_patience: int = 5, fallback_margin: float = 0.05) -> None: ...

    def update(self: Any, track_id: int, emb: List[float], inst_label: Optional[str], inst_sim: float) -> Tuple[str, float]: ...


# From embedding_manager
class EmbeddingConfig:
    # Configuration for embedding processing and search.

    ...

# From embedding_manager
class EmbeddingManager:
    # Manages face embeddings, search operations, and caching.
    #
    # CRITICAL INITIALIZATION FLOW:
    # 1. __init__() creates the manager but does NOT load embeddings or start background refresh
    # 2. External caller MUST call await _load_staff_embeddings() to load embeddings synchronously
    # 3. After successful load, caller SHOULD call start_background_refresh() for periodic updates
    # 4. The _embeddings_loaded flag tracks whether embeddings are ready for use
    # 5. All search operations check _embeddings_loaded before proceeding
    #
    # This design prevents race conditions where:
    # - Background thread tries to load while main thread is loading
    # - Search operations are called before embeddings are loaded
    # - Multiple threads compete for the embeddings_lock during initialization
    #
    # Thread Safety:
    # - _embeddings_lock protects embeddings_matrix and embedding_metadata
    # - _cache_lock protects track_id_cache
    # - _embeddings_loaded is set only after successful load under lock

    def __init__(self: Any, config: Any, face_client: Optional[Any] = None) -> None: ...

    def extract_embedding_from_detection(self: Any, detection: Dict) -> Tuple[Dict, Optional[List[float]]]:
        """
        Extract and validate embedding from detection.
        """
        ...

    def get_best_similarity(self: Any, query_embedding: List[float]) -> float:
        """
        Return the best cosine similarity for debugging/observability (no threshold gating).
        """
        ...

    def get_status(self: Any) -> Dict[str, Any]:
        """
        Get detailed status of embedding manager for debugging and health checks.
        
        Returns:
            Dictionary with status information
        """
        ...

    def is_ready(self: Any) -> bool:
        """
        Check if embeddings are loaded and ready for use.
        
        Held under _embeddings_lock so the (flag, matrix, metadata) tuple is
        observed atomically — preventing a torn read where the flag is True but
        the matrix has been swapped out by a concurrent reload.
        """
        ...

    async def search_face_embedding(self: Any, embedding: List[float], track_id: str = None, _location: str = '', _timestamp: str = '') -> Optional[Any]:
        """
        Search for similar faces using embedding with local similarity search first, then API fallback.
        
        Args:
            embedding: Face embedding vector
            track_id: Track ID for caching optimization
            location: Location identifier for logging
            timestamp: Current timestamp in ISO format
        
        Returns:
            SearchResult containing staff information as variables or None if failed
        """
        ...

    def set_face_client(self: Any, face_client: Any) -> Any:
        """
        Set the face recognition client.
        """
        ...

    def start_background_refresh(self: Any) -> Any:
        """
        Start the background embedding refresh thread
        """
        ...

    def stop_background_refresh(self: Any) -> Any:
        """
        Stop the background embedding refresh thread
        """
        ...

    def update_detection_with_search_result(self: Any, search_result: Any, detection: Dict) -> Dict:
        """
        Update detection object with search result data.
        """
        ...


# From embedding_manager
class SearchResult:
    # Search result containing staff information as separate variables.

    ...

# From embedding_manager
class StaffEmbedding:
    # Staff embedding data structure.

    ...

# From face_recognition
class FaceRecognitionEmbeddingConfig:
    # Configuration for face recognition with embeddings use case.

    ...

# From face_recognition
class FaceRecognitionEmbeddingUseCase:
    def __init__(self: Any, config: Any | None = None) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def clear_unknown_faces_storage(self: Any) -> None:
        """
        Clear stored unknown face images
        """
        ...

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame vs the previous one.
        """
        ...

    def get_person_tracking_summary(self: Any, frame_counts: Dict[str, int] | None = None) -> Dict:
        """
        Recent sightings per person; with frame_counts, only this frame's sightings.
        """
        ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def get_unknown_faces_storage(self: Any) -> Dict[str, Any]:
        """
        Get stored unknown face images as bytes
        """
        ...

    async def initialize(self: Any, config: Any | None = None, emb: bool = False) -> None:
        """
        Async initialization method to set up face client and all components.
        Must be called after __init__ before process() can be called.
        
        CRITICAL INITIALIZATION SEQUENCE:
        1. Initialize face client and update deployment
        2. Create EmbeddingManager (does NOT load embeddings yet)
        3. Synchronously load embeddings with _load_staff_embeddings() - MUST succeed
        4. Verify embeddings are actually loaded (fail-fast if not)
        5. Start background refresh thread (only after successful load)
        6. Initialize TemporalIdentityManager with loaded EmbeddingManager
        7. Final verification of all components
        
        This sequence ensures:
        - No race conditions between main load and background thread
        - Fail-fast behavior if embeddings can't be loaded
        - All components have verified embeddings before use
        
        Args:
            config: Optional config to use. If not provided, uses config from __init__.
            emb: Optional boolean to indicate if embedding manager should be loaded. If True, embedding manager will be loaded.
        Raises:
            RuntimeError: If embeddings fail to load or verification fails
        """
        ...

    async def process(self: Any, data: Any, config: Any, input_bytes: Any | None = None, context: Any | None = None, stream_info: Dict[str, Any] | None = None) -> Any:
        """
        Main entry point for face recognition with embeddings post-processing.
        Applies all standard processing plus face recognition and auto-enrollment.
        
        Thread-safe: Uses local variables for per-request state and locks for global totals.
        Order-preserving: Processes detections sequentially to maintain input order.
        """
        ...


# From face_recognition
class RedisFaceMatchResult:
    ...

# From face_recognition
class RedisFaceMatcher:
    # Handles Redis-based face similarity search.

    def __init__(self: Any, session: Any = None, logger: Any.Any | None = None, redis_url: str | None = None, face_client: Any = None) -> None: ...

    def is_available(self: Any) -> bool: ...

    async def match_embedding(self: Any, embedding: List[float], search_id: str | None, location: str = '', camera_id: str = '', min_confidence: float | None = None) -> Any | None:
        """
        Send embedding to Redis stream and wait for match result.
        """
        ...

    def set_application_id(self: Any, application_id: str | None) -> None:
        """
        Seed the applicationId for subsequent stream payloads.
        
                Called once per frame by ``FaceRecognitionUseCase.process`` with the value it
                already extracts from ``stream_info``. Empty values are ignored rather than
                cached, so one frame that arrives without deployment identity cannot blank out
                an id that was already resolved.
        """
        ...


# From face_recognition
class TemporalIdentityManager:
    # Maintains stable identity labels per tracker ID using temporal smoothing and embedding history.
    #
    # Adaptation for production: _compute_best_identity uses EmbeddingManager for local similarity
    # search first (fast), then falls back to API only if needed (slow).

    def __init__(self: Any, face_client: Any, embedding_manager: Any = None, redis_matcher: Any | None = None, recognition_threshold: float = 0.15, history_size: int = 20, unknown_patience: int = 7, switch_patience: int = 5, fallback_margin: float = 0.0, sticky_id: bool = False, high_confidence_thresh: float = 0.0, sticky_min_votes: int = 3, max_tracks: int = bounded_state.FACE_TRACK_MAX, track_ttl_s: float = bounded_state.FACE_TRACK_TTL_S) -> None: ...

    async def update(self: Any, track_id: Any, emb: List[float], eligible_for_recognition: bool, location: str = '', camera_id: str = '', timestamp: str = '', search_id: str | None = None) -> Tuple[str | None, str, float, str | None, Dict[str, Any], str]:
        """
        Update temporal identity state for a track and return a stabilized identity.
        Returns (staff_id, person_name, score, employee_id, staff_details, detection_type).
        """
        ...


# From people_activity_logging
class PeopleActivityLogging:
    # Background logging system for face recognition activity

    def __init__(self: Any, face_client: Any | None = None) -> None: ...

    def clear_unknown_faces_storage(self: Any) -> None:
        """
        Clear stored unknown face images
        """
        ...

    async def enqueue_detection(self: Any, detection: Dict, current_frame: Any.Any | None = None, location: str = '', camera_name: str = '', camera_id: str = '', rtp_number: str = '', application_id: str = '') -> Any:
        """
        Enqueue a detection for background processing
        """
        ...

    def get_unknown_faces_storage(self: Any) -> Dict[str, Any]:
        """
        Get stored unknown face images as bytes
        """
        ...

    def start_background_processing(self: Any) -> Any:
        """
        Start the background processing thread
        """
        ...

    def stop_background_processing(self: Any) -> Any:
        """
        Stop the background processing thread
        """
        ...


from . import bounded_state, compare_similarity, embedding_manager, face_recognition, people_activity_logging