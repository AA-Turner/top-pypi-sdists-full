from dataclasses import dataclass, field
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class SchedulerStarted(SchedulerEventData):
    """
    Represents the event data generated when the scheduler starts.

    This data class extends `SchedulerEventData` and encapsulates information
    about the scheduler's start event, such as the start time and the list of
    tasks scheduled at that moment.

    Attributes
    ----------
    time : str
        The time when the scheduler started.
    tasks : list
        The list of tasks that were scheduled at the time the scheduler started.

    Returns
    -------
    SchedulerStarted
        An instance containing the scheduler start event data.
    """

    # The time when the scheduler started
    time: str = ""

    # List of tasks scheduled at the time of start
    tasks: list = field(default_factory=list)