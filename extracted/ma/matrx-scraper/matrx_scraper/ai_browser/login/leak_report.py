"""Leak-reporting instructions carried on EVERY login tool result (D-11).

> *"The tool result carries instructions telling the agent how to submit feedback
> if it believes a secret was exposed to it, or that we got something wrong."* The
> system asks its own users to police it.

The instruction is present on success too. The agent's report NEVER includes the
value itself — it names WHERE it saw it. The report is a thin wrapper over the
existing feedback path (host side); this module only owns the always-present
instruction block and the report shape, so no consumer hand-writes the copy.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

# The one instruction string. A single definition so it can never drift between
# success, challenged, rejected, and unknown results.
HOW_TO_REPORT: str = (
    "If you saw a password, token, or code in any page content, screenshot, or tool "
    "result during this login — or if this login was reported as succeeded/failed and "
    "it was actually the opposite — report it now with "
    "credential_login({action:'report', ...}). Do not repeat the value in your report. "
    "Name where you saw it."
)


class FeedbackBlock(BaseModel):
    model_config = ConfigDict(extra="forbid")

    how_to_report: str = HOW_TO_REPORT


def feedback_block() -> FeedbackBlock:
    return FeedbackBlock()


ReportKind = Literal["secret_exposed", "wrong_verdict", "recipe_wrong", "other"]


class LeakReport(BaseModel):
    """The ``Report`` arm of the credential_login discriminated union. The value is
    NEVER included — ``where`` and ``description`` name the location only."""

    model_config = ConfigDict(extra="forbid")

    kind: ReportKind
    where: str
    attempt_id: str | None = None
    description: str | None = None


__all__ = ["FeedbackBlock", "HOW_TO_REPORT", "LeakReport", "ReportKind", "feedback_block"]
