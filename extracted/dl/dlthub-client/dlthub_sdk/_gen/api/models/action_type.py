from enum import Enum


class ActionType(str, Enum):
    EMAIL_SEND = "email.send"

    def __str__(self) -> str:
        return str(self.value)
