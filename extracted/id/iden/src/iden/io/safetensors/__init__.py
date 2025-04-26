r"""Contain safetensors data loaders and savers."""

from __future__ import annotations

__all__ = [
    "NumpyLoader",
    "NumpySafetensorsLoader",
    "NumpySafetensorsSaver",
    "NumpySaver",
    "TorchLoader",
    "TorchSafetensorsLoader",
    "TorchSafetensorsSaver",
    "TorchSaver",
]

from iden.io.safetensors.loaders import NumpySafetensorsLoader
from iden.io.safetensors.loaders import NumpySafetensorsLoader as NumpyLoader
from iden.io.safetensors.loaders import TorchSafetensorsLoader
from iden.io.safetensors.loaders import TorchSafetensorsLoader as TorchLoader
from iden.io.safetensors.savers import NumpySafetensorsSaver
from iden.io.safetensors.savers import NumpySafetensorsSaver as NumpySaver
from iden.io.safetensors.savers import TorchSafetensorsSaver
from iden.io.safetensors.savers import TorchSafetensorsSaver as TorchSaver
