from __future__ import annotations

from collections import deque
from types import TracebackType
from typing import TYPE_CHECKING, Literal, TypeAlias

import anyio
from anyio.from_thread import BlockingPortal, start_blocking_portal

from ._backend import ITEMSIZE, Backend, DType, RawStream
from ._exceptions import Overflow, StreamClosed

if TYPE_CHECKING:
    from typing_extensions import Self

OnOverflow: TypeAlias = Literal["drop", "raise"]


class _StreamBase:
    def __init__(
        self,
        *,
        samplerate: int,
        channels: int,
        dtype: DType,
        blocksize: int,
        device: int | None,
        backend: Backend | None,
    ) -> None:
        if samplerate <= 0:
            raise ValueError(f"samplerate must be positive, got {samplerate}")
        if channels <= 0:
            raise ValueError(f"channels must be positive, got {channels}")
        if blocksize <= 0:
            raise ValueError(f"blocksize must be positive, got {blocksize}")
        self.samplerate = samplerate
        self.channels = channels
        self.dtype: DType = dtype
        self.blocksize = blocksize
        self.device = device
        self._backend = backend
        self._raw: RawStream | None = None
        self._portal: BlockingPortal | None = None
        self._wakeup = anyio.Event()

    @property
    def blockbytes(self) -> int:
        return self.blocksize * self.channels * ITEMSIZE[self.dtype]

    def _resolved_backend(self) -> Backend:
        if self._backend is None:  # pragma: no cover - requires the real PortAudio library and audio hardware
            from ._portaudio import default_backend

            self._backend = default_backend()
        return self._backend

    def _raw_stream(self) -> RawStream:
        if self._raw is None:
            raise StreamClosed("stream is not open; use it inside `async with`")
        return self._raw

    def _callback(self, indata: memoryview | None, outdata: memoryview | None, frames: int) -> None:
        raise NotImplementedError

    def _wake(self) -> None:
        portal = self._portal
        if portal is not None:
            try:
                portal.start_task_soon(self._set_wakeup)
            except RuntimeError:  # pragma: no cover - portal already shut down during close
                pass

    async def _set_wakeup(self) -> None:
        self._wakeup.set()

    async def _wait_wakeup(self) -> None:
        self._wakeup = anyio.Event()
        await self._wakeup.wait()

    async def _open(self, *, input_channels: int, output_channels: int) -> None:
        portal = BlockingPortal()
        await portal.__aenter__()
        self._portal = portal
        raw = self._resolved_backend().open(
            samplerate=self.samplerate,
            blocksize=self.blocksize,
            dtype=self.dtype,
            input_channels=input_channels,
            output_channels=output_channels,
            input_device=self.device if input_channels else None,
            output_device=self.device if output_channels else None,
            callback=self._callback,
        )
        await anyio.to_thread.run_sync(raw.start)
        self._raw = raw

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        raw, self._raw = self._raw, None
        if raw is not None:
            await anyio.to_thread.run_sync(raw.stop)
            await anyio.to_thread.run_sync(raw.close)
        portal, self._portal = self._portal, None
        if portal is not None:
            await portal.__aexit__(None, None, None)


class InputStream(_StreamBase):
    """Capture audio and iterate over blocks of raw bytes.

    ```python
    async with InputStream(samplerate=48_000, channels=1) as stream:
        async for block in stream:
            process(block)
    ```
    """

    def __init__(
        self,
        *,
        samplerate: int,
        channels: int,
        dtype: DType = "float32",
        blocksize: int = 1024,
        device: int | None = None,
        max_buffered_blocks: int = 64,
        on_overflow: OnOverflow = "drop",
        backend: Backend | None = None,
    ) -> None:
        super().__init__(
            samplerate=samplerate, channels=channels, dtype=dtype, blocksize=blocksize, device=device, backend=backend
        )
        if max_buffered_blocks <= 0:
            raise ValueError(f"max_buffered_blocks must be positive, got {max_buffered_blocks}")
        self.on_overflow: OnOverflow = on_overflow
        self._blocks: deque[bytes] = deque(maxlen=max_buffered_blocks)
        self._overflowed = False

    def _callback(self, indata: memoryview | None, outdata: memoryview | None, frames: int) -> None:
        assert indata is not None
        if len(self._blocks) == self._blocks.maxlen:
            self._overflowed = True
        self._blocks.append(bytes(indata))
        self._wake()

    async def __aenter__(self) -> Self:
        await self._open(input_channels=self.channels, output_channels=0)
        return self

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> bytes:
        return await self.read()

    async def read(self) -> bytes:
        self._raw_stream()
        while not self._blocks:
            await self._wait_wakeup()
        if self._overflowed:
            self._overflowed = False
            if self.on_overflow == "raise":
                raise Overflow("input blocks were dropped because the consumer fell behind")
        return self._blocks.popleft()


class OutputStream(_StreamBase):
    """Play audio by awaiting `write()` with blocks of raw bytes.

    ```python
    async with OutputStream(samplerate=48_000, channels=2) as stream:
        await stream.write(block)
    ```
    """

    def __init__(
        self,
        *,
        samplerate: int,
        channels: int,
        dtype: DType = "float32",
        blocksize: int = 1024,
        device: int | None = None,
        backend: Backend | None = None,
    ) -> None:
        super().__init__(
            samplerate=samplerate, channels=channels, dtype=dtype, blocksize=blocksize, device=device, backend=backend
        )
        self._pending = bytearray()

    def _callback(self, indata: memoryview | None, outdata: memoryview | None, frames: int) -> None:
        assert outdata is not None
        n = min(len(self._pending), len(outdata))
        outdata[:n] = self._pending[:n]
        del self._pending[:n]
        if n < len(outdata):
            outdata[n:] = bytes(len(outdata) - n)
        if not self._pending:
            self._wake()

    async def __aenter__(self) -> Self:
        await self._open(input_channels=0, output_channels=self.channels)
        return self

    async def write(self, data: bytes) -> None:
        self._raw_stream()
        self._pending.extend(data)
        await self.drain()

    async def drain(self) -> None:
        self._raw_stream()
        while self._pending:
            await self._wait_wakeup()


class DuplexStream(_StreamBase):
    """Capture and play simultaneously: `read()` captured blocks, `write()` playback data.

    ```python
    async with DuplexStream(samplerate=48_000, channels=1) as stream:
        block = await stream.read()
        await stream.write(block)
    ```
    """

    def __init__(
        self,
        *,
        samplerate: int,
        channels: int,
        dtype: DType = "float32",
        blocksize: int = 1024,
        device: int | None = None,
        max_buffered_blocks: int = 64,
        on_overflow: OnOverflow = "drop",
        backend: Backend | None = None,
    ) -> None:
        super().__init__(
            samplerate=samplerate, channels=channels, dtype=dtype, blocksize=blocksize, device=device, backend=backend
        )
        if max_buffered_blocks <= 0:
            raise ValueError(f"max_buffered_blocks must be positive, got {max_buffered_blocks}")
        self.on_overflow: OnOverflow = on_overflow
        self._blocks: deque[bytes] = deque(maxlen=max_buffered_blocks)
        self._overflowed = False
        self._pending = bytearray()

    def _callback(self, indata: memoryview | None, outdata: memoryview | None, frames: int) -> None:
        assert indata is not None and outdata is not None
        if len(self._blocks) == self._blocks.maxlen:
            self._overflowed = True
        self._blocks.append(bytes(indata))
        n = min(len(self._pending), len(outdata))
        outdata[:n] = self._pending[:n]
        del self._pending[:n]
        if n < len(outdata):
            outdata[n:] = bytes(len(outdata) - n)
        self._wake()

    async def __aenter__(self) -> Self:
        await self._open(input_channels=self.channels, output_channels=self.channels)
        return self

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> bytes:
        return await self.read()

    async def read(self) -> bytes:
        self._raw_stream()
        while not self._blocks:
            await self._wait_wakeup()
        if self._overflowed:
            self._overflowed = False
            if self.on_overflow == "raise":
                raise Overflow("input blocks were dropped because the consumer fell behind")
        return self._blocks.popleft()

    async def write(self, data: bytes) -> None:
        self._raw_stream()
        self._pending.extend(data)

    async def drain(self) -> None:
        self._raw_stream()
        while self._pending:
            await self._wait_wakeup()


def play(
    data: bytes, *, samplerate: int, channels: int, dtype: DType = "float32", backend: Backend | None = None
) -> None:
    """Play raw audio bytes, blocking until playback finishes."""

    async def run() -> None:
        async with OutputStream(samplerate=samplerate, channels=channels, dtype=dtype, backend=backend) as stream:
            await stream.write(data)

    with start_blocking_portal() as portal:
        portal.call(run)


def record(
    seconds: float, *, samplerate: int, channels: int, dtype: DType = "float32", backend: Backend | None = None
) -> bytes:
    """Record audio for `seconds`, blocking, and return the raw bytes."""
    target = int(seconds * samplerate) * channels * ITEMSIZE[dtype]

    async def run() -> bytes:
        chunks = bytearray()
        async with InputStream(samplerate=samplerate, channels=channels, dtype=dtype, backend=backend) as stream:
            async for block in stream:
                chunks.extend(block)
                if len(chunks) >= target:
                    break
        return bytes(chunks[:target])

    with start_blocking_portal() as portal:
        return portal.call(run)
