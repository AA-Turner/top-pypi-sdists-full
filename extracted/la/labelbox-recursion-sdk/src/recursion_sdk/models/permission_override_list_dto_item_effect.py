from enum import StrEnum

class PermissionOverrideListDtoItemEffect(StrEnum):
    ALLOW = "allow"
    DENY = "deny"

    def __str__(self) -> str:
        return str(self.value)
