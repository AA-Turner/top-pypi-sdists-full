from enum import StrEnum

class RunConfigListItemListDtoItemsPropertiesScopeOrgLevel(StrEnum):
    ORG = "org"

    def __str__(self) -> str:
        return str(self.value)
