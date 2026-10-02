from enum import StrEnum

class CreateTuningRunDtoPropertiesCadenceStepsType(StrEnum):
    STEPS = "steps"

    def __str__(self) -> str:
        return str(self.value)
