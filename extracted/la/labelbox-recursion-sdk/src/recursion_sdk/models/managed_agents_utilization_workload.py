from enum import StrEnum

class ManagedAgentsUtilizationWorkload(StrEnum):
    AUTONOMOUS = "autonomous"
    INTERACTIVE = "interactive"

    def __str__(self) -> str:
        return str(self.value)
