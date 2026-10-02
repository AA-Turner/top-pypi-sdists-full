from enum import StrEnum

class RunConfigDtoPropertiesScopeOrgLevel(StrEnum):
    ORG = "org"

    def __str__(self) -> str:
        return str(self.value)
