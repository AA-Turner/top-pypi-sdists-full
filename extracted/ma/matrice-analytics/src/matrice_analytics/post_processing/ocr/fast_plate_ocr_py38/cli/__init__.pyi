"""Stub file for post_processing.ocr.fast_plate_ocr_py38.cli directory."""
from typing import Any, Callable, Optional

# Constants
console: Any = ...  # From dataset_stats
console: Any = ...  # From validate_dataset

# Functions
# From cli
def main_cli() -> Any:
    """
    FastPlateOCR CLI.
    """
    ...

# From dataset_stats
def dataset_stats(annotations_path: Any, plate_config_file: Any, top_chars: int, workers: int) -> None:
    """
    Display statistics for a `fast-plate-ocr` dataset.
    """
    ...

# From export
def export(model_path: Any.Any, export_format: str, simplify: bool, plate_config_file: Any.Any, save_dir: Any.Any, dynamic_batch: bool, skip_validation: bool, onnx_input_dtype: str, onnx_data_format: Any) -> None:
    """
    Export Keras models to other formats.
    """
    ...

# From export
def export_coreml(model: Any.Any, plate_config: Any, out_file: Any.Any, skip_validation: bool = False) -> None: ...

# From export
def export_onnx(model: Any.Any, plate_config: Any, out_file: Any.Any, simplify: bool, dynamic_batch: bool, skip_validation: bool = False, onnx_input_dtype: str = 'uint8', onnx_data_format: Any = 'channels_last') -> None: ...

# From export
def export_tflite(model: Any.Any, plate_config: Any, out_file: Any.Any, skip_validation: bool = False) -> None: ...

# From train
def train(model_config_file: Any.Any, plate_config_file: Any.Any, train_annotations: Any.Any, val_annotations: Any.Any, validation_freq: int, augmentation_path: Optional[Any.Any], lr: float, final_lr_factor: float, warmup_fraction: float, weight_decay: float, clipnorm: float, loss: str, focal_alpha: float, focal_gamma: float, label_smoothing: float, mixed_precision_policy: Optional[str], batch_size: int, workers: int, use_multiprocessing: bool, max_queue_size: int, output_dir: Any.Any, epochs: int, tensorboard: bool, tensorboard_dir: Any.Any, early_stopping_patience: int, early_stopping_metric: str, weights_path: Optional[Any.Any], use_ema: bool, wd_ignore: str, seed: Optional[int]) -> None:
    """
    Train the License Plate OCR model.
    """
    ...

# From utils
def print_params(table_title: str = 'Parameters Table', c1_title: str = 'Variable', c2_title: str = 'Value') -> Callable:
    """
    A decorator that prints the parameters of a function in a formatted table
    using the rich library.
    
    Args:
        c1_title (str, optional): Title of the first column. Defaults to "Variable".
        c2_title (str, optional): Title of the second column. Defaults to "Value".
        table_title (str, optional): Title of the table. Defaults to "Parameters Table".
    
    Returns:
        Callable: The wrapped function with parameter printing functionality.
    """
    ...

# From utils
def print_train_details(augmentation: Any.Any, config: dict[str, Any]) -> None: ...

# From utils
def print_variables_as_table(c1_title: str, c2_title: str, title: str = 'Variables Table', **kwargs: Any) -> None:
    """
    Prints variables in a formatted table using the rich library.
    
    Args:
        c1_title (str): Title of the first column.
        c2_title (str): Title of the second column.
        title (str): Title of the table.
        **kwargs (Any): Variable names and values to be printed.
    """
    ...

# From utils
def requires(*modules: Any) -> Callable:
    """
    Decorator that checks if given modules are importable. If not, raises ModuleNotFoundError with
    a hint to install the package(s).
    
    Args:
        modules (str): Names of modules to check (via importlib.util.find_spec).
        pkg_name (Optional[Sequence[str]]): Names of packages to suggest installing.
    
    Returns:
        Callable: The wrapped function that checks for module availability.
    """
    ...

# From utils
def seed_everything(seed: int) -> None:
    """
    Seed random number generators for reproducibility.
    
    Args:
        seed (int): The seed value to set.
    """
    ...

# From valid
def valid(model_path: Any.Any, plate_config_file: Any.Any, annotations_path: Any.Any, batch_size: int, workers: int, use_multiprocessing: bool, max_queue_size: int) -> None:
    """
    Validate the trained OCR model on a labeled set.
    """
    ...

# From validate_dataset
def partial_decode_ok(path: Any) -> tuple[bool, Optional[tuple[int, int]]]: ...

# From validate_dataset
def rich_report(errors: Any, warnings: Any) -> Any: ...

# From validate_dataset
def validate_dataset(annotations_file: Any, plate_config_file: Any, warn_only: bool, export_fixed: Optional[str], min_height: int, min_width: int) -> Any:
    """
    Script to validate the dataset before training.
    """
    ...

# From visualize_augmentation
def display_images(images: list[Any.Any[Any.Any]], augmented_images: list[Any.Any[Any.Any]], columns: int, rows: int, show_original: bool) -> None: ...

# From visualize_augmentation
def load_images(img_dir: Any.Any, num_images: int, shuffle: bool, plate_config: Any, augmentation: Any.Any) -> tuple[list[Any.Any[Any.Any]], list[Any.Any[Any.Any]]]: ...

# From visualize_augmentation
def visualize_augmentation(img_dir: Any.Any, plate_config_file: Any.Any, num_images: int, augmentation_path: Optional[Any.Any], shuffle: bool, columns: int, rows: int, seed: Optional[int], show_original: bool) -> None:
    """
    Visualize augmentation pipeline applied to raw images.
    """
    ...

# From visualize_predictions
def visualize_predictions(model_path: Any.Any, plate_config_file: Any.Any, img_dir: Any.Any, low_conf_thresh: float, filter_conf: Optional[float]) -> Any:
    """
    Visualize OCR model predictions on unlabeled data.
    """
    ...

from . import cli, dataset_stats, export, train, utils, valid, validate_dataset, visualize_augmentation, visualize_predictions