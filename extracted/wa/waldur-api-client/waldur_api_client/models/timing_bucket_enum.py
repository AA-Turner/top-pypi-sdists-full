from enum import Enum


class TimingBucketEnum(str, Enum):
    EARLY = "early"
    LATE_START = "late_start"
    ON_TIME = "on_time"
    OVERRUN = "overrun"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
