from enum import StrEnum

class ListReflectionsTriggeredBy(StrEnum):
    COUNTER = "counter"
    MANUAL = "manual"
    SCHEDULE = "schedule"

    def __str__(self) -> str:
        return str(self.value)
