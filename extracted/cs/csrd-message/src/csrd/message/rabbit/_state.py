"""AMQP connection state shared across the application."""

from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractExchange,
    AbstractQueue,
)
from pydantic import BaseModel, ConfigDict


class AMQPState(BaseModel):
    """Runtime state containing the AMQP connection and declared resources."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    connection: AbstractConnection
    channel: AbstractChannel
    exchanges: dict[str, AbstractExchange] = {}
    queues: dict[str, AbstractQueue] = {}
