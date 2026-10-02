from enum import Enum


class ProposalReviewStateEnum(str, Enum):
    IN_REVIEW = "in_review"
    REJECTED = "rejected"
    SUBMITTED = "submitted"

    def __str__(self) -> str:
        return str(self.value)
