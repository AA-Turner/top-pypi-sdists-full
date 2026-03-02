"""Auto-generated stub for module: roi_processor."""
from typing import Any, Dict, List, Optional

# Classes
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

class ROIConfig:
    # Configuration for ROI processing.

    ...
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

