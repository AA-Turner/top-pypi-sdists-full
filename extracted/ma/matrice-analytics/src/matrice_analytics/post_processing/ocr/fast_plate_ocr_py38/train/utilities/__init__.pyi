"""Stub file for post_processing.ocr.fast_plate_ocr_py38.train.utilities directory."""
from typing import Any, Optional, Set, Union

# Functions
# From backend_utils
def reload_keras_backend(framework: Any) -> None:
    """
    Reload the Keras backend with a given framework.
    """
    ...

# From backend_utils
def set_jax_backend() -> None:
    """
    Set Keras backend to jax.
    """
    ...

# From backend_utils
def set_keras_backend(framework: Any) -> None:
    """
    Set the Keras backend to a given framework.
    """
    ...

# From backend_utils
def set_pytorch_backend() -> None:
    """
    Set Keras backend to pytorch.
    """
    ...

# From backend_utils
def set_tensorflow_backend() -> None:
    """
    Set Keras backend to tensorflow.
    """
    ...

# From utils
def display_predictions(image: Any.Any, plate: str, probs: Any.Any, low_conf_thresh: float) -> None:
    """
    Display plate and corresponding prediction.
    """
    ...

# From utils
def load_images_from_folder(img_dir: Any.Any, width: int, height: int, image_color_mode: Any = 'grayscale', keep_aspect_ratio: bool = False, interpolation_method: Any = 'linear', padding_color: Any = (114, 114, 114), shuffle: bool = False, limit: Optional[int] = None) -> Any[Any.Any]:
    """
    Return all images read from a directory. This uses the same read function used during training.
    """
    ...

# From utils
def load_keras_model(model_path: Union[str, Any.Any], plate_config: Any) -> Any.Any:
    """
    Utility helper function to load the keras OCR model.
    """
    ...

# From utils
def low_confidence_positions(probs: Any, thresh: Any = 0.3) -> Any.Any:
    """
    Returns indices of elements in `probs` less than `thresh`, indicating low confidence.
    """
    ...

# From utils
def one_hot_plate(plate: str, alphabet: str) -> list[list[int]]: ...

# From utils
def postprocess_model_output(prediction: Any.Any, alphabet: str, max_plate_slots: int, vocab_size: int) -> tuple[str, Any.Any]:
    """
    Return plate text and confidence scores from raw model output.
    """
    ...

# From utils
def target_transform(plate_text: str, max_plate_slots: int, alphabet: str, pad_char: str) -> Any.Any[Any.Any]: ...

from . import backend_utils, utils