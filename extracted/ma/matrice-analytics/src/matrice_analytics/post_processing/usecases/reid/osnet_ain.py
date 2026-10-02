"""OSNet-AIN x1.0 architecture, vendored for person re-identification.

Adapted from Torchreid (https://github.com/KaiyangZhou/deep-person-reid),
MIT licensed, Copyright (c) 2018 Kaiyang Zhou. Reference:

    Zhou et al. "Omni-Scale Feature Learning for Person Re-Identification",
    ICCV 2019.
    Zhou et al. "Learning Generalisable Omni-Scale Representations for
    Person Re-Identification", TPAMI 2021.

**Why vendored rather than depending on ``torchreid``**: ``torchreid`` is not
in ``APPROVED_DEPS.toml`` and pulls a large dependency tree (including
``gdown``, which fetches from Google Drive) into a package whose runtime
dependencies are otherwise just numpy and scipy. Only the inference path is
needed here, so the architecture is vendored and the training-only pieces
(``init_pretrained_weights``, the gdown URLs, the softmax/triplet training
heads, weight init) are dropped.

**The structure below must match the published checkpoint exactly.** A
``.pth`` is a state dict, not a self-contained model: every module name and
channel count here is load-bearing, because ``load_state_dict(strict=True)``
matches on parameter names. Do not "tidy" the layer names or restructure the
blocks -- a rename silently breaks checkpoint loading.

``AIN`` = Adaptive Instance Normalization: the network learns *where* to apply
instance normalization (``OSBlockINin`` vs plain ``OSBlock``, plus
``conv1_IN``) rather than hard-coding it, which is what buys the cross-domain
robustness this use case depends on.
"""

from __future__ import annotations

from torch import nn
from torch.nn import functional as F

__all__ = ["OSNET_AIN_X1_0_FEATURE_DIM", "OSNet", "osnet_ain_x1_0"]

#: Embedding width emitted by :func:`osnet_ain_x1_0` in ``eval()`` mode.
OSNET_AIN_X1_0_FEATURE_DIM = 512


# --------------------------------------------------------------------------
# Basic layers
# --------------------------------------------------------------------------
class ConvLayer(nn.Module):
    """Convolution layer (conv + bn + relu)."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: int,
        stride: int = 1,
        padding: int = 0,
        groups: int = 1,
        IN: bool = False,  # noqa: N803  (upstream name; kept for clarity)
    ) -> None:
        super().__init__()
        self.conv = nn.Conv2d(
            in_channels,
            out_channels,
            kernel_size,
            stride=stride,
            padding=padding,
            bias=False,
            groups=groups,
        )
        if IN:
            self.bn = nn.InstanceNorm2d(out_channels, affine=True)
        else:
            self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        return self.relu(x)


class Conv1x1(nn.Module):
    """1x1 convolution + bn + relu."""

    def __init__(
        self, in_channels: int, out_channels: int, stride: int = 1, groups: int = 1
    ) -> None:
        super().__init__()
        self.conv = nn.Conv2d(
            in_channels, out_channels, 1, stride=stride, padding=0, bias=False, groups=groups
        )
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        return self.relu(x)


class Conv1x1Linear(nn.Module):
    """1x1 convolution + bn (without non-linearity)."""

    def __init__(
        self, in_channels: int, out_channels: int, stride: int = 1, bn: bool = True
    ) -> None:
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, 1, stride=stride, padding=0, bias=False)
        self.bn = None
        if bn:
            self.bn = nn.BatchNorm2d(out_channels)

    def forward(self, x):
        x = self.conv(x)
        if self.bn is not None:
            x = self.bn(x)
        return x


class LightConv3x3(nn.Module):
    """Lightweight 3x3 convolution: 1x1 (linear) + depthwise 3x3 (nonlinear)."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 1, stride=1, padding=0, bias=False)
        self.conv2 = nn.Conv2d(
            out_channels, out_channels, 3, stride=1, padding=1, bias=False, groups=out_channels
        )
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.bn(x)
        return self.relu(x)


class LightConvStream(nn.Module):
    """Lightweight convolution stream (``depth`` stacked ``LightConv3x3``)."""

    def __init__(self, in_channels: int, out_channels: int, depth: int) -> None:
        super().__init__()
        if depth < 1:
            raise ValueError(f"depth must be >= 1, but got {depth}")
        layers = [LightConv3x3(in_channels, out_channels)]
        for _ in range(depth - 1):
            layers += [LightConv3x3(out_channels, out_channels)]
        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        return self.layers(x)


# --------------------------------------------------------------------------
# Building blocks for omni-scale feature learning
# --------------------------------------------------------------------------
class ChannelGate(nn.Module):
    """Mini-network generating channel-wise gates conditioned on the input."""

    def __init__(
        self,
        in_channels: int,
        num_gates: int | None = None,
        return_gates: bool = False,
        gate_activation: str = "sigmoid",
        reduction: int = 16,
        layer_norm: bool = False,
    ) -> None:
        super().__init__()
        if num_gates is None:
            num_gates = in_channels
        self.return_gates = return_gates
        self.global_avgpool = nn.AdaptiveAvgPool2d(1)
        self.fc1 = nn.Conv2d(
            in_channels, in_channels // reduction, kernel_size=1, bias=True, padding=0
        )
        self.norm1 = None
        if layer_norm:
            self.norm1 = nn.LayerNorm((in_channels // reduction, 1, 1))
        self.relu = nn.ReLU()
        self.fc2 = nn.Conv2d(
            in_channels // reduction, num_gates, kernel_size=1, bias=True, padding=0
        )
        if gate_activation == "sigmoid":
            self.gate_activation = nn.Sigmoid()
        elif gate_activation == "relu":
            self.gate_activation = nn.ReLU()
        elif gate_activation == "linear":
            self.gate_activation = None
        else:
            raise RuntimeError(f"Unknown gate activation: {gate_activation}")

    def forward(self, x):
        identity = x
        x = self.global_avgpool(x)
        x = self.fc1(x)
        if self.norm1 is not None:
            x = self.norm1(x)
        x = self.relu(x)
        x = self.fc2(x)
        if self.gate_activation is not None:
            x = self.gate_activation(x)
        if self.return_gates:
            return x
        return identity * x


class OSBlock(nn.Module):
    """Omni-scale feature learning block."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        reduction: int = 4,
        T: int = 4,  # noqa: N803  (upstream name)
        **kwargs,
    ) -> None:
        super().__init__()
        _ = kwargs
        if T < 1:
            raise ValueError(f"T must be >= 1, got {T}")
        if out_channels < reduction or out_channels % reduction != 0:
            raise ValueError(f"out_channels={out_channels} incompatible with reduction={reduction}")
        mid_channels = out_channels // reduction

        self.conv1 = Conv1x1(in_channels, mid_channels)
        self.conv2 = nn.ModuleList()
        for t in range(1, T + 1):
            self.conv2 += [LightConvStream(mid_channels, mid_channels, t)]
        self.gate = ChannelGate(mid_channels)
        self.conv3 = Conv1x1Linear(mid_channels, out_channels)
        self.downsample = None
        if in_channels != out_channels:
            self.downsample = Conv1x1Linear(in_channels, out_channels)

    def forward(self, x):
        identity = x
        x1 = self.conv1(x)
        x2 = 0
        for conv2_t in self.conv2:
            x2_t = conv2_t(x1)
            x2 = x2 + self.gate(x2_t)
        x3 = self.conv3(x2)
        if self.downsample is not None:
            identity = self.downsample(identity)
        out = x3 + identity
        return F.relu(out)


class OSBlockINin(nn.Module):
    """Omni-scale feature learning block with instance normalization."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        reduction: int = 4,
        T: int = 4,  # noqa: N803  (upstream name)
        **kwargs,
    ) -> None:
        super().__init__()
        _ = kwargs
        if T < 1:
            raise ValueError(f"T must be >= 1, got {T}")
        if out_channels < reduction or out_channels % reduction != 0:
            raise ValueError(f"out_channels={out_channels} incompatible with reduction={reduction}")
        mid_channels = out_channels // reduction

        self.conv1 = Conv1x1(in_channels, mid_channels)
        self.conv2 = nn.ModuleList()
        for t in range(1, T + 1):
            self.conv2 += [LightConvStream(mid_channels, mid_channels, t)]
        self.gate = ChannelGate(mid_channels)
        self.conv3 = Conv1x1Linear(mid_channels, out_channels, bn=False)
        self.downsample = None
        if in_channels != out_channels:
            self.downsample = Conv1x1Linear(in_channels, out_channels)
        self.IN = nn.InstanceNorm2d(out_channels, affine=True)

    def forward(self, x):
        identity = x
        x1 = self.conv1(x)
        x2 = 0
        for conv2_t in self.conv2:
            x2_t = conv2_t(x1)
            x2 = x2 + self.gate(x2_t)
        x3 = self.conv3(x2)
        x3 = self.IN(x3)  # IN inside the residual branch -- this is the "AIN" part
        if self.downsample is not None:
            identity = self.downsample(identity)
        out = x3 + identity
        return F.relu(out)


# --------------------------------------------------------------------------
# Network architecture
# --------------------------------------------------------------------------
class OSNet(nn.Module):
    """Omni-Scale Network.

    In ``eval()`` mode ``forward`` returns the ``feature_dim``-wide embedding
    (the classifier head is skipped), which is exactly what re-identification
    needs. Keep the module in ``eval()``.
    """

    def __init__(
        self,
        num_classes: int,
        blocks,
        layers,
        channels,
        feature_dim: int = 512,
        conv1_IN: bool = False,  # noqa: N803  (upstream name)
        **kwargs,
    ) -> None:
        super().__init__()
        _ = kwargs
        num_blocks = len(blocks)
        if num_blocks != len(layers) or num_blocks != len(channels) - 1:
            raise ValueError("blocks/layers/channels are inconsistent")
        self.feature_dim = feature_dim

        self.conv1 = ConvLayer(3, channels[0], 7, stride=2, padding=3, IN=conv1_IN)
        self.maxpool = nn.MaxPool2d(3, stride=2, padding=1)
        self.conv2 = self._make_layer(blocks[0], layers[0], channels[0], channels[1])
        self.pool2 = nn.Sequential(Conv1x1(channels[1], channels[1]), nn.AvgPool2d(2, stride=2))
        self.conv3 = self._make_layer(blocks[1], layers[1], channels[1], channels[2])
        self.pool3 = nn.Sequential(Conv1x1(channels[2], channels[2]), nn.AvgPool2d(2, stride=2))
        self.conv4 = self._make_layer(blocks[2], layers[2], channels[2], channels[3])
        self.conv5 = Conv1x1(channels[3], channels[3])
        self.global_avgpool = nn.AdaptiveAvgPool2d(1)
        self.fc = self._construct_fc_layer(self.feature_dim, channels[3], dropout_p=None)
        # Retained so `load_state_dict(strict=True)` matches the published
        # checkpoint, which carries classifier weights. Unused at inference.
        self.classifier = nn.Linear(self.feature_dim, num_classes)

    @staticmethod
    def _make_layer(blocks, layer, in_channels: int, out_channels: int) -> nn.Sequential:
        _ = layer
        layers = [blocks[0](in_channels, out_channels)]
        for i in range(1, len(blocks)):
            layers += [blocks[i](out_channels, out_channels)]
        return nn.Sequential(*layers)

    def _construct_fc_layer(self, fc_dims, input_dim: int, dropout_p=None):
        if fc_dims is None or fc_dims < 0:
            self.feature_dim = input_dim
            return None
        if isinstance(fc_dims, int):
            fc_dims = [fc_dims]
        layers = []
        for dim in fc_dims:
            layers.append(nn.Linear(input_dim, dim))
            layers.append(nn.BatchNorm1d(dim))
            layers.append(nn.ReLU())
            if dropout_p is not None:
                layers.append(nn.Dropout(p=dropout_p))
            input_dim = dim
        self.feature_dim = fc_dims[-1]
        return nn.Sequential(*layers)

    def featuremaps(self, x):
        x = self.conv1(x)
        x = self.maxpool(x)
        x = self.conv2(x)
        x = self.pool2(x)
        x = self.conv3(x)
        x = self.pool3(x)
        x = self.conv4(x)
        return self.conv5(x)

    def forward(self, x):
        x = self.featuremaps(x)
        v = self.global_avgpool(x)
        v = v.view(v.size(0), -1)
        if self.fc is not None:
            v = self.fc(v)
        if not self.training:
            return v
        return self.classifier(v)


def osnet_ain_x1_0(num_classes: int = 1000, **kwargs) -> OSNet:
    """OSNet-AIN x1.0 -- ~2.2M params, ~0.98 GFLOPs at 256x128, 512-d output.

    ``num_classes`` only sizes the (inference-unused) classifier head, but it
    must match the checkpoint for ``strict=True`` loading. Verified against
    the author's published MSMT17 checkpoint: **4101 identities**. Callers
    should read the width from ``classifier.weight`` rather than hardcoding
    it -- see ``model.load_reid_model``.
    """
    return OSNet(
        num_classes,
        blocks=[[OSBlockINin, OSBlockINin], [OSBlock, OSBlockINin], [OSBlockINin, OSBlock]],
        layers=[2, 2, 2],
        channels=[64, 256, 384, 512],
        conv1_IN=True,
        **kwargs,
    )
