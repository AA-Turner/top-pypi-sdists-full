"""Queue and exchange configuration models."""

from aio_pika import ExchangeType
from pydantic import BaseModel, ConfigDict, Field

from ._handler import RabbitMessageHandler


class QueueConfig(BaseModel):
    """Configuration for a single queue/exchange/routing-key binding.

    Each ``QueueConfig`` declares one exchange, one queue, one routing key,
    and an optional handler.  Pass multiple ``QueueConfig`` objects to
    :class:`RabbitLifespan` to declare multiple queues.

    Parameters
    ----------
    exchange_name
        Name of the AMQP exchange.
    queue_name
        Name of the AMQP queue.
    routing_key
        Routing key for the queue → exchange binding.
    message_handler
        Handler class instantiated per queue on startup.  If ``None``,
        only the exchange is declared (publish-only mode — no queue,
        no dead-letter wiring, no consumer).
    exchange_type
        Exchange type (direct, topic, fanout, headers).
    queue_type
        RabbitMQ queue type (``"quorum"`` or ``"classic"``).
    retry_interval
        Dead-letter retry interval in milliseconds.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        arbitrary_types_allowed=True,
    )

    exchange_name: str = Field(..., description="Name of the exchange")
    queue_name: str = Field(..., description="Name of the queue")
    routing_key: str = Field(..., description="Routing key for queue binding")

    message_handler: type[RabbitMessageHandler] | None = Field(default=None)
    exchange_type: ExchangeType = Field(default=ExchangeType.DIRECT)
    queue_type: str | None = Field(default="quorum")
    retry_interval: int = Field(
        default=60_000, description="Retry interval in milliseconds", ge=1000
    )
