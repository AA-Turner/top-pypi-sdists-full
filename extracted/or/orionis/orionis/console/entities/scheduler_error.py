from dataclasses import dataclass
from typing import Optional
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class SchedulerError(SchedulerEventData):
    """
    Represents an error event triggered by the scheduler.

    This data class extends `SchedulerEventData` and is used to encapsulate
    information related to errors that occur during scheduler operations.
    It stores the exception that caused the error and the associated traceback
    for debugging and logging purposes.

    Attributes
    ----------
    exception : Optional[BaseException]
        The exception instance that caused the scheduler error, if any.
    traceback : Optional[str]
        The traceback string providing details about where the error occurred.

    Returns
    -------
    SchedulerError
        An instance containing details about the scheduler error event.
    """

    # Exception that caused the scheduler error, if present
    exception: Optional[BaseException] = None

    # Traceback information related to the scheduler error, if available
    traceback: Optional[str] = None