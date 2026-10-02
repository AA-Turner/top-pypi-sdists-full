from enum import StrEnum

class CustomerSecretListDtoItemsPropertiesScopeEnvLevel(StrEnum):
    ENV = "env"

    def __str__(self) -> str:
        return str(self.value)
