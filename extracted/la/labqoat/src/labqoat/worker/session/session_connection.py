"""A worker's credential-bearing WebSocket handshake never follows redirects."""

from websockets.asyncio.client import connect


class SessionConnection(connect):
    """Retain the explicitly configured worker origin for every handshake."""

    def process_redirect(self, exc: Exception) -> Exception:
        """Reject redirects before credentials can reach another endpoint."""
        return exc
