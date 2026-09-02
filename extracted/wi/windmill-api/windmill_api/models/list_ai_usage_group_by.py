from enum import Enum


class ListAiUsageGroupBy(str, Enum):
    DAY = "day"
    MODEL = "model"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
