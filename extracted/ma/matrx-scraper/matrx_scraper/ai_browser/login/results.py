"""The result an agent receives from a login attempt — verdict, confidence, signals,
capture ids, and the always-present leak-report block. **No value ever appears here.**
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .leak_report import FeedbackBlock, feedback_block
from .verifier import Outcome, VerdictSignal

# The status the tool surfaces. ``ok`` carries a verdict; ``spec_incomplete`` is the
# refusal-before-touch refusal (nothing was typed); ``human_required`` maps a
# ``challenged``/``rejected`` verdict onto S6's park shape at the host.
AttemptStatus = Literal["ok", "spec_incomplete"]


class CaptureRef(BaseModel):
    """A handle to a stored before/after state capture (S1 ``browser.capture``). The
    id is a row id, never a URL — a signed URL is a handoff, never an identity."""

    model_config = ConfigDict(extra="forbid")

    capture_id: str | None = None
    privacy_class: Literal["redacted", "sensitive", "operator_only"] = "redacted"


class RecipeRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    recipe_id: str | None = None
    recipe_version: int | None = None
    recipe_overrode_agent_spec: bool = False


class LoginAttemptResult(BaseModel):
    """What the executor returns. Carries names, verdicts, and capture ids only."""

    model_config = ConfigDict(extra="forbid")

    status: AttemptStatus
    outcome: Outcome | None = None
    confidence: float | None = None
    low_confidence: bool = False  # a low-confidence success proceeds, but flagged (D-16 #4)
    signals: list[VerdictSignal] = Field(default_factory=list)
    challenge_class: str | None = None
    contradiction: bool = False
    field_keys: list[str] = Field(default_factory=list)  # NAMES only
    recipe: RecipeRef = Field(default_factory=RecipeRef)
    before_capture: CaptureRef | None = None
    after_capture: CaptureRef | None = None
    url: str | None = None
    title: str | None = None
    # Refusal-before-touch detail (spec_incomplete only).
    missing_fields: list[str] = Field(default_factory=list)
    refusal_detail: str | None = None
    feedback: FeedbackBlock = Field(default_factory=feedback_block)


__all__ = ["AttemptStatus", "CaptureRef", "LoginAttemptResult", "RecipeRef"]
