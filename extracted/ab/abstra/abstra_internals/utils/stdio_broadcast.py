import json
import threading
import time
from typing import Any, Dict, Optional, Tuple, Type

import pika
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.exceptions import AMQPError

from abstra_internals.logger import AbstraLogger

STDIO_BROADCAST_EXCHANGE = "stdio_broadcast"


class StdioBroadcastPublisher:
    """Publishes stdio messages to a RabbitMQ fanout exchange.

    Singleton per executor process. Thread-safe. Includes heartbeat thread
    and auto-reconnect on failure. All publish calls are best-effort:
    if RabbitMQ is down, messages are silently dropped (logs are already
    persisted to DB via insert_stdio).

    Note: task/execution:ended messages are forwarded via consume_and_forward
    in producer.py, not through this publisher.
    """

    _instance: Optional["StdioBroadcastPublisher"] = None
    _instance_lock = threading.Lock()

    @classmethod
    def get_or_create(
        cls,
        connection_uri: str,
        connection_factory: Optional[Type[BlockingConnection]] = None,
    ) -> "StdioBroadcastPublisher":
        with cls._instance_lock:
            if cls._instance is None or cls._instance._closed:
                cls._instance = cls(connection_uri, connection_factory)
            elif cls._instance._connection_uri != connection_uri:
                try:
                    cls._instance.close()
                except Exception:
                    pass
                cls._instance = cls(connection_uri, connection_factory)
            return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton (for tests)."""
        with cls._instance_lock:
            if cls._instance is not None:
                try:
                    cls._instance.close()
                except Exception:
                    pass
                cls._instance = None

    def __init__(
        self,
        connection_uri: str,
        connection_factory: Optional[Type[BlockingConnection]] = None,
    ):
        self._connection_uri = connection_uri
        self._connection_factory = connection_factory or pika.BlockingConnection
        self._connection: Optional[BlockingConnection] = None
        self._channel: Optional[BlockingChannel] = None
        self._lock = threading.Lock()
        self._closed = False
        self._heartbeat_stop = threading.Event()
        self._heartbeat_thread: Optional[threading.Thread] = None

        self._connect()
        self._start_heartbeat()

    def _connect(self) -> None:
        params = pika.URLParameters(self._connection_uri)
        params.connection_attempts = 1
        params.socket_timeout = 10
        params.blocked_connection_timeout = 10
        params.heartbeat = 30

        delay = 1.0
        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            try:
                self._connection = self._connection_factory(params)
                self._channel = self._connection.channel()
                self._channel.exchange_declare(
                    exchange=STDIO_BROADCAST_EXCHANGE,
                    exchange_type="fanout",
                    durable=True,
                )
                AbstraLogger.info(
                    "[StdioBroadcastPublisher] Connected and exchange declared"
                )
                return
            except Exception as e:
                if self._channel:
                    try:
                        self._channel.close()
                    except Exception:
                        pass
                    self._channel = None
                if self._connection:
                    try:
                        self._connection.close()
                    except Exception:
                        pass
                    self._connection = None

                if attempt < max_attempts:
                    AbstraLogger.warning(
                        f"[StdioBroadcastPublisher] Connection failed (attempt {attempt}): {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                    delay *= 2
                else:
                    AbstraLogger.error(
                        f"[StdioBroadcastPublisher] Failed to connect after {max_attempts} attempts: {e}"
                    )

    def _reconnect(self) -> bool:
        try:
            if self._channel:
                try:
                    self._channel.close()
                except Exception:
                    pass
            if self._connection:
                try:
                    self._connection.close()
                except Exception:
                    pass
            self._connect()
            return self._channel is not None and getattr(
                self._channel, "is_open", False
            )
        except Exception as e:
            AbstraLogger.error(f"[StdioBroadcastPublisher] Reconnect failed: {e}")
            return False

    def _start_heartbeat(self) -> None:
        def heartbeat_loop():
            while not self._heartbeat_stop.wait(timeout=10.0):
                try:
                    with self._lock:
                        if self._connection and getattr(
                            self._connection, "is_open", False
                        ):
                            self._connection.process_data_events(time_limit=0)
                except Exception as e:
                    if not self._closed:
                        AbstraLogger.debug(
                            f"[StdioBroadcastPublisher] Heartbeat error: {e}"
                        )

        self._heartbeat_thread = threading.Thread(
            target=heartbeat_loop,
            daemon=True,
            name="StdioBroadcastPublisher-Heartbeat",
        )
        self._heartbeat_thread.start()

    def publish(self, message: Dict[str, Any]) -> None:
        if self._closed:
            return

        try:
            body = json.dumps(message).encode("utf-8")
        except (TypeError, ValueError) as e:
            AbstraLogger.error(f"[StdioBroadcastPublisher] Serialization error: {e}")
            return

        with self._lock:
            for attempt in range(2):
                try:
                    if (
                        not self._connection
                        or getattr(self._connection, "is_closed", True)
                        or not self._channel
                        or getattr(self._channel, "is_closed", True)
                    ):
                        if not self._reconnect():
                            return

                    assert self._channel is not None
                    self._channel.basic_publish(
                        exchange=STDIO_BROADCAST_EXCHANGE,
                        routing_key="",
                        body=body,
                        properties=pika.BasicProperties(
                            delivery_mode=pika.DeliveryMode.Transient,
                            content_type="application/json",
                        ),
                    )
                    return
                except (AMQPError, Exception) as e:
                    if attempt == 0:
                        AbstraLogger.warning(
                            f"[StdioBroadcastPublisher] Publish failed, reconnecting: {e}"
                        )
                        self._reconnect()
                    else:
                        AbstraLogger.error(
                            f"[StdioBroadcastPublisher] Publish failed after retry: {e}"
                        )

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        self._heartbeat_stop.set()

        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            self._heartbeat_thread.join(timeout=2.0)

        try:
            if self._channel and getattr(self._channel, "is_open", False):
                self._channel.close()
        except Exception:
            pass
        try:
            if self._connection and getattr(self._connection, "is_open", False):
                self._connection.close()
        except Exception:
            pass


def start_stdio_broadcast_consumer(
    connection_uri: str,
    stop_event: Optional[threading.Event] = None,
) -> Tuple[threading.Thread, threading.Event]:
    """Start a daemon thread that consumes from stdio_broadcast fanout exchange
    and forwards messages to BroadcastController.

    Returns (thread, stop_event) so callers can stop the consumer cleanly.
    """
    if stop_event is None:
        stop_event = threading.Event()

    def consumer_loop():
        from abstra_internals.controllers.execution.execution_stdio import (
            BroadcastController,
        )
        from abstra_internals.utils import serialize

        delay = 2.0
        max_delay = 30.0

        while not stop_event.is_set():
            connection = None
            try:
                params = pika.URLParameters(connection_uri)
                params.connection_attempts = 1
                params.socket_timeout = 10
                params.blocked_connection_timeout = 10
                params.heartbeat = 30

                connection = pika.BlockingConnection(params)
                channel = connection.channel()

                channel.exchange_declare(
                    exchange=STDIO_BROADCAST_EXCHANGE,
                    exchange_type="fanout",
                    durable=True,
                )

                result = channel.queue_declare(queue="", exclusive=True)
                queue_name = result.method.queue
                channel.queue_bind(exchange=STDIO_BROADCAST_EXCHANGE, queue=queue_name)

                AbstraLogger.info(
                    f"[StdioBroadcastConsumer] Connected, bound to '{STDIO_BROADCAST_EXCHANGE}' "
                    f"with exclusive queue '{queue_name}'"
                )

                delay = 2.0

                for method, _, body in channel.consume(
                    queue=queue_name, auto_ack=True, inactivity_timeout=5.0
                ):
                    if stop_event.is_set():
                        break

                    if method is None:
                        continue

                    try:
                        message = json.loads(body.decode("utf-8"))
                        msg_type = message.get("type")

                        if msg_type == "stdio_batch":
                            for item in message.get("payload", []):
                                individual = {"type": "stdio", "payload": item}
                                BroadcastController.broadcast(msg=serialize(individual))

                        elif msg_type == "stdio":
                            BroadcastController.broadcast(msg=serialize(message))
                    except Exception as e:
                        AbstraLogger.error(
                            f"[StdioBroadcastConsumer] Error processing message: {e}"
                        )

            except Exception as e:
                if not stop_event.is_set():
                    AbstraLogger.error(
                        f"[StdioBroadcastConsumer] Connection error: {e}. "
                        f"Reconnecting in {delay}s..."
                    )
            finally:
                if connection:
                    try:
                        connection.close()
                    except Exception:
                        pass

            if not stop_event.is_set():
                stop_event.wait(delay)
                delay = min(delay * 2, max_delay)

    thread = threading.Thread(
        target=consumer_loop, daemon=True, name="StdioBroadcastConsumer"
    )
    thread.start()
    AbstraLogger.info("[StdioBroadcastConsumer] Consumer thread started")
    return thread, stop_event
