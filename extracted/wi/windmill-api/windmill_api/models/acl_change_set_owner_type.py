from enum import Enum


class AclChangeSetOwnerType(str, Enum):
    SET_OWNER = "set_owner"

    def __str__(self) -> str:
        return str(self.value)
