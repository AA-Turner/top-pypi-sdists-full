from enum import Enum


class OnboardingJustificationOEnum(str, Enum):
    CREATED = "created"
    MODIFIED = "modified"
    VALIDATED_AT = "validated_at"
    VALUE_0 = "-created"
    VALUE_1 = "-modified"
    VALUE_2 = "-validated_at"

    def __str__(self) -> str:
        return str(self.value)
