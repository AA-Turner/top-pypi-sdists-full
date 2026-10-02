from enum import StrEnum

class CreateCostLimitDtoScope(StrEnum):
    ENVIRONMENT = "environment"
    PROBLEM = "problem"

    def __str__(self) -> str:
        return str(self.value)
