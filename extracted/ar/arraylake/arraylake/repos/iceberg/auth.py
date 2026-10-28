"""PyIceberg authentication using Arraylake's cached user login.

Loaded only by the optional PyIceberg integration. Expiry is inspected locally
for refresh scheduling; the API still verifies the token's signature and claims.
"""

from pyiceberg.catalog.rest.auth import AuthManager

from arraylake.token import get_fresh_id_token


class ArraylakeAuthManager(AuthManager):
    """Supply a current ID token, refreshing the cached login before expiry."""

    def __init__(self, service_uri: str):
        self.service_uri = service_uri

    def auth_header(self) -> str:
        return f"Bearer {get_fresh_id_token(self.service_uri)}"
