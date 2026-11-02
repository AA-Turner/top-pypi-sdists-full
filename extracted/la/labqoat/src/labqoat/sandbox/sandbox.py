"""A handle on one sandbox."""

import contextlib
from collections.abc import Mapping
from time import monotonic
from typing import TYPE_CHECKING, ClassVar, Unpack

from labqoat.sandbox.sandbox_error import SandboxError
from labqoat.sandbox.sandbox_snapshots import SandboxSnapshots
from labqoat.sandbox.sandbox_not_found_error import SandboxNotFoundError
from labqoat.sandbox.sandbox_process import SandboxProcess
from labqoat.sandbox.sandbox_request import SandboxRequest
from labqoat.sandbox.sandbox_response import SandboxResponse
from labqoat.sandbox.sandbox_state import SandboxState
from labqoat.sandbox.sandbox_stream_reader import SandboxStreamReader
from labqoat.sandbox.sandbox_stream_writer import SandboxStreamWriter
from labqoat.sandbox.sandbox_timeout_error import SandboxTimeoutError
from labqoat.sandbox.sandbox_transport import SandboxTransport
from labqoat.sandbox.sandbox_tunnel import SandboxTunnel
from labqoat.sandbox.sandbox_unavailable_error import SandboxUnavailableError

if TYPE_CHECKING:
    from labqoat.compute.image import Image
    from labqoat.sandbox.sandbox_platform_options import SandboxPlatformOptions


class Sandbox(SandboxSnapshots):
    """Run processes and move files in one sandbox, and follow it until it finishes.

    ``Sandbox.create`` starts one from any image, from a laptop or from any run, on a host the platform runs
    for the project; a function that declares ``sandboxes=[...]`` starts them on its own machine through
    ``SandboxClient`` instead. A sandbox is root inside. It finishes when its entrypoint exits,
    when it is terminated, or when its host ends it for its ``timeout`` or ``idle_timeout``; its exit code and
    its processes' output stay readable for about ten minutes after that. Every operation has a blocking
    form and an ``_async`` form. Anything that prevents a result raises a ``SandboxError``. Used as a context
    manager, the sandbox is terminated on exit unless it was detached.
    """

    WAIT_SECONDS: ClassVar[float] = 60.0
    ANSWER_SECONDS: ClassVar[float] = 30.0

    @classmethod
    def create(cls, *entrypoint: str, image: "str | Image", **options: "Unpack[SandboxPlatformOptions]") -> "Sandbox":
        """Start a sandbox the platform places, from a laptop or from any run, and return its handle.

        ``image`` is a registry reference, such as ``python:3.12-slim``, pulled anonymously unless it is in the
        platform's own registry, or a ``compute.Image``, which the platform builds first. ``secrets`` become
        environment variables, as for a function; a run gives only secrets it was given. ``gpu`` names a GPU
        model and optionally a count, such as ``"a10g"`` or ``"l4:2"``, and the sandbox runs on a host launched
        for sandboxes that ask for the same; the first such sandbox waits for that host. Every other option
        means what it means to ``SandboxClient.create``, which also documents the entrypoint. Outside a run the
        CLI's default profile and selected project are used; ``SandboxPlatform.for_client`` names another
        client. The first sandbox of a project waits minutes while the platform starts a host for it, up to
        ``wait`` seconds (15 minutes by default); later ones start in about a second.
        """
        from labqoat.sandbox.sandbox_platform import SandboxPlatform

        return SandboxPlatform.default().create(*entrypoint, image=image, **options)

    @classmethod
    async def create_async(
        cls, *entrypoint: str, image: "str | Image", **options: "Unpack[SandboxPlatformOptions]"
    ) -> "Sandbox":
        """Start a sandbox the platform places without blocking the event loop; see ``create``."""
        from labqoat.sandbox.sandbox_platform import SandboxPlatform

        return await SandboxPlatform.default().create_async(*entrypoint, image=image, **options)

    @classmethod
    def from_id(cls, sandbox_id: str) -> "Sandbox":
        """Return a handle on a sandbox the platform placed, from any process that acts in its project.

        Nothing is asked until the handle is used; a sandbox that is gone raises ``SandboxNotFoundError`` then.
        """
        from labqoat.sandbox.sandbox_platform import SandboxPlatform

        return SandboxPlatform.default().from_id(sandbox_id)

    @classmethod
    def from_name(cls, name: str) -> "Sandbox":
        """Return the project's sandbox the platform placed under ``name``, from any process in the project."""
        from labqoat.sandbox.sandbox_platform import SandboxPlatform

        return SandboxPlatform.default().from_name(name)

    @classmethod
    def list(cls, tags: "Mapping[str, str] | None" = None) -> "tuple[Sandbox, ...]":
        """Return the project's platform sandboxes, only those carrying every one of ``tags`` when given."""
        from labqoat.sandbox.sandbox_platform import SandboxPlatform

        return SandboxPlatform.default().list(tags)

    def __init__(self, sandbox_id: str, transport: SandboxTransport) -> None:
        """Bind the sandbox's identifier and the host that has it, without contacting the host."""
        super().__init__(sandbox_id, transport)
        self._state: SandboxState | None = None
        self._detached = False
        streams = ("stdout", "stderr")
        self._main = SandboxProcess(transport, f"{self._path}/processes/main", "main", self._text, streams, True)

    @property
    def stdin(self) -> SandboxStreamWriter:
        """Write the entrypoint's standard input."""
        return self._main.stdin

    @property
    def stdout(self) -> SandboxStreamReader[str]:
        """Read the entrypoint's standard output as it is written."""
        return self._main.stdout

    @property
    def stderr(self) -> SandboxStreamReader[str]:
        """Read the entrypoint's standard error as it is written."""
        return self._main.stderr

    @property
    def returncode(self) -> int | None:
        """Return the exit code once the sandbox is known here to have finished, without asking the host."""
        return None if self._state is None else self._state.exit_code

    def wait(self) -> int:
        """Return the exit code once the sandbox has finished."""
        state = self._state
        while state is None or state.exit_code is None:
            state = self._observed(self.transport.send(self._state_request("finished", self.WAIT_SECONDS)))
        return state.exit_code

    async def wait_async(self) -> int:
        """Wait for the sandbox to finish without blocking the event loop; see ``wait``."""
        state = self._state
        while state is None or state.exit_code is None:
            state = self._observed(await self.transport.send_async(self._state_request("finished", self.WAIT_SECONDS)))
        return state.exit_code

    def poll(self) -> int | None:
        """Return the exit code if the sandbox has finished, and ``None`` while it runs."""
        if self.returncode is None:
            self._observed(self.transport.send(self._state_request(None, 0)))
        return self.returncode

    async def poll_async(self) -> int | None:
        """Ask whether the sandbox finished without blocking the event loop; see ``poll``."""
        if self.returncode is None:
            self._observed(await self.transport.send_async(self._state_request(None, 0)))
        return self.returncode

    def wait_until_ready(self, timeout: float = 300.0) -> None:
        """Return once the sandbox's readiness probe has passed.

        Raises ``SandboxTimeoutError`` when it has not passed within ``timeout`` seconds, and ``SandboxError``
        when the sandbox finished before it did.
        """
        deadline = monotonic() + timeout
        while not self._ready(deadline, timeout):
            self._observed(self.transport.send(self._state_request("ready", self._patience(deadline))))

    async def wait_until_ready_async(self, timeout: float = 300.0) -> None:
        """Wait for readiness without blocking the event loop; see ``wait_until_ready``."""
        deadline = monotonic() + timeout
        while not self._ready(deadline, timeout):
            self._observed(await self.transport.send_async(self._state_request("ready", self._patience(deadline))))

    def set_tags(self, tags: Mapping[str, str]) -> None:
        """Replace the sandbox's tags, which ``SandboxClient.list`` filters by."""
        self.transport.send(self._tags_request(tags))

    async def set_tags_async(self, tags: Mapping[str, str]) -> None:
        """Replace the tags without blocking the event loop; see ``set_tags``."""
        await self.transport.send_async(self._tags_request(tags))

    def get_tags(self) -> dict[str, str]:
        """Return the sandbox's tags."""
        return self._observed(self.transport.send(self._state_request(None, 0))).tags

    async def get_tags_async(self) -> dict[str, str]:
        """Read the tags without blocking the event loop; see ``get_tags``."""
        return self._observed(await self.transport.send_async(self._state_request(None, 0))).tags

    def tunnel(self, port: int) -> SandboxTunnel:
        """Reach ``port`` inside the sandbox at a local address, ``tunnel.url``; see ``SandboxTunnel``.

        The sandbox needs ``ports=[...]`` at creation, and only the worker hosting it can open a tunnel.
        """
        socket_path = self.transport.socket_path
        if socket_path is None:
            raise SandboxUnavailableError("Only the worker that hosts a sandbox reaches its ports")
        return SandboxTunnel(socket_path, f"{self._path}/ports/{port}", port)

    def terminate(self) -> None:
        """End the sandbox and return its share of the host budget; one already gone counts as terminated."""
        with contextlib.suppress(SandboxNotFoundError):
            self.transport.send(SandboxRequest("DELETE", self._path))

    async def terminate_async(self) -> None:
        """End the sandbox without blocking the event loop; see ``terminate``."""
        with contextlib.suppress(SandboxNotFoundError):
            await self.transport.send_async(SandboxRequest("DELETE", self._path))

    def detach(self) -> None:
        """Leave the sandbox running when its ``with`` block ends; its lifetime limits still apply."""
        self._detached = True

    def __enter__(self) -> "Sandbox":
        """Use the sandbox for the length of a block."""
        return self

    def __exit__(self, *_failure: object) -> None:
        """Terminate the sandbox when the block ends, however it ends, unless it was detached."""
        if not self._detached:
            self.terminate()

    async def __aenter__(self) -> "Sandbox":
        """Use the sandbox for the length of an asynchronous block."""
        return self

    async def __aexit__(self, *_failure: object) -> None:
        """Terminate the sandbox when the asynchronous block ends, however it ends, unless it was detached."""
        if not self._detached:
            await self.terminate_async()

    def _state_request(self, until: str | None, wait: float) -> SandboxRequest:
        """Ask for the sandbox's state, letting the host hold the answer up to ``wait`` seconds for ``until``."""
        query = {"until": until, "wait_ms": str(round(wait * 1000))} if until else {}
        return SandboxRequest("GET", self._path, query, timeout=wait + self.ANSWER_SECONDS)

    def _tags_request(self, tags: Mapping[str, str]) -> SandboxRequest:
        """Replace every tag with the given ones."""
        return SandboxRequest("PUT", f"{self._path}/tags", document={"tags": dict(tags)})

    def _observed(self, content: bytes) -> SandboxState:
        """Read and keep the state the host reported."""
        self._state = SandboxResponse.decoded(content, SandboxState.decode)
        return self._state

    def _ready(self, deadline: float, timeout: float) -> bool:
        """Report readiness from the last state seen, raising when it can no longer come in time."""
        state = self._state
        if state is not None and state.ready:
            return True
        if state is not None and state.exit_code is not None:
            raise SandboxError(f"Sandbox {self.id} finished ({state.reason}) before it was ready")
        if state is not None and monotonic() >= deadline:
            raise SandboxTimeoutError(f"Sandbox {self.id} was not ready within {timeout:g} s")
        return False

    def _patience(self, deadline: float) -> float:
        """Hold the next question for readiness until the deadline, at most a minute."""
        return max(0.0, min(self.WAIT_SECONDS, deadline - monotonic()))
