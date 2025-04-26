r"""Define some PyTest fixtures."""

from __future__ import annotations

__all__ = ["safetensors_available", "yaml_available"]

import pytest

from iden.utils.imports import is_safetensors_available, is_yaml_available

safetensors_available = pytest.mark.skipif(
    not is_safetensors_available(), reason="Require safetensors"
)
yaml_available = pytest.mark.skipif(not is_yaml_available(), reason="Require yaml")
