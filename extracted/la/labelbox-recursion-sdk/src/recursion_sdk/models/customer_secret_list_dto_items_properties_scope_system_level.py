from enum import StrEnum

class CustomerSecretListDtoItemsPropertiesScopeSystemLevel(StrEnum):
    SYSTEM = "system"

    def __str__(self) -> str:
        return str(self.value)
