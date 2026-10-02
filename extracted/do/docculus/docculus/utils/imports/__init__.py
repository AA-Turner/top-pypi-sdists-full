r"""Helpers to detect and validate optional dependencies."""

from __future__ import annotations

__all__ = [
    "check_faker",
    "check_persista",
    "faker_available",
    "is_faker_available",
    "is_persista_available",
    "persista_available",
    "raise_faker_missing_error",
    "raise_persista_missing_error",
]

from docculus.utils.imports.faker import (
    check_faker,
    faker_available,
    is_faker_available,
    raise_faker_missing_error,
)
from docculus.utils.imports.persista import (
    check_persista,
    is_persista_available,
    persista_available,
    raise_persista_missing_error,
)
