from enum import Enum


class LinkTypeEnum(str, Enum):
    BLOCKED_BY = "blocked_by"
    DUPLICATES = "duplicates"
    RELATED = "related"

    def __str__(self) -> str:
        return str(self.value)
