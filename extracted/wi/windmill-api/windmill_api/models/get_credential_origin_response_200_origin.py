from enum import Enum


class GetCredentialOriginResponse200Origin(str, Enum):
    BORROWED = "borrowed"
    HELD = "held"

    def __str__(self) -> str:
        return str(self.value)
