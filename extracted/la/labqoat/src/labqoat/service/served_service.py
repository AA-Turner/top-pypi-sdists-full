"""A local HTTP server served to the worker's project for the length of a block."""

from contextlib import ExitStack
from threading import Event
from time import monotonic
from types import TracebackType

from labqoat.service.service_endpoint import ServiceEndpoint
from labqoat.service.service_loop import ServiceLoop
from labqoat.service.service_target import ServiceTarget
from labqoat.service.service_tunnel import ServiceTunnel


class ServedService:
    """Serve a local server under a name from the moment the block is entered until it is left.

    Entering waits for the server to listen and for the tunnel to open, so code inside the block may tell
    others the service is there. The tunnel runs on a thread of its own and never blocks the worker's code.
    """

    def __init__(self, endpoint: ServiceEndpoint, target: ServiceTarget, startup_timeout: float) -> None:
        """Bind what is served and where, without contacting anything yet."""
        self.name = endpoint.name
        self.url = endpoint.call_url()
        self._endpoint = endpoint
        self._target = target
        self._startup_timeout = startup_timeout
        self._serving = ExitStack()

    def __enter__(self) -> "ServedService":
        """Wait for the local server, open the tunnel, and fail if either takes longer than the startup allows."""
        deadline = monotonic() + self._startup_timeout
        self._target.wait(self._startup_timeout, f"service {self.name}")
        opened = Event()
        tunnel = ServiceTunnel(self._endpoint, self._target, opened)
        self._serving.callback(ServiceLoop(f"labqoat-service-{self.name}", tunnel.serve()).stop)
        if not opened.wait(max(deadline - monotonic(), 0.0)):
            self._serving.close()
            raise TimeoutError(f"Service {self.name} could not be opened within {self._startup_timeout:g} s")
        return self

    def __exit__(
        self, kind: type[BaseException] | None, error: BaseException | None, trace: TracebackType | None
    ) -> None:
        """Stop serving; requests in flight are abandoned."""
        self._serving.close()
