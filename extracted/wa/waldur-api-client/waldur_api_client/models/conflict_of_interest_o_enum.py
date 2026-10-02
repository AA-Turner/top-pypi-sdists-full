from enum import Enum


class ConflictOfInterestOEnum(str, Enum):
    CREATED = "created"
    DETECTED_AT = "detected_at"
    SEVERITY = "severity"
    STATUS = "status"
    VALUE_0 = "-created"
    VALUE_1 = "-detected_at"
    VALUE_2 = "-severity"
    VALUE_3 = "-status"

    def __str__(self) -> str:
        return str(self.value)
