from enum import Enum


class HpcSuggestionKindEnum(str, Enum):
    CPU_EFFICIENCY = "cpu_efficiency"
    TIME_LIMIT = "time_limit"

    def __str__(self) -> str:
        return str(self.value)
