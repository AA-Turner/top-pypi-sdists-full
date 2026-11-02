"""A pool of warm verifier servers in sandboxes, reached from the function that hosts them."""

import socket
import time
from collections.abc import Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor
from types import TracebackType
from typing import ClassVar

from labqoat.rl.verifier_client import VerifierClient
from labqoat.sandbox.sandbox import Sandbox
from labqoat.sandbox.sandbox_client import SandboxClient
from labqoat.sandbox.sandbox_tunnel import SandboxTunnel


class Verifiers:
    """Start ``size`` sandboxes that each run a verifier server on ``port``, and keep them until the block ends.

    Write each of ``files`` into every sandbox, start ``command``, and wait until the port answers. A server is
    then reached at a local address (``urls``), so samples are checked the moment they are produced, by this
    process or by any other process of the worker through ``client()``. Use a sandbox only for what is
    untrusted, such as code the model wrote; a trusted checker runs in the function itself.
    """

    READY_SECONDS: ClassVar[float] = 120.0

    def __init__(  # noqa: PLR0913 -- the sandbox's own options, passed through.
        self,
        command: Sequence[str],
        port: int,
        *,
        size: int = 4,
        files: Mapping[str, bytes] | None = None,
        client: SandboxClient | None = None,
        image: str | None = None,
        cpu: float = 1,
        memory: int = 1024,
        timeout: float = 86_400.0,
    ) -> None:
        """Bind what each server runs and how many there are, without starting any."""
        if size < 1:
            raise ValueError("A pool needs at least one verifier")
        self._command, self._port, self._size = tuple(command), port, size
        self._files = dict(files or {})
        self._options = {"image": image, "cpu": cpu, "memory": memory, "timeout": timeout}
        self._client = client
        self._started: list[tuple[Sandbox, SandboxTunnel]] = []

    @property
    def urls(self) -> tuple[str, ...]:
        """Where each server answers in this worker."""
        return tuple(tunnel.url for _sandbox, tunnel in self._started)

    def client(self, path: str = "/", timeout: float = 120.0) -> VerifierClient:
        """A client of every server in the pool, which another process of the worker may use."""
        return VerifierClient(self.urls, path, timeout)

    def __enter__(self) -> "Verifiers":
        """Start every server at once and return when all of them answer."""
        client = self._client or SandboxClient()
        with ThreadPoolExecutor(self._size) as starting:
            self._started = list(starting.map(lambda _index: self._start(client), range(self._size)))
        return self

    def __exit__(
        self, kind: type[BaseException] | None, error: BaseException | None, trace: TracebackType | None
    ) -> None:
        """Close every tunnel and end every sandbox."""
        for sandbox, tunnel in self._started:
            tunnel.close()
            sandbox.terminate()
        self._started = []

    def _start(self, client: SandboxClient) -> tuple[Sandbox, SandboxTunnel]:
        """One sandbox with the files written and the server listening."""
        sandbox = client.create(ports=[self._port], **self._options)  # type: ignore[arg-type]
        for path, content in self._files.items():
            sandbox.write_file(path, content)
        sandbox.exec(*self._command)
        tunnel = sandbox.tunnel(self._port)
        self._await(tunnel)
        return sandbox, tunnel

    def _await(self, tunnel: SandboxTunnel) -> None:
        """Wait until a connection through the tunnel stays open, as one does only when the server listens."""
        deadline = time.monotonic() + self.READY_SECONDS
        while not self._listening(tunnel.port):
            if time.monotonic() >= deadline:
                raise TimeoutError(f"The verifier did not listen on port {self._port} within {self.READY_SECONDS:g} s")
            time.sleep(0.5)

    @staticmethod
    def _listening(port: int) -> bool:
        """A server that does not listen has its connection closed at once by the tunnel."""
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=5) as probe:
                probe.settimeout(0.5)
                return Verifiers._held(probe)
        except ConnectionResetError:
            return False

    @staticmethod
    def _held(probe: socket.socket) -> bool:
        """An open connection stays silent; a closed one reads end of stream."""
        try:
            return probe.recv(1) != b""
        except TimeoutError:
            return True
