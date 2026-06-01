"""Low-level AMQP consumer with dead-letter and poison-message handling."""

import json
import logging
from contextlib import suppress
from typing import Any

from aio_pika import MessageProcessError
from aio_pika.abc import AbstractIncomingMessage
from pydantic import ValidationError

from ._handler import RabbitMessageHandler

logger = logging.getLogger(__name__)


class RabbitConsumer:
    """Wraps a :class:`RabbitMessageHandler` with ack/nack/reject logic.

    Handles:
    * JSON decode errors → reject (no requeue)
    * Validation errors → reject (no requeue)
    * Handler exceptions → reject (no requeue)
    * Poison-message detection via ``x-death`` headers
    * Safe fallback nack when nothing else handled the message
    """

    _handler: RabbitMessageHandler[Any]

    def __init__(self, handler: RabbitMessageHandler[Any]) -> None:
        self._handler = handler

    async def __call__(self, message: AbstractIncomingMessage) -> None:
        async with message.process(ignore_processed=True):
            handled = False

            if self._is_poison(message.headers or {}):
                logger.warning(
                    "Dropping poison message (rejected ≥5 times)",
                    extra={"message_id": message.message_id},
                )
                await message.ack()
                return

            try:
                logger.debug(
                    "Processing message",
                    extra={"message_id": message.message_id},
                )
                await self._handler.receive_message(message)
                await message.ack()
                handled = True

            except json.JSONDecodeError:
                logger.exception(
                    "Invalid JSON in message body",
                    extra={"message_id": message.message_id},
                )
                await self._reject_safely(message)
                handled = True

            except ValidationError:
                logger.exception(
                    "Message validation failed",
                    extra={"message_id": message.message_id},
                )
                await self._reject_safely(message)
                handled = True

            except Exception:
                logger.exception(
                    "Error processing message",
                    extra={"message_id": message.message_id},
                )
                await self._reject_safely(message)
                handled = True

            finally:
                if not handled:
                    await self._nack_safely(message)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    async def _nack_safely(message: AbstractIncomingMessage, *, requeue: bool = False) -> None:
        with suppress(MessageProcessError):
            await message.nack(requeue=requeue)

    @staticmethod
    async def _reject_safely(message: AbstractIncomingMessage) -> None:
        with suppress(MessageProcessError):
            await message.reject(requeue=False)

    @staticmethod
    def _is_poison(headers: dict[str, Any] | None) -> bool:
        """Check if a message has been rejected ≥5 times via ``x-death``."""
        if not headers:
            return False
        for death in headers.get("x-death", []):
            if death.get("reason") == "rejected" and death.get("count", 0) >= 5:
                return True
        return False
