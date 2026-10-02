from enum import StrEnum

class CreateCustomerSecretDtoPropertiesScopeSystemLevel(StrEnum):
    SYSTEM = "system"

    def __str__(self) -> str:
        return str(self.value)
