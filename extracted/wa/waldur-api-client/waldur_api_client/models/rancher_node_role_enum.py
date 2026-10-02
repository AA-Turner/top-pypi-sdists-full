from enum import Enum


class RancherNodeRoleEnum(str, Enum):
    AGENT = "agent"
    SERVER = "server"

    def __str__(self) -> str:
        return str(self.value)
