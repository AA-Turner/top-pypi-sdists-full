r"""Contain fallback implementations used when ``joblib`` dependency is
not available."""

from __future__ import annotations

__all__ = ["joblib"]

from types import ModuleType
from typing import Any, NoReturn

from iden.utils.imports import raise_error_joblib_missing


def fake_function(*args: Any, **kwargs: Any) -> NoReturn:  # noqa: ARG001
    r"""Fake function that raises an error because joblib is not
    installed.

    Args:
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Raises:
        RuntimeError: joblib is required for this functionality.
    """
    raise_error_joblib_missing()


# Create a fake joblib package
joblib: ModuleType = ModuleType("joblib")
joblib.dump = fake_function
joblib.load = fake_function
