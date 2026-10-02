from enum import StrEnum

class ManagedAgentsSessionHourEstimateUnit(StrEnum):
    SESSION_HOUR = "session_hour"

    def __str__(self) -> str:
        return str(self.value)
