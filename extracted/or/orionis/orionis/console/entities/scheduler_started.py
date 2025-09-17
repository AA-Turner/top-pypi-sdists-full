from dataclasses import dataclass
from datetime import datetime
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class SchedulerStarted(SchedulerEventData):
    """
    Represents the event data generated when the scheduler starts.

    This data class extends `SchedulerEventData` and encapsulates information about the scheduler's
    start event, such as the start time and the list of tasks scheduled at that moment.

    Parameters
    ----------
    time : str or datetime, optional
        The time when the scheduler started. Can be a string or a `datetime` object.
    tasks : list, optional
        The list of tasks that were scheduled at the time the scheduler started.

    Returns
    -------
    SchedulerStarted
        An instance of `SchedulerStarted` containing the scheduler start event data.
    """

    # The time when the scheduler started; can be a string or datetime object
    time: str | datetime = None