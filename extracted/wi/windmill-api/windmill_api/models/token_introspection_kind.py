from enum import Enum


class TokenIntrospectionKind(str, Enum):
    API_TOKEN = "api_token"
    EXTERNAL = "external"
    JWT = "jwt"
    SESSION = "session"
    SUPERADMIN_SECRET = "superadmin_secret"

    def __str__(self) -> str:
        return str(self.value)
