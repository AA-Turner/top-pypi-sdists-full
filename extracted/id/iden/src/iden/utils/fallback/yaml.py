r"""Contain fallback implementations used when ``yaml`` dependency is
not available."""

from __future__ import annotations

__all__ = ["yaml"]

from types import ModuleType
from typing import Any, NoReturn

from iden.utils.imports import raise_error_yaml_missing


def fake_function(*args: Any, **kwargs: Any) -> NoReturn:  # noqa: ARG001
    r"""Fake function that raises an error because yaml is not installed.

    Args:
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Raises:
        RuntimeError: yaml is required for this functionality.
    """
    raise_error_yaml_missing()


# Create a fake yaml package
yaml: ModuleType = ModuleType("yaml")
yaml.dump = fake_function
yaml.safe_load = fake_function
