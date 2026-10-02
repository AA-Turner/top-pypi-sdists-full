from enum import StrEnum

class EstimateSessionHourCostWorkload(StrEnum):
    AUTONOMOUS = "autonomous"
    INTERACTIVE = "interactive"

    def __str__(self) -> str:
        return str(self.value)
