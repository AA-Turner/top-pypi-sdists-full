"""
Fast frame difference detector for skipping similar frames.

Uses adaptive background model with:
- Aggressive downscaling (0.4x) for speed
- No Gaussian blur (saves CPU)
- Integer background (uint8, no float32)
- Background update every N frames
- Direct ratio computation (no mask generation)

Memory footprint: ~100KB per camera at 0.4x scale (720p -> 288p grayscale)
"""

import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple, Any

import cv2
import numpy as np


import os

# Environment variable for sampling interval (Phase 4)
FRAME_OPTIMIZER_SAMPLE_INTERVAL = int(os.getenv("FRAME_OPTIMIZER_SAMPLE_INTERVAL", "5"))

# Default configuration constants (moved outside class to avoid forward reference issues)
DEFAULT_SCALE = 0.4  # Downscale factor (0.4 = 40% of original)
DEFAULT_ALPHA = 0.05  # Background update weight (lower = slower adaptation)
DEFAULT_DIFF_THRESHOLD = 15  # Pixel difference threshold (0-255)
DEFAULT_SIMILARITY_THRESHOLD = 0.05  # Max motion ratio to consider "similar" (5%)
DEFAULT_BG_UPDATE_INTERVAL = 3  # Update background every N frames
DEFAULT_MAX_STREAMS = 10000  # Max streams to track (memory limit)
# Sampling defaults (Phase 4)
DEFAULT_SAMPLE_INTERVAL = FRAME_OPTIMIZER_SAMPLE_INTERVAL  # Check every N frames
DEFAULT_ALWAYS_CHECK_FIRST_N = 3  # Always check first N frames for background init


@dataclass
class StreamState:
    """Per-stream state for background tracking."""

    background: Optional[np.ndarray] = None
    frame_count: int = 0
    last_update_time: float = field(default_factory=time.time)
    last_motion_ratio: float = 0.0
    last_frame_id: Optional[str] = None
    # Sampling state (Phase 4)
    optimizer_frame_count: int = 0  # Separate counter for sampling
    last_was_similar: bool = False  # Cached result for non-sampled frames
    cached_motion_ratio: float = 0.0  # Cached score for non-sampled frames

    def reset(self) -> None:
        """Reset state to initial values."""
        self.background = None
        self.frame_count = 0
        self.last_update_time = time.time()
        self.last_motion_ratio = 0.0
        self.last_frame_id = None
        self.optimizer_frame_count = 0
        self.last_was_similar = False
        self.cached_motion_ratio = 0.0


class FrameOptimizer:
    """
    Fast frame difference detector for skipping similar frames.

    Designed for high-throughput streaming pipelines where we want to:
    - Skip encoding/sending frames that are similar to previous frames
    - Reduce CPU usage on streaming gateway
    - Reduce network bandwidth
    - Enable server-side result caching

    Thread-safe for use from multiple workers.

    Usage:
        optimizer = FrameOptimizer()

        # In streaming loop:
        is_similar, score = optimizer.is_similar(frame, stream_key)
        if is_similar:
            # Skip encoding, send reference to previous frame
            reference_frame_id = optimizer.get_last_frame_id(stream_key)
        else:
            # Normal encoding and send
            optimizer.set_last_frame_id(stream_key, new_frame_id)
    """

    def __init__(
        self,
        scale: float = DEFAULT_SCALE,
        alpha: float = DEFAULT_ALPHA,
        diff_threshold: int = DEFAULT_DIFF_THRESHOLD,
        similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
        bg_update_interval: int = DEFAULT_BG_UPDATE_INTERVAL,
        max_streams: int = DEFAULT_MAX_STREAMS,
        enabled: bool = True,
        # Sampling parameters (Phase 4 - 80% CPU savings)
        sample_interval: int = DEFAULT_SAMPLE_INTERVAL,
        always_check_first_n: int = DEFAULT_ALWAYS_CHECK_FIRST_N,
    ):
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
        self.scale = max(0.1, min(1.0, scale))
        self.alpha = max(0.01, min(0.5, alpha))
        self.diff_threshold = max(1, min(100, diff_threshold))
        self.similarity_threshold = max(0.01, min(0.5, similarity_threshold))
        self.bg_update_interval = max(1, bg_update_interval)
        self.max_streams = max(100, max_streams)
        self.enabled = enabled
        # Sampling configuration (Phase 4)
        self.sample_interval = max(1, sample_interval)
        self.always_check_first_n = max(1, always_check_first_n)

        # Per-stream state
        self._streams: Dict[str, StreamState] = {}
        self._lock = threading.RLock()

        # Metrics
        self._metrics: Dict[str, Any] = {
            "frames_processed": 0,
            "frames_similar": 0,
            "frames_different": 0,
            "cache_evictions": 0,
        }
        self._metrics_lock = threading.Lock()

        self.logger = logging.getLogger(f"{__name__}.FrameOptimizer")

    def is_similar(self, frame: np.ndarray, stream_key: str) -> Tuple[bool, float]:
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
        if not self.enabled:
            return False, 1.0

        if frame is None or frame.size == 0:
            return False, 1.0

        try:
            # LOCK: Get state and check sampling
            with self._lock:
                state = self._get_or_create_state(stream_key)
                state.optimizer_frame_count += 1

                # ================================================================
                # SAMPLING OPTIMIZATION (Phase 4)
                # ================================================================
                # Always check first N frames for background initialization
                # After that, only check every sample_interval frames
                should_sample = (
                    state.optimizer_frame_count <= self.always_check_first_n or
                    state.optimizer_frame_count % self.sample_interval == 0
                )

                if not should_sample:
                    # Return cached result without expensive computation
                    self._update_metrics("frames_similar" if state.last_was_similar else "frames_different")
                    return state.last_was_similar, state.cached_motion_ratio

            # Preprocess frame (downscale + grayscale) - NO LOCK NEEDED
            processed = self._preprocess_frame(frame)

            # LOCK 1: Get state and check if initialization needed
            with self._lock:
                state = self._get_or_create_state(stream_key)

                # First frame - initialize background
                if state.background is None:
                    state.background = processed.copy()
                    state.frame_count = 1
                    state.last_was_similar = False
                    state.cached_motion_ratio = 1.0
                    self._update_metrics("frames_different")
                    return False, 1.0

                # Get a copy of background for comparison OUTSIDE the lock
                background_copy = state.background.copy()
                state.frame_count += 1
                should_update = state.frame_count % self.bg_update_interval == 0

            # Compute motion ratio WITHOUT lock (CPU intensive operation)
            motion_ratio = self._compute_motion_ratio(processed, background_copy)

            # LOCK 2: Update background if needed
            if should_update:
                with self._lock:
                    # Re-fetch state in case it changed
                    retrieved_state = self._streams.get(stream_key)
                    if retrieved_state is not None and retrieved_state.background is not None:
                        state = retrieved_state
                        # Accumulate weighted average
                        assert state.background is not None  # Type safety for mypyc
                        processed_float: np.ndarray = processed.astype(np.float32)
                        background_float: np.ndarray = state.background.astype(np.float32)
                        cv2.accumulateWeighted(processed_float, background_float, self.alpha)
                        # Keep as uint8 for memory efficiency
                        state.background = background_float.astype(np.uint8)
                        state.last_motion_ratio = motion_ratio

            # Determine if similar
            is_similar = motion_ratio < self.similarity_threshold

            # Cache result for non-sampled frames (Phase 4)
            with self._lock:
                retrieved_state = self._streams.get(stream_key)
                if retrieved_state is not None:
                    state = retrieved_state
                    state.last_was_similar = is_similar
                    state.cached_motion_ratio = motion_ratio

            # Update metrics (has its own lock)
            if is_similar:
                self._update_metrics("frames_similar")
            else:
                self._update_metrics("frames_different")

            return is_similar, motion_ratio

        except Exception as e:
            self.logger.error(f"Error in is_similar for stream={stream_key}: {e}")
            return False, 1.0

    def _preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """Downscale and convert to grayscale for fast comparison."""
        # Convert to grayscale if needed
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame

        # Downscale for speed
        if self.scale < 1.0:
            h, w = gray.shape[:2]
            new_h = int(h * self.scale)
            new_w = int(w * self.scale)
            gray = cv2.resize(gray, (new_w, new_h), interpolation=cv2.INTER_AREA)

        return gray

    def _compute_motion_ratio(self, current: np.ndarray, background: np.ndarray) -> float:
        """
        Compute motion ratio between current frame and background.

        Returns:
            Motion ratio (0.0-1.0), where 0 means identical
        """
        # Absolute difference
        diff = cv2.absdiff(current, background)

        # Threshold to get motion pixels
        motion_pixels: int = np.sum(diff > self.diff_threshold)
        total_pixels: int = diff.size

        # Return motion ratio
        return motion_pixels / total_pixels if total_pixels > 0 else 0.0

    def get_motion_mask(
        self,
        frame: np.ndarray,
        stream_key: str,
        return_full_size: bool = False
    ) -> Tuple[Optional[np.ndarray], float]:
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
        if not self.enabled:
            return None, 1.0

        if frame is None or frame.size == 0:
            return None, 1.0

        try:
            # Preprocess frame (downscale + grayscale)
            processed = self._preprocess_frame(frame)

            # LOCK: Get state
            with self._lock:
                state = self._get_or_create_state(stream_key)

                # First frame - initialize background
                if state.background is None:
                    state.background = processed.copy()
                    state.frame_count = 1
                    self._update_metrics("frames_different")
                    return None, 1.0

                # Get background copy
                background_copy = state.background.copy()
                state.frame_count += 1
                should_update = state.frame_count % self.bg_update_interval == 0

            # Compute difference WITHOUT lock
            diff = cv2.absdiff(processed, background_copy)

            # Create binary motion mask
            motion_mask = (diff > self.diff_threshold).astype(np.uint8) * 255

            # Compute motion ratio
            motion_pixels: int = np.sum(motion_mask > 0)
            total_pixels: int = motion_mask.size
            motion_ratio = motion_pixels / total_pixels if total_pixels > 0 else 0.0

            # Update background if needed
            if should_update:
                with self._lock:
                    retrieved_state = self._streams.get(stream_key)
                    if retrieved_state is not None and retrieved_state.background is not None:
                        state = retrieved_state
                        assert state.background is not None  # Type safety for mypyc
                        processed_float: np.ndarray = processed.astype(np.float32)
                        background_float: np.ndarray = state.background.astype(np.float32)
                        cv2.accumulateWeighted(processed_float, background_float, self.alpha)
                        state.background = background_float.astype(np.uint8)
                        state.last_motion_ratio = motion_ratio

            # Upscale mask to original size if requested
            if return_full_size and self.scale < 1.0:
                frame_h, frame_w = frame.shape[:2]
                motion_mask = cv2.resize(
                    motion_mask,
                    (frame_w, frame_h),
                    interpolation=cv2.INTER_NEAREST
                )

            return motion_mask, motion_ratio

        except Exception as e:
            self.logger.error(f"Error in get_motion_mask for stream={stream_key}: {e}")
            return None, 1.0

    def check_frame_and_rois(
        self,
        frame: np.ndarray,
        stream_key: str,
    ) -> Tuple[bool, Optional[np.ndarray], float]:
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
        if not self.enabled:
            return False, None, 1.0

        # Get motion mask at full resolution
        motion_mask, motion_ratio = self.get_motion_mask(
            frame, stream_key, return_full_size=True
        )

        # Determine similarity
        is_similar = motion_ratio < self.similarity_threshold

        # Update metrics
        if is_similar:
            self._update_metrics("frames_similar")
        else:
            self._update_metrics("frames_different")

        return is_similar, motion_mask, motion_ratio

    def _get_or_create_state(self, stream_key: str) -> StreamState:
        """Get existing state or create new one for stream."""
        if stream_key not in self._streams:
            # Check if we need to evict old streams
            if len(self._streams) >= self.max_streams:
                self._evict_oldest_stream()

            self._streams[stream_key] = StreamState()

        return self._streams[stream_key]

    def _evict_oldest_stream(self) -> None:
        """Evict the oldest stream to make room for new ones."""
        if not self._streams:
            return

        # Find stream with oldest update time
        oldest_key = min(
            self._streams.keys(),
            key=lambda k: self._streams[k].last_update_time
        )

        del self._streams[oldest_key]

        with self._metrics_lock:
            self._metrics["cache_evictions"] += 1

        self.logger.debug(f"Evicted stream state for {oldest_key}")

    def get_last_frame_id(self, stream_key: str) -> Optional[str]:
        """
        Get the last frame_id that was successfully processed for a stream.

        Use this when is_similar() returns True to get the reference frame ID.

        Args:
            stream_key: Stream identifier

        Returns:
            Last frame_id or None if no frame has been processed
        """
        with self._lock:
            state = self._streams.get(stream_key)
            return state.last_frame_id if state else None

    def set_last_frame_id(self, stream_key: str, frame_id: str) -> None:
        """
        Set the last frame_id for a stream after successful processing.

        Call this after encoding/sending a full frame (not a reference).

        Args:
            stream_key: Stream identifier
            frame_id: The frame_id that was just processed
        """
        with self._lock:
            state = self._streams.get(stream_key)
            if state:
                state.last_frame_id = frame_id
                state.last_update_time = time.time()

    def reset(self, stream_key: Optional[str] = None) -> None:
        """
        Reset background model for a specific stream or all streams.

        Args:
            stream_key: Stream to reset, or None to reset all
        """
        with self._lock:
            if stream_key is None:
                self._streams.clear()
                self.logger.info("Reset all stream states")
            elif stream_key in self._streams:
                self._streams[stream_key].reset()
                self.logger.info(f"Reset stream state for {stream_key}")

    def remove_stream(self, stream_key: str) -> None:
        """
        Remove a stream's state completely.

        Call this when a camera is disconnected/removed.

        Args:
            stream_key: Stream to remove
        """
        with self._lock:
            if stream_key in self._streams:
                del self._streams[stream_key]
                self.logger.debug(f"Removed stream state for {stream_key}")

    def _update_metrics(self, metric_key: str) -> None:
        """Update metrics counter."""
        with self._metrics_lock:
            self._metrics["frames_processed"] += 1
            self._metrics[metric_key] += 1

    def get_metrics(self) -> Dict[str, Any]:
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
        with self._metrics_lock:
            metrics = dict(self._metrics)

        with self._lock:
            metrics["active_streams"] = len(self._streams)

        # Calculate similarity rate
        total = metrics.get("frames_processed", 0)
        similar = metrics.get("frames_similar", 0)
        metrics["similarity_rate"] = (similar / total * 100) if total > 0 else 0.0

        # Add config
        metrics["config"] = {
            "enabled": self.enabled,
            "scale": self.scale,
            "diff_threshold": self.diff_threshold,
            "similarity_threshold": self.similarity_threshold,
            "bg_update_interval": self.bg_update_interval,
        }

        return metrics

    def get_stream_info(self, stream_key: str) -> Optional[Dict]:
        """
        Get info about a specific stream's state.

        Args:
            stream_key: Stream to get info for

        Returns:
            Dict with stream info or None if not found
        """
        with self._lock:
            state = self._streams.get(stream_key)
            if not state:
                return None

            return {
                "stream_key": stream_key,
                "frame_count": state.frame_count,
                "last_motion_ratio": state.last_motion_ratio,
                "last_frame_id": state.last_frame_id,
                "last_update_time": state.last_update_time,
                "has_background": state.background is not None,
            }
