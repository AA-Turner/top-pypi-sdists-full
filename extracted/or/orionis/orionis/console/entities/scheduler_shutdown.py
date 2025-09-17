from dataclasses import dataclass
from datetime import datetime
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class SchedulerShutdown(SchedulerEventData):
    """
    Represents an event triggered when the scheduler shuts down.

    This dataclass extends `SchedulerEventData` and encapsulates information
    related to the shutdown of the scheduler, such as the shutdown time and
    the list of tasks present at shutdown.

    Attributes
    ----------
    time : str or datetime, optional
        The time when the scheduler was shut down. Can be a string or a datetime object.

    Returns
    -------
    SchedulerShutdown
        An instance of SchedulerShutdown containing the shutdown time and
        any additional event data inherited from SchedulerEventData.
    """

    # The time when the scheduler was shut down; can be a string or datetime object
    time: str | datetime = None
