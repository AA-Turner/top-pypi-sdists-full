from enum import Enum


class ChatSessionFieldEnum(str, Enum):
    CREATED = "created"
    MODIFIED = "modified"
    USER = "user"
    USER_FULL_NAME = "user_full_name"
    USER_USERNAME = "user_username"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
