"""Auto-generated stub for module: utils."""
from typing import Any, Optional, Union

# Functions
def display_predictions(image: Any.Any, plate: str, probs: Any.Any, low_conf_thresh: float) -> None:
    """
    Display plate and corresponding prediction.
    """
    ...
def load_images_from_folder(img_dir: Any.Any, width: int, height: int, image_color_mode: Any = 'grayscale', keep_aspect_ratio: bool = False, interpolation_method: Any = 'linear', padding_color: Any = (114, 114, 114), shuffle: bool = False, limit: Optional[int] = None) -> Any[Any.Any]:
    """
    Return all images read from a directory. This uses the same read function used during training.
    """
    ...
def load_keras_model(model_path: Union[str, Any.Any], plate_config: Any) -> Any.Any:
    """
    Utility helper function to load the keras OCR model.
    """
    ...
def low_confidence_positions(probs: Any, thresh: Any = 0.3) -> Any.Any:
    """
    Returns indices of elements in `probs` less than `thresh`, indicating low confidence.
    """
    ...
def one_hot_plate(plate: str, alphabet: str) -> list[list[int]]: ...
def postprocess_model_output(prediction: Any.Any, alphabet: str, max_plate_slots: int, vocab_size: int) -> tuple[str, Any.Any]:
    """
    Return plate text and confidence scores from raw model output.
    """
    ...
def target_transform(plate_text: str, max_plate_slots: int, alphabet: str, pad_char: str) -> Any.Any[Any.Any]: ...
