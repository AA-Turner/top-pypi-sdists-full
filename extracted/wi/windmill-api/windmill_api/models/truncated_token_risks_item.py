from enum import Enum


class TruncatedTokenRisksItem(str, Enum):
    ADMIN = "admin"
    ALL_WORKSPACES = "all_workspaces"
    NEVER_EXPIRES = "never_expires"
    SUPERADMIN = "superadmin"
    UNUSED = "unused"

    def __str__(self) -> str:
        return str(self.value)
