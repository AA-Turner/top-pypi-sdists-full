from enum import StrEnum

class CustomerSecretDtoPropertiesScopeSystemLevel(StrEnum):
    SYSTEM = "system"

    def __str__(self) -> str:
        return str(self.value)
