from enum import StrEnum

class BindableRunConfigListDtoItemsPropertiesScopeSystemLevel(StrEnum):
    SYSTEM = "system"

    def __str__(self) -> str:
        return str(self.value)
