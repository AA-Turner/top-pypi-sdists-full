from enum import Enum


class ChangelogEntryListTypeEnum(str, Enum):
    BREAKING = "breaking"
    DEPRECATION = "deprecation"
    FEATURE = "feature"
    FIX = "fix"
    IMPROVEMENT = "improvement"
    SECURITY = "security"

    def __str__(self) -> str:
        return str(self.value)
