from enum import Enum


class DecidingEntityEnum(str, Enum):
    AUTOMATIC = "automatic"
    BY_CALL_MANAGER = "by_call_manager"

    def __str__(self) -> str:
        return str(self.value)
