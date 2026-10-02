from enum import StrEnum

class ManagedAgentsModelCostComponentResponseUnit(StrEnum):
    MILLISECOND = "millisecond"
    REQUEST = "request"
    TOKEN = "token"

    def __str__(self) -> str:
        return str(self.value)
