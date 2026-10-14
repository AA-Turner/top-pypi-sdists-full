from enum import Enum


class LoadBalancerModeEnum(str, Enum):
    DISABLED = "disabled"
    OPTIONAL = "optional"
    REQUIRED = "required"

    def __str__(self) -> str:
        return str(self.value)
