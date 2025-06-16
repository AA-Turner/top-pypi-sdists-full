from enum import Enum

class ActivityStatus(Enum):
    """
    Model activity statuses.
    PENDING -> STARTED -> Terminal(COMPLETED or FAILED)
    """

    PENDING = "pending"
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"
