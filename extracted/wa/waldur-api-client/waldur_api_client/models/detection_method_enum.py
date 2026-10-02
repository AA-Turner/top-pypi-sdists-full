from enum import Enum


class DetectionMethodEnum(str, Enum):
    AUTOMATED = "automated"
    MANAGER_IDENTIFIED = "manager_identified"
    REPORTED = "reported"
    SELF_DISCLOSED = "self_disclosed"

    def __str__(self) -> str:
        return str(self.value)
