from dataclasses import dataclass
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
    # This class does not define additional attributes or methods. It serves as a
    # specific type of event data for the scheduler shutdown event.