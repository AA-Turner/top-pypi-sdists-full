from enum import StrEnum

class RunConfigWithVersionListDtoItemsPropertiesScopeEnvLevel(StrEnum):
    ENV = "env"

    def __str__(self) -> str:
        return str(self.value)
