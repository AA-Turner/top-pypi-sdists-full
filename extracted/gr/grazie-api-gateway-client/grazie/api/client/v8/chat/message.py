from typing import Optional

import attrs

from grazie.api.client.v8.chat.roles import ChatRole


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
    Used for model-generated messages.

    :param text - for common model-generated messages
    """

    text: Optional[str]

    def to_json(self) -> dict:
        return {
            "type": ChatRole.ASSISTANT.value.lower() + "_message",
            "content": self.text,
        }


@attrs.define(auto_attribs=True, frozen=True)
class AssistantChatMessageTool(ChatMessage):
    id: str
    tool_name: str
    content: str

    def to_json(self) -> dict:
        return {
            "type": ChatRole.ASSISTANT.value.lower() + "_message_tool",
            "id": self.id,
            "toolName": self.tool_name,
            "content": self.content,
        }


@attrs.define(auto_attribs=True, frozen=True)
class ChatToolMessage(ChatMessage):
    id: str
    tool_name: str
    result: str

    def to_json(self) -> dict:
        return {
            "type": ChatRole.TOOL.value.lower() + "_message",
            "id": self.id,
            "toolName": self.tool_name,
            "result": self.result,
        }
