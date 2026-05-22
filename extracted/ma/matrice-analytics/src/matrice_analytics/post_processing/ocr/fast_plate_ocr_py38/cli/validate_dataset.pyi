"""Auto-generated stub for module: validate_dataset."""
from typing import Any, Optional

# Constants
console: Any

# Functions
def partial_decode_ok(path: Any) -> tuple[bool, Optional[tuple[int, int]]]: ...
def rich_report(errors: Any, warnings: Any) -> Any: ...
def validate_dataset(annotations_file: Any, plate_config_file: Any, warn_only: bool, export_fixed: Optional[str], min_height: int, min_width: int) -> Any:
    """
    Script to validate the dataset before training.
    """
    ...
