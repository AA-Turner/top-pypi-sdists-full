"""Auto-generated stub for module: visualize_augmentation."""
from typing import Any, Optional

# Functions
def display_images(images: list[Any.Any[Any.Any]], augmented_images: list[Any.Any[Any.Any]], columns: int, rows: int, show_original: bool) -> None: ...
def load_images(img_dir: Any.Any, num_images: int, shuffle: bool, plate_config: Any, augmentation: Any.Any) -> tuple[list[Any.Any[Any.Any]], list[Any.Any[Any.Any]]]: ...
def visualize_augmentation(img_dir: Any.Any, plate_config_file: Any.Any, num_images: int, augmentation_path: Optional[Any.Any], shuffle: bool, columns: int, rows: int, seed: Optional[int], show_original: bool) -> None:
    """
    Visualize augmentation pipeline applied to raw images.
    """
    ...
