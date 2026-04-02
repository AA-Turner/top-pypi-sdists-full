from enum import Enum


class AssignmentItemOEnum(str, Enum):
    AFFINITY_SCORE = "affinity_score"
    CREATED = "created"
    RESPONDED_AT = "responded_at"
    STATUS = "status"
    VALUE_0 = "-affinity_score"
    VALUE_1 = "-created"
    VALUE_2 = "-responded_at"
    VALUE_3 = "-status"

    def __str__(self) -> str:
        return str(self.value)
