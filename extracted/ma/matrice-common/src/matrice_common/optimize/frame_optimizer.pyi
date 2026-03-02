"""Auto-generated stub for module: frame_optimizer."""
from typing import Any, Dict, Optional, Set, Tuple

# Constants
DEFAULT_ALPHA: float
DEFAULT_ALWAYS_CHECK_FIRST_N: int
DEFAULT_BG_UPDATE_INTERVAL: int
DEFAULT_DIFF_THRESHOLD: int
DEFAULT_MAX_STREAMS: int
DEFAULT_SAMPLE_INTERVAL: Any
DEFAULT_SCALE: float
DEFAULT_SIMILARITY_THRESHOLD: float
FRAME_OPTIMIZER_SAMPLE_INTERVAL: Any

# Classes
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

class StreamState:
    # Per-stream state for background tracking.

    def reset(self: Any) -> None:
        """
        Reset state to initial values.
        """
        ...

