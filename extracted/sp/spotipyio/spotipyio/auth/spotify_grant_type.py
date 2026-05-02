from enum import Enum


class SpotifyGrantType(Enum):
    CLIENT_CREDENTIALS = "client_credentials"
    AUTHORIZATION_CODE = "authorization_code"
    REFRESH_TOKEN = "refresh_token"

    def __eq__(self, other):
        return self.value == other.value
