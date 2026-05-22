"""Stub file for post_processing.ocr.fast_plate_ocr_py38.train.model directory."""
from typing import Any, Optional

# Constants
AnyModelConfig: Any = ...  # From model_schema
LayerConfig: Any = ...  # From model_schema

# Functions
# From config
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

# From layers
def build_norm_layer(norm_type: Any) -> Any.Any.Any: ...

# From loss
def cce_loss(vocabulary_size: int, label_smoothing: float = 0.01) -> Any:
    """
    Categorical cross-entropy loss.
    """
    ...

# From loss
def focal_cce_loss(vocabulary_size: int, alpha: float = 0.25, gamma: float = 2.0, label_smoothing: float = 0.01) -> Any:
    """
    Categorical focal cross-entropy loss.
    """
    ...

# From metric
def cat_acc_metric(max_plate_slots: int, vocabulary_size: int) -> Any:
    """
    Categorical accuracy metric.
    """
    ...

# From metric
def plate_acc_metric(max_plate_slots: int, vocabulary_size: int) -> Any:
    """
    Plate accuracy metric.
    """
    ...

# From metric
def plate_len_acc_metric(max_plate_slots: int, vocabulary_size: int, pad_token_index: int) -> Any:
    """
    Plate-length accuracy metric.
    """
    ...

# From metric
def top_3_k_metric(vocabulary_size: int) -> Any:
    """
    Top 3 K categorical accuracy metric.
    """
    ...

# From model_builders
def build_model(model_cfg: Any, plate_cfg: Any) -> Any.Any:
    """
    Build a Keras OCR model based on the specified model and plate configuration.
    """
    ...

# From model_schema
def load_model_config_from_yaml(yaml_path: Any) -> Any:
    """
    Loads, parses, and validates a YAML file defining a model architecture.
    
    Args:
        yaml_path: Path to the YAML file.
    
    Returns:
        AnyModelConfig: Parsed and validated model configuration.
    
    Raises:
        FileNotFoundError: If the YAML file does not exist.
    """
    ...

# Classes
# From config
class PlateOCRConfig:
    # Model License Plate OCR config.

    def check_alphabet_and_pad(self: Any) -> 'Any': ...

    def num_channels(self: Any) -> int: ...

    def pad_idx(self: Any) -> int: ...

    def vocabulary_size(self: Any) -> int: ...


# From layers
class AddCoords:
    # Add coords to a tensor, modified from paper: https://arxiv.org/abs/1807.03247

    def __init__(self: Any, with_r: Any = False) -> None: ...

    def build(self: Any, input_shape: Any) -> Any: ...

    def call(self: Any, input_tensor: Any) -> Any:
        """
        input_tensor: (batch, x_dim, y_dim, c)
        """
        ...


# From layers
class CoordConv2D:
    # CoordConv2D layer as in the paper, modified from paper: https://arxiv.org/abs/1807.03247

    def __init__(self: Any, with_r: bool = False, **conv_kwargs: Any) -> None: ...

    def call(self: Any, inputs: Any) -> Any: ...

    def get_config(self: Any) -> Any: ...


# From layers
class DyT:
    # Dynamic Tanh (DyT) is an element-wise operation as a drop-in replacement for normalization
    # layers in Transformers.
    #
    # Paper: https://arxiv.org/abs/2503.10622.

    def __init__(self: Any, alpha_init_value: float = 0.5, **kwargs: Any) -> None: ...

    def build(self: Any, input_shape: Any) -> Any: ...

    def call(self: Any, x: Any) -> Any: ...

    def get_config(self: Any) -> Any: ...


# From layers
class MLP:
    def __init__(self: Any, hidden_units: Any, dropout_rate: float = 0.1, activation: str = 'gelu', use_bias: bool = True, **kwargs: Any) -> None: ...

    def build(self: Any, input_shape: Any) -> Any: ...

    def call(self: Any, inputs: Any, training: Any = None) -> Any: ...

    def get_config(self: Any) -> Any: ...


# From layers
class MaxBlurPooling2D:
    def __init__(self: Any, pool_size: int = 2, filter_size: int = 3, padding: str = 'same', **kwargs: Any) -> None: ...

    def build(self: Any, input_shape: Any) -> Any: ...

    def call(self: Any, x: Any) -> Any: ...

    def compute_output_shape(self: Any, input_shape: Any) -> Any: ...

    def get_config(self: Any) -> Any: ...


# From layers
class PatchExtractor:
    # Extract non-overlapping patches from an image and flatten them.
    #
    # Modified from https://keras.io/examples/vision/image_classification_with_vision_transformer.

    def __init__(self: Any, patch_size: Any, **kwargs: Any) -> None: ...

    def call(self: Any, images: Any) -> Any: ...

    def get_config(self: Any) -> Any: ...


# From layers
class PositionEmbedding:
    def __init__(self: Any, sequence_length: Any, initializer: Any = 'glorot_uniform', **kwargs: Any) -> None: ...

    def build(self: Any, input_shape: Any) -> Any: ...

    def call(self: Any, inputs: Any, start_index: Any = 0) -> Any: ...

    def compute_output_shape(self: Any, input_shape: Any) -> Any: ...

    def get_config(self: Any) -> Any: ...


# From layers
class SqueezeExcite:
    # Applies squeeze and excitation to input feature maps as seen in https://arxiv.org/abs/1709.01507
    #
    # Note: this was taken from https://keras.io/examples/vision/patch_convnet.

    def __init__(self: Any, ratio: float = 1.0, **kwargs: Any) -> None: ...

    def build(self: Any, input_shape: Any) -> Any: ...

    def call(self: Any, x: Any) -> Any: ...

    def get_config(self: Any) -> Any: ...


# From layers
class StochasticDepth:
    def __init__(self: Any, drop_prob: float, **kwargs: Any) -> None: ...

    def call(self: Any, x: Any, training: Any = None) -> Any: ...

    def get_config(self: Any) -> Any: ...


# From layers
class TokenReducer:
    def __init__(self: Any, num_tokens: Any, projection_dim: Any, num_heads: Any = 2, **kwargs: Any) -> None: ...

    def build(self: Any, input_shape: Any) -> Any: ...

    def call(self: Any, inputs: Any) -> Any:
        """
        inputs: Tensor of shape (batch_size, seq_length, projection_dim)
        returns: Tensor of shape (batch_size, num_tokens, projection_dim)
        """
        ...

    def compute_output_shape(self: Any, input_shape: Any) -> Any: ...

    def get_config(self: Any) -> Any: ...


# From layers
class TransformerBlock:
    def __init__(self: Any, projection_dim: int, num_heads: int, mlp_units: Any[int], attention_dropout: float, mlp_dropout: float, drop_path_rate: float, norm_type: Optional[str] = 'layer_norm', activation: str = 'gelu', **kwargs: Any) -> None: ...

    def build(self: Any, input_shape: Any) -> None: ...

    def call(self: Any, x: Any, training: Any = None) -> Any: ...

    def get_config(self: Any) -> Any: ...


# From layers
class VocabularyProjection:
    def __init__(self: Any, vocabulary_size: int, dropout_rate: Optional[float] = None, **kwargs: Any) -> None: ...

    def build(self: Any, input_shape: Any) -> Any: ...

    def call(self: Any, x: Any, training: Any = None) -> Any: ...

    def get_config(self: Any) -> Any: ...


# From model_schema
class CCTModelConfig:
    ...

from . import config, layers, loss, metric, model_builders, model_schema