from enum import StrEnum

class CustomerSecretListDtoItemsPropertiesScopeProblemLevel(StrEnum):
    PROBLEM = "problem"

    def __str__(self) -> str:
        return str(self.value)
