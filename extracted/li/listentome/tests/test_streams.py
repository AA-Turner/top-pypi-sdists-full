from __future__ import annotations

import anyio
import pytest

import listentome as ltm
from tests.fake_backend import FakeBackend

pytestmark = pytest.mark.anyio


def test_devices(backend: FakeBackend) -> None:
    names = [d.name for d in ltm.devices(backend=backend)]
    assert names == ["Fake Mic", "Fake Speaker"]


def test_default_devices(backend: FakeBackend) -> None:
    default_input = ltm.default_input(backend=backend)
    default_output = ltm.default_output(backend=backend)
    assert default_input is not None and default_input.name == "Fake Mic"
    assert default_output is not None and default_output.name == "Fake Speaker"


def test_no_default_devices() -> None:
    backend = FakeBackend(device_list=[])
    assert ltm.default_input(backend=backend) is None
    assert ltm.default_output(backend=backend) is None


async def test_input_stream_iteration(backend: FakeBackend) -> None:
    async with ltm.InputStream(samplerate=48_000, channels=1, blocksize=256, backend=backend) as stream:
        blocks = []
        async for block in stream:
            blocks.append(block)
            if len(blocks) == 3:
                break
    assert all(len(b) == stream.blockbytes for b in blocks)
    assert backend.streams[0].closed


async def test_input_stream_overflow_drop(backend: FakeBackend) -> None:
    async with ltm.InputStream(
        samplerate=48_000, channels=1, backend=backend, max_buffered_blocks=1, on_overflow="drop"
    ) as stream:
        await anyio.sleep(0.05)
        block = await stream.read()
    assert len(block) == stream.blockbytes


async def test_input_stream_overflow_raise(backend: FakeBackend) -> None:
    async with ltm.InputStream(
        samplerate=48_000, channels=1, backend=backend, max_buffered_blocks=1, on_overflow="raise"
    ) as stream:
        await anyio.sleep(0.05)
        with pytest.raises(ltm.Overflow):
            await stream.read()
        block = await stream.read()
    assert len(block) == stream.blockbytes


async def test_output_stream_write(backend: FakeBackend) -> None:
    async with ltm.OutputStream(samplerate=48_000, channels=2, dtype="int16", blocksize=128, backend=backend) as stream:
        payload = bytes(range(256)) * 4
        await stream.write(payload)
    assert payload in bytes(backend.streams[0].written)


async def test_duplex_stream(backend: FakeBackend) -> None:
    async with ltm.DuplexStream(samplerate=48_000, channels=1, blocksize=64, backend=backend) as stream:
        block = await stream.read()
        await stream.write(block)
        await stream.drain()
        async for extra in stream:
            break
    assert len(block) == stream.blockbytes
    assert len(extra) == stream.blockbytes


async def test_duplex_stream_read_waits() -> None:
    backend = FakeBackend(interval=0.02)
    async with ltm.DuplexStream(samplerate=48_000, channels=1, blocksize=64, backend=backend) as stream:
        first = await stream.read()
        block = await stream.read()
    assert len(first) == stream.blockbytes
    assert len(block) == stream.blockbytes


async def test_duplex_stream_overflow(backend: FakeBackend) -> None:
    async with ltm.DuplexStream(
        samplerate=48_000, channels=1, backend=backend, max_buffered_blocks=1, on_overflow="raise"
    ) as stream:
        await anyio.sleep(0.05)
        with pytest.raises(ltm.Overflow):
            await stream.read()


async def test_stream_closed_outside_context(backend: FakeBackend) -> None:
    stream = ltm.InputStream(samplerate=48_000, channels=1, backend=backend)
    with pytest.raises(ltm.StreamClosed):
        await stream.read()
    out = ltm.OutputStream(samplerate=48_000, channels=1, backend=backend)
    with pytest.raises(ltm.StreamClosed):
        await out.write(b"\x00")


async def test_aexit_without_open(backend: FakeBackend) -> None:
    stream = ltm.InputStream(samplerate=48_000, channels=1, backend=backend)
    await stream.__aexit__(None, None, None)


def test_invalid_parameters(backend: FakeBackend) -> None:
    with pytest.raises(ValueError):
        ltm.InputStream(samplerate=0, channels=1, backend=backend)
    with pytest.raises(ValueError):
        ltm.InputStream(samplerate=48_000, channels=0, backend=backend)
    with pytest.raises(ValueError):
        ltm.InputStream(samplerate=48_000, channels=1, blocksize=0, backend=backend)
    with pytest.raises(ValueError):
        ltm.InputStream(samplerate=48_000, channels=1, max_buffered_blocks=0, backend=backend)


def test_duplex_invalid_max_buffered_blocks(backend: FakeBackend) -> None:
    with pytest.raises(ValueError):
        ltm.DuplexStream(samplerate=48_000, channels=1, max_buffered_blocks=-1, backend=backend)
