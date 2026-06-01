from enum import Enum


class ChatRole(str, Enum):
    SYSTEM = "System"
    ASSISTANT = "Assistant"
    USER = "User"
    TOOL = "Tool"
