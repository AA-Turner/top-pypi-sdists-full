from enum import Enum


class AuthKindEnum(str, Enum):
    OIDC = "oidc"
    PAT = "pat"
    SESSION = "session"
    TOKEN = "token"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
