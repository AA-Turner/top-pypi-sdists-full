from dataclasses import dataclass, field
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class SchedulerStarted(SchedulerEventData):
    """
    Represents an event triggered when the scheduler starts running.

    This class is a data structure that inherits from `SchedulerEventData`
    and is used to encapsulate information about the scheduler's start event.

    Attributes
    ----------
    (No additional attributes are defined in this class; it inherits all attributes from `SchedulerEventData`.)

    Returns
    -------
    SchedulerStarted
        An instance of the `SchedulerStarted` class, representing the scheduler start event.
    """
    time: str = ""                              # The time when the scheduler started
    tasks: list = field(default_factory=list)   # List of tasks scheduled at the time of start