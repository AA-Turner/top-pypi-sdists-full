from enum import Enum


class AuthMethodEnum(str, Enum):
    API_TOKEN = "api_token"
    BASIC = "basic"
    OAUTH2_CLIENT_CREDENTIALS = "oauth2_client_credentials"
    PERSONAL_ACCESS_TOKEN = "personal_access_token"

    def __str__(self) -> str:
        return str(self.value)
