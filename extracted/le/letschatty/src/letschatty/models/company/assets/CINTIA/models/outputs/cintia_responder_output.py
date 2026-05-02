from typing import List, Literal, Optional

from pydantic import BaseModel, Field, model_validator

from letschatty.models.messages.chatty_messages.base.message_draft import MessageDraft
from .cintia_decision_output import DecisionOutput, DecisionOutputType


class CintiaResponderOutputData(BaseModel):
    messages: Optional[List[MessageDraft]] = Field(
        default=[], description="The messages to send to the chat"
    )
    fast_answer_id: Optional[str] = Field(
        default=None, description="Resolved FastAnswer._id when AI selected a fast answer"
    )
    fast_answer_slug: Optional[str] = Field(
        default=None, description="Slug the AI produced; resolved server-side"
    )
    pre_fast_answer_message: Optional[str] = Field(
        default=None, description="Optional connector before the FA body"
    )
    post_fast_answer_message: Optional[str] = Field(
        default=None, description="Optional connector after the FA body"
    )


class CintiaResponderOutput(DecisionOutput):
    type: Literal[DecisionOutputType.RESPONDER] = DecisionOutputType.RESPONDER
    data: CintiaResponderOutputData

    @property
    def messages_to_send(self) -> List[MessageDraft]:
        if not self.data.messages:
            raise ValueError("Messages are required when action is send or suggest")
        return self.data.messages

    @model_validator(mode="after")
    def set_cintia_id_on_messages(self):
        if self.data.messages:
            for message in self.data.messages:
                message.context_value.cintia_id = self.cintia_id
        return self
