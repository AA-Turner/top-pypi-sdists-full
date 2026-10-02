from enum import StrEnum

class CreateTuningRunDtoPropertiesCadenceEveryNStepsType(StrEnum):
    EVERY_N_STEPS = "every_n_steps"

    def __str__(self) -> str:
        return str(self.value)
