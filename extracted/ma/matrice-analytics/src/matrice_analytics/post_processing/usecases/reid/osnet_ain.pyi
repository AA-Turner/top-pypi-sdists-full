"""Auto-generated stub for module: osnet_ain."""
from typing import Any

# Constants
OSNET_AIN_X1_0_FEATURE_DIM: int

# Functions
def osnet_ain_x1_0(num_classes: int = 1000, **kwargs: Any) -> Any:
    """
    OSNet-AIN x1.0 -- ~2.2M params, ~0.98 GFLOPs at 256x128, 512-d output.
    
        ``num_classes`` only sizes the (inference-unused) classifier head, but it
        must match the checkpoint for ``strict=True`` loading. Verified against
        the author's published MSMT17 checkpoint: **4101 identities**. Callers
        should read the width from ``classifier.weight`` rather than hardcoding
        it -- see ``model.load_reid_model``.
    """
    ...

# Classes
class ChannelGate:
    # Mini-network generating channel-wise gates conditioned on the input.

    def __init__(self: Any, in_channels: int, num_gates: int | None = None, return_gates: bool = False, gate_activation: str = 'sigmoid', reduction: int = 16, layer_norm: bool = False) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...

class Conv1x1:
    # 1x1 convolution + bn + relu.

    def __init__(self: Any, in_channels: int, out_channels: int, stride: int = 1, groups: int = 1) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...

class Conv1x1Linear:
    # 1x1 convolution + bn (without non-linearity).

    def __init__(self: Any, in_channels: int, out_channels: int, stride: int = 1, bn: bool = True) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...

class ConvLayer:
    # Convolution layer (conv + bn + relu).

    def __init__(self: Any, in_channels: int, out_channels: int, kernel_size: int, stride: int = 1, padding: int = 0, groups: int = 1, IN: bool = False) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...

class LightConv3x3:
    # Lightweight 3x3 convolution: 1x1 (linear) + depthwise 3x3 (nonlinear).

    def __init__(self: Any, in_channels: int, out_channels: int) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...

class LightConvStream:
    # Lightweight convolution stream (``depth`` stacked ``LightConv3x3``).

    def __init__(self: Any, in_channels: int, out_channels: int, depth: int) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...

class OSBlock:
    # Omni-scale feature learning block.

    def __init__(self: Any, in_channels: int, out_channels: int, reduction: int = 4, T: int = 4, **kwargs: Any) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...

class OSBlockINin:
    # Omni-scale feature learning block with instance normalization.

    def __init__(self: Any, in_channels: int, out_channels: int, reduction: int = 4, T: int = 4, **kwargs: Any) -> None: ...

    def forward(self: Any, x: Any) -> Any: ...

class OSNet:
    # Omni-Scale Network.
    #
    #     In ``eval()`` mode ``forward`` returns the ``feature_dim``-wide embedding
    #     (the classifier head is skipped), which is exactly what re-identification
    #     needs. Keep the module in ``eval()``.

    def __init__(self: Any, num_classes: int, blocks: Any, layers: Any, channels: Any, feature_dim: int = 512, conv1_IN: bool = False, **kwargs: Any) -> None: ...

    def featuremaps(self: Any, x: Any) -> Any: ...

    def forward(self: Any, x: Any) -> Any: ...

