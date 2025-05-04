r"""Define some PyTest fixtures."""

from __future__ import annotations

__all__ = ["cloudpickle_available", "joblib_available", "safetensors_available", "yaml_available"]

import pytest

from iden.utils.imports import (
    is_cloudpickle_available,
    is_joblib_available,
    is_safetensors_available,
    is_yaml_available,
)

cloudpickle_available = pytest.mark.skipif(
    not is_cloudpickle_available(), reason="Require cloudpickle"
)
joblib_available = pytest.mark.skipif(not is_joblib_available(), reason="Require joblib")
safetensors_available = pytest.mark.skipif(
    not is_safetensors_available(), reason="Require safetensors"
)
yaml_available = pytest.mark.skipif(not is_yaml_available(), reason="Require yaml")
