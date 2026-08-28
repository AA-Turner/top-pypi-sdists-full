"""Auto-generated stub for module: color_classifier."""
from typing import Any, Dict, List, Optional

# Constants
DEFAULT_CACHE_DIR: Any
DEFAULT_INPUT_SIZE: int
DEFAULT_MAX_RETRIES: int
DEFAULT_MIN_CROP_SIZE: int
DEFAULT_TIMEOUT: int
IMAGENET_MEAN: Any
IMAGENET_STD: Any
MIN_VALID_FILE_SIZE: int
logger: Any
ort: None
timm: None
torch: None

# Functions
def preprocess_crop(crop: Any.Any, input_size: int = DEFAULT_INPUT_SIZE) -> Any.Any:
    """
    Preprocess single crop: resize, normalize, transpose to NCHW.
    """
    ...

# Classes
class ColorCache:
    # Track-ID based LRU cache for color predictions.

    def __init__(self: Any, max_size: int = 1000, update_interval: int = 5) -> None: ...

    def get(self: Any, track_id: int) -> Optional[Any]: ...

    def set(self: Any, track_id: int, color: str, confidence: float, frame: int) -> Any: ...

    def should_classify(self: Any, track_id: int, frame: int) -> bool: ...

class ColorCacheEntry:
    ...
class ColorClassifier:
    # CNN-based color classifier for vehicle color detection.
    #
    # Model Loading Priority:
    #     1. PyTorch checkpoint (.pt/.pth) - preferred
    #     2. ONNX model (.onnx) - fallback
    #
    # Source Priority:
    #     1. URL (HTTP/S3) → download to ~/.cache/color_classifier/ → load
    #     2. Local path → load directly
    #
    # Supports:
    #     - PyTorch checkpoint with timm models (ConvNeXt, EfficientNet, etc.)
    #     - ONNX model with optional external weights (.onnx.data)
    #     - Automatic CUDA/CPU device selection
    #     - Track-ID based caching with frame-skip

    def __init__(self: Any, checkpoint_path: Optional[str] = None, onnx_path: Optional[str] = None, onnx_data_path: Optional[str] = None, color_palette: Optional[List[str]] = None, input_size: int = DEFAULT_INPUT_SIZE, min_crop_size: int = DEFAULT_MIN_CROP_SIZE, return_probabilities: bool = False, cache_dir: str = DEFAULT_CACHE_DIR) -> None:
        """
        Initialize color classifier.
        
        Args:
            checkpoint_path: Path or URL to PyTorch checkpoint (.pt/.pth)
            onnx_path: Path or URL to ONNX model (.onnx)
            onnx_data_path: Path or URL to ONNX external weights (.onnx.data)
            color_palette: List of color labels (default: 7 classes)
            input_size: Input image size (default: 224)
            min_crop_size: Minimum crop dimension to process (default: 32)
            return_probabilities: Include full probability dict in output
            cache_dir: Directory for caching downloaded models
        """
        ...

    def classify(self: Any, detections: List[Dict], input_bytes: Any, frame_number: int = 0, cache: Optional[Any] = None) -> Dict[int, Dict[str, Any]]:
        """
        Classify colors for detections in a frame.
        
        Args:
            detections: List of detection dicts with 'track_id' and 'bounding_box'
            input_bytes: JPEG/PNG encoded frame bytes
            frame_number: Current frame number (for cache logic)
            cache: Optional ColorCache instance
        
        Returns:
            Dict mapping track_id → {"color": str, "confidence": float}
        """
        ...

    def classify_crops(self: Any, crops: List[Any.Any]) -> List[Dict]:
        """
        Batch classification API (ClipProcessor compatible).
        
        Args:
            crops: List of RGB numpy arrays
        
        Returns:
            List of {"color": str, "confidence": float, "all_colors": [...]}
        """
        ...

    def is_available(self: Any) -> bool:
        """
        Check if classifier is ready for inference.
        """
        ...

