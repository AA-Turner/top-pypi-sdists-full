from enum import Enum


class FeedbackCategoryEnum(str, Enum):
    INACCURATE = "inaccurate"
    INCOMPLETE = "incomplete"
    MISUNDERSTOOD = "misunderstood"
    OTHER = "other"
    SLOW_OR_FAILED = "slow_or_failed"

    def __str__(self) -> str:
        return str(self.value)
