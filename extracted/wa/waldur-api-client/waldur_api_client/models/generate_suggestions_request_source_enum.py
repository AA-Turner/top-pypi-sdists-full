from enum import Enum


class GenerateSuggestionsRequestSourceEnum(str, Enum):
    ALL_PROPOSALS = "all_proposals"
    CALL_DESCRIPTION = "call_description"
    CUSTOM_KEYWORDS = "custom_keywords"
    SELECTED_PROPOSALS = "selected_proposals"

    def __str__(self) -> str:
        return str(self.value)
