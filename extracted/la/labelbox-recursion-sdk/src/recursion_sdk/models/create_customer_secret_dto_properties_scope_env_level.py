from enum import StrEnum

class CreateCustomerSecretDtoPropertiesScopeEnvLevel(StrEnum):
    ENV = "env"

    def __str__(self) -> str:
        return str(self.value)
