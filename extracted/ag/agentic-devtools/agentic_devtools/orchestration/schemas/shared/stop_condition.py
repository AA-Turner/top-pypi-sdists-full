"""StopCondition model for structured LLM output schemas.

Represents why processing should halt (budget exceeded, blocked, ambiguous).
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class StopCondition(BaseModel):
    """Structured representation of why processing should halt.

    Used when a workflow determines it cannot continue and must stop
    gracefully, providing a clear reason and any relevant context.
    """

    reason: str = Field(description="Human-readable explanation of why processing must stop")
    is_recoverable: bool = Field(
        default=False,
        description="Whether the condition could be resolved by retrying or providing additional input",
    )
    details: str = Field(
        default="",
        description="Additional technical details about the stop condition",
    )
