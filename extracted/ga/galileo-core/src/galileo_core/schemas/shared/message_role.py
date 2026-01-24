from enum import Enum


class MessageRole(str, Enum):
    agent = "agent"
    assistant = "assistant"
    function = "function"
    system = "system"
    tool = "tool"
    user = "user"
