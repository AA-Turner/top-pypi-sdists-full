from enum import Enum


class OnboardingVerificationValidationMethodEnum(str, Enum):
    AUSTRIAN_BUSINESS_REGISTER_WIRTSCHAFTSCOMPASS = "Austrian Business Register (WirtschaftsCompass)"
    ESTONIAN_BUSINESS_REGISTER_ARIREGISTER = "Estonian Business Register (ariregister)"
    NORWEGIAN_BUSINESS_REGISTER_BRREG = "Norwegian Business Register (Brreg)"
    SWEDISH_BUSINESS_REGISTER_BOLAGSVERKET = "Swedish Business Register (Bolagsverket)"

    def __str__(self) -> str:
        return str(self.value)
