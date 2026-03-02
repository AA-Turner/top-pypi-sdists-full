"""Stub file for optimize directory."""
from typing import Any, Dict, List, Optional, Set, Tuple

# Constants
DEFAULT_ALPHA: float = ...  # From frame_optimizer
DEFAULT_ALWAYS_CHECK_FIRST_N: int = ...  # From frame_optimizer
DEFAULT_BG_UPDATE_INTERVAL: int = ...  # From frame_optimizer
DEFAULT_DIFF_THRESHOLD: int = ...  # From frame_optimizer
DEFAULT_MAX_STREAMS: int = ...  # From frame_optimizer
DEFAULT_SAMPLE_INTERVAL: Any = ...  # From frame_optimizer
DEFAULT_SCALE: float = ...  # From frame_optimizer
DEFAULT_SIMILARITY_THRESHOLD: float = ...  # From frame_optimizer
FRAME_OPTIMIZER_SAMPLE_INTERVAL: Any = ...  # From frame_optimizer
DEFAULT_CLEANUP_INTERVAL: int = ...  # From result_cache
DEFAULT_MAX_SIZE: int = ...  # From result_cache
DEFAULT_TTL_SECONDS: int = ...  # From result_cache

# Classes
# From frame_optimizer
class FrameOptimizer:
    # Fast frame difference detector for skipping similar frames.
    #
    # Designed for high-throughput streaming pipelines where we want to:
    # - Skip encoding/sending frames that are similar to previous frames
    # - Reduce CPU usage on streaming gateway
    # - Reduce network bandwidth
    # - Enable server-side result caching
    #
    # Thread-safe for use from multiple workers.
    #
    # Usage:
    #     optimizer = FrameOptimizer()
    #
    #     # In streaming loop:
    #     is_similar, score = optimizer.is_similar(frame, stream_key)
    #     if is_similar:
    #         # Skip encoding, send reference to previous frame
    #         reference_frame_id = optimizer.get_last_frame_id(stream_key)
    #     else:
    #         # Normal encoding and send
    #         optimizer.set_last_frame_id(stream_key, new_frame_id)

    def __init__(self: Any, scale: float = DEFAULT_SCALE, alpha: float = DEFAULT_ALPHA, diff_threshold: int = DEFAULT_DIFF_THRESHOLD, similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD, bg_update_interval: int = DEFAULT_BG_UPDATE_INTERVAL, max_streams: int = DEFAULT_MAX_STREAMS, enabled: bool = True, sample_interval: int = DEFAULT_SAMPLE_INTERVAL, always_check_first_n: int = DEFAULT_ALWAYS_CHECK_FIRST_N) -> None:
        """
        Initialize FrameOptimizer.
        
        Args:
            scale: Downscale factor for faster processing (0.4 = 40%)
            alpha: Background update weight (0.0-1.0, lower = slower adaptation)
            diff_threshold: Pixel difference threshold (0-255)
            similarity_threshold: Motion ratio below which frames are "similar"
            bg_update_interval: Update background every N frames
            max_streams: Maximum number of streams to track
            enabled: If False, all frames are marked as "not similar"
            sample_interval: Run optimizer every N frames (1 = every frame, 5 = every 5th frame)
            always_check_first_n: Always check first N frames per stream for background initialization
        """
        ...

    def check_frame_and_rois(self: Any, frame: Any.Any, stream_key: str) -> Tuple[bool, Optional[Any.Any], float]:
        """
        Combined check for frame similarity and ROI extraction.
        
        This is a convenience method that combines is_similar() and get_motion_mask()
        for use in ROI-based differential streaming.
        
        Args:
            frame: BGR or grayscale frame (np.ndarray)
            stream_key: Unique identifier for this stream/camera
        
        Returns:
            Tuple of (is_similar, motion_mask, motion_ratio):
            - is_similar: True if frame should be skipped
            - motion_mask: Binary mask for ROI extraction (full size)
            - motion_ratio: 0.0-1.0, lower means more similar
        """
        ...

    def get_last_frame_id(self: Any, stream_key: str) -> Optional[str]:
        """
        Get the last frame_id that was successfully processed for a stream.
        
        Use this when is_similar() returns True to get the reference frame ID.
        
        Args:
            stream_key: Stream identifier
        
        Returns:
            Last frame_id or None if no frame has been processed
        """
        ...

    def get_metrics(self: Any) -> Dict[str, Any]:
        """
        Get optimizer metrics for monitoring.
        
        Returns:
            Dict with metrics including:
            - frames_processed: Total frames checked
            - frames_similar: Frames marked as similar
            - frames_different: Frames marked as different
            - similarity_rate: Percentage of frames skipped
            - active_streams: Number of active stream states
        """
        ...

    def get_motion_mask(self: Any, frame: Any.Any, stream_key: str, return_full_size: bool = False) -> Tuple[Optional[Any.Any], float]:
        """
        Get binary motion mask for ROI extraction.
        
        Similar to is_similar() but returns the motion mask instead of just a boolean.
        Used by ROI processor to identify regions of motion.
        
        Args:
            frame: BGR or grayscale frame (np.ndarray)
            stream_key: Unique identifier for this stream/camera
            return_full_size: If True, upscale mask to original frame size
        
        Returns:
            Tuple of (motion_mask, motion_ratio):
            - motion_mask: Binary mask (0=static, 255=motion) or None if first frame
            - motion_ratio: 0.0-1.0, lower means more similar
        """
        ...

    def get_stream_info(self: Any, stream_key: str) -> Optional[Dict]:
        """
        Get info about a specific stream's state.
        
        Args:
            stream_key: Stream to get info for
        
        Returns:
            Dict with stream info or None if not found
        """
        ...

    def is_similar(self: Any, frame: Any.Any, stream_key: str) -> Tuple[bool, float]:
        """
        Check if frame is similar to background model.
        
        Optimized for low latency - lock is only used for dict access,
        not for CPU-intensive operations like motion ratio computation.
        
        This is the main entry point for frame comparison. It:
        1. Downscales the frame for fast processing
        2. Converts to grayscale
        3. Compares against adaptive background (WITHOUT lock)
        4. Returns whether frame is similar + motion score
        
        Phase 4 Sampling Optimization:
        - Only runs full check every sample_interval frames (default: 5)
        - Returns cached result for non-sampled frames
        - Always checks first always_check_first_n frames for background init
        - Saves ~80% CPU when sample_interval=5
        
        Args:
            frame: BGR or grayscale frame (np.ndarray)
            stream_key: Unique identifier for this stream/camera
        
        Returns:
            Tuple of (is_similar, motion_ratio):
            - is_similar: True if frame should be skipped
            - motion_ratio: 0.0-1.0, lower means more similar
        """
        ...

    def remove_stream(self: Any, stream_key: str) -> None:
        """
        Remove a stream's state completely.
        
        Call this when a camera is disconnected/removed.
        
        Args:
            stream_key: Stream to remove
        """
        ...

    def reset(self: Any, stream_key: Optional[str] = None) -> None:
        """
        Reset background model for a specific stream or all streams.
        
        Args:
            stream_key: Stream to reset, or None to reset all
        """
        ...

    def set_last_frame_id(self: Any, stream_key: str, frame_id: str) -> None:
        """
        Set the last frame_id for a stream after successful processing.
        
        Call this after encoding/sending a full frame (not a reference).
        
        Args:
            stream_key: Stream identifier
            frame_id: The frame_id that was just processed
        """
        ...


# From frame_optimizer
class StreamState:
    # Per-stream state for background tracking.

    def reset(self: Any) -> None:
        """
        Reset state to initial values.
        """
        ...


# From result_cache
class CachedResult:
    # Container for cached inference result with metadata.

    def is_expired(self: Any, ttl_seconds: float) -> bool:
        """
        Check if this result has expired based on TTL.
        """
        ...

    def touch(self: Any) -> None:
        """
        Update access metadata (called on cache hit).
        """
        ...


# From result_cache
class InferenceResultCache:
    # Thread-safe LRU cache for inference results.
    #
    # Designed for high-throughput inference pipelines where:
    # - Similar frames use cached results instead of re-running inference
    # - Results are keyed by frame_id from streaming gateway
    # - Memory is bounded by max_size with LRU eviction
    # - Old entries expire after ttl_seconds
    #
    # Usage:
    #     cache = InferenceResultCache(max_size=50000, ttl_seconds=300)
    #
    #     # After inference:
    #     cache.put(frame_id, {"model_result": result, "metadata": meta})
    #
    #     # When receiving reference frame:
    #     cached = cache.get(reference_frame_id)
    #     if cached:
    #         # Use cached result
    #     else:
    #         # Cache miss - frame expired or was evicted

    def __init__(self: Any, max_size: int = DEFAULT_MAX_SIZE, ttl_seconds: float = DEFAULT_TTL_SECONDS, cleanup_interval: float = DEFAULT_CLEANUP_INTERVAL, enabled: bool = True) -> None:
        """
        Initialize InferenceResultCache.
        
        Args:
            max_size: Maximum number of cached results
            ttl_seconds: Time-to-live for cached results
            cleanup_interval: How often to clean up expired entries
            enabled: If False, cache operations are no-ops
        """
        ...

    def clear(self: Any) -> None:
        """
        Clear all cached results.
        """
        ...

    def get(self: Any, frame_id: str) -> Optional[Dict[str, Any]]:
        """
        Get cached result for a frame_id.
        
        Args:
            frame_id: Frame identifier to look up
        
        Returns:
            Cached result dict or None if not found/expired
        """
        ...

    def get_cache_info(self: Any, frame_id: str) -> Optional[Dict]:
        """
        Get detailed info about a cached entry.
        
        Args:
            frame_id: Frame to get info for
        
        Returns:
            Dict with cache entry info or None if not found
        """
        ...

    def get_metrics(self: Any) -> Dict[str, Any]:
        """
        Get cache metrics for monitoring.
        
        Returns:
            Dict with metrics including:
            - hits: Number of cache hits
            - misses: Number of cache misses
            - puts: Number of items cached
            - evictions: LRU evictions
            - expirations: TTL expirations
            - hit_rate: Cache hit percentage
            - size: Current cache size
        """
        ...

    def has(self: Any, frame_id: str) -> bool:
        """
        Check if frame_id has a valid (non-expired) cached result.
        
        Note: This does NOT update LRU order - use get() if you need the result.
        
        Args:
            frame_id: Frame identifier to check
        
        Returns:
            True if valid cached result exists
        """
        ...

    def put(self: Any, frame_id: str, result: Dict[str, Any]) -> bool:
        """
        Cache inference result for a frame_id.
        
        Args:
            frame_id: Unique frame identifier from streaming gateway
            result: Inference result to cache (should include model_result, metadata)
        
        Returns:
            True if cached successfully, False otherwise
        """
        ...

    def remove(self: Any, frame_id: str) -> bool:
        """
        Remove a specific entry from cache.
        
        Args:
            frame_id: Frame identifier to remove
        
        Returns:
            True if entry was removed, False if not found
        """
        ...


# From roi_processor
class ROI:
    # Region of Interest bounding box.

    def from_dict(cls: Any, data: Dict[str, Any]) -> 'Any':
        """
        Create ROI from dictionary.
        """
        ...

    def to_dict(self: Any) -> Dict[str, Any]:
        """
        Convert to dictionary for serialization.
        """
        ...


# From roi_processor
class ROIConfig:
    # Configuration for ROI processing.

    ...

# From roi_processor
class ROIProcessor:
    # Processor for extracting and reconstructing ROI regions.
    #
    # Thread-safe for use from multiple workers.
    #
    # Usage:
    #     # Sender side:
    #     processor = ROIProcessor(config)
    #     motion_mask = get_motion_mask(frame)
    #     rois = processor.extract_roi_regions(frame, motion_mask)
    #     patches = [processor.encode_roi_patch(frame, roi) for roi in rois]
    #
    #     # Receiver side:
    #     base_frame = get_cached_frame()
    #     reconstructed = processor.overlay_roi_patches(base_frame, patches)

    def __init__(self: Any, config: Optional[Any] = None) -> None:
        """
        Initialize ROI processor.
        
        Args:
            config: ROI configuration (uses defaults if None)
        """
        ...

    def clear_stream_state(self: Any, stream_key: str) -> Any:
        """
        Clear state for a stream (e.g., when camera disconnects).
        
        Args:
            stream_key: Stream identifier
        """
        ...

    def decode_roi_patch(self: Any, patch_data: Any) -> Optional[Any.Any]:
        """
        Decode ROI patch from bytes.
        
        Args:
            patch_data: Encoded patch bytes (JPEG)
        
        Returns:
            Decoded image as numpy array (BGR) or None if failed
        """
        ...

    def encode_roi_patch(self: Any, frame: Any.Any, roi: Any, quality: Optional[int] = None) -> Dict[str, Any]:
        """
        Extract and encode ROI patch from frame.
        
        Args:
            frame: Full frame image (BGR or grayscale)
            roi: ROI region to extract
            quality: JPEG quality (uses config default if None)
        
        Returns:
            Dictionary with patch data and metadata:
            {
                "x": int, "y": int, "width": int, "height": int,
                "patch_data": bytes,  # Encoded JPEG
                "patch_id": str,
                "encoding": "jpeg",
                "quality": int,
                "size_bytes": int
            }
        """
        ...

    def extract_roi_regions(self: Any, frame: Any.Any, motion_mask: Any.Any, stream_key: Optional[str] = None) -> List[Any]:
        """
        Extract ROI bounding boxes from motion mask.
        
        Uses contour detection to find regions of motion, merges nearby
        regions, and filters by minimum area.
        
        Args:
            frame: Full frame image (BGR or grayscale)
            motion_mask: Binary motion mask (0 = no motion, 255 = motion)
            stream_key: Optional stream identifier for state tracking
        
        Returns:
            List of ROI objects representing motion regions
        """
        ...

    def get_cached_frame(self: Any, stream_key: str) -> Optional[Any]:
        """
        Get cached full frame for reconstruction.
        
        Args:
            stream_key: Stream identifier
        
        Returns:
            Cached frame bytes or None if not found
        """
        ...

    def get_stats(self: Any, stream_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Get ROI processing statistics.
        
        Args:
            stream_key: Optional stream to get stats for (all streams if None)
        
        Returns:
            Dictionary with statistics
        """
        ...

    def overlay_roi_patches(self: Any, base_frame_bytes: Any, roi_patches: List[Dict[str, Any]]) -> Any:
        """
        Overlay ROI patches onto base frame and return encoded result.
        
        This is the reconstruction method used on the receiver side to rebuild
        full frames from differential ROI updates.
        
        Args:
            base_frame_bytes: Base frame bytes (JPEG encoded)
            roi_patches: List of ROI patch dictionaries from encode_roi_patch()
        
        Returns:
            Reconstructed frame bytes (JPEG encoded)
        """
        ...

    def record_full_sync(self: Any, stream_key: str, frame_id: str, frame_bytes: Optional[Any] = None) -> Any:
        """
        Record a full sync for tracking.
        
        Args:
            stream_key: Stream identifier
            frame_id: Frame identifier
            frame_bytes: Optional frame bytes to cache
        """
        ...

    def record_roi_update(self: Any, stream_key: str, frame_id: str) -> Any:
        """
        Record an ROI update for sync tracking.
        
        Args:
            stream_key: Stream identifier
            frame_id: Frame identifier
        """
        ...

    def should_send_full_sync(self: Any, stream_key: str) -> bool:
        """
        Check if full frame sync is needed for this stream.
        
        Args:
            stream_key: Stream identifier
        
        Returns:
            True if full sync should be sent
        """
        ...


# From roi_processor
class ROIState:
    # Per-stream state for ROI tracking.

    def needs_full_sync(self: Any, config: Any) -> bool:
        """
        Check if full sync is needed based on time and update count.
        """
        ...

    def reset_sync_state(self: Any) -> Any:
        """
        Reset sync counters after full sync.
        """
        ...


from . import frame_optimizer, result_cache, roi_processor