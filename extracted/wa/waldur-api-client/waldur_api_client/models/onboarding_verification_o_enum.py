from enum import Enum


class OnboardingVerificationOEnum(str, Enum):
    CREATED = "created"
    EXPIRES_AT = "expires_at"
    MODIFIED = "modified"
    VALIDATED_AT = "validated_at"
    VALUE_0 = "-created"
    VALUE_1 = "-expires_at"
    VALUE_2 = "-modified"
    VALUE_3 = "-validated_at"

    def __str__(self) -> str:
        return str(self.value)
