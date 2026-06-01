"""FastAPI lifespan manager for RabbitMQ connections.

Handles connection setup, dead-letter exchange wiring, queue declaration,
consumer startup, and graceful shutdown.
"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from uuid import uuid4

import aio_pika
from aio_pika.abc import (
    AbstractChannel,
    AbstractExchange,
    AbstractQueue,
    ExchangeType,
)
from fastapi import FastAPI

from ._config import QueueConfig
from ._constants import DEAD_LETTER_EXCHANGE, RETRY_EXCHANGE
from ._consumer import RabbitConsumer
from ._state import AMQPState

logger = logging.getLogger(__name__)


class RabbitLifespan:
    """FastAPI lifespan context manager for RabbitMQ.

    Establishes a robust connection, declares queues and dead-letter
    exchanges, wires up consumers, and tears everything down on shutdown.

    Parameters
    ----------
    connection_url
        AMQP connection string (e.g.
        ``amqp://guest:guest@rabbitmq:5672/``).
    queues
        Queue configurations to auto-declare on startup.
    prefetch_count
        Channel QoS prefetch count.
    """

    def __init__(
        self,
        connection_url: str,
        queues: list[QueueConfig] | None = None,
        *,
        prefetch_count: int = 100,
    ) -> None:
        if not connection_url:
            raise ValueError("RabbitMQ connection_url is required")
        self._connection_url = connection_url
        self._queues = queues or []
        self._prefetch_count = prefetch_count

    # ------------------------------------------------------------------
    # Lifespan entry point
    # ------------------------------------------------------------------

    @asynccontextmanager
    async def __call__(self, app: FastAPI) -> AsyncIterator[dict[str, object]]:
        """Connect, declare, consume, yield, then tear down."""
        logger.info("Connecting to RabbitMQ")

        connection = await aio_pika.connect_robust(
            url=f"{self._connection_url}?reconnect_interval=5&fail_fast=false",
            timeout=30,
        )
        channel = await connection.channel()

        if self._prefetch_count:
            await channel.set_qos(prefetch_count=self._prefetch_count)

        state = AMQPState(connection=connection, channel=channel)

        try:
            # Declare queues and wire consumers
            for config in self._queues:
                await self._declare_queue(state, config)

            # Expose state on app.state for dependency injection
            app.state.rabbit = state

            # Start consuming
            for config in self._queues:
                await self._start_consumer(state, config)

            logger.info("RabbitMQ ready — %d queue(s)", len(self._queues))
            yield {"rabbit": state}

        finally:
            logger.info("Shutting down RabbitMQ connection")
            await channel.close()
            await connection.close()
            logger.info("RabbitMQ connection closed")

    # ------------------------------------------------------------------
    # Queue declaration
    # ------------------------------------------------------------------

    async def _declare_queue(self, state: AMQPState, config: QueueConfig) -> None:
        """Declare exchange (and optionally queue + DLX wiring).

        When ``message_handler`` is ``None`` (publish-only), only the
        exchange is declared — no queue, no dead-letter infrastructure.
        """
        if config.message_handler is None:
            # Publish-only: just declare the exchange
            exchange = await state.channel.declare_exchange(
                name=config.exchange_name, durable=True, type=config.exchange_type
            )
            state.exchanges[config.exchange_name] = exchange
            logger.info("Declared exchange %s (publish-only)", config.exchange_name)
            return

        exchange, queue = await self._declare_dead_letter_backed_queue(
            channel=state.channel,
            config=config,
        )
        state.exchanges[config.exchange_name] = exchange
        state.queues[config.queue_name] = queue

        logger.info(
            "Declared queue %s on exchange %s",
            config.queue_name,
            config.exchange_name,
        )

    @staticmethod
    async def _declare_dead_letter_backed_queue(
        channel: AbstractChannel,
        config: QueueConfig,
    ) -> tuple[AbstractExchange, AbstractQueue]:
        """Declare an exchange + queue with dead-letter and retry wiring.

        Creates three exchanges:
        1. The primary exchange for the queue binding
        2. A dead-letter exchange for rejected messages
        3. A retry exchange that re-delivers after ``retry_interval`` ms

        And two queues:
        1. The primary queue (messages → DLX on reject)
        2. A dead-letter queue (DL messages → retry exchange after TTL)
        """
        # Ensure DLX/retry exchanges exist
        await channel.declare_exchange(
            name=DEAD_LETTER_EXCHANGE, durable=True, type=ExchangeType.TOPIC
        )
        await channel.declare_exchange(name=RETRY_EXCHANGE, durable=True, type=ExchangeType.TOPIC)

        # Primary exchange
        exchange = await channel.declare_exchange(
            name=config.exchange_name, durable=True, type=config.exchange_type
        )

        type_args = {"x-queue-type": config.queue_type} if config.queue_type else {}

        # Primary queue — rejected messages go to DLX
        primary_args = {
            **type_args,
            "x-dead-letter-exchange": DEAD_LETTER_EXCHANGE,
            "x-dead-letter-routing-key": config.queue_name,
        }
        queue = await channel.declare_queue(
            name=config.queue_name, durable=True, arguments=primary_args
        )

        # Dead-letter queue — messages retry after TTL
        dl_args = {
            **type_args,
            "x-dead-letter-exchange": RETRY_EXCHANGE,
            "x-dead-letter-routing-key": config.queue_name,
            "x-message-ttl": config.retry_interval,
        }
        dl_queue = await channel.declare_queue(
            f"{config.queue_name}-dl", durable=True, arguments=dl_args
        )

        # Bind primary queue to its exchange
        await queue.bind(config.exchange_name, routing_key=config.routing_key)
        # Bind primary queue to retry exchange (re-delivery after DL TTL)
        await queue.bind(RETRY_EXCHANGE, routing_key=config.queue_name)
        # Bind DL queue to DLX
        await dl_queue.bind(DEAD_LETTER_EXCHANGE, routing_key=config.queue_name)

        return exchange, queue

    # ------------------------------------------------------------------
    # Consumer startup
    # ------------------------------------------------------------------

    async def _start_consumer(self, state: AMQPState, config: QueueConfig) -> None:
        """Start consuming from a declared queue."""
        if config.message_handler is None:
            return

        queue = state.queues.get(config.queue_name)
        if queue is None:
            logger.error("Queue %s not found in state", config.queue_name)
            return

        handler = config.message_handler()
        consumer = RabbitConsumer(handler=handler)
        tag = self._consumer_tag(queue)

        await queue.consume(callback=consumer, consumer_tag=tag)
        logger.info("Consumer started on queue %s (tag=%s)", config.queue_name, tag)

    @staticmethod
    def _consumer_tag(queue: AbstractQueue) -> str:
        """Generate a unique consumer tag for management UI identification."""
        return f"csrd-{queue.name}-{uuid4()}"
