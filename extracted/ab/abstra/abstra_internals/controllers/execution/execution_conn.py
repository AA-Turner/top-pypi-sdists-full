import threading
from typing import Any, Dict, List, Optional

from abstra_internals.controllers.execution.connection_protocol import (
    ConnectionProtocol,
)

_current_conn: Optional[ConnectionProtocol] = None
_stdio_buffer: Optional["StdioBuffer"] = None
_broadcast_publisher: Optional[Any] = None


def set_broadcast_publisher(publisher: Optional[Any]) -> None:
    global _broadcast_publisher
    _broadcast_publisher = publisher


def get_broadcast_publisher() -> Optional[Any]:
    return _broadcast_publisher


class StdioBuffer:
    """Buffers stdio messages and flushes them periodically as batches via RabbitMQ.

    Instead of one RabbitMQ publish per print(), messages are batched and sent
    every flush_interval seconds. This avoids blocking user code on network I/O
    and reduces RabbitMQ message volume by orders of magnitude.
    """

    def __init__(self, conn: ConnectionProtocol, flush_interval: float = 0.2):
        self._conn = conn
        self._flush_interval = flush_interval
        self._buffer: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread = threading.Thread(
            target=self._flush_loop, daemon=True, name="StdioBuffer-flush"
        )
        self._thread.start()

    def add(self, msg: Dict[str, Any]) -> None:
        with self._lock:
            self._buffer.append(msg)

    def _flush_loop(self) -> None:
        while not self._stop.wait(self._flush_interval):
            self._flush()

    def _flush(self) -> None:
        with self._lock:
            if not self._buffer:
                return
            batch = self._buffer[:]
            self._buffer.clear()

        message = {"type": "stdio_batch", "payload": batch}

        try:
            self._conn.send(message)
        except Exception:
            pass  # Don't break execution if broadcast fails

        try:
            publisher = _broadcast_publisher
            if publisher is not None:
                publisher.publish(message)
        except Exception:
            pass  # Don't break execution if broadcast fails

    def close(self) -> None:
        self._stop.set()
        self._thread.join(timeout=2.0)
        self._flush()  # Final flush for any remaining messages


def set_execution_conn(conn: Optional[ConnectionProtocol]) -> None:
    global _current_conn, _stdio_buffer

    if _stdio_buffer is not None:
        _stdio_buffer.close()
        _stdio_buffer = None

    _current_conn = conn

    if conn is not None:
        _stdio_buffer = StdioBuffer(conn)


def get_execution_conn() -> Optional[ConnectionProtocol]:
    return _current_conn


def get_stdio_buffer() -> Optional["StdioBuffer"]:
    return _stdio_buffer
