from enum import StrEnum

class BindableRunConfigListDtoItemsPropertiesScopeProblemLevel(StrEnum):
    PROBLEM = "problem"

    def __str__(self) -> str:
        return str(self.value)
