from enum import StrEnum

class CustomerSecretDtoPropertiesScopeEnvLevel(StrEnum):
    ENV = "env"

    def __str__(self) -> str:
        return str(self.value)
