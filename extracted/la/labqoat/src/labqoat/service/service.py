"""A named service of the project, as one of its callers sees it."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from time import monotonic
from time import sleep as pause
from typing import ClassVar

from labqoat.net.http_client import HttpClient
from labqoat.net.http_error import HttpError
from labqoat.net.request import Handler


@dataclass(frozen=True)
class Service:
    """Where a service answers and the headers that let a request through to it.

    ``url`` is the base address: the service's own paths go after it. ``headers`` carry this caller's
    credentials, which stop at the platform; anything else a request sends reaches the service unchanged.
    Requests naming the same ``X-Labqoat-Session`` reach the same serving worker.
    """

    UNAVAILABLE: ClassVar[str] = "x-labqoat-service-status"
    PROBE_SECONDS: ClassVar[float] = 0.5

    name: str
    url: str
    headers: Mapping[str, str] = field(repr=False)
    handler: Handler | None = field(default=None, repr=False, compare=False)

    def available(self) -> bool:
        """Report whether a worker serves the name right now, by asking for its root."""
        try:
            with HttpClient(timeout=30.0, handler=self.handler, proxy=True) as client:
                response = client.request("GET", self.url + "/", headers=dict(self.headers))
        except HttpError:
            return False
        return self.UNAVAILABLE not in response.headers

    def wait(self, timeout: float = 600.0) -> "Service":
        """Return once a worker serves the name, or raise when none does within ``timeout`` seconds."""
        deadline = monotonic() + timeout
        while not self.available():
            if monotonic() >= deadline:
                raise TimeoutError(f"No worker served {self.name} within {timeout:g} s")
            pause(self.PROBE_SECONDS)
        return self
