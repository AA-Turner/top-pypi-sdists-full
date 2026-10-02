from enum import Enum


class AuthTypeEnum(str, Enum):
    PASSWORD = "password"
    V3APPLICATIONCREDENTIAL = "v3applicationcredential"

    def __str__(self) -> str:
        return str(self.value)
