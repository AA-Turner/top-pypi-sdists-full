from enum import Enum


class MatrixExternalLoginMethodEnum(str, Enum):
    NONE = "none"
    OIDC = "oidc"
    PASSWORD = "password"

    def __str__(self) -> str:
        return str(self.value)
