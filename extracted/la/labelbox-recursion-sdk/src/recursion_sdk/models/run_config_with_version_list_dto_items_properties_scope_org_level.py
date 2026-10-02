from enum import StrEnum

class RunConfigWithVersionListDtoItemsPropertiesScopeOrgLevel(StrEnum):
    ORG = "org"

    def __str__(self) -> str:
        return str(self.value)
