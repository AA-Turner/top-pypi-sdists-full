from enum import Enum


class PosixIdSourceEnum(str, Enum):
    POOL = "pool"
    USER_ATTRIBUTE = "user_attribute"

    def __str__(self) -> str:
        return str(self.value)
