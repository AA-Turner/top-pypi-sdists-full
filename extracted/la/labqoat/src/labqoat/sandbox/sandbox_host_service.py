"""A platform sandbox host's own work: serve its machine's sandboxes until the platform retires it."""

from collections.abc import Callable
from time import sleep
from typing import ClassVar

from labqoat.run_context import RunContext
from labqoat.sandbox.sandbox_client import SandboxClient
from labqoat.worker.worker_api import WorkerApi


class SandboxHostService:
    """Serve the sandbox socket under the host's own name and ask now and then whether to stop.

    The platform answers yes once the host has had no sandbox for a while, and it never places a sandbox on a
    host after telling it to stop, so returning then strands nothing.
    """

    PREFIX: ClassVar[str] = "labqoat-sandboxes-"
    PAUSE_SECONDS: ClassVar[float] = 15.0

    def __init__(
        self, context: RunContext, api: WorkerApi | None = None, pause: Callable[[float], None] = sleep
    ) -> None:
        """Bind the run and the worker API its retirement is asked through."""
        self._context = context
        self._api = api or WorkerApi.from_environment()
        self._pause = pause

    def serve(self) -> None:
        """Return once the platform retires this host."""
        with self._context.serve(self.PREFIX + self._context.run_id, unix_socket=SandboxClient.socket_path()):
            while not self._retired():
                self._pause(self.PAUSE_SECONDS)

    def _retired(self) -> bool:
        """Ask the platform whether this host should stop now."""
        return self._api.json("POST", "/api/v1/worker/sandbox-hosts/retire", {})["retire"] is True
