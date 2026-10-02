r"""Contain utilities for runnables."""

from __future__ import annotations

__all__ = ["InputOutputPair"]

from dataclasses import dataclass
from typing import Generic, TypeVar

Input = TypeVar("Input")
Output = TypeVar("Output")


@dataclass(frozen=True)
class InputOutputPair(Generic[Input, Output]):
    r"""A frozen pair holding a runnable's input alongside the output it
    produced.

    Args:
        input: The input value passed to the wrapped runnable.
        output: The output value produced by the wrapped runnable for
            ``input``.
    """

    input: Input
    output: Output
