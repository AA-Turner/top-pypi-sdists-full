from enum import Enum


class IdentityBridgeRequestGenderEnum(str, Enum):
    FEMALE = "female"
    MALE = "male"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
