import logging
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from imagehash import average_hash, phash, dhash
from PIL import Image
from typing import Tuple, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

class FrameComparator:
    """Base class for frame comparison methods."""
    
    def compare(self, static_frame: np.ndarray, new_frame: np.ndarray, stream_key: Optional[str] = None) -> Tuple[bool, float]:
        """Compare frames and determine if they are similar.
        
        Args:
            static_frame: Reference frame (RGB, cv2 image as np.ndarray).
            new_frame: New frame to compare (RGB, cv2 image as np.ndarray).
            stream_key: Optional identifier for the video stream (e.g., camera ID).
            
        Returns:
            Tuple[bool, float]: (is_similar, similarity_score)
        """
        raise NotImplementedError("Compare method must be implemented in subclass")

class AbsDiffComparator(FrameComparator):
    """Compare frames using absolute difference."""
    
    def __init__(self, threshold: float = 10.0):
        """Initialize with threshold for mean absolute difference.
        
        Args:
            threshold: Mean difference threshold (default: 10.0).
            
        Raises:
            ValueError: If threshold is negative.
        """
        try:
            if not isinstance(threshold, (int, float)) or threshold < 0:
                msg = f"Invalid threshold: {threshold}, must be non-negative"
                logger.error(msg)
                raise ValueError(msg)
            self.threshold = threshold
        except Exception as exc:
            logger.error("Failed to initialize AbsDiffComparator: %s", str(exc))
            print(f"Error initializing AbsDiffComparator: {str(exc)}")
            raise

    def compare(self, static_frame: np.ndarray, new_frame: np.ndarray, stream_key: Optional[str] = None) -> Tuple[bool, float]:
        """Compare frames using mean absolute difference.
        
        Args:
            static_frame: Reference frame (RGB, cv2 image as np.ndarray).
            new_frame: New frame to compare (RGB, cv2 image as np.ndarray).
            stream_key: Optional identifier for the video stream (e.g., camera ID).
            
        Returns:
            Tuple[bool, float]: (is_similar, mean_difference)
        """
        try:
            stream_key = stream_key or "default_stream_key"
            if not isinstance(static_frame, np.ndarray) or not isinstance(new_frame, np.ndarray):
                msg = f"Invalid frame type for stream {stream_key}: static_frame and new_frame must be np.ndarray"
                logger.error(msg)
                return False, 0.0
            if static_frame.shape != new_frame.shape or static_frame.shape[2] != 3:
                msg = f"Frames for stream {stream_key} have mismatched dimensions or are not RGB"
                logger.error(msg)
                return False, 0.0
            
            diff = cv2.absdiff(static_frame, new_frame)
            mean_diff = np.mean(diff)
            if np.isnan(mean_diff):
                msg = f"NaN detected in AbsDiff comparison for stream {stream_key}"
                logger.error(msg)
                return False, 0.0
            return mean_diff < self.threshold, float(mean_diff)
        except cv2.error as exc:
            logger.error("OpenCV error in AbsDiff comparison for stream %s: %s", stream_key, str(exc))
            print(f"OpenCV error in AbsDiff for stream {stream_key}: {str(exc)}")
            return False, 0.0
        except (ValueError, TypeError) as exc:
            logger.error("Value or Type error in AbsDiff comparison for stream %s: %s", stream_key, str(exc))
            print(f"Value/Type error in AbsDiff for stream {stream_key}: {str(exc)}")
            return False, 0.0
        except Exception as exc:
            logger.error("Unexpected error in AbsDiff comparison for stream %s: %s", stream_key, str(exc))
            print(f"Unexpected error in AbsDiff for stream {stream_key}: {str(exc)}")
            return False, 0.0

class SSIMComparator(FrameComparator):
    """Compare frames using Structural Similarity Index (SSIM)."""
    
    def __init__(self, threshold: float = 0.9):
        """Initialize with threshold for SSIM score.
        
        Args:
            threshold: SSIM score threshold (default: 0.9).
        
        Raises:
            ValueError: If threshold is not in [0, 1].
        """
        try:
            if not isinstance(threshold, (int, float)) or not 0 <= threshold <= 1:
                msg = f"Invalid threshold: {threshold}, must be between 0 and 1"
                logger.error(msg)
                raise ValueError(msg)
            self.threshold = threshold
        except Exception as exc:
            logger.error("Failed to initialize SSIMComparator: %s", str(exc))
            print(f"Error initializing SSIMComparator: {str(exc)}")
            raise

    def compare(self, static_frame: np.ndarray, new_frame: np.ndarray, stream_key: Optional[str] = None) -> Tuple[bool, float]:
        """Compare frames using SSIM.
        
        Args:
            static_frame: Reference frame (RGB, cv2 image as np.ndarray).
            new_frame: New frame to compare (RGB, cv2 image as np.ndarray).
            stream_key: Optional identifier for the video stream (e.g., camera ID).
            
        Returns:
            Tuple[bool, float]: (is_similar, ssim_score)
        """
        try:
            stream_key = stream_key or "default_stream_key"
            if not isinstance(static_frame, np.ndarray) or not isinstance(new_frame, np.ndarray):
                msg = f"Invalid frame type for stream {stream_key}: static_frame and new_frame must be np.ndarray"
                logger.error(msg)
                return False, 0.0
            if static_frame.shape != new_frame.shape or static_frame.shape[2] != 3:
                msg = f"Frames for stream {stream_key} have mismatched dimensions or are not RGB"
                logger.error(msg)
                return False, 0.0
            
            gray_static = cv2.cvtColor(static_frame, cv2.COLOR_BGR2GRAY)
            gray_new = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
            score, _ = ssim(gray_static, gray_new, full=True)
            if np.isnan(score):
                msg = f"NaN detected in SSIM comparison for stream {stream_key}"
                logger.error(msg)
                return False, 0.0
            return score > self.threshold, float(score)
        except cv2.error as exc:
            logger.error("OpenCV error in SSIM comparison for stream %s: %s", stream_key, str(exc))
            print(f"OpenCV error in SSIM for stream {stream_key}: {str(exc)}")
            return False, 0.0
        except (ValueError, TypeError) as exc:
            logger.error("Value or Type error in SSIM comparison for stream %s: %s", stream_key, str(exc))
            print(f"Value/Type error in SSIM for stream {stream_key}: {str(exc)}")
            return False, 0.0
        except Exception as exc:
            logger.error("Unexpected error in SSIM comparison for stream %s: %s", stream_key, str(exc))
            print(f"Unexpected error in SSIM for stream {stream_key}: {str(exc)}")
            return False, 0.0

class AverageHashComparator(FrameComparator):
    """Compares frames using average hashing (aHash)."""
    
    def __init__(self, threshold: int = 5):
        """Initialize with threshold for hash difference.
        
        Args:
            threshold: Hash difference threshold (default: 5).
        
        Raises:
            ValueError: If threshold is negative.
        """
        try:
            if not isinstance(threshold, int) or threshold < 0:
                msg = f"Invalid threshold: {threshold}, must be a non-negative integer"
                logger.error(msg)
                raise ValueError(msg)
            self.threshold = threshold
        except Exception as exc:
            logger.error("Failed to initialize AverageHashComparator: %s", str(exc))
            print(f"Error initializing AverageHashComparator: {str(exc)}")
            raise

    def compare(self, static_frame: np.ndarray, new_frame: np.ndarray, stream_key: Optional[str] = None) -> Tuple[bool, float]:
        """Compare frames using average hash difference.
        
        Args:
            static_frame: Reference frame (RGB, cv2 image as np.ndarray).
            new_frame: New frame to compare (RGB, cv2 image as np.ndarray).
            stream_key: Optional identifier for the video stream (e.g., camera ID).
            
        Returns:
            Tuple[bool, float]: (is_similar, hash_difference)
        """
        try:
            stream_key = stream_key or "default_stream_key"
            if not isinstance(static_frame, np.ndarray) or not isinstance(new_frame, np.ndarray):
                msg = f"Invalid frame type for stream {stream_key}: static_frame and new_frame must be np.ndarray"
                logger.error(msg)
                return False, 0.0
            if static_frame.shape != new_frame.shape or static_frame.shape[2] != 3:
                msg = f"Frames for stream {stream_key} have mismatched dimensions or are not RGB"
                logger.error(msg)
                return False, 0.0
            
            static_pil = Image.fromarray(cv2.cvtColor(static_frame, cv2.COLOR_BGR2RGB))
            new_pil = Image.fromarray(cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB))
            diff = average_hash(static_pil) - average_hash(new_pil)
            return diff < self.threshold, float(diff)
        except cv2.error as exc:
            logger.error("OpenCV error in AverageHash comparison for stream %s: %s", stream_key, str(exc))
            print(f"OpenCV error in AverageHash for stream {stream_key}: {str(exc)}")
            return False, 0.0
        except (ValueError, TypeError, Image.UnidentifiedImageError) as exc:
            logger.error("Value, Type, or PIL error in AverageHash comparison for stream %s: %s", stream_key, str(exc))
            print(f"Value/Type/PIL error in AverageHash for stream {stream_key}: {str(exc)}")
            return False, 0.0
        except Exception as exc:
            logger.error("Unexpected error in AverageHash comparison for stream %s: %s", stream_key, str(exc))
            print(f"Unexpected error in AverageHash for stream {stream_key}: {str(exc)}")
            return False, 0.0

class PerceptualHashComparator(FrameComparator):
    """Compares frames using perceptual hashing (pHash)."""
    
    def __init__(self, threshold: int = 6):
        """Initialize with threshold for hash difference.
        
        Args:
            threshold: Hash difference threshold (default: 6).
        
        Raises:
            ValueError: If threshold is negative.
        """
        try:
            if not isinstance(threshold, int) or threshold < 0:
                msg = f"Invalid threshold: {threshold}, must be a non-negative integer"
                logger.error(msg)
                raise ValueError(msg)
            self.threshold = threshold
        except Exception as exc:
            logger.error("Failed to initialize PerceptualHashComparator: %s", str(exc))
            print(f"Error initializing PerceptualHashComparator: {str(exc)}")
            raise

    def compare(self, static_frame: np.ndarray, new_frame: np.ndarray, stream_key: Optional[str] = None) -> Tuple[bool, float]:
        """Compare frames using perceptual hash difference.
        
        Args:
            static_frame: Reference frame (RGB, cv2 image as np.ndarray).
            new_frame: New frame to compare (RGB, cv2 image as np.ndarray).
            stream_key: Optional identifier for the video stream (e.g., camera ID).
            
        Returns:
            Tuple[bool, float]: (is_similar, hash_difference)
        """
        try:
            stream_key = stream_key or "default_stream_key"
            if not isinstance(static_frame, np.ndarray) or not isinstance(new_frame, np.ndarray):
                msg = f"Invalid frame type for stream {stream_key}: static_frame and new_frame must be np.ndarray"
                logger.error(msg)
                return False, 0.0
            if static_frame.shape != new_frame.shape or static_frame.shape[2] != 3:
                msg = f"Frames for stream {stream_key} have mismatched dimensions or are not RGB"
                logger.error(msg)
                return False, 0.0
            
            static_pil = Image.fromarray(cv2.cvtColor(static_frame, cv2.COLOR_BGR2RGB))
            new_pil = Image.fromarray(cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB))
            diff = phash(static_pil) - phash(new_pil)
            return diff < self.threshold, float(diff)
        except cv2.error as exc:
            logger.error("OpenCV error in PerceptualHash comparison for stream %s: %s", stream_key, str(exc))
            print(f"OpenCV error in PerceptualHash for stream {stream_key}: {str(exc)}")
            return False, 0.0
        except (ValueError, TypeError, Image.UnidentifiedImageError) as exc:
            logger.error("Value, Type, or PIL error in PerceptualHash comparison for stream %s: %s", stream_key, str(exc))
            print(f"Value/Type/PIL error in PerceptualHash for stream {stream_key}: {str(exc)}")
            return False, 0.0
        except Exception as exc:
            logger.error("Unexpected error in PerceptualHash comparison for stream %s: %s", stream_key, str(exc))
            print(f"Unexpected error in PerceptualHash for stream {stream_key}: {str(exc)}")
            return False, 0.0
        
class DifferenceHashComparator(FrameComparator):
    """Compares frames using difference hashing (dHash)."""
    
    def __init__(self, threshold: int = 5):
        """Initialize with threshold for hash difference.
        
        Args:
            threshold: Hash difference threshold (default: 5).
        
        Raises:
            ValueError: If threshold is negative.
        """
        try:
            if not isinstance(threshold, int) or threshold < 0:
                msg = f"Invalid threshold: {threshold}, must be a non-negative integer"
                logger.error(msg)
                raise ValueError(msg)
            self.threshold = threshold
        except Exception as exc:
            logger.error("Failed to initialize DifferenceHashComparator: %s", str(exc))
            print(f"Error initializing DifferenceHashComparator: {str(exc)}")
            raise

    def compare(self, static_frame: np.ndarray, new_frame: np.ndarray, stream_key: Optional[str] = None) -> Tuple[bool, float]:
        """Compare frames using difference hash difference.
        
        Args:
            static_frame: Reference frame (RGB, cv2 image as np.ndarray).
            new_frame: New frame to compare (RGB, cv2 image as np.ndarray).
            stream_key: Optional identifier for the video stream (e.g., camera ID).
            
        Returns:
            Tuple[bool, float]: (is_similar, hash_difference)
        """
        try:
            stream_key = stream_key or "default_stream_key"
            if not isinstance(static_frame, np.ndarray) or not isinstance(new_frame, np.ndarray):
                msg = f"Invalid frame type for stream {stream_key}: static_frame and new_frame must be np.ndarray"
                logger.error(msg)
                return False, 0.0
            if static_frame.shape != new_frame.shape or static_frame.shape[2] != 3:
                msg = f"Frames for stream {stream_key} have mismatched dimensions or are not RGB"
                logger.error(msg)
                return False, 0.0

            static_pil = Image.fromarray(cv2.cvtColor(static_frame, cv2.COLOR_BGR2RGB))
            new_pil = Image.fromarray(cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB))
            diff = dhash(static_pil) - dhash(new_pil)
            return diff < self.threshold, float(diff)
        except cv2.error as exc:
            logger.error("OpenCV error in DifferenceHash comparison for stream %s: %s", stream_key, str(exc))
            print(f"OpenCV error in DifferenceHash for stream {stream_key}: {str(exc)}")
            return False, 0.0
        except (ValueError, TypeError, Image.UnidentifiedImageError) as exc:
            logger.error("Value, Type, or PIL error in DifferenceHash comparison for stream %s: %s", stream_key, str(exc))
            print(f"Value/Type/PIL error in DifferenceHash for stream {stream_key}: {str(exc)}")
            return False, 0.0
        except Exception as exc:
            logger.error("Unexpected error in DifferenceHash comparison for stream %s: %s", stream_key, str(exc))
            print(f"Unexpected error in DifferenceHash for stream {stream_key}: {str(exc)}")
            return False, 0.0

class HistogramComparator(FrameComparator):
    """Compare frames using histogram correlation."""
    
    def __init__(self, threshold: float = 0.9):
        """Initialize with threshold for histogram correlation.
        
        Args:
            threshold: Correlation score threshold (default: 0.9).
        
        Raises:
            ValueError: If threshold is not in [0, 1].
        """
        try:
            if not isinstance(threshold, (int, float)) or not 0 <= threshold <= 1:
                msg = f"Invalid threshold: {threshold}, must be between 0 and 1"
                logger.error(msg)
                raise ValueError(msg)
            self.threshold = threshold
        except Exception as exc:
            logger.error("Failed to initialize HistogramComparator: %s", str(exc))
            print(f"Error initializing HistogramComparator: {str(exc)}")
            raise
    
    def compare(self, static_frame: np.ndarray, new_frame: np.ndarray, stream_key: Optional[str] = None) -> Tuple[bool, float]:
        """Compare frames using histogram correlation.
        
        Args:
            static_frame: Reference frame (RGB, cv2 image as np.ndarray).
            new_frame: New frame to compare (RGB, cv2 image as np.ndarray).
            stream_key: Optional identifier for the video stream (e.g., camera ID).
            
        Returns:
            Tuple[bool, float]: (is_similar, correlation_score)
        """
        try:
            stream_key = stream_key or "default_stream_key"
            if not isinstance(static_frame, np.ndarray) or not isinstance(new_frame, np.ndarray):
                msg = f"Invalid frame type for stream {stream_key}: static_frame and new_frame must be np.ndarray"
                logger.error(msg)
                return False, 0.0
            if static_frame.shape != new_frame.shape or static_frame.shape[2] != 3:
                msg = f"Frames for stream {stream_key} have mismatched dimensions or are not RGB"
                logger.error(msg)
                return False, 0.0
            
            static_hist = cv2.calcHist([static_frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            new_hist = cv2.calcHist([new_frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            static_hist = cv2.normalize(static_hist, static_hist).flatten()
            new_hist = cv2.normalize(new_hist, new_hist).flatten()
            correlation = cv2.compareHist(static_hist, new_hist, cv2.HISTCMP_CORREL)
            if np.isnan(correlation):
                msg = f"NaN detected in Histogram comparison for stream {stream_key}"
                logger.error(msg)
                return False, 0.0
            return correlation > self.threshold, float(correlation)
        except cv2.error as exc:
            logger.error("OpenCV error in Histogram comparison for stream %s: %s", stream_key, str(exc))
            print(f"OpenCV error in Histogram for stream {stream_key}: {str(exc)}")
            return False, 0.0
        except (ValueError, TypeError) as exc:
            logger.error("Value or Type error in Histogram comparison for stream %s: %s", stream_key, str(exc))
            print(f"Value/Type error in Histogram for stream {stream_key}: {str(exc)}")
            return False, 0.0
        except Exception as exc:
            logger.error("Unexpected error in Histogram comparison for stream %s: %s", stream_key, str(exc))
            print(f"Unexpected error in Histogram for stream {stream_key}: {str(exc)}")
            return False, 0.0
