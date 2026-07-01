"""Search space distribution types for optimization studies."""

import typing as t
from dataclasses import dataclass

from dreadnode.core.types.common import Primitive


@dataclass
class Distribution:
    """Base class for all search space distributions."""


@dataclass
class Float(Distribution):
    """Floating-point distribution for continuous parameters.

    Args:
        low: Lower bound (inclusive).
        high: Upper bound (inclusive).
        log: If True, sample in log space.
        step: Discretization step size.
    """

    low: float
    high: float
    log: bool = False
    step: float | None = None


@dataclass
class Int(Distribution):
    """Integer distribution for discrete parameters.

    Args:
        low: Lower bound (inclusive).
        high: Upper bound (inclusive).
        log: If True, sample in log space.
        step: Step size between values.
    """

    low: int
    high: int
    log: bool = False
    step: int = 1


@dataclass
class Categorical(Distribution):
    """Categorical distribution for discrete choices.

    Args:
        choices: List of possible values.
    """

    choices: list[Primitive]


SearchSpace = t.Mapping[str, Distribution | list[Primitive]]
"""Type alias for search space definitions."""
