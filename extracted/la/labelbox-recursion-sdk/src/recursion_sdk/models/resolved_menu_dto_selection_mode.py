from enum import StrEnum

class ResolvedMenuDtoSelectionMode(StrEnum):
    FLEXIBLE = "flexible"
    LOCKED = "locked"

    def __str__(self) -> str:
        return str(self.value)
