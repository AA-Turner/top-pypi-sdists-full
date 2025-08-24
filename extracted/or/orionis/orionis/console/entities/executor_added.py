from dataclasses import dataclass
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class ExecutorAdded(SchedulerEventData):
    """
    Represents an event triggered when an executor is added to the system.

    This event is used to notify that a new executor has been successfully added.

    Attributes
    ----------
    alias : str
        The unique alias or identifier of the added executor.

    Returns
    -------
    ExecutorAdded
        An instance of the ExecutorAdded event containing the alias of the added executor.
    """

    # The alias of the added executor, used to uniquely identify it
    alias: str
