"""Abstract message handler for RabbitMQ consumers."""

import logging
from abc import ABC, abstractmethod

from aio_pika.abc import AbstractIncomingMessage, HeadersType
from pydantic import TypeAdapter

from .._types import Message

logger = logging.getLogger(__name__)


class RabbitMessageHandler[T](ABC):
    """Base class for RabbitMQ message handlers.

    Subclass this and implement :meth:`handle_message` to process
    deserialized messages.  The handler is instantiated per queue by
    :class:`RabbitLifespan`.

    Parameters
    ----------
    message_type
        Pydantic model (or any ``TypeAdapter``-compatible type) used to
        validate the raw message body.
    """

    _type_adapter: TypeAdapter[T]

    def __init__(self, message_type: type[T] | None = None) -> None:
        if message_type is None:
            message_type = Message  # type: ignore[assignment]
        self._type_adapter = TypeAdapter(message_type)

    async def receive_message(self, message: AbstractIncomingMessage) -> None:
        """Deserialize and dispatch to :meth:`handle_message`."""
        parsed = self._type_adapter.validate_json(message.body)
        await self.handle_message(parsed, message.headers)

    @abstractmethod
    async def handle_message(self, message: T, headers: HeadersType) -> None:
        """Process a deserialized message.

        Implement this in your handler subclass.
        """
