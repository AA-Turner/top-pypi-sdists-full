"""ChecklistItem model for structured LLM output schemas.

Provides a structured checklist item with acceptance criteria and complexity.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

ComplexityLevel = Literal["low", "medium", "high"]


class ChecklistItem(BaseModel):
    """An actionable checklist item for implementation tracking.

    Represents a single unit of work with clear acceptance criteria
    and estimated complexity for progress tracking.
    """

    description: str = Field(description="Human-readable description of the checklist item")
    acceptance_criteria: str = Field(description="Criteria that must be met for this item to be considered complete")
    estimated_complexity: ComplexityLevel = Field(
        default="medium",
        description="Estimated complexity: 'low', 'medium', or 'high'",
    )
    is_complete: bool = Field(default=False, description="Whether this item has been completed")
