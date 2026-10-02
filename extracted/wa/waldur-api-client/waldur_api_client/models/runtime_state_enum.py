from enum import Enum


class RuntimeStateEnum(str, Enum):
    ACTIVE = "Active"
    PENDING_ACCOUNT_LINKING = "Pending account linking"
    PENDING_ADDITIONAL_VALIDATION = "Pending additional validation"

    def __str__(self) -> str:
        return str(self.value)
