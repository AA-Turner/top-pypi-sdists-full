from enum import StrEnum

class EnvironmentWithCountsPageDtoItemsItemQaGateOverrideAllowedStagesItem(StrEnum):
    LOCKING = "locking"
    RUNNING = "running"
    SUBMITTING = "submitting"

    def __str__(self) -> str:
        return str(self.value)
