from enum import Enum


class CallReviewerPoolOEnum(str, Enum):
    CREATED = "created"
    CURRENT_ASSIGNMENTS = "current_assignments"
    EXPERTISE_MATCH_SCORE = "expertise_match_score"
    INVITED_AT = "invited_at"
    VALUE_0 = "-created"
    VALUE_1 = "-current_assignments"
    VALUE_2 = "-expertise_match_score"
    VALUE_3 = "-invited_at"

    def __str__(self) -> str:
        return str(self.value)
