from enum import Enum


class GetOidcSigningStatusResponse200KeysItemState(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"
    PUBLISHED = "published"
    RETIRED = "retired"

    def __str__(self) -> str:
        return str(self.value)
