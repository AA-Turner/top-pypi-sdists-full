from enum import StrEnum

class ResolvedMenuDtoPropertiesEffectiveSelectionVersionedKind(StrEnum):
    VERSIONED = "versioned"

    def __str__(self) -> str:
        return str(self.value)
