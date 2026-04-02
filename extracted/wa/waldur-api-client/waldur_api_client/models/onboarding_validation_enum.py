from enum import Enum


class OnboardingValidationEnum(str, Enum):
    ARIREGISTER = "ariregister"
    BOLAGSVERKET = "bolagsverket"
    WIRTSCHAFTSCOMPASS = "wirtschaftscompass"

    def __str__(self) -> str:
        return str(self.value)
