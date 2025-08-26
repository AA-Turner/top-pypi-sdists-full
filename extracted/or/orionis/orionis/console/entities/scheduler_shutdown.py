from dataclasses import dataclass, field
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class SchedulerShutdown(SchedulerEventData):
    """
    Represents an event triggered when the scheduler shuts down.

    This class is a specialized type of `SchedulerEventData` that is used to
    encapsulate information related to the shutdown of the scheduler.

    Attributes
    ----------
    (No additional attributes are defined in this class. It inherits all attributes
    from `SchedulerEventData`.)

    Returns
    -------
    SchedulerShutdown
        An instance of the `SchedulerShutdown` class representing the shutdown event.
    """
    time: str = ""                              # The time when the scheduler started
    tasks: list = field(default_factory=list)   # List of tasks scheduled at the time of start