from enum import StrEnum

class CreateCustomerSecretDtoPropertiesScopeOrgLevel(StrEnum):
    ORG = "org"

    def __str__(self) -> str:
        return str(self.value)
