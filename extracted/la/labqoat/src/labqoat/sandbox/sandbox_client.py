"""A sandbox host: the one a worker was launched beside, or one another run serves."""

from collections.abc import Mapping
from pathlib import Path
from typing import ClassVar, Unpack

from labqoat.json_document import JsonDocument
from labqoat.sandbox.sandbox import Sandbox
from labqoat.sandbox.sandbox_admission import SandboxAdmission
from labqoat.sandbox.sandbox_capacity import SandboxCapacity
from labqoat.sandbox.sandbox_creation import SandboxCreation
from labqoat.sandbox.sandbox_not_found_error import SandboxNotFoundError
from labqoat.sandbox.sandbox_options import SandboxOptions
from labqoat.sandbox.sandbox_request import SandboxRequest
from labqoat.sandbox.sandbox_response import SandboxResponse
from labqoat.sandbox.sandbox_route import SandboxRoute
from labqoat.sandbox.sandbox_state import SandboxState
from labqoat.sandbox.sandbox_transport import SandboxTransport
from labqoat.sandbox.sandbox_unavailable_error import SandboxUnavailableError


class SandboxClient:
    """Create and find sandboxes and read a host's budget, over its worker's private socket or through a service."""

    WAIT_SECONDS: ClassVar[float] = 900.0

    def __init__(
        self, socket_path: str | Path | None = None, *, timeout: float = 180.0, route: SandboxRoute | None = None
    ) -> None:
        """Bind a host: a socket path, an explicit route, or by default what the environment names.

        ``timeout`` is the seconds to wait for any answer that is not held open on purpose.
        """
        chosen = route or (
            SandboxRoute.from_environment() if socket_path is None else SandboxRoute.local(str(socket_path))
        )
        self._transport = SandboxTransport(chosen, timeout)

    @classmethod
    def served(cls, url: str, headers: Mapping[str, str], *, timeout: float = 180.0) -> "SandboxClient":
        """Bind a host whose worker serves its sandbox socket under a name.

        Give a service's ``url`` and ``headers``, as ``context.service(name)`` returns them. The host's worker
        offers them with ``context.serve(name, unix_socket=SandboxClient.socket_path())``.
        """
        return cls(timeout=timeout, route=SandboxRoute.served(url, headers))

    @staticmethod
    def socket_path() -> str:
        """Return the private socket of the host this worker was launched beside, for serving it to others."""
        route = SandboxRoute.from_environment()
        if route.socket_path is None:
            raise SandboxUnavailableError(f"{SandboxRoute.SOCKET_VARIABLE} is not set: this worker hosts no sandboxes")
        return route.socket_path

    def capacity(self) -> SandboxCapacity:
        """Report the host's budget, the part in use, and the sandboxes holding it."""
        content = self._transport.send(SandboxRequest("GET", "/sandboxes"))
        return SandboxResponse.decoded(content, SandboxCapacity.decode)

    async def capacity_async(self) -> SandboxCapacity:
        """Report capacity without blocking the event loop; see ``capacity``."""
        content = await self._transport.send_async(SandboxRequest("GET", "/sandboxes"))
        return SandboxResponse.decoded(content, SandboxCapacity.decode)

    def create(self, *entrypoint: str, **options: Unpack[SandboxOptions]) -> Sandbox:
        """Start a sandbox and return its handle; with ``entrypoint`` arguments it runs that command.

        Without an entrypoint the sandbox idles until it ends. With one it ends when the command exits, and
        ``wait`` returns the command's exit code; ``stdout`` and ``stderr`` read its output and ``workdir`` is
        where it starts. ``readiness_probe`` (``Probe.with_tcp(port)`` or ``Probe.with_exec(...)``) tells when
        such a server is ready, for ``wait_until_ready``.

        A host launched with one image needs no ``image``; one launched with several must be told which.
        ``cpu`` and ``memory`` are in a function's units, cores and MiB, with a function's defaults:
        ``memory`` is reserved from the host's budget, and ``cpu`` is the most the sandbox may use of the CPU
        all the host's sandboxes share. ``gpu`` gives the sandbox that many of the GPUs the host keeps for its
        sandboxes (``Sandboxes(driver_gpu=...)``), none by default. The host ends the sandbox ``timeout`` seconds after it started (5
        minutes by default, 24 hours at most), and with ``idle_timeout`` once that long passes with no
        process of its own running and no request about it. ``env`` sets variables for everything in it.

        ``name`` is unique among the host's running sandboxes and finds it with ``from_name``; ``tags`` are
        labels ``list`` filters by. Without ``sandbox_id`` a fresh identifier is generated. ``volumes`` maps a
        path in the sandbox to the path one of this worker's volumes is mounted at, which the sandbox then sees
        read-only. ``network=True`` gives the sandbox the worker's outbound network; without it the sandbox has
        none. A sequence of host names, such as ``["pypi.org", "files.pythonhosted.org"]``, lets it reach
        exactly those hosts over TCP at the public addresses they have when the sandbox starts, and resolve no
        other name. ``ports`` lists ports this worker reaches inside the sandbox through ``tunnel(port)``,
        such as a verifier's server; the sandbox gets no outbound network from them. ``wait`` is how many seconds to keep asking while the budget is full
        before the refusal is raised: 15 minutes by default, so creations beyond the budget queue until sandboxes
        end; ``wait=0`` refuses at once.
        """
        request = SandboxCreation.request(entrypoint, options)
        content = SandboxAdmission(self._transport, options.get("wait", self.WAIT_SECONDS)).send(request)
        return SandboxResponse.decoded(content, self._sandbox)

    async def create_async(self, *entrypoint: str, **options: Unpack[SandboxOptions]) -> Sandbox:
        """Start a sandbox without blocking the event loop; see ``create``."""
        request = SandboxCreation.request(entrypoint, options)
        content = await SandboxAdmission(self._transport, options.get("wait", self.WAIT_SECONDS)).send_async(request)
        return SandboxResponse.decoded(content, self._sandbox)

    def from_id(self, sandbox_id: str) -> Sandbox:
        """Return a handle on a sandbox by identifier without contacting the host.

        Use it to terminate a sandbox whose creation was interrupted before the host's answer arrived, or one
        that ``capacity`` lists and no handle remains for. Using a sandbox that does not exist raises
        ``SandboxNotFoundError``.
        """
        return Sandbox(sandbox_id, self._transport)

    def from_name(self, name: str) -> Sandbox:
        """Return the running sandbox created under ``name``, or raise ``SandboxNotFoundError``."""
        return self._named(name, self._running(self._transport.send(SandboxRequest("GET", "/sandboxes"))))

    async def from_name_async(self, name: str) -> Sandbox:
        """Find a sandbox by name without blocking the event loop; see ``from_name``."""
        content = await self._transport.send_async(SandboxRequest("GET", "/sandboxes"))
        return self._named(name, self._running(content))

    def list(self, tags: Mapping[str, str] | None = None) -> tuple[Sandbox, ...]:
        """Return the host's running sandboxes, only those carrying every one of ``tags`` when given."""
        return self._tagged(tags, self._running(self._transport.send(SandboxRequest("GET", "/sandboxes"))))

    async def list_async(self, tags: Mapping[str, str] | None = None) -> tuple[Sandbox, ...]:
        """List running sandboxes without blocking the event loop; see ``list``."""
        content = await self._transport.send_async(SandboxRequest("GET", "/sandboxes"))
        return self._tagged(tags, self._running(content))

    def _sandbox(self, document: JsonDocument) -> Sandbox:
        """Bind the identifier the host confirmed to this client's host."""
        return Sandbox(JsonDocument.expect_scalar(document["id"], str), self._transport)

    @staticmethod
    def _running(content: bytes) -> tuple[SandboxState, ...]:
        """Read the sandboxes a capacity document lists."""
        return SandboxResponse.decoded(content, SandboxState.listed)

    def _named(self, name: str, running: tuple[SandboxState, ...]) -> Sandbox:
        """Pick the one sandbox with a name."""
        for state in running:
            if state.name == name:
                return Sandbox(state.id, self._transport)
        raise SandboxNotFoundError(f"No running sandbox on this host is named {name}")

    def _tagged(self, tags: Mapping[str, str] | None, running: tuple[SandboxState, ...]) -> tuple[Sandbox, ...]:
        """Keep the sandboxes that carry every wanted tag."""
        wanted = dict(tags or {}).items()
        return tuple(Sandbox(state.id, self._transport) for state in running if wanted <= state.tags.items())
