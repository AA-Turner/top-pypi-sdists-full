from enum import Enum


class IntrospectTokenResponse200Kind(str, Enum):
    API_TOKEN = "api_token"
    EXTERNAL = "external"
    JWT = "jwt"
    SESSION = "session"
    SUPERADMIN_SECRET = "superadmin_secret"

    def __str__(self) -> str:
        return str(self.value)
