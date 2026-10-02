from enum import Enum


class OnboardingVerificationStatusEnum(str, Enum):
    ESCALATED = "escalated"
    EXPIRED = "expired"
    FAILED = "failed"
    PENDING = "pending"
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
