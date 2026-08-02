"""Shared types for the execution record domain."""

from typing import Literal

__all__ = [
    "GenerationStatus",
]

# Whether a history entry is still being built or is finalized.
# "generating" means in-progress (e.g., LLM streaming text, subtask running);
# "complete" means finalized.
GenerationStatus = Literal["generating", "complete"]
