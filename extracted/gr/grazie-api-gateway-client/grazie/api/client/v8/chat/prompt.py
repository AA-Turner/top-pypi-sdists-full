from typing import Dict, List

import attr

from grazie.api.client._common import DeprecatedError
from grazie.api.client.v8.chat.message import (
    AssistantChatMessage,
    AssistantChatMessageTool,
    ChatMessage,
    ChatToolMessage,
    TextChatMessage,
)
from grazie.api.client.v8.chat.roles import ChatRole

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
        raise DeprecatedError(FUNC_DEPRECATION_MSG)

    def add_function(self, name: str, content: str):
        raise DeprecatedError(FUNC_DEPRECATION_MSG)

    def add_tool(self, id: str, tool_name: str, content: str, result: str):
        """
        Used to specify the result of the tool execution.

        :param id: The unique tool identifier. Can be an arbitrary string.
        :param tool_name: Name of the tool to which the message is related.
        :param content: The content of the response to the tool call.
        :param result: The result of running the tool with the provided parameters.
        """
        self.messages.append(AssistantChatMessageTool(id, tool_name, content))
        self.messages.append(ChatToolMessage(id, tool_name, result))
        return self

    def get_messages(self) -> List[Dict[str, str]]:
        return [message.to_json() for message in self.messages]
