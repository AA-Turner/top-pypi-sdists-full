from enum import StrEnum

class ResolvedRunConfigDtoPropertiesProvenancePropertiesScopeEnvLevel(StrEnum):
    ENV = "env"

    def __str__(self) -> str:
        return str(self.value)
