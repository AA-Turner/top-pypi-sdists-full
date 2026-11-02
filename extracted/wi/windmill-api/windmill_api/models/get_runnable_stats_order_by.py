from enum import Enum


class GetRunnableStatsOrderBy(str, Enum):
    CPU = "cpu"
    MAX_MEMORY = "max_memory"
    TOTAL_DURATION = "total_duration"

    def __str__(self) -> str:
        return str(self.value)
