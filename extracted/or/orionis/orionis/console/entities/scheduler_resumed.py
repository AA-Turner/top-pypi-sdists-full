from dataclasses import dataclass
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class SchedulerResumed(SchedulerEventData):
    """
    Represents an event triggered when the scheduler is resumed.

    This class is a specialized data structure that inherits from
    `SchedulerEventData` and is used to encapsulate information
    about the resumption of the scheduler.

    Attributes
    ----------
    (Inherited from SchedulerEventData)

    Returns
    -------
    SchedulerResumed
        An instance of the `SchedulerResumed` class representing
        the resumed scheduler event.
    """
    # No additional fields or methods are defined here, as this class
    # serves as a marker for the resumed scheduler event.