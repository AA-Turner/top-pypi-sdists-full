from enum import Enum


class ChatRole(str, Enum):
    SYSTEM = "System"
    ASSISTANT = "Assistant"
    FUNCTION = "Function"
    USER = "User"
