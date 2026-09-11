from enum import Enum


class PrincipalKind(str, Enum):
    HUMAN = "human"
    MANAGED = "managed"
    SERVICE_ACCOUNT = "service_account"

    def __str__(self) -> str:
        return str(self.value)
