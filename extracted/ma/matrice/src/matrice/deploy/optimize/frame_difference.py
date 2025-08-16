"""Frame difference utilities for intelligent caching."""

import cv2
import numpy as np
import base64
import logging
from typing import Dict, Any, Optional, Tuple, Union
from PIL import Image

logger = logging.getLogger(__name__)


class FrameDifferenceProcessor:
    """Handles frame difference calculation and reconstruction for intelligent caching."""
    
    def __init__(self):
        """Initialize frame difference processor."""
        self.logger = logging.getLogger(__name__)
    
    def calculate_frame_difference(
        self, 
        reference_frame: np.ndarray, 
        current_frame: np.ndarray
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Calculate difference between reference and current frame.
        
        Args:
            reference_frame: Reference frame (RGB, cv2 image as np.ndarray)
            current_frame: Current frame to compare (RGB, cv2 image as np.ndarray)
            
        Returns:
            Tuple of (difference_data, metadata)
        """
        try:
            if reference_frame.shape != current_frame.shape:
                raise ValueError("Frame dimensions must match")
            
            # Calculate absolute difference
            diff = cv2.absdiff(reference_frame, current_frame)
            
            # Create a mask for changed pixels (threshold-based)
            gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray_diff, 25, 255, cv2.THRESH_BINARY)
            
            # Find bounding box of changes
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                # No significant changes
                return np.zeros_like(diff), {
                    "has_changes": False,
                    "change_ratio": 0.0,
                    "bounding_boxes": []
                }
            
            # Calculate change statistics
            change_pixels = np.sum(mask > 0)
            total_pixels = mask.shape[0] * mask.shape[1]
            change_ratio = change_pixels / total_pixels
            
            # Get bounding boxes for major changes
            bounding_boxes = []
            for contour in contours:
                if cv2.contourArea(contour) > 100:  # Filter small changes
                    x, y, w, h = cv2.boundingRect(contour)
                    bounding_boxes.append({"x": int(x), "y": int(y), "width": int(w), "height": int(h)})
            
            metadata = {
                "has_changes": True,
                "change_ratio": float(change_ratio),
                "change_pixels": int(change_pixels),
                "total_pixels": int(total_pixels),
                "bounding_boxes": bounding_boxes,
                "mask_shape": mask.shape
            }
            
            return diff, metadata
            
        except Exception as exc:
            self.logger.error(f"Error calculating frame difference: {str(exc)}")
            return np.zeros_like(current_frame), {"has_changes": False, "error": str(exc)}
    
    def encode_frame_difference(
        self, 
        difference_data: np.ndarray, 
        metadata: Dict[str, Any],
        compression_quality: int = 85
    ) -> str:
        """Encode frame difference data to base64.
        
        Args:
            difference_data: Frame difference as numpy array
            metadata: Difference metadata
            compression_quality: JPEG compression quality (1-100)
            
        Returns:
            Base64 encoded difference data
        """
        try:
            if not metadata.get("has_changes", False):
                return ""
            
            # Compress difference data
            encode_params = [cv2.IMWRITE_JPEG_QUALITY, compression_quality]
            _, buffer = cv2.imencode(".jpg", difference_data, encode_params)
            
            return base64.b64encode(buffer.tobytes()).decode('utf-8')
            
        except Exception as exc:
            self.logger.error(f"Error encoding frame difference: {str(exc)}")
            return ""
    
    def decode_frame_difference(self, encoded_diff: str) -> Optional[np.ndarray]:
        """Decode base64 frame difference data.
        
        Args:
            encoded_diff: Base64 encoded difference data
            
        Returns:
            Decoded difference as numpy array or None if failed
        """
        try:
            if not encoded_diff:
                return None
            
            diff_bytes = base64.b64decode(encoded_diff)
            diff_array = cv2.imdecode(np.frombuffer(diff_bytes, np.uint8), cv2.IMREAD_COLOR)
            
            return diff_array
            
        except Exception as exc:
            self.logger.error(f"Error decoding frame difference: {str(exc)}")
            return None
    
    def reconstruct_frame(
        self, 
        reference_frame: np.ndarray, 
        difference_data: np.ndarray,
        metadata: Dict[str, Any]
    ) -> Optional[np.ndarray]:
        """Reconstruct frame from reference frame and difference data.
        
        Args:
            reference_frame: Reference frame (RGB, cv2 image as np.ndarray)
            difference_data: Frame difference data
            metadata: Difference metadata
            
        Returns:
            Reconstructed frame or None if failed
        """
        try:
            if not metadata.get("has_changes", False):
                return reference_frame.copy()
            
            if reference_frame.shape != difference_data.shape:
                self.logger.warning("Shape mismatch in frame reconstruction")
                return None
            
            # Simple reconstruction: add difference to reference
            # In practice, you might want more sophisticated reconstruction
            reconstructed = cv2.add(reference_frame, difference_data)
            
            return reconstructed
            
        except Exception as exc:
            self.logger.error(f"Error reconstructing frame: {str(exc)}")
            return None
    
    def encode_frame_to_base64(self, frame: np.ndarray, quality: int = 95) -> str:
        """Encode frame to base64 string.
        
        Args:
            frame: Frame as numpy array
            quality: JPEG quality (1-100)
            
        Returns:
            Base64 encoded frame
        """
        try:
            encode_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
            _, buffer = cv2.imencode(".jpg", frame, encode_params)
            return base64.b64encode(buffer.tobytes()).decode('utf-8')
        except Exception as exc:
            self.logger.error(f"Error encoding frame to base64: {str(exc)}")
            return ""
    
    def decode_base64_to_frame(self, encoded_frame: str) -> Optional[np.ndarray]:
        """Decode base64 string to frame.
        
        Args:
            encoded_frame: Base64 encoded frame
            
        Returns:
            Decoded frame as numpy array or None if failed
        """
        try:
            frame_bytes = base64.b64decode(encoded_frame)
            frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
            return frame
        except Exception as exc:
            self.logger.error(f"Error decoding base64 to frame: {str(exc)}")
            return None


class IntelligentFrameCache:
    """Intelligent frame cache with two-threshold logic."""
    
    def __init__(
        self, 
        threshold_a: float = 0.95,  # High similarity threshold
        threshold_b: float = 0.85,  # Medium similarity threshold
        max_cache_size: int = 50
    ):
        """Initialize intelligent frame cache.
        
        Args:
            threshold_a: High similarity threshold for cache reuse
            threshold_b: Medium similarity threshold for difference-based reconstruction
            max_cache_size: Maximum number of cached frames per stream
        """
        self.threshold_a = threshold_a
        self.threshold_b = threshold_b
        self.max_cache_size = max_cache_size
        
        # Cache storage: stream_key -> cache_data
        self.frame_cache = {}
        self.difference_processor = FrameDifferenceProcessor()
        
        self.logger = logging.getLogger(__name__)
    
    def should_use_cache(
        self, 
        current_frame: np.ndarray, 
        stream_key: str,
        ssim_comparator
    ) -> Tuple[str, Dict[str, Any]]:
        """Determine caching strategy based on frame similarity.
        
        Args:
            current_frame: Current frame to analyze
            stream_key: Stream identifier
            ssim_comparator: SSIM comparator for similarity calculation
            
        Returns:
            Tuple of (action, data) where action is:
            - "use_cache": Use cached result (Threshold A)
            - "use_difference": Use difference-based reconstruction (Threshold B)
            - "process_new": Process as new frame (exceeds both thresholds)
        """
        if stream_key not in self.frame_cache:
            return "process_new", {}
        
        cache_data = self.frame_cache[stream_key]
        reference_frame = cache_data["frame"]
        
        # Calculate SSIM similarity
        is_similar, similarity_score = ssim_comparator.compare(
            reference_frame, current_frame, stream_key
        )
        
        if similarity_score >= self.threshold_a:
            # High similarity - reuse cached result
            return "use_cache", {
                "similarity_score": similarity_score,
                "cache_data": cache_data
            }
        elif similarity_score >= self.threshold_b:
            # Medium similarity - use difference-based approach
            diff_data, diff_metadata = self.difference_processor.calculate_frame_difference(
                reference_frame, current_frame
            )
            
            return "use_difference", {
                "similarity_score": similarity_score,
                "cache_data": cache_data,
                "difference_data": diff_data,
                "difference_metadata": diff_metadata
            }
        else:
            # Low similarity - process as new frame
            return "process_new", {
                "similarity_score": similarity_score
            }
    
    def cache_frame_result(
        self, 
        stream_key: str, 
        frame: np.ndarray, 
        model_result: Any,
        input_hash: Optional[str] = None
    ) -> None:
        """Cache frame and its model result.
        
        Args:
            stream_key: Stream identifier
            frame: Frame that was processed
            model_result: Result from model inference
            input_hash: Optional input hash for additional indexing
        """
        try:
            cache_entry = {
                "frame": frame.copy(),
                "model_result": model_result,
                "input_hash": input_hash,
                "timestamp": np.datetime64('now'),
                "access_count": 0
            }
            
            if stream_key not in self.frame_cache:
                self.frame_cache[stream_key] = {}
            
            # Simple LRU-like cache management
            cache = self.frame_cache[stream_key]
            if len(cache) >= self.max_cache_size:
                # Remove oldest entry
                oldest_key = min(cache.keys(), key=lambda k: cache[k]["timestamp"])
                del cache[oldest_key]
            
            # Add new entry
            cache_key = input_hash if input_hash else f"frame_{len(cache)}"
            cache[cache_key] = cache_entry
            
            self.logger.debug(f"Cached frame result for stream {stream_key}, cache size: {len(cache)}")
            
        except Exception as exc:
            self.logger.error(f"Error caching frame result: {str(exc)}")
    
    def get_cached_result(self, stream_key: str, action_data: Dict[str, Any]) -> Any:
        """Get cached result based on action data.
        
        Args:
            stream_key: Stream identifier
            action_data: Data from should_use_cache decision
            
        Returns:
            Cached model result or None
        """
        try:
            if "cache_data" not in action_data:
                return None
            
            cache_data = action_data["cache_data"]
            
            # Update access count
            if isinstance(cache_data, dict) and "access_count" in cache_data:
                cache_data["access_count"] += 1
            
            return cache_data.get("model_result")
            
        except Exception as exc:
            self.logger.error(f"Error getting cached result: {str(exc)}")
            return None
    
    def clear_cache(self, stream_key: Optional[str] = None) -> None:
        """Clear cache for specific stream or all streams.
        
        Args:
            stream_key: Stream to clear, or None to clear all
        """
        if stream_key:
            self.frame_cache.pop(stream_key, None)
        else:
            self.frame_cache.clear()
        
        self.logger.info(f"Cleared cache for stream: {stream_key or 'all streams'}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        total_entries = sum(len(cache) for cache in self.frame_cache.values())
        stream_count = len(self.frame_cache)
        
        return {
            "total_cached_entries": total_entries,
            "cached_streams": stream_count,
            "threshold_a": self.threshold_a,
            "threshold_b": self.threshold_b,
            "max_cache_size": self.max_cache_size,
            "cache_details": {
                stream_key: {
                    "entry_count": len(cache),
                    "total_accesses": sum(entry.get("access_count", 0) for entry in cache.values())
                }
                for stream_key, cache in self.frame_cache.items()
            }
        }