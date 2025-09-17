from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class SchedulerError(SchedulerEventData):
    """
    Represents an error event triggered by the scheduler.

    This data class extends `SchedulerEventData` and encapsulates information about errors
    that occur during scheduler operations. It stores the exception that caused the error,
    the traceback for debugging, and the time the error occurred.

    Attributes
    ----------
    time : str or datetime, optional
        The time when the error occurred. Can be a string or a datetime object.
    exception : BaseException, optional
        The exception instance that caused the scheduler error, if any.
    traceback : str, optional
        The traceback string providing details about where the error occurred.

    Returns
    -------
    SchedulerError
        An instance containing details about the scheduler error event.
    """

    # The time when the error occurred (string or datetime)
    time: str | datetime = None

    # Exception that caused the scheduler error, if present
    exception: Optional[BaseException] = None

    # Traceback information related to the scheduler error, if available
    traceback: Optional[str] = None