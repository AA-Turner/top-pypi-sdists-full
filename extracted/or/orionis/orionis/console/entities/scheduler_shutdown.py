from dataclasses import dataclass, field
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class SchedulerShutdown(SchedulerEventData):
    """
    Represents an event triggered when the scheduler shuts down.

    This class extends `SchedulerEventData` and is used to encapsulate
    information related to the shutdown of the scheduler, such as the
    shutdown time and the list of tasks present at shutdown.

    Attributes
    ----------
    time : str
        The time when the scheduler was shut down.
    tasks : list
        The list of tasks that were scheduled at the time of shutdown.

    Returns
    -------
    SchedulerShutdown
        An instance representing the scheduler shutdown event, containing
        the shutdown time and the list of scheduled tasks.
    """

    # The time when the scheduler was shut down
    time: str = ""

    # List of tasks scheduled at the time of shutdown
    tasks: list = field(default_factory=list)