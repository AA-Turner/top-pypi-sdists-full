from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, model_validator

from letschatty.models.messages.chatty_messages.base.message_draft import MessageDraft
from .cintia_decision_output import AiOutput, DecisionOutput, DecisionOutputType


class SmartFollowUpOutputAction(StrEnum):
    """Actions that the smart follow-up PGP can take.

    N8N sends these as lowercase strings — values match exactly what N8N sends.
    """
    SEND = "send"
    SKIP = "skip"
    SUGGEST = "suggest"
    ESCALATE = "escalate"


class SmartFollowUpAiOutput(AiOutput):
    """AiOutput with smart follow-up specific action set."""
    action: SmartFollowUpOutputAction  # type: ignore[assignment]


class CintiaSmartFollowOutputData(BaseModel):
    next_call_time: Optional[datetime] = Field(
        default=None,
        description="When to schedule the next follow-up call (set by N8N or defaulted by the handler)",
    )
    messages: Optional[List[MessageDraft]] = Field(
        default=[],
        description="Messages to send or suggest",
    )

    # ── Fast-answer fields ──
    # Populated ONLY by pgp-implementator-smart-follow-up-with-fast-answers when
    # the AI picks a business-approved canned response from the SlugCatalog.
    # Every field defaults to None so pgp-implementator-smart-follow-up-default
    # (which never emits these) stays fully compatible.
    fast_answer_slug: Optional[str] = Field(
        default=None,
        description=(
            "Slug the AI picked from the wrapper catalog; resolved to "
            "``fast_answer_id`` in the callback via the execution's "
            "``metadata.asset_slug_catalog`` snapshot."
        ),
    )
    fast_answer_id: Optional[str] = Field(
        default=None,
        description=(
            "Resolved FA id after slug → id lookup in the callback. Reader "
            "consumers should key FA-rendering off this field."
        ),
    )
    pre_fast_answer_message: Optional[str] = Field(
        default=None,
        description=(
            "Optional AI-written connector sent BEFORE the FA body. Dropped "
            "silently if the wrapper has ``allow_pre_connector=False``."
        ),
    )
    post_fast_answer_message: Optional[str] = Field(
        default=None,
        description=(
            "Optional AI-written connector sent AFTER the FA body. Dropped "
            "silently if the wrapper has ``allow_post_connector=False``."
        ),
    )


class CintiaSmartFollowOutput(DecisionOutput):
    type: Literal[DecisionOutputType.SMART_FOLLOW_UP] = DecisionOutputType.SMART_FOLLOW_UP
    output: SmartFollowUpAiOutput  # type: ignore[assignment]
    data: CintiaSmartFollowOutputData

    @model_validator(mode="after")
    def set_cintia_id_on_messages(self):
        if self.data.messages:
            for message in self.data.messages:
                message.context_value.cintia_id = self.cintia_id
        return self
