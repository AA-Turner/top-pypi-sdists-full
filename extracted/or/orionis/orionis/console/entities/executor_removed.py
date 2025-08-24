from dataclasses import dataclass
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class ExecutorRemoved(SchedulerEventData):
    """
    Represents an event triggered when an executor is removed.

    This event is used to notify the system that a specific executor, identified 
    by its alias, has been removed from the scheduler.

    Attributes
    ----------
    alias : str
        The alias (unique identifier) of the removed executor.

    Returns
    -------
    None
        This class does not return a value; it is used as a data structure 
        to encapsulate event information.
    """

    # The alias of the removed executor
    alias: str