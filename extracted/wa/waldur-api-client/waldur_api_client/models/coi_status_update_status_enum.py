from enum import Enum


class COIStatusUpdateStatusEnum(str, Enum):
    DISMISSED = "dismissed"
    RECUSED = "recused"
    WAIVED = "waived"

    def __str__(self) -> str:
        return str(self.value)
