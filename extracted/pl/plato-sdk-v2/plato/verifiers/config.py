"""Verifier configuration base class."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class VerifierConfig(BaseModel):
    """Base configuration for all verifiers.

    Verifier-specific configs should subclass this and add their own fields.
    """

    model_config = ConfigDict(extra="allow")

    session_id: str = Field(description="Target session ID to publish annotations to")
    verifier_session_id: str = Field(default="", description="Session ID of the verifier run (for traceability)")
    chronos_base_url: str = Field(default="", description="Chronos API base URL")
    plato_api_key: str = Field(default="", description="Plato API key for Chronos access")

    review_id: str | None = Field(
        default=None,
        description="Existing review ID to attach annotations to. If None, a new review is created.",
    )
    annotation_tags: list[str] = Field(
        default_factory=list,
        description="Extra tags to add to all created annotations",
    )
