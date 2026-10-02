from enum import StrEnum

class ManagedAgentsModelCostReceiptQuantityResponseUnit(StrEnum):
    MILLISECOND = "millisecond"
    REQUEST = "request"
    TOKEN = "token"

    def __str__(self) -> str:
        return str(self.value)
