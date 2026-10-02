from enum import StrEnum

class CustomerSecretListDtoItemsPropertiesScopeOrgLevel(StrEnum):
    ORG = "org"

    def __str__(self) -> str:
        return str(self.value)
