import asyncio
import bisect
import logging
import time
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from uuid import UUID

logger = logging.getLogger(__name__)


def _ensure_uuid(id: str | UUID) -> UUID:
    return UUID(id) if isinstance(id, str) else id


def stream_id_key(stream_id: str | bytes) -> tuple[int, int]:
    """Numeric order of a `<ms>-<seq>` stream id, for comparing resume cursors.

    Clients send `-` or a negative id such as `-1` to replay everything, so
    those sort first, and `<ms>` or `<ms>-*` to replay that whole millisecond.
    Raises ValueError for an id without a numeric `<ms>`.
    """
    if isinstance(stream_id, bytes):
        stream_id = stream_id.decode()
    if stream_id.startswith("-"):
        return (-1, -1)
    ms, _, seq = stream_id.partition("-")
    return int(ms), int(seq) if seq.isdigit() else -1


@dataclass
class Message:
    topic: bytes
    data: bytes
    id: bytes | None = None
    # Control messages only: server-generated explanation of an interrupt/rollback
    reason: str | None = None
    # Stored for replay, so a client can resume after its id.
    resumable: bool = False


class ContextQueue(asyncio.Queue):
    """Queue that supports async context manager protocol"""

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        # Clear the queue
        while not self.empty():
            try:
                self.get_nowait()
            except asyncio.QueueEmpty:
                break


THREADLESS_KEY = "no-thread"


class StreamManager:
    def __init__(self):
        self.queues = defaultdict(
            lambda: defaultdict(list)
        )  # Dict[str, List[asyncio.Queue]]
        self.control_keys = defaultdict(lambda: defaultdict())
        self.control_queues = defaultdict(lambda: defaultdict(list))
        self.thread_streams = defaultdict(list)

        self.message_stores = defaultdict(
            lambda: defaultdict(list[Message])
        )  # Dict[str, List[Message]]
        self._last_id = (0, -1)

    def _next_id(self) -> bytes:
        """Strictly increasing, as a resume replays only the ids above its cursor."""
        ms = int(time.time() * 1000)
        last_ms, last_seq = self._last_id
        self._last_id = (ms, 0) if ms > last_ms else (last_ms, last_seq + 1)
        return f"{self._last_id[0]}-{self._last_id[1]}".encode()

    def get_queues(
        self, run_id: UUID | str, thread_id: UUID | str | None
    ) -> list[asyncio.Queue]:
        run_id = _ensure_uuid(run_id)
        if thread_id is None:
            thread_id = THREADLESS_KEY
        else:
            thread_id = _ensure_uuid(thread_id)
        return self.queues[thread_id][run_id]

    def get_control_queues(
        self, run_id: UUID | str, thread_id: UUID | str | None
    ) -> list[asyncio.Queue]:
        run_id = _ensure_uuid(run_id)
        if thread_id is None:
            thread_id = THREADLESS_KEY
        else:
            thread_id = _ensure_uuid(thread_id)
        return self.control_queues[thread_id][run_id]

    def get_control_key(
        self, run_id: UUID | str, thread_id: UUID | str | None
    ) -> Message | None:
        run_id = _ensure_uuid(run_id)
        if thread_id is None:
            thread_id = THREADLESS_KEY
        else:
            thread_id = _ensure_uuid(thread_id)
        return self.control_keys.get(thread_id, {}).get(run_id)

    async def put(
        self,
        run_id: UUID | str | None,
        thread_id: UUID | str | None,
        message: Message,
        resumable: bool = False,
    ) -> None:
        run_id = _ensure_uuid(run_id)
        if thread_id is None:
            thread_id = THREADLESS_KEY
        else:
            thread_id = _ensure_uuid(thread_id)

        message.id = self._next_id()
        topic = message.topic.decode()
        if resumable:
            message.resumable = True
            self._drop_expired()
            self.message_stores[thread_id][run_id].append(message)
        if "control" in topic:
            self.control_keys[thread_id][run_id] = message
            queues = self.control_queues[thread_id][run_id]
        else:
            queues = self.queues[thread_id][run_id]
        coros = [queue.put(message) for queue in queues]
        results = await asyncio.gather(*coros, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                logger.exception(f"Failed to put message in queue: {result}")

    async def put_thread(
        self,
        thread_id: UUID | str,
        message: Message,
    ) -> None:
        thread_id = _ensure_uuid(thread_id)
        message.id = self._next_id()
        # Thread-level events (state updates) replay too, filed under the thread id.
        message.resumable = True
        self._drop_expired()
        self.message_stores[thread_id][thread_id].append(message)
        queues = self.thread_streams.get(thread_id, ())
        coros = [queue.put(message) for queue in queues]
        results = await asyncio.gather(*coros, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                logger.exception(f"Failed to put message in queue: {result}")

    async def add_queue(
        self, run_id: UUID | str, thread_id: UUID | str | None
    ) -> asyncio.Queue:
        run_id = _ensure_uuid(run_id)
        queue = ContextQueue()
        if thread_id is None:
            thread_id = THREADLESS_KEY
        else:
            thread_id = _ensure_uuid(thread_id)
        self.queues[thread_id][run_id].append(queue)
        return queue

    async def add_control_queue(
        self, run_id: UUID | str, thread_id: UUID | str | None
    ) -> asyncio.Queue:
        run_id = _ensure_uuid(run_id)
        if thread_id is None:
            thread_id = THREADLESS_KEY
        else:
            thread_id = _ensure_uuid(thread_id)
        queue = ContextQueue()
        self.control_queues[thread_id][run_id].append(queue)
        return queue

    async def add_thread_stream(self, thread_id: UUID | str) -> asyncio.Queue:
        thread_id = _ensure_uuid(thread_id)
        queue = ContextQueue()
        self.thread_streams[thread_id].append(queue)
        return queue

    async def remove_queue(
        self, run_id: UUID | str, thread_id: UUID | str | None, queue: asyncio.Queue
    ):
        run_id = _ensure_uuid(run_id)
        if thread_id is None:
            thread_id = THREADLESS_KEY
        else:
            thread_id = _ensure_uuid(thread_id)
        if thread_id in self.queues and run_id in self.queues[thread_id]:
            self.queues[thread_id][run_id].remove(queue)
            if not self.queues[thread_id][run_id]:
                del self.queues[thread_id][run_id]

    async def remove_thread_stream(self, thread_id: UUID | str, queue: asyncio.Queue):
        thread_id = _ensure_uuid(thread_id)
        if thread_id in self.thread_streams:
            self.thread_streams[thread_id].remove(queue)
            if not self.thread_streams[thread_id]:
                del self.thread_streams[thread_id]

    async def remove_control_queue(
        self, run_id: UUID | str, thread_id: UUID | str | None, queue: asyncio.Queue
    ):
        run_id = _ensure_uuid(run_id)
        if thread_id is None:
            thread_id = THREADLESS_KEY
        else:
            thread_id = _ensure_uuid(thread_id)
        if (
            thread_id in self.control_queues
            and run_id in self.control_queues[thread_id]
        ):
            self.control_queues[thread_id][run_id].remove(queue)
            if not self.control_queues[thread_id][run_id]:
                del self.control_queues[thread_id][run_id]

    def restore_messages(
        self, run_id: UUID | str, thread_id: UUID | str | None, message_id: str | None
    ) -> Iterator[Message]:
        """Get a stored message by ID for resumable streams."""
        run_id = _ensure_uuid(run_id)
        if thread_id is None:
            thread_id = THREADLESS_KEY
        else:
            thread_id = _ensure_uuid(thread_id)
        if message_id is None:
            return
        self._drop_expired()
        if thread_id not in self.message_stores:
            return
        try:
            after = stream_id_key(message_id)
        except ValueError:
            return
        # A copy: a write while the replay is sent can drop expired entries from the front.
        for message in list(self.message_stores[thread_id].get(run_id, ())):
            if stream_id_key(message.id) > after:
                yield message

    def _drop_expired(self) -> None:
        """Forget stored events older than the resumable TTL, as the Redis cache does."""
        from langgraph_api.config import RESUMABLE_STREAM_TTL_SECONDS  # noqa: PLC0415

        oldest_ms = int(time.time() * 1000) - RESUMABLE_STREAM_TTL_SECONDS * 1000
        for thread_id, runs in list(self.message_stores.items()):
            for run_id, messages in list(runs.items()):
                expired = bisect.bisect_left(
                    messages, oldest_ms, key=lambda m: stream_id_key(m.id)[0]
                )
                del messages[:expired]
                if not messages:
                    del runs[run_id]
            if not runs:
                del self.message_stores[thread_id]

    def get_queues_by_thread_id(self, thread_id: UUID | str) -> list[asyncio.Queue]:
        """Get all queues for a specific thread_id across all runs."""
        all_queues = []
        # Search through all stored queue keys for ones ending with the thread_id
        thread_id = _ensure_uuid(thread_id)
        if thread_id in self.queues:
            for run_id in self.queues[thread_id]:
                all_queues.extend(self.queues[thread_id][run_id])

        return all_queues


# Global instance
stream_manager = StreamManager()


async def start_stream() -> None:
    """Initialize the queue system.
    In this in-memory implementation, we just need to ensure we have a clean StreamManager instance.
    """
    global stream_manager
    stream_manager = StreamManager()


async def stop_stream() -> None:
    """Drop the run stream queues, control queues and stored stream messages."""
    # Sends no `done`: every request has ended or been cancelled by the time this
    # runs, and a thread stream would report a run cut short as finished.
    stream_manager.queues.clear()
    stream_manager.control_queues.clear()
    stream_manager.message_stores.clear()


def get_stream_manager() -> StreamManager:
    """Get the global stream manager instance."""
    return stream_manager
