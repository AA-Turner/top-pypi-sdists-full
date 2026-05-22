"""Stub file for post_processing.face_reg directory."""
from typing import Any, Dict, List, Optional, Set, Tuple

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_categories, filter_by_confidence, match_results_structure
from .embedding_manager import EmbeddingConfig, EmbeddingManager
from .face_recognition_client import FacialRecognitionClient
from .people_activity_logging import PeopleActivityLogging

# Constants
ALIGN: bool = ...  # From compare_similarity
DETECTOR_BACKEND: str = ...  # From compare_similarity
MODEL_NAME: str = ...  # From compare_similarity
cmd: List[Any] = ...  # From face_recognition
log_file: Any = ...  # From face_recognition

# Functions
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

# From face_recognition_client
def create_face_client(account_number: str = None, access_key: str = None, secret_key: str = None, project_id: str = None, server_id: str = '', session: Any = None) -> Any:
    """
    Create a facial recognition client with automatic credential detection
    """
    ...

# Classes
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

    def __init__(self: Any, config: Any, face_client: Any = None) -> None: ...

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
    def __init__(self: Any, config: Optional[Any] = None) -> None: ...

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

    def get_person_tracking_summary(self: Any) -> Dict:
        """
        Get summary of tracked persons with camera IDs and timestamps
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

    async def initialize(self: Any, config: Optional[Any] = None, emb: bool = False) -> None:
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

    async def process(self: Any, data: Any, config: Any, input_bytes: Optional[Any] = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
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

    def __init__(self: Any, session: Any = None, logger: Optional[Any.Any] = None, redis_url: Optional[str] = None, face_client: Any = None) -> None: ...

    ACTION_ID_PATTERN: Any

    def is_available(self: Any) -> bool: ...

    async def match_embedding(self: Any, embedding: List[float], search_id: Optional[str], location: str = '', min_confidence: Optional[float] = None) -> Optional[Any]:
        """
        Send embedding to Redis stream and wait for match result.
        """
        ...


# From face_recognition
class TemporalIdentityManager:
    # Maintains stable identity labels per tracker ID using temporal smoothing and embedding history.
    #
    # Adaptation for production: _compute_best_identity uses EmbeddingManager for local similarity
    # search first (fast), then falls back to API only if needed (slow).

    def __init__(self: Any, face_client: Any, embedding_manager: Any = None, redis_matcher: Optional[Any] = None, recognition_threshold: float = 0.15, history_size: int = 20, unknown_patience: int = 7, switch_patience: int = 5, fallback_margin: float = 0.05) -> None: ...

    async def update(self: Any, track_id: Any, emb: List[float], eligible_for_recognition: bool, location: str = '', timestamp: str = '', search_id: Optional[str] = None) -> Tuple[Optional[str], str, float, Optional[str], Dict[str, Any], str]:
        """
        Update temporal identity state for a track and return a stabilized identity.
        Returns (staff_id, person_name, score, employee_id, staff_details, detection_type).
        """
        ...


# From face_recognition_client
class FacialRecognitionClient:
    # Simplified Face Recognition Client using Matrice Session.
    # All API calls are made through the Matrice session RPC interface.

    def __init__(self: Any, account_number: str = '', access_key: str = '', secret_key: str = '', project_id: str = '', server_id: str = '', session: Any = None) -> None: ...

    ACTION_ID_PATTERN: Any

    async def enroll_staff(self: Any, staff_data: Dict[str, Any], image_paths: List[str]) -> Dict[str, Any]:
        """
        Enroll a new staff member with face images
        
        Args:
            staff_data: Dictionary containing staff information (staffId, firstName, lastName, etc.)
            image_paths: List of file paths to face images
        
        Returns:
            Dict containing enrollment response
        """
        ...

    async def enroll_staff_base64(self: Any, staff_data: Dict[str, Any], base64_images: List[str]) -> Dict[str, Any]:
        """
        Enroll staff with base64 encoded images
        
                API: POST /v1/facial_recognition/staff/enroll?projectId={projectId}&serverID={serverID}
        """
        ...

    async def enroll_unknown_person(self: Any, embedding: List[float], image_source: str = None, timestamp: str = None, location: str = None, _employee_id: str = None) -> Dict[str, Any]:
        """
        Enroll an unknown person
        
                API: POST /v1/facial_recognition/enroll_unknown_person?projectId={projectId}&serverID={serverID}
        """
        ...

    async def get_all_staff_embeddings(self: Any) -> Dict[str, Any]:
        """
        Get all staff embeddings
        
                API: GET /v1/facial_recognition/get_all_staff_embeddings?projectId={projectId}&serverID={serverID}
        """
        ...

    async def get_redis_details(self: Any) -> Dict[str, Any]:
        """
        Get Redis connection details from facial recognition server
        
                API: GET /v1/facial_recognition/get_redis_details
        
                Returns:
                    Dict containing Redis connection details (REDIS_IP, REDIS_PORT, REDIS_PASSWORD)
        """
        ...

    def get_server_connection_info(self: Any) -> Optional[Dict[str, Any]]:
        """
        Fetch server connection info from RPC.
        """
        ...

    async def get_staff_details(self: Any, staff_id: str) -> Dict[str, Any]:
        """
        Get full staff details by staff ID
        
                API: GET /v1/facial_recognition/staff/:staffId?projectId={projectId}&serverID={serverID}
        """
        ...

    async def health_check(self: Any) -> Dict[str, Any]:
        """
        Check if the facial recognition service is healthy
        """
        ...

    async def search_similar_faces(self: Any, face_embedding: List[float], threshold: float = 0.3, limit: int = 10, collection: str = 'staff_embeddings', location: str = '', timestamp: str = '') -> Dict[str, Any]:
        """
        Search for staff members by face embedding vector
        
        API: POST /v1/facial_recognition/search/similar?projectId={projectId}&serverID={serverID}
        
        Args:
            face_embedding: Face embedding vector
            collection: Vector collection name
            threshold: Similarity threshold (0.0 to 1.0)
            limit: Maximum number of results to return
            location: Location identifier for logging
            timestamp: Current timestamp in ISO format
        
        Returns:
            Dict containing search results with detectionType (known/unknown)
        """
        ...

    async def shutdown_service(self: Any, action_record_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Gracefully shutdown the service
        
                API: DELETE /v1/facial_recognition/shutdown?projectId={projectId}&serverID={serverID}
        """
        ...

    async def store_people_activity(self: Any, staff_id: str, detection_type: str, bbox: List[float], location: str, employee_id: Optional[str] = None, timestamp: str = datetime.now(timezone.utc).isoformat(), image_data: Optional[str] = None, camera_name: Optional[str] = None, camera_id: Optional[str] = None, rtp_number: Optional[str] = None) -> Dict[str, Any]:
        """
        Store people activity data with optional image data
        
        API: POST /v1/facial_recognition/store_people_activity?projectId={projectId}&serverID={serverID}
        
        Args:
            staff_id: Staff identifier (empty for unknown faces)
            detection_type: Type of detection (known, unknown, empty)
            bbox: Bounding box coordinates [x1, y1, x2, y2]
            location: Location identifier
            employee_id: Employee ID (for unknown faces, this will be generated)
            timestamp: Timestamp in ISO format
            image_data: Base64-encoded JPEG image data (optional)
        
        Returns:
            Dict containing response data with success status
        """
        ...

    async def update_deployment_action(self: Any, deployment_id: str) -> Dict[str, Any]:
        """
        Update deployment action in backend
        
                API: PUT /internal/v1/actions/update_facial_recognition_deployment/:server_id?app_deployment_id=:deployment_id
        
                Args:
                    deployment_id: The deployment ID to update
        
                Returns:
                    Dict containing response data
        """
        ...

    async def update_staff_images(self: Any, image_url: str, employee_id: str) -> Dict[str, Any]:
        """
        Update staff images with uploaded image URL
        
                API: PUT /v1/facial_recognition/staff/update_images?projectId={projectId}&serverID={serverID}
        """
        ...

    async def upload_image_to_url(self: Any, image_bytes: Any, upload_url: str) -> bool:
        """
        Upload image bytes to the provided URL
        """
        ...


# From people_activity_logging
class PeopleActivityLogging:
    # Background logging system for face recognition activity

    def __init__(self: Any, face_client: Any = None) -> None: ...

    def clear_unknown_faces_storage(self: Any) -> None:
        """
        Clear stored unknown face images
        """
        ...

    async def enqueue_detection(self: Any, detection: Dict, current_frame: Optional[Any.Any] = None, location: str = '', camera_name: str = '', camera_id: str = '', rtp_number: str = '') -> Any:
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


from . import compare_similarity, embedding_manager, face_recognition, face_recognition_client, people_activity_logging