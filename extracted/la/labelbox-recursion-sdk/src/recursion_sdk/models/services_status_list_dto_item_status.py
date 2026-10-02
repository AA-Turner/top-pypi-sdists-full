from enum import StrEnum

class ServicesStatusListDtoItemStatus(StrEnum):
    DEGRADED = "degraded"
    DOWN = "down"
    OPERATIONAL = "operational"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
