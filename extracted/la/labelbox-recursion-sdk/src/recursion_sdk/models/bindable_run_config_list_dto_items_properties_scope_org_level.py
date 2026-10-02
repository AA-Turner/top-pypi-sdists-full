from enum import StrEnum

class BindableRunConfigListDtoItemsPropertiesScopeOrgLevel(StrEnum):
    ORG = "org"

    def __str__(self) -> str:
        return str(self.value)
