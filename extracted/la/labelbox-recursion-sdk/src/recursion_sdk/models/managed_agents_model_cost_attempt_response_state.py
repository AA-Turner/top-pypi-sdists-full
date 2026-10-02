from enum import StrEnum

class ManagedAgentsModelCostAttemptResponseState(StrEnum):
    CHARGED = "charged"
    DISPATCHED = "dispatched"
    INDETERMINATE = "indeterminate"
    NOT_CHARGED = "not_charged"
    PREPARED = "prepared"

    def __str__(self) -> str:
        return str(self.value)
