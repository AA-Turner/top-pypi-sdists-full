from enum import StrEnum

class ManagedAgentsAutomationScheduleTriggerRequestOverlapPolicy(StrEnum):
    ALLOW_ALL = "allow_all"
    BUFFER_ALL = "buffer_all"
    BUFFER_ONE = "buffer_one"
    CANCEL_OTHER = "cancel_other"
    SKIP = "skip"

    def __str__(self) -> str:
        return str(self.value)
