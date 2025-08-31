from dataclasses import dataclass
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class SchedulerPaused(SchedulerEventData):
    """
    Represents an event triggered when the scheduler is paused.

    This data class extends `SchedulerEventData` and encapsulates information
    related to the scheduler pause event, such as the time at which the pause occurred.

    Attributes
    ----------
    time : str
        The time when the scheduler was paused, formatted as a string.
    (Other attributes are inherited from SchedulerEventData.)

    Returns
    -------
    SchedulerPaused
        An instance of SchedulerPaused containing information about the pause event.
    """

    # The time when the scheduler was paused
    time: str