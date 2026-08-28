import logging
import threading
import time
from dataclasses import dataclass
from typing import Any, Dict, List, NamedTuple, Optional, Tuple

import numpy as np

from .face_recognition_client import FacialRecognitionClient


class SearchResult(NamedTuple):
    """Search result containing staff information as separate variables."""

    employee_id: str
    staff_id: str
    detection_type: str  # "known" or "unknown"
    staff_details: Dict[str, Any]
    person_name: str
    similarity_score: float


class StaffEmbedding(NamedTuple):
    """Staff embedding data structure."""

    embedding_id: str
    staff_id: str
    embedding: List[float]
    employee_id: str
    staff_details: Dict[str, Any]
    is_active: bool


@dataclass
class EmbeddingConfig:
    """Configuration for embedding processing and search."""

    # Similarity and confidence thresholds
    similarity_threshold: float = 0.35
    confidence_threshold: float = 0.6

    # Track ID cache optimization settings
    enable_track_id_cache: bool = True
    cache_max_size: int = 3000
    cache_ttl: int = 3600  # Cache time-to-live in seconds (1 hour)

    # Search settings
    search_limit: int = 5
    search_collection: str = "staff_embeddings"

    # Background embedding refresh settings
    enable_background_refresh: bool = True
    # Refresh embeddings every 12 hours by default
    background_refresh_interval: int = 43200
    # TTL for cached staff embeddings (controls on-demand refresh checks)
    staff_embeddings_cache_ttl: int = 43200


# codeql[py/should-be-context-manager]
class EmbeddingManager:
    """
    Manages face embeddings, search operations, and caching.

    CRITICAL INITIALIZATION FLOW:
    1. __init__() creates the manager but does NOT load embeddings or start background refresh
    2. External caller MUST call await _load_staff_embeddings() to load embeddings synchronously
    3. After successful load, caller SHOULD call start_background_refresh() for periodic updates
    4. The _embeddings_loaded flag tracks whether embeddings are ready for use
    5. All search operations check _embeddings_loaded before proceeding

    This design prevents race conditions where:
    - Background thread tries to load while main thread is loading
    - Search operations are called before embeddings are loaded
    - Multiple threads compete for the embeddings_lock during initialization

    Thread Safety:
    - _embeddings_lock protects embeddings_matrix and embedding_metadata
    - _cache_lock protects track_id_cache
    - _embeddings_loaded is set only after successful load under lock
    """

    def __init__(self, config: EmbeddingConfig, face_client: FacialRecognitionClient = None):
        self.config = config
        self.face_client = face_client
        self.logger = logging.getLogger(__name__)

        # Track ID cache for optimization - cache track IDs and their best results
        # Format: {track_id: {"result": search_result, "similarity_score": float, "timestamp": timestamp}}
        self.track_id_cache = {}

        # Staff embeddings cache for local similarity search
        self.staff_embeddings: List[StaffEmbedding] = []
        self.staff_embeddings_last_update = 0
        # Use configured TTL (default: 12 hours)
        self.staff_embeddings_cache_ttl = int(self.config.staff_embeddings_cache_ttl)

        # Numpy arrays for fast similarity computation
        self.embeddings_matrix = None
        self.embedding_metadata = []  # List of StaffEmbedding objects corresponding to matrix rows

        # Unknown faces cache - storing unknown embeddings locally
        self.unknown_faces_counter = 0

        # Thread safety
        self._cache_lock = threading.Lock()
        self._embeddings_lock = threading.Lock()

        # Background refresh thread
        self._refresh_thread = None
        self._is_running = False
        self._stop_event = threading.Event()

        # Initialization status flag
        self._embeddings_loaded = False

        # DON'T start background refresh yet - wait for initial load in initialize()
        # This prevents race conditions where background thread interferes with main init
        self.logger.info(
            f"EmbeddingManager created - background refresh will start after initial load (interval: {self.config.background_refresh_interval}s)"
        )

    def is_ready(self) -> bool:
        """
        Check if embeddings are loaded and ready for use.

        Held under _embeddings_lock so the (flag, matrix, metadata) tuple is
        observed atomically — preventing a torn read where the flag is True but
        the matrix has been swapped out by a concurrent reload.
        """
        with self._embeddings_lock:
            return (
                self._embeddings_loaded
                and self.embeddings_matrix is not None
                and len(self.embedding_metadata) > 0
            )

    def get_status(self) -> Dict[str, Any]:
        """
        Get detailed status of embedding manager for debugging and health checks.

        Returns:
            Dictionary with status information
        """
        with self._embeddings_lock:
            matrix_shape = self.embeddings_matrix.shape if self.embeddings_matrix is not None else None

        return {
            "embeddings_loaded": self._embeddings_loaded,
            "embeddings_count": len(self.staff_embeddings),
            "matrix_shape": matrix_shape,
            "metadata_count": len(self.embedding_metadata),
            "cache_size": len(self.track_id_cache),
            "last_update": self.staff_embeddings_last_update,
            "is_running": self._is_running,
            "is_ready": self.is_ready(),
        }

    def set_face_client(self, face_client: FacialRecognitionClient):
        """Set the face recognition client."""
        self.face_client = face_client

        # Start background refresh if it wasn't started yet
        if self.config.enable_background_refresh and not self._is_running:
            self.start_background_refresh()
            self.logger.info("Background embedding refresh started after setting face client")

    def start_background_refresh(self):
        """Start the background embedding refresh thread"""
        if not self._is_running and self.face_client:
            self._is_running = True
            self._stop_event.clear()
            self._refresh_thread = threading.Thread(
                target=self._run_refresh_loop,
                daemon=True,
                name="EmbeddingRefreshThread",
            )
            self._refresh_thread.start()
            self.logger.info("Started background embedding refresh thread")

    def stop_background_refresh(self):
        """Stop the background embedding refresh thread"""
        if self._is_running:
            self.logger.info("Stopping background embedding refresh thread...")
            self._is_running = False
            self._stop_event.set()
            if self._refresh_thread:
                self._refresh_thread.join(timeout=10.0)
                self.logger.info("Background embedding refresh thread stopped")

    def _run_refresh_loop(self):
        """Run the embedding refresh loop in background thread"""
        import asyncio

        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Run initial load
            self.logger.info("Loading initial staff embeddings in background thread...")
            loop.run_until_complete(self._load_staff_embeddings())

            # Periodic refresh loop
            while self._is_running and not self._stop_event.is_set():
                try:
                    # Wait for refresh interval with ability to stop
                    if self._stop_event.wait(timeout=self.config.background_refresh_interval):
                        # Stop event was set
                        break

                    if not self._is_running:
                        break

                    # Refresh embeddings
                    self.logger.info("Refreshing staff embeddings from server...")
                    success = loop.run_until_complete(self._load_staff_embeddings())

                    if success:
                        self.logger.info("Successfully refreshed staff embeddings in background")
                    else:
                        self.logger.warning("Failed to refresh staff embeddings in background")

                except Exception as e:
                    self.logger.error(
                        f"Error in background embedding refresh loop: {e}",
                        exc_info=True,
                    )
                    # Continue loop even on error
                    time.sleep(60)  # Wait 1 minute before retry on error

        except Exception as e:
            self.logger.error(f"Fatal error in background refresh thread: {e}", exc_info=True)
        finally:
            try:
                loop.close()
            except Exception:
                # Non-fatal: exception ignored here; execution continues per surrounding logic.
                pass
            self.logger.info("Background embedding refresh loop ended")

    async def _load_staff_embeddings(self) -> bool:
        """Load all staff embeddings from API and cache them."""
        if not self.face_client:
            self.logger.error("Face client not available for loading staff embeddings")
            print("ERROR: Face client not available for loading staff embeddings")
            return False

        try:
            # self.logger.info("Loading staff embeddings from API...")
            # print("=============== LOADING STAFF EMBEDDINGS FROM API ===============")
            response = await self.face_client.get_all_staff_embeddings()
            # print(f"API RESPONSE TYPE: {type(response)}, IS_LIST: {isinstance(response, list)}, LEN: {len(response) if isinstance(response, list) else 'N/A'}")

            # Robust response handling: accept dict with data or raw list
            embeddings_data: List[Dict[str, Any]] = []
            if isinstance(response, dict):
                # Typical: { success: True, data: [...] }
                if response.get("success", False) and isinstance(response.get("data"), list):
                    embeddings_data = response.get("data", [])
                # Alternate: { data: [...] } without success flag
                elif isinstance(response.get("data"), list):
                    embeddings_data = response.get("data", [])
                # Fallback keys sometimes used
                elif isinstance(response.get("items"), list):
                    embeddings_data = response.get("items", [])
                else:
                    self.logger.error(f"Unexpected embeddings response shape (dict): keys={list(response.keys())}")
                    return False
            elif isinstance(response, list):
                # Some deployments return raw list directly
                embeddings_data = response
            else:
                self.logger.error(f"Unexpected embeddings response type: {type(response)}")
                return False

            self.staff_embeddings = []
            embeddings_list = []
            expected_dim: Optional[int] = None
            dims_observed: List[int] = []
            mismatch_examples: List[Tuple[str, int]] = []  # (staffId, dim)

            for item in embeddings_data:
                # Skip inactive if provided
                if isinstance(item, dict) and item.get("isActive") is False:
                    continue

                raw_emb = []
                try:
                    raw_emb = item.get("embedding", []) if isinstance(item, dict) else []
                except Exception:
                    raw_emb = []
                # Record observed dimension for debugging
                try:
                    dims_observed.append(len(raw_emb) if isinstance(raw_emb, list) else 0)
                except Exception:
                    dims_observed.append(0)

                # Validate and coerce embedding list
                if not isinstance(raw_emb, list) or len(raw_emb) == 0:
                    continue
                try:
                    # Ensure numeric float32 list
                    clean_emb = [float(v) for v in raw_emb]
                except Exception:
                    continue

                # Dimension consistency
                if expected_dim is None:
                    expected_dim = len(clean_emb)
                if len(clean_emb) != expected_dim:
                    # Collect a few examples to aid debugging
                    try:
                        mismatch_examples.append((str(item.get("staffId", "")), len(clean_emb)))
                    except Exception:
                        mismatch_examples.append(("", len(clean_emb)))
                    self.logger.warning(
                        f"Skipping embedding with mismatched dimension: got {len(clean_emb)} expected {expected_dim}"
                    )
                    continue

                staff_embedding = StaffEmbedding(
                    embedding_id=(item.get("embeddingId", "") if isinstance(item, dict) else ""),
                    staff_id=(item.get("staffId", "") if isinstance(item, dict) else ""),
                    embedding=clean_emb,
                    employee_id=str(item.get("employeeId", "")) if isinstance(item, dict) else "",
                    staff_details=(item.get("staffDetails", {}) if isinstance(item, dict) else {}),
                    is_active=(item.get("isActive", True) if isinstance(item, dict) else True),
                )

                self.staff_embeddings.append(staff_embedding)
                embeddings_list.append(clean_emb)

            # Create numpy matrix for fast similarity computation (thread-safe)
            with self._embeddings_lock:
                if embeddings_list:
                    self.embeddings_matrix = np.array(embeddings_list, dtype=np.float32)
                    # Normalize embeddings for cosine similarity
                    norms = np.linalg.norm(self.embeddings_matrix, axis=1, keepdims=True)
                    norms[norms == 0] = 1  # Avoid division by zero
                    self.embeddings_matrix = self.embeddings_matrix / norms

                    self.embedding_metadata = self.staff_embeddings.copy()
                    self.staff_embeddings_last_update = time.time()
                    self._embeddings_loaded = True  # Mark as successfully loaded

                    self.logger.info(
                        f"Successfully loaded and cached {len(self.staff_embeddings)} staff embeddings (dim={self.embeddings_matrix.shape[1]})"
                    )
                    # print(f"=============== SUCCESS: LOADED {len(self.staff_embeddings)} EMBEDDINGS, MATRIX SHAPE: {self.embeddings_matrix.shape} ===============")
                    return True
                else:
                    # Build diagnostics and raise to stop pipeline early with actionable info
                    dims_summary: Dict[int, int] = {}
                    for d in dims_observed:
                        dims_summary[d] = dims_summary.get(d, 0) + 1
                    error_msg = (
                        f"No valid staff embeddings loaded. Observed dimension distribution: {dims_summary}. "
                        f"Expected_dim={expected_dim}. Mismatch examples (staffId, dim): {mismatch_examples[:5]}"
                    )
                    self.logger.error(error_msg)
                    print("=============== ERROR: NO VALID EMBEDDINGS ===============")
                    print(f"ERROR: {error_msg}")
                    print("=============== STOPPING PIPELINE ===============")
                    raise RuntimeError(
                        f"Failed to load staff embeddings due to dimension mismatch. Observed dims: {dims_summary}"
                    )

        except Exception as e:
            self.logger.error(f"Error loading staff embeddings: {e}", exc_info=True)
            return False

    def _should_refresh_embeddings(self) -> bool:
        """Check if staff embeddings should be refreshed."""
        current_time = time.time()
        return (current_time - self.staff_embeddings_last_update) > self.staff_embeddings_cache_ttl

    def _add_embedding_to_local_cache(self, staff_embedding: StaffEmbedding):
        """Add a new embedding to the local cache and update the matrix."""
        try:
            if not staff_embedding.embedding:
                return

            # Add to staff_embeddings list
            self.staff_embeddings.append(staff_embedding)
            self.embedding_metadata.append(staff_embedding)

            # Update the embeddings matrix
            new_embedding = np.array([staff_embedding.embedding], dtype=np.float32)
            # Normalize the new embedding
            norm = np.linalg.norm(new_embedding)
            if norm > 0:
                new_embedding = new_embedding / norm

            if self.embeddings_matrix is None:
                self.embeddings_matrix = new_embedding
            else:
                self.embeddings_matrix = np.vstack([self.embeddings_matrix, new_embedding])

            self.logger.debug(f"Added embedding for {staff_embedding.staff_id} to local cache")

        except Exception as e:
            self.logger.error(f"Error adding embedding to local cache: {e}", exc_info=True)

    def _find_best_local_match(self, query_embedding: List[float]) -> Optional[Tuple[StaffEmbedding, float]]:
        """Find best matching staff member using optimized matrix operations (thread-safe)."""
        # Check if embeddings are loaded at all
        if not self._embeddings_loaded:
            # print(f"ERROR: _find_best_local_match called but embeddings not loaded yet (_embeddings_loaded={self._embeddings_loaded})")
            self.logger.error("Embeddings not loaded - _find_best_local_match cannot proceed")
            return None

        with self._embeddings_lock:
            if self.embeddings_matrix is None or len(self.embedding_metadata) == 0:
                # print(f"ERROR: _find_best_local_match - embeddings_matrix is None={self.embeddings_matrix is None}, metadata_len={len(self.embedding_metadata)}, _embeddings_loaded={self._embeddings_loaded}")
                self.logger.error(f"Embeddings matrix is None despite _embeddings_loaded={self._embeddings_loaded}")
                return None

            # Create local copies to avoid issues with concurrent modifications
            embeddings_matrix = self.embeddings_matrix.copy() if self.embeddings_matrix is not None else None
            embedding_metadata = self.embedding_metadata.copy()

        if embeddings_matrix is None:
            print("ERROR: _find_best_local_match - embeddings_matrix copy is None")
            return None

        try:
            query_array = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
            # Dimension check
            if embeddings_matrix.shape[1] != query_array.shape[1]:
                self.logger.warning(
                    f"Query embedding dim mismatch: query={query_array.shape[1]} staff={embeddings_matrix.shape[1]}"
                )
                print(f"ERROR: DIMENSION MISMATCH - query={query_array.shape[1]} staff={embeddings_matrix.shape[1]}")
                return None

            # Normalize query embedding
            query_norm = np.linalg.norm(query_array)
            if query_norm == 0:
                return None
            query_array = query_array / query_norm

            # Compute cosine similarities using matrix multiplication (much faster)
            similarities = np.dot(embeddings_matrix, query_array.T).flatten()

            # Find the best match
            best_idx = np.argmax(similarities)
            best_similarity = similarities[best_idx]

            # Check if similarity meets threshold
            if best_similarity >= self.config.similarity_threshold:
                best_staff_embedding = embedding_metadata[best_idx]
                return best_staff_embedding, float(best_similarity)

            return None

        except Exception as e:
            self.logger.error(f"Error in local similarity search: {e}", exc_info=True)
            return None

    def get_best_similarity(self, query_embedding: List[float]) -> float:
        """Return the best cosine similarity for debugging/observability (no threshold gating)."""
        with self._embeddings_lock:
            if self.embeddings_matrix is None or len(self.embedding_metadata) == 0:
                return 0.0
            embeddings_matrix = self.embeddings_matrix.copy() if self.embeddings_matrix is not None else None
        if embeddings_matrix is None:
            return 0.0
        try:
            query_array = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
            if embeddings_matrix.shape[1] != query_array.shape[1]:
                print(
                    f"ERROR: get_best_similarity DIMENSION MISMATCH - query={query_array.shape[1]} staff={embeddings_matrix.shape[1]}"
                )
                return 0.0
            qn = np.linalg.norm(query_array)
            if qn == 0:
                return 0.0
            query_array = query_array / qn
            similarities = np.dot(embeddings_matrix, query_array.T).flatten()
            return float(np.max(similarities)) if similarities.size > 0 else 0.0
        except Exception:
            return 0.0

    def extract_embedding_from_detection(self, detection: Dict) -> Tuple[Dict, Optional[List[float]]]:
        """Extract and validate embedding from detection."""
        embedding = detection.get("embedding", [])

        # Validate embedding format and dimensions
        if not embedding:
            self.logger.warning(f"Missing embedding in detection: {detection.get('track_id', 'unknown')}")
            return detection, None

        if not isinstance(embedding, list):
            self.logger.warning(
                f"Invalid embedding type {type(embedding)} in detection: {detection.get('track_id', 'unknown')}"
            )
            return detection, None

        if len(embedding) == 0:
            self.logger.warning(f"Empty embedding in detection: {detection.get('track_id', 'unknown')}")
            return detection, None

        # Additional validation for embedding values
        try:
            # Check if all embedding values are numeric
            if not all(isinstance(val, (int, float)) for val in embedding):
                self.logger.warning(
                    f"Non-numeric values in embedding for detection: {detection.get('track_id', 'unknown')}"
                )
                return detection, None
        except Exception as e:
            self.logger.warning(
                f"Error validating embedding values for detection {detection.get('track_id', 'unknown')}: {e}"
            )
            return detection, None

        return detection, embedding

    def _check_track_id_cache(self, track_id: str) -> Optional[SearchResult]:
        """
        Check if a track_id exists in cache and return the best result.
        Returns cached SearchResult if found, None otherwise.
        """
        if not self.config.enable_track_id_cache or not track_id:
            return None

        try:
            with self._cache_lock:
                current_time = time.time()

                # Clean expired entries
                expired_keys = [
                    key
                    for key, data in self.track_id_cache.items()
                    if current_time - data["timestamp"] > self.config.cache_ttl
                ]
                for key in expired_keys:
                    del self.track_id_cache[key]

                # Check for existing track_id
                if track_id in self.track_id_cache:
                    cached_data = self.track_id_cache[track_id]
                    self.logger.debug(
                        f"Found cached result for track_id: {track_id} with similarity: {cached_data['similarity_score']:.3f}"
                    )
                    return cached_data["result"]

                return None
        except Exception as e:
            self.logger.warning(f"Error checking track_id cache: {e}")
            return None

    def _update_track_id_cache(self, track_id: str, search_result: SearchResult):
        """
        Update track_id cache with new result.
        Note: Similarity comparison is now handled in the search method.
        """
        if not self.config.enable_track_id_cache or not track_id:
            return

        try:
            with self._cache_lock:
                current_time = time.time()
                similarity_score = search_result.similarity_score

                # Manage cache size
                if len(self.track_id_cache) >= self.config.cache_max_size:
                    # Remove oldest entries (simple FIFO)
                    oldest_key = min(
                        self.track_id_cache.keys(),
                        key=lambda k: self.track_id_cache[k]["timestamp"],
                    )
                    del self.track_id_cache[oldest_key]

                # Update cache entry
                self.track_id_cache[track_id] = {
                    "result": search_result,
                    "similarity_score": similarity_score,
                    "timestamp": current_time,
                }

                self.logger.debug(f"Updated cache for track_id {track_id} with similarity {similarity_score:.3f}")

        except Exception as e:
            self.logger.warning(f"Error updating track_id cache: {e}")

    def _create_unknown_face_local(self, _embedding: List[float], _track_id: str = None) -> SearchResult:
        """Unknown face creation disabled - returns None"""
        _ = (_embedding, _track_id)
        return None

    async def search_face_embedding(
        self,
        embedding: List[float],
        track_id: str = None,
        _location: str = "",
        _timestamp: str = "",
    ) -> Optional[SearchResult]:
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
        _ = (_location, _timestamp)
        if not self.face_client:
            self.logger.error("Face client not available for embedding search")
            return None

        # Refresh staff embeddings if needed
        if self._should_refresh_embeddings() or self.embeddings_matrix is None:
            self.logger.debug("Staff embeddings cache expired or empty, refreshing...")
            await self._load_staff_embeddings()

        # Always perform similarity search first
        local_match = self._find_best_local_match(embedding)
        current_search_result = None

        if local_match:
            staff_embedding, similarity_score = local_match
            self.logger.info(
                f"Local embedding match found - staff_id={staff_embedding.staff_id}, similarity={similarity_score:.3f}, employee_id={staff_embedding.employee_id}"
            )
            self.logger.debug(f"Match details: staff_details={staff_embedding.staff_details}")

            current_search_result = SearchResult(
                employee_id=staff_embedding.employee_id,
                staff_id=staff_embedding.staff_id,
                detection_type="known",
                staff_details=staff_embedding.staff_details,
                person_name=self._extract_person_name(staff_embedding.staff_details),
                similarity_score=similarity_score,
            )
        else:
            # Create unknown face entry (thread-safe counter)
            with self._cache_lock:
                self.unknown_faces_counter += 1
                counter_value = self.unknown_faces_counter
            employee_id = f"unknown_{int(time.time())}_{counter_value}"
            staff_id = track_id if track_id else f"unknown_{counter_value}"

            self.logger.info(
                f"No local match found - creating unknown face entry: employee_id={employee_id}, track_id={track_id}"
            )

            current_search_result = SearchResult(
                employee_id=employee_id,
                staff_id=staff_id,
                detection_type="unknown",
                staff_details={"name": f"Unknown {track_id}"},
                person_name=f"Unknown {track_id}",
                similarity_score=0.0,
            )

        # Check cache and compare similarities (if caching enabled and track_id available)
        # BUT: For unknown faces, always re-check to allow for potential identification
        if self.config.enable_track_id_cache and track_id:
            cached_result = self._check_track_id_cache(track_id)

            # If current result is unknown, never cache it — every frame should
            # re-attempt identification. The "upgrade unknown -> known" path
            # below is the only way an unknown becomes cached.
            if current_search_result.detection_type == "unknown":
                self.logger.debug(
                    f"Unknown face with track_id={track_id} - not caching, will re-check for potential identification"
                )
                return current_search_result

            if cached_result:
                cached_similarity = cached_result.similarity_score
                current_similarity = current_search_result.similarity_score

                # If cached result was unknown but current is known, always use current (upgrade)
                if cached_result.detection_type == "unknown" and current_search_result.detection_type == "known":
                    self.logger.info(
                        f"Upgrading unknown face to known for track_id: {track_id} - similarity: {current_similarity:.3f}"
                    )
                    self._update_track_id_cache(track_id, current_search_result)
                    return current_search_result
                elif current_similarity > cached_similarity:
                    # New result is better - update cache and return new result
                    self.logger.debug(
                        f"New similarity {current_similarity:.3f} > cached {cached_similarity:.3f} for track_id: {track_id} - updating cache"
                    )
                    self._update_track_id_cache(track_id, current_search_result)
                    return current_search_result
                else:
                    # Cached result is better or equal - keep cache and return cached result
                    self.logger.debug(
                        f"Cached similarity {cached_similarity:.3f} >= new {current_similarity:.3f} for track_id: {track_id} - using cached result"
                    )
                    return cached_result
            else:
                # No cached result - add to cache and return current result (only for known faces)
                if current_search_result.detection_type == "known":
                    self.logger.debug(f"No cached result for track_id: {track_id} - adding known face to cache")
                    self._update_track_id_cache(track_id, current_search_result)
                return current_search_result

        # If caching is disabled, just return the current result
        return current_search_result

    def _extract_person_name(self, staff_details: Dict[str, Any]) -> str:
        """Extract person name from staff details."""
        return str(
            staff_details.get(
                "name",
                staff_details.get("firstName", "Unknown") + " " + staff_details.get("lastName", "Unknown"),
            )
        )

    def _parse_api_result_to_search_result(self, api_result: Dict) -> SearchResult:
        """Parse API result to SearchResult."""
        employee_id = api_result["_id"]
        staff_id = api_result["staffId"]
        detection_type = api_result["detectionType"]
        staff_details = api_result["staffDetails"]

        person_name = "Unknown"
        if detection_type == "known":
            person_name = self._extract_person_name(staff_details)
        elif detection_type == "unknown":
            person_name = "Unknown"

        return SearchResult(
            employee_id=employee_id,
            staff_id=staff_id,
            detection_type=detection_type,
            staff_details=staff_details,
            person_name=person_name,
            similarity_score=api_result.get("score", 0.0),
        )

    async def _enroll_unknown_face(
        self,
        _embedding: List[float],
        _location: str = "",
        _timestamp: str = "",
        _track_id: str = None,
    ) -> Optional[SearchResult]:
        """Enroll unknown face — currently a no-op (remote enrollment disabled)."""
        _ = (_embedding, _location, _timestamp, _track_id)
        return None

    def update_detection_with_search_result(self, search_result: SearchResult, detection: Dict) -> Dict:
        """Update detection object with search result data."""
        detection = detection.copy()  # Create a copy to avoid modifying original

        detection["person_id"] = search_result.staff_id
        detection["person_name"] = search_result.person_name
        detection["recognition_status"] = search_result.detection_type
        detection["employee_id"] = search_result.employee_id
        detection["staff_details"] = search_result.staff_details
        detection["similarity_score"] = search_result.similarity_score

        if search_result.detection_type == "known":
            detection["enrolled"] = True
            detection["category"] = f"{search_result.person_name.replace(' ', '_')}_{search_result.staff_id}"
        elif search_result.detection_type == "unknown":
            detection["enrolled"] = False
            detection["category"] = "unrecognized"
        else:
            self.logger.warning(f"Unknown detection type: {search_result.detection_type}")
            return None

        return detection

    def __enter__(self) -> "EmbeddingManager":
        return self

    def __exit__(self, _exc_type: Any, _exc: Any, _tb: Any) -> None:
        return None

    def __del__(self):
        """Cleanup when object is destroyed"""
        try:
            self.stop_background_refresh()
        except Exception:
            # Non-fatal: exception ignored here; execution continues per surrounding logic.
            pass
