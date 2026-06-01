"""Messaging abstractions for publisher/consumer workflows.

This package intentionally provides broker-agnostic interfaces first.
Concrete adapters (for example RabbitMQ/Kafka) are expected to implement
these protocols in follow-up iterations.
"""

from ._types import Acknowledgement, Message, MessageConsumer, MessagePublisher

__all__ = ("Acknowledgement", "Message", "MessageConsumer", "MessagePublisher")
