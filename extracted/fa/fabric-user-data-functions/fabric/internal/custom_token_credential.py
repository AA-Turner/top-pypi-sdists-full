# flake8: noqa: I005
import jwt
from azure.core.credentials import AccessToken, TokenCredential  # noqa: I900


class CustomTokenCredential(TokenCredential):
    def __init__(self, token: str):
        alg = jwt.get_unverified_header(token)['alg']
        decoded_access_token = jwt.decode(token, algorithms=[alg], options={"verify_signature": False,  # Needed or else it complains about Exception: ValueError: Unable to load PEM file.
                                                                            "verify_exp": False}  # Needed to not throw if the access token is already expired
                                          )
        # Token Expiry
        token_expiry = decoded_access_token["exp"]

        self._token = AccessToken(token, token_expiry)

    def get_token(self, *scopes, **kwargs) -> AccessToken:
        return self._token
