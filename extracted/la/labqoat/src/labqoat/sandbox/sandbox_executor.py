"""Processes started in one sandbox."""

import asyncio
import contextlib
import uuid
from collections.abc import Sequence
from typing import ClassVar, Literal, Unpack, overload
from urllib.parse import quote

from labqoat.sandbox.sandbox_command import SandboxCommand
from labqoat.sandbox.sandbox_error import SandboxError
from labqoat.sandbox.sandbox_exec_options import SandboxExecOptions
from labqoat.sandbox.sandbox_process import SandboxProcess
from labqoat.sandbox.sandbox_process_info import SandboxProcessInfo
from labqoat.sandbox.sandbox_request import SandboxRequest
from labqoat.sandbox.sandbox_response import SandboxResponse
from labqoat.sandbox.sandbox_transport import SandboxTransport
from labqoat.sandbox.stream_type import StreamType


class SandboxExecutor:
    """Start commands in one sandbox and hand back their processes; ``Sandbox`` adds files and its lifecycle."""

    TRANSFER_SECONDS: ClassVar[float] = 600.0
    ABANDON_SECONDS: ClassVar[float] = 5.0

    def __init__(self, sandbox_id: str, transport: SandboxTransport) -> None:
        """Bind the sandbox's identifier and the host that has it, without contacting the host."""
        self.id = sandbox_id
        self.transport = transport

    @overload
    def exec(
        self, *args: str, text: Literal[True] = True, **options: Unpack[SandboxExecOptions]
    ) -> SandboxProcess[str]: ...

    @overload
    def exec(
        self, *args: str, text: Literal[False], **options: Unpack[SandboxExecOptions]
    ) -> SandboxProcess[bytes]: ...

    def exec(
        self, *args: str, text: bool = True, **options: Unpack[SandboxExecOptions]
    ) -> SandboxProcess[str] | SandboxProcess[bytes]:
        """Start ``args`` as a command and return its process at once, while it runs.

        ``SandboxExecOptions`` lists the keyword arguments. Output is read as text, decoded from UTF-8, or as
        bytes with ``text=False``.
        """
        process_id = uuid.uuid4().hex
        self.transport.send(self._start_request(process_id, args, options))
        return self._process(process_id, text, options)

    @overload
    async def exec_async(
        self, *args: str, text: Literal[True] = True, **options: Unpack[SandboxExecOptions]
    ) -> SandboxProcess[str]: ...

    @overload
    async def exec_async(
        self, *args: str, text: Literal[False], **options: Unpack[SandboxExecOptions]
    ) -> SandboxProcess[bytes]: ...

    async def exec_async(
        self, *args: str, text: bool = True, **options: Unpack[SandboxExecOptions]
    ) -> SandboxProcess[str] | SandboxProcess[bytes]:
        """Start a command without blocking the event loop; see ``exec``.

        A start that is cancelled before the host answered kills the command, which may have started anyway.
        """
        process_id = uuid.uuid4().hex
        try:
            await self.transport.send_async(self._start_request(process_id, args, options))
        except asyncio.CancelledError:
            await self._abandon(process_id)
            raise
        return self._process(process_id, text, options)

    def processes(self) -> tuple[SandboxProcessInfo, ...]:
        """Return the sandbox's processes, its entrypoint and those started from anywhere, in the order they started."""
        return SandboxResponse.decoded(self.transport.send(self._processes_request()), SandboxProcessInfo.listed)

    async def processes_async(self) -> tuple[SandboxProcessInfo, ...]:
        """List the sandbox's processes without blocking the event loop; see ``processes``."""
        content = await self.transport.send_async(self._processes_request())
        return SandboxResponse.decoded(content, SandboxProcessInfo.listed)

    @overload
    def process(self, process_id: str, text: Literal[True] = True) -> SandboxProcess[str]: ...

    @overload
    def process(self, process_id: str, text: Literal[False]) -> SandboxProcess[bytes]: ...

    def process(self, process_id: str, text: bool = True) -> SandboxProcess[str] | SandboxProcess[bytes]:
        """Open a process started from anywhere, such as one ``processes`` lists, without contacting the host.

        Its output reads from the oldest the host keeps. Its stdin is best written only where it was started,
        since the host takes stdin by offset from one writer.
        """
        return self._process(process_id, text, {})

    @property
    def _path(self) -> str:
        """Address this sandbox in the host's API."""
        return f"/sandboxes/{quote(self.id, safe='')}"

    def _completed(self, argv: Sequence[str]) -> tuple[int, str]:
        """Run a command of the SDK's own to its end and return its exit code with its merged output."""
        process = self.exec(*argv, stdin=StreamType.DEVNULL, stderr=StreamType.STDOUT, timeout=self.TRANSFER_SECONDS)
        output = process.stdout.read()
        return process.wait(), output

    async def _completed_async(self, argv: Sequence[str]) -> tuple[int, str]:
        """Run a command of the SDK's own without blocking the event loop; see ``_completed``."""
        process = await self.exec_async(
            *argv, stdin=StreamType.DEVNULL, stderr=StreamType.STDOUT, timeout=self.TRANSFER_SECONDS
        )
        output = await process.stdout.read_async()
        return await process.wait_async(), output

    def _processes_request(self) -> SandboxRequest:
        """Ask the host for every process of the sandbox it keeps."""
        return SandboxRequest("GET", f"{self._path}/processes")

    def _start_request(self, process_id: str, args: Sequence[str], options: SandboxExecOptions) -> SandboxRequest:
        """Ask the host to start a process under an identifier chosen here, so it can be found again."""
        return SandboxRequest(
            "POST", f"{self._path}/processes", document=SandboxCommand.document(process_id, args, options)
        )

    def _process(
        self, process_id: str, text: bool, options: SandboxExecOptions
    ) -> SandboxProcess[str] | SandboxProcess[bytes]:
        """Hand back a started process whose output reads as text or bytes."""
        path = f"{self._path}/processes/{process_id}"
        streams, piped = SandboxCommand.streams(options), SandboxCommand.piped(options)
        if text:
            return SandboxProcess(self.transport, path, process_id, self._text, streams, piped)
        return SandboxProcess(self.transport, path, process_id, bytes, streams, piped)

    @staticmethod
    def _text(data: bytes) -> str:
        """Decode output as UTF-8, replacing bytes that are not."""
        return data.decode(errors="replace")

    async def _abandon(self, process_id: str) -> None:
        """Kill a process nobody waits for; a host that cannot must not hide the cancellation."""
        request = SandboxRequest("DELETE", f"{self._path}/processes/{process_id}", timeout=self.ABANDON_SECONDS)
        with contextlib.suppress(SandboxError):
            await self.transport.send_async(request)
