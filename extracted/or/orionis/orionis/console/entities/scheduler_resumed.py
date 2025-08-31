from dataclasses import dataclass
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class SchedulerResumed(SchedulerEventData):
    """
    Represents an event triggered when the scheduler is resumed.

    This data class extends `SchedulerEventData` and is used to encapsulate
    information about the scheduler's resumption event.

    Attributes
    ----------
    time : str
        The time when the scheduler was resumed.

    Returns
    -------
    SchedulerResumed
        An instance containing information about the resumed scheduler event.
    """

    # The time when the scheduler was resumed
    time: str