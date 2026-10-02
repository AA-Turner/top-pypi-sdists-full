from enum import StrEnum

class CreateRunConfigDtoPropertiesScopeOrgLevel(StrEnum):
    ORG = "org"

    def __str__(self) -> str:
        return str(self.value)
