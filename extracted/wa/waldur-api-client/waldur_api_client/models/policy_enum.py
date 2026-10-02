from enum import Enum


class PolicyEnum(str, Enum):
    AFFINITY = "affinity"
    ANTI_AFFINITY = "anti-affinity"
    SOFT_AFFINITY = "soft-affinity"
    SOFT_ANTI_AFFINITY = "soft-anti-affinity"

    def __str__(self) -> str:
        return str(self.value)
