"""Auto-generated stub for module: dataset."""
from typing import Any, Optional, Union

# Classes
class PlateRecognitionPyDataset:
    # Custom PyDataset for OCR license plate recognition.

    def __init__(self: Any, annotations_file: Union[str, Any.Any], plate_config: Any, batch_size: int, transform: Optional[Any.Any] = None, shuffle: bool = True, **kwargs: Any) -> None: ...

    def on_epoch_begin(self: Any) -> None: ...

