"""Auto-generated stub for module: clip."""
from typing import Any, Dict, List, Optional

# Constants
CLIPProcessor: None
Image: None
ir_as_file: None
ir_files: None
ort: None

# Functions
def load_model_from_checkpoint(checkpoint_url: str, providers: Optional[List] = None) -> Any:
    """
    Load an ONNX model from a URL directly into memory without writing locally.
    Enforces the specified providers (e.g., CUDAExecutionProvider) for execution.
    """
    ...
def preprocess_crop_paper_vcr(crop_rgb: Any, output_size: Any = (224, 224), contrast_alpha: Any = 1.3, gaussian_kernel: Any = (5, 5), sat_scale: Any = 0.9, val_scale: Any = 1.0) -> Any: ...
def try_install_clip_dependencies() -> Any:
    """
    Attempt to install missing CLIP dependencies.
    Only called when ClipProcessor is actually instantiated (lazy installation).
    Uses singleton pattern to ensure installation only happens ONCE per session.
    Returns True if successful, False otherwise.
    """
    ...

# Classes
class ClipProcessor:
    def __init__(self: Any, image_model_path: str = 'https://s3.us-west-2.amazonaws.com/testing.resources/datasets/clip_image.onnx', text_model_path: str = 'https://s3.us-west-2.amazonaws.com/testing.resources/datasets/clip_text.onnx', processor_dir: Optional[str] = None, providers: Optional[List[str]] = None) -> None: ...

    def process_color_in_frame(self: Any, detections: Any, input_bytes: Any, _zones: Optional[Dict[str, List[List[float]]]], _stream_info: Any) -> Any: ...

    def run_image_onnx_on_crops(self: Any, crops: Any) -> Any: ...

