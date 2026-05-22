"""Auto-generated stub for module: face_recognition."""
from typing import Any, Dict, List, Optional, Tuple

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_categories, filter_by_confidence, match_results_structure
from .embedding_manager import EmbeddingConfig, EmbeddingManager
from .face_recognition_client import FacialRecognitionClient
from .people_activity_logging import PeopleActivityLogging

# Constants
cmd: List[Any]
log_file: Any

# Classes
class FaceRecognitionEmbeddingConfig:
    # Configuration for face recognition with embeddings use case.

    ...
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

class RedisFaceMatchResult:
    ...
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

