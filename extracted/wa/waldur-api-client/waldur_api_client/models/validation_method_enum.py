from enum import Enum


class ValidationMethodEnum(str, Enum):
    ARIREGISTER = "ariregister"
    BOLAGSVERKET = "bolagsverket"
    BREG = "breg"
    WIRTSCHAFTSCOMPASS = "wirtschaftscompass"

    def __str__(self) -> str:
        return str(self.value)
