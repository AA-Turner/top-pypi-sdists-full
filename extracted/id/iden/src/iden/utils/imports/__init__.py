r"""Implement some utility functions to manage optional dependencies."""

from __future__ import annotations

__all__ = [
    "check_cloudpickle",
    "check_joblib",
    "check_safetensors",
    "check_yaml",
    "cloudpickle_available",
    "is_cloudpickle_available",
    "is_joblib_available",
    "is_safetensors_available",
    "is_yaml_available",
    "joblib_available",
    "raise_error_cloudpickle_missing",
    "raise_error_joblib_missing",
    "raise_error_safetensors_missing",
    "raise_error_yaml_missing",
    "safetensors_available",
    "yaml_available",
]

from iden.utils.imports.cloudpickle import (
    check_cloudpickle,
    cloudpickle_available,
    is_cloudpickle_available,
    raise_error_cloudpickle_missing,
)
from iden.utils.imports.joblib import (
    check_joblib,
    is_joblib_available,
    joblib_available,
    raise_error_joblib_missing,
)
from iden.utils.imports.safetensors import (
    check_safetensors,
    is_safetensors_available,
    raise_error_safetensors_missing,
    safetensors_available,
)
from iden.utils.imports.yaml import (
    check_yaml,
    is_yaml_available,
    raise_error_yaml_missing,
    yaml_available,
)
