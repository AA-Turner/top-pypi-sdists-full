from enum import StrEnum

class CreateCustomerSecretDtoPropertiesScopeProblemLevel(StrEnum):
    PROBLEM = "problem"

    def __str__(self) -> str:
        return str(self.value)
