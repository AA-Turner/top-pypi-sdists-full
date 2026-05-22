"""Auto-generated stub for module: config."""
from typing import Any

# Classes
class PlateOCRConfig:
    # Plate OCR Config used for inference.
    #
    # This dataclass is used to read and parse the config file used for training the OCR model.
    # We prefer to keep the inference package with minimal dependencies and avoid using Pydantic here.

    def from_yaml(cls: Any, path: Any) -> 'Any':
        """
        Read and parse a yaml containing the Plate OCR config.
        """
        ...

    def num_channels(self: Any) -> int: ...

    def pad_idx(self: Any) -> int: ...

    def vocabulary_size(self: Any) -> int: ...

