from enum import Enum


class ProposalStates(str, Enum):
    ACCEPTED = "accepted"
    CANCELED = "canceled"
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    REJECTED = "rejected"
    SUBMITTED = "submitted"

    def __str__(self) -> str:
        return str(self.value)
