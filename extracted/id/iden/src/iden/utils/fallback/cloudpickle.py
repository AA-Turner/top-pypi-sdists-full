r"""Contain fallback implementations used when ``cloudpickle``
dependency is not available."""

from __future__ import annotations

__all__ = ["cloudpickle"]

from types import ModuleType
from typing import Any, NoReturn

from iden.utils.imports import raise_error_cloudpickle_missing


def fake_function(*args: Any, **kwargs: Any) -> NoReturn:  # noqa: ARG001
    r"""Fake function that raises an error because cloudpickle is not
    installed.

    Args:
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Raises:
        RuntimeError: cloudpickle is required for this functionality.
    """
    raise_error_cloudpickle_missing()


# Create a fake cloudpickle package
cloudpickle: ModuleType = ModuleType("cloudpickle")
cloudpickle.dump = fake_function
cloudpickle.load = fake_function
