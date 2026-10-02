from enum import Enum


class ReviewerSuggestionOEnum(str, Enum):
    AFFINITY_SCORE = "affinity_score"
    CREATED = "created"
    REVIEWED_AT = "reviewed_at"
    STATUS = "status"
    VALUE_0 = "-affinity_score"
    VALUE_1 = "-created"
    VALUE_2 = "-reviewed_at"
    VALUE_3 = "-status"

    def __str__(self) -> str:
        return str(self.value)
