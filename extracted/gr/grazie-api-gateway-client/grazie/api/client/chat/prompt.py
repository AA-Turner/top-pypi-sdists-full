from typing import Dict, List

import attr

from grazie.api.client.chat.message import (
    AssistantChatMessage,
    ChatMessage,
    FunctionCallChatMessage,
    TextChatMessage,
)
from grazie.api.client.chat.roles import ChatRole

FUNC_DEPRECATION_MSG = "Function calls are deprecated. Use add_tool instead."


@attr.s(auto_attribs=True, frozen=False)
class ChatPrompt:
    messages: List[ChatMessage] = attr.ib(default=attr.Factory(list))

    def _add_text(self, item: str, role: ChatRole):
        self.messages.append(TextChatMessage(role, item))
        return self

    def add_user(self, item: str):
        return self._add_text(item, ChatRole.USER)

    def add_system(self, item: str):
        return self._add_text(item, ChatRole.SYSTEM)

    def add_assistant(self, item: str):
        self.messages.append(AssistantChatMessage(text=item))
        return self

    def add_assistant_function(self, name: str, content: str):
        self.messages.append(
            AssistantChatMessage(
                text=None,
                functionCall=AssistantChatMessage.FunctionCallResponse(
                    functionName=name, content=content
                ),
            )
        )
        return self

    def add_function(self, name: str, content: str):
        self.messages.append(FunctionCallChatMessage(name=name, content=content))
        return self

    def get_messages(self) -> List[Dict[str, str]]:
        return [message.to_json() for message in self.messages]
