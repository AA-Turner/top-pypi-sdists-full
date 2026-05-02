"""
Unofficial Spotify Creators GraphQL connector.

Exports the main ``SpotifyGraphQLConnector`` class and the exception types
so that callers only need to import from ``spotifygraphqlconnector``.
"""

from .connector import (
    AuthenticationError,
    CredentialsExpired,
    MaxRetriesException,
    SpotifyGraphQLConnector,
)

__all__ = [
    "SpotifyGraphQLConnector",
    "CredentialsExpired",
    "AuthenticationError",
    "MaxRetriesException",
]
