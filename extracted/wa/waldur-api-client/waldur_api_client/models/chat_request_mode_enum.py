from enum import Enum


class ChatRequestModeEnum(str, Enum):
    EDIT = "edit"
    RELOAD = "reload"

    def __str__(self) -> str:
        return str(self.value)
