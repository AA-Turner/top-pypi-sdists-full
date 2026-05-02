from spotipyio.auth.spotify_grant_type import SpotifyGrantType
from spotipyio.logic.consts.api_consts import GRANT_TYPE, CODE, REDIRECT_URI, JSON, REFRESH_TOKEN, CLIENT_ID


class AuthorizationPayloadBuilder:
    @staticmethod
    def build(grant_type: SpotifyGrantType, access_code: str, redirect_uri: str, client_id: str) -> dict:
        if grant_type == SpotifyGrantType.AUTHORIZATION_CODE:
            return {GRANT_TYPE: grant_type.value, CODE: access_code, REDIRECT_URI: redirect_uri, JSON: True}

        elif grant_type == SpotifyGrantType.REFRESH_TOKEN:
            return {GRANT_TYPE: grant_type.value, REFRESH_TOKEN: access_code, CLIENT_ID: client_id}

        elif grant_type == SpotifyGrantType.CLIENT_CREDENTIALS:
            return {GRANT_TYPE: grant_type.value, JSON: True}

        raise ValueError("Did not recognize grant type")
