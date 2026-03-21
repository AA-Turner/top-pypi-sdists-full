"""Tests for checkpoint context manager with file triggers."""

from __future__ import annotations

import asyncio

import pytest

from plato.worlds.checkpoint import (
    CheckpointTriggerEvent,
    CheckpointTriggerServer,
    FileCheckpointTrigger,
    checkpoint,
)


@pytest.mark.asyncio
async def test_periodic_checkpoint():
    """Basic periodic checkpoint still works."""
    calls: list[str] = []

    async def fn(label: str, **kwargs: object) -> None:
        calls.append(label)

    async with checkpoint(fn, "test", step=1, interval_s=0):
        pass

    assert calls == ["step.1.stage.test"]


@pytest.mark.asyncio
async def test_periodic_checkpoint_with_interval():
    """Periodic background checkpoints fire on interval."""
    calls: list[str] = []

    async def fn(label: str, **kwargs: object) -> None:
        calls.append(label)

    async with checkpoint(fn, "test", step=1, interval_s=1):
        await asyncio.sleep(0.1)

    # Final checkpoint always fires
    assert "step.1.stage.test" in calls


@pytest.mark.asyncio
async def test_trigger_server_start_stop():
    """Server starts and stops cleanly."""
    server = CheckpointTriggerServer()
    await server.start()
    assert server.port > 0
    await server.stop()


@pytest.mark.asyncio
async def test_trigger_server_idempotent():
    """Calling start() twice doesn't create a second server."""
    server = CheckpointTriggerServer()
    await server.start()
    port1 = server.port
    await server.start()
    assert server.port == port1
    await server.stop()


@pytest.mark.asyncio
async def test_trigger_server_receives_event():
    """Events pushed over TCP are received by the server."""
    server = CheckpointTriggerServer()
    await server.start()

    # Connect and send event
    reader, writer = await asyncio.open_connection("127.0.0.1", server.port)
    event = CheckpointTriggerEvent(
        path="/workspace/code/progress.json",
        pattern="**/progress.json",
        span_id="abc123",
        trace_id="def456",
        tool_name="Write",
    )
    writer.write(event.model_dump_json().encode() + b"\n")
    await writer.drain()

    received = await asyncio.wait_for(server.wait(), timeout=2.0)
    assert received.path == "/workspace/code/progress.json"
    assert received.span_id == "abc123"
    assert received.pattern == "**/progress.json"

    writer.close()
    await server.stop()


@pytest.mark.asyncio
async def test_file_trigger_checkpoint():
    """File trigger events cause checkpoint with trigger_span_id."""
    calls: list[tuple[str, str]] = []

    async def fn(label: str, *, trigger_span_id: str = "") -> None:
        calls.append((label, trigger_span_id))

    server = CheckpointTriggerServer()
    await server.start()

    async def send_trigger():
        await asyncio.sleep(0.1)
        reader, writer = await asyncio.open_connection("127.0.0.1", server.port)
        event = CheckpointTriggerEvent(
            path="/workspace/code/progress.json",
            pattern="**/progress.json",
            span_id="span123",
        )
        writer.write(event.model_dump_json().encode() + b"\n")
        await writer.drain()
        writer.close()

    async with checkpoint(
        fn,
        "improve",
        step=1,
        file_triggers=[FileCheckpointTrigger(pattern="**/progress.json", debounce_s=0.1)],
        trigger_server=server,
    ):
        await send_trigger()
        # Wait for debounce + processing
        await asyncio.sleep(0.5)

    # Should have file trigger checkpoint + final checkpoint
    assert len(calls) >= 2
    file_calls = [(label, span) for label, span in calls if ".file." in label]
    assert len(file_calls) == 1
    assert file_calls[0][1] == "span123"
    # Final checkpoint
    assert calls[-1][0] == "step.1.stage.improve"

    await server.stop()


@pytest.mark.asyncio
async def test_unmatched_pattern_ignored():
    """Events with unmatched patterns don't trigger checkpoints."""
    calls: list[str] = []

    async def fn(label: str, **kwargs: object) -> None:
        calls.append(label)

    server = CheckpointTriggerServer()
    await server.start()

    async def send_unmatched():
        await asyncio.sleep(0.1)
        reader, writer = await asyncio.open_connection("127.0.0.1", server.port)
        event = CheckpointTriggerEvent(
            path="/workspace/code/other.txt",
            pattern="**/other.txt",
            span_id="span999",
        )
        writer.write(event.model_dump_json().encode() + b"\n")
        await writer.drain()
        writer.close()

    async with checkpoint(
        fn,
        "test",
        step=1,
        file_triggers=[FileCheckpointTrigger(pattern="**/progress.json")],
        trigger_server=server,
    ):
        await send_unmatched()
        await asyncio.sleep(0.5)

    # Only the final checkpoint, no file trigger checkpoint
    assert calls == ["step.1.stage.test"]

    await server.stop()
