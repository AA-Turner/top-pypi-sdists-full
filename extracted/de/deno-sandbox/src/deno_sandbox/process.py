from __future__ import annotations

import asyncio
import sys
from typing import Any, BinaryIO, Callable, Optional, TypedDict, TypeVar, cast
from typing_extensions import Literal

from .bridge import AsyncBridge
from .errors import ProcessAlreadyExited
from .rpc import (
    AsyncFetchResponse,
    AsyncRpcClient,
    FetchResponse,
)

T = TypeVar("T")


class AbortSignal:
    pass


class RemoteProcessOptions(TypedDict):
    stdout_inherit: bool
    stderr_inherit: bool


class ProcessSpawnResult(TypedDict):
    pid: int
    stdout_stream_id: int
    stderr_stream_id: int


class ProcessWaitResult(TypedDict):
    success: bool
    code: int
    signal: AbortSignal | None


class ChildProcessStatus(TypedDict):
    """Whether the subprocess exited successfully, i.e. with a zero exit code."""

    success: bool
    """The exit code of the subprocess. Negative values indicate that the process was killed by a signal."""
    code: int
    """The signal that caused the process to exit, if any. If the process exited normally, this will be `null`."""
    signal: AbortSignal | None


class AsyncChildProcess:
    def __init__(
        self,
        pid: int,
        stdout: asyncio.StreamReader,
        stderr: asyncio.StreamReader,
        wait_task: asyncio.Task,
        rpc: AsyncRpcClient,
        _stdout_task: Optional[asyncio.Task] = None,
        _stderr_task: Optional[asyncio.Task] = None,
        _process_list: Optional[list["AsyncChildProcess"]] = None,
    ):
        self.pid = pid
        self.stdout = stdout
        self.stderr = stderr
        self._wait_task = wait_task
        self.returncode = None
        self._rpc = rpc
        self._stdout_task = _stdout_task
        self._stderr_task = _stderr_task
        self._process_list = _process_list

    def _remove_from_list(self) -> None:
        """Remove this process from the tracking list."""
        if self._process_list is not None and self in self._process_list:
            self._process_list.remove(self)

    @classmethod
    async def create(
        cls: type["AsyncChildProcess"],
        res: ProcessSpawnResult,
        rpc: AsyncRpcClient,
        options: RemoteProcessOptions,
        process_list: Optional[list[AsyncChildProcess]] = None,
    ) -> AsyncChildProcess:
        return create_process_like(cls, res, rpc, options, process_list)

    async def wait(self) -> ChildProcessStatus:
        raw = await self._wait_task
        result = cast(ProcessWaitResult, raw)
        self._remove_from_list()
        return ChildProcessStatus(
            success=result["success"], code=result["code"], signal=result["signal"]
        )

    async def kill(self) -> None:
        """Kill the process and cancel all associated tasks."""

        try:
            await self._rpc.call("processKill", {"pid": self.pid})
        except ProcessAlreadyExited:
            # Process already exited
            pass

        # Cancel all associated tasks
        self._wait_task.cancel()
        if self._stdout_task is not None:
            self._stdout_task.cancel()
        if self._stderr_task is not None:
            self._stderr_task.cancel()

        self._remove_from_list()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.kill()


async def _pipe_stream(reader: asyncio.StreamReader, writer: BinaryIO):
    """Helper to pump data from the StreamReader to a local binary stream."""
    try:
        while not reader.at_eof():
            data = await reader.read(1024)
            if not data:
                break

            writer.write(data)
            writer.flush()
    except Exception:
        # Handle potential connection drops or closed pipes silently
        pass


def create_process_like(
    cls: Callable[
        [
            int,
            asyncio.StreamReader,
            asyncio.StreamReader,
            asyncio.Task,
            AsyncRpcClient,
            Optional[asyncio.Task],
            Optional[asyncio.Task],
            Optional[list[AsyncChildProcess]],
        ],
        T,
    ],
    res: ProcessSpawnResult,
    rpc: AsyncRpcClient,
    options: RemoteProcessOptions,
    process_list: Optional[list[AsyncChildProcess]] = None,
) -> T:
    pid = res["pid"]

    stdout = asyncio.StreamReader()
    stderr = asyncio.StreamReader()

    rpc._pending_processes[res["stdout_stream_id"]] = stdout
    rpc._pending_processes[res["stderr_stream_id"]] = stderr

    wait_task = rpc._loop.create_task(rpc.call("processWait", {"pid": pid}))

    stdout_task: Optional[asyncio.Task] = None
    stderr_task: Optional[asyncio.Task] = None

    if options.get("stdout_inherit"):
        stdout_coro = _pipe_stream(stdout, sys.stdout.buffer)
        stdout_task = rpc._loop.create_task(stdout_coro)
    if options.get("stderr_inherit"):
        stderr_coro = _pipe_stream(stderr, sys.stderr.buffer)
        stderr_task = rpc._loop.create_task(stderr_coro)

    instance = cls(
        pid, stdout, stderr, wait_task, rpc, stdout_task, stderr_task, process_list
    )

    return instance


class SyncStreamReader:
    """Wraps asyncio.StreamReader to provide synchronous read methods."""

    def __init__(self, bridge: AsyncBridge, reader: asyncio.StreamReader):
        self._bridge = bridge
        self._reader = reader

    def read(self, n: int = -1) -> bytes:
        return self._bridge.run(self._reader.read(n))

    def readline(self) -> bytes:
        return self._bridge.run(self._reader.readline())

    def readexactly(self, n: int) -> bytes:
        return self._bridge.run(self._reader.readexactly(n))


class ChildProcess:
    def __init__(
        self,
        rpc: AsyncRpcClient,
        bridge: AsyncBridge,
        async_proc: AsyncChildProcess,
    ):
        self._rpc = rpc
        self._bridge = bridge

        self._async_proc = async_proc
        self.stdout = SyncStreamReader(bridge, self._async_proc.stdout)
        self.stderr = SyncStreamReader(bridge, self._async_proc.stderr)
        self.returncode: int | None = None

    @property
    def pid(self) -> int:
        return self._async_proc.pid

    def wait(self) -> ChildProcessStatus:
        return self._bridge.run(self._async_proc.wait())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._bridge.run(self._async_proc.__aexit__(exc_type, exc_val, exc_tb))


class AsyncDenoProcess(AsyncChildProcess):
    def __init__(
        self,
        pid: int,
        stdout: asyncio.StreamReader,
        stderr: asyncio.StreamReader,
        wait_task: asyncio.Task,
        rpc: AsyncRpcClient,
        stdout_task: Optional[asyncio.Task],
        stderr_task: Optional[asyncio.Task],
        process_list: Optional[list[AsyncChildProcess]] = None,
    ):
        super().__init__(
            pid, stdout, stderr, wait_task, rpc, stdout_task, stderr_task, process_list
        )
        self._listening_task: asyncio.Task | None = None

    @classmethod
    async def create(
        cls: type["AsyncDenoProcess"],
        res: ProcessSpawnResult,
        rpc: AsyncRpcClient,
        options: RemoteProcessOptions,
        process_list: Optional[list[AsyncChildProcess]] = None,
    ) -> AsyncDenoProcess:
        p = create_process_like(cls, res, rpc, options, process_list)

        p._listening_task = rpc._loop.create_task(
            rpc.call("denoHttpWait", {"pid": p.pid})
        )
        return p

    async def kill(self) -> None:
        """Kill the process and cancel all associated tasks."""
        if self._listening_task is not None:
            self._listening_task.cancel()
        await super().kill()

    async def wait_http_ready(self) -> bool:
        """Whether the Deno process is ready to accept HTTP requests."""

        if self._listening_task is not None:
            return await self._listening_task

        return False

    async def fetch(
        self,
        url: str,
        method: Optional[str] = "GET",
        headers: Optional[dict[str, str]] = None,
        redirect: Optional[Literal["follow", "manual"]] = None,
    ) -> AsyncFetchResponse:
        """Fetch a URL from the Deno process."""
        return await self._rpc.fetch(url, method, headers, redirect, self.pid)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._listening_task is not None:
            self._listening_task.cancel()
        await super().__aexit__(exc_type, exc_val, exc_tb)


class DenoProcess(ChildProcess):
    def __init__(
        self,
        rpc: AsyncRpcClient,
        bridge: AsyncBridge,
        async_proc: AsyncDenoProcess,
    ):
        super().__init__(rpc, bridge, async_proc)
        self._async = async_proc

    def wait_http_ready(self) -> bool:
        """Whether the Deno process is ready to accept HTTP requests."""
        return self._bridge.run(self._async.wait_http_ready())

    def fetch(
        self,
        url: str,
        method: Optional[str] = "GET",
        headers: Optional[dict[str, str]] = None,
        redirect: Optional[Literal["follow", "manual"]] = None,
    ) -> FetchResponse:
        """Fetch a URL from the Deno process."""
        async_response = self._bridge.run(
            self._rpc.fetch(url, method, headers, redirect, self.pid)
        )
        return FetchResponse(async_response)


class AsyncDenoRepl(AsyncChildProcess):
    @classmethod
    async def create(
        cls: type["AsyncDenoRepl"],
        res: ProcessSpawnResult,
        rpc: AsyncRpcClient,
        options: RemoteProcessOptions,
        process_list: Optional[list[AsyncChildProcess]] = None,
    ) -> AsyncDenoRepl:
        return create_process_like(cls, res, rpc, options, process_list)

    async def eval(self, code: str) -> str:
        """Evaluate code in the REPL and return the output."""

        result = await self._rpc.call("denoReplEval", {"code": code, "pid": self.pid})

        return result

    async def call(self, fn: str, args: list[Any]) -> Any:
        """Call a function in the REPL process."""

        result = await self._rpc.call(
            "denoReplCall", {"pid": self.pid, "fn": fn, "args": args}
        )

        return result

    async def close(self) -> None:
        """Close the REPL process."""

        await self._rpc.call("denoReplClose", {"pid": self.pid})
        self._wait_task.cancel()
        if self._stdout_task is not None:
            self._stdout_task.cancel()
        if self._stderr_task is not None:
            self._stderr_task.cancel()
        self._remove_from_list()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class DenoRepl:
    def __init__(
        self,
        rpc: AsyncRpcClient,
        bridge: AsyncBridge,
        async_proc: AsyncDenoRepl,
    ):
        self._rpc = rpc
        self._bridge = bridge

        self._async = async_proc
        self.stdout = SyncStreamReader(bridge, self._async.stdout)
        self.stderr = SyncStreamReader(bridge, self._async.stderr)

    def eval(self, code: str) -> str:
        """Evaluate code in the REPL and return the output."""
        return self._bridge.run(self._async.eval(code))

    def call(self, fn: str, args: list[Any]) -> Any:
        """Call a function in the REPL process."""
        return self._bridge.run(self._async.call(fn, args))

    def close(self) -> None:
        """Close the REPL process."""
        self._bridge.run(self._async.close())

    @property
    def returncode(self) -> int | None:
        return self._async.returncode

    @property
    def pid(self) -> int:
        return self._async.pid

    def wait(self) -> ChildProcessStatus:
        return self._bridge.run(self._async.wait())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._bridge.run(self._async.__aexit__(exc_type, exc_val, exc_tb))
