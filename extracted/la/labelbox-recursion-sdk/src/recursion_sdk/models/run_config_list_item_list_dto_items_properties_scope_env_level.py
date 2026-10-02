from enum import StrEnum

class RunConfigListItemListDtoItemsPropertiesScopeEnvLevel(StrEnum):
    ENV = "env"

    def __str__(self) -> str:
        return str(self.value)
