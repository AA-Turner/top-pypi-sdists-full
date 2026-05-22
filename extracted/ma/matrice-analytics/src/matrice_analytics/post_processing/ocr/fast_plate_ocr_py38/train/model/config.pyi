"""Auto-generated stub for module: config."""
from typing import Any

# Functions
def load_plate_config_from_yaml(yaml_path: Any) -> Any:
    """
    Reads and parses a YAML file containing the plate configuration.
    
    Args:
        yaml_path: Path to the YAML file containing the plate config.
    
    Returns:
        PlateOCRConfig: Parsed and validated plate configuration.
    
    Raises:
        FileNotFoundError: If the YAML file does not exist.
    """
    ...

# Classes
class PlateOCRConfig:
    # Model License Plate OCR config.

    def check_alphabet_and_pad(self: Any) -> 'Any': ...

    def num_channels(self: Any) -> int: ...

    def pad_idx(self: Any) -> int: ...

    def vocabulary_size(self: Any) -> int: ...

