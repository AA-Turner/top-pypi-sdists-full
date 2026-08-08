from enum import Enum


class VariableUpsertType(str, Enum):
    PLAIN = "plain"
    SECRET = "secret"

    def __str__(self) -> str:
        return str(self.value)
