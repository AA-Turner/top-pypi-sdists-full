"""Auto-generated stub for module: embedding_manager."""
from typing import Any, Dict, List, Optional, Set, Tuple

from .face_recognition_client import FacialRecognitionClient

# Classes
class EmbeddingConfig:
    # Configuration for embedding processing and search.

    ...
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

class SearchResult:
    # Search result containing staff information as separate variables.

    ...
class StaffEmbedding:
    # Staff embedding data structure.

    ...
