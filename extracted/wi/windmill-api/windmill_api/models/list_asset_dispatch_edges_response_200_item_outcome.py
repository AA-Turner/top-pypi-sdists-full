from enum import Enum


class ListAssetDispatchEdgesResponse200ItemOutcome(str, Enum):
    DISPATCHED = "dispatched"
    JOIN_PENDING = "join_pending"

    def __str__(self) -> str:
        return str(self.value)
