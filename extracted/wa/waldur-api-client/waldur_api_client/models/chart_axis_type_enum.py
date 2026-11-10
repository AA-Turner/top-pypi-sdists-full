from enum import Enum


class ChartAxisTypeEnum(str, Enum):
    CATEGORY = "category"
    LOG = "log"
    TIME = "time"
    VALUE = "value"

    def __str__(self) -> str:
        return str(self.value)
