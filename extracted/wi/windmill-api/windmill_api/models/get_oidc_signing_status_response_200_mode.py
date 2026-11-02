from enum import Enum


class GetOidcSigningStatusResponse200Mode(str, Enum):
    DATABASE = "database"
    EXTERNAL = "external"
    FILE = "file"

    def __str__(self) -> str:
        return str(self.value)
