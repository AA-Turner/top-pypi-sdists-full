"""ImplementationSummary model for structured LLM output schemas.

Summarizes what was done, what changed, and what tests were added.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ImplementationSummary(BaseModel):
    """Summary of completed implementation work.

    Provides a structured overview of changes made, files affected,
    and tests added during an implementation session.
    """

    summary: str = Field(description="Brief human-readable summary of what was implemented")
    files_changed: list[str] = Field(
        default_factory=list,
        description="List of file paths that were modified",
    )
    files_created: list[str] = Field(
        default_factory=list,
        description="List of file paths that were newly created",
    )
    tests_added: list[str] = Field(
        default_factory=list,
        description="List of test names or test file paths that were added",
    )
    notes: str = Field(
        default="",
        description="Additional notes about the implementation (edge cases, known limitations)",
    )
