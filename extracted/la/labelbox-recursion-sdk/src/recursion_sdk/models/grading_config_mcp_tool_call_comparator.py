from enum import StrEnum

class GradingConfigMcpToolCallComparator(StrEnum):
    BETWEEN = "between"
    CONTAINS = "contains"
    EXACT_MATCH = "exact_match"
    GREATER_THAN = "greater_than"
    GREATER_THAN_OR_EQUAL = "greater_than_or_equal"
    LESS_THAN = "less_than"
    LESS_THAN_OR_EQUAL = "less_than_or_equal"
    REGEX = "regex"

    def __str__(self) -> str:
        return str(self.value)
