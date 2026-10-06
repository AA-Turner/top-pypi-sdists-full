"""Identity-service v2 OAuth operations (admin.identity.oauth)."""

from __future__ import annotations

from typing import Any

from istari_digital_client.sdk._base import _Manager


class IdentityOAuth(_Manager):
    """Issue and introspect v2 tokens. The browser ``authorize`` redirect is not wrapped."""

    def issue_token(self, *, grant_type: str = "client_credentials", client_assertion: str | None = None,
                    client_assertion_type: str = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                    code: str | None = None, redirect_uri: str | None = None,
                    refresh_token: str | None = None) -> Any:
        """Post a client assertion (or code/refresh token) to /api/v2/oauth2/token."""
        return self._call(self._engine.identity_v2_api.issue_token, grant_type=grant_type,
                          client_assertion=client_assertion, client_assertion_type=client_assertion_type,
                          code=code, redirect_uri=redirect_uri, refresh_token=refresh_token)

    def introspect(self, token: str, *, client_assertion: str,
                   client_assertion_type: str = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer") -> Any:
        """Introspect a token at /api/v2/oauth2/introspect.

        Only a registered platform service may introspect, and it authenticates
        with ``client_assertion``: an RFC 7523 assertion audienced at the
        identity-service base URL (not the introspection endpoint).
        """
        return self._call(self._engine.identity_v2_api.introspect_token, client_assertion=client_assertion,
                          client_assertion_type=client_assertion_type, token=token)
