from dataclasses import dataclass
from orionis.console.entities.scheduler_event_data import SchedulerEventData

@dataclass(kw_only=True)
class JobstoreAdded(SchedulerEventData):
    """
    Event triggered when a job store is added to the scheduler.

    This event is used to notify that a new job store has been successfully added to the scheduler. 
    It provides the alias of the added job store, which can be used to identify it.

    Attributes
    ----------
    alias : str
        The alias (name) of the added job store.

    Returns
    -------
    None
        This class does not return a value; it is used to encapsulate event data.
    """

    # The alias of the added job store
    alias: str
