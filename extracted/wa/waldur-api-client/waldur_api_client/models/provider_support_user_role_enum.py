from enum import Enum


class ProviderSupportUserRoleEnum(str, Enum):
    AGENT = "agent"
    MANAGER = "manager"

    def __str__(self) -> str:
        return str(self.value)
