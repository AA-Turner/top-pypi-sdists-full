"""Container for all values used in the automation."""
from enum import Enum


class _Constants:
    """Container for all values used in the automation."""

    BATCH_DESCRIPTION_NOT_FOUND = "A batch with the provided description was not found"

    class WORK_ITEM_PHASE(Enum):
        NOT_STARTED = "NOT_STARTED"
        IN_PROGRESS = "IN_PROGRESS"
        RETRY = "RETRY"
        IMPORTED = "IMPORTED"
        START_IMPORTING = "START_IMPORTING"


CONST = _Constants()
