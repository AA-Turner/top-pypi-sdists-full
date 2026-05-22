"""Stub file for post_processing.ocr.fast_plate_ocr_py38.core directory."""
from typing import Any, Callable, Optional, Union

# Constants
BatchArray: Any = ...  # From types
BatchOrImgLike: Any = ...  # From types
ImageColorMode: Any = ...  # From types
ImageInterpolation: Any = ...  # From types
ImgLike: Any = ...  # From types
KerasDtypes: Any = ...  # From types
PaddingColor: Any = ...  # From types
PathLike: Any = ...  # From types
TensorDataFormat: Any = ...  # From types

# Functions
# From process
def postprocess_output(model_output: Any.Any, max_plate_slots: int, model_alphabet: str, return_confidence: bool = False) -> tuple[list[str], Union[Any.Any, list[str]]]:
    """
    Decodes model predictions into licence-plate strings.
    
    Args:
        model_output: Raw output tensor from the model.
        max_plate_slots: Maximum number of character positions.
        model_alphabet: Alphabet used by the model.
        return_confidence: If ``True``, also return per-character confidence scores.
            Defaults to ``False``.
    
    Returns:
        If ``return_confidence`` is ``False``: a list of decoded plate strings.
            If ``True``: a two-tuple ``(plates, probs)`` where
    
            * ``plates`` is the list of decoded strings, and
            * ``probs`` is an array of shape ``(N, max_plate_slots)`` with the corresponding
              confidence scores.
    """
    ...

# From process
def preprocess_image(images: Any.Any) -> Any.Any:
    """
    Converts image data to the format expected by the model.
    
    The model itself handles pixel-value normalisation, so this function only ensures the
    batch-dimension and dtype are correct.
    
    Args:
        images: Image or batch of images with shape ``(H, W, C)`` or ``(N, H, W, C)``.
    
    Returns:
        A NumPy array with shape ``(N, H, W, C)`` and dtype ``uint8``.
    
    Raises:
        ValueError: If the input does not have 3 or 4 dimensions.
    """
    ...

# From process
def read_and_resize_plate_image(image_path: Any, img_height: int, img_width: int, image_color_mode: Any = 'grayscale', keep_aspect_ratio: bool = False, interpolation_method: Any = 'linear', padding_color: Any = (114, 114, 114)) -> Any.Any:
    """
    Reads an image from disk and resizes it for model input.
    
    Args:
        image_path: Path to the image.
        img_height: Desired output height.
        img_width: Desired output width.
        image_color_mode: ``"grayscale"`` or ``"rgb"``. Defaults to ``"grayscale"``.
        keep_aspect_ratio: Whether to preserve aspect ratio via letter-boxing. Defaults to
            ``False``.
        interpolation_method: Interpolation method to use. Defaults to ``"linear"``.
        padding_color: Colour used for padding when aspect ratio is preserved. Defaults to
            ``(114, 114, 114)``.
    
    Returns:
        The resized (and possibly padded) image with shape ``(H, W, C)``.
    """
    ...

# From process
def read_plate_image(image_path: Any, image_color_mode: Any = 'grayscale') -> Any.Any:
    """
    Reads an image from disk in the requested colour mode.
    
    Args:
        image_path: Path to the image file.
        image_color_mode: ``"grayscale"`` for single-channel or ``"rgb"`` for three-channel
            colour. Defaults to ``"grayscale"``.
    
    Returns:
        The image as a NumPy array.
            Grayscale images have shape ``(H, W)``, RGB images have shape ``(H, W, 3)``.
    
    Raises:
        FileNotFoundError: If the image file does not exist.
        ValueError: If the image cannot be decoded.
    """
    ...

# From process
def resize_image(img: Any.Any, img_height: int, img_width: int, image_color_mode: Any = 'grayscale', keep_aspect_ratio: bool = False, interpolation_method: Any = 'linear', padding_color: Any = (114, 114, 114)) -> Any.Any:
    """
    Resizes an in-memory image with optional aspect-ratio preservation and padding.
    
    Args:
        img: Input image.
        img_height: Target image height.
        img_width: Target image width.
        image_color_mode: Output colour mode, ``"grayscale"`` or ``"rgb"``.
        keep_aspect_ratio: If ``True``, maintain the original aspect ratio using letter-box
            padding. Defaults to ``False``.
        interpolation_method: Interpolation method used for resizing. Defaults to ``"linear"``.
        padding_color: Padding colour (scalar for grayscale, tuple for RGB). Defaults to
            ``(114, 114, 114)``.
    
    Returns:
        The resized image with shape ``(H, W, C)`` (a channel axis is added for grayscale).
    
    Raises:
        ValueError: If ``padding_color`` length is not 3 for RGB output.
    """
    ...

# From utils
def log_time_taken(process_name: str) -> Any[None]:
    """
    A concise context manager to time code snippets and log the result.
    
    Usage:
        ```python
        with log_time_taken("process_name"):
            # Code snippet to be timed
        ```
    
    Args:
        process_name: Name of the process being timed.
    """
    ...

# From utils
def measure_time() -> Any[Callable[[], float]]:
    """
    A context manager for measuring execution time (in milliseconds) within its code block.
    
    Usage:
        ```python
        with measure_time() as timer:
            # Code snippet to be timed
        print(f"Code took: {timer()} ms")
        ```
    
    Returns:
        A function that returns the elapsed time in milliseconds.
    """
    ...

# From utils
def safe_write(file: Union[str, Any.Any[str]], mode: str = 'wb', encoding: Optional[str] = None, **kwargs: Any) -> Any[Any]:
    """
    Context manager for safe file writing.
    
    Opens the specified file for writing and yields a file object.
    If an exception occurs during writing, the file is removed before raising the exception.
    
    Args:
        file: Path to the file to write.
        mode: File open mode (e.g. ``"wb"``, ``"w"``, etc.). Defaults to ``"wb"``.
        encoding: Encoding to use (for text modes). Ignored in binary mode.
        **kwargs: Additional arguments passed to ``open()``.
    
    Returns:
        A writable file object.
    """
    ...

from . import process, types, utils