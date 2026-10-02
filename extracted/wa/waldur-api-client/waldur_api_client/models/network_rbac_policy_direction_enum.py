from enum import Enum


class NetworkRBACPolicyDirectionEnum(str, Enum):
    ALL = "all"
    INBOUND = "inbound"
    OUTBOUND = "outbound"

    def __str__(self) -> str:
        return str(self.value)
