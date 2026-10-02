from enum import Enum


class ChecklistOperators(str, Enum):
    CONTAINS = "contains"
    EQUALS = "equals"
    IN = "in"
    NOT_EQUALS = "not_equals"
    NOT_IN = "not_in"

    def __str__(self) -> str:
        return str(self.value)
