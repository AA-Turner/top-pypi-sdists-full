from enum import StrEnum

class ResolvedMenuDtoPropertiesEffectiveSelectionPlatformDefaultKind(StrEnum):
    PLATFORM_DEFAULT = "platform-default"

    def __str__(self) -> str:
        return str(self.value)
