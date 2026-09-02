"""Troubleshooting block data models — matches TroubleshootingBlock.tsx."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

_camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class TroubleshootingLink(BaseModel):
    model_config = _camel_config

    title: str
    url: str


class TroubleshootingStep(BaseModel):
    model_config = _camel_config

    id: str
    title: str
    description: str
    commands: list[str] = Field(default_factory=list)
    difficulty: Literal["easy", "medium", "hard"] | None = None
    estimated_time: str | None = None
    links: list[TroubleshootingLink] = Field(default_factory=list)


class TroubleshootingSolution(BaseModel):
    model_config = _camel_config

    id: str
    title: str
    description: str | None = None
    priority: Literal["low", "medium", "high"] | None = None
    success_rate: int | None = None   # 0–100 integer, e.g. 85
    tags: list[str] = Field(default_factory=list)
    steps: list[TroubleshootingStep] = Field(default_factory=list)


class TroubleshootingIssue(BaseModel):
    model_config = _camel_config

    id: str
    symptom: str
    description: str | None = None
    severity: Literal["low", "medium", "high", "critical"] | None = None
    causes: list[str] = Field(default_factory=list)
    related_issues: list[str] = Field(default_factory=list)
    solutions: list[TroubleshootingSolution] = Field(default_factory=list)


class TroubleshootingBlockData(BaseModel):
    model_config = _camel_config

    title: str
    description: str | None = None
    issues: list[TroubleshootingIssue] = Field(default_factory=list)
