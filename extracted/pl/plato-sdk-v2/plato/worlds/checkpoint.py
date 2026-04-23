"""Async context manager for checkpointing around stage execution."""

from __future__ import annotations

import asyncio
import dataclasses
import logging
from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class FileCheckpointTrigger(BaseModel):
    """Configuration for a file-pattern checkpoint trigger.

    Specifies a glob pattern (e.g. ``"**/progress.json"``) and debounce
    window.  The actual file watching is done by a sidecar on the agent VM
    which pushes events to a :class:`CheckpointTriggerServer` on the world VM.
    """

    pattern: str
    debounce_s: float = 2.0


class CheckpointTriggerEvent(BaseModel):
    """Event received from an agent-side file watcher."""

    path: str
    pattern: str
    span_id: str = ""
    trace_id: str = ""
    tool_name: str = ""
    timestamp: str = ""


# ---------------------------------------------------------------------------
# Trigger server (world VM side)
# ---------------------------------------------------------------------------


class CheckpointTriggerServer:
    """Lightweight TCP server that receives file-trigger events from agent VMs.

    Protocol: newline-delimited JSON over a plain TCP socket.  Each line is a
    JSON-serialized :class:`CheckpointTriggerEvent`.

    Usage::

        server = CheckpointTriggerServer()
        await server.start()
        print(server.port)       # pass to agent runner
        event = await server.wait()  # blocks until next trigger
        await server.stop()
    """

    def __init__(self) -> None:
        self._server: asyncio.AbstractServer | None = None
        self._port: int = 0
        self._queue: asyncio.Queue[CheckpointTriggerEvent] = asyncio.Queue()

    @property
    def port(self) -> int:
        return self._port

    async def start(self) -> None:
        """Start listening on a random available port.  Idempotent."""
        if self._server is not None:
            return
        self._server = await asyncio.start_server(self._handle_connection, "0.0.0.0", 0)
        sock = self._server.sockets[0]
        self._port = sock.getsockname()[1]
        logger.debug("CheckpointTriggerServer listening on port %d", self._port)

    async def _handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        peer = writer.get_extra_info("peername")
        logger.debug("Trigger connection from %s", peer)
        try:
            while True:
                line = await reader.readline()
                if not line:
                    break
                try:
                    event = CheckpointTriggerEvent.model_validate_json(line)
                    logger.debug(
                        "Trigger event: path=%s pattern=%s span_id=%s",
                        event.path,
                        event.pattern,
                        event.span_id,
                    )
                    await self._queue.put(event)
                except Exception:
                    logger.warning("Failed to parse trigger event: %s", line[:200])
        except asyncio.CancelledError:
            pass
        except Exception:
            logger.debug("Trigger connection closed from %s", peer, exc_info=True)
        finally:
            writer.close()

    async def wait(self) -> CheckpointTriggerEvent:
        """Block until the next trigger event arrives."""
        return await self._queue.get()

    def try_get(self) -> CheckpointTriggerEvent | None:
        """Non-blocking: return event if available, else ``None``."""
        try:
            return self._queue.get_nowait()
        except asyncio.QueueEmpty:
            return None

    async def stop(self) -> None:
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
            self._server = None
            logger.debug("CheckpointTriggerServer stopped")


# ---------------------------------------------------------------------------
# Checkpoint context
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class CheckpointContext:
    """Yielded by :func:`checkpoint` so callers can wire up agent runners."""

    trigger_server: CheckpointTriggerServer | None = None
    file_triggers: list[FileCheckpointTrigger] = dataclasses.field(default_factory=list)

    @property
    def trigger_url(self) -> str | None:
        """URL for the trigger server (``runtime.plato.internal:{port}``)."""
        if self.trigger_server is None:
            return None
        return f"runtime.plato.internal:{self.trigger_server.port}"

    @property
    def trigger_patterns(self) -> list[str]:
        """Glob patterns extracted from :attr:`file_triggers`."""
        return [t.pattern for t in self.file_triggers]


# ---------------------------------------------------------------------------
# Checkpoint context manager
# ---------------------------------------------------------------------------


@asynccontextmanager
async def checkpoint(
    fn: Callable[..., Awaitable[Any]],
    name: str,
    *,
    step: int = 0,
    interval_s: int = 0,
    file_triggers: list[FileCheckpointTrigger] | None = None,
):
    """Checkpoint world state after the wrapped block completes.

    Usage::

        async with checkpoint(world.checkpoint, "annotate", step=2, interval_s=300):
            await annotate(...)

        # With file triggers:
        async with checkpoint(
            world.checkpoint, "improve", step=1, interval_s=300,
            file_triggers=[FileCheckpointTrigger(pattern="**/progress.json")],
        ) as ctx:
            agent_runner.with_file_triggers_from(ctx)
            await agent_runner.run(instruction)

    Args:
        fn: Async checkpoint function (e.g. ``world.checkpoint``).
            Signature: ``async def fn(label: str, *, trigger_span_id: str = "") -> None``.
        name: Stage name for the checkpoint label.
        step: Step number. Label becomes ``step.{N}.stage.{name}``.
        interval_s: If > 0, run periodic background checkpoints.
        file_triggers: Patterns to watch for.  A trigger server is
            auto-created and exposed via the yielded :class:`CheckpointContext`.
    """
    label = f"step.{step}.stage.{name}"
    checkpoint_lock = asyncio.Lock()
    bg_tasks: list[asyncio.Task[None]] = []

    # Auto-create trigger server when file triggers are configured
    trigger_server: CheckpointTriggerServer | None = None
    if file_triggers:
        trigger_server = CheckpointTriggerServer()
        await trigger_server.start()

    ctx = CheckpointContext(
        trigger_server=trigger_server,
        file_triggers=file_triggers or [],
    )

    if interval_s > 0:

        async def _periodic() -> None:
            counter = 0
            while True:
                await asyncio.sleep(interval_s)
                counter += 1
                async with checkpoint_lock:
                    try:
                        await fn(f"{label}.auto.{counter}")
                    except Exception:
                        logger.exception("background checkpoint failed")

        bg_tasks.append(asyncio.create_task(_periodic()))

    if trigger_server and file_triggers:
        # Build a lookup from pattern → debounce config
        trigger_map = {t.pattern: t for t in file_triggers}

        async def _watch_triggers() -> None:
            counter = 0
            while True:
                event = await trigger_server.wait()
                # Only trigger for events matching a configured pattern
                trigger = trigger_map.get(event.pattern)
                if trigger is None:
                    logger.debug("Ignoring trigger for unmatched pattern: %s", event.pattern)
                    continue
                debounce = trigger.debounce_s
                if debounce > 0:
                    await asyncio.sleep(debounce)
                    # Drain any events that arrived during debounce
                    latest = event
                    while True:
                        queued = trigger_server.try_get()
                        if queued is None:
                            break
                        if queued.pattern in trigger_map:
                            latest = queued
                    event = latest
                counter += 1
                async with checkpoint_lock:
                    try:
                        await fn(
                            f"{label}.file.{counter}",
                            trigger_span_id=event.span_id,
                        )
                    except Exception:
                        logger.exception("file-triggered checkpoint failed")

        bg_tasks.append(asyncio.create_task(_watch_triggers()))

    try:
        yield ctx
    finally:
        for task in bg_tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        if trigger_server:
            await trigger_server.stop()

    await fn(label)
