from enum import Enum


class OnboardingVerificationValidationMethodEnum(str, Enum):
    AUSTRIAN_BUSINESS_REGISTER_WIRTSCHAFTSCOMPASS = "Austrian Business Register (WirtschaftsCompass)"
    DUN_BRADSTREET_DENMARK = "Dun & Bradstreet Denmark"
    DUN_BRADSTREET_FINLAND = "Dun & Bradstreet Finland"
    DUN_BRADSTREET_NORWAY = "Dun & Bradstreet Norway"
    DUN_BRADSTREET_SWEDEN = "Dun & Bradstreet Sweden"
    ESTONIAN_BUSINESS_REGISTER_ARIREGISTER = "Estonian Business Register (ariregister)"
    NORWEGIAN_BUSINESS_REGISTER_BRREG = "Norwegian Business Register (Brreg)"
    SWEDISH_BUSINESS_REGISTER_BOLAGSVERKET = "Swedish Business Register (Bolagsverket)"

    def __str__(self) -> str:
        return str(self.value)
