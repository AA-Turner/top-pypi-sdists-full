"""Stub file for post_processing.ocr.fast_plate_ocr_py38.train.data directory."""
from typing import Any, Optional, Union

# Functions
# From augmentation
def default_train_augmentation(img_color_mode: Any) -> Any.Any:
    """
    Default training augmentation pipeline.
    """
    ...

# Classes
# From dataset
class PlateRecognitionPyDataset:
    # Custom PyDataset for OCR license plate recognition.

    def __init__(self: Any, annotations_file: Union[str, Any.Any], plate_config: Any, batch_size: int, transform: Optional[Any.Any] = None, shuffle: bool = True, **kwargs: Any) -> None: ...

    def on_epoch_begin(self: Any) -> None: ...


from . import augmentation, dataset