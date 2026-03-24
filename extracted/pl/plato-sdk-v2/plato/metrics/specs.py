"""Metric specification types — discriminated union for pluggable evaluation."""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field


class VerifierPassRate(BaseModel):
    """Pass rate from verifier findings: count(signal==pass) / total."""

    type: Literal["verifier_pass_rate"] = "verifier_pass_rate"


class VerifierScore(BaseModel):
    """Average numeric score from verifier ScoreData findings."""

    type: Literal["verifier_score"] = "verifier_score"


class HumanAgreement(BaseModel):
    """Agreement rate between verifier signals and human approve/reject annotations."""

    type: Literal["human_agreement"] = "human_agreement"


class LLMComparison(BaseModel):
    """Ask an LLM to compare session results against criteria or a reference session."""

    type: Literal["llm_comparison"] = "llm_comparison"
    comparison_prompt: str = Field(
        description="Prompt template for the comparison. Use {session_result} and {reference_result} placeholders."
    )
    llm_model: str = Field(
        default="gemini/gemini-3-flash-preview",
        description="LiteLLM model string for the comparison LLM",
    )
    llm_api_key: str | None = Field(
        default=None,
        description="API key for the comparison LLM (if not set, uses env default)",
    )
    reference_session_id: str | None = Field(
        default=None,
        description="Session ID to compare against. If not set, evaluates the session in isolation.",
    )


class SessionResultField(BaseModel):
    """Extract a numeric field from ChronosSession.result JSON by dot path."""

    type: Literal["session_result_field"] = "session_result_field"
    field_path: str = Field(description="Dot-separated path into session.result, e.g. 'cua_verification.pass_rate'")


MetricSpec = Annotated[
    VerifierPassRate | VerifierScore | HumanAgreement | LLMComparison | SessionResultField,
    Field(discriminator="type"),
]


class MetricResult(BaseModel):
    """Result of computing a metric for a session."""

    value: float = Field(description="The metric value (0.0-1.0 for rates, arbitrary for scores)")
    details: dict[str, Any] = Field(
        default_factory=dict,
        description="Breakdown: per-task scores, raw counts, intermediate values, etc.",
    )
