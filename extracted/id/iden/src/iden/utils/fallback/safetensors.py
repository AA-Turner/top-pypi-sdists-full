r"""Contain fallback implementations used when ``safetensors``
dependency is not available."""

from __future__ import annotations

__all__ = ["safetensors"]

from types import ModuleType
from typing import Any, NoReturn

from iden.utils.imports import raise_error_safetensors_missing


def fake_function(*args: Any, **kwargs: Any) -> NoReturn:  # noqa: ARG001
    r"""Fake function that raises an error because safetensors is not
    installed.

    Args:
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Raises:
        RuntimeError: safetensors is required for this functionality.
    """
    raise_error_safetensors_missing()


# Create fake submodules
numpy: ModuleType = ModuleType("safetensors.numpy")
numpy.load_file = fake_function
numpy.save_file = fake_function

torch: ModuleType = ModuleType("safetensors.torch")
torch.load_file = fake_function
torch.save_file = fake_function

# Create a fake safetensors package with submodules as attributes
safetensors: ModuleType = ModuleType("safetensors")
safetensors.numpy = numpy
safetensors.torch = torch
