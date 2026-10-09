"""Define messages attached to workflow results."""

from .base import Base, LowercaseStrEnum


class MessageType(LowercaseStrEnum):
    """Message severity level."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class Message(Base):
    """User-facing message with severity, title, and body.

    Attributes:
        type: severity or category of the message
        title: short message heading
        body: message text
    """

    type: MessageType
    title: str
    body: str
