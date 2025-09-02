from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

from ....meta_message_model.schema.values.value_messages import MetaContext

class ChattyContext(BaseModel):
    message_id: Optional[str] = Field(default="")
    template_name: Optional[str] = Field(default=None)
    campaign_id: Optional[str] = Field(default=None)
    response_id: Optional[str] = Field(default=None)
    chain_of_thought_id: Optional[str] = Field(default=None)
    forwarded: Optional[bool] = Field(default=False)
    continuous_conversation_id: Optional[str] = Field(default=None)
    scheduled_messages_id: Optional[str] = Field(default=None)

    def model_dump(self, *args, **kwargs):
        kwargs['exclude_unset'] = True
        return super().model_dump(*args, **kwargs)

    @classmethod
    def from_meta(cls, meta_context: MetaContext | None) -> ChattyContext:
        if meta_context is None:
            return cls.default()
        return cls(message_id=meta_context.id, forwarded=meta_context.forwarded)

    @classmethod
    def default(cls) -> ChattyContext:
        return cls()