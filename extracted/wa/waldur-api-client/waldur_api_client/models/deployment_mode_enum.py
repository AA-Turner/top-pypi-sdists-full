from enum import Enum


class DeploymentModeEnum(str, Enum):
    MANAGED = "managed"
    SELF_MANAGED = "self_managed"

    def __str__(self) -> str:
        return str(self.value)
