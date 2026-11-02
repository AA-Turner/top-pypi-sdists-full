"""A client library for accessing Octostar API"""

from .client import AuthenticatedClient, Client, make_client

__all__ = (
    "AuthenticatedClient",
    "Client",
    "make_client",
)
