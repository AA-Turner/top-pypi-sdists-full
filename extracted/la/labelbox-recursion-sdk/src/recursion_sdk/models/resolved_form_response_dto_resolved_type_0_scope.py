from enum import StrEnum

class ResolvedFormResponseDtoResolvedType0Scope(StrEnum):
    ENVIRONMENT = "environment"
    PROBLEM = "problem"

    def __str__(self) -> str:
        return str(self.value)
