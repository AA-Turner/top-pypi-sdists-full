"""RabbitMQ publisher implementing the csrd.message.MessagePublisher protocol."""

import json
import logging

import aio_pika
from aio_pika.abc import AbstractExchange

from .._types import Message

logger = logging.getLogger(__name__)


class RabbitPublisher:
    """Publishes :class:`~csrd.message.Message` objects to a RabbitMQ exchange.

    Satisfies the :class:`~csrd.message.MessagePublisher` protocol.

    Parameters
    ----------
    exchange
        The exchange to publish to.
    default_routing_key
        Fallback routing key when ``message.key`` is not set.
    """

    def __init__(
        self,
        exchange: AbstractExchange,
        *,
        default_routing_key: str = "",
    ) -> None:
        self._exchange = exchange
        self._default_routing_key = default_routing_key

    async def publish(self, message: Message) -> None:
        """Publish a broker-agnostic ``Message`` to RabbitMQ.

        The ``message.payload`` is JSON-serialized as the body.
        ``message.headers`` are forwarded as AMQP headers.
        ``message.key`` is used as the routing key (falls back to
        ``default_routing_key``).
        ``message.message_id`` is set when present.
        """
        body = json.dumps(message.payload).encode()

        amqp_message = aio_pika.Message(
            body=body,
            content_type="application/json",
            headers=message.headers or {},
            message_id=message.message_id or "",
        )

        routing_key = message.key or self._default_routing_key

        await self._exchange.publish(
            amqp_message,
            routing_key=routing_key,
        )

        logger.debug(
            "Published message to %s with routing_key=%s",
            self._exchange.name,
            routing_key,
            extra={"message_id": message.message_id},
        )
