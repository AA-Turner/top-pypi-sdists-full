from enum import Enum


class GetOidcSigningStatusResponse200SignerBreaker(str, Enum):
    CLOSED = "closed"
    HALF_OPEN = "half_open"
    OPEN = "open"

    def __str__(self) -> str:
        return str(self.value)
