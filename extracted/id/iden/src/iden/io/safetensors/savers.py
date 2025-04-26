r"""Contain implementation of savers that use the safetensors format."""

from __future__ import annotations

__all__ = ["NumpySafetensorsSaver", "TorchSafetensorsSaver"]

from typing import TYPE_CHECKING
from unittest.mock import Mock

from coola.utils import check_numpy, check_torch, is_numpy_available, is_torch_available

from iden.io.base import BaseFileSaver
from iden.utils.imports import check_safetensors, is_safetensors_available

if TYPE_CHECKING:
    from pathlib import Path


if is_safetensors_available() and is_numpy_available():
    import numpy as np
    from safetensors import numpy as sn
else:  # pragma: no cover
    np = Mock()
    sn = Mock()

if is_safetensors_available() and is_torch_available():
    import torch
    from safetensors import torch as st
else:  # pragma: no cover
    st = Mock()
    torch = Mock()


class NumpySafetensorsSaver(BaseFileSaver[dict[str, np.ndarray]]):
    r"""Implement a file saver to save ``numpy.ndarray``s with the
    safetensors format.

    This saver can only save a dictionary of ``numpy.ndarray``s.

    Link: https://huggingface.co/docs/safetensors/en/index
    """

    def __init__(self) -> None:
        check_safetensors()
        check_numpy()

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def _save_file(self, to_save: dict[str, np.ndarray], path: Path) -> None:
        sn.save_file(to_save, path)


class TorchSafetensorsSaver(BaseFileSaver[dict[str, torch.Tensor]]):
    r"""Implement a file saver to save ``torch.Tensor``s with the
    safetensors format.

    This saver can only save a dictionary of ``torch.Tensor``s.

    Link: https://huggingface.co/docs/safetensors/en/index
    """

    def __init__(self) -> None:
        check_safetensors()
        check_torch()

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def _save_file(self, to_save: dict[str, torch.Tensor], path: Path) -> None:
        st.save_file(to_save, path)
