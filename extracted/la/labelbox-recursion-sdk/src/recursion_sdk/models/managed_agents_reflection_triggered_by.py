from enum import StrEnum

class ManagedAgentsReflectionTriggeredBy(StrEnum):
    COUNTER = "counter"
    MANUAL = "manual"
    SCHEDULE = "schedule"

    def __str__(self) -> str:
        return str(self.value)
