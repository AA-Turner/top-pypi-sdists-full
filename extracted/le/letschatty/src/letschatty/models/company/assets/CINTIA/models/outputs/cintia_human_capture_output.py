from typing import List, Literal, Optional

from pydantic import BaseModel, Field, model_validator

from letschatty.models.messages.chatty_messages.base.message_draft import MessageDraft
from .cintia_decision_output import DecisionOutput, DecisionOutputType


class CintiaHumanCaptureOutputData(BaseModel):
    messages: Optional[List[MessageDraft]] = Field(
        default=[],
        description="The human-authored messages captured as the reference output",
    )


class CintiaHumanCaptureOutput(DecisionOutput):
    """A manually-sent human reply captured as a training reference.

    Mirrors the responder output shape (messages-only). Produced not by an AI
    call but by the human-capture pipeline, which records what a human agent
    actually replied so it can be reviewed and promoted into the reference pool.
    """

    type: Literal[DecisionOutputType.HUMAN_CAPTURE] = DecisionOutputType.HUMAN_CAPTURE
    data: CintiaHumanCaptureOutputData

    @model_validator(mode="after")
    def set_cintia_id_on_messages(self):
        if self.data.messages:
            for message in self.data.messages:
                message.context_value.cintia_id = self.cintia_id
        return self
