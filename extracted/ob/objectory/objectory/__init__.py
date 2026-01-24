r"""Contain the main features of the ``objectory`` package."""

from __future__ import annotations

__all__ = ["OBJECT_INIT", "OBJECT_TARGET", "AbstractFactory", "Registry", "__version__", "factory"]

from importlib.metadata import PackageNotFoundError, version

from objectory.abstract_factory import AbstractFactory
from objectory.constants import OBJECT_INIT, OBJECT_TARGET
from objectory.registry import Registry
from objectory.universal import factory

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    # Package is not installed, fallback if needed
    __version__ = "0.0.0"
