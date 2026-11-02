"""When a request to a served sandbox host is sent again, and for how long."""

from collections.abc import Mapping
from time import monotonic
from typing import ClassVar

from labqoat.sandbox.sandbox_request import SandboxRequest


class SandboxRetry:
    """Ride out a served host's tunnel being opened again, as it is whenever the platform is redeployed.

    A request the platform refused because nothing served the name never reached the host, so any request is
    sent again. A request lost on the way, or answered with a timeout or a broken stream, is sent again only
    when sending it twice does what sending it once does: reads, deletions and a file's first piece. A host
    reached over its own socket is never retried: nothing between the caller and the host can come back.
    """

    SECONDS: ClassVar[float] = 300.0
    PAUSE: ClassVar[float] = 2.0
    UNSERVED: ClassVar[str] = "x-labqoat-service-status"
    LOST: ClassVar[frozenset[int]] = frozenset({408, 502, 504})

    def __init__(self, served: bool) -> None:
        """Start the clock for one request; a request over a socket has no time to retry in."""
        self._deadline = monotonic() + self.SECONDS if served else 0.0

    def refused(self, request: SandboxRequest, status: int, headers: Mapping[str, str]) -> bool:
        """Whether a failed answer may be followed by the same request."""
        if monotonic() >= self._deadline:
            return False
        return (status == 503 and self.UNSERVED in headers) or (status in self.LOST and self.idempotent(request))

    def lost(self, request: SandboxRequest) -> bool:
        """Whether a request whose answer never came may be sent again."""
        return monotonic() < self._deadline and self.idempotent(request)

    @staticmethod
    def idempotent(request: SandboxRequest) -> bool:
        """Whether sending the request twice leaves the host as sending it once does."""
        return request.method in ("GET", "DELETE") or (request.method == "PUT" and "append" not in request.query)
