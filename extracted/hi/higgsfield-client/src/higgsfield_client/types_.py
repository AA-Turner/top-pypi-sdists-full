from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict

AnyJSON = Dict[str, Any]
"""Type alias for JSON-like dictionary structures with string keys and any values."""


@dataclass
class Status:
    """
    This is an abstract base class used to represent the various states
    of a request. Use one of the concrete subclasses to represent
    specific status states.
    """
    pass


@dataclass
class Queued(Status):
    """
    Status indicating that a request is queued and waiting to be processed.

    This status means the request has been accepted but processing has not yet started.
    """
    pass


@dataclass
class InProgress(Status):
    """
    Status indicating that a request is currently being processed.
    """
    pass


@dataclass
class Completed(Status):
    """
    Status indicating that a request has been successfully completed.
    """
    pass


@dataclass
class Failed(Status):
    """
    Status indicating that a request has failed due to an error.
    """
    pass


@dataclass
class NSFW(Status):
    """
    Status indicating that a request was flagged as NSFW (Not Safe For Work) content.
    """
    pass


@dataclass
class Cancelled(Status):
    """
    Status indicating that a request was cancelled before processing started.

    Note: Requests that have already started processing cannot be cancelled.
    """
    pass


class StatusEnum(str, Enum):
    QUEUED = 'queued'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'
    NSFW = 'nsfw'
    CANCELED = 'canceled'
