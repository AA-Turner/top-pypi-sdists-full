from enum import Enum


class ReviewerSuggestionStatusEnum(str, Enum):
    CONFIRMED = "confirmed"
    INVITED = "invited"
    PENDING = "pending"
    REJECTED = "rejected"

    def __str__(self) -> str:
        return str(self.value)
