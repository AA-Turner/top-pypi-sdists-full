from dataclasses import dataclass
from datetime import datetime
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class SchedulerResumed(SchedulerEventData):
    """
    Represents an event that is triggered when the scheduler is resumed.

    This data class extends `SchedulerEventData` and encapsulates
    information about the scheduler's resumption event.

    Attributes
    ----------
    time : str or datetime, optional
        The time when the scheduler was resumed. Can be a string or a datetime object.

    Returns
    -------
    SchedulerResumed
        An instance of `SchedulerResumed` containing information about the resumed scheduler event.
    """

    # The time when the scheduler was resumed; can be a string or datetime object
    time: str | datetime = None