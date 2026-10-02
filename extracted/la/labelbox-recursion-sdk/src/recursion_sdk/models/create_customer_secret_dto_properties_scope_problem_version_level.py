from enum import StrEnum

class CreateCustomerSecretDtoPropertiesScopeProblemVersionLevel(StrEnum):
    PROBLEM_VERSION = "problem-version"

    def __str__(self) -> str:
        return str(self.value)
