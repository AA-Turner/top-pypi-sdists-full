from enum import StrEnum

class CustomerSecretListDtoItemsPropertiesScopeProblemVersionLevel(StrEnum):
    PROBLEM_VERSION = "problem-version"

    def __str__(self) -> str:
        return str(self.value)
