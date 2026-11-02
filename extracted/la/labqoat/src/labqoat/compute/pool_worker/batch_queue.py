"""Bounded-latency grouping of independently accepted input envelopes."""

import asyncio
from dataclasses import dataclass, field

from labqoat.json_document import JsonDocument


@dataclass
class BatchQueue:
    """Emit a full batch immediately or a short batch at the oldest queued input's deadline."""

    maximum: int = 1
    wait_ms: int = 0
    queue: asyncio.Queue[tuple[float, JsonDocument] | None] = field(default_factory=asyncio.Queue)

    def put(self, item: JsonDocument | None) -> None:
        """Timestamp admission so queued inputs do not restart their batching window after a busy execution."""
        self.queue.put_nowait(None if item is None else (asyncio.get_running_loop().time(), item))

    async def take(self) -> list[JsonDocument]:
        """Count the latency window from the first input and never extend it for arriving peers."""
        first = await self.queue.get()
        if first is None:
            return []
        arrived, envelope = first
        batch = [envelope]
        deadline = arrived + self.wait_ms / 1000
        while len(batch) < self.maximum:
            remaining = deadline - asyncio.get_running_loop().time()
            try:
                item = (
                    self.queue.get_nowait()
                    if not self.queue.empty()
                    else await asyncio.wait_for(self.queue.get(), max(remaining, 0))
                )
            except TimeoutError:
                break
            if item is None:
                self.queue.put_nowait(None)
                break
            batch.append(item[1])
        return batch
