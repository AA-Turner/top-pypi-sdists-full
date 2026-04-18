import asyncio
import json
import threading
import time
from queue import Empty, Full, Queue
from typing import Any, Optional

import nats as nats_module
from nats.aio.client import RawCredentials

from abstra_internals.logger import AbstraLogger


class NATSPersistentConnection:
    """
    Persistent NATS connection. Created once per executor process,
    reused across all executions. Owns the TCP connection + asyncio event loop.
    """

    def __init__(self, nats_url: str, nats_creds: str):
        self.nats_url = nats_url
        self.nats_creds = nats_creds
        self._nc: Any = None
        self._closed = False

        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._run_loop, daemon=True, name="NATS-persistent"
        )
        self._thread.start()

        self._ready = threading.Event()
        self._connect_error: Optional[Exception] = None
        asyncio.run_coroutine_threadsafe(self._connect(), self._loop)

        if not self._ready.wait(timeout=10.0):
            self._stop_loop()
            raise TimeoutError("[NATSPersistentConnection] Connection timeout")
        if self._connect_error:
            self._stop_loop()
            raise self._connect_error

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    async def _connect(self):
        try:
            self._nc = await nats_module.connect(
                servers=self.nats_url,
                user_credentials=RawCredentials(self.nats_creds),
                max_reconnect_attempts=-1,
                reconnect_time_wait=1,
                ping_interval=30,
            )
            self._ready.set()
        except Exception as e:
            AbstraLogger.error(f"[NATSPersistentConnection] Connection failed: {e}")
            self._connect_error = e
            self._ready.set()

    def _stop_loop(self):
        """Stop the event loop and join the thread to avoid leaking resources."""
        try:
            self._loop.call_soon_threadsafe(self._loop.stop)
            self._thread.join(timeout=5.0)
        except Exception:
            pass

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @property
    def nc(self) -> Any:
        return self._nc

    @property
    def is_alive(self) -> bool:
        return not self._closed and self._nc is not None and not self._nc.is_closed

    def close(self):
        if self._closed:
            return
        self._closed = True
        try:
            if self._nc and not self._nc.is_closed:
                future = asyncio.run_coroutine_threadsafe(self._nc.close(), self._loop)
                future.result(timeout=5.0)
        except Exception as e:
            AbstraLogger.error(f"[NATSPersistentConnection] Error closing: {e}")
        self._stop_loop()


class NATSConnection:
    """
    Per-execution connection wrapper. Uses the shared NATSPersistentConnection
    for TCP, creates a per-execution subscription. Implements ConnectionProtocol.

    If no persistent connection is provided, creates its own (backward compatible).
    """

    def __init__(
        self,
        nats_url: str,
        nats_creds: str,
        send_subject: str,
        recv_subject: str,
        execution_id: str,
        persistent: Optional[NATSPersistentConnection] = None,
    ):
        self.send_subject = send_subject
        self.recv_subject = recv_subject
        self.execution_id = execution_id
        self._closed = False
        self._recv_buffer: Queue = Queue(maxsize=10000)
        self._sub: Any = None

        if persistent and persistent.is_alive:
            self._persistent = persistent
            self._owns_connection = False
        else:
            self._persistent = NATSPersistentConnection(nats_url, nats_creds)
            self._owns_connection = True

        self._setup_subscription()

    def _setup_subscription(self):
        future = asyncio.run_coroutine_threadsafe(
            self._subscribe(), self._persistent.loop
        )
        future.result(timeout=5.0)

    async def _subscribe(self):
        async def message_handler(msg):
            if self._closed:
                return
            try:
                data = msg.data.decode("utf-8")
                try:
                    parsed = json.loads(data)
                except json.JSONDecodeError:
                    parsed = data

                try:
                    self._recv_buffer.put_nowait(parsed)
                except Full:
                    try:
                        self._recv_buffer.get_nowait()
                    except Empty:
                        pass
                    try:
                        self._recv_buffer.put_nowait(parsed)
                    except Full:
                        pass
            except Exception as e:
                AbstraLogger.error(
                    f"[NATSConnection:{self.execution_id}] Error processing message: {e}"
                )

        self._sub = await self._persistent.nc.subscribe(
            self.recv_subject, cb=message_handler
        )

    def send(self, obj: Any):
        if self._closed:
            raise EOFError("Connection is closed")

        if isinstance(obj, str):
            data = obj.encode("utf-8")
        elif hasattr(obj, "dump") and callable(obj.dump):
            data = json.dumps(obj.dump()).encode("utf-8")
        else:
            try:
                data = json.dumps(obj).encode("utf-8")
            except (TypeError, ValueError):
                data = str(obj).encode("utf-8")

        future = asyncio.run_coroutine_threadsafe(
            self._persistent.nc.publish(self.send_subject, data),
            self._persistent.loop,
        )
        future.result(timeout=5.0)

    def recv(self, timeout: Optional[float] = None) -> Any:
        if self._closed:
            raise EOFError("Connection is closed")

        try:
            message = self._recv_buffer.get(timeout=timeout)
            if self._closed:
                raise EOFError("Connection is closed")
            return message
        except Empty:
            if self._closed:
                raise EOFError("Connection is closed")
            raise TimeoutError("No message received within timeout")

    def poll(self, timeout: float = 0.0) -> bool:
        if self._closed:
            return False

        if not self._recv_buffer.empty():
            return True

        if timeout <= 0:
            return False

        check_interval = 0.1
        elapsed = 0.0
        while elapsed < timeout:
            if self._closed:
                return False
            if not self._recv_buffer.empty():
                return True
            sleep_time = min(check_interval, timeout - elapsed)
            time.sleep(sleep_time)
            elapsed += sleep_time

        return not self._recv_buffer.empty()

    def close(self):
        if self._closed:
            return

        self._closed = True

        if self._sub:
            try:
                future = asyncio.run_coroutine_threadsafe(
                    self._sub.unsubscribe(), self._persistent.loop
                )
                future.result(timeout=2.0)
            except Exception:
                pass

        if self._owns_connection:
            self._persistent.close()

    @property
    def closed(self) -> bool:
        return self._closed
