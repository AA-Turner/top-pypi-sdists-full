from enum import Enum


class ValidationMethodEnum(str, Enum):
    ARIREGISTER = "ariregister"
    BOLAGSVERKET = "bolagsverket"
    BREG = "breg"
    DNB_DK = "dnb_dk"
    DNB_FI = "dnb_fi"
    DNB_NO = "dnb_no"
    DNB_SE = "dnb_se"
    WIRTSCHAFTSCOMPASS = "wirtschaftscompass"

    def __str__(self) -> str:
        return str(self.value)
