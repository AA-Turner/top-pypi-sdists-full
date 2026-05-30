import json
import threading
import time
from abc import ABC, abstractmethod
from multiprocessing import Pipe, Queue
from multiprocessing.connection import Connection
from queue import Empty
from typing import Optional
from uuid import uuid4

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPConnectionError

from abstra_internals.controllers.execution.connection_protocol import (
    ConnectionProtocol,
)
from abstra_internals.entities.execution_context import ClientContext, FormContext
from abstra_internals.environment import (
    NATS_CREDS,
    NATS_URL,
    PROCESS_TIMEOUT_SECONDS,
    RABBITMQ_CONNECTION_TIMEOUT_SECONDS,
    RABBITMQ_DEFAUT_EXCHANGE,
    RABBITMQ_EXECUTION_QUEUE,
    RABBITMQ_RETRY_INITIAL_DELAY_SECONDS,
    RABBITMQ_RETRY_MAX_ATTEMPTS,
    WORKER_LOG_TO_QUEUE,
)
from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.models import (
    ControlMessage,
    ControlQueueMessage,
    PreExecution,
    QueueMessage,
    StopAllExecutionsMessage,
    StopExecutionMessage,
)
from abstra_internals.utils import serialize
from abstra_internals.utils.nats_connection import NATSConnection
from abstra_internals.utils.rabbitmq_connection import RabbitMQConnection

CONSUMER_INACTIVITY_TIMEOUT = 600  # 10 minutes


class ProducerRepository(ABC):
    queue: Queue

    @abstractmethod
    def enqueue(
        self, stage_id: str, context: ClientContext, user_jwt: Optional[str] = None
    ) -> ConnectionProtocol:
        raise NotImplementedError()

    @abstractmethod
    def enqueue_fire_and_forget(
        self, stage_id: str, context: ClientContext, user_jwt: Optional[str] = None
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def enqueue_control(self, message: ControlMessage) -> ConnectionProtocol:
        raise NotImplementedError()

    def clear_queue(self) -> None:
        """Discard pending execution messages so no new executions start."""
        raise NotImplementedError()

    def consume_and_forward(self, conn: ConnectionProtocol, stage_id: str) -> None:
        """Start background consumer to forward worker messages to BroadcastController.
        Default: closes the connection (local editor uses file watchers)."""
        conn.close()


class LocalProducerRepository(ProducerRepository):
    def __init__(self, local_queue: Queue):
        self.queue = local_queue

    def enqueue(
        self, stage_id: str, context: ClientContext, user_jwt: Optional[str] = None
    ) -> Connection:
        execution_id = uuid4().__str__()

        parent_conn, child_conn = Pipe()

        preexecution = PreExecution(
            stage_id=stage_id,
            context=context,
            execution_id=execution_id,
            user_jwt=user_jwt,
        )

        self.queue.put(
            QueueMessage(
                preexecution=preexecution,
                delivery_tag=0,
                connection=child_conn,
            ),
        )

        return parent_conn

    def enqueue_fire_and_forget(
        self, stage_id: str, context: ClientContext, user_jwt: Optional[str] = None
    ) -> None:
        execution_id = uuid4().__str__()

        parent_conn, child_conn = Pipe()
        parent_conn.close()  # Not used in fire-and-forget — close to avoid fd leak

        preexecution = PreExecution(
            stage_id=stage_id,
            context=context,
            execution_id=execution_id,
            user_jwt=user_jwt,
        )

        self.queue.put(
            QueueMessage(
                preexecution=preexecution,
                delivery_tag=0,
                connection=child_conn,
            ),
        )

    def enqueue_control(self, message: ControlMessage) -> Connection:
        parent_conn, child_conn = Pipe()
        self.queue.put(
            ControlQueueMessage(
                message=message,
                delivery_tag=0,
                connection=child_conn,
            )
        )
        return parent_conn

    def clear_queue(self) -> None:
        while True:
            try:
                self.queue.get_nowait()
            except Empty:
                return
            except (OSError, ValueError):
                return


class RabbitMQProducerRepository(ProducerRepository):
    """
    Base RabbitMQ producer repository that works with any queue.
    Publishes execution requests to a specified queue and creates bidirectional
    communication channels for real-time interaction with workers.
    """

    def __init__(self, connection_uri: str, queue_name: str):
        self.connection_uri = connection_uri
        self.queue_name = queue_name
        AbstraLogger.info(
            f"[RabbitMQProducerRepository] Initialized with URI: {connection_uri}, Queue: {queue_name}"
        )

    @property
    def conn_params(self):
        params = pika.URLParameters(self.connection_uri)
        params.connection_attempts = 1  # Single attempt per retry iteration
        params.socket_timeout = RABBITMQ_CONNECTION_TIMEOUT_SECONDS
        params.blocked_connection_timeout = RABBITMQ_CONNECTION_TIMEOUT_SECONDS
        return params

    @property
    def props(self):
        return pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent,
            content_type="application/json",
        )

    def _connect_with_retry(self) -> pika.BlockingConnection:
        """
        Establish RabbitMQ connection with exponential backoff retry logic.
        Retries connection attempts with exponential backoff to handle
        transient network issues during pod startup.
        """
        delay = RABBITMQ_RETRY_INITIAL_DELAY_SECONDS
        last_exception = None

        for attempt in range(1, RABBITMQ_RETRY_MAX_ATTEMPTS + 1):
            try:
                AbstraLogger.info(
                    f"[RabbitMQProducerRepository] Connection attempt {attempt}/{RABBITMQ_RETRY_MAX_ATTEMPTS}"
                )
                connection = pika.BlockingConnection(self.conn_params)
                AbstraLogger.info(
                    "[RabbitMQProducerRepository] Connection established successfully"
                )
                return connection
            except AMQPConnectionError as e:
                last_exception = e
                if attempt < RABBITMQ_RETRY_MAX_ATTEMPTS:
                    AbstraLogger.warning(
                        f"[RabbitMQProducerRepository] Connection failed (attempt {attempt}): {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                    delay = min(delay * 2, 30)  # Exponential backoff, max 30s
                else:
                    AbstraLogger.error(
                        f"[RabbitMQProducerRepository] All {RABBITMQ_RETRY_MAX_ATTEMPTS} connection attempts failed with params {self.conn_params}"
                    )

        raise last_exception or AMQPConnectionError("Failed to connect to RabbitMQ")

    def enqueue(
        self, stage_id: str, context: ClientContext, user_jwt: Optional[str] = None
    ) -> ConnectionProtocol:
        execution_id = uuid4().__str__()

        preexecution = PreExecution(
            stage_id=stage_id,
            context=context,
            execution_id=execution_id,
            user_jwt=user_jwt,
        )

        is_form = isinstance(context, FormContext)

        nats_conn = None
        if NATS_URL and NATS_CREDS and not is_form:
            nats_conn = NATSConnection(
                nats_url=NATS_URL,
                nats_creds=NATS_CREDS,
                send_subject=f"{execution_id}.s2w",
                recv_subject=f"{execution_id}.w2s",
                execution_id=execution_id,
            )

        try:
            with self._connect_with_retry() as connection:
                with connection.channel() as channel:
                    channel: BlockingChannel
                    channel.queue_declare(queue=self.queue_name, durable=True)
                    channel.basic_publish(
                        body=preexecution.dump_json(),
                        routing_key=self.queue_name,
                        exchange=RABBITMQ_DEFAUT_EXCHANGE,
                        properties=self.props,
                    )
        except Exception:
            if nats_conn:
                nats_conn.close()
            raise

        if nats_conn:
            return nats_conn

        rabbitmq_connection = RabbitMQConnection(
            connection_uri=self.connection_uri,
            send_queue=f"server_to_worker_{execution_id}",
            recv_queue=f"worker_to_server_{execution_id}",
            execution_id=execution_id,
            auto_start_consumer=False,
        )

        return rabbitmq_connection

    def enqueue_control(self, message: ControlMessage) -> ConnectionProtocol:
        correlation_id = uuid4().__str__()

        enriched_message = message.model_copy(update={"correlation_id": correlation_id})

        with self._connect_with_retry() as connection:
            with connection.channel() as channel:
                channel: BlockingChannel
                channel.queue_declare(queue=self.queue_name, durable=True)
                channel.basic_publish(
                    body=enriched_message.dump_json(),
                    routing_key=self.queue_name,
                    exchange=RABBITMQ_DEFAUT_EXCHANGE,
                    properties=self.props,
                )

        rabbitmq_connection = RabbitMQConnection(
            connection_uri=self.connection_uri,
            send_queue=f"server_to_worker_{correlation_id}",
            recv_queue=f"worker_to_server_{correlation_id}",
            execution_id=correlation_id,
            auto_start_consumer=False,
        )

        return rabbitmq_connection

    def clear_queue(self) -> None:
        try:
            with self._connect_with_retry() as connection:
                with connection.channel() as channel:
                    channel: BlockingChannel
                    channel.queue_declare(queue=self.queue_name, durable=True)
                    channel.queue_purge(queue=self.queue_name)
        except Exception as e:
            AbstraLogger.warning(
                f"[RabbitMQProducerRepository] Failed to purge queue {self.queue_name}: {e}"
            )

    def enqueue_fire_and_forget(
        self, stage_id: str, context: ClientContext, user_jwt: Optional[str] = None
    ) -> None:
        conn = self.enqueue(stage_id, context, user_jwt)

        if WORKER_LOG_TO_QUEUE:
            AbstraLogger.warning(
                f"[Server] ABSTRA_WORKER_LOG_TO_QUEUE=true, keeping connection open "
                f"to receive worker logs (stage_id={stage_id})"
            )
            self.consume_and_forward(conn, stage_id)
        else:
            self._wait_and_close(conn, stage_id)

    def _wait_and_close(self, conn: ConnectionProtocol, stage_id: str) -> None:
        def target():
            try:
                if conn.poll(timeout=60.0):
                    conn.recv()
                else:
                    AbstraLogger.warning(
                        f"[enqueue_fire_and_forget] Timeout waiting for execution:started "
                        f"(stage_id={stage_id})"
                    )
            except Exception as e:
                AbstraLogger.error(
                    f"[enqueue_fire_and_forget] Error waiting for execution:started: {e}"
                )
            finally:
                conn.close()

        threading.Thread(target=target, daemon=True).start()

    def consume_and_forward(self, conn: ConnectionProtocol, stage_id: str) -> None:
        def target():
            from abstra_internals.controllers.execution.execution_stdio import (
                BroadcastController,
            )

            try:
                deadline = time.time() + PROCESS_TIMEOUT_SECONDS + 300
                last_message_time = time.time()

                while time.time() < deadline:
                    if time.time() - last_message_time > CONSUMER_INACTIVITY_TIMEOUT:
                        AbstraLogger.warning(
                            f"[consume_and_forward] No message for {CONSUMER_INACTIVITY_TIMEOUT}s, "
                            f"disconnecting (stage_id={stage_id})"
                        )
                        break

                    if conn.poll(timeout=1.0):
                        msg = conn.recv()
                        last_message_time = time.time()

                        # Normalize: parse string messages to dict
                        if isinstance(msg, str):
                            try:
                                msg = json.loads(msg)
                            except (json.JSONDecodeError, AttributeError):
                                continue

                        if isinstance(msg, dict):
                            msg_type = msg.get("type")
                            if msg_type in ("stdio", "stdio_batch", "task"):
                                # Fanout consumer handles broadcast
                                continue
                            if msg_type == "execution:ended":
                                execution_id = msg.get("execution_id")
                                if execution_id:
                                    BroadcastController.broadcast(
                                        msg=serialize(
                                            {
                                                "type": "execution:update",
                                                "payload": {
                                                    "execution_id": execution_id,
                                                },
                                            }
                                        )
                                    )
                                    break

                    if hasattr(conn, "closed") and conn.closed:
                        break
            except Exception as e:
                AbstraLogger.error(
                    f"[consume_and_forward] Error (stage_id={stage_id}): {e}"
                )
            finally:
                conn.close()

        threading.Thread(target=target, daemon=True).start()


class ProductionProducerRepository(RabbitMQProducerRepository):
    """Producer repository for production environment using 'executions' queue."""

    def __init__(self, connection_uri: str):
        super().__init__(connection_uri, RABBITMQ_EXECUTION_QUEUE)


class WebEditorProducerRepository(RabbitMQProducerRepository):
    """Producer repository for web editor using 'web_editor_executions' queue."""

    def __init__(self, connection_uri: str, queue_name: str = "web_editor_executions"):
        super().__init__(connection_uri, queue_name)


class WebEditorControlProducerRepository:
    """Producer repository for web editor control messages.
    Publishes to a fanout exchange so all workers receive broadcast messages."""

    def __init__(self, connection_uri: str):
        self.connection_uri = connection_uri
        self.exchange_name = "web_editor_control"

    @property
    def conn_params(self):
        params = pika.URLParameters(self.connection_uri)
        params.connection_attempts = 1
        params.socket_timeout = RABBITMQ_CONNECTION_TIMEOUT_SECONDS
        params.blocked_connection_timeout = RABBITMQ_CONNECTION_TIMEOUT_SECONDS
        return params

    @property
    def props(self):
        return pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent,
            content_type="application/json",
        )

    def _connect_with_retry(self) -> pika.BlockingConnection:
        delay = RABBITMQ_RETRY_INITIAL_DELAY_SECONDS
        last_exception = None

        for attempt in range(1, RABBITMQ_RETRY_MAX_ATTEMPTS + 1):
            try:
                return pika.BlockingConnection(self.conn_params)
            except AMQPConnectionError as e:
                last_exception = e
                if attempt < RABBITMQ_RETRY_MAX_ATTEMPTS:
                    AbstraLogger.warning(
                        f"[WebEditorControlProducerRepository] Connection failed (attempt {attempt}): {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                    delay = min(delay * 2, 30)

        raise last_exception or AMQPConnectionError("Failed to connect to RabbitMQ")

    def stop_execution(self, execution_id: str):
        payload = StopExecutionMessage.create(execution_id)

        with self._connect_with_retry() as connection:
            with connection.channel() as channel:
                channel: BlockingChannel
                channel.exchange_declare(
                    exchange=self.exchange_name,
                    exchange_type="fanout",
                    durable=True,
                )
                channel.basic_publish(
                    body=payload.dump_json(),
                    routing_key="",
                    exchange=self.exchange_name,
                    properties=self.props,
                )

    def stop_all_executions(self):
        payload = StopAllExecutionsMessage()

        with self._connect_with_retry() as connection:
            with connection.channel() as channel:
                channel: BlockingChannel
                channel.exchange_declare(
                    exchange=self.exchange_name,
                    exchange_type="fanout",
                    durable=True,
                )
                channel.basic_publish(
                    body=payload.dump_json(),
                    routing_key="",
                    exchange=self.exchange_name,
                    properties=self.props,
                )

    def restart_workers(self):
        """Broadcast restart message to all workers.
        Used after updating abstra version to ensure workers reload with new code."""
        payload = ControlMessage(type="restart")

        with self._connect_with_retry() as connection:
            with connection.channel() as channel:
                channel: BlockingChannel
                channel.exchange_declare(
                    exchange=self.exchange_name,
                    exchange_type="fanout",
                    durable=True,
                )
                channel.basic_publish(
                    body=payload.dump_json(),
                    routing_key="",
                    exchange=self.exchange_name,
                    properties=self.props,
                )
