from enum import StrEnum

class TranscriptReformatRunDtoPropertiesResultAnyOf0ReformattedTurnsItemBlocksItemType(StrEnum):
    ASSISTANT = "assistant"
    THINKING = "thinking"

    def __str__(self) -> str:
        return str(self.value)
