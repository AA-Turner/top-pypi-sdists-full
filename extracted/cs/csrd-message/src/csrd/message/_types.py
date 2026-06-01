from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Protocol


class Acknowledgement(StrEnum):
    """Consumer acknowledgement decision for a processed message."""

    ACK = "ack"
    RETRY = "retry"
    REJECT = "reject"


@dataclass(frozen=True, slots=True)
class Message:
    """Immutable transport-agnostic message envelope."""

    topic: str
    payload: dict[str, Any]
    key: str | None = None
    headers: dict[str, str] = field(default_factory=dict)
    message_id: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


class MessagePublisher(Protocol):
    """Protocol contract for outbound message publishing."""

    async def publish(self, message: Message) -> None: ...


class MessageConsumer(Protocol):
    """Protocol contract for inbound message consumption."""

    async def consume(self, message: Message) -> Acknowledgement: ...
