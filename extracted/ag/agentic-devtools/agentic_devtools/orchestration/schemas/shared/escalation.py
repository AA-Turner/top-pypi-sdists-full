"""EscalationReason model for structured LLM output schemas.

Represents why an autonomous agent cannot proceed and needs human intervention.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

from .._enums import EscalationCategory, normalize_escalation_category


class EscalationReason(BaseModel):
    """Structured reason for why autonomous processing cannot proceed.

    Used when a node determines that human intervention is required
    due to ambiguity, security concerns, or policy constraints.
    """

    category: Annotated[
        EscalationCategory,
        BeforeValidator(normalize_escalation_category),
    ] = Field(description="Category of the escalation reason")
    description: str = Field(description="Human-readable explanation of why escalation is needed")
    context: str = Field(
        default="",
        description="Additional context relevant to the escalation (e.g., file path, requirement ID)",
    )
    suggested_action: str = Field(
        default="",
        description="Recommended action for the human reviewer to take",
    )
