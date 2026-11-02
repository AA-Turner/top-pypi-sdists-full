"""QualityGateResult model for structured LLM output schemas.

Provides pass/fail results per quality gate with supporting details.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

from .._enums import QualityGateName, normalize_quality_gate_name


class QualityGateResult(BaseModel):
    """Result of a single quality gate check.

    Represents whether a specific quality gate (lint, tests, coverage, etc.)
    passed or failed, with details about the outcome.
    """

    gate: Annotated[QualityGateName, BeforeValidator(normalize_quality_gate_name)] = Field(
        description="Name of the quality gate that was checked"
    )
    passed: bool = Field(description="Whether the quality gate passed")
    details: str = Field(default="", description="Details about the gate result (e.g., error messages)")
    metric_value: str = Field(
        default="",
        description="Measured value if applicable (e.g., '98.5%' for coverage)",
    )
