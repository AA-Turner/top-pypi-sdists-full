from enum import Enum


class OnboardingVerificationStatusEnum1(str, Enum):
    ESCALATED_FOR_MANUAL_VALIDATION = "Escalated for manual validation"
    EXPIRED = "Expired"
    FAILED = "Failed"
    PENDING = "Pending"
    VERIFIED = "Verified"

    def __str__(self) -> str:
        return str(self.value)
