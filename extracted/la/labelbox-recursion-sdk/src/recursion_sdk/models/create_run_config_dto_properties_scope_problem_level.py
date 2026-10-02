from enum import StrEnum

class CreateRunConfigDtoPropertiesScopeProblemLevel(StrEnum):
    PROBLEM = "problem"

    def __str__(self) -> str:
        return str(self.value)
