"""The user message of a Workflow input, as Harness types.

Like ``update_inputs``, kept out of the package ``__init__``, which imports no Harness module.
"""

from typing import Annotated

from pydantic import AfterValidator, JsonValue, TypeAdapter

from mistralai.vibe.harness.app_server.session import (
    ContentBlock,
    ContextMessage,
    UserMessageInput,
)
from mistralai.vibe.harness.app_server.session.models.content import refuse_unsupported_blocks
from mistralai.vibe_agents.session_workflow.inputs import WorkflowUserMessage

# A reader keeps a block it cannot run; a message to run must not hold one.
_RUNNABLE_BLOCKS: TypeAdapter[list[ContentBlock]] = TypeAdapter(
    Annotated[list[ContentBlock], AfterValidator(refuse_unsupported_blocks)]
)


def message_json(user_message: UserMessageInput) -> list[dict[str, JsonValue]]:
    return [block.model_dump(mode="json", exclude_none=True) for block in user_message.message]


def context_messages_json(user_message: UserMessageInput) -> list[dict[str, JsonValue]]:
    return [context.model_dump(mode="json", exclude_none=True) for context in user_message.context_messages]


def read_user_message(user_message: WorkflowUserMessage) -> tuple[list[ContentBlock], list[ContextMessage]]:
    """Return the message's content blocks and context messages.

    Raise ``pydantic.ValidationError`` for a block this Worker cannot read.
    """

    blocks = _RUNNABLE_BLOCKS.validate_python(user_message.message)
    context_messages = [ContextMessage.model_validate(context) for context in user_message.context_messages]
    return blocks, context_messages


__all__ = ["context_messages_json", "message_json", "read_user_message"]
