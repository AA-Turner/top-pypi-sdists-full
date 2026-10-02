from enum import Enum


class OnboardingJustificationValidationDecisionEnum(str, Enum):
    APPROVED = "Approved"
    PENDING_REVIEW = "Pending Review"
    REJECTED = "Rejected"

    def __str__(self) -> str:
        return str(self.value)
