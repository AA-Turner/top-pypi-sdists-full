from enum import Enum


class SramProjectRuleMatch(str, Enum):
    EXACT = "exact"
    PREFIX = "prefix"
    REGEX = "regex"

    def __str__(self) -> str:
        return str(self.value)
