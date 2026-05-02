"""CintiaExecution — tracks state through the CINTIA v3 AI pipeline."""

from __future__ import annotations

from enum import StrEnum
from typing import Any, ClassVar

from pydantic import ConfigDict, Field

from ....base_models.chatty_asset_model import CompanyAssetModel, ChattyAssetPreview
from ....utils.types.identifier import StrObjectId
from .models.cintia_feedback import CintiaFeedback, CintiaCorrection
from .models.cintia_trigger import CintiaTrigger
from .models.outputs.cintia_decision_output import (
    DecisionOutput,
    DecisionOutputType,
    _decision_output_union,
)
from .models.chat_vector import ChatVector
from .events.cintia_event_type import CintiaEvent, CintiaEventType
from pydantic import BaseModel

class CintiaStatus(StrEnum):
    QUEUED = "queued"
    STARTING = "starting"
    PROMPTING = "prompting"
    AI_CALL_PROCESSING = "ai_call_processing"
    FINISHED = "finished"
    ERROR = "error"
    MERGED = "merged"
    AWAITING_FEEDBACK = "awaiting_feedback"

class CintiaCallback(BaseModel):
    event : CintiaEvent = Field(description="The event that triggered the callback")
    url : str = Field(description="The url for the webhook to send the callback to")

class CintiaExecution(CompanyAssetModel):
    """Record created at the start of each CINTIA v3 run."""
    chat_id: StrObjectId
    status: CintiaStatus = CintiaStatus.QUEUED
    pgp_id: StrObjectId | None = Field(default=None, description="The pgp id of the cintia execution")
    trigger: CintiaTrigger = Field(description="The trigger of the cintia execution")
    # NOTE: the type here is the ``DecisionOutput`` base for static analysis,
    # but the real validator is a discriminated union over every concrete
    # subclass, injected below via ``__class_vars__``. Using the union type
    # directly at class-body time triggers a circular import because every
    # subclass imports this module. See ``_rebuild_decision_output_field`` at
    # the bottom of this file.
    decision_output: DecisionOutput | None = None
    components_used: list[StrObjectId] = Field(default_factory=list)
    tokens_real: int | None = None
    on_finish_callback: CintiaCallback | None = None
    feedback: CintiaFeedback | None = Field(default=None, description="The feedback of the cintia execution")
    correction: CintiaCorrection | None = Field(default=None, description="Latest agent-authored correction of the AI response")
    metadata: dict[str, Any] = Field(default_factory=dict, description="The metadata of the cintia execution")
    chat_vector: ChatVector | None = Field(default=None, description="The vector of the chat")
    cintia_type: DecisionOutputType | None = Field(default=None, description="Type of execution: responder, tagger, smart_follow_up. Set at creation.")
    last_message_id: str | None = Field(default=None, description="ID of the last incoming message for debounce tracking")
    queued_message_ids: list[str] = Field(default_factory=list, description="Ordered list of incoming message IDs accumulated during debounce")
    merged_from_cintia_id: StrObjectId | None = Field(default=None, description="ID of previous execution that was merged into this one")
    iterated_from_cintia_id: StrObjectId | None = Field(default=None, description="ID of execution this was iterated from")
    iterated_to_cintia_id: StrObjectId | None = Field(default=None, description="ID of execution this was iterated to")
    pgp_url: str | None = Field(default=None, description="PGP implementator URL that handled this execution")
    ai_agent_id: StrObjectId | None = Field(default=None, description="AI agent ID resolved at dequeue time from the chat's assigned agent")
    preview_class: ClassVar[type[ChattyAssetPreview]] = ChattyAssetPreview

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True
    )


# ── Swap ``decision_output`` for the discriminated union ────────────────────
#
# Rationale: if we declare ``decision_output`` directly as the union on the
# class body, pydantic validates incoming mongo docs against ``DecisionOutput``
# (the abstract base) and **silently strips** the per-subclass ``data`` field
# — because the base doesn't declare ``data``. Concretely this caused
# ``execution.decision_output.data.messages`` to come back empty on copilot
# accept, so feedback handlers built zero drafts and the accept silently
# finalized without sending anything to WhatsApp.
#
# Rebuilding the field here (after the module finishes importing) lets us
# reference the union — which itself needs every concrete subclass imported,
# and those subclasses import ``DecisionOutput`` from the outputs module,
# which is why we can't put the union on the class body without circular
# imports.
def _rebuild_decision_output_field() -> None:
    from typing import Optional

    from pydantic.fields import FieldInfo

    union = _decision_output_union()
    CintiaExecution.model_fields["decision_output"] = FieldInfo(
        annotation=Optional[union],
        default=None,
    )
    CintiaExecution.model_rebuild(force=True)


_rebuild_decision_output_field()
