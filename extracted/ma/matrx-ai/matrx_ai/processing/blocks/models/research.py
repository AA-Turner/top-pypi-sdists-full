"""Research block data models — matches ResearchData interface in ResearchBlock.tsx."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

_camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ResearchFinding(BaseModel):
    model_config = _camel_config

    id: str
    title: str
    primary_source: str = ""
    additional_sources: list[str] = Field(default_factory=list)
    urls: list[str] = Field(default_factory=list)
    key_details: str = ""
    significance: str = ""
    future_implications: str = ""
    confidence_level: Literal["HIGH", "MEDIUM", "LOW"] = "MEDIUM"


class ResearchSection(BaseModel):
    model_config = _camel_config

    id: str
    title: str
    subtitle: str | None = None
    findings: list[ResearchFinding] = Field(default_factory=list)


class ConvergentTheme(BaseModel):
    model_config = _camel_config

    theme: str
    description: str


class ResearchChallenge(BaseModel):
    model_config = _camel_config

    id: str
    title: str
    description: str
    current_solutions: str | None = None
    research_gaps: str | None = None
    category: Literal["technical", "ethical", "regulatory", "other"] = "other"


class ResearchRecommendation(BaseModel):
    model_config = _camel_config

    id: str
    recommendation: str
    target: Literal["researchers", "industry", "policymakers", "general"] = "general"


class ResearchMetadata(BaseModel):
    model_config = _camel_config

    research_date: str | None = None
    last_updated: str | None = None
    confidence_rating: str | None = None
    bias_assessment: str | None = None


class ResearchBlockData(BaseModel):
    model_config = _camel_config

    title: str
    overview: str = ""
    introduction: str = ""
    conclusion: str = ""
    executive_summary: str | None = None
    research_scope: str | None = None
    key_focus_areas: str | None = None
    analysis_period: str | None = None
    research_questions: list[str] = Field(default_factory=list)
    sections: list[ResearchSection] = Field(default_factory=list)
    convergent_themes: list[ConvergentTheme] = Field(default_factory=list)
    short_term_outlook: list[str] = Field(default_factory=list)
    medium_term_outlook: list[str] = Field(default_factory=list)
    long_term_vision: list[str] = Field(default_factory=list)
    challenges: list[ResearchChallenge] = Field(default_factory=list)
    recommendations: list[ResearchRecommendation] = Field(default_factory=list)
    key_takeaways: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    metadata: ResearchMetadata = Field(default_factory=ResearchMetadata)
