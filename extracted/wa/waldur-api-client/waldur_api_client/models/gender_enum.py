from enum import Enum


class GenderEnum(str, Enum):
    FEMALE = "female"
    MALE = "male"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
