from typing import Callable, Tuple

import grpc

_SIGNATURE_HEADER_KEY = "authorization"


class Auth0Client(grpc.AuthMetadataPlugin):
    def __init__(self):
        self._auth_client = None

    def __call__(
        self,
        context: grpc.AuthMetadataContext,
        callback: Callable[[Tuple[Tuple[str, str]], None], None],
    ):
        """Implements authentication by passing metadata to a callback.

        Args:
            context: An AuthMetadataContext providing information on the RPC that
                the plugin is being called to authenticate.
            callback: A callback that accepts a tuple of metadata key/value pairs and a None
                parameter.
        """
        # Get token from Auth0 client
        token = self.get_token()
        metadata = ((_SIGNATURE_HEADER_KEY, f"Bearer {token}"),)
        callback(metadata, None)

    def get_token(self) -> str:
        """Get the authentication token."""
        if not self._auth_client:
            from qwak.inner.tool.auth import Auth0ClientBase

            self._auth_client = Auth0ClientBase()
        return self._auth_client.get_token()
