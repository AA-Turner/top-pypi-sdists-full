"""Typed prior context annotations stored on message history entries."""

from typing import Final, Literal

from pydantic import BaseModel, ConfigDict, Field

from mistralai.vibe_agents.session_workflow.annotations import annotations_for
from mistralai.vibe_agents.session_workflow.commands import JsonObject, MessageContext

MESSAGE_CONTEXT_ANNOTATION_KEY: Final[Literal["vibe_agents.message_context"]] = "vibe_agents.message_context"


class MessageContextAnnotations(BaseModel):
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    message_context: MessageContext = Field(alias=MESSAGE_CONTEXT_ANNOTATION_KEY)


def annotations_for_context(context: MessageContext) -> JsonObject:
    return annotations_for(MESSAGE_CONTEXT_ANNOTATION_KEY, context, exclude_none=True)
