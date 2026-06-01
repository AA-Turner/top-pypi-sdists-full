"""RabbitMQ adapter for csrd-message.

Provides a concrete RabbitMQ implementation of the broker-agnostic
``csrd.message`` protocols using ``aio-pika``.

Install with::

    pip install csrd-message[rabbit]

Usage::

    from csrd.message.rabbit import (
        RabbitPublisher,
        RabbitConsumer,
        RabbitLifespan,
        QueueConfig,
    )
"""

from ._config import QueueConfig
from ._consumer import RabbitConsumer
from ._handler import RabbitMessageHandler
from ._lifespan import RabbitLifespan
from ._publisher import RabbitPublisher
from ._state import AMQPState

__all__ = [
    "AMQPState",
    "QueueConfig",
    "RabbitConsumer",
    "RabbitLifespan",
    "RabbitMessageHandler",
    "RabbitPublisher",
]
