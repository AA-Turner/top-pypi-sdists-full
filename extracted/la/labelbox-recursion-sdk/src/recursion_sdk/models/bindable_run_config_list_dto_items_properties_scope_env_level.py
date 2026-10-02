from enum import StrEnum

class BindableRunConfigListDtoItemsPropertiesScopeEnvLevel(StrEnum):
    ENV = "env"

    def __str__(self) -> str:
        return str(self.value)
