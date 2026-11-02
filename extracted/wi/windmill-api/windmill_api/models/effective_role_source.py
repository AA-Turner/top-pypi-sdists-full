from enum import Enum


class EffectiveRoleSource(str, Enum):
    INSTANCE = "instance"
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)
