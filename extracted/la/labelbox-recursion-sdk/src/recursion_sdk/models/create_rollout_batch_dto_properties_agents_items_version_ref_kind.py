from enum import StrEnum

class CreateRolloutBatchDtoPropertiesAgentsItemsVersionRefKind(StrEnum):
    VERSIONREF = "versionRef"

    def __str__(self) -> str:
        return str(self.value)
