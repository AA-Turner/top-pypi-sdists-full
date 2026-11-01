"""Lane: a model or poller beside the writer, on its own asyncio task in the worker's event loop.
Variants live in lanes/ (ReaderLane, RunAlertLane, AuditLane); the worker stops each at session end."""

from __future__ import annotations

import asyncio
from typing import Protocol, runtime_checkable


@runtime_checkable
class Lane(Protocol):
    """What the worker holds of a lane: its task while it runs, and how it ends."""

    #: The lane's own task in the worker's loop; None before it starts and once it stopped.
    task: asyncio.Task | None

    async def run(self) -> object:
        """The lane's whole life, on its task."""
        ...

    async def stop(self) -> None:
        """Cancel the task and wait for it (the session is ending, or Probe left the daemon)."""
        ...
