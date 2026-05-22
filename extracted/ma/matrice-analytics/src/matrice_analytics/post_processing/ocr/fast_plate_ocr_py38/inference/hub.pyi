"""Auto-generated stub for module: hub."""
from typing import Any, Optional

# Constants
OcrModel: Any

# Functions
def download_model(model_name: Any, save_directory: Optional[Any.Any] = None, force_download: bool = False) -> tuple[Any.Any, Any.Any]:
    """
    Download an OCR model and the config to a given directory.
    
    Args:
        model_name: Which model to download.
        save_directory: Directory to save the OCR model. It should point to a folder.
            If not supplied, this will point to '~/.cache/<model_name>'.
        force_download: Force and download the model if it already exists in
            `save_directory`.
    
    Returns:
        A tuple consisting of (model_downloaded_path, config_downloaded_path).
    """
    ...
