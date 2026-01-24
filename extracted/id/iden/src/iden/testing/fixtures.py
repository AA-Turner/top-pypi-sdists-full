r"""Define some PyTest fixtures."""

from __future__ import annotations

__all__ = [
    "cloudpickle_available",
    "cloudpickle_not_available",
    "joblib_available",
    "joblib_not_available",
    "safetensors_available",
    "safetensors_not_available",
    "yaml_available",
    "yaml_not_available",
]

import pytest

from iden.utils.imports import (
    is_cloudpickle_available,
    is_joblib_available,
    is_safetensors_available,
    is_yaml_available,
)

cloudpickle_available: pytest.MarkDecorator = pytest.mark.skipif(
    not is_cloudpickle_available(), reason="Require cloudpickle"
)
cloudpickle_not_available: pytest.MarkDecorator = pytest.mark.skipif(
    is_cloudpickle_available(), reason="Skip if cloudpickle is available"
)
joblib_available: pytest.MarkDecorator = pytest.mark.skipif(
    not is_joblib_available(), reason="Require joblib"
)
joblib_not_available: pytest.MarkDecorator = pytest.mark.skipif(
    is_joblib_available(), reason="Skip if joblib is available"
)
safetensors_available: pytest.MarkDecorator = pytest.mark.skipif(
    not is_safetensors_available(), reason="Require safetensors"
)
safetensors_not_available: pytest.MarkDecorator = pytest.mark.skipif(
    is_safetensors_available(), reason="Skip if safetensors is available"
)
yaml_available: pytest.MarkDecorator = pytest.mark.skipif(
    not is_yaml_available(), reason="Require yaml"
)
yaml_not_available: pytest.MarkDecorator = pytest.mark.skipif(
    is_yaml_available(), reason="Skip if yaml is available"
)
