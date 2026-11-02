"""ExecutiveDecisionOutput — decision output for the executive PGP.

The executive PGP runs a two-tier AI on coexistence owner echoes: a light
triage model fires on every relevant owner message to decide whether action is
needed, and a strong model drafts the follow-up only when warranted. The
output carries an action (what to do), an intent label (why), an optional
UTC ISO timestamp to (re)schedule, and an optional drafted message for the
customer or owner follow-up.

Spec (cintia-lambdas repo): docs/superpowers/specs/2026-06-13-executive-chatty-v1-design.md
"""
from __future__ import annotations

from enum import StrEnum
from typing import Literal, Optional

from pydantic import ConfigDict, BaseModel

from .cintia_decision_output import DecisionOutput, DecisionOutputType


class ExecutiveAction(StrEnum):
    SCHEDULE_CUSTOMER_FOLLOWUP = "schedule_customer_followup"
    SCHEDULE_OWNER_REMINDER = "schedule_owner_reminder"
    CANCEL = "cancel"
    CHANGE = "change"
    RESCHEDULE = "reschedule"
    KEEP = "keep"
    SKIP = "skip"


class ExecutiveData(BaseModel):
    model_config = ConfigDict(extra="allow")

    action: ExecutiveAction
    intent: str
    when_iso: Optional[str] = None
    draft: Optional[str] = None


class ExecutiveDecisionOutput(DecisionOutput):
    type: Literal[DecisionOutputType.EXECUTIVE] = DecisionOutputType.EXECUTIVE
    data: ExecutiveData
