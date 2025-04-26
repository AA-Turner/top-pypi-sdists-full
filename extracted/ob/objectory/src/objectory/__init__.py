r"""Contain the main features of the ``objectory`` package."""

from __future__ import annotations

__all__ = ["AbstractFactory", "OBJECT_INIT", "OBJECT_TARGET", "Registry", "factory"]

from objectory.abstract_factory import AbstractFactory
from objectory.constants import OBJECT_INIT, OBJECT_TARGET
from objectory.registry import Registry
from objectory.universal import factory
