from enum import StrEnum

class RunConfigDtoPropertiesScopeSystemLevel(StrEnum):
    SYSTEM = "system"

    def __str__(self) -> str:
        return str(self.value)
