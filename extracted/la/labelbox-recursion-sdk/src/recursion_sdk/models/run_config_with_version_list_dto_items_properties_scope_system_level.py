from enum import StrEnum

class RunConfigWithVersionListDtoItemsPropertiesScopeSystemLevel(StrEnum):
    SYSTEM = "system"

    def __str__(self) -> str:
        return str(self.value)
