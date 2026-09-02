from typing import Optional

import attr
import attrs

from grazie.api.client.chat.roles import ChatRole


@attrs.define(auto_attribs=True, frozen=True)
class ChatMessage:
    def to_json(self) -> dict:
        raise NotImplementedError


@attrs.define(auto_attribs=True, frozen=True)
class TextChatMessage(ChatMessage):
    """
    A message that is just text.
    """

    role: ChatRole
    text: str

    def to_json(self) -> dict:
        return {"type": self.role.value.lower() + "_message", "content": self.text}


@attrs.define(auto_attribs=True, frozen=True)
class AssistantChatMessage(ChatMessage):
    """
    Assistant LLM chat message.
    Used for model-generated messages including model-generated functionCall response.

    :param text - for common model-generated messages
    :param functionCall - for model-generated functionCall response
    """

    @attrs.define(auto_attribs=True, frozen=True)
    class FunctionCallResponse:
        """
        :param functionName - the name of the function which was called
        :param content - the content of the function call response
        """

        functionName: str
        content: str

    text: Optional[str]
    functionCall: Optional[FunctionCallResponse] = None

    def to_json(self) -> dict:
        return {
            "type": ChatRole.ASSISTANT.value.lower() + "_message",
            "content": self.text,
            "functionCall": (attr.asdict(self.functionCall) if self.functionCall else None),
        }


@attrs.define(auto_attribs=True, frozen=True)
class FunctionCallChatMessage(ChatMessage):
    """
    This message is used to specify a result of a function execution with model-generated parameters.
    """

    name: str
    content: str

    def to_json(self) -> dict:
        return {
            "type": ChatRole.FUNCTION.value.lower() + "_message",
            "content": self.content,
            "functionName": self.name,
        }
