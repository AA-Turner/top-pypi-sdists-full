from enum import StrEnum

class CreateRunConfigDtoPropertiesScopeEnvLevel(StrEnum):
    ENV = "env"

    def __str__(self) -> str:
        return str(self.value)
