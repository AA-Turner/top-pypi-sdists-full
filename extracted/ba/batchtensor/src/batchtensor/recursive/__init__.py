r"""Contain features to easily work on nested objects."""

from __future__ import annotations

__all__ = [
    "ApplyState",
    "AutoApplier",
    "BaseApplier",
    "DefaultApplier",
    "MappingApplier",
    "SequenceApplier",
    "recursive_apply",
]

from batchtensor.recursive.auto import AutoApplier
from batchtensor.recursive.base import BaseApplier
from batchtensor.recursive.default import DefaultApplier
from batchtensor.recursive.interface import recursive_apply
from batchtensor.recursive.mapping import MappingApplier
from batchtensor.recursive.sequence import SequenceApplier
from batchtensor.recursive.state import ApplyState
