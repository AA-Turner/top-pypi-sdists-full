from enum import Enum


class KeywordSearchModeEnum(str, Enum):
    EXPERTISE_ONLY = "expertise_only"
    FULL_TEXT = "full_text"

    def __str__(self) -> str:
        return str(self.value)
