"""Data models for Plato worlds."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Observation(BaseModel):
    """Observation returned from reset/step."""

    data: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


class StepResult(BaseModel):
    """Result of a step."""

    observation: Observation
    done: bool = False
    info: dict[str, Any] = Field(default_factory=dict)
