"""Stub file for post_processing.usecases.color directory."""
from typing import Any, Dict, List, Optional, Tuple

# Constants
CLIPProcessor: None = ...  # From clip
Image: None = ...  # From clip
ir_as_file: None = ...  # From clip
ir_files: None = ...  # From clip
ort: None = ...  # From clip
DEFAULT_CACHE_DIR: Any = ...  # From color_classifier
DEFAULT_INPUT_SIZE: int = ...  # From color_classifier
DEFAULT_MAX_RETRIES: int = ...  # From color_classifier
DEFAULT_MIN_CROP_SIZE: int = ...  # From color_classifier
DEFAULT_TIMEOUT: int = ...  # From color_classifier
IMAGENET_MEAN: Any = ...  # From color_classifier
IMAGENET_STD: Any = ...  # From color_classifier
MIN_VALID_FILE_SIZE: int = ...  # From color_classifier
logger: Any = ...  # From color_classifier
ort: None = ...  # From color_classifier
timm: None = ...  # From color_classifier
torch: None = ...  # From color_classifier
ColorInfo: Any = ...  # From color_map_utils
PALETTE: Any = ...  # From color_map_utils
PALETTE_RGB: Dict[Any, Any] = ...  # From color_map_utils
logger: Any = ...  # From color_mapper

# Functions
# From clip
def load_model_from_checkpoint(checkpoint_url: str, providers: Optional[List] = None) -> Any:
    """
    Load an ONNX model from a URL directly into memory without writing locally.
    Enforces the specified providers (e.g., CUDAExecutionProvider) for execution.
    """
    ...

# From clip
def preprocess_crop_paper_vcr(crop_rgb: Any, output_size: Any = (224, 224), contrast_alpha: Any = 1.3, gaussian_kernel: Any = (5, 5), sat_scale: Any = 0.9, val_scale: Any = 1.0) -> Any: ...

# From clip
def try_install_clip_dependencies() -> Any:
    """
    Attempt to install missing CLIP dependencies.
    Only called when ClipProcessor is actually instantiated (lazy installation).
    Uses singleton pattern to ensure installation only happens ONCE per session.
    Returns True if successful, False otherwise.
    """
    ...

# From color_classifier
def preprocess_crop(crop: Any.Any, input_size: int = DEFAULT_INPUT_SIZE) -> Any.Any:
    """
    Preprocess single crop: resize, normalize, transpose to NCHW.
    """
    ...

# From color_map_utils
def extract_major_colors(image: Any.Any, k: int = 3) -> Any: ...

# From color_map_utils
def find_nearest_color(lab_color: Any.Any) -> Any: ...

# From color_map_utils
def lab_distance(c1: Any.Any, c2: Any.Any) -> float: ...

# From color_map_utils
def rgb_to_lab(rgb: tuple) -> Any.Any: ...

# From color_mapper
def process_video_with_color_detection(video_bytes: Any, yolo_predictions: Dict[str, List[Dict]], output_dir: str = './output', top_k_colors: int = 3, min_confidence: float = 0.5, fps: Optional[float] = None) -> Tuple[str, str]:
    """
    Process video with YOLO predictions and extract color information.
    
    Args:
        video_bytes: Raw video file bytes
        yolo_predictions: Dict with frame_id -> list of YOLO detection dicts
        output_dir: Directory to save output files
        top_k_colors: Number of top colors to extract per detection
        min_confidence: Minimum confidence threshold for detections
        fps: Video FPS (auto-detected if not provided)
    
    Returns:
        Tuple of (detailed_results_path, summary_results_path)
    
    Example:
        >>> with open("video.mp4", "rb") as f:
        ...     video_bytes = f.read()
        >>>
        >>> # YOLO predictions format:
        >>> predictions = {
        ...     "0": [
        ...         {
        ...             "category": "car",
        ...             "bounding_box": {"xmin": 100, "ymin": 50, "xmax": 200, "ymax": 150},
        ...             "confidence": 0.95,
        ...             "track_id": "car_001"
        ...         }
        ...     ],
        ...     "1": [...]
        ... }
        >>>
        >>> detailed_path, summary_path = process_video_with_color_detection(
        ...     video_bytes, predictions, "./results"
        ... )
    """
    ...

# Classes
# From clip
class ClipProcessor:
    def __init__(self: Any, image_model_path: str = 'https://s3.us-west-2.amazonaws.com/testing.resources/datasets/clip_image.onnx', text_model_path: str = 'https://s3.us-west-2.amazonaws.com/testing.resources/datasets/clip_text.onnx', processor_dir: Optional[str] = None, providers: Optional[List[str]] = None) -> None: ...

    def process_color_in_frame(self: Any, detections: Any, input_bytes: Any, _zones: Optional[Dict[str, List[List[float]]]], _stream_info: Any) -> Any: ...

    def run_image_onnx_on_crops(self: Any, crops: Any) -> Any: ...


# From color_classifier
class ColorCache:
    # Track-ID based LRU cache for color predictions.

    def __init__(self: Any, max_size: int = 1000, update_interval: int = 5) -> None: ...

    def get(self: Any, track_id: int) -> Optional[Any]: ...

    def set(self: Any, track_id: int, color: str, confidence: float, frame: int) -> Any: ...

    def should_classify(self: Any, track_id: int, frame: int) -> bool: ...


# From color_classifier
class ColorCacheEntry:
    ...

# From color_classifier
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


# From color_mapper
class VideoColorClassifier:
    # A comprehensive system for processing video frames with YOLO predictions
    # and extracting color information from detected objects.

    def __init__(self: Any, top_k_colors: int = 3, min_confidence: float = 0.5) -> None:
        """
        Initialize the video color classifier.
        
        Args:
            top_k_colors: Number of top colors to extract per detection
            min_confidence: Minimum confidence threshold for detections
        """
        ...

    def process_video_with_predictions(self: Any, video_bytes: Any, predictions: Dict[str, List[Dict]], output_dir: str = './output', fps: Optional[float] = None) -> Tuple[str, str]:
        """
        Main function to process video with YOLO predictions and extract colors.
        
        Args:
            video_bytes: Raw video file bytes
            predictions: Dict with frame_id -> list of detection dicts
            output_dir: Directory to save output files
            fps: Video FPS (will be auto-detected if not provided)
        
        Returns:
            Tuple of (detailed_results_path, summary_results_path)
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset the classifier for processing a new video.
        """
        ...


from . import clip, color_classifier, color_map_utils, color_mapper