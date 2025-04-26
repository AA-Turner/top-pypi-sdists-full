from __future__ import annotations

from typing import Protocol

from benchling_api_client.v2.benchling_client import AuthorizationMethod


class BearerTokenProvider(Protocol):
    """A callable function for providing a bearer token."""

    def __call__(self, base_url: str) -> str:
        """Return a bearer token to be used with an HTTP Authorization header."""
        pass


class BearerTokenAuth(AuthorizationMethod):
    """
    Bearer Token Authorization.

    Use in combination with the Benchling() client constructor to be authorized with Bearer Token Authorization
    """

    _token_function: BearerTokenProvider

    def __init__(self, token_function: BearerTokenProvider) -> None:
        """Init BearerTokenAuth with a callable BearerTokenProvider for providing bearer tokens."""
        super().__init__()
        self._token_function = token_function

    @classmethod
    def from_token(cls, bearer_token: str) -> BearerTokenAuth:
        """Create a BearerTokenAuth that always uses a static bearer token string."""
        return cls(lambda base_url: bearer_token)

    def get_authorization_header(self, base_url: str) -> str:
        """Get content for a HTTP Authorization header."""
        return f"Bearer {self._token_function(base_url)}"
