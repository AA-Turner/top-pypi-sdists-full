"""A process running in a sandbox, with its standard streams."""

import contextlib
from collections.abc import Callable
from typing import AnyStr, ClassVar, Generic

from labqoat.sandbox.sandbox_not_found_error import SandboxNotFoundError
from labqoat.sandbox.sandbox_process_state import SandboxProcessState
from labqoat.sandbox.sandbox_request import SandboxRequest
from labqoat.sandbox.sandbox_response import SandboxResponse
from labqoat.sandbox.sandbox_stream_reader import SandboxStreamReader
from labqoat.sandbox.sandbox_stream_writer import SandboxStreamWriter
from labqoat.sandbox.sandbox_timeout_error import SandboxTimeoutError
from labqoat.sandbox.sandbox_transport import SandboxTransport


class SandboxProcess(Generic[AnyStr]):
    """Write to ``stdin``, read ``stdout`` and ``stderr`` as the process writes them, and wait for its exit code.

    The process runs on its own once started: nothing here has to be read or awaited for it to finish. Its
    output stays readable for about ten minutes after it exits. An exit code is a result whatever its value;
    a process the host killed for running past its ``timeout`` raises ``SandboxTimeoutError`` from ``wait``.
    Reading a stream to its end also learns the exit code, so ``wait`` afterwards asks the host nothing.
    """

    WAIT_SECONDS: ClassVar[float] = 60.0
    ANSWER_SECONDS: ClassVar[float] = 30.0

    def __init__(
        self,
        transport: SandboxTransport,
        path: str,
        process_id: str,
        decode: Callable[[bytes], AnyStr],
        streams: tuple[str | None, str | None],
        piped: bool,
    ) -> None:
        """Bind the process's path on its host, how its output becomes values, which outputs it keeps, and its input."""
        self.id = process_id
        self._transport = transport
        self._path = path
        self._state: SandboxProcessState | None = None
        self.stdin = SandboxStreamWriter(transport, f"{path}/stdin", piped)
        output = f"{path}/output"
        self.stdout: SandboxStreamReader[AnyStr] = SandboxStreamReader(
            transport, output, streams[0], decode, self._observe
        )
        self.stderr: SandboxStreamReader[AnyStr] = SandboxStreamReader(
            transport, output, streams[1], decode, self._observe
        )

    @property
    def returncode(self) -> int | None:
        """Return the exit code once it is known here, without asking the host."""
        return None if self._state is None else self._state.exit_code

    def wait(self) -> int:
        """Return the exit code once the process has exited."""
        state = self._state
        while state is None or state.exit_code is None:
            state = self._observed(self._transport.send(self._state_request(self.WAIT_SECONDS)))
        return self._returned(state.exit_code, state.timed_out)

    async def wait_async(self) -> int:
        """Wait for the exit code without blocking the event loop; see ``wait``."""
        state = self._state
        while state is None or state.exit_code is None:
            state = self._observed(await self._transport.send_async(self._state_request(self.WAIT_SECONDS)))
        return self._returned(state.exit_code, state.timed_out)

    def poll(self) -> int | None:
        """Return the exit code if the process has exited, and ``None`` while it runs."""
        if self._state is None or self._state.running:
            self._observed(self._transport.send(self._state_request(0)))
        return self.returncode

    async def poll_async(self) -> int | None:
        """Ask whether the process has exited without blocking the event loop; see ``poll``."""
        if self._state is None or self._state.running:
            self._observed(await self._transport.send_async(self._state_request(0)))
        return self.returncode

    def kill(self) -> None:
        """Kill the process and everything it started; one that already ended is left as it is."""
        with contextlib.suppress(SandboxNotFoundError):
            self._transport.send(SandboxRequest("DELETE", self._path))

    async def kill_async(self) -> None:
        """Kill the process without blocking the event loop; see ``kill``."""
        with contextlib.suppress(SandboxNotFoundError):
            await self._transport.send_async(SandboxRequest("DELETE", self._path))

    def _state_request(self, wait: float) -> SandboxRequest:
        """Ask for the process's state, letting the host hold the answer up to ``wait`` seconds for its exit."""
        query = {"wait_ms": str(round(wait * 1000))} if wait else {}
        return SandboxRequest("GET", self._path, query, timeout=wait + self.ANSWER_SECONDS)

    def _observed(self, content: bytes) -> SandboxProcessState:
        """Read and keep the state the host reported."""
        state = SandboxResponse.decoded(content, SandboxProcessState.decode)
        self._observe(state)
        return state

    def _observe(self, state: SandboxProcessState) -> None:
        """Keep a state learned here or by a stream that read to the process's end."""
        self._state = state

    def _returned(self, exit_code: int, timed_out: bool) -> int:
        """Return an exit code, or raise when the process was killed for its timeout."""
        if timed_out:
            raise SandboxTimeoutError(f"Sandbox process {self.id} ran past its timeout and was killed")
        return exit_code
