from enum import StrEnum

class ReviewStateDecision(StrEnum):
    APPROVED = "approved"
    CHANGES_REQUESTED = "changes_requested"
    NONE = "none"
    REVIEW_REQUIRED = "review_required"

    def __str__(self) -> str:
        return str(self.value)
