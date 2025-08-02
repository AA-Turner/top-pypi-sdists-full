"""Code generation and manipulation utilities."""

from .inspector import WithBlockInspector, inspect_with_block_from_frame
from .mutator import (
    record_step_execution,
)

__all__ = [
    # Block inspection utilities
    "WithBlockInspector",
    "inspect_with_block_from_frame",
    # Simplified recording API
    "record_step_execution",
]
