"""PyIceberg authentication using Arraylake's cached user login.

Loaded only by the optional PyIceberg integration. Expiry is inspected locally
for refresh scheduling; the API still verifies the token's signature and claims.
"""

import base64
import json
import threading
import time

from pyiceberg.catalog.rest.auth import AuthManager

from arraylake.asyn import sync
from arraylake.exceptions import AuthException
from arraylake.token import TokenHandler
from arraylake.types import OauthTokensResponse

# Serialize catalog refreshes, including separate catalogs sharing a token file.
# Reloading inside the lock also picks up logins/refreshes by the Arraylake client.
_refresh_lock = threading.Lock()


class ArraylakeAuthManager(AuthManager):
    """Supply a current ID token, refreshing the cached login before expiry."""

    def __init__(self, service_uri: str):
        self.service_uri = service_uri

    def auth_header(self) -> str:
        with _refresh_lock:
            handler = TokenHandler(api_endpoint=self.service_uri, raise_if_not_logged_in=True)
            assert handler.tokens is not None
            token = handler.tokens.id_token.get_secret_value()
            try:
                payload = token.split(".")[1]
                expires_at = float(json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))["exp"])
            except (IndexError, ValueError, KeyError, TypeError) as exc:
                raise AuthException("Invalid cached login token; log in again with `al auth login`.") from exc
            if expires_at <= time.time() + 60:
                sync(_refresh_login, handler)
                token = handler.tokens.id_token.get_secret_value()
            return f"Bearer {token}"


async def _refresh_login(handler: TokenHandler) -> None:
    """Refresh quietly so CLI JSON output stays machine-readable."""
    request = await handler.build_refresh_request()
    async with handler._create_async_client() as client:
        response = await client.send(request)
        if response.is_error:
            raise AuthException(f"Could not refresh Arraylake login ({response.status_code}); run `al auth login`.")
        tokens = OauthTokensResponse.model_validate_json(response.content)
    handler.update(tokens)
