"""
ROI (Region of Interest) processor for differential streaming.

This module provides utilities for:
- Extracting ROI regions from motion masks
- Encoding/decoding ROI patches
- Overlaying ROI patches onto base frames
- Managing ROI configurations

Designed for bandwidth reduction in video streaming by sending only
changed regions instead of full frames.
"""

import logging
import time
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any

import cv2
import numpy as np


@dataclass
class ROI:
    """Region of Interest bounding box."""

    x: int  # Top-left X coordinate
    y: int  # Top-left Y coordinate
    width: int  # ROI width
    height: int  # ROI height
    area: int = 0  # ROI area in pixels
    patch_id: Optional[str] = None  # Unique patch identifier

    def __post_init__(self):
        """Calculate area if not provided."""
        if self.area == 0:
            self.area = self.width * self.height

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "area": self.area,
            "patch_id": self.patch_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ROI":
        """Create ROI from dictionary."""
        return cls(
            x=data["x"],
            y=data["y"],
            width=data["width"],
            height=data["height"],
            area=data.get("area", data["width"] * data["height"]),
            patch_id=data.get("patch_id"),
        )


@dataclass
class ROIConfig:
    """Configuration for ROI processing."""

    enabled: bool = False  # Enable ROI differential streaming

    # ROI extraction
    min_area: int = 500  # Minimum ROI area in pixels
    merge_distance: int = 50  # Merge regions within this distance (pixels)
    padding: int = 10  # Add border around detected ROI (pixels)
    max_rois: int = 10  # Maximum number of ROIs per frame

    # Encoding
    roi_quality: int = 85  # JPEG quality for ROI patches (1-100)
    full_quality: int = 95  # JPEG quality for full sync frames (1-100)

    # Full sync strategy
    full_sync_interval: float = 30.0  # Force full frame every N seconds
    max_roi_updates_before_sync: int = 50  # Or after N ROI updates

    def __post_init__(self):
        """Validate configuration values."""
        self.min_area = max(100, self.min_area)
        self.merge_distance = max(10, self.merge_distance)
        self.padding = max(0, min(50, self.padding))
        self.max_rois = max(1, min(50, self.max_rois))
        self.roi_quality = max(1, min(100, self.roi_quality))
        self.full_quality = max(1, min(100, self.full_quality))
        self.full_sync_interval = max(1.0, self.full_sync_interval)
        self.max_roi_updates_before_sync = max(1, self.max_roi_updates_before_sync)


@dataclass
class ROIState:
    """Per-stream state for ROI tracking."""

    last_full_sync_time: float = field(default_factory=time.time)
    roi_update_count: int = 0
    last_frame_id: Optional[str] = None
    last_full_frame: Optional[bytes] = None  # Cached for reconstruction

    def needs_full_sync(self, config: ROIConfig) -> bool:
        """Check if full sync is needed based on time and update count."""
        elapsed = time.time() - self.last_full_sync_time
        return (
            elapsed >= config.full_sync_interval or
            self.roi_update_count >= config.max_roi_updates_before_sync
        )

    def reset_sync_state(self):
        """Reset sync counters after full sync."""
        self.last_full_sync_time = time.time()
        self.roi_update_count = 0


class ROIProcessor:
    """
    Processor for extracting and reconstructing ROI regions.

    Thread-safe for use from multiple workers.

    Usage:
        # Sender side:
        processor = ROIProcessor(config)
        motion_mask = get_motion_mask(frame)
        rois = processor.extract_roi_regions(frame, motion_mask)
        patches = [processor.encode_roi_patch(frame, roi) for roi in rois]

        # Receiver side:
        base_frame = get_cached_frame()
        reconstructed = processor.overlay_roi_patches(base_frame, patches)
    """

    def __init__(self, config: Optional[ROIConfig] = None):
        """
        Initialize ROI processor.

        Args:
            config: ROI configuration (uses defaults if None)
        """
        self.config = config or ROIConfig()
        self.logger = logging.getLogger(f"{__name__}.ROIProcessor")

        # Per-stream state (for tracking full sync)
        self._stream_states: Dict[str, ROIState] = {}

    def extract_roi_regions(
        self,
        frame: np.ndarray,
        motion_mask: np.ndarray,
        stream_key: Optional[str] = None,
    ) -> List[ROI]:
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
        if motion_mask is None or motion_mask.size == 0:
            return []

        try:
            # Ensure motion_mask is binary uint8
            if motion_mask.dtype != np.uint8:
                motion_mask = (motion_mask > 0).astype(np.uint8) * 255

            # Merge nearby regions using morphological closing
            kernel_size = max(3, self.config.merge_distance // 10)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
            closed_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_CLOSE, kernel)

            # Find contours
            contours, _ = cv2.findContours(
                closed_mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            if not contours:
                return []

            # Extract bounding boxes
            frame_h, frame_w = frame.shape[:2]
            rois = []

            for contour in contours:
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                area = w * h

                # Filter by minimum area
                if area < self.config.min_area:
                    continue

                # Add padding
                pad = self.config.padding
                x = max(0, x - pad)
                y = max(0, y - pad)
                w = min(frame_w - x, w + 2 * pad)
                h = min(frame_h - y, h + 2 * pad)

                roi = ROI(x=x, y=y, width=w, height=h, area=area)
                rois.append(roi)

            # Sort by area (largest first) and limit count
            rois.sort(key=lambda r: r.area, reverse=True)
            rois = rois[:self.config.max_rois]

            self.logger.debug(
                f"Extracted {len(rois)} ROIs from {len(contours)} contours "
                f"(min_area={self.config.min_area})"
            )

            return rois

        except Exception as e:
            self.logger.error(f"Error extracting ROI regions: {e}", exc_info=True)
            return []

    def encode_roi_patch(
        self,
        frame: np.ndarray,
        roi: ROI,
        quality: Optional[int] = None,
    ) -> Dict[str, Any]:
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
        try:
            # Extract ROI region from frame
            patch_img = frame[roi.y:roi.y+roi.height, roi.x:roi.x+roi.width]

            if patch_img.size == 0:
                self.logger.warning(f"Empty patch for ROI {roi}")
                return {}

            # Encode as JPEG
            quality = quality or self.config.roi_quality
            encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            success, encoded = cv2.imencode('.jpg', patch_img, encode_params)

            if not success:
                self.logger.error(f"Failed to encode ROI patch {roi}")
                return {}

            patch_data = encoded.tobytes()

            return {
                "x": roi.x,
                "y": roi.y,
                "width": roi.width,
                "height": roi.height,
                "patch_data": patch_data,
                "patch_id": roi.patch_id,
                "encoding": "jpeg",
                "quality": quality,
                "size_bytes": len(patch_data),
            }

        except Exception as e:
            self.logger.error(f"Error encoding ROI patch: {e}", exc_info=True)
            return {}

    def decode_roi_patch(self, patch_data: bytes) -> Optional[np.ndarray]:
        """
        Decode ROI patch from bytes.

        Args:
            patch_data: Encoded patch bytes (JPEG)

        Returns:
            Decoded image as numpy array (BGR) or None if failed
        """
        try:
            if not patch_data:
                return None

            # Decode JPEG
            nparr = np.frombuffer(patch_data, np.uint8)
            patch_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            return patch_img

        except Exception as e:
            self.logger.error(f"Error decoding ROI patch: {e}", exc_info=True)
            return None

    def overlay_roi_patches(
        self,
        base_frame_bytes: bytes,
        roi_patches: List[Dict[str, Any]],
    ) -> bytes:
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
        try:
            # Decode base frame
            base_arr = np.frombuffer(base_frame_bytes, np.uint8)
            base_frame = cv2.imdecode(base_arr, cv2.IMREAD_COLOR)

            if base_frame is None:
                self.logger.error("Failed to decode base frame")
                return base_frame_bytes  # Return original on error

            # Overlay each ROI patch
            patches_applied = 0

            for patch in roi_patches:
                try:
                    # Extract patch info
                    x = patch.get("x", 0)
                    y = patch.get("y", 0)
                    patch_data = patch.get("patch_data", b"")

                    if not patch_data:
                        continue

                    # Decode patch
                    patch_img = self.decode_roi_patch(patch_data)
                    if patch_img is None:
                        continue

                    # Get actual dimensions
                    patch_h, patch_w = patch_img.shape[:2]

                    # Bounds checking
                    frame_h, frame_w = base_frame.shape[:2]
                    if x < 0 or y < 0 or x + patch_w > frame_w or y + patch_h > frame_h:
                        self.logger.warning(
                            f"ROI patch out of bounds: ({x}, {y}) {patch_w}*{patch_h} "
                            f"in frame {frame_w}*{frame_h}"
                        )
                        continue

                    # Overlay patch
                    base_frame[y:y+patch_h, x:x+patch_w] = patch_img
                    patches_applied += 1

                except Exception as e:
                    self.logger.warning(f"Failed to overlay ROI patch: {e}")
                    continue

            # Re-encode frame
            quality = self.config.roi_quality
            encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            success, encoded = cv2.imencode('.jpg', base_frame, encode_params)

            if not success:
                self.logger.error("Failed to encode reconstructed frame")
                return base_frame_bytes

            reconstructed_bytes = encoded.tobytes()

            self.logger.debug(
                f"Reconstructed frame with {patches_applied}/{len(roi_patches)} patches "
                f"({len(reconstructed_bytes)} bytes)"
            )

            return reconstructed_bytes

        except Exception as e:
            self.logger.error(f"Error overlaying ROI patches: {e}", exc_info=True)
            return base_frame_bytes  # Return original on error

    def should_send_full_sync(self, stream_key: str) -> bool:
        """
        Check if full frame sync is needed for this stream.

        Args:
            stream_key: Stream identifier

        Returns:
            True if full sync should be sent
        """
        if stream_key not in self._stream_states:
            self._stream_states[stream_key] = ROIState()
            return True  # First frame always full sync

        state = self._stream_states[stream_key]
        return state.needs_full_sync(self.config)

    def record_roi_update(self, stream_key: str, frame_id: str):
        """
        Record an ROI update for sync tracking.

        Args:
            stream_key: Stream identifier
            frame_id: Frame identifier
        """
        if stream_key not in self._stream_states:
            self._stream_states[stream_key] = ROIState()

        state = self._stream_states[stream_key]
        state.roi_update_count += 1
        state.last_frame_id = frame_id

    def record_full_sync(self, stream_key: str, frame_id: str, frame_bytes: Optional[bytes] = None):
        """
        Record a full sync for tracking.

        Args:
            stream_key: Stream identifier
            frame_id: Frame identifier
            frame_bytes: Optional frame bytes to cache
        """
        if stream_key not in self._stream_states:
            self._stream_states[stream_key] = ROIState()

        state = self._stream_states[stream_key]
        state.reset_sync_state()
        state.last_frame_id = frame_id
        if frame_bytes:
            state.last_full_frame = frame_bytes

    def get_cached_frame(self, stream_key: str) -> Optional[bytes]:
        """
        Get cached full frame for reconstruction.

        Args:
            stream_key: Stream identifier

        Returns:
            Cached frame bytes or None if not found
        """
        state = self._stream_states.get(stream_key)
        return state.last_full_frame if state else None

    def clear_stream_state(self, stream_key: str):
        """
        Clear state for a stream (e.g., when camera disconnects).

        Args:
            stream_key: Stream identifier
        """
        if stream_key in self._stream_states:
            del self._stream_states[stream_key]
            self.logger.debug(f"Cleared ROI state for stream {stream_key}")

    def get_stats(self, stream_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Get ROI processing statistics.

        Args:
            stream_key: Optional stream to get stats for (all streams if None)

        Returns:
            Dictionary with statistics
        """
        if stream_key:
            state = self._stream_states.get(stream_key)
            if not state:
                return {}

            return {
                "stream_key": stream_key,
                "roi_update_count": state.roi_update_count,
                "last_frame_id": state.last_frame_id,
                "time_since_sync": time.time() - state.last_full_sync_time,
                "has_cached_frame": state.last_full_frame is not None,
            }
        else:
            return {
                "total_streams": len(self._stream_states),
                "streams": [self.get_stats(key) for key in self._stream_states.keys()],
            }
