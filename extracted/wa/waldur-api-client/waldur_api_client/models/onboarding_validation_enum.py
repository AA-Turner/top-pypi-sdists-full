from enum import Enum


class OnboardingValidationEnum(str, Enum):
    ARIREGISTER = "ariregister"
    BOLAGSVERKET = "bolagsverket"
    DNB_DK = "dnb_dk"
    DNB_FI = "dnb_fi"
    DNB_NO = "dnb_no"
    DNB_SE = "dnb_se"
    WIRTSCHAFTSCOMPASS = "wirtschaftscompass"

    def __str__(self) -> str:
        return str(self.value)
