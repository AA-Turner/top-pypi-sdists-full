from enum import StrEnum

class RunConfigDtoPropertiesScopeEnvLevel(StrEnum):
    ENV = "env"

    def __str__(self) -> str:
        return str(self.value)
