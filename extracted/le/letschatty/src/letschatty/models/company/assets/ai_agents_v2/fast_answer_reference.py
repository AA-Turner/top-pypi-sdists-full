from typing import Literal, Optional

from pydantic import Field, model_validator

from letschatty.models.base_models.ai_agent_component import (
    AiAgentComponent,
    AiAgentComponentType,
)
from letschatty.models.utils.types.identifier import StrObjectId


class FastAnswerReference(AiAgentComponent):
    """Points at a ChattyFastAnswer and makes it AI-selectable.

    Carries the AI-specific metadata that does not belong on the human-facing
    ChattyFastAnswer: when to use it ("description"), per-agent scoping
    (inherited "ai_agent_id"), filter criteria (inherited), and whether the AI
    is allowed to wrap the fast answer with connector messages.

    ``cintia_type`` scopes which PGP surface may select this FA at runtime:
    responder PGPs filter wrappers to ``"responder"``; smart-follow-up PGPs
    filter to ``"smart_follow_up"``. Businesses that want an FA available in
    both surfaces create two wrappers (one per cintia_type). Pre-migration docs
    that lack this field are backfilled to ``"responder"`` at read time by the
    ``_default_cintia_type_to_responder`` validator.

    ``follow_up_strategy_id`` (smart_follow_up only) further narrows the
    wrapper to a single ``FollowUpStrategy``; ``None`` means "eligible for
    whichever strategy the picker selects at runtime". Setting this field on a
    ``"responder"`` wrapper is a domain invariant violation and will raise a
    ``ValueError`` at model construction time.

    ``follow_up_attempt_number`` (smart_follow_up only) scopes the wrapper to
    a specific attempt in the follow-up sequence — e.g. only fire on the 1st
    follow-up of a silence period vs. only on the 3rd. Matched against
    ``SmartFollowUpState.consecutive_count`` (resets on user reply), so
    "1°" means "first follow-up after silence begins", not "first ever sent
    to this chat". ``None`` = eligible on any attempt.

    Connector fields (``allow_pre_connector`` / ``allow_post_connector``) are
    force-stored as ``False`` on smart_follow_up wrappers; pre/post connectors
    don't apply to proactive follow-ups (no trigger message to wrap).
    ``description`` is force-stored as ``""`` on smart_follow_up wrappers;
    the "when to use" is answered by the scoping fields
    (strategy + attempt_number) plus the FA body itself.
    """

    type: Literal[AiAgentComponentType.FAST_ANSWER] = AiAgentComponentType.FAST_ANSWER
    fast_answer_id: StrObjectId = Field(description="Reference to ChattyFastAnswer._id")
    description: str = Field(
        default="",
        description="When the AI should select this fast answer (responder only; forced empty on smart_follow_up).",
    )
    allow_pre_connector: bool = Field(default=True)
    allow_post_connector: bool = Field(default=True)
    cintia_type: Literal["responder", "smart_follow_up"] = Field(
        description="Which PGP surface is allowed to select this FA at runtime."
    )
    follow_up_strategy_id: Optional[StrObjectId] = Field(
        default=None,
        description=(
            "Only meaningful when cintia_type='smart_follow_up'. When set, the FA "
            "is only eligible while this specific FollowUpStrategy is the active "
            "one for the chat. None = eligible under any strategy."
        ),
    )
    follow_up_attempt_number: Optional[int] = Field(
        default=None,
        description=(
            "Only meaningful when cintia_type='smart_follow_up'. When set, the "
            "FA is only eligible on the Nth follow-up of a silence period "
            "(matched against SmartFollowUpState.consecutive_count). None = "
            "eligible on any attempt. Must be >= 1 when set."
        ),
    )

    @model_validator(mode="before")
    @classmethod
    def _default_cintia_type_to_responder(cls, data):
        """Backfill ``cintia_type`` for pre-migration documents.

        Until the introduction of this field every ``FastAnswerReference``
        was consumed exclusively by the responder PGP. Stored docs that
        pre-date this field are therefore semantically ``"responder"``.
        Defaulting here guarantees reads never crash during rollout and
        before the one-shot migration has finished.
        """
        if isinstance(data, dict) and "cintia_type" not in data:
            data["cintia_type"] = "responder"
        return data

    @model_validator(mode="after")
    def _reject_strategy_on_responder(self):
        if self.cintia_type == "responder" and self.follow_up_strategy_id is not None:
            raise ValueError(
                "follow_up_strategy_id is only valid when cintia_type='smart_follow_up'"
            )
        return self

    @model_validator(mode="after")
    def _reject_attempt_number_on_responder(self):
        if self.cintia_type == "responder" and self.follow_up_attempt_number is not None:
            raise ValueError(
                "follow_up_attempt_number is only valid when cintia_type='smart_follow_up'"
            )
        if self.follow_up_attempt_number is not None and self.follow_up_attempt_number < 1:
            raise ValueError("follow_up_attempt_number must be >= 1 when set")
        return self

    @model_validator(mode="after")
    def _force_smart_follow_up_defaults(self):
        """Smart-follow-up wrappers never use connectors and carry no
        description. Force these server-side so a buggy client can't persist
        contradictory values.
        """
        if self.cintia_type == "smart_follow_up":
            object.__setattr__(self, "allow_pre_connector", False)
            object.__setattr__(self, "allow_post_connector", False)
            object.__setattr__(self, "description", "")
        return self
